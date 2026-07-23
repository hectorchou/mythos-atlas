from PIL import Image
import os

d = r"C:\Users\Hector\Documents\lingxi-claw\20260704-13-50-36-390\mythos-atlas\mvp-site\public\images\entries"
ids = [
    "sekhmet-egypt",
    "bastet-egypt",
    "nut-egypt",
    "geb-egypt",
    "khonsu-egypt"
]

for name in ids:
    raw = os.path.join(d, name + "-raw.jpg")
    out = os.path.join(d, name + ".jpg")
    im = Image.open(raw).convert("RGB")
    if im.width > 1920:
        ratio = 1920 / im.width
        new_height = int(im.height * ratio)
        im = im.resize((1920, new_height), Image.LANCZOS)
    im.save(out, "JPEG", quality=72, optimize=True)
    size_kb = os.path.getsize(out) / 1024
    print(f"{name}.jpg: {size_kb:.1f} KB")
