"""Build the 呼吸環 app icon (direction B) as SVG, then rasterize every size needed."""
import base64, math, os, sys
import resvg_py

OUT = sys.argv[1]
os.makedirs(OUT, exist_ok=True)

BG, CELADON, AMBER, PALE = "#0C1517", "#86C4B7", "#E3A75E", "#DAE5E2"
C, R = 512, 330            # ring centre / radius on a 1024 canvas; outer edge stays inside the 80% maskable safe zone
PHASES = [(4, CELADON, 1.0), (7, PALE, 0.32), (8, AMBER, 1.0)]   # the 4-7-8 cycle from the breathing page
GAP = 9                    # degrees between arcs (before round caps)


def pt(deg, r=R):
    a = math.radians(deg - 90)
    return C + r * math.cos(a), C + r * math.sin(a)


def arcs(stroke):
    total, start, out = sum(p[0] for p in PHASES), 0.0, []
    for secs, colour, op in PHASES:
        span = secs / total * 360
        a0, a1 = start + GAP / 2, start + span - GAP / 2
        (x0, y0), (x1, y1) = pt(a0), pt(a1)
        large = 1 if a1 - a0 > 180 else 0
        out.append(f'<path d="M{x0:.1f} {y0:.1f} A{R} {R} 0 {large} 1 {x1:.1f} {y1:.1f}" fill="none" '
                   f'stroke="{colour}" stroke-opacity="{op}" stroke-width="{stroke}" stroke-linecap="round"/>')
        start += span
    return "\n  ".join(out)


def svg(corner=0, stroke=34, dot=True):
    dx, dy = pt(4 / 19 * 360 * 0.62)          # progress dot, part-way through the inhale
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1024 1024">
  <defs>
    <radialGradient id="halo" cx="50%" cy="50%" r="50%">
      <stop offset="0" stop-color="{CELADON}" stop-opacity="0.30"/>
      <stop offset="0.6" stop-color="{CELADON}" stop-opacity="0.10"/>
      <stop offset="1" stop-color="{CELADON}" stop-opacity="0"/>
    </radialGradient>
  </defs>
  <rect width="1024" height="1024" rx="{corner}" fill="{BG}"/>
  <circle cx="{C}" cy="{C}" r="250" fill="url(#halo)"/>
  {arcs(stroke)}
  <circle cx="{C}" cy="{C}" r="156" fill="{CELADON}" fill-opacity="0.2" stroke="{CELADON}" stroke-width="10"/>
  <circle cx="{C}" cy="{C}" r="100" fill="none" stroke="{CELADON}" stroke-opacity="0.38" stroke-width="6"/>
  {f'<circle cx="{dx:.1f}" cy="{dy:.1f}" r="24" fill="{PALE}"/>' if dot else ''}
</svg>
'''


full = svg()                                   # full-bleed: the OS applies its own mask
fav = svg(corner=220, stroke=56, dot=False)    # browser tab: rounded, heavier strokes for 16–32 px

open(os.path.join(OUT, "icon.svg"), "w", encoding="utf-8").write(full)
open(os.path.join(OUT, "favicon.svg"), "w", encoding="utf-8").write(fav)

for name, size, src in [("icon-1024.png", 1024, full), ("icon-512.png", 512, full), ("icon-192.png", 192, full),
                        ("apple-touch-icon.png", 180, full), ("favicon-32.png", 32, fav)]:
    png = resvg_py.svg_to_bytes(svg_string=src, width=size, height=size)
    open(os.path.join(OUT, name), "wb").write(bytes(png) if not isinstance(png, str) else base64.b64decode(png))
    print(name, size)
