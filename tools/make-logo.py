"""Generate the Beltway Demolition logo kit.

The mark is a vector adaptation of the client's chosen BD lockup: a steel B,
a gold D, and the excavator boom working through the D's counter with the
bucket breaking out of the top right. Flattened to strokes and one clean
intersection so it survives at favicon size, where the illustrated original
cannot. The steel elements are drawn in currentColor so the mark follows the
text colour of whatever it sits in.

Run: python3 tools/make-logo.py
"""
import os

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'assets', 'img')
AMBER, INK, WHITE, MUTED = '#f0a11a', '#0a0c0e', '#ffffff', '#98a4b0'
LABEL = 'Beltway Demolition mark: the letters B and D with an excavator boom working through the D'
VB_W, VB_H = 86, 64


def mark(steel, gold, indent='  '):
    """steel = the B, boom and bucket; gold = the D."""
    return f'''{indent}<path d="M10 12v40M10 52h13a10 10 0 0 0 0-20H10M10 32h11a10 10 0 0 0 0-20H10"
{indent}      fill="none" stroke="{steel}" stroke-width="8" stroke-linecap="round" stroke-linejoin="round"/>
{indent}<path d="M44 12v40h10a20 20 0 0 0 0-40z" fill="none" stroke="{gold}" stroke-width="8"
{indent}      stroke-linejoin="round"/>
{indent}<path d="M50 46L68 20" fill="none" stroke="{steel}" stroke-width="6.5" stroke-linecap="round"/>
{indent}<path d="M67 14l10 3-3 10-10-4z" fill="{steel}"/>'''


def svg(body, vb=f'0 0 {VB_W} {VB_H}', label=None, extra=''):
    a = f' role="img" aria-label="{label}"' if label else ''
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vb}"{a}>\n{extra}{body}\n</svg>\n'


def lockup(word_colour, sub_colour, steel_colour):
    gold = AMBER if steel_colour != 'currentColor' else 'currentColor'
    return (f'  <g transform="translate(2 8)">\n{mark(steel_colour, gold, indent="    ")}\n  </g>\n'
            f'  <g font-family="Oswald, \'Arial Narrow\', Arial, sans-serif" fill="{word_colour}">\n'
            f'    <text x="104" y="42" font-size="34" font-weight="600" letter-spacing="3.4">BELTWAY</text>\n'
            f'    <text x="106" y="63" font-size="15" font-weight="400" letter-spacing="6.2"\n'
            f'          fill="{sub_colour}">DEMOLITION</text>\n'
            f'  </g>')


# Favicon: centre the wide mark in a 64x64 tile with its own ground.
_FAV_T = 'transform="translate(1 9) scale(0.72)"'

FILES = {
    'favicon.svg': (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64">\n'
                    f'  <rect width="64" height="64" rx="8" fill="{INK}"/>\n'
                    f'  <g {_FAV_T}>\n{mark(AMBER, WHITE, indent="    ")}\n  </g>\n</svg>\n'),
    # Inline use: boom + bucket inherit the surrounding text colour.
    'logo-mark.svg':        svg(mark(AMBER, 'currentColor'), label=LABEL),
    'logo-mark-dark.svg':   svg(mark(AMBER, WHITE), label=LABEL),
    'logo-mark-light.svg':  svg(mark(AMBER, INK), label=LABEL),
    # One colour, for vinyl, embroidery, stamps and single-plate print.
    'logo-mark-mono.svg':   svg(mark('currentColor', 'currentColor'), label=LABEL),
    'logo-lockup-dark.svg':  svg(lockup(WHITE, AMBER, WHITE), '0 0 448 80', 'Beltway Demolition'),
    'logo-lockup-light.svg': svg(lockup(INK, '#cf860c', INK), '0 0 448 80', 'Beltway Demolition'),
    'logo-lockup-mono.svg':  svg(lockup('currentColor', 'currentColor', 'currentColor'),
                                 '0 0 448 80', 'Beltway Demolition'),
}

if __name__ == '__main__':
    os.makedirs(OUT, exist_ok=True)
    for name, body in FILES.items():
        open(os.path.join(OUT, name), 'w').write(body)
        print(' ', name)
