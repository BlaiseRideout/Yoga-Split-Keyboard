#!/usr/bin/env python3
"""Write JLCPCB-style BOM and CPL (pick-and-place) CSVs for the SMD parts on a board.
usage: gen_fab.py board.kicad_pcb out_prefix      (run with KiCad's python)

Only parts that suit machine assembly are listed: diodes, Choc hotswap sockets, power switch, reset
button and the charge-link fuse and resistor. The nice!nano, nice!view, battery, pogo connector and
switches are hand-fitted.
LCSC numbers marked '?' were not verified against the LCSC catalogue: check them before ordering."""
import sys, csv, collections, pcbnew

src, prefix = sys.argv[1:3]
b = pcbnew.LoadBoard(src)

PARTS = {  # footprint name -> (comment, footprint label, LCSC)
    'D_SOD-123': ('1N4148W', 'SOD-123', 'C81598'),
    'PG1350': ('Kailh Choc hotswap socket CPG135001S30', 'Choc_Hotswap', '?'),
    'SW_MSK12C02': ('MSK-12C02 side slide switch', 'SW_MSK12C02', 'C431540?'),
    'E73:SW_TACT_ALPS_SKQGABE010': ('Alps SKQGABE010 tact switch', 'SKQG', '?'),
    # charge link (split halves only); the pogo connector itself is hand-fitted
    'SMD_1206:10R': ('10R 1206 0.25W resistor', '1206', 'C17903?'),
    'SMD_1206:PTC': ('PTC resettable fuse 1206, 0.1 A hold', '1206', 'C70069?'),
}

rows, groups = [], collections.defaultdict(list)
for fp in b.GetFootprints():
    name = str(fp.GetFPID().GetLibItemName())
    lib = str(fp.GetFPID().GetLibNickname())
    key = f'{lib}:{name}' if lib else name
    if name == 'SMD_1206':
        key = 'SMD_1206:' + ('PTC' if 'PTC' in fp.GetValue() else '10R')
    if key not in PARTS and name not in PARTS or (name == 'SMD_1206' and key not in PARTS):
        continue
    part = PARTS.get(key) or PARTS[name]
    ref = fp.GetReference()
    if name == 'PG1350':
        ref = ref.replace('S', 'HS', 1)  # the socket is the assembled part, the switch is hand-fitted
    pos = fp.GetPosition()
    side = 'bottom' if name == 'PG1350' or fp.IsFlipped() or fp.GetLayer() == pcbnew.B_Cu else 'top'
    rows.append([ref, f'{pcbnew.ToMM(pos.x):.3f}mm', f'{-pcbnew.ToMM(pos.y):.3f}mm', side,
                 f'{fp.GetOrientationDegrees():.1f}'])
    groups[part].append(ref)

with open(prefix + '-cpl.csv', 'w', newline='') as f:
    w = csv.writer(f); w.writerow(['Designator', 'Mid X', 'Mid Y', 'Layer', 'Rotation']); w.writerows(rows)
with open(prefix + '-bom.csv', 'w', newline='') as f:
    w = csv.writer(f); w.writerow(['Comment', 'Designator', 'Footprint', 'LCSC Part #', 'Qty'])
    for (c, fpn, lcsc), refs in groups.items():
        w.writerow([c, ','.join(refs), fpn, lcsc, len(refs)])
print(prefix, len(rows), 'placements')
