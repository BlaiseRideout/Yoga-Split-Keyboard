// Generic 2-lead through-hole part: axial resistor (pitch 7.62, DIN0204), radial PTC (pitch 5.08),
// or a 2-pin reset button / pads. pitch and drill are parameters; value goes on Fab and in the BOM.
module.exports = {
  params: { designator: 'R', from: undefined, to: undefined, pitch: 7.62, drill: 0.8, value: '', label: '' },
  body: p => `
  (module THT2_P${p.pitch} (layer F.Cu) (tedit 6500000)
    ${p.at}
    (fp_text reference "${p.ref}" (at 0 -1.8 ${p.r}) (layer F.SilkS) ${p.ref_hide} (effects (font (size 0.8 0.8) (thickness 0.12))))
    (fp_text value "${p.value}" (at 0 1.8 ${p.r}) (layer F.Fab) (effects (font (size 0.8 0.8) (thickness 0.12))))
    ${p.label ? `(fp_text user "${p.label}" (at 0 1.8 ${p.r}) (layer F.SilkS) (effects (font (size 0.8 0.8) (thickness 0.12))))` : ''}
    (fp_line (start ${-p.pitch / 2 + 1.1} 0) (end ${p.pitch / 2 - 1.1} 0) (layer F.SilkS) (width 0.12))
    (pad 1 thru_hole rect (at ${-p.pitch / 2} 0 ${p.r}) (size 1.6 1.6) (drill ${p.drill}) (layers *.Cu *.Mask) ${p.from})
    (pad 2 thru_hole circle (at ${p.pitch / 2} 0 ${p.r}) (size 1.6 1.6) (drill ${p.drill}) (layers *.Cu *.Mask) ${p.to})
  )`
}
