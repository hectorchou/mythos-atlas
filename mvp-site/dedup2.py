import pathlib, re

base = pathlib.Path("src/content/entries")

# 需要人工确认的疑似重复对
pairs = [
    ("stribo-south-slavic", "stribog-south-slavic"),
    ("tawaret-egypt", "taweret-egypt"),
    ("amesha-spenta-zoroastrian", "amesha-spentas-zoroastrian"),
    ("gshen-rab-mibo-bon", "shenrab-miwo-bon"),
    ("druj-nasu-zoroastrian", "druj-zoroastrian"),
    ("serket-egypt", "selket-egypt"),
    ("weret-hekau-egypt", "werethekau-egypt"),
    ("samshin-korean", "sanshin-korean"),
    ("volos-south-slavic", "veles-south-slavic"),
    ("adad-mesopotamian", "adapa-mesopotamian"),
]

for a, b in pairs:
    fa = base / f"{a}.md"
    fb = base / f"{b}.md"
    if not fa.exists() or not fb.exists():
        print(f"SKIP (file missing): {a} vs {b}")
        continue
    ta = fa.read_text(encoding='utf-8')
    tb = fb.read_text(encoding='utf-8')
    ma = re.search(r'^name_primary:\s*(.+)', ta, re.M)
    mb = re.search(r'^name_primary:\s*(.+)', tb, re.M)
    sa = re.search(r'^summary:\s*(.+)', ta, re.M)
    sb = re.search(r'^summary:\s*(.+)', tb, re.M)
    print(f"--- {a} vs {b} ---")
    print(f"  A: {ma.group(1).strip() if ma else '?'}")
    print(f"     {sa.group(1).strip()[:120] if sa else '?'}...")
    print(f"  B: {mb.group(1).strip() if mb else '?'}")
    print(f"     {sb.group(1).strip()[:120] if sb else '?'}...")
    # content similarity
    body_a = re.sub(r'^---.*?---', '', ta, flags=re.DOTALL)[:2000]
    body_b = re.sub(r'^---.*?---', '', tb, flags=re.DOTALL)[:2000]
    from difflib import SequenceMatcher
    ratio = SequenceMatcher(None, body_a, body_b).ratio()
    print(f"  正文相似度: {ratio:.1%}")
    print()
