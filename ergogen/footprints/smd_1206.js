// Generic 1206 two-terminal SMD part (resistor, PTC fuse). value is printed on Fab and used for the BOM.
module.exports = {
  params: { designator: 'R', side: 'B', from: undefined, to: undefined, value: '' },
  body: p => `
  (module SMD_1206 (layer ${p.side}.Cu) (tedit 6500000)
    ${p.at}
    (attr smd)
    (fp_text reference "${p.ref}" (at 0 -1.8 ${p.r}) (layer ${p.side}.SilkS) ${p.ref_hide} (effects (font (size 0.8 0.8) (thickness 0.12)) ${p.side === 'B' ? '(justify mirror)' : ''}))
    (fp_text value "${p.value}" (at 0 1.8 ${p.r}) (layer ${p.side}.Fab) (effects (font (size 0.8 0.8) (thickness 0.12)) ${p.side === 'B' ? '(justify mirror)' : ''}))
    (fp_line (start -0.6 -1) (end 0.6 -1) (layer ${p.side}.SilkS) (width 0.12))
    (fp_line (start -0.6 1) (end 0.6 1) (layer ${p.side}.SilkS) (width 0.12))
    (pad 1 smd rect (at -1.475 0 ${p.r}) (size 1.15 1.8) (layers ${p.side}.Cu ${p.side}.Paste ${p.side}.Mask) ${p.from})
    (pad 2 smd rect (at 1.475 0 ${p.r}) (size 1.15 1.8) (layers ${p.side}.Cu ${p.side}.Paste ${p.side}.Mask) ${p.to})
  )`
}
