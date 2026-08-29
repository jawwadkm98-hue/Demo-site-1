"""Generate placeholder scene plates for the site's image slots.

These are NOT photographs — they are layered SVG scenes (dusk sky, haze bands,
three depth planes, grain, vignette) cut to the exact aspect ratio of each
slot, so the layout is final and real photography drops straight in.

Subjects are matched to the work: commercial teardown, small-structure
demolition, a cleared and graded lot, and plant staged on site.

Run: python3 tools/make-plates.py
"""
import os, random

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'assets', 'img', 'photos')
ACCENT = '#f0a11a'                       # matches --amber in styles.css
SKY = [('#141a20', 0.0), ('#1c242c', 0.34), ('#2f3339', 0.58),
       ('#5c5346', 0.78), ('#232a31', 0.90), ('#0d1114', 1.0)]
FAR, MID, NEAR, FORE = '#3f4954', '#242c34', '#141a1f', '#0a0d10'


def defs(w, h, seed):
    stops = ''.join('<stop offset="%.2f" stop-color="%s"/>' % (o, c) for c, o in SKY)
    return f'''<defs>
<linearGradient id="sky" x1="0" y1="0" x2="0" y2="1">{stops}</linearGradient>
<radialGradient id="glow" cx="0.68" cy="0.74" r="0.42">
  <stop offset="0" stop-color="#c9a06a" stop-opacity="0.30"/>
  <stop offset="1" stop-color="#c9a06a" stop-opacity="0"/>
</radialGradient>
<radialGradient id="vig" cx="0.5" cy="0.45" r="0.78">
  <stop offset="0.38" stop-color="#000" stop-opacity="0"/>
  <stop offset="1" stop-color="#000" stop-opacity="0.70"/>
</radialGradient>
<linearGradient id="hazeGrad" x1="0" y1="0" x2="0" y2="1">
  <stop offset="0" stop-color="#9aa6b2" stop-opacity="0"/>
  <stop offset="0.45" stop-color="#9aa6b2" stop-opacity="1"/>
  <stop offset="1" stop-color="#9aa6b2" stop-opacity="0"/>
</linearGradient>
<filter id="grain" x="0" y="0" width="100%" height="100%">
  <feTurbulence type="fractalNoise" baseFrequency="0.82" numOctaves="3" seed="{seed}"/>
  <feColorMatrix type="saturate" values="0"/>
</filter>
<filter id="soft" x="-20%" y="-20%" width="140%" height="140%">
  <feGaussianBlur stdDeviation="{max(2, w // 340)}"/>
</filter>
</defs>'''


def haze(y, h, w, op):
    return f'<rect x="0" y="{y:.0f}" width="{w}" height="{h:.0f}" fill="#9aa6b2" opacity="{op}"/>'


def plume(x, base, w, h):
    return (f'<ellipse cx="{x:.0f}" cy="{base - h*0.35:.0f}" rx="{w*0.55:.0f}" ry="{h*0.42:.0f}" '
            f'fill="#b9b0a2" opacity="0.15" filter="url(#soft)"/>'
            f'<ellipse cx="{x - w*0.22:.0f}" cy="{base - h*0.12:.0f}" rx="{w*0.40:.0f}" '
            f'ry="{h*0.24:.0f}" fill="#b9b0a2" opacity="0.11" filter="url(#soft)"/>')


def block(x, base, w, h, fill, windows=True, floors=6):
    s = f'<rect x="{x:.0f}" y="{base-h:.0f}" width="{w:.0f}" height="{h:.0f}" fill="{fill}"/>'
    if windows:
        cw, ch = w / 9.0, h / (floors + 2.0)
        for r in range(1, floors):
            for c in range(1, 8, 2):
                s += (f'<rect x="{x + c*cw:.0f}" y="{base - h + (r + 0.6)*ch:.0f}" '
                      f'width="{cw:.0f}" height="{ch*0.6:.0f}" fill="#000" opacity="0.4"/>')
    return s


