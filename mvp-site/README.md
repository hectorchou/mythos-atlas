# Mythos Atlas · MVP 静态站原型

## 技术栈
- **Astro** + Markdown Content Collections（Git 即数据库）
- 无后端、无 DB，条目就是一堆 `.md` 文件
- 部署到 Cloudflare Pages / Vercel（免费）

## 目录结构
```
mvp-site/
├── src/
│   ├── content/
│   │   ├── config.ts           # Schema 校验（Zod）
│   │   └── entries/            # 每条记录一个 .md 文件
│   │       ├── kappa-japan-water.md
│   │       └── ...
│   ├── layouts/
│   │   └── EntryLayout.astro
│   ├── components/
│   │   └── SourceList.astro
│   └── pages/
│       ├── index.astro         # 首页：按文化体系分区
│       ├── entries/[id].astro  # 详情页
│       └── cultures/[path].astro
├── astro.config.mjs
└── package.json
```

## 快速启动
```bash
cd mvp-site
npm install
npm run dev    # http://localhost:4321
```

## 录入一条新记录
1. 在 `src/content/entries/` 新建 `<id>.md`
2. 粘贴 Schema v0.1 的 YAML front-matter 模板
3. 填字段，写正文
4. `npm run dev` 立刻能看
5. `git commit` 就是版本历史

**注意**：本目录只是原型骨架，用于让你立刻开始录入。等录入到 30-50 条、字段规范验证过后，再考虑升级到带 DB 的方案。
