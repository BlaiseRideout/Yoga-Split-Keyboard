// 2-pin right-angle magnetic pogo connector (2.54 mm pitch) on the split edge of each half.
// Origin = board edge; the connector body overhangs +x through a slot in the case's join wall so its
// contact face sits flush with the split face. Spring pins on the left half, flat targets on the right
// (generic "2P magnetic pogo connector, right angle, SMD" pair). Check the land pattern against the
// part you buy: these modules vary by vendor.
// a / b: nets of the pin at local y = -1.27 / +1.27.
module.exports = {
  params: { designator: 'J', side: 'F', a: undefined, b: undefined, kind: 'male' },
  body: p => `
  (module Pogo_2P_RA_${p.kind} (layer ${p.side}.Cu) (tedit 6500000)
    ${p.at}
    (attr smd)
    (fp_text reference "${p.ref}" (at -5 -3.5 ${p.r}) (layer ${p.side}.SilkS) ${p.ref_hide} (effects (font (size 0.8 0.8) (thickness 0.12))))
    (fp_text value "Pogo 2P ${p.kind}" (at -3 4 ${p.r}) (layer ${p.side}.Fab) (effects (font (size 0.8 0.8) (thickness 0.12))))
    (fp_text user CHG (at -5 3.5 ${p.r}) (layer ${p.side}.SilkS) (effects (font (size 0.8 0.8) (thickness 0.12))))
    (fp_line (start -6 -3) (end 5.5 -3) (layer Dwgs.User) (width 0.12))
    (fp_line (start 5.5 -3) (end 5.5 3) (layer Dwgs.User) (width 0.12))
    (fp_line (start 5.5 3) (end -6 3) (layer Dwgs.User) (width 0.12))
    (fp_line (start -6 3) (end -6 -3) (layer Dwgs.User) (width 0.12))
    (pad 1 smd rect (at -4.2 -1.27 ${p.r}) (size 2.4 1.2) (layers ${p.side}.Cu ${p.side}.Paste ${p.side}.Mask) ${p.a})
    (pad 2 smd rect (at -4.2 1.27 ${p.r}) (size 2.4 1.2) (layers ${p.side}.Cu ${p.side}.Paste ${p.side}.Mask) ${p.b})
    (pad "" smd rect (at -1.9 -3.4 ${p.r}) (size 1.8 1.4) (layers ${p.side}.Cu ${p.side}.Paste ${p.side}.Mask))
    (pad "" smd rect (at -1.9 3.4 ${p.r}) (size 1.8 1.4) (layers ${p.side}.Cu ${p.side}.Paste ${p.side}.Mask))
  )`
}