def broken_block(x, base, w, h, fill):
    """A block with its top floors already taken off — a live demolition face."""
    s = (f'<path d="M{x:.0f} {base:.0f}V{base-h:.0f}h{w*0.46:.0f}v{h*0.20:.0f}'
         f'l{w*0.16:.0f} {h*0.08:.0f}v{h*0.12:.0f}l{w*0.12:.0f} {h*0.06:.0f}'
         f'V{base:.0f}z" fill="{fill}"/>')
    cw, ch = w / 9.0, h / 8.0
    for r in range(3, 8):
        for c in range(1, 6, 2):
            s += (f'<rect x="{x + c*cw:.0f}" y="{base - h + r*ch:.0f}" width="{cw:.0f}" '
                  f'height="{ch*0.6:.0f}" fill="#000" opacity="0.42"/>')
    return s


def house(x, base, w, h, fill, gable=True):
    s = f'<rect x="{x:.0f}" y="{base-h:.0f}" width="{w:.0f}" height="{h:.0f}" fill="{fill}"/>'
    if gable:
        s += (f'<path d="M{x-w*0.06:.0f} {base-h:.0f}L{x+w*0.5:.0f} {base-h*1.45:.0f}'
              f'L{x+w*1.06:.0f} {base-h:.0f}z" fill="{fill}"/>')
    s += (f'<rect x="{x+w*0.16:.0f}" y="{base-h*0.66:.0f}" width="{w*0.20:.0f}" '
          f'height="{h*0.26:.0f}" fill="#000" opacity="0.4"/>'
          f'<rect x="{x+w*0.60:.0f}" y="{base-h*0.66:.0f}" width="{w*0.20:.0f}" '
          f'height="{h*0.26:.0f}" fill="#000" opacity="0.4"/>')
    return s


def excavator(x, base, s, accent=ACCENT):
    """High-reach machine. Body reads dark against the sky; the accent is paint
    and a beacon, not the whole machine."""
    dark, mid = '#161c22', '#414b56'
    return (f'<g transform="translate({x:.0f} {base:.0f}) scale({s:.3f})">'
            f'<path d="M10 -76L120 -250" stroke="{mid}" stroke-width="17" stroke-linecap="round"/>'
            f'<path d="M10 -76L120 -250" stroke="{accent}" stroke-width="6" stroke-linecap="round" opacity="0.9"/>'
            f'<path d="M120 -250L186 -196" stroke="{mid}" stroke-width="12" stroke-linecap="round"/>'
            f'<path d="M186 -196l26 22-14 20-30-24z" fill="{accent}"/>'
            f'<path d="M-70 0h150v-34h-150z" fill="{mid}"/>'
            f'<rect x="-70" y="-34" width="46" height="7" fill="{accent}"/>'
            f'<path d="M-32 -34h62v-46h-62z" fill="{mid}"/>'
            f'<rect x="-32" y="-80" width="62" height="6" fill="{accent}"/>'
            f'<rect x="-25" y="-70" width="34" height="26" fill="#c8b184" opacity="0.45"/>'
            f'<rect x="16" y="-84" width="7" height="7" fill="{accent}"/>'
            f'<rect x="-78" y="-8" width="168" height="16" rx="8" fill="{dark}"/>'
            f'</g>')


def dozer(x, base, s, accent=ACCENT):
    mid = '#414b56'
    return (f'<g transform="translate({x:.0f} {base:.0f}) scale({s:.3f})">'
            f'<path d="M-58 0h108v-30h-108z" fill="{mid}"/>'
            f'<rect x="-58" y="-30" width="38" height="6" fill="{accent}"/>'
            f'<path d="M-16 -30h40v-30h-40z" fill="{mid}"/>'
            f'<rect x="-11" y="-56" width="24" height="18" fill="#c8b184" opacity="0.4"/>'
            f'<path d="M-66 6h124v14h-124z" rx="7" fill="#12171c"/>'
            f'<path d="M56 8v-46h13v46z" fill="{mid}"/>'
            f'</g>')


