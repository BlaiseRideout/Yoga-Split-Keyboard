// 3 mm through-hole LED (T-1), leads at 2.54 mm. Pad 1 (square) = cathode (short lead, flat side).
// Used for the optional status LEDs that replace the nice!view: seat the LED flush on the PCB
// (5.3 mm tall) so its dome sits in the light hole in the top frame / cover.
module.exports = {
  params: { designator: 'LED', K: {type: 'net', value: 'GND'}, A: undefined, color: '' },
  body: p => `
  (module LED_D3.0mm (layer F.Cu) (tedit 6500000)
    ${p.at}
    (fp_text reference "${p.ref}" (at 0 -2.8 ${p.r}) (layer F.SilkS) ${p.ref_hide} (effects (font (size 0.8 0.8) (thickness 0.12))))
    (fp_text value "3mm LED ${p.color}" (at 0 2.6 ${p.r}) (layer F.Fab) (effects (font (size 0.8 0.8) (thickness 0.12))))
    (fp_circle (center 0 0) (end 1.5 0) (layer F.Fab) (width 0.1))
    (fp_arc (start 0 0) (end -1.32 -1.32) (angle 270) (layer F.SilkS) (width 0.12))
    (fp_line (start -1.32 -1.32) (end -1.32 1.32) (layer F.SilkS) (width 0.12))
    (fp_circle (center 0 0) (end 1.9 0) (layer F.CrtYd) (width 0.05))
    (pad 1 thru_hole rect (at -1.27 0 ${p.r}) (size 1.6 1.6) (drill 0.8) (layers *.Cu *.Mask) ${p.K})
    (pad 2 thru_hole circle (at 1.27 0 ${p.r}) (size 1.6 1.6) (drill 0.8) (layers *.Cu *.Mask) ${p.A})
  )`
}
