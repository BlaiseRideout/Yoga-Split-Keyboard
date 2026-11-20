// SWD programming header for the on-board nRF52840: 1 x 4, 2.54 mm pitch, plated through-holes, no part
// fitted. The holes are staggered 0.13 mm either side of the centre line, so a plain pin header (or a
// probe's Dupont leads on one) pressed in from the top holds without solder while the bootloader is flashed.
// Pin 1 (square) is VDD, then SWDIO, SWDCLK, GND, labelled on both sides.
module.exports = {
  params: { designator: 'J', vdd: {type: 'net', value: 'VDD'}, dio: {type: 'net', value: 'SWDIO'},
            clk: {type: 'net', value: 'SWDCLK'}, gnd: {type: 'net', value: 'GND'} },
  body: p => {
    const pads = [['VDD', p.vdd], ['DIO', p.dio], ['CLK', p.clk], ['GND', p.gnd]]
    return `
  (module SWD_Header_1x04_P2.54 (layer F.Cu) (tedit 6500000)
    ${p.at}
    (attr through_hole)
    (fp_text reference "${p.ref}" (at 0 -2.4 ${p.r}) (layer F.SilkS) hide (effects (font (size 0.8 0.8) (thickness 0.12))))
    (fp_text value "SWD header" (at 0 2.4 ${p.r}) (layer F.Fab) (effects (font (size 0.8 0.8) (thickness 0.12))))
    (fp_text user SWD (at ${-3.4 * 2.54 / 2 - 1.4} 0 ${90 + p.r}) (layer F.SilkS) (effects (font (size 0.7 0.7) (thickness 0.12))))
    (fp_line (start -5.08 -1.27) (end 5.08 -1.27) (layer F.CrtYd) (width 0.05))
    (fp_line (start 5.08 -1.27) (end 5.08 1.27) (layer F.CrtYd) (width 0.05))
    (fp_line (start 5.08 1.27) (end -5.08 1.27) (layer F.CrtYd) (width 0.05))
    (fp_line (start -5.08 1.27) (end -5.08 -1.27) (layer F.CrtYd) (width 0.05))
${pads.map(([t, n], i) => `    (fp_text user ${t} (at ${(i - 1.5) * 2.54} 1.9 ${p.r}) (layer F.SilkS) (effects (font (size 0.6 0.6) (thickness 0.1))))
    (fp_text user ${t} (at ${(i - 1.5) * 2.54} 1.9 ${p.r}) (layer B.SilkS) (effects (font (size 0.6 0.6) (thickness 0.1)) (justify mirror)))
    (pad ${i + 1} thru_hole ${i ? 'circle' : 'rect'} (at ${(i - 1.5) * 2.54} ${i % 2 ? 0.127 : -0.127} ${p.r}) (size 1.6 1.6) (drill 1.0) (layers *.Cu *.Mask) ${n})`).join('\n')}
  )`
  }
}
