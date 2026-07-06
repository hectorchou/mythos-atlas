import re, pathlib

files = ["kinich-ahau-maya.md","ah-puch-maya.md","kawiil-maya.md","chilam-balam-maya.md","ek-chuah-maya.md","yum-kaax-maya.md"]
base = pathlib.Path("src/content/entries")

for fn in files:
    p = base / fn
    txt = p.read_text(encoding="utf-8")
    
    # Split into frontmatter and body
    parts = txt.split("---", 2)
    if len(parts) < 3:
        print(f"SKIP {fn}: no frontmatter")
        continue
    
    fm = parts[1]
    body = parts[2]
    
    # 1. Fix type: article -> paper, phd_thesis -> paper
    fm = fm.replace("type: article", "type: paper")
    fm = fm.replace("type: phd_thesis", "type: paper")
    
    # 2. Fix access: limited -> paywall
    fm = fm.replace("access: limited", "access: paywall")
    
    # 3. Remove created_at/updated_at from body (they were placed after ---)
    body = re.sub(r'\ncreated_at: "[^"]*"\nupdated_at: "[^"]*"\n*$', '\n', body)
    body = re.sub(r'\ncreated_at: "[^"]*"\nupdated_at: "[^"]*"', '', body)
    
    # 4. Add required fields to frontmatter if missing
    if "confidence:" not in fm:
        fm += 'confidence: documented\n'
    if "curator:" not in fm:
        fm += 'curator: hector\n'
    if "review_status:" not in fm:
        fm += 'review_status: draft\n'
    if "llm_assisted:" not in fm:
        fm += 'llm_assisted: true\n'
    if "created_at:" not in fm:
        fm += 'created_at: "2026-07-06"\n'
    if "updated_at:" not in fm:
        fm += 'updated_at: "2026-07-06"\n'
    
    # 5. Replace parallel_motifs with entry_id format
    # Remove the old parallel_motifs block and cross_culture_parallels
    # Find and remove parallel_motifs section (it's a list with motif/cultures/relation)
    # These fields are not in schema, so Zod will strip them - but let's clean them up
    # Actually, Zod strips unknown keys by default, so cross_culture_parallels and 
    # the old parallel_motifs format won't cause errors. But parallel_motifs IS in schema
    # with entry_id/relation format, so we need to fix that.
    
    # Find the parallel_motifs block in frontmatter and replace with proper format
    # The old format uses motif/cultures/relation keys
    # New format should use entry_id/relation
    
    # Actually, let me check - the old parallel_motifs in my files uses:
    # parallel_motifs:
    #   - motif: ...
    #     cultures: [...]
    #     relation: "..."
    # This won't match the schema's {entry_id, relation} format.
    # Since parallel_motifs is optional, let's just remove it from frontmatter
    # and keep cross_culture_parallels (which Zod will strip as unknown)
    
    # Remove parallel_motifs block from frontmatter
    # It starts with "parallel_motifs:" and goes until the next top-level key
    lines = fm.split('\n')
    new_lines = []
    skip = False
    for line in lines:
        if line.startswith("parallel_motifs:"):
            skip = True
            continue
        if skip:
            # Check if this line is a continuation (indented) or a new top-level key
            if line.startswith("  ") or line.startswith("\t") or line.strip() == "":
                continue
            else:
                skip = False
        if not skip:
            new_lines.append(line)
    fm = '\n'.join(new_lines)
    
    # Write back
    txt = "---" + fm + "---" + body
    p.write_text(txt, encoding="utf-8")
    print(f"fixed {fn}")

print("done")