def rolloff(x, base, w, h, fill=NEAR, accent=None):
    s = (f'<path d="M{x:.0f} {base:.0f}v-{h:.0f}h{w:.0f}v{h*0.62:.0f}l-{w*0.14:.0f} {h*0.38:.0f}z" '
         f'fill="{fill}"/>')
    if accent:
        s += f'<rect x="{x:.0f}" y="{base-h:.0f}" width="{w:.0f}" height="{h*0.11:.0f}" fill="{accent}"/>'
    return s


def hoarding(base, w, fill=FORE):
    posts = ''.join(f'<rect x="{i}" y="{base:.0f}" width="5" height="46" fill="#080b0d"/>'
                    for i in range(0, int(w) + 60, 78))
    return f'<rect x="-10" y="{base:.0f}" width="{w+20}" height="30" fill="{fill}"/>' + posts


def stakes(base, w, n, accent=ACCENT):
    rnd = random.Random(4)
    out = []
    for i in range(n):
        x = 60 + i * (w - 120) / max(1, n - 1)
        y = base - rnd.randint(2, 14)
        out.append(f'<rect x="{x:.0f}" y="{y-26:.0f}" width="3" height="26" fill="#3a4149"/>')
        out.append(f'<rect x="{x-4:.0f}" y="{y-30:.0f}" width="11" height="7" fill="{accent}" opacity="0.85"/>')
    return "".join(out)


def rubble(base, w, fill, seed):
    rnd = random.Random(seed)
    pts, x = [], -20
    while x < w + 20:
        pts.append((x, base - rnd.randint(0, 30)))
        x += rnd.randint(26, 70)
    d = 'M-20 %d' % (base + 90) + ''.join('L%d %d' % p for p in pts) + 'L%d %d z' % (w + 20, base + 90)
    return f'<path d="{d}" fill="{fill}"/>'


def scene(w, h, seed, build, horizon=0.76, label=''):
    hz = int(h * horizon)
    body = [f'<rect width="{w}" height="{h}" fill="url(#sky)"/>',
            f'<rect width="{w}" height="{h}" fill="url(#glow)"/>',
            build(w, h, hz),
            f'<rect x="0" y="{hz}" width="{w}" height="{h-hz}" fill="#0b0e11"/>',
            f'<rect width="{w}" height="{h}" fill="url(#vig)"/>',
            f'<rect width="{w}" height="{h}" filter="url(#grain)" opacity="0.16" '
            f'style="mix-blend-mode:overlay"/>']
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" '
            f'preserveAspectRatio="xMidYMid slice" role="presentation">'
            + defs(w, h, seed) + ''.join(body) + '</svg>')


# --------------------------------------------------------------- scenes ----
def commercial_teardown(w, h, hz):
    """Mid-rise commercial building part way down, machine working the face."""
    return ''.join([
        f'<g filter="url(#soft)" opacity="0.7">',
        block(w*0.03, hz, w*0.17, h*0.30, FAR),
        block(w*0.78, hz, w*0.20, h*0.26, FAR),
        '</g>',
        haze(hz - h*0.22, h*0.26, w, 0.22),
        block(w*0.22, hz, w*0.16, h*0.40, MID, floors=7),
        broken_block(w*0.42, hz, w*0.26, h*0.46, MID),
        haze(hz - h*0.09, h*0.14, w, 0.16),
        plume(w*0.56, hz, w*0.22, h*0.30),
        excavator(w*0.30, hz, min(w, h) / 640.0),
        rolloff(w*0.72, hz, w*0.13, h*0.09, NEAR, ACCENT),
        rubble(hz, w, FORE, 7),
        hoarding(hz + h*0.12, w),
    ])


