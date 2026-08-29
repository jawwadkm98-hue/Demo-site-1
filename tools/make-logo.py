"""Generate the Beltway Demolition logo kit.

The idea: the Capital Beltway is a ring road, and demolition takes a piece out
of things. So the mark is a heavy ring with a segment broken out of the upper
right, and that segment kicked clear of the gap it left.

One idea, two shapes, no letterforms — which is what survives at favicon size.
Geometry is computed rather than hand-placed, so the gap and the loose piece
stay concentric at every size and weight.

Run: python3 tools/make-logo.py
"""
import math, os

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'assets', 'img')
AMBER, INK, WHITE, MUTED = '#f0a11a', '#0a0c0e', '#ffffff', '#98a4b0'
LABEL = 'Beltway Demolition mark: a ring with a segment broken out of it'

CX = CY = 32.0
R = 18.0
W = 9.0                                  # heavy enough to hold at 16px
GAP_MID, GAP_HALF = 45.0, 30.0           # break centred on the 1:30 position
FRAG_START, FRAG_END = 19.0, 71.0        # the loose piece, spanning the gap
FRAG_KICK, FRAG_TURN = 6.5, 13.0         # how far out, and how far rotated


def pt(angle_deg, r=R):
    """Point on the ring; angle measured clockwise from twelve o'clock."""
    a = math.radians(angle_deg)
    return CX + r * math.sin(a), CY - r * math.cos(a)


def arc(a0, a1):
    """Clockwise arc from a0 to a1."""
    x0, y0 = pt(a0)
    x1, y1 = pt(a1)
    large = 1 if (a1 - a0) % 360 > 180 else 0
    return f'M{x0:.2f} {y0:.2f}A{R} {R} 0 {large} 1 {x1:.2f} {y1:.2f}'


RING = arc(GAP_MID + GAP_HALF, GAP_MID - GAP_HALF)     # the long way round
FRAG = arc(FRAG_START, FRAG_END)                       # the short piece
_kx = FRAG_KICK * math.sin(math.radians(GAP_MID))
_ky = -FRAG_KICK * math.cos(math.radians(GAP_MID))
FRAG_TRANSFORM = f'translate({_kx:.2f} {_ky:.2f}) rotate({FRAG_TURN} {CX} {CY})'


def mark(ring_colour, frag_colour, indent='  '):
    return (
        f'{indent}<path d="{RING}" fill="none" stroke="{ring_colour}" stroke-width="{W}"\n'
        f'{indent}      stroke-linecap="round"/>\n'
        f'{indent}<path d="{FRAG}" fill="none" stroke="{frag_colour}" stroke-width="{W}"\n'
        f'{indent}      stroke-linecap="round" transform="{FRAG_TRANSFORM}"/>'
    )


def svg(body, vb='0 0 64 64', label=None, extra=''):
    a = f' role="img" aria-label="{label}"' if label else ''
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vb}"{a}>\n{extra}{body}\n</svg>\n'


def lockup(word_colour, sub_colour, frag_colour):
    return (f'  <g transform="translate(4 8)">\n'
            f'{mark(AMBER if frag_colour != "currentColor" else "currentColor", frag_colour, indent="    ")}\n'
            f'  </g>\n'
            f'  <g font-family="Oswald, \'Arial Narrow\', Arial, sans-serif" fill="{word_colour}">\n'
            f'    <text x="86" y="42" font-size="34" font-weight="600" letter-spacing="3.4">BELTWAY</text>\n'
            f'    <text x="88" y="63" font-size="15" font-weight="400" letter-spacing="6.2"\n'
            f'          fill="{sub_colour}">DEMOLITION</text>\n'
            f'  </g>')


FILES = {
    # Favicon carries its own ground, so its colours are fixed.
    'favicon.svg':          svg(mark(AMBER, WHITE),
                                extra=f'  <rect width="64" height="64" rx="8" fill="{INK}"/>\n'),
    # Inline use: the fragment inherits the surrounding text colour.
    'logo-mark.svg':        svg(mark(AMBER, 'currentColor'), label=LABEL),
    # Fixed variants for <img>, where currentColor cannot reach in.
    'logo-mark-dark.svg':   svg(mark(AMBER, WHITE), label=LABEL),
    'logo-mark-light.svg':  svg(mark(AMBER, INK), label=LABEL),
    # One colour, for vinyl, embroidery, stamps and single-plate print.
    'logo-mark-mono.svg':   svg(mark('currentColor', 'currentColor'), label=LABEL),
    'logo-lockup-dark.svg':  svg(lockup(WHITE, MUTED, WHITE), '0 0 420 80', 'Beltway Demolition'),
    'logo-lockup-light.svg': svg(lockup(INK, '#5a6672', INK), '0 0 420 80', 'Beltway Demolition'),
    'logo-lockup-mono.svg':  svg(lockup('currentColor', 'currentColor', 'currentColor'),
                                 '0 0 420 80', 'Beltway Demolition'),
}

if __name__ == '__main__':
    os.makedirs(OUT, exist_ok=True)
    for name, body in FILES.items():
        open(os.path.join(OUT, name), 'w').write(body)
        print(' ', name)
    print('\ninline mark for partials/header.html and partials/footer.html:\n')
    print(mark(AMBER, 'currentColor', indent='        '))
