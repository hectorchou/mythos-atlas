from PIL import Image
import pathlib
src = pathlib.Path("public/images/entries/generated_e0329b75.jpg")
img = Image.open(src).convert("RGB")
w,h = img.size
if w>1920:
    img = img.resize((1920,int(h*1920/w)), Image.LANCZOS)
out = pathlib.Path("public/images/entries/ezekiel-hebrew.jpg")
img.save(out,"JPEG",quality=72,optimize=True)
print(out.stat().st_size//1024,"KB")
