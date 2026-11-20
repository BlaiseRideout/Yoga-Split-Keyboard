#!/usr/bin/env python3
"""Set design rules on an ergogen-generated board and export a Specctra DSN for Freerouting.
usage: prep_dsn.py in.kicad_pcb out.kicad_pcb out.dsn   (run with KiCad's python, KiCad >= 7)"""
import sys, pcbnew
src, dst, dsn = sys.argv[1:4]
b = pcbnew.LoadBoard(src)
ds = b.GetDesignSettings()
ds.SetCopperLayerCount(2)
b.SetCopperLayerCount(2)
ds.m_TrackMinWidth = pcbnew.FromMM(0.2)
ds.m_MinClearance = pcbnew.FromMM(0.2)
ds.m_ViasMinSize = pcbnew.FromMM(0.6)
ds.m_MinThroughDrill = pcbnew.FromMM(0.3)
ns = ds.m_NetSettings
dflt = ns.m_DefaultNetClass
dflt.SetTrackWidth(pcbnew.FromMM(0.25)); dflt.SetClearance(pcbnew.FromMM(0.2))
dflt.SetViaDiameter(pcbnew.FromMM(0.6)); dflt.SetViaDrill(pcbnew.FromMM(0.3))
pwr = pcbnew.NETCLASS('Power')
pwr.SetTrackWidth(pcbnew.FromMM(0.4)); pwr.SetClearance(pcbnew.FromMM(0.2))
pwr.SetViaDiameter(pcbnew.FromMM(0.8)); pwr.SetViaDrill(pcbnew.FromMM(0.4))
ns.m_NetClasses['Power'] = pwr
# The thin build's on-board module has 0.8 mm-pitch pads that only escape outwards, so its boards use
# 0.2 mm tracks with 0.15 mm gaps (JLC's standard 2-layer process does 0.1 / 0.1).
if any(str(f.GetFPID().GetLibItemName()) == 'Raytac_MDBT50Q' for f in b.GetFootprints()):
    ds.m_TrackMinWidth = pcbnew.FromMM(0.15); ds.m_MinClearance = pcbnew.FromMM(0.15)
    dflt.SetTrackWidth(pcbnew.FromMM(0.2)); dflt.SetClearance(pcbnew.FromMM(0.15)); pwr.SetClearance(pcbnew.FromMM(0.15))
POWER = ('GND', 'RAW', 'BAT_P', 'VCC', 'LINK_F', 'LINK_B', 'VBUS', 'SW_OUT')

# On-board nRF52840 module (thin build): an all-copper keep-out at the antenna end, per the KiCad library
# footprint (moved 0.2 mm off the antenna-end pads so Freerouting's 0.2 mm clearance to it holds), and a
# named rule area around the mid-mount USB-C so the edge rule below can let its tracks near the notch.
import os
def local_pt(fp, x, y):
    v = pcbnew.VECTOR2I(pcbnew.FromMM(x), pcbnew.FromMM(y))
    v = pcbnew.VECTOR2I(int(v.x), int(v.y))
    a = fp.GetOrientation().AsRadians()
    import math
    c, s_ = math.cos(a), math.sin(a)
    p0 = fp.GetPosition()
    return pcbnew.VECTOR2I(int(p0.x + v.x * c + v.y * s_), int(p0.y - v.x * s_ + v.y * c))
has_module = False
for fp in list(b.GetFootprints()):
    if str(fp.GetFPID().GetLibItemName()) != 'Raytac_MDBT50Q':
        continue
    has_module = True
    for (x0, y0, x1, y1), lyr in (((-6.2, -7.75, 6.2, -4.2), (pcbnew.F_Cu, pcbnew.B_Cu)),
                                  ((-2.3, -3.95, -0.7, -2.75), (pcbnew.F_Cu,))):
        z = pcbnew.ZONE(b); o = z.Outline(); o.NewOutline()
        for x, y in ((x0, y0), (x1, y0), (x1, y1), (x0, y1)):
            q = local_pt(fp, x, y); o.Append(q.x, q.y)
        z.SetIsRuleArea(True)
        for f in (z.SetDoNotAllowCopperPour, z.SetDoNotAllowTracks, z.SetDoNotAllowVias, z.SetDoNotAllowPads):
            f(True)
        z.SetDoNotAllowFootprints(False)
        ls = pcbnew.LSET()
        for l in lyr: ls.AddLayer(l)
        z.SetLayerSet(ls); z.SetZoneName('antenna_keepout'); b.Add(z)
for fp in list(b.GetFootprints()):
    if 'C168688' not in str(fp.GetFPID().GetLibItemName()):
        continue
    bb = None
    for pd in fp.Pads():
        if bb is None: bb = pd.GetBoundingBox()
        else: bb.Merge(pd.GetBoundingBox())
    bb.Inflate(pcbnew.FromMM(1.0))
    z = pcbnew.ZONE(b); o = z.Outline(); o.NewOutline()
    for x, y in ((bb.GetLeft(), bb.GetTop()), (bb.GetRight(), bb.GetTop()), (bb.GetRight(), bb.GetBottom()), (bb.GetLeft(), bb.GetBottom())):
        o.Append(x, y)
    z.SetIsRuleArea(True)
    for f in (z.SetDoNotAllowCopperPour, z.SetDoNotAllowTracks, z.SetDoNotAllowVias, z.SetDoNotAllowPads, z.SetDoNotAllowFootprints):
        f(False)
    ls = pcbnew.LSET(); ls.AddLayer(pcbnew.F_Cu); ls.AddLayer(pcbnew.B_Cu)
    z.SetLayerSet(ls); z.SetZoneName('usb_area'); b.Add(z)
