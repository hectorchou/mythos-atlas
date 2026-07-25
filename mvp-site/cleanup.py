import os, re

base = r"C:\Users\Hector\Documents\lingxi-claw\20260704-13-50-36-390\mythos-atlas\mvp-site\src\content\entries"
files = [
    "batara-guru-indonesian.md",
    "semar-indonesian.md",
    "hainuwele-indonesian.md",
    "mulajadi-nabolon-indonesian.md",
    "sawerigading-indonesian.md"
]

# Step 1: Check summary length
print("=== Summary Length Check ===")
for f in files:
    p = os.path.join(base, f)
    with open(p, encoding="utf-8") as fh:
        content = fh.read()
    m = re.search(r"^summary:\s*(.+)$", content, re.MULTILINE)
    if m:
        summary = m.group(1)
        status = "OK" if len(summary) <= 230 else "TOO LONG!"
        print(f"{f}: summary len={len(summary)} {status}")
    else:
        print(f"{f}: NO SUMMARY FOUND!")

# Step 2: Clean YAML flow lists
print("\n=== YAML Flow List Cleaning ===")
for f in files:
    p = os.path.join(base, f)
    with open(p, encoding="utf-8") as fh:
        t = fh.read()
    m = re.match(r"^(---\n.*?\n---\n)(.*)", t, re.S)
    if not m:
        print(f"{f}: Invalid YAML format!")
        continue
    fm, body = m.group(1), m.group(2)
    def fix(match):
        c = match.group(0)
        c = c.replace('"', "'").replace('"', "'").replace("=", "为")
        return c
    fm2 = re.sub(r"\[[^\]]*\]", fix, fm)
    if fm2 != fm:
        open(p, "w", encoding="utf-8").write(fm2 + body)
        print(f"{f}: cleaned")
    else:
        print(f"{f}: no changes needed")