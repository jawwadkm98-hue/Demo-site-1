"""Generate atmospheric industrial scene plates as SVG.

These occupy the site's photo slots until real photography is dropped in.
Layered dusk scenes: warm sky, haze bands, three depth planes of structures,
foreground silhouettes, film grain and a vignette.
"""
import os, random

OUT = '/home/user/Demo-site-1/assets/img/photos'

SKY = [('#191713', 0.0), ('#241d16', 0.34), ('#3d2c1b', 0.58),
       ('#6b4826', 0.76), ('#2a2018', 0.90), ('#14110e', 1.0)]
PLANE = {                       # depth: (fill, haze opacity)
    'far':  ('#4a3b2a', 0.55),
    'mid':  ('#241d15', 0.26),
    'near': ('#12100d', 0.0),
    'fore': ('#0a0907', 0.0),
}

def defs(w, h, seed):
    stops = ''.join('<stop offset="%.2f" stop-color="%s"/>' % (o, c) for c, o in SKY)
    return f'''<defs>
<linearGradient id="sky" x1="0" y1="0" x2="0" y2="1">{stops}</linearGradient>
<radialGradient id="glow" cx="0.70" cy="0.72" r="0.40">
  <stop offset="0" stop-color="#e0934a" stop-opacity="0.34"/>
  <stop offset="1" stop-color="#e0934a" stop-opacity="0"/>
</radialGradient>
<radialGradient id="vig" cx="0.5" cy="0.45" r="0.78">
  <stop offset="0.38" stop-color="#000" stop-opacity="0"/>
  <stop offset="1" stop-color="#000" stop-opacity="0.74"/>
</radialGradient>
<filter id="grain" x="0" y="0" width="100%" height="100%">
  <feTurbulence type="fractalNoise" baseFrequency="0.82" numOctaves="3" seed="{seed}"/>
  <feColorMatrix type="saturate" values="0"/>
</filter>
<filter id="soft" x="-20%" y="-20%" width="140%" height="140%">
  <feGaussianBlur stdDeviation="{max(2, w // 340)}"/>
</filter>
</defs>'''

# ------------------------------------------------------------- structures --
def stack(x, base, h, w, fill, lamp=False):
    top = base - h
    s = f'<path d="M{x} {base}V{top + h*0.10}l{w*0.28} -{h*0.055}V{top}h{w*0.44}v{h*0.055}l{w*0.28} {h*0.055}V{base}z" fill="{fill}"/>'
    if lamp:
        s += f'<rect x="{x + w*0.30:.0f}" y="{top - 6:.0f}" width="7" height="7" fill="#ff5c00"/>'
    return s

def cooling(x, base, h, w, fill):
    top = base - h
    return (f'<path d="M{x} {base}V{top + h*0.42}c0 -{h*0.28} {w*0.22} -{h*0.16} {w*0.22} -{h*0.42}'
            f'h{w*0.56}c0 {h*0.26} {w*0.22} {h*0.14} {w*0.22} {h*0.42}V{base}z" fill="{fill}"/>'
            f'<ellipse cx="{x + w/2:.0f}" cy="{top:.0f}" rx="{w*0.28:.0f}" ry="{h*0.035:.0f}" '
            f'fill="#000" opacity="0.35"/>')

def block(x, base, h, w, fill, windows=True, roof=0):
    s = f'<rect x="{x}" y="{base-h}" width="{w}" height="{h}" fill="{fill}"/>'
    if roof:
        s += f'<path d="M{x} {base-h}l{w/2} -{roof} {w/2} {roof}z" fill="{fill}"/>'
    if windows:
        cw, ch = w / 9.0, h / 8.0
        for r in range(2, 7):
            for c in range(1, 8, 2):
                s += (f'<rect x="{x + c*cw:.0f}" y="{base - h + r*ch:.0f}" '
                      f'width="{cw:.0f}" height="{ch*0.62:.0f}" fill="#000" opacity="0.42"/>')
    return s

def silos(x, base, h, w, n, fill):
    s = ''
    for i in range(n):
        s += (f'<rect x="{x + i*(w+4)}" y="{base-h}" width="{w}" height="{h}" '
              f'rx="{w/2:.0f}" fill="{fill}"/>')
    return s

