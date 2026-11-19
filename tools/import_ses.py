#!/usr/bin/env python3
"""Import a Freerouting session (.ses) into a board, save it, and print a DRC summary.
KiCad 7's pcbnew.ImportSpecctraSES only works inside the GUI, so this parses the SES itself.
usage: import_ses.py board.kicad_pcb routes.ses drc_report.txt     (run with KiCad's python, KiCad >= 7)"""
import re, sys, pcbnew

board, ses, rpt = sys.argv[1:4]
b = pcbnew.LoadBoard(board)

def parse(text):
    toks = re.findall(r'\(|\)|"[^"]*"|[^\s()]+', text)
    stack = [[]]
    for t in toks:
        if t == '(':
            stack.append([])
        elif t == ')':
            x = stack.pop(); stack[-1].append(x)
        else:
            stack[-1].append(t.strip('"'))
    return stack[0][0]

def find(node, key):
    return [c for c in node[1:] if isinstance(c, list) and c and c[0] == key]

tree = parse(open(ses).read())
routes = find(tree, 'routes')[0]
res = find(routes, 'resolution')[0]
scale = {'um': 1e3, 'mm': 1e6, 'mil': 25400.0, 'inch': 25.4e6}[res[1]] / float(res[2])  # -> nm
pt = lambda x, y: pcbnew.VECTOR2I(int(round(float(x) * scale)), int(round(-float(y) * scale)))

vias = {}
for ps in find(find(routes, 'library_out')[0], 'padstack') if find(routes, 'library_out') else []:
    m = re.search(r'_(\d+):(\d+)_um', ps[1])
    if m:
        vias[ps[1]] = (int(m.group(1)) * 1000, int(m.group(2)) * 1000)

layers = {'F.Cu': pcbnew.F_Cu, 'B.Cu': pcbnew.B_Cu}
for t in list(b.GetTracks()):
    b.Remove(t)
nw = nv = 0
for net in find(find(routes, 'network_out')[0], 'net'):
    ni = b.FindNet(net[1])
    for w in find(net, 'wire'):
        path = find(w, 'path')[0]
        layer, width, coords = path[1], float(path[2]) * scale, path[3:]
        p = [pt(coords[i], coords[i + 1]) for i in range(0, len(coords), 2)]
        for a, c in zip(p, p[1:]):
            t = pcbnew.PCB_TRACK(b)
            t.SetStart(a); t.SetEnd(c); t.SetWidth(int(width)); t.SetLayer(layers[layer]); t.SetNet(ni)
            b.Add(t); nw += 1
    for v in find(net, 'via'):
        d, drill = vias.get(v[1], (600000, 300000))
        via = pcbnew.PCB_VIA(b)
        via.SetPosition(pt(v[2], v[3])); via.SetWidth(d); via.SetDrill(drill); via.SetNet(ni)
        via.SetLayerPair(pcbnew.F_Cu, pcbnew.B_Cu)
        b.Add(via); nv += 1

pcbnew.SaveBoard(board, b)
b = pcbnew.LoadBoard(board)
pcbnew.WriteDRCReport(b, rpt, pcbnew.EDA_UNITS_MILLIMETRES, True)
txt = open(rpt).read()
errs = [x for x in txt.split('\n[')[1:] if 'Severity: error' in x and not x.startswith(('lib_footprint', 'unconnected_items'))]
unrouted = [l for l in txt.splitlines() if l.startswith('** Found') and 'unconnected' in l]
print(board, f'segments {nw} vias {nv} | DRC errors {len(errs)} |', unrouted[0] if unrouted else '')
for e in errs[:8]:
    print('  [' + e[:300].replace('\n', ' | '))
