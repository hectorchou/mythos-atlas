# Mythos Atlas · Entry Schema v0.1

> 一条记录 = 一个"神秘学实体"（神、妖、怪、事件、地点、仪式、传说母题）。
> 本规范是项目的 DNA，字段一旦确定，后续所有采集、录入、检索都围绕它展开。

---

## 一、核心原则

1. **一条记录只讲一个实体**：不要把"日本妖怪概述"塞进一条，要拆成"河童""天狗""座敷童子"等独立条目
2. **一手来源不可为空**：宁缺毋滥。没有可溯源的一手记载，条目不进库，进"待考"区
3. **文化归属是路径而非标签**：使用层级路径 `东亚/日本/民间信仰/水系妖怪`，而不是扁平标签
4. **可信度必须显式标注**：读者需要知道"这是学术共识"还是"这是 19 世纪某本志怪笔记的孤证"

---

## 二、字段定义

### 2.1 标识字段
| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `id` | string | ✅ | slug 格式，如 `kappa-japan-water` |
| `name_primary` | string | ✅ | 主名称，用原文化的通用称呼 |
| `name_original` | string | ✅ | 原文语言写法，如 `河童` `καππα` |
| `name_aliases` | string[] | ⭕ | 别称、方言称呼、罗马音 |
| `name_translations` | object | ⭕ | `{ "zh": "河童", "en": "Kappa" }` |

### 2.2 分类字段
| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `culture_path` | string | ✅ | 层级路径，如 `东亚/日本/民间信仰/水系妖怪` |
| `entity_type` | enum | ✅ | `deity` / `creature` / `spirit` / `event` / `place` / `ritual` / `motif`（母题） |
| `era` | string | ⭕ | 如 `平安时代` `19世纪` `前哥伦布时期` `年代不详` |
| `geo_region` | string | ⭕ | 地理范围，如 `日本关东` `北欧全境` |
| `geo_coords` | [lat,lng] | ⭕ | 有具体传说地点时填 |

### 2.3 内容字段
| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `summary` | string(≤280) | ✅ | 一句话摘要，用于列表/卡片展示 |
| `description` | markdown | ✅ | 完整描述，建议 300-800 字 |
| `attributes` | string[] | ⭕ | 特征标签：`两栖` `喜好相扑` `头顶有盘` |
| `related_entries` | id[] | ⭕ | 关联条目 id（用于图谱） |
| `parallel_motifs` | object[] | ⭕ | 跨文化对照：`[{entry_id: "kelpie-scotland", relation: "同为水系诱溺型妖怪"}]` |

### 2.4 溯源字段（**核心**）
| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `primary_sources` | Source[] | ✅ | 至少 1 条一手来源 |
| `secondary_sources` | Source[] | ⭕ | 二手研究/引用 |
| `confidence` | enum | ✅ | `attested`（学术共识）/ `documented`（有一手文献但争议）/ `folk`（口传为主）/ `speculative`（存疑） |
| `first_recorded` | string | ⭕ | 最早文献记载年代 |

**Source 对象结构**：
```yaml
- type: book | paper | manuscript | inscription | oral_record | news | archive
  title: "和汉三才图会"
  author: "寺岛良安"
  year: 1712
  language: ja
  location: "卷四十"           # 章节/页码
  url: "https://..."           # 深链到原文/扫描版/数据库
  access: open | paywall | offline
  retrieved_at: 2026-07-04
  note: "江户时代类书，收录河童条目最早的系统性图谱之一"
```

### 2.5 元数据字段
| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `created_at` | date | ✅ | 录入日期 |
| `updated_at` | date | ✅ | 最近更新 |
| `curator` | string | ✅ | 录入/审核人 |
| `review_status` | enum | ✅ | `draft` / `in_review` / `published` / `archived` |
| `llm_assisted` | bool | ✅ | 是否有 LLM 参与抽取（透明性） |

---

## 三、示例条目（YAML front-matter 格式）

```yaml
---
id: kappa-japan-water
name_primary: 河童
name_original: 河童（かっぱ）
name_aliases: [川太郎, 河伯, Kappa]
name_translations:
  zh: 河童
  en: Kappa
  ko: 갓파

culture_path: 东亚/日本/民间信仰/水系妖怪
entity_type: creature
era: 有文献记载始于江户时代，口传更早
geo_region: 日本全境，九州、关东记载最密集

summary: 日本民间信仰中栖息于河川池沼的两栖妖怪，头顶有盛水凹盘，力量与盘中水量相关。
attributes: [两栖, 头顶水盘, 喜好相扑, 拉马入水, 惧铁与猿]

primary_sources:
  - type: book
    title: 和汉三才图会
    author: 寺岛良安
    year: 1712
    language: ja
    location: 卷四十
    url: https://dl.ndl.go.jp/pid/2569722
    access: open
    note: 日本国立国会图书馆藏本，江户时代类书

  - type: book
    title: 遠野物語
    author: 柳田國男
    year: 1910
    language: ja
    location: 第55-59话
    url: https://www.aozora.gr.jp/cards/001566/files/52504_49667.html
    access: open

secondary_sources:
  - type: paper
    title: "Water Imps and Cultural Anxiety in Edo Japan"
    author: Foster, M. D.
    year: 2009
    language: en
    url: https://doi.org/xxxx

confidence: attested
first_recorded: 1712（《和汉三才图会》系统记载）

parallel_motifs:
  - entry_id: kelpie-scotland
    relation: 同为水系诱溺型妖怪，均有变形与拉人入水母题
  - entry_id: shuigui-china
    relation: 中国水鬼在东亚水系妖怪谱系中的对应位

curator: hector
review_status: draft
llm_assisted: true
created_at: 2026-07-04
updated_at: 2026-07-04
---

## 描述

河童是日本民间信仰中最广为人知的水系妖怪之一……（正文 markdown）
```

---

## 四、字段演进策略

- **v0.1（当前）**：先跑通 100 条录入，验证字段够不够用
- **v0.2**：根据实际录入痛点增删（预计增加"图像/插画"字段、"现代流行文化衍生"字段）
- **v1.0**：固定 schema，导出 JSON Schema 供 API 使用

**修改原则**：只增字段不删字段；删字段必须做数据迁移。
