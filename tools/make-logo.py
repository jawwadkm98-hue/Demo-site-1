"""Generate the Beltway Demolition logo kit.

The mark is a vector adaptation of the client's chosen concept: a bold B with
an excavator boom rising off the top of the stem, the stick dropping to a
bucket working clear of the bowls. Flattened to two weights and plain
geometry so it survives at favicon size, where the illustrated original
cannot.

Run: python3 tools/make-logo.py
"""
import os

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'assets', 'img')
AMBER, INK, WHITE, MUTED = '#f0a11a', '#0a0c0e', '#ffffff', '#98a4b0'
LABEL = 'Beltway Demolition mark: a letter B with an excavator boom and bucket'
VB_W, VB_H = 82, 64


def mark(c1, c2, indent='  '):
    """c1 = the B, c2 = boom + bucket."""
    return f'''{indent}<path d="M14 12v44M14 56h15a11 11 0 0 0 0-22H14M14 34h13a11 11 0 0 0 0-22H14"
{indent}      fill="none" stroke="{c1}" stroke-width="9" stroke-linecap="round" stroke-linejoin="round"/>
{indent}<path d="M14 12L44 4l20 15" fill="none" stroke="{c2}" stroke-width="8"
{indent}      stroke-linecap="round" stroke-linejoin="round"/>
{indent}<path d="M64 19l3 14" fill="none" stroke="{c2}" stroke-width="6" stroke-linecap="round"/>
{indent}<path d="M70 33l6 5-6 9-9-6z" fill="{c2}"/>'''


def svg(body, vb=f'0 0 {VB_W} {VB_H}', label=None, extra=''):
    a = f' role="img" aria-label="{label}"' if label else ''
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vb}"{a}>\n{extra}{body}\n</svg>\n'


def lockup(word_colour, sub_colour, frag_colour):
    b = AMBER if frag_colour != 'currentColor' else 'currentColor'
    return (f'  <g transform="translate(2 8)">\n{mark(b, frag_colour, indent="    ")}\n  </g>\n'
            f'  <g font-family="Oswald, \'Arial Narrow\', Arial, sans-serif" fill="{word_colour}">\n'
            f'    <text x="100" y="42" font-size="34" font-weight="600" letter-spacing="3.4">BELTWAY</text>\n'
            f'    <text x="102" y="63" font-size="15" font-weight="400" letter-spacing="6.2"\n'
            f'          fill="{sub_colour}">DEMOLITION</text>\n'
            f'  </g>')


# Favicon: centre the wide mark in a 64x64 tile with its own ground.
_FAV_T = f'transform="translate(1.5 8) scale(0.75)"'

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
    'logo-lockup-dark.svg':  svg(lockup(WHITE, MUTED, WHITE), '0 0 440 80', 'Beltway Demolition'),
    'logo-lockup-light.svg': svg(lockup(INK, '#5a6672', INK), '0 0 440 80', 'Beltway Demolition'),
    'logo-lockup-mono.svg':  svg(lockup('currentColor', 'currentColor', 'currentColor'),
                                 '0 0 440 80', 'Beltway Demolition'),
}

if __name__ == '__main__':
    os.makedirs(OUT, exist_ok=True)
    for name, body in FILES.items():
        open(os.path.join(OUT, name), 'w').write(body)
        print(' ', name)