if has_module:
    b.GetDesignSettings().m_CopperEdgeClearance = 0
    open(os.path.splitext(dst)[0] + '.kicad_dru', 'w').write('''(version 1)
# 0.5 mm copper to board edge everywhere (the board setup minimum is 0 on these boards, so that) ...
(rule "edge"
  (constraint edge_clearance (min 0.5mm)))
# small 0805/SOT-23 GND pads in the crowded controller area may get one thermal spoke instead of two
(rule "thermal spokes"
  (constraint min_resolved_spokes 1)
  (condition "A.NetName == 'GND'"))
# ... the mid-mount USB-C's pads and shell tabs run up to its notch and the back edge, as the footprint intends.
(rule "usb-c notch"
  (constraint edge_clearance (min 0.05mm))
  (condition "A.Type == 'Pad' && (A.Pad_Number == 'A*' || A.Pad_Number == 'B*' || A.Pad_Number == 'S*')"))
# ... and the tracks leaving those pads may come 0.2 mm from the notch (Freerouting's clearance)
(rule "usb-c tracks"
  (constraint edge_clearance (min 0.15mm))
  (condition "A.Type != 'Pad' && A.insideArea('usb_area')"))
''')
pcbnew.SaveBoard(dst, b)
# KiCad 7's python API doesn't expose netclass patterns, and ergogen pins every net to Default.
# So: rewrite the project file's patterns, then set the class on each power net for the DSN export.
import json, os
pro = os.path.splitext(dst)[0] + '.kicad_pro'
d = json.load(open(pro))
for a in d['net_settings'].get('netclass_patterns') or []:
    if a['pattern'] in POWER: a['netclass'] = 'Power'
json.dump(d, open(pro, 'w'), indent=2)
b = pcbnew.LoadBoard(dst)
pc = b.GetDesignSettings().m_NetSettings.m_NetClasses['Power']
for n in POWER:
    net = b.FindNet(n)
    if net: net.SetNetClass(pc)
for z in list(b.Zones()):   # the DSN exporter would make the (permission-only) USB rule area a keep-out
    if z.GetIsRuleArea() and z.GetZoneName() == 'usb_area': b.Remove(z)
ok = pcbnew.ExportSpecctraDSN(b, dsn)
print('dsn export', ok)
# The DSN exporter groups nets by the project file's patterns, which a bare LoadBoard doesn't read,
# so move the power nets into the Power class in the DSN text (Freerouting then routes them 0.4 mm).
import re
t = open(dsn).read()
m = re.search(r'\(class kicad_default ((?:[^()]|\n)*?)\n\s*\(circuit', t)
names = m.group(1).split()
keep = [n for n in names if n not in POWER]
moved = [n for n in names if n in POWER]
t = t[:m.start(1)] + ' '.join(keep) + t[m.end(1):]
t = t.replace('(class Power\n', '(class Power ' + ' '.join(moved) + '\n', 1)
# Freerouting rounds angled tracks a little under the clearance; give it 5 um of slack on the 0.15 mm boards
t = t.replace('(clearance 150.1', '(clearance 155')
open(dsn, 'w').write(t)
print('power nets', moved)
# Freerouting keeps wires only the default clearance (0.2 mm) from the board edge, under the 0.5 mm
# edge rule, which shows up on the join edges. Add a 0.45 mm wire keep-out band inside the outline.
try:
    from shapely.geometry import Polygon, box
    m = re.search(r'\(boundary\s*\(path pcb 0\s+([-\d.\s]+)\)', t)
    v = [float(x) for x in m.group(1).split()]
    poly = Polygon(list(zip(v[0::2], v[1::2])))
    band = poly.difference(poly.buffer(-450, join_style=2))
    # ... except where a part's pads are meant to reach the edge (the mid-mount USB-C in its notch)
    for fp in b.GetFootprints():
        if 'C168688' not in str(fp.GetFPID().GetLibItemName()):
            continue
        for pd in fp.Pads():
            bb = pd.GetBoundingBox()
            x0_, x1_ = pcbnew.ToMM(bb.GetLeft()) * 1000, pcbnew.ToMM(bb.GetRight()) * 1000
            y0_, y1_ = -pcbnew.ToMM(bb.GetBottom()) * 1000, -pcbnew.ToMM(bb.GetTop()) * 1000
            band = band.difference(box(x0_ - 250, y0_ - 250, x1_ + 250, y1_ + 250))
    x0, y0, x1, y1 = poly.bounds; xm, ym = (x0 + x1) / 2, (y0 + y1) / 2
    kos = []
    for q in (box(x0 - 1, y0 - 1, xm, ym), box(xm, y0 - 1, x1 + 1, ym), box(x0 - 1, ym, xm, y1 + 1), box(xm, ym, x1 + 1, y1 + 1)):
        piece = band.intersection(q)
        for g in getattr(piece, 'geoms', [piece]):
            if g.geom_type != 'Polygon' or g.is_empty: continue
            pts = ' '.join(f'{x:.1f} {y:.1f}' for x, y in g.exterior.coords)
            kos.append(f'    (keepout "" (polygon signal 0 {pts}))')
    i = t.index('(boundary')
    t = t[:i] + '\n'.join(kos).strip() + '\n    ' + t[i:]
    open(dsn, 'w').write(t)
    print('edge keep-outs', len(kos))
except ImportError:
    print('shapely missing: no edge keep-outs')
