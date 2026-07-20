import pathlib, re
from collections import defaultdict
from difflib import get_close_matches

base = pathlib.Path("src/content/entries")

# 1. ID重复
id_map = defaultdict(list)
for p in sorted(base.glob('*.md')):
    text = p.read_text(encoding='utf-8')
    m = re.search(r'^id:\s*(.+)', text, re.M)
    if m:
        id_map[m.group(1).strip()].append(p.name)
    else:
        print(f'NO ID: {p.name}')

print('=== ID重复 ===')
for k,v in id_map.items():
    if len(v) > 1:
        print(f'  {k}: {v}')

# 2. name_primary重复
name_map = defaultdict(list)
for p in sorted(base.glob('*.md')):
    text = p.read_text(encoding='utf-8')
    m = re.search(r'^name_primary:\s*(.+)', text, re.M)
    if m:
        name_map[m.group(1).strip()].append(p.name)

print()
print('=== name_primary重复 ===')
for k,v in name_map.items():
    if len(v) > 1:
        print(f'  {k}: {v}')

# 3. 文件名高度相似
print()
print('=== 疑似重复文件名(相似度>85%) ===')
stems = [p.stem for p in base.glob('*.md')]
seen = set()
for s in sorted(stems):
    if s in seen: continue
    matches = get_close_matches(s, [x for x in stems if x not in seen], n=5, cutoff=0.85)
    if len(matches) > 1:
        for m in matches:
            seen.add(m)
        print(f'  {matches}')
