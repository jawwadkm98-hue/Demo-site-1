#!/usr/bin/env python3
"""Derive the site's brand images from the master logo artwork.

Input:  assets/brand/logo-v2-full.png  (1536x1024, transparent background)
Output: assets/brand/logo-emblem-v2.png  header/footer mark (2x, transparent)
        assets/brand/social-card.jpg     1200x630 link-preview card
"""
import os
from PIL import Image, ImageDraw

BRAND = os.path.join(os.path.dirname(__file__), '..', 'assets', 'brand')
INK = (10, 12, 14)


def trim(im, tol=8):
    bbox = im.getchannel('A').point(lambda v: 255 if v > tol else 0).getbbox()
    return im.crop(bbox) if bbox else im


def fit(im, box_w, box_h):
    """Scale to fit inside box, centred, on a transparent canvas."""
    s = min(box_w / im.width, box_h / im.height)
    im = im.resize((max(1, round(im.width * s)), max(1, round(im.height * s))), Image.LANCZOS)
    canvas = Image.new('RGBA', (box_w, box_h), (0, 0, 0, 0))
    canvas.paste(im, ((box_w - im.width) // 2, (box_h - im.height) // 2), im)
    return canvas


master = Image.open(os.path.join(BRAND, 'logo-v2-full.png')).convert('RGBA')

# --- header / footer emblem: the arc + machine, without the wordmark ------
# The wordmark plate starts a little below y=660 in the master.
# Rendered at exactly 2x the CSS height so it lands on whole device pixels;
# keep DISPLAY_H in step with .brand__mark in assets/css/styles.css.
DISPLAY_H = 88
scene = trim(master.crop((0, 0, master.width, 665)))
emblem = scene.resize((round(scene.width * DISPLAY_H * 2 / scene.height), DISPLAY_H * 2),
                      Image.LANCZOS)
emblem.save(os.path.join(BRAND, 'logo-emblem-v2.png'), optimize=True)
print(f'logo-emblem-v2.png  {emblem.width}x{emblem.height}  '
      f'(display {emblem.width // 2}x{DISPLAY_H})')

full = trim(master)

# --- 1200x630 social card -------------------------------------------------
card = Image.new('RGBA', (1200, 630), INK + (255,))
draw = ImageDraw.Draw(card)
for y in range(630):                     # subtle top-down lift
    t = 1 - y / 630
    draw.line([(0, y), (1200, y)], fill=(
        INK[0] + round(14 * t), INK[1] + round(16 * t), INK[2] + round(18 * t), 255))
art = fit(full, 1040, 500)
card.alpha_composite(art, (80, 65))
draw.rectangle([(0, 624), (1200, 630)], fill=(240, 161, 26, 255))
# JPEG, not PNG: the card is a photographic-looking illustration on a gradient,
# which PNG stores at roughly four times the size for no visible gain, and it
# ships on every link preview.
card.convert('RGB').save(os.path.join(BRAND, 'social-card.jpg'),
                         quality=88, optimize=True, progressive=True)
print('social-card.jpg     1200x630')
