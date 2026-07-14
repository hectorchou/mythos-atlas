import pathlib, re

schema_fields = {
    'id','name_primary','name_original','name_aliases','name_translations',
    'hero_image','hero_image_alt','hero_image_credit',
    'culture_path','entity_type','era','geo_region','geo_coords',
    'summary','attributes','related_entries','parallel_motifs',
    'primary_sources','secondary_sources','confidence','first_recorded',
    'created_at','updated_at','curator','review_status','llm_assisted',
}

custom_top = {}
total = len(list(pathlib.Path('src/content/entries').glob('*.md')))
for p in sorted(pathlib.Path('src/content/entries').glob('*.md')):
    text = p.read_text(encoding='utf-8')
    m = re.match(r'^---\n(.*?)\n---', text, re.DOTALL)
    if not m: continue
    for line in m.group(1).split('\n'):
        key = line.split(':')[0].strip()
        if key and key not in schema_fields:
            custom_top.setdefault(key, []).append(p.stem)

print(f"Total entries: {total}")
print()
print("Schema-external top-level YAML fields:")
for k,v in sorted(custom_top.items(), key=lambda x: -len(x[1])):
    pct = len(v)*100//total
    print(f"  {k}: {len(v)} files ({pct}%)")
