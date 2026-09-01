#!/usr/bin/env python3
"""Crop, resize and compress the client's photographs into the site's image slots.

Each slot has a fixed aspect ratio the layout is already built around, so the
crop happens here rather than at render time: the CSS uses object-fit: cover,
which would otherwise silently eat whichever edge it liked.

`bias` picks what survives the crop — 0.5 is centred, lower keeps the left or
top, higher the right or bottom. It is set per image by what is actually in
the frame, not by a rule.

Run: python3 tools/prepare-photos.py
"""
import os

from PIL import Image, ImageOps

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, '..', 'assets', 'brand', 'photo-originals')
OUT = os.path.join(HERE, '..', 'assets', 'img', 'photos')
MAP_OUT = os.path.join(HERE, '..', 'assets', 'img')

QUALITY = 78

# Width is set by how large the slot ever renders, not by the source: a
# half-column figure never needs more than ~1200px even on a 2x display,
# and every extra pixel is bytes a visitor pays for.
# slot -> (source file, target ratio, bias, max width, note)
SLOTS = [
    ('hero.jpg',          'hero-wide.png',    2400 / 1250, 0.50, 1510,
     'Home hero, tablet and desktop. Machine right, quiet left third for the headline.'),
    ('hero-portrait.jpg', 'hero-tall.png',     900 / 1300, 0.50,  900,
     'Home hero on phones. The same scene shot vertically.'),
    ('site-wide.jpg',     'fleet-wide.png',   2400 / 1000, 0.50, 1600,
     'About page head, full bleed. Wide establishing shot across a whole job.'),
    ('commercial.jpg',    'commercial.png',   1600 / 1200, 0.30, 1200,
     'Home "before" feature. Bias left onto the machine and the breach it has opened.'),
    ('commercial-wide.jpg', 'commercial.png',  1600 / 1000, 0.80, 1400,
     'Contact head. Same building, biased right onto the intact end, so the two '
     'uses of this photograph do not read as the same picture twice.'),
    ('cleared-lot.jpg',   'cleared-lot.png',  1600 / 1200, 0.50, 1200,
     'About "after" feature. Already 4:3, so barely cropped.'),
    ('teardown.jpg',      'house.png',        1600 / 1000, 0.42, 1400,
     'Services head, full bleed. Bias up: the roofline matters more than the foreground.'),
    ('plant.jpg',         'fleet-wide.png',   1600 / 1000, 0.18, 1294,
     'Areas We Serve head, full bleed. Biased left onto the machine working the '
     'structure. The About head is the same photograph, and its full-width band '
     'lands on the fleet at the right, so this end keeps them distinct.'),
]


def crop_to(im, ratio, bias):
    """Crop to `ratio` off whichever axis is long, keeping `bias` of the frame."""
    w, h = im.size
    if w / h > ratio:                       # too wide: trim the sides
        new_w = round(h * ratio)
        x = round((w - new_w) * bias)
        return im.crop((x, 0, x + new_w, h))
    new_h = round(w / ratio)                # too tall: trim top and bottom
    y = round((h - new_h) * bias)
    return im.crop((0, y, w, y + new_h))


def save(im, path, max_w):
    if im.width > max_w:                    # never upscale: it costs bytes, adds nothing
        im = im.resize((max_w, round(im.height * max_w / im.width)), Image.LANCZOS)
    im.convert('RGB').save(path, quality=QUALITY, optimize=True, progressive=True)
    return im


if __name__ == '__main__':
    os.makedirs(OUT, exist_ok=True)
    for name, src, ratio, bias, max_w, _note in SLOTS:
        im = ImageOps.exif_transpose(Image.open(os.path.join(SRC, src)))
        out = save(crop_to(im, ratio, bias), os.path.join(OUT, name), max_w)
        kb = os.path.getsize(os.path.join(OUT, name)) / 1024
        print(f'{name:20s} {out.width:4d}x{out.height:<4d} {kb:6.0f} KB   from {src}')

    m = ImageOps.exif_transpose(Image.open(os.path.join(SRC, 'service-area-map.png')))
    save(m, os.path.join(MAP_OUT, 'service-area-map.jpg'), 1400)
    kb = os.path.getsize(os.path.join(MAP_OUT, 'service-area-map.jpg')) / 1024
    print(f'{"service-area-map.jpg":20s} {min(m.width,1400):4d}x{"":4s} {kb:6.0f} KB')
