#!/usr/bin/env python3
"""Add GND pours on both layers, a no-pour area over the controller, and stitching vias, then DRC.
usage: add_ground.py board.kicad_pcb drc_report.txt     (run with KiCad's python, KiCad >= 7)
Run after import_ses.py. Re-running replaces the zones and stitching vias it added before."""
import sys, math, pcbnew
board, rpt = sys.argv[1:3]
mm, to = pcbnew.FromMM, pcbnew.ToMM
b = pcbnew.LoadBoard(board)
gnd = b.FindNet('GND')

# start clean: drop earlier zones and stitching vias (locked 0.6 mm GND vias)
old = [t for t in b.GetTracks()
       if t.GetClass() == 'PCB_VIA' and t.GetNetname() == 'GND' and t.GetWidth() == mm(0.6) and t.IsLocked()]
old += [z for z in b.Zones()]
for item in old:
    b.Remove(item)

# Remove dangling track stubs the router left behind.
b.BuildConnectivity()
c = b.GetConnectivity()
dang = [t for t in b.GetTracks() if t.GetClass() == 'PCB_TRACK' and c.TestTrackEndpointDangling(t, False)]
for t in dang:
    b.Remove(t)
nd = len(dang)
gnd = b.FindNet('GND')

def layers(*ls):
    s = pcbnew.LSET()
    for l in ls:
        s.AddLayer(l)
    return s

def rect_zone(x0, y0, x1, y1):
    z = pcbnew.ZONE(b)
    o = z.Outline(); o.NewOutline()
    for x, y in ((x0, y0), (x1, y0), (x1, y1), (x0, y1)):
        o.Append(mm(x), mm(y))
    return z

e = b.GetBoardEdgesBoundingBox()
X0, Y0, X1, Y1 = [to(v) for v in (e.GetLeft(), e.GetTop(), e.GetRight(), e.GetBottom())]
for layer, name in ((pcbnew.F_Cu, 'GND_F'), (pcbnew.B_Cu, 'GND_B')):
    z = rect_zone(X0 - 1, Y0 - 1, X1 + 1, Y1 + 1)   # the fill is clipped to the board edge
    z.SetLayerSet(layers(layer)); z.SetNet(gnd); z.SetZoneName(name)
    z.SetLocalClearance(mm(0.3)); z.SetMinThickness(mm(0.25))
    # Thermal reliefs so the GND pads stay easy to hand-solder.
    z.SetPadConnection(pcbnew.ZONE_CONNECTION_THERMAL)
    z.SetThermalReliefGap(mm(0.5)); z.SetThermalReliefSpokeWidth(mm(0.5))
    # keep islands for the first fill, so stitching vias can land on them (removed after)
    z.SetIslandRemovalMode(pcbnew.ISLAND_REMOVAL_MODE_NEVER)
    b.Add(z)

# No pour under the controller (keeps copper away from its antenna) or within 2 mm of it.
m = b.FindFootprintByReference('MCU1').GetBoundingBox(False, False)
k = rect_zone(to(m.GetLeft()) - 2, to(m.GetTop()) - 2, to(m.GetRight()) + 2, to(m.GetBottom()) + 2)
k.SetIsRuleArea(True); k.SetDoNotAllowCopperPour(True)
k.SetDoNotAllowTracks(False); k.SetDoNotAllowVias(False); k.SetDoNotAllowPads(False); k.SetDoNotAllowFootprints(False)
k.SetLayerSet(layers(pcbnew.F_Cu, pcbnew.B_Cu)); k.SetZoneName('no_pour_controller')
b.Add(k)

filler = pcbnew.ZONE_FILLER(b)
filler.Fill(b.Zones())

# Stitching vias on a 6 mm grid wherever both pours have solid copper 1 mm around the spot.
fills = [z.GetFilledPolysList(z.GetLayerSet().Seq()[0]) for z in b.Zones() if not z.GetIsRuleArea()]
def solid(x, y):
    pts = [(x, y)] + [(x + math.cos(i * math.pi / 4), y + math.sin(i * math.pi / 4)) for i in range(8)]
    return all(f.Contains(pcbnew.VECTOR2I(mm(px), mm(py))) for f in fills for px, py in pts)
nv = 0
y = Y0 + 4
while y < Y1 - 3:
    x = X0 + 4
    while x < X1 - 3:
        if solid(x, y):
            v = pcbnew.PCB_VIA(b); v.SetPosition(pcbnew.VECTOR2I(mm(x), mm(y)))
            v.SetWidth(mm(0.6)); v.SetDrill(mm(0.3)); v.SetNet(gnd); v.SetLocked(True)
            v.SetLayerPair(pcbnew.F_Cu, pcbnew.B_Cu); b.Add(v); nv += 1
        x += 6
    y += 6
for z in b.Zones():
    if not z.GetIsRuleArea():
        z.SetIslandRemovalMode(pcbnew.ISLAND_REMOVAL_MODE_ALWAYS)
filler.Fill(b.Zones())
pcbnew.SaveBoard(board, b)

# DRC. A GND pad whose thermal relief only gets one spoke (tracks in the way) is connected solid
# instead; it's a small pad, so it still solders fine. Then check again.
import os, re
for attempt in range(4):
    b = pcbnew.LoadBoard(board)
    if os.path.exists(rpt): os.remove(rpt)
    if not pcbnew.WriteDRCReport(b, rpt, pcbnew.EDA_UNITS_MILLIMETRES, True):
        sys.exit('DRC failed to run')
    txt = open(rpt).read()
    starved = re.findall(r'\[starved_thermal\].*?PTH pad (\S+) \[GND\] of (\S+)', txt, re.S)
    if not starved or attempt == 3:
        break
    for num, ref in starved:
        for pad in b.FindFootprintByReference(ref).Pads():
            if pad.GetNumber() == num:
                pad.SetZoneConnection(pcbnew.ZONE_CONNECTION_FULL)
    pcbnew.ZONE_FILLER(b).Fill(b.Zones())
    pcbnew.SaveBoard(board, b)
errs = [x for x in txt.split('\n[')[1:] if 'Severity: error' in x and not x.startswith(('lib_footprint', 'unconnected_items'))]
unrouted = [l for l in txt.splitlines() if l.startswith('** Found') and 'unconnected' in l]
print(board, f'stubs removed {nd} | stitching vias {nv} | DRC errors {len(errs)} |', unrouted[0] if unrouted else '')
for e in errs[:8]:
    print('  [' + e[:300].replace('\n', ' | '))
