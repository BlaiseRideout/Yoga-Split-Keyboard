#!/usr/bin/env python3
"""Check that a board's key matrix supports full n-key rollover with ZMK col2row scanning:
every switch has exactly one diode of its own, switch pin -> diode anode, diode cathode -> row net,
and no two keys share a (row, column) position or an intermediate net.
usage: check_matrix.py board.kicad_pcb [...]      (run with KiCad's python)"""
import sys, collections, pcbnew

ok_all = True
for f in sys.argv[1:]:
    b = pcbnew.LoadBoard(f)
    pads_by_net = collections.defaultdict(list)
    switches, diodes = [], {}
    for fp in b.GetFootprints():
        ref = fp.GetReference()
        for p in fp.Pads():
            if p.GetNetname():
                pads_by_net[p.GetNetname()].append((ref, p.GetNumber()))
        if ref.startswith('S') and not ref.startswith('SW'):
            switches.append(fp)
        if ref.startswith('D') and not ref.startswith('DISP'):
            diodes[ref] = {p.GetNumber(): p.GetNetname() for p in fp.Pads() if p.GetNetname()}
    errs, seen = [], {}
    for sw in switches:
        nets = sorted({p.GetNetname() for p in sw.Pads() if p.GetNetname()})
        cols = [n for n in nets if n.startswith(('C', 'MC')) and n[-1].isdigit() and n.lstrip('MC').isdigit()]
        mids = [n for n in nets if n not in cols]
        if len(cols) != 1 or len(mids) != 1:
            errs.append(f'{sw.GetReference()}: nets {nets}'); continue
        mid = mids[0]
        on_mid = [r for r, _ in pads_by_net[mid] if r != sw.GetReference()]
        ds = sorted(set(r for r in on_mid if r in diodes))
        if len(ds) != 1 or len(set(on_mid)) != 1:
            errs.append(f'{sw.GetReference()}: net {mid} also on {sorted(set(on_mid))}'); continue
        d = diodes[ds[0]]
        if d.get('2') != mid:   # pad 2 = anode on both diode footprints
            errs.append(f'{sw.GetReference()}: diode {ds[0]} reversed (anode on {d.get("2")})'); continue
        row = d.get('1')
        if not row or not row.lstrip('M').startswith('R'):
            errs.append(f'{sw.GetReference()}: diode {ds[0]} cathode on {row}, not a row'); continue
        key = (row, cols[0])
        if key in seen:
            errs.append(f'{sw.GetReference()} and {seen[key]} share matrix position {key}')
        seen[key] = sw.GetReference()
    print(f'{f}: {len(switches)} switches, {len(diodes)} diodes, {len(seen)} unique (row, col) positions, '
          f'{"OK" if not errs else str(len(errs)) + " problems"}')
    for e in errs[:10]:
        print('   ', e)
    ok_all &= not errs and len(switches) == len(diodes) == len(seen)
sys.exit(0 if ok_all else 1)
