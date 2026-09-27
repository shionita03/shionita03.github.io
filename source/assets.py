"""Image pipeline: resize + WebP encode + base64. Pure: path in, data URI out."""
import base64, io, os
HERE = os.path.dirname(os.path.abspath(__file__))
from PIL import Image

SRC = {"p": os.path.join(HERE, "img", "port", "p-{:03d}.png"), "d": os.path.join(HERE, "img", "doc", "d-{:03d}.png"), "photo": os.path.join(HERE, "img", "port", "p-{:03d}.png"), "t": os.path.join(HERE, "img", "ta", "t-{:03d}.png")}
_stats = {"count": 0, "bytes": 0}
USED = set()
# Gambar spreadsheet kecil: potong ke bagian penting lalu perbesar 2x agar teks tajam saat ditampilkan penuh.
PREP = {"d6": dict(crop=(0, 0, 960, 690), scale=2), "d7": dict(crop=(0, 0, 700, 464), scale=2)}

def _open(key):
    kind, num = ("photo", 0) if key.startswith("photo") else (key[0], int(key[1:]))
    im = Image.open(SRC[kind].format(num)).convert("RGB")
    p = PREP.get(key)
    if p:
        from PIL import ImageFilter
        im = im.crop(p["crop"])
        im = im.resize((im.width * p["scale"], im.height * p["scale"]), Image.LANCZOS).filter(ImageFilter.UnsharpMask(radius=1.2, percent=60, threshold=2))
    return im

def data_uri(key: str, max_w: int = 2000, q: int = 90) -> str:
    USED.add(key)
    im = _open(key)
    if max_w <= 400:  # logo: buang margin putih agar logo tampil penuh
        from PIL import ImageOps, ImageChops
        bg = Image.new("RGB", im.size, (255, 255, 255))
        box = ImageChops.difference(im, bg).convert("L").point(lambda v: 255 if v > 18 else 0).getbbox()
        if box: im = ImageOps.expand(im.crop(box), border=max(4, (box[2]-box[0])//25), fill="white")
    if im.width > max_w:
        im = im.resize((max_w, round(im.height * max_w / im.width)), Image.LANCZOS)
    buf = io.BytesIO(); im.save(buf, "WEBP", quality=q, method=6)
    _stats["count"] += 1; _stats["bytes"] += buf.tell()
    return "data:image/webp;base64," + base64.b64encode(buf.getvalue()).decode()

def stats(): return dict(_stats)

FULL_WIDTH = set(PREP) | {"d2"}

def aspect(key: str) -> float:
    if key in FULL_WIDTH: return 99.0  # selalu satu baris penuh
    w, h = _open(key).size
    return w / h
