import pathlib, re

schema_fields = {
    'id','name_primary','name_original','name_aliases','name_translations',
    'hero_image','hero_image_alt','hero_image_credit',
    'culture_path','entity_type','era','geo_region','geo_coords',
    'summary','attributes','related_entries','parallel_motifs',
    'primary_sources','secondary_sources','confidence','first_recorded',
    'created_at','updated_at','curator','review_status','llm_assisted',
}

extra_fields = {}
for p in sorted(pathlib.Path('src/content/entries').glob('*.md')):
    text = p.read_text(encoding='utf-8')
    m = re.match(r'^---\n(.*?)\n---', text, re.DOTALL)
    if not m: continue
    fm = m.group(1)
    for line in fm.split('\n'):
        key = line.split(':')[0].strip()
        if key and key not in schema_fields:
            extra_fields.setdefault(key, []).append(p.stem)

print(f"Schema外字段总数: {sum(len(v) for v in extra_fields.values())}")
print()
for k,v in sorted(extra_fields.items(), key=lambda x: -len(x[1])):
    print(f'{k}: {len(v)} files')
    if len(v) <= 5:
        print(f'  -> {v}')
print()

# Check fields used but NOT in schema vs schema fields missing from files
print("=== Schema定义但文件从未使用的字段 ===")
used = set(extra_fields.keys())
all_keys = set()
for p in pathlib.Path('src/content/entries').glob('*.md'):
    text = p.read_text(encoding='utf-8')
    m = re.match(r'^---\n(.*?)\n---', text, re.DOTALL)
    if not m: continue
    for line in m.group(1).split('\n'):
        key = line.split(':')[0].strip()
        if key: all_keys.add(key)

for f in schema_fields:
    if f not in all_keys:
        print(f"  UNUSED: {f}")

print()
print("=== summary超280字符的文件数 ===")
over = 0
for p in pathlib.Path('src/content/entries').glob('*.md'):
    text = p.read_text(encoding='utf-8')
    m = re.search(r'^summary:\s*(.+)', text, re.M)
    if m and len(m.group(1)) > 280:
        over += 1
        if over <= 3:
            print(f"  {p.stem}: {len(m.group(1))}")
print(f"Total: {over}")
