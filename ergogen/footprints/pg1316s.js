// Kailh PG1316S ultra-low-profile (laptop-style) switch, SMD, reflowed by the PCB assembler.
// Land pattern from two independent open-source footprints (marbastlib SW_PG1316S and
// palette-system azfootprints Kailh_socket_PG1316S), which agree: contacts at (+/-2.5, 2.65)
// 1.55 x 2 mm, four 2 x 2 mm mechanical pads at (+/-6.35, +/-6), locating holes 1.05 and 1.25 mm.
// Courtyard 13.6 mm square. Caps are about 16.05 x 16.25 mm. from / to = the two contacts.
module.exports = {
  params: { designator: 'S', from: undefined, to: undefined, keycaps: false },
  body: p => `
  (module PG1316S (layer F.Cu) (tedit 6500000)
    ${p.at}
    (attr smd)
    (fp_text reference "${p.ref}" (at 0 -4.6 ${p.r}) (layer F.SilkS) ${p.ref_hide} (effects (font (size 0.8 0.8) (thickness 0.12))))
    (fp_text value PG1316S (at 0 4.6 ${p.r}) (layer F.Fab) (effects (font (size 0.8 0.8) (thickness 0.12))))
    (fp_line (start -6.8 -6.8) (end 6.8 -6.8) (layer F.CrtYd) (width 0.05))
    (fp_line (start 6.8 -6.8) (end 6.8 6.8) (layer F.CrtYd) (width 0.05))
    (fp_line (start 6.8 6.8) (end -6.8 6.8) (layer F.CrtYd) (width 0.05))
    (fp_line (start -6.8 6.8) (end -6.8 -6.8) (layer F.CrtYd) (width 0.05))
    (fp_line (start -6.5 -6.5) (end -4.5 -6.5) (layer F.SilkS) (width 0.12))
    (fp_line (start 4.5 -6.5) (end 6.5 -6.5) (layer F.SilkS) (width 0.12))
    ${p.keycaps ? `(fp_line (start -8.1 -8.1) (end 8.1 -8.1) (layer Dwgs.User) (width 0.1))
    (fp_line (start 8.1 -8.1) (end 8.1 8.1) (layer Dwgs.User) (width 0.1))
    (fp_line (start 8.1 8.1) (end -8.1 8.1) (layer Dwgs.User) (width 0.1))
    (fp_line (start -8.1 8.1) (end -8.1 -8.1) (layer Dwgs.User) (width 0.1))` : ''}
    (pad "" np_thru_hole circle (at -5.8 2.75 ${p.r}) (size 1.05 1.05) (drill 1.05) (layers *.Cu *.Mask))
    (pad "" np_thru_hole circle (at 5.8 -2.75 ${p.r}) (size 1.25 1.25) (drill 1.25) (layers *.Cu *.Mask))
    (pad 1 smd rect (at -2.5 2.65 ${p.r}) (size 1.55 2) (layers F.Cu F.Paste F.Mask) ${p.from})
    (pad 2 smd rect (at 2.5 2.65 ${p.r}) (size 1.55 2) (layers F.Cu F.Paste F.Mask) ${p.to})
    (pad "" smd rect (at -6.35 -6 ${p.r}) (size 2 2) (layers F.Cu F.Paste F.Mask))
    (pad "" smd rect (at -6.35 6 ${p.r}) (size 2 2) (layers F.Cu F.Paste F.Mask))
    (pad "" smd rect (at 6.35 -6 ${p.r}) (size 2 2) (layers F.Cu F.Paste F.Mask))
    (pad "" smd rect (at 6.35 6 ${p.r}) (size 2 2) (layers F.Cu F.Paste F.Mask))
  )`
}
