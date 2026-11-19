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
POWER = ('GND', 'RAW', 'BAT_P', 'VCC', 'LINK_F', 'LINK_B')
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
open(dsn, 'w').write(t)
print('power nets', moved)
