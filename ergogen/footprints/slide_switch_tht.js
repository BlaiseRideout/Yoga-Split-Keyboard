// C&K OS102011MA1QN1 right-angle SPDT slide switch, through-hole (land pattern from KiCad's
// Button_Switch_THT:SW_Slide_SPDT_Angled_CK_OS102011MA1Q, re-centred on the lever).
// The lever points toward +y in ergogen terms (the board's back edge); origin = lever centre, pin row.
// from = battery +, to = MCU RAW (common pin). Third throw unconnected.
module.exports = {
  params: { designator: 'SW', from: undefined, to: undefined },
  body: p => `
  (module SW_OS102011MA1Q_THT (layer F.Cu) (tedit 6500000)
    ${p.at}
    (fp_text reference "${p.ref}" (at 1 3.2 ${p.r}) (layer F.SilkS) ${p.ref_hide} (effects (font (size 0.8 0.8) (thickness 0.12))))
    (fp_text value OS102011MA1QN1 (at 1 4.4 ${p.r}) (layer F.Fab) (effects (font (size 0.8 0.8) (thickness 0.12))))
    (fp_line (start -3.3 -2.2) (end 5.3 -2.2) (layer F.Fab) (width 0.1))
    (fp_line (start 5.3 -2.2) (end 5.3 2.2) (layer F.Fab) (width 0.1))
    (fp_line (start 5.3 2.2) (end -3.3 2.2) (layer F.Fab) (width 0.1))
    (fp_line (start -3.3 2.2) (end -3.3 -2.2) (layer F.Fab) (width 0.1))
    (fp_line (start -1 -2.2) (end -1 -6.2) (layer Dwgs.User) (width 0.1))
    (fp_line (start 1 -2.2) (end 1 -6.2) (layer Dwgs.User) (width 0.1))
    (fp_line (start -1 -6.2) (end 1 -6.2) (layer Dwgs.User) (width 0.1))
    (fp_line (start -3.4 2.3) (end 5.4 2.3) (layer F.SilkS) (width 0.12))
    (pad "" thru_hole oval (at -3.1 0 ${p.r}) (size 2.2 3.5) (drill 1.5) (layers *.Cu *.Mask))
    (pad "" thru_hole oval (at 5.1 0 ${p.r}) (size 2.2 3.5) (drill 1.5) (layers *.Cu *.Mask))
    (pad 1 thru_hole rect (at -1 0 ${p.r}) (size 1.5 2.5) (drill 0.9) (layers *.Cu *.Mask) ${p.from})
    (pad 2 thru_hole oval (at 1 0 ${p.r}) (size 1.5 2.5) (drill 0.9) (layers *.Cu *.Mask) ${p.to})
    (pad 3 thru_hole oval (at 3 0 ${p.r}) (size 1.5 2.5) (drill 0.9) (layers *.Cu *.Mask))
  )`
}
