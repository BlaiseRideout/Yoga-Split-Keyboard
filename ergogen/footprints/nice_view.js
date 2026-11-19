// nice!view display header (single-sided, KiCad 5 syntax for ergogen 4 kicad5 template).
// Pin order (front, left->right, header at bottom when display points up):
//   MOSI, SCK, VCC, GND, CS   (per nicekeyboards.com/docs/nice-view/pinout-schematic)
// Footprint origin = center of the 14 x 36 mm nice!view board. Header row 16.7 mm below center.
module.exports = {
  params: {
    designator: 'DISP',
    MOSI: {type: 'net', value: 'MOSI'},
    SCK: {type: 'net', value: 'SCK'},
    VCC: {type: 'net', value: 'VCC'},
    GND: {type: 'net', value: 'GND'},
    CS: {type: 'net', value: 'CS'},
  },
  body: p => `
  (module nice_view (layer F.Cu) (tedit 6500000)
    ${p.at}
    (fp_text reference "${p.ref}" (at 0 12 ${p.r}) (layer F.SilkS) ${p.ref_hide} (effects (font (size 1 1) (thickness 0.15))))
    (fp_text value nice!view (at 0 0 ${p.r}) (layer F.Fab) (effects (font (size 1 1) (thickness 0.15))))
    (fp_line (start -7 -18) (end 7 -18) (layer Dwgs.User) (width 0.15))
    (fp_line (start 7 -18) (end 7 18) (layer Dwgs.User) (width 0.15))
    (fp_line (start 7 18) (end -7 18) (layer Dwgs.User) (width 0.15))
    (fp_line (start -7 18) (end -7 -18) (layer Dwgs.User) (width 0.15))
    (fp_line (start -5.4 -11.9) (end 5.4 -11.9) (layer Dwgs.User) (width 0.1))
    (fp_line (start 5.4 -11.9) (end 5.4 13.4) (layer Dwgs.User) (width 0.1))
    (fp_line (start 5.4 13.4) (end -5.4 13.4) (layer Dwgs.User) (width 0.1))
    (fp_line (start -5.4 13.4) (end -5.4 -11.9) (layer Dwgs.User) (width 0.1))
    (fp_line (start -6.41 15.37) (end 6.41 15.37) (layer F.SilkS) (width 0.12))
    (fp_line (start 6.41 15.37) (end 6.41 18.03) (layer F.SilkS) (width 0.12))
    (fp_line (start 6.41 18.03) (end -6.41 18.03) (layer F.SilkS) (width 0.12))
    (fp_line (start -6.41 18.03) (end -6.41 15.37) (layer F.SilkS) (width 0.12))
    (fp_text user MOSI (at -5.08 19.5 ${p.r + 90}) (layer F.SilkS) (effects (font (size 0.6 0.6) (thickness 0.1)) (justify right)))
    (fp_text user SCK (at -2.54 19.5 ${p.r + 90}) (layer F.SilkS) (effects (font (size 0.6 0.6) (thickness 0.1)) (justify right)))
    (fp_text user VCC (at 0 19.5 ${p.r + 90}) (layer F.SilkS) (effects (font (size 0.6 0.6) (thickness 0.1)) (justify right)))
    (fp_text user GND (at 2.54 19.5 ${p.r + 90}) (layer F.SilkS) (effects (font (size 0.6 0.6) (thickness 0.1)) (justify right)))
    (fp_text user CS (at 5.08 19.5 ${p.r + 90}) (layer F.SilkS) (effects (font (size 0.6 0.6) (thickness 0.1)) (justify right)))
    (pad 1 thru_hole oval (at -5.08 16.7 ${p.r}) (size 1.7 1.7) (drill 1) (layers *.Cu *.Mask) ${p.MOSI})
    (pad 2 thru_hole oval (at -2.54 16.7 ${p.r}) (size 1.7 1.7) (drill 1) (layers *.Cu *.Mask) ${p.SCK})
    (pad 3 thru_hole oval (at 0 16.7 ${p.r}) (size 1.7 1.7) (drill 1) (layers *.Cu *.Mask) ${p.VCC})
    (pad 4 thru_hole oval (at 2.54 16.7 ${p.r}) (size 1.7 1.7) (drill 1) (layers *.Cu *.Mask) ${p.GND})
    (pad 5 thru_hole rect (at 5.08 16.7 ${p.r}) (size 1.7 1.7) (drill 1) (layers *.Cu *.Mask) ${p.CS})
  )
  `
}