def gantry(x, base, h, w, fill):
    t = base - h
    return (f'<g stroke="{fill}" stroke-width="{max(4, w//34)}" fill="none">'
            f'<path d="M{x} {base}V{t}h{w}v{h}"/><path d="M{x-w*0.10:.0f} {t}h{w*1.20:.0f}"/>'
            f'<path d="M{x+w*0.30:.0f} {base}V{t}M{x+w*0.70:.0f} {base}V{t}"/>'
            f'<path d="M{x+w*0.5:.0f} {t}v{h*0.26:.0f}h-{w*0.14:.0f}"/></g>')

def tower_crane(x, base, h, fill):
    t = base - h
    return (f'<g stroke="{fill}" stroke-width="5" fill="none">'
            f'<path d="M{x} {base}V{t}"/><path d="M{x-6} {base}L{x} {t}L{x+6} {base}"/>'
            f'<path d="M{x-h*0.30:.0f} {t}h{h*0.72:.0f}"/>'
            f'<path d="M{x} {t-30}L{x-h*0.26:.0f} {t}M{x} {t-30}L{x+h*0.60:.0f} {t}"/>'
            f'<path d="M{x+h*0.44:.0f} {t}v{h*0.20:.0f}"/></g>'
            f'<rect x="{x+h*0.42:.0f}" y="{t-14:.0f}" width="7" height="7" fill="#ffc61a"/>')

def excavator(x, base, s, fill):
    """High-reach machine. Mostly dark, as plant is against a bright sky; the
    hi-vis paint and beacon are the only saturated marks in the frame."""
    dark, mid = '#15120f', '#241e18'
    return (f'<g transform="translate({x} {base}) scale({s})">'
            f'<path d="M10 -76L120 -250" stroke="{mid}" stroke-width="17" stroke-linecap="round"/>'
            f'<path d="M10 -76L120 -250" stroke="{fill}" stroke-width="6" stroke-linecap="round"'
            f' opacity="0.85"/>'
            f'<path d="M120 -250L186 -196" stroke="{mid}" stroke-width="12" stroke-linecap="round"/>'
            f'<path d="M186 -196l26 22-14 20-30-24z" fill="{fill}"/>'
            f'<path d="M-70 0h150v-34h-150z" fill="{mid}"/>'
            f'<rect x="-70" y="-34" width="150" height="7" fill="{fill}"/>'
            f'<path d="M-30 -34h58v-42h-58z" fill="{mid}"/>'
            f'<rect x="-24" y="-70" width="30" height="24" fill="#c8a05a" opacity="0.45"/>'
            f'<rect x="16" y="-84" width="7" height="7" fill="#ffc61a"/>'
            f'<rect x="-78" y="-8" width="168" height="16" rx="8" fill="{dark}"/>'
            f'</g>')

def rubble(base, w, fill, seed):
    rnd = random.Random(seed)
    pts, x = [], -20
    while x < w + 20:
        pts.append((x, base - rnd.randint(0, 34)))
        x += rnd.randint(26, 70)
    d = 'M-20 %d' % (base + 90) + ''.join('L%d %d' % p for p in pts) + 'L%d %d z' % (w + 20, base + 90)
    return f'<path d="{d}" fill="{fill}"/>'

def plume(x, base, w, h):
    return (f'<ellipse cx="{x:.0f}" cy="{base - h*0.35:.0f}" rx="{w*0.55:.0f}" '
            f'ry="{h*0.42:.0f}" fill="#c9a271" opacity="0.13" filter="url(#soft)"/>'
            f'<ellipse cx="{x - w*0.22:.0f}" cy="{base - h*0.14:.0f}" rx="{w*0.40:.0f}" '
            f'ry="{h*0.26:.0f}" fill="#c9a271" opacity="0.10" filter="url(#soft)"/>')

def hoarding(base, w, fill):
    posts = ''.join(f'<rect x="{i}" y="{base}" width="5" height="46" fill="#0a0907"/>'
                    for i in range(0, int(w) + 60, 78))
    return (f'<rect x="-10" y="{base}" width="{w+20}" height="30" fill="{fill}"/>' + posts)

def haze(y, h, w, op):
    return (f'<rect x="0" y="{y}" width="{w}" height="{h}" fill="#c98a45" opacity="{op}"/>')

