// M2 mounting hole (non-plated 2.2 mm) with 4.4 mm keepout ring on silk.
module.exports = {
  params: { designator: 'H' },
  body: p => `
  (module MountingHole_M2 (layer F.Cu) (tedit 6500000)
    ${p.at}
    (fp_text reference "${p.ref}" (at 0 -3 ${p.r}) (layer F.SilkS) hide (effects (font (size 0.8 0.8) (thickness 0.12))))
    (fp_text value M2 (at 0 3 ${p.r}) (layer F.Fab) hide (effects (font (size 0.8 0.8) (thickness 0.12))))
    (fp_circle (center 0 0) (end 2.2 0) (layer F.SilkS) (width 0.12))
    (fp_circle (center 0 0) (end 2.5 0) (layer F.CrtYd) (width 0.05))
    (pad "" np_thru_hole circle (at 0 0) (size 2.2 2.2) (drill 2.2) (layers *.Cu *.Mask))
  )`
}
