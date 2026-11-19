// Two SMD solder pads for a flat LiPo pouch cell's leads (no connector, keeps height down).
module.exports = {
  params: { designator: 'BT', side: 'F', pos: undefined, neg: undefined },
  body: p => `
  (module Battery_Pads (layer ${p.side}.Cu) (tedit 6500000)
    ${p.at}
    (attr smd)
    (fp_text reference "${p.ref}" (at 0 -2.6 ${p.r}) (layer ${p.side}.SilkS) ${p.ref_hide} (effects (font (size 0.8 0.8) (thickness 0.12))))
    (fp_text value LiPo (at 0 2.6 ${p.r}) (layer ${p.side}.Fab) (effects (font (size 0.8 0.8) (thickness 0.12))))
    (fp_text user + (at -2 -2.6 ${p.r}) (layer ${p.side}.SilkS) (effects (font (size 1 1) (thickness 0.15))))
    (fp_text user - (at 2 -2.6 ${p.r}) (layer ${p.side}.SilkS) (effects (font (size 1 1) (thickness 0.15))))
    (pad 1 smd rect (at -2 0 ${p.r}) (size 2.5 3) (layers ${p.side}.Cu ${p.side}.Mask) ${p.pos})
    (pad 2 smd rect (at 2 0 ${p.r}) (size 2.5 3) (layers ${p.side}.Cu ${p.side}.Mask) ${p.neg})
  )`
}
