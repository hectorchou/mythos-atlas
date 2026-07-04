# SOP-01 · 奠基作反向检索（Foundational Works Reverse Search）

> Mythos Atlas 项目文献检索规范 v1.0
> 建立日期：2026-07-04
> 触发原因：`east-asian-fox-cult` 词条首轮检索遗漏 Kang Xiaofei、Huntington、Smyers、Foster 四大英文学界奠基作

---

## 为什么需要这条 SOP

**问题**：主题式关键词检索（如 "cross-cultural fox"、"East Asian mythology"）**系统性地遗漏学科奠基作**——因为：

1. 奠基作被引用时通常用作者姓氏简称（"as Kang argues..."），全书标题反而不出现在关键词密集区
2. 奠基作发布时间往往较早（1990s-2000s 居多），SEO 权重低于近年论文
3. 搜索引擎更容易返回**引用了**奠基作的近期论文，而非奠基作本身
4. 中文/日文/韩文奠基作的英文关键词命中率极低

**后果**：如果只做主题式检索，词条会呈现"引用了大量二线论文，却漏掉了学科的核心权威"——这在学术出版中是**致命的可信度问题**。

---

## SOP 执行步骤（每个母题词条 / 每条深度词条完稿前必须执行）

### 第 1 步：识别学科归属
明确条目所属的学科主领域，例如：
- 中国民俗学 / 中国宗教史
- 日本妖怪学 / 神道研究
- 韩国民俗学 / 朝鲜文学
- 北欧萨迦研究 / 凯尔特神话学
- 中美洲民族志 / 玛雅研究

### 第 2 步：按学界列出该领域"必读作者"3-5 位

**建立 [foundational-authors 索引表](./FOUNDATIONAL-AUTHORS.md)（本项目累积维护）**，条目类型如下：

```
学科：中国狐仙研究（英文）
必读作者：
  - Kang Xiaofei（康笑菲）· George Washington University
  - Rania Huntington · University of Wisconsin
  - Leo Chan（次要）
关键代表作：
  - Kang: The Cult of the Fox (2005/06)
  - Huntington: Alien Kind (2003)
```

### 第 3 步：按作者姓名单独检索（不含主题关键词）

**关键**：直接检索 `作者姓 + 关键代表作简写`，避开主题词干扰。

例：
- ✅ `Kang Xiaofei Cult of the Fox`
- ✅ `Huntington Alien Kind Chinese fox`
- ✅ `Smyers Inari Fox Jewel`
- ❌ `Chinese fox spirit worship`（会命中大量二线论文，遗漏奠基作）

### 第 4 步：语种交叉验证

对于跨文化条目（如"东亚狐信仰"），必须**至少**检索三个语种的奠基作：

| 语种 | 常用检索平台 | 提示 |
|------|-------------|------|
| 英文 | Semantic Scholar / Google Scholar | 优先按作者姓 |
| 中文 | 万方数据 / NCPSSD | 优先按学者姓名 + "研究" |
| 日文 | J-STAGE / CiNii | 优先按学者名 + 领域词 |
| 韩文 | RISS / DBpia | 优先按学者名 + 主题 |

**遗漏语种 = 遗漏该文化本土学界的原初理论支撑**。

### 第 5 步：检索"学科综述文章"作为地图

搜 `"[主题]"+"研究综述" / "review" / "state of the art"` 类文章，这类文章通常**在引言部分密集罗列所有奠基作**，是识别遗漏的最快方式。

### 第 6 步：完稿前的自查清单

在词条 `secondary_sources` 字段完成后，回答以下 5 个问题，任何一个答"否"则必须回补：

- [ ] 该文化的**英文汉学/学界**前 3 位权威学者是否至少各引 1 篇？
- [ ] 该文化的**本土学界**（中/日/韩语学者）是否至少引 2 篇？
- [ ] 是否有**至少 1 部专著**（book/monograph 类型的 source）？
- [ ] 是否有**至少 1 篇发表在 SSCI / A&HCI / 核心期刊**的论文？
- [ ] 是否引用了**近 5 年**内的新研究，证明学术脉络仍在延续？

---

## 案例对比

### 反例：east-asian-fox-cult 词条第一轮（2026-07-04 上午）
- 主题式检索："cross-cultural fox"、"nine-tailed fox China Japan Korea"
- 结果：22 篇二线论文，**0 篇英文汉学奠基作**
- 疏漏率：约 **30%** 核心文献缺失

### 正例：east-asian-fox-cult 词条第二轮补搜（2026-07-04 晚间）
- 反向检索："Kang Xiaofei Cult of the Fox"、"Rania Huntington Alien Kind"、"Karen Smyers Inari Worship"、"Michael Dylan Foster Yokai"
- 结果：**6 篇奠基作**（Columbia UP / Harvard EAS / U of Hawai'i / UC Press / 日本本土）
- 文献总量翻倍，学术等级从"科普整理"升级为"学术综述基础"

---

## 已识别领域的奠基作者速查表（持续维护）

### 东亚

| 领域 | 英文学界奠基者 | 本土奠基者 |
|------|--------------|------------|
| 中国狐仙 | **Kang Xiaofei**, **Rania Huntington** | 李剑国 |
| 日本妖怪学 | **Michael Dylan Foster** | **小松和彦**, 柳田国男（历史）, 井上圆了（历史） |
| 稲荷信仰 | **Karen A. Smyers** | 直江広治 |
| 玉藻前研究 | Michael Bathgate | 田中貴子 |
| 韩国民俗学 | James H. Grayson | 崔仁鶴（최인학）, 임동권 |

### 西欧

| 领域 | 奠基者（待补） |
|------|--------------|
| 北欧萨迦研究 | Carolyne Larrington, Armann Jakobsson |
| 凯尔特民俗 | Ronald Black, John Francis Campbell（史料）|
| 英国民俗学 | Katharine Briggs, Jacqueline Simpson |

### 拉美

| 领域 | 奠基者（待补） |
|------|--------------|
| 玛雅研究 | Michael D. Coe, Allen J. Christenson, Karl Taube |
| 阿兹特克研究 | Bernardino de Sahagún（史料）, Miguel León-Portilla |
| La Llorona 研究 | Stephen Winick, María Herrera-Sobek |

**该表在每次新条目完成后必须回填新学到的奠基者姓名——项目积累的核心资产之一**。

---

## 长期意义

这条 SOP 是 Mythos Atlas 从"个人爱好整理"跨向"可作为学术资源被引用"的分水岭。

**没有反向检索的词条**：只是二手信息的重新组织
**有反向检索的词条**：等于把该主题在世界学界的"权威地图"复刻到你的知识库中，任何一位研究者进来都能一眼看出这条词条**接入了学界主脉**

未来所有类型为 `motif` 的伞形词条 + 任何深度超过 3000 字的具体词条，**必须完成 SOP-01 才能标记为 review_status: published**。
