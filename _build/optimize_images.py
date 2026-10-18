"""Create .webp copies of every JPG/PNG under public/assets (originals are kept).
Run: python3 _build/optimize_images.py   (needs Pillow with WebP support)"""
import pathlib
from PIL import Image
root = pathlib.Path(__file__).resolve().parent.parent / "assets"
SKIP = {"favicon-16.png", "favicon-32.png", "apple-touch-icon.png", "icon-192.png", "icon-512.png"}  # icons stay PNG
for p in sorted(list(root.rglob("*.jpg")) + list(root.rglob("*.png"))):
    if p.name in SKIP or p.name == "social-card.jpg":  # OG images must stay JPG/PNG for social sites
        continue
    out = p.with_suffix(".webp")
    im = Image.open(p)
    if p.suffix == ".png":
        im.save(out, "WEBP", quality=80, method=6, alpha_quality=90)  # keeps alpha
    else:
        im.convert("RGB").save(out, "WEBP", quality=60, method=6)
    if "photos" in p.parts or p.name == "service-area-map.jpg":
        # 800px-wide variant for phones (used via srcset)
        if im.width > 800:
            small = im.convert("RGB").resize((800, round(im.height * 800 / im.width)), Image.LANCZOS)
            small.save(p.with_name(p.stem + "-800.webp"), "WEBP", quality=60, method=6)
    print(f"{p.relative_to(root)}: {p.stat().st_size//1024} KB -> {out.stat().st_size//1024} KB")
