# Mythos Atlas · 世界神话与神秘学谱系

> 结构化、可溯源、跨文化对照的世界神秘学谱系数据库。

## 项目定位

- 不是猎奇聚合，不是二手转载
- 每条记录必须挂接到一手文献来源（书目 / 论文 / 档案 / 口传采集）
- 按文化体系（Culture Path）层级归类，而非扁平标签
- 强调跨文化母题对照：同一母题在不同文化中的三极分化

## 当前进度（Phase 0 · Seed Content）

- **10 条种子条目**，覆盖三大文化体系
- **东亚**：河童 / 水鬼 / 天狗 / 狐妖（中）/ 稻荷狐（日）/ 九尾狐（韩）
- **西欧**：Kelpie / Draugr
- **拉美**：Xibalba / La Llorona

首个完整的跨文化谱系："东亚狐信仰三国分化" 已闭环。

## 目录结构

```
mythos-atlas/
├── schema/          # 数据字段规范（Entry Schema v0.1）
├── sources/         # 一手资料源清单
├── docs/            # 采集流水线架构等设计文档
├── mvp-site/        # Astro 静态站
│   └── src/content/entries/  # 每条记录一个 .md 文件
└── .github/workflows/deploy.yml  # GitHub Pages 自动部署
```

## 本地开发

```bash
cd mvp-site
npm install
npm run dev    # http://localhost:4321
npm run build
```

## 录入新条目

1. 参考 `schema/entry-schema-v0.1.md`
2. 在 `mvp-site/src/content/entries/` 新建 `<id>.md`
3. 按 YAML front-matter 格式填字段
4. `primary_sources` 至少 1 条不可省略
5. 深度词条 / 母题伞形词条 发布前必须完成 [SOP-01: 奠基作反向检索](./docs/SOP-01-foundational-works-reverse-search.md)
6. 提交 PR

## 项目规范

- [SOP-01 · 奠基作反向检索](./docs/SOP-01-foundational-works-reverse-search.md) — 防止遗漏学科权威文献的检索方法学
- [奠基学者索引表](./docs/FOUNDATIONAL-AUTHORS.md) — 各文化学科必读作者名单（持续维护）
- [字段规范 Schema v0.2](./schema/entry-schema-v0.1.md)
- [采集流水线架构](./docs/pipeline-architecture.md)

## Roadmap

- **Phase 0**（当前）：10 条种子内容 + MVP 静态站
- **Phase 1**（1-3 月）：手工扩充至 150 条，验证 schema
- **Phase 2**（4-8 月）：接入 LLM 采集流水线（CrossRef / RSS / arXiv）
- **Phase 3**（9-12 月）：关系图谱可视化 + 月度简报
- **Phase 4**（13-18 月）：可持续运营模式

## License

内容 CC BY-SA 4.0 · 代码 MIT
