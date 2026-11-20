#!/usr/bin/env python3
"""Make the innermost thumb key (thumb_reachy) a vertical 1.5u, Corne-style, in an ergogen config.

The switch moves a quarter unit up its own axis so the cap grows toward the key block, the
keycaps/caps outlines get a 1.5u entry for it, and (Choc v1 only, --rotate) the switch turns 90 deg
under the cap, because a Choc v1 stem takes a cap one way round. MX-stem switches (Choc v2) don't
need turning. Ergogen mirrors adjust rotations on the right half, so the mirrored key gets -90,
which keeps the switch pins on the same side of the diode as on the left.

usage: python3 tools/tall_thumb.py <config.yaml> <row pitch mm> [--rotate]
Idempotent: a config that already has the tall key is left alone.
"""
import re, sys

path, pitch = sys.argv[1], float(sys.argv[2])
rotate = '--rotate' in sys.argv
s = open(path).read()
if 'thumb_reachy/' in s:
    print(f'{path}: already has the 1.5u thumb'); sys.exit(0)
extra = pitch / 2   # 0.5u

# key: shift up a quarter unit (local axis), tag its height
m = re.search(r'(        reachy:\n          key: \{[^\n]*?)(, column_net)', s)
assert m, 'reachy key not found'
kh = float(re.search(r'\n  keycaps:[^\n]*\n    - what: rectangle\n      where: true\n      size: \[[\d.]+, ([\d.]+)\]', s).group(1))
s = s[:m.start()] + m.group(1) + f', shift: [0, {extra / 2:g}], height: {kh + extra:g}' + m.group(2) + s[m.end():]

NOT_TALL, TALL = '/^(?!(mirror_)?thumb_reachy)/', '/^(mirror_)?thumb_reachy/'
for name in ('keycaps', 'caps'):
    m = re.search(rf'\n  {name}:[^\n]*\n    - what: rectangle\n      where: true\n      size: \[([\d.]+), ([\d.]+)\]', s)
    assert m, name
    w, h = float(m.group(1)), float(m.group(2))
    new = (m.group(0).replace('where: true', f'where: {NOT_TALL}') +
           f'\n    - what: rectangle\n      where: {TALL}\n      size: [{w:g}, {h + extra:g}]')
    s = s[:m.start()] + new + s[m.end():]

# switch footprints: the tall key gets its own entry (rotated for Choc v1)
L, R = ('/^thumb_reachy/', 90), ('/^mirror_thumb_reachy/', -90)
for where_all, where_main, talls in (
        ('/^(matrix|thumb)_/', '/^(matrix|thumb)_(?!reachy)/', [L]),
        ('/^mirror_/', '/^mirror_(?!thumb_reachy)/', [R]),
        ('/^(matrix|thumb|mirror)_/', '/^(?!(mirror_)?thumb_reachy)(matrix|thumb|mirror)_/', [L, R])):
    m = re.search(rf'      choc:\n        what: choc\n        where: {re.escape(where_all)}\n        params: (\{{[^\n]*\}})\n', s)
    assert m, where_all
    params = m.group(1)
    new = m.group(0).replace(f'where: {where_all}', f'where: {where_main}')
    for i, (wt, rot) in enumerate(talls):
        new += f'      choc_tall{i or ""}:\n        what: choc\n        where: {wt}\n'
        if rotate:
            new += f'        adjust: {{rotate: {rot}}}\n'
        new += f'        params: {params.replace("keycaps: true", "keycaps: false")}\n'
    s = s[:m.start()] + new + s[m.end():]
open(path, 'w').write(s)
print(f'{path}: 1.5u inner thumb added' + (' (switch rotated)' if rotate else ''))