# ----------------------------------------------------------------- scenes --
def scene(w, h, seed, build, horizon=0.72):
    hz = int(h * horizon)
    body = [f'<rect width="{w}" height="{h}" fill="url(#sky)"/>',
            f'<rect width="{w}" height="{h}" fill="url(#glow)"/>']
    body.append(build(w, h, hz))
    body += [
        f'<rect x="0" y="{hz}" width="{w}" height="{h-hz}" fill="#100d0b"/>',
        f'<rect width="{w}" height="{h}" fill="url(#vig)"/>',
        f'<rect width="{w}" height="{h}" filter="url(#grain)" opacity="0.16" '
        f'style="mix-blend-mode:overlay"/>',
    ]
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" '
            f'preserveAspectRatio="xMidYMid slice" role="presentation">'
            + defs(w, h, seed) + ''.join(body) + '</svg>')

def demolition(w, h, hz):
    ff, mf, nf = PLANE['far'][0], PLANE['mid'][0], PLANE['near'][0]
    g = [f'<g filter="url(#soft)" opacity="0.75">',
         stack(w*0.07, hz, h*0.52, w*0.030, ff, True),
         cooling(w*0.15, hz, h*0.40, w*0.115, ff),
         block(w*0.33, hz, h*0.26, w*0.16, ff),
         stack(w*0.55, hz, h*0.46, w*0.026, ff, True),
         '</g>',
         haze(hz - h*0.20, h*0.22, w, 0.16),
         gantry(w*0.60, hz, h*0.30, w*0.20, mf),
         block(w*0.03, hz, h*0.22, w*0.20, mf),
         silos(w*0.44, hz, h*0.24, w*0.030, 3, mf),
         haze(hz - h*0.10, h*0.13, w, 0.13),
         # near plane: a half-taken-down frame, then the machine working it
         f'<path d="M{w*0.72:.0f} {hz}v-{h*0.34:.0f}h{w*0.16:.0f}v{h*0.10:.0f}'
         f'l-{w*0.05:.0f} {h*0.05:.0f}h-{w*0.04:.0f}v{h*0.19:.0f}z" fill="{nf}"/>',
         f'<g stroke="{nf}" stroke-width="6" fill="none">'
         f'<path d="M{w*0.74:.0f} {hz-h*0.30:.0f}h{w*0.12:.0f}"/>'
         f'<path d="M{w*0.74:.0f} {hz-h*0.20:.0f}h{w*0.09:.0f}"/></g>',
         plume(w*0.40, hz, w*0.26, h*0.30),
         excavator(w*0.34, hz, min(w, h)/620.0, '#ff5c00'),
         rubble(hz, w, PLANE['fore'][0], 7),
         ]
    return ''.join(g)

def powerplant(w, h, hz):
    ff, mf, nf = PLANE['far'][0], PLANE['mid'][0], PLANE['near'][0]
    return ''.join([
        f'<g filter="url(#soft)" opacity="0.7">',
        stack(w*0.78, hz, h*0.56, w*0.035, ff, True),
        block(w*0.60, hz, h*0.20, w*0.14, ff),
        '</g>',
        haze(hz - h*0.22, h*0.24, w, 0.15),
        cooling(w*0.05, hz, h*0.50, w*0.26, mf),
        block(w*0.40, hz, h*0.34, w*0.26, mf),
        haze(hz - h*0.09, h*0.12, w, 0.12),
        stack(w*0.72, hz, h*0.44, w*0.030, nf, True),
        silos(w*0.34, hz, h*0.16, w*0.026, 4, nf),
        f'<g stroke="{nf}" stroke-width="5" fill="none">'
        f'<path d="M{w*0.30:.0f} {hz-h*0.10:.0f}L{w*0.40:.0f} {hz-h*0.20:.0f}"/>'
        f'<path d="M{w*0.30:.0f} {hz-h*0.06:.0f}L{w*0.40:.0f} {hz-h*0.16:.0f}"/></g>',
        rubble(hz, w, PLANE['fore'][0], 3),
    ])

def millworks(w, h, hz):
    ff, mf, nf = PLANE['far'][0], PLANE['mid'][0], PLANE['near'][0]
    saw = ''.join(f'<path d="M{w*0.06 + i*w*0.075:.0f} {hz-h*0.26:.0f}'
                  f'l{w*0.037:.0f} -{h*0.07:.0f} {w*0.038:.0f} {h*0.07:.0f}z" fill="{mf}"/>'
                  for i in range(8))
    return ''.join([
        f'<g filter="url(#soft)" opacity="0.7">',
        stack(w*0.86, hz, h*0.48, w*0.028, ff, True),
        block(w*0.66, hz, h*0.24, w*0.16, ff),
        '</g>',
        haze(hz - h*0.20, h*0.22, w, 0.15),
        block(w*0.06, hz, h*0.26, w*0.60, mf), saw,
        tower_crane(w*0.80, hz, h*0.44, mf),
        haze(hz - h*0.08, h*0.11, w, 0.12),
        block(w*0.52, hz, h*0.34, w*0.13, nf, roof=int(h*0.03)),
        rubble(hz, w, PLANE['fore'][0], 11),
    ])

