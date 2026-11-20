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
    # thin build (pcb-thin/): everything is machine-placed on the top side
    'PG1316S': ('Kailh PG1316S switch (consign if LCSC has none)', 'PG1316S', '?'),
    'TVS': ('SMF10A TVS diode, SOD-123FL', 'SOD-123FL', '?'),
    'SMD_0805_LED:red': ('red LED 0805', '0805', '?'),
    'SMD_0805_LED:green': ('green LED 0805', '0805', '?'),
    'SMD_0805_LED:blue': ('blue LED 0805', '0805', '?'),
    'SMD_0805:680R': ('680R 0805 resistor', '0805', '?'),
    'SMD_0805:150R': ('150R 0805 resistor', '0805', '?'),
    # thin build's on-board controller (tools/make_thin.py controller()); check rotations in JLC's preview
    'Raytac_MDBT50Q': ('Raytac MDBT50Q-1MV2 nRF52840 module', 'SMD-61P', 'C5118826'),
    'USB_C_C168688': ('USB-C 16P mid-mount receptacle 918-418K2024S40000', 'USB-C-SMD_16P', 'C168688'),
    'SOT-23:TP4054': ('TP4054 Li-ion charger', 'SOT-23-5', 'C32574'),
    'SOT-23:USBLC6-2SC6': ('USBLC6-2SC6 USB ESD clamp', 'SOT-23-6', 'C7519'),
    'SOT-23-3:AO3401A': ('AO3401A P-MOSFET', 'SOT-23', 'C15127?'),
    'D_SOD-123:B5819W': ('B5819W Schottky diode', 'SOD-123', '?'),
    'Crystal_3215': ('32.768 kHz crystal 12.5 pF, Epson Q13FC13500004', '3215', 'C32346'),
    'SMD_0805:5.1k': ('5.1k 0805 resistor', '0805', '?'),
    'SMD_0805:10k': ('10k 0805 resistor', '0805', '?'),
    'SMD_0805:100k': ('100k 0805 resistor', '0805', '?'),
    'SMD_0805:4.7uF': ('4.7uF 0805 X5R capacitor, 10 V or more', '0805', '?'),
    'SMD_0805:20pF': ('20pF 0805 C0G capacitor', '0805', '?'),
}

rows, groups = [], collections.defaultdict(list)
for fp in b.GetFootprints():
    name = str(fp.GetFPID().GetLibItemName())
    lib = str(fp.GetFPID().GetLibNickname())
    key = f'{lib}:{name}' if lib else name
    if name == 'SMD_1206':
        key = 'SMD_1206:' + ('PTC' if 'PTC' in fp.GetValue() else '10R')
    if name == 'D_SOD-123' and any(pd.GetNetname() == 'LINK_B' for pd in fp.Pads()):
        key = name = 'TVS'
    if name.startswith('SMD_0805') or name in ('SOT-23', 'SOT-23-3'):
        key = name + ':' + fp.GetValue().split()[0]
    if name == 'D_SOD-123' and fp.GetValue() != '1N4148W' and key != 'TVS':
        key = name + ':' + fp.GetValue()
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
