import os
import re

base = r"C:\Users\Hector\Documents\lingxi-claw\20260704-13-50-36-390\mythos-atlas\mvp-site\src\content\entries"
files = [
    "sekhmet-egypt.md",
    "bastet-egypt.md",
    "nut-egypt.md",
    "geb-egypt.md",
    "khonsu-egypt.md"
]

for f in files:
    p = os.path.join(base, f)
    with open(p, encoding="utf-8") as fi:
        t = fi.read()
    m = re.match(r"^(---\n.*?\n---\n)(.*)", t, re.S)
    if m:
        fm, body = m.group(1), m.group(2)
        def fix(match):
            c = match.group(0)
            c = c.replace('"', '')
            c = c.replace('=', '为')
            return c
        fm2 = re.sub(r'\[[^\]]*\]', fix, fm)
        # 还需要检查summary长度
        if 'summary:' in fm:
            summary_start = fm.index('summary:')
            next_field = [fm.index(k) for k in ['attributes:', 'primary_sources:'] if k in fm]
            if next_field:
                summary_end = min(next_field)
                summary = fm[summary_start + len('summary:'):summary_end].strip()
                if len(summary) > 230:
                    print(f"WARNING: {f} summary is {len(summary)} characters > 230")
                else:
                    print(f"OK: {f} summary is {len(summary)} characters")
        if fm2 != fm:
            print(f"Cleaned: {f}")
            with open(p, "w", encoding="utf-8") as fo:
                fo.write(fm2 + body)
        else:
            print(f"No changes needed: {f}")
    else:
        print(f"ERROR: Could not find YAML frontmatter in {f}")
