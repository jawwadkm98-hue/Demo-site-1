"""Generate the Beltway Demolition icon kit.

Two different jobs, two different sources:

* The tab icon, home-screen icon and .ico come from the client's circular
  badge, assets/brand/favicon-source.png. A circle inside a gold ring holds
  its silhouette down to 16px even though the scene inside it does not.
* The one-colour marks (logo-mark-*.svg) are a deliberate reduction of the
  logo's two most distinctive shapes, the gold arc and the wrecking ball.
  They exist for the jobs no detailed raster can do: one-colour print,
  vinyl and embroidery.

Run: python3 tools/make-logo.py
"""
import os

from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, '..', 'assets', 'img')
SRC = os.path.join(HERE, '..', 'assets', 'brand', 'favicon-source.png')
GOLD, STEEL, INK = '#f0a11a', '#d8dde2', '#0a0c0e'
LABEL = 'Beltway Demolition: a wrecking ball swinging beneath the brand arc'

# Sizes browsers and platforms actually ask for.
PNGS = [(16, 'favicon-16.png'), (32, 'favicon-32.png'), (48, 'favicon-48.png')]
# Android home screen, via site.webmanifest. Flattened onto ink: the launcher
# applies its own mask, and an opaque PNG compresses far better than an alpha one.
MANIFEST = [(192, 'icon-192.png'), (512, 'icon-512.png')]
ICO = [16, 32, 48]
APPLE = 180          # iOS home screen: composited on ink, no transparency
APPLE_INSET = 0.92   # iOS rounds the corners, so leave the ring a little room


def mark(arc_colour, ball_colour):
    return f'''  <path d="M8 42A26 26 0 0 1 56 26" fill="none" stroke="{arc_colour}"
        stroke-width="8" stroke-linecap="round"/>
  <path d="M45 29v9" stroke="{ball_colour}" stroke-width="4" stroke-linecap="round"/>
  <circle cx="45" cy="48" r="11" fill="{ball_colour}"/>'''


def svg(body, label=None):
    a = f' role="img" aria-label="{label}"' if label else ''
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"{a}>\n'
            f'{body}\n</svg>\n')


FILES = {
    'logo-mark.svg':        svg(mark(GOLD, 'currentColor'), LABEL),
    'logo-mark-dark.svg':   svg(mark(GOLD, STEEL), LABEL),
    'logo-mark-light.svg':  svg(mark(GOLD, INK), LABEL),
    'logo-mark-mono.svg':   svg(mark('currentColor', 'currentColor'), LABEL),
}


def rgb(h):
    return tuple(int(h[i:i + 2], 16) for i in (1, 3, 5))


def badge():
    """The badge, trimmed to its artwork and squared on a transparent canvas."""
    im = Image.open(SRC).convert('RGBA')
    box = im.getchannel('A').point(lambda v: 255 if v > 8 else 0).getbbox()
    im = im.crop(box)
    n = max(im.size)
    sq = Image.new('RGBA', (n, n), (0, 0, 0, 0))
    sq.paste(im, ((n - im.width) // 2, (n - im.height) // 2), im)
    return sq


if __name__ == '__main__':
    os.makedirs(OUT, exist_ok=True)
    # The vector lockups and the drawn favicon belonged to earlier marks.
    for stale in ('logo-lockup-dark.svg', 'logo-lockup-light.svg',
                  'logo-lockup-mono.svg', 'favicon.svg'):
        p = os.path.join(OUT, stale)
        if os.path.exists(p):
            os.remove(p); print('  removed', stale)

    for name, body in FILES.items():
        open(os.path.join(OUT, name), 'w').write(body)
        print(' ', name)

    src = badge()
    for size, name in PNGS:
        src.resize((size, size), Image.LANCZOS).save(os.path.join(OUT, name), optimize=True)
        print(f'  {name}  {size}x{size}')

    for size, name in MANIFEST:
        tile = Image.new('RGBA', (size, size), rgb(INK) + (255,))
        tile.alpha_composite(src.resize((size, size), Image.LANCZOS))
        # Only fetched on "add to home screen", but it still ships: an
        # illustration this flat quantises to 256 colours with no visible loss
        # and roughly a quarter of the bytes.
        tile.convert('RGB').quantize(colors=256, method=Image.MEDIANCUT, dither=Image.FLOYDSTEINBERG) \
            .save(os.path.join(OUT, name), optimize=True)
        print(f'  {name}  {size}x{size}')

    src.resize((max(ICO),) * 2, Image.LANCZOS).save(
        os.path.join(OUT, 'favicon.ico'), sizes=[(s, s) for s in ICO])
    print('  favicon.ico ', '+'.join(str(s) for s in ICO))

    # iOS draws no background behind a transparent icon, so give it one.
    apple = Image.new('RGBA', (APPLE, APPLE), rgb(INK) + (255,))
    inner = round(APPLE * APPLE_INSET)
    art = src.resize((inner, inner), Image.LANCZOS)
    apple.alpha_composite(art, ((APPLE - inner) // 2,) * 2)
    apple.convert('RGB').quantize(colors=256, method=Image.MEDIANCUT,
                                  dither=Image.FLOYDSTEINBERG) \
         .save(os.path.join(OUT, 'apple-touch-icon.png'), optimize=True)
    print(f'  apple-touch-icon.png  {APPLE}x{APPLE}')
