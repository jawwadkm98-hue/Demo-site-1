"""Generate the Beltway Demolition favicon and simplified marks.

The full logo (assets/brand/logo-v2-full.png) is an illustration: excavator,
skyline, rubble and a wordmark. It carries the brand everywhere it has room —
the header, the social card, print. It cannot be a favicon: at 16px the scene
turns to noise, as the crops in review showed.

So the tab icon is drawn from the logo's two most distinctive simple shapes,
the gold arc and the wrecking ball, at a weight that survives 16px. The same
geometry is rasterised into the PNG sizes SVG icons don't cover (iOS home
screen, older Android, some feed readers).

Run: python3 tools/make-logo.py
"""
import os

from PIL import Image, ImageDraw

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'assets', 'img')
GOLD, STEEL, INK = '#f0a11a', '#d8dde2', '#0a0c0e'
LABEL = 'Beltway Demolition: a wrecking ball swinging beneath the brand arc'


def mark(arc_colour, ball_colour):
    return f'''  <path d="M8 42A26 26 0 0 1 56 26" fill="none" stroke="{arc_colour}"
        stroke-width="8" stroke-linecap="round"/>
  <path d="M45 29v9" stroke="{ball_colour}" stroke-width="4" stroke-linecap="round"/>
  <circle cx="45" cy="48" r="11" fill="{ball_colour}"/>'''


def svg(body, label=None, extra=''):
    a = f' role="img" aria-label="{label}"' if label else ''
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"{a}>\n'
            f'{extra}{body}\n</svg>\n')


RASTER = [(32, 'favicon-32.png'), (180, 'apple-touch-icon.png'), (512, 'icon-512.png')]
SS = 8  # supersample factor, so the arc and ball edges come down clean


def rgb(h):
    return tuple(int(h[i:i + 2], 16) for i in (1, 3, 5)) + (255,)


def raster(size):
    """The same 64-unit geometry as mark(), drawn with pixels."""
    n = size * SS
    im = Image.new("RGBA", (n, n), (0, 0, 0, 0))
    d, u = ImageDraw.Draw(im), n / 64.0
    d.rounded_rectangle([0, 0, n - 1, n - 1], radius=n * 10 / 64, fill=rgb(INK))
    d.arc([4 * u, 6 * u, 60 * u, 62 * u], start=203, end=310, fill=rgb(GOLD), width=int(8 * u))
    d.line([(45 * u, 29 * u), (45 * u, 38 * u)], fill=rgb(STEEL), width=int(4 * u))
    d.ellipse([34 * u, 37 * u, 56 * u, 59 * u], fill=rgb(STEEL))
    return im.resize((size, size), Image.LANCZOS)


FILES = {
    # Favicon carries its own ground so it reads on light and dark tab bars.
    'favicon.svg':          svg(mark(GOLD, STEEL),
                                extra=f'  <rect width="64" height="64" rx="10" fill="{INK}"/>\n'),
    'logo-mark.svg':        svg(mark(GOLD, 'currentColor'), LABEL),
    'logo-mark-dark.svg':   svg(mark(GOLD, STEEL), LABEL),
    'logo-mark-light.svg':  svg(mark(GOLD, INK), LABEL),
    'logo-mark-mono.svg':   svg(mark('currentColor', 'currentColor'), LABEL),
}

if __name__ == '__main__':
    os.makedirs(OUT, exist_ok=True)
    # The old vector lockups belonged to the retired BD monogram.
    for stale in ('logo-lockup-dark.svg', 'logo-lockup-light.svg', 'logo-lockup-mono.svg'):
        pth = os.path.join(OUT, stale)
        if os.path.exists(pth):
            os.remove(pth); print('  removed', stale)
    for name, body in FILES.items():
        open(os.path.join(OUT, name), 'w').write(body)
        print(' ', name)
    for size, name in RASTER:
        raster(size).save(os.path.join(OUT, name), optimize=True)
        print(f'  {name}  {size}x{size}')
