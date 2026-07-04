# 自动采集流水线架构 v0.1

> **设计原则**：采集器只负责"抓 + 筛 + 塞进收件箱"，绝不直接写入正式库。
> 所有条目必须经过人工审核这一关，这是产品价值的保证。

---

## 一、整体架构（收件箱模式）

```
┌─────────────────────────────────────────────────────────────┐
│                      SOURCES 数据源层                        │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐       │
│  │ Academic │ │   RSS    │ │ OpenAPI  │ │  Manual  │       │
│  │  APIs    │ │  Feeds   │ │  Scrape  │ │  Upload  │       │
│  │ CrossRef │ │ Fortean  │ │   NDL    │ │  (人工   │       │
│  │ OpenAlex │ │ Atlas Ob.│ │   ctext  │ │   补录)  │       │
│  │  arXiv   │ │ Reddit   │ │  SciELO  │ │          │       │
│  └────┬─────┘ └────┬─────┘ └────┬─────┘ └────┬─────┘       │
└───────┼────────────┼────────────┼────────────┼─────────────┘
        │            │            │            │
        ▼            ▼            ▼            ▼
┌─────────────────────────────────────────────────────────────┐
│                   FETCHER 采集层（定时）                     │
│    · 每类源一个 adapter（统一输出 RawItem 结构）             │
│    · 增量抓取（记录 last_seen 游标）                         │
│    · 失败重试 + 限流                                         │
└──────────────────────┬──────────────────────────────────────┘
                       ▼
              ┌─────────────────┐
              │  RAW INBOX      │  ← SQLite / Postgres 一张表
              │  (未处理原始)   │     status = raw
              └────────┬────────┘
                       ▼
┌─────────────────────────────────────────────────────────────┐
│                 FILTER 初筛层（LLM + 规则）                  │
│  1. 规则过滤：关键词命中、语言检测、去重（URL+title hash）   │
│  2. LLM 分类：is_relevant? + 建议 culture_path + entity_type │
│  3. 打相关性分 0-1，低于阈值丢弃                             │
└──────────────────────┬──────────────────────────────────────┘
                       ▼
              ┌─────────────────┐
              │  CANDIDATES     │  status = candidate
              │  (待抽取)       │
              └────────┬────────┘
                       ▼
┌─────────────────────────────────────────────────────────────┐
│              EXTRACTOR 抽取层（LLM 结构化）                  │
│  · 按 Schema v0.1 生成 draft 条目                            │
│  · 保留原文引用（source snippets）供人工核对                 │
│  · 自动补充别名翻译、跨文化对照建议                          │
└──────────────────────┬──────────────────────────────────────┘
                       ▼
              ┌─────────────────┐
              │  DRAFTS         │  status = draft
              │  (待审核)       │
              └────────┬────────┘
                       ▼
┌─────────────────────────────────────────────────────────────┐
│              REVIEW 人工审核层（永久环节）                   │
│  · 审核台 UI：并排显示原文 + LLM 草稿 + 编辑区              │
│  · 三选一：Publish / Revise / Reject                         │
│  · 审核人签名 + 时间戳                                       │
└──────────────────────┬──────────────────────────────────────┘
                       ▼
              ┌─────────────────┐
              │  PUBLISHED      │  → 静态站 build → 上线
              │  (正式条目)     │
              └─────────────────┘
```

---

## 二、模块清单与技术选型

| 模块 | 建议技术 | 说明 |
|------|---------|------|
| Fetcher | Python + `httpx` + `feedparser` | 每 source 一个 adapter 文件 |
| Scheduler | 系统 cron / GitHub Actions（免服务器） | Phase 1 用 cron 足够 |
| Storage | SQLite（Phase 1）→ PostgreSQL（Phase 2+） | 前期一个文件搞定 |
| LLM 调用 | DeepSeek API / Claude API | 初筛用便宜模型，抽取用强模型 |
| 去重 | `simhash` 或 URL 规范化 + title embedding | |
| 审核台 | Astro Admin 页面 / 简易 FastAPI + 单页 | Phase 2 才做 |
| 正式站 | Astro + Markdown Content Collections | 静态站，Git 即数据库 |
| 检索 | Pagefind（静态）→ Meilisearch（Phase 3） | |

---

## 三、Fetcher Adapter 统一接口

```python
# scripts/fetchers/base.py
from dataclasses import dataclass
from typing import Iterator

@dataclass
class RawItem:
    source_id: str          # 'crossref' / 'ndl' / 'fortean-rss'
    external_id: str        # DOI / URL / GUID
    title: str
    authors: list[str]
    abstract: str | None
    language: str
    published_at: str | None
    url: str
    raw_payload: dict       # 原始响应，全存下来备查

class BaseFetcher:
    source_id: str
    def fetch(self, since: str | None) -> Iterator[RawItem]: ...
```

**已规划的 adapter（Phase 2 优先级排序）**：
1. `crossref.py` — 关键词监听新论文（DOI 元数据）
2. `openalex.py` — CrossRef 补充，覆盖更全
3. `arxiv.py` — 数字人文相关
4. `rss_generic.py` — 通吃 Fortean Times / Atlas Obscura / Reddit RSS
5. `ndl.py` — 日本国会图书馆 API
6. `ctext.py` — 中国古籍全文（用于反向查询：某条目在哪本古籍出现过）
7. `scielo.py` — 拉美学术库

---

## 四、LLM Prompt 关键设计（骨架）

### 4.1 初筛 Prompt
```
输入：{title, abstract, source}
任务：判断这条内容是否属于"神秘学/民俗学/神话/超自然传说"研究范畴。
输出 JSON：
{
  "is_relevant": bool,
  "relevance_score": 0-1,
  "suggested_culture_path": "东亚/日本/..." | null,
  "suggested_entity_type": "creature|deity|..." | null,
  "reject_reason": string | null
}
```

### 4.2 抽取 Prompt（关键）
```
输入：原文全文（或摘要 + 一手来源URL）
任务：按 Schema v0.1 生成条目草稿。
硬约束：
- primary_sources 必须来自原文中明确引用的文献，不得编造
- 若无一手来源，直接输出 {"status": "insufficient_source"}
- 不确定的字段留空，不要臆测
- 引用的原文片段必须逐字复制到 source_snippets 字段
输出：符合 Schema v0.1 的 YAML
```

---

## 五、成本估算（Phase 2 稳态）

假设每周新增候选 500 条：
- 初筛（DeepSeek-chat）：500 × 500 tokens × ¥0.001/1k ≈ **¥0.25/周**
- 抽取（Claude Sonnet，仅通过初筛的 ~50 条）：50 × 3000 tokens × ¥0.02/1k ≈ **¥3/周**
- **月成本 < ¥15**，完全可承受

---

## 六、里程碑

- **M1**（第 4 周）：CrossRef + 2 个 RSS 跑通，SQLite 收件箱有数据
- **M2**（第 6 周）：初筛 LLM 接入，人工从收件箱能捞出候选
- **M3**（第 10 周）：抽取 LLM 接入，产出符合 Schema 的 draft
- **M4**（第 12 周）：审核台上线，闭环打通
