// Generic 0805 two-terminal SMD part (resistor or LED). For an LED, from = anode, to = cathode
// (pad 2, marked on silkscreen). value is printed on Fab and used for the BOM.
module.exports = {
  params: { designator: 'R', side: 'F', from: undefined, to: undefined, value: '', led: false },
  body: p => `
  (module SMD_0805${p.led ? '_LED' : ''} (layer ${p.side}.Cu) (tedit 6500000)
    ${p.at}
    (attr smd)
    (fp_text reference "${p.ref}" (at 0 -1.5 ${p.r}) (layer ${p.side}.SilkS) ${p.ref_hide} (effects (font (size 0.6 0.6) (thickness 0.1)) ${p.side === 'B' ? '(justify mirror)' : ''}))
    (fp_text value "${p.value}" (at 0 1.5 ${p.r}) (layer ${p.side}.Fab) (effects (font (size 0.6 0.6) (thickness 0.1)) ${p.side === 'B' ? '(justify mirror)' : ''}))
    ${p.led ? `(fp_line (start 1.9 -0.9) (end 1.9 0.9) (layer ${p.side}.SilkS) (width 0.15))` : ''}
    (pad 1 smd rect (at -0.95 0 ${p.r}) (size 1 1.3) (layers ${p.side}.Cu ${p.side}.Paste ${p.side}.Mask) ${p.from})
    (pad 2 smd rect (at 0.95 0 ${p.r}) (size 1 1.3) (layers ${p.side}.Cu ${p.side}.Paste ${p.side}.Mask) ${p.to})
  )`
}
