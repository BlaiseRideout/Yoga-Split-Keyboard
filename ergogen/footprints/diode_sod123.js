// 1N4148W SOD-123 SMD diode, bottom side by default (JLCPCB-assemblable, LCSC C81598).
// from = switch side (anode), to = row net (cathode, pad 1)
module.exports = {
  params: { designator: 'D', side: 'B', from: undefined, to: undefined, value: '1N4148W' },
  body: p => {
    const s = p.side
    const mir = s === 'B' ? ' (justify mirror)' : ''
    return `
  (module D_SOD-123 (layer ${s}.Cu) (tedit 6500000)
    ${p.at}
    (attr smd)
    (fp_text reference "${p.ref}" (at 0 -1.8 ${p.r}) (layer ${s}.SilkS) ${p.ref_hide} (effects (font (size 0.8 0.8) (thickness 0.12))${mir}))
    (fp_text value "${p.value}" (at 0 1.8 ${p.r}) (layer ${s}.Fab) (effects (font (size 0.8 0.8) (thickness 0.12))${mir}))
    (fp_line (start -2.35 -1) (end -2.35 1) (layer ${s}.SilkS) (width 0.12))
    (fp_line (start -2.35 -1) (end 1.65 -1) (layer ${s}.SilkS) (width 0.12))
    (fp_line (start -2.35 1) (end 1.65 1) (layer ${s}.SilkS) (width 0.12))
    (fp_line (start -2.6 -1.2) (end 2.6 -1.2) (layer ${s}.CrtYd) (width 0.05))
    (fp_line (start 2.6 -1.2) (end 2.6 1.2) (layer ${s}.CrtYd) (width 0.05))
    (fp_line (start 2.6 1.2) (end -2.6 1.2) (layer ${s}.CrtYd) (width 0.05))
    (fp_line (start -2.6 1.2) (end -2.6 -1.2) (layer ${s}.CrtYd) (width 0.05))
    (pad 1 smd roundrect (at -1.65 0 ${p.r}) (size 0.9 1.2) (layers ${s}.Cu ${s}.Paste ${s}.Mask) (roundrect_rratio 0.25) ${p.to})
    (pad 2 smd roundrect (at 1.65 0 ${p.r}) (size 0.9 1.2) (layers ${s}.Cu ${s}.Paste ${s}.Mask) (roundrect_rratio 0.25) ${p.from})
  )`
  }
}
