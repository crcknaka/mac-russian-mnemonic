#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generate docs/keyboard.svg — a diagram of the Russian – Mnemonic key map."""
import io, os

base = {
    'q':'я','w':'ш','e':'е','r':'р','t':'т','y':'ы','u':'у','i':'и','o':'о','p':'п',
    'a':'а','s':'с','d':'д','f':'ф','g':'г','h':'х','j':'й','k':'к','l':'л',"'":'ь',
    'z':'з','x':'ж','c':'ц','v':'в','b':'б','n':'н','m':'м','`':'ъ',
}
dead = {'y','s','j','c'}

rows = [
    (0.0,  ['q','w','e','r','t','y','u','i','o','p']),
    (0.45, ['a','s','d','f','g','h','j','k','l',"'"]),
    (0.95, ['z','x','c','v','b','n','m']),
]

U = 66          # cell pitch
KW = KH = 58    # key size
PADX, PADY = 26, 150
parts = []

def esc(s):
    return s.replace('&','&amp;').replace('<','&lt;').replace('>','&gt;')

for ri, (off, keys) in enumerate(rows):
    y = PADY + ri * U
    for ci, latin in enumerate(keys):
        x = PADX + (off + ci) * U
        cyr = base[latin]
        is_dead = latin in dead
        fill   = '#2563EB' if is_dead else '#f3f4f6'
        stroke = '#1d4ed8' if is_dead else '#d1d5db'
        cyr_c  = '#ffffff' if is_dead else '#111827'
        lat_c  = '#bfdbfe' if is_dead else '#9ca3af'
        parts.append(f'<rect x="{x}" y="{y}" width="{KW}" height="{KH}" rx="9" '
                     f'fill="{fill}" stroke="{stroke}" stroke-width="1.5"/>')
        parts.append(f'<text x="{x+8}" y="{y+17}" font-size="13" fill="{lat_c}" '
                     f'font-family="Menlo, monospace">{esc(latin)}</text>')
        parts.append(f'<text x="{x+KW/2}" y="{y+42}" font-size="26" fill="{cyr_c}" '
                     f'text-anchor="middle" font-weight="700" '
                     f'font-family="Helvetica, Arial, sans-serif">{esc(cyr)}</text>')
        if is_dead:
            parts.append(f'<text x="{x+KW-9}" y="{y+17}" font-size="13" fill="#ffffff" '
                         f'text-anchor="end">★</text>')

# backtick ъ key, sitting above-left of the first row
bx, by = PADX, PADY - U
parts.append(f'<rect x="{bx}" y="{by}" width="{KW}" height="{KH}" rx="9" '
             f'fill="#f3f4f6" stroke="#d1d5db" stroke-width="1.5"/>')
parts.append(f'<text x="{bx+8}" y="{by+17}" font-size="13" fill="#9ca3af" '
             f'font-family="Menlo, monospace">`</text>')
parts.append(f'<text x="{bx+KW/2}" y="{by+42}" font-size="26" fill="#111827" '
             f'text-anchor="middle" font-weight="700" '
             f'font-family="Helvetica, Arial, sans-serif">ъ</text>')

width = PADX*2 + 10*U
legend_y = PADY + 3*U + 24
legend = [
    ('★ dead keys', '#2563EB'),
    ('y/j → ы/й   ·   +a +e +u +o → я э ю ё', '#374151'),
    ('s → с   ·   s+ц=щ  s+х=ш        c → ц   ·   c+х=ч', '#374151'),
    ('Shift / Caps Lock → uppercase        ⌘ / Ctrl → Latin (⌘C ⌘V ⌘A)', '#6b7280'),
]
ly = legend_y
parts.append(f'<text x="{PADX}" y="{ly}" font-size="15" font-weight="700" '
             f'fill="#111827" font-family="Helvetica, Arial, sans-serif">How to type</text>')
for i,(txt,col) in enumerate(legend):
    parts.append(f'<text x="{PADX}" y="{ly+24+i*22}" font-size="13.5" fill="{col}" '
                 f'font-family="Helvetica, Arial, sans-serif">{esc(txt)}</text>')

height = ly + 24 + len(legend)*22 + 10
svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
       f'viewBox="0 0 {width} {height}" font-family="Helvetica, Arial, sans-serif">\n'
       f'<rect width="{width}" height="{height}" fill="#ffffff"/>\n'
       f'<text x="{PADX}" y="38" font-size="22" font-weight="700" fill="#111827">'
       f'Russian – Mnemonic — key map</text>\n'
       f'<text x="{PADX}" y="60" font-size="13" fill="#6b7280">Latin key (small) → Cyrillic letter (big). Blue = dead key.</text>\n'
       + '\n'.join(parts) + '\n</svg>\n')

os.makedirs('docs', exist_ok=True)
with io.open('docs/keyboard.svg','w',encoding='utf-8') as f:
    f.write(svg)
print('wrote docs/keyboard.svg (%d bytes)' % len(svg))
