// Two through-holes for a flat LiPo pouch cell's leads: push the wires through and solder (no connector, keeps height down).
module.exports = {
  params: { designator: 'BT', side: 'F', pos: undefined, neg: undefined },
  body: p => `
  (module Battery_Pads (layer ${p.side}.Cu) (tedit 6500000)
    ${p.at}
        (fp_text reference "${p.ref}" (at 0 -2.6 ${p.r}) (layer ${p.side}.SilkS) ${p.ref_hide} (effects (font (size 0.8 0.8) (thickness 0.12))))
    (fp_text value LiPo (at 0 2.6 ${p.r}) (layer ${p.side}.Fab) (effects (font (size 0.8 0.8) (thickness 0.12))))
    (fp_text user + (at -2 -2.6 ${p.r}) (layer ${p.side}.SilkS) (effects (font (size 1 1) (thickness 0.15))))
    (fp_text user - (at 2 -2.6 ${p.r}) (layer ${p.side}.SilkS) (effects (font (size 1 1) (thickness 0.15))))
    (pad 1 thru_hole rect (at -2 0 ${p.r}) (size 2.2 2.2) (drill 1.1) (layers *.Cu *.Mask) ${p.pos})
    (pad 2 thru_hole circle (at 2 0 ${p.r}) (size 2.2 2.2) (drill 1.1) (layers *.Cu *.Mask) ${p.neg})
  )`
}
