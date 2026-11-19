// Side-actuated SMD slide switch, MSK-12C02 / Alps SSSS811101 land pattern (LCSC C431540). Lever points toward -y (board edge).
// from = battery +, to = MCU RAW. Third throw is left unconnected.
module.exports = {
  params: { designator: 'SW', side: 'F', from: undefined, to: undefined },
  body: p => `
  (module SW_MSK12C02 (layer ${p.side}.Cu) (tedit 6500000)
    ${p.at}
    (attr smd)
    (fp_text reference "${p.ref}" (at 0 3 ${p.r}) (layer ${p.side}.SilkS) ${p.ref_hide} (effects (font (size 0.8 0.8) (thickness 0.12))))
    (fp_text value MSK-12C02 (at 0 4.2 ${p.r}) (layer ${p.side}.Fab) (effects (font (size 0.8 0.8) (thickness 0.12))))
    (fp_line (start -3.35 -1.6) (end 3.35 -1.6) (layer ${p.side}.SilkS) (width 0.12))
    (fp_line (start -3.35 1.6) (end 3.35 1.6) (layer ${p.side}.SilkS) (width 0.12))
    (fp_line (start -0.4 -1.6) (end -0.4 -3.1) (layer Dwgs.User) (width 0.12))
    (fp_line (start -0.4 -3.1) (end 1.1 -3.1) (layer Dwgs.User) (width 0.12))
    (fp_line (start 1.1 -3.1) (end 1.1 -1.6) (layer Dwgs.User) (width 0.12))
    (pad "" np_thru_hole circle (at -1.5 -0.025) (size 0.9 0.9) (drill 0.9) (layers *.Cu *.Mask))
    (pad "" np_thru_hole circle (at 1.5 -0.025) (size 0.9 0.9) (drill 0.9) (layers *.Cu *.Mask))
    (pad 1 smd rect (at 2.25 1.735 ${p.r}) (size 0.7 1.5) (layers ${p.side}.Cu ${p.side}.Paste ${p.side}.Mask) ${p.from})
    (pad 2 smd rect (at -0.75 1.735 ${p.r}) (size 0.7 1.5) (layers ${p.side}.Cu ${p.side}.Paste ${p.side}.Mask) ${p.to})
    (pad 3 smd rect (at -2.25 1.735 ${p.r}) (size 0.7 1.5) (layers ${p.side}.Cu ${p.side}.Paste ${p.side}.Mask))
    (pad 4 smd rect (at -3.65 -1.125 ${p.r}) (size 1 0.8) (layers ${p.side}.Cu ${p.side}.Paste ${p.side}.Mask))
    (pad 4 smd rect (at 3.65 -1.125 ${p.r}) (size 1 0.8) (layers ${p.side}.Cu ${p.side}.Paste ${p.side}.Mask))
    (pad 4 smd rect (at -3.65 1.085 ${p.r}) (size 1 0.8) (layers ${p.side}.Cu ${p.side}.Paste ${p.side}.Mask))
    (pad 4 smd rect (at 3.65 1.085 ${p.r}) (size 1 0.8) (layers ${p.side}.Cu ${p.side}.Paste ${p.side}.Mask))
  )`
}
