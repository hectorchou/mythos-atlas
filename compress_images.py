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
    # Try different quality levels to get 200-380KB
    quality = 72
    im.save(out, "JPEG", quality=quality, optimize=True)
    file_size = os.path.getsize(out) / 1024
    print(f"{name}.jpg: {file_size:.1f} KB at quality {quality}")
    if file_size < 200:
        # Increase quality if too small
        quality = 85
        im.save(out, "JPEG", quality=quality, optimize=True)
        file_size = os.path.getsize(out) / 1024
        print(f"  Increased to quality {quality}: {file_size:.1f} KB")
    elif file_size > 380:
        # Decrease quality if too big
        quality = 60
        im.save(out, "JPEG", quality=quality, optimize=True)
        file_size = os.path.getsize(out) / 1024
        print(f"  Decreased to quality {quality}: {file_size:.1f} KB")