def small_structure(w, h, hz):
    """A house or small commercial structure coming down."""
    return ''.join([
        f'<g filter="url(#soft)" opacity="0.65">',
        house(w*0.06, hz, w*0.14, h*0.16, FAR),
        house(w*0.80, hz, w*0.15, h*0.17, FAR),
        '</g>',
        haze(hz - h*0.20, h*0.24, w, 0.22),
        house(w*0.24, hz, w*0.20, h*0.22, MID),
        f'<path d="M{w*0.50:.0f} {hz:.0f}v-{h*0.20:.0f}h{w*0.16:.0f}v{h*0.07:.0f}'
        f'l-{w*0.06:.0f} {h*0.05:.0f}h-{w*0.04:.0f}v{h*0.08:.0f}z" fill="{MID}"/>',
        haze(hz - h*0.07, h*0.12, w, 0.15),
        plume(w*0.55, hz, w*0.18, h*0.22),
        excavator(w*0.68, hz, min(w, h) / 780.0),
        rolloff(w*0.12, hz, w*0.14, h*0.10, NEAR, ACCENT),
        rubble(hz, w, FORE, 3),
        hoarding(hz + h*0.14, w),
    ])


def cleared_lot(w, h, hz):
    """Graded parcel, stakes set, ready to hand back."""
    return ''.join([
        f'<g filter="url(#soft)" opacity="0.6">',
        block(w*0.02, hz, w*0.16, h*0.22, FAR),
        house(w*0.62, hz, w*0.12, h*0.13, FAR),
        block(w*0.84, hz, w*0.14, h*0.19, FAR),
        '</g>',
        haze(hz - h*0.18, h*0.22, w, 0.20),
        # graded ground: shallow banded fill rather than structures
        f'<path d="M0 {hz:.0f}h{w}v{h*0.06:.0f}H0z" fill="#1a2027"/>',
        f'<path d="M0 {hz + h*0.05:.0f}q{w*0.5:.0f} -{h*0.03:.0f} {w} 0v{h:.0f}H0z" fill="#12171c"/>',
        stakes(hz, w, 7),
        dozer(w*0.72, hz + h*0.02, min(w, h) / 620.0),
        f'<g stroke="#2b333c" stroke-width="3" fill="none" opacity="0.8">'
        f'<path d="M0 {hz + h*0.11:.0f}q{w*0.5:.0f} -{h*0.04:.0f} {w} 0"/>'
        f'<path d="M0 {hz + h*0.16:.0f}q{w*0.5:.0f} -{h*0.04:.0f} {w} 0"/></g>',
    ])


def plant_on_site(w, h, hz):
    """Machines and containers staged before a job."""
    return ''.join([
        f'<g filter="url(#soft)" opacity="0.62">',
        block(w*0.04, hz, w*0.20, h*0.24, FAR),
        block(w*0.74, hz, w*0.22, h*0.28, FAR),
        '</g>',
        haze(hz - h*0.19, h*0.23, w, 0.22),
        rolloff(w*0.05, hz, w*0.15, h*0.11, MID, ACCENT),
        rolloff(w*0.23, hz, w*0.15, h*0.11, MID),
        rolloff(w*0.41, hz, w*0.15, h*0.11, MID, ACCENT),
        haze(hz - h*0.06, h*0.11, w, 0.14),
        excavator(w*0.72, hz, min(w, h) / 760.0),
        dozer(w*0.30, hz, min(w, h) / 900.0),
        rubble(hz, w, FORE, 11),
        hoarding(hz + h*0.13, w),
    ])


SCENES = [
    ('hero.svg',         2400, 1250, 3,  commercial_teardown, 0.74),
    ('teardown.svg',     1600, 1000, 9,  small_structure,     0.76),
    ('commercial.svg',   1600, 1200, 5,  commercial_teardown, 0.74),
    ('cleared-lot.svg',  1600, 1200, 13, cleared_lot,         0.72),
    ('plant.svg',        1600, 1000, 17, plant_on_site,       0.76),
    ('site-wide.svg',    2400, 1000, 23, plant_on_site,       0.78),
]

if __name__ == '__main__':
    os.makedirs(OUT, exist_ok=True)
    for name, w, h, seed, fn, hzr in SCENES:
        svg = scene(w, h, seed, fn, hzr)
        open(os.path.join(OUT, name), 'w').write(svg)
        print('%-18s %5d x %-5d %5.1f KB' % (name, w, h, len(svg) / 1024))
