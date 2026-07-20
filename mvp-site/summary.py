import pathlib, os

base = pathlib.Path("C:/Users/Hector/Documents/lingxi-claw/20260704-13-50-36-390/mythos-atlas/mvp-site")

# 1. 词条
entries = ["elisha-hebrew","isaiah-hebrew","jeremiah-hebrew","ezekiel-hebrew","tsukuyomi-japan","toyouke-japan"]
print("=== 本次会话生成的词条 ===")
for e in entries:
    p = base / f"src/content/entries/{e}.md"
    if p.exists():
        print(f"  ✓ {e}.md ({p.stat().st_size//1024}KB)")

# 2. hero images (本会话生成)
heroes = entries.copy()
print("\n=== 本次会话生成的hero images ===")
for h in heroes:
    p = base / f"public/images/entries/{h}.jpg"
    if p.exists():
        print(f"  ✓ {h}.jpg ({p.stat().st_size//1024}KB)")

# 3. 补齐的21条hero image
filled = [
    "baba-yaga-south-slavic","cheoyong-korean","dazhbog-south-slavic","jumong-korean",
    "mokosh-south-slavic","morana-south-slavic","nanabozho-ojibwe","perun-south-slavic",
    "raven-trickster-pacific","rod-rozhanitsy-south-slavic","sami-mythology-corpus",
    "sanshin-korean","slavic-mythology-corpus","soma-vedic","spider-grandmother-hopi",
    "stribog-south-slavic","svarog-south-slavic","thunderbird-algonquian",
    "veles-south-slavic","wendigo-algonquian","korean-mythology-corpus",
]
print(f"\n=== 补齐的21条缺失hero image ===")
count = 0
for h in filled:
    p = base / f"public/images/entries/{h}.jpg"
    if p.exists():
        print(f"  ✓ {h}.jpg ({p.stat().st_size//1024}KB)")
        count += 1
print(f"  Total: {count}/21")

# 4. 基础设施
infra = ["validate.cjs","src/content/config.ts","package.json"]
print("\n=== 基础设施改动 ===")
for f in infra:
    p = base / f
    if p.exists():
        print(f"  ✓ {f} ({p.stat().st_size//1024}KB)")

# 5. 残留临时文件
print("\n=== 残留临时文件(未被清理) ===")
temp_files = []
for p in base.glob("*.py"):
    temp_files.append(p.name)
    print(f"  ⚠ {p.name}")
raw_count = len(list((base / "public/images/entries").glob("*-raw.jpg")))
print(f"  ⚠ public/images/entries/*-raw.jpg × {raw_count} files")

# 6. 统计
print("\n=== 站点整体统计 ===")
total_entries = len(list((base / "src/content/entries").glob("*.md")))
total_images = len(list((base / "public/images/entries").glob("*.jpg")))
img_size = sum(f.stat().st_size for f in (base / "public/images/entries").glob("*.jpg"))
print(f"  词条总数: {total_entries}")
print(f"  图片总数: {total_images} (含raw)")
print(f"  图片总大小: {img_size//1024//1024}MB")
