// 1N4148 in DO-35, through-hole, 7.62 mm pitch. Lay the body flat on the bottom side (the side the
// switch pins come through), solder from the top, trim the leads. from = anode side, to = cathode (row).
module.exports = {
  params: { designator: 'D', from: undefined, to: undefined },
  body: p => `
  (module D_DO-35_THT (layer F.Cu) (tedit 6500000)
    ${p.at}
    (fp_text reference "${p.ref}" (at 0 -1.6 ${p.r}) (layer B.SilkS) ${p.ref_hide} (effects (font (size 0.8 0.8) (thickness 0.12)) (justify mirror)))
    (fp_text value 1N4148 (at 0 1.6 ${p.r}) (layer B.Fab) (effects (font (size 0.8 0.8) (thickness 0.12)) (justify mirror)))
    (fp_line (start -2 -0.95) (end 2 -0.95) (layer B.SilkS) (width 0.12))
    (fp_line (start -2 0.95) (end 2 0.95) (layer B.SilkS) (width 0.12))
    (fp_line (start -2 -0.95) (end -2 0.95) (layer B.SilkS) (width 0.12))
    (fp_line (start 2 -0.95) (end 2 0.95) (layer B.SilkS) (width 0.12))
    (fp_line (start -1.4 -0.95) (end -1.4 0.95) (layer B.SilkS) (width 0.3))
    (pad 1 thru_hole rect (at -3.81 0 ${p.r}) (size 1.6 1.6) (drill 0.8) (layers *.Cu *.Mask) ${p.to})
    (pad 2 thru_hole circle (at 3.81 0 ${p.r}) (size 1.6 1.6) (drill 0.8) (layers *.Cu *.Mask) ${p.from})
  )`
}
