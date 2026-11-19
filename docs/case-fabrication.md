# Outsourcing the case: 3D printing, CNC and laser-cut options

This compares having the case made by a service instead of printing it at home, for both the split and
the monolithic version, with delivery to Tokyo.

**About the prices:** these are rough estimates from typical hobby-order pricing in late 2026. They are
**not instant quotes.** JLC3DP and JLCCNC only show prices after you upload a model while signed in.
Before ordering, upload the files listed under [Getting real quotes](#getting-real-quotes). Prices are in
USD, before Japanese import tax. Shipping is included in the "delivered" columns.

## What gets made

Measured from the STLs in `case/stl/` (rendered from `case/case.scad`):

| Part | Bounding box (mm) | Volume | Notes |
|---|---|---|---|
| Tray, left or right | 147.7 × 113.2 × 8.8 | 26.9 cm³ | 1.0 mm floor, 2.0 mm walls, 0.4 mm skin under the docking magnets, side holes for joining magnets and dowels |
| Frame, left or right | 147.7 × 113.0 × 2.2 | 9.4 cm³ | 1.2 mm top plate plus a 1 mm locating rim |
| Tray, mono | 295.3 × 113.2 × 8.8 | 46.1 cm³ | Same features, without the split face |
| Frame, mono | 295.3 × 113.0 × 2.2 | 19.3 cm³ | |
| **Split set** (2 trays + 2 frames) | | **72.6 cm³** | about 80 g in nylon or resin |
| **Mono set** (1 tray + 1 frame) | | **65.4 cm³** | about 72 g |

Two size limits matter. The 295 mm mono tray fits JLC3DP's MJF bed (370 × 276 mm) and its SLS and resin
machines, so it can be made in one piece. It does not fit most hobby printers.

## Summary

Cost is the case alone, delivered to Tokyo. "Build total" swaps it into the BOM in
[bom-comparison.md](bom-comparison.md) in place of the $5 home print. The rest of that BOM comes to
$284 for the split version and $211 for the mono version.

### Split version

| Option | Case, delivered | Build total | Lead time to Tokyo | Design changes |
|---|---|---|---|---|
| Home print (current BOM) | ~$5 | ≈ $289 | your printer time | none |
| **A. Resin, all 4 parts** (JLC3DP 9600 / Black Resin) | $40–70 | $325–355 | 1–1.5 weeks | small |
| **B. MJF PA12 nylon, all 4 parts** (JLC3DP, dyed black) | $60–105 | $345–390 | 1.5–2 weeks | moderate |
| **C. MJF trays + FR4 frames** (JLC3DP + JLCPCB) ★ | $60–95 | $345–380 | 1.5–2 weeks | moderate |
| **D. CNC aluminum trays + laser-cut aluminum frames** (JLCCNC) | $175–340 | $460–625 | 2–3 weeks | significant |
| **E. Laser-cut stack: FR4 floor and frame, acrylic wall rings** | $95–155 | $380–440 | 1.5–3 weeks | redesign |

### Monolithic version

| Option | Case, delivered | Build total | Lead time to Tokyo | Design changes |
|---|---|---|---|---|
| Home print (current BOM, ≥300 mm bed) | ~$5 | ≈ $216 | your printer time | none |
| **A. Resin** | $45–75 | $255–285 | 1–1.5 weeks | small, but the 295 mm frame will likely warp |
| **B. MJF PA12 nylon** | $70–115 | $280–325 | 1.5–2 weeks | moderate |
| **C. MJF tray + FR4 frame** ★ | $75–125 | $285–335 | 1.5–2 weeks | moderate |
| **D. CNC aluminum tray + laser-cut aluminum frame** | $160–300 | $370–510 | 2–3 weeks | significant (fewer setups than split) |
| **E. Laser-cut stack** | $110–180 | $320–390 | 1.5–3 weeks | redesign |

★ The recommended option. The reasons are below.

PCBWay is usually 10–30% above JLC for the same 3D print or CNC part, and takes about the same time.
Craftcloud, an aggregator of EU and US print shops, tends to cost $80–150 for the MJF set, and often
takes 2–4 weeks to reach Japan. Both are worth a quote if JLC rejects a file.

## Recommendation

**Option C: MJF nylon trays from JLC3DP, plus 1.2 mm black FR4 frames ordered from JLCPCB as bare PCBs.**

- The trays need nylon's toughness. Their 2 mm walls and the dowel and magnet holes in the split face
  would chip in resin. Nylon also takes heat-set inserts well.
- The frame is the part most likely to warp. It's a 1.2 mm sheet the full width of the board, below both
  JLC's 2.0 mm guideline for large printed parts. FR4 stays flat at that thickness and costs about the
  same. Black solder mask also looks good, and it's transparent to the Bluetooth radio.
- Both come from the JLC group, and JLC usually lets you ship the two orders together.
- For the split version, the left and right frames are mirror images, so one FR4 design flipped over
  serves both halves. The 5-piece minimum gives you spares.

If you mainly want it cheap and fast, **option A (resin)** works for the split version, provided you
thicken the floor and frame as described below. For the mono version, resin is risky because of the
295 mm frame.

**CNC aluminum (D)** is the premium option. It costs $100–250 more and needs the most design work. The
main catch is radio: an aluminum tray with an aluminum frame on top would shield the nice!nano's antenna.
Pair a CNC tray with an FR4 frame, or leave a window over the controller.

## Design changes per option

### Changes that apply to every outsourced option

1. **Make the docking-magnet pockets through-holes, not blind pockets.** The 0.4 mm skin under each
   magnet is too thin for MJF and SLS (1.0 mm minimum), is fragile in resin, and can't be made at all with
   a laser-cut stack. Instead, cut 6.2 mm holes right through the floor, glue the magnets flush with the
   bottom face, and cover the whole bottom with a 0.2–0.3 mm adhesive film (PET or microfiber). The film
   also protects the lower screen. The magnets end up as close to the laptop as they are now.
2. **Add a protective bottom film or feet anyway.** MJF nylon is slightly grainy, and aluminum and FR4 are
   hard. All of them can scuff the glass of the lower screen.
3. **Send STEP files as well as STL.** JLCCNC requires STEP for CNC. OpenSCAD can't export STEP, so
   convert the STL with FreeCAD, or re-model the tray there, for option D.

### A. Resin (SLA)

- Raise the floor from 1.0 to 1.5 mm, and the frame from 1.2 to 1.5 mm. JLC's guideline asks for
  1.5–2.0 mm on parts this size. That adds about 0.8 mm to the case height, from 10.0 to about 10.8 mm.
- Resin cracks around heat-set inserts. Use M2 self-tapping screws into 1.6 mm pilot holes, or JLC's
  insert option, which starts at M3 and so needs bigger bosses.
- Choose JLC Black or Imagine Black over the white 9600 resin, which yellows in sunlight.

### B and C. MJF or SLS nylon

- The floor and frame need the same thickening to 1.5 mm. MJF and SLS walls are more forgiving than resin
  at 2.0 mm, so the side walls can stay as they are.
- Heat-set M2 inserts work as designed.
- The mono tray fits the MJF bed (370 × 276 mm).
- For **C**, export the frame outline (`envelope*.dxf` minus the keycap and nice!view openings) as a
  board outline in KiCad and order it with no copper. The flat FR4 can't have the 1 mm locating rim, so
  the frame needs 4–6 M2 screw holes into new bosses in the tray. The walls are only 2 mm thick, so the
  bosses have to grow inward at the corners, clear of the PCB outline.

### D. CNC aluminum

- Every inside corner of the cavity needs a radius of at least 1.5 mm, which is what a 3 mm end mill
  leaves. Round the PCB outline's corners to match.
- Raise the magnet skin to at least 0.8 mm, JLCCNC's metal minimum, or use the through-hole approach
  above.
- Replace heat-set inserts with tapped M2 holes in the bosses.
- The USB-C opening, the switch slot and, for the split version, the joining-magnet and dowel holes are
  all on the sides. Each face adds a machining setup, and that's most of the extra cost of the split
  version here. Moving the joining hardware to vertical pockets from above, with the magnets glued into
  a short slot, would save two setups.
- Radio: see the recommendation above. Use an FR4 frame, or cut the aluminum frame open over the
  nice!nano and nice!view, and cover that window with acrylic.
- Aluminum doesn't affect the docking magnets or the laptop's hall sensors.

### E. Laser-cut stack

This is a different case, not a re-skin of the printed one:

- Layers, bottom to top: FR4 floor 0.8 mm (with magnet through-holes) → acrylic wall rings 3 + 3 + 2 mm
  → FR4 frame 1.2 mm. M2 screws run through every layer into nuts or standoffs.
- The rings are only 2 mm wide, which is fragile in acrylic. Trim the PCB outline by 1 mm so the rings
  can be 3 mm wide.
- The USB-C and switch openings become notches cut into the top ring.
- The FR4 layers come from JLCPCB as bare boards. The acrylic can come from Ponoko, or you can cut it
  yourself at a Tokyo makerspace with a laser cutter (FabCafe Tokyo in Shibuya has one), which makes it
  the cheapest and fastest route if you're willing to do the cutting.

### Optional switch plate

The current design has no switch plate: the Choc switches sit in hotswap sockets on the PCB, and the frame
covers only the border. A plate stiffens the board and reduces the risk of switches pulling out of the
sockets with the keycaps.

- Choc switches need a **1.2 mm** plate. It sits in the existing 5.6 mm gap above the PCB, so the case
  doesn't get any taller. Cut it back around the controller and battery.
- Use **FR4 (JLCPCB, about $10–20 per split design or $25–45 mono) or 5052 aluminum (JLCCNC sheet metal,
  about $15–30 per part)**. Don't use steel. A steel plate a few millimetres above the docking magnets
  would pull them in, weakening the dock and distorting the field the laptop's hall sensors read.

## Shipping and import tax in Japan

- JLC orders usually ship by DHL, FedEx or JLC's own express lines in 3–6 days to Tokyo, costing about
  $15–40 depending on weight. Combine the JLC3DP and JLCPCB orders when you can.
- Personal imports are free of duty and consumption tax when the taxable value is ¥10,000 or less. For
  personal-use goods the taxable value is 60% of the price, so orders under about ¥16,600 qualify. Above
  that, expect 10% consumption tax plus a courier handling fee. Japan plans to remove this exemption in
  April 2028.

## Getting real quotes

| Service | Upload | Settings to choose |
|---|---|---|
| JLC3DP | `case/stl/tray_*.stl`, `frame_*.stl` (after the thickening above) | MJF PA12, dyed black; or JLC Black resin |
| JLCPCB | KiCad board with the frame outline, no copper | 1.2 mm FR4, black mask, 5 pcs |
| JLCCNC | STEP of the tray | 6061-T6, black anodize, ISO 2768-m |
| JLCCNC sheet metal | DXF of the frame or plate | 5052, 1.2 mm, black anodize |

## The 4-row MX-spaced variant

That variant is being designed in a separate thread. The same comparison applies, with two differences.
MX switches are taller, so the tray walls are taller and hold more material: expect print prices about
20–40% higher and deeper CNC pockets. An MX plate is 1.5 mm instead of 1.2 mm. The outer size stays at
295 × 113 mm, so the bed-size and shipping notes above don't change.