def tankfarm(w, h, hz):
    ff, mf, nf = PLANE['far'][0], PLANE['mid'][0], PLANE['near'][0]
    tanks = ''.join(f'<g><ellipse cx="{w*(0.10+i*0.135):.0f}" cy="{hz-h*0.20:.0f}" '
                    f'rx="{w*0.055:.0f}" ry="{h*0.022:.0f}" fill="{mf}"/>'
                    f'<rect x="{w*(0.10+i*0.135)-w*0.055:.0f}" y="{hz-h*0.20:.0f}" '
                    f'width="{w*0.11:.0f}" height="{h*0.20:.0f}" fill="{mf}"/></g>'
                    for i in range(5))
    return ''.join([
        f'<g filter="url(#soft)" opacity="0.7">',
        gantry(w*0.55, hz, h*0.30, w*0.30, ff),
        stack(w*0.12, hz, h*0.42, w*0.024, ff, True),
        '</g>',
        haze(hz - h*0.20, h*0.22, w, 0.16),
        tanks,
        f'<g stroke="{nf}" stroke-width="7" fill="none">'
        f'<path d="M0 {hz-h*0.06:.0f}h{w}"/><path d="M0 {hz-h*0.02:.0f}h{w}"/></g>',
        haze(hz - h*0.06, h*0.09, w, 0.10),
        excavator(w*0.76, hz, min(w, h)/760.0, '#ff5c00'),
        rubble(hz, w, PLANE['fore'][0], 5),
        hoarding(hz + h*0.13, w, '#161310'),
    ])

def yard(w, h, hz):
    mf, nf = PLANE['mid'][0], PLANE['near'][0]
    return ''.join([
        haze(hz - h*0.22, h*0.24, w, 0.14),
        block(w*0.04, hz, h*0.20, w*0.30, mf),
        block(w*0.40, hz, h*0.16, w*0.26, mf),
        tower_crane(w*0.76, hz, h*0.40, mf),
        haze(hz - h*0.08, h*0.11, w, 0.12),
        # stacked material and containers, the working end of a site
        ''.join(f'<rect x="{w*(0.06+i*0.075):.0f}" y="{hz-h*0.09:.0f}" '
                f'width="{w*0.065:.0f}" height="{h*0.09:.0f}" fill="{nf}"/>' for i in range(4)),
        f'<rect x="{w*0.44:.0f}" y="{hz-h*0.11:.0f}" width="{w*0.12:.0f}" '
        f'height="{h*0.11:.0f}" fill="#7e3418"/>',
        f'<rect x="{w*0.58:.0f}" y="{hz-h*0.10:.0f}" width="{w*0.11:.0f}" '
        f'height="{h*0.10:.0f}" fill="{nf}"/>',
        plume(w*0.26, hz, w*0.20, h*0.24),
        excavator(w*0.20, hz, min(w, h)/700.0, '#ff5c00'),
        rubble(hz, w, PLANE['fore'][0], 19),
        hoarding(hz + h*0.15, w, '#161310'),
    ])

SCENES = [
    ('hero.svg',        2400, 1250, 3,  demolition, 0.74),
    ('powerplant.svg',  1600, 1200, 5,  powerplant, 0.74),
    ('millworks.svg',   1600, 1000, 9,  millworks,  0.76),
    ('tankfarm.svg',    1600, 1000, 13, tankfarm,   0.76),
    ('demolition.svg',  1600, 1000, 17, demolition, 0.76),
    ('yard.svg',        1600, 1000, 23, yard,       0.76),
    ('site-wide.svg',   2400, 1000, 29, millworks,  0.78),
]

os.makedirs(OUT, exist_ok=True)
for name, w, h, seed, fn, hzr in SCENES:
    svg = scene(w, h, seed, fn, hzr)
    open(os.path.join(OUT, name), 'w').write(svg)
    print('%-18s %5d x %-5d %5.1f KB' % (name, w, h, len(svg)/1024))
