// SOT-23 (3-pin) land pattern from the KiCad library: pin 1 top left, pin 2 bottom left, pin 3 right.
// For a MOSFET such as the AO3401A: 1 = gate, 2 = source, 3 = drain.
module.exports = {
  params: { designator: 'Q', value: '', P1: {type: 'net', value: ''}, P2: {type: 'net', value: ''}, P3: {type: 'net', value: ''} },
  body: p => `
  (module SOT-23-3 (layer F.Cu) (tedit 6500000)
    ${p.at}
    (attr smd)
    (fp_text reference "${p.ref}" (at 0 -2.4 ${p.r}) (layer F.SilkS) ${p.ref_hide} (effects (font (size 0.8 0.8) (thickness 0.12))))
    (fp_text value "${p.value}" (at 0 2.4 ${p.r}) (layer F.Fab) (effects (font (size 0.8 0.8) (thickness 0.12))))
    (fp_line (start -0.7 -1.5) (end 0.7 -1.5) (layer F.Fab) (width 0.1))
    (fp_line (start 0.7 -1.5) (end 0.7 1.5) (layer F.Fab) (width 0.1))
    (fp_line (start 0.7 1.5) (end -0.7 1.5) (layer F.Fab) (width 0.1))
    (fp_line (start -0.7 1.5) (end -0.7 -1.5) (layer F.Fab) (width 0.1))
    (fp_circle (center -1.9 -1.6) (end -1.75 -1.6) (layer F.SilkS) (width 0.25))
    (pad 1 smd roundrect (at -1.1375 -0.95 ${p.r}) (size 1.325 0.6) (layers F.Cu F.Paste F.Mask) (roundrect_rratio 0.25) ${p.P1})
    (pad 2 smd roundrect (at -1.1375 0.95 ${p.r}) (size 1.325 0.6) (layers F.Cu F.Paste F.Mask) (roundrect_rratio 0.25) ${p.P2})
    (pad 3 smd roundrect (at 1.1375 0 ${p.r}) (size 1.325 0.6) (layers F.Cu F.Paste F.Mask) (roundrect_rratio 0.25) ${p.P3})
  )`
}
