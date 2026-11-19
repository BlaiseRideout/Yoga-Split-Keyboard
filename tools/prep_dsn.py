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
for n in ('GND', 'RAW', 'BAT_P', 'VCC'):
    ns.m_NetClassPatternAssignments.push_back(pcbnew.NETCLASS_PATTERN_ASSIGNMENT_PTR(pcbnew.EDA_COMBINED_MATCHER(n, pcbnew.CTX_NETCLASS), 'Power')) if hasattr(pcbnew,'NETCLASS_PATTERN_ASSIGNMENT_PTR') else None
    ns.SetNetclassPatternAssignment(n, 'Power') if hasattr(ns,'SetNetclassPatternAssignment') else None
b.SynchronizeNetsAndNetClasses(True) if hasattr(b,'SynchronizeNetsAndNetClasses') else None
pcbnew.SaveBoard(dst, b)
b = pcbnew.LoadBoard(dst)
ok = pcbnew.ExportSpecctraDSN(b, dsn)
print('dsn export', ok)
