from PIL import Image
import pathlib

mapping = {
    "generated_b0f6360b.jpg": "baba-yaga-south-slavic.jpg",
    "generated_cbce4792.jpg": "cheoyong-korean.jpg",
    "generated_e7b7389b.jpg": "dazhbog-south-slavic.jpg",
    "generated_e03ca0ca.jpg": "jumong-korean.jpg",
    "generated_c1a72501.jpg": "mokosh-south-slavic.jpg",
    "generated_afc3a940.jpg": "morana-south-slavic.jpg",
    "generated_72f981fb.jpg": "nanabozho-ojibwe.jpg",
    "generated_69f7d52b.jpg": "perun-south-slavic.jpg",
    "generated_bbc6067b.jpg": "raven-trickster-pacific.jpg",
    "generated_843209fb.jpg": "rod-rozhanitsy-south-slavic.jpg",
    "generated_e27a5d23.jpg": "sami-mythology-corpus.jpg",
    "generated_99fd5aa1.jpg": "sanshin-korean.jpg",
    "generated_d45613fd.jpg": "slavic-mythology-corpus.jpg",
    "generated_9999bc16.jpg": "soma-vedic.jpg",
    "generated_02cfa776.jpg": "spider-grandmother-hopi.jpg",
    "generated_f97a4d26.jpg": "stribog-south-slavic.jpg",
    "generated_e19ef7f6.jpg": "svarog-south-slavic.jpg",
    "generated_ebca78d0.jpg": "thunderbird-algonquian.jpg",
    "generated_c66fa320.jpg": "veles-south-slavic.jpg",
    "generated_616f1cdd.jpg": "wendigo-algonquian.jpg",
    "generated_648a744d.jpg": "korean-mythology-corpus.jpg",
}

base = pathlib.Path("public/images/entries")
for src, dst in mapping.items():
    p = base / src
    if not p.exists():
        print(f"SKIP missing: {src}")
        continue
    img = Image.open(p).convert("RGB")
    w, h = img.size
    if w > 1920:
        img = img.resize((1920, int(h * 1920 / w)), Image.LANCZOS)
    out = base / dst
    img.save(out, "JPEG", quality=72, optimize=True)
    print(f"{dst}: {out.stat().st_size // 1024}KB")
