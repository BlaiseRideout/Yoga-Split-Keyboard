# Outsourcing the case: 3D printing, CNC and laser-cut options

This compares having the case made by a service instead of printing it at home, for both the split and
the monolithic version, delivered to Kirkland, WA. It covers Chinese services (JLC3DP, JLCPCB, JLCCNC),
which ship with US import duty prepaid, and US services (Craftcloud's US vendors, Xometry, Protolabs and
SendCutSend), which have no duty.

**About the prices:** these are rough estimates from typical hobby-order pricing in late 2026. They are
**not instant quotes.** Upload the files listed under [Getting real quotes](#getting-real-quotes) before
ordering. JLC needs you signed in to see a price. Craftcloud, Xometry, Protolabs and SendCutSend quote
without an account. Prices are in USD. The "delivered" columns include shipping and, for the Chinese
services, US import duty. They don't include WA sales tax, which is about 10% in Kirkland.

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

The 295 mm mono tray fits JLC3DP's MJF bed (370 × 276 mm) and typical MJF and SLS machines at US shops,
so it can be made in one piece. It does not fit most hobby printers.

## US import duty on Chinese-made parts (November 2026)

- **There is no de minimis exemption for China.** The $800 duty-free threshold ended for Chinese goods in
  May 2025 and for all countries in August 2025, so even a $20 order pays duty.
- **Plastic and FR4 parts** pay roughly 37.5–45%: the 25% Section 301 tariff, the 12.5% Section 301 tariff
  that took effect on 24 July 2026, and the normal MFN rate. The IEEPA tariffs ended on 24 February 2026
  after the Supreme Court ruling.
- **Aluminum parts** pay roughly 75–90%, because the 50% Section 232 metals tariff stacks with Section 301.
- **JLC collects the duty at checkout** (DDP) for individual US buyers, so no bill arrives at the door. JLC
  usually settles any difference later, except for orders it charged at between 35% and 90%. JLC's
  published rates were 35% for PCBs, about 40% for plastic and FR4 parts, and 90% for CNC and sheet-metal
  aluminum.
- These rates have changed several times in 2026. Check the duty line at checkout before you rely on the
  totals below.

## Summary

Cost is the case alone, delivered. "Build total" swaps it into the BOM in
[cost-comparison.md](cost-comparison.md) in place of the $5 home print. The rest of that BOM comes to
$284 for the split version and $211 for the mono version.

### Split version

| Option | Case, delivered | Build total | Lead time to Kirkland | Design changes |
|---|---|---|---|---|
| Home print (current BOM) | ~$5 | ≈ $289 | your printer time | none |
| **A. Resin**, JLC3DP | $55–95 | $340–380 | 1–1.5 weeks | small |
| **B1. MJF PA12 nylon**, JLC3DP | $85–140 | $370–425 | 1–1.5 weeks | moderate |
| **B2. MJF or SLS nylon**, Craftcloud US vendor ★ | $80–150 | $365–435 | 1–2 weeks | moderate |
| **B3. MJF nylon**, Xometry or Protolabs | $150–300 | $435–585 | 3 days–1.5 weeks | moderate |
| **C. MJF trays + FR4 frames**, JLC3DP + JLCPCB | $85–140 | $370–425 | 1–1.5 weeks | moderate |
| **D1. CNC aluminum**, JLCCNC (≈ 90% duty) | $290–590 | $575–875 | 2–3 weeks | significant |
| **D2. CNC aluminum**, Xometry or Protolabs | $500–1,000 | $785–1,285 | 1–2 weeks | significant |
| **E. Laser-cut stack**, SendCutSend | $60–110 | $345–395 | about 1 week | redesign |

### Monolithic version

| Option | Case, delivered | Build total | Lead time to Kirkland | Design changes |
|---|---|---|---|---|
| Home print (current BOM, ≥300 mm bed) | ~$5 | ≈ $216 | your printer time | none |
| **A. Resin**, JLC3DP | $60–100 | $270–310 | 1–1.5 weeks | small, but the 295 mm frame will likely warp |
| **B1. MJF PA12 nylon**, JLC3DP | $100–155 | $310–365 | 1–1.5 weeks | moderate |
| **B2. MJF or SLS nylon**, Craftcloud US vendor ★ | $70–140 | $280–350 | 1–2 weeks | moderate |
| **B3. MJF nylon**, Xometry or Protolabs | $130–260 | $340–470 | 3 days–1.5 weeks | moderate |
| **C. MJF tray + FR4 frame**, JLC3DP + JLCPCB | $105–175 | $315–385 | 1–1.5 weeks | moderate |
| **D1. CNC aluminum**, JLCCNC (≈ 90% duty) | $250–520 | $460–730 | 2–3 weeks | significant (fewer setups than split) |
| **D2. CNC aluminum**, Xometry or Protolabs | $300–600 | $510–810 | 1–2 weeks | significant |
| **E. Laser-cut stack**, SendCutSend | $50–100 | $260–310 | about 1 week | redesign |

★ The recommended option. The reasons are below.

Lead times are production plus shipping. JLC orders go by DHL, UPS or FedEx Express, about $20–30 and
3–5 days to the Seattle area, after 2–5 days of production. US vendors ship by ground in 2–4 days.
SendCutSend's nearest plant is in Reno, NV. Protolabs and Xometry can expedite MJF to a few days for a
large surcharge.

## Recommendation

**Option B2: MJF or SLS nylon from a US vendor through Craftcloud, with the floor and frame thickened
to 1.5 mm.**

- Once duty is added, the JLC options cost about the same as US MJF. A US vendor avoids the duty, which
  changed four times in 2026, and arrives just as fast.
- The trays need nylon's toughness. Their 2 mm walls and the dowel and magnet holes in the split face
  would chip in resin. Nylon also takes heat-set inserts well.
- Craftcloud compares many shops in one quote. Pick a US shop, which it shows by location, and black dyed
  PA12.

**If you want the flattest frame,** option C from JLC is a close second. The frame is the part most
likely to warp, and a 1.2 mm black FR4 frame from JLCPCB stays perfectly flat. It's also transparent to
the Bluetooth radio. With duty, it costs about the same as B2.

**If you want it cheapest and fastest,** **option E (SendCutSend)** is about a week door to door with no
duty, but it means redesigning the case as a stack of flat layers.

**CNC aluminum (D)** is now much more expensive than before. From China it pays about 90% duty, and US
machine shops charge $250–500 per one-off tray. It also needs the most design work. Its radio problem
still applies: an aluminum tray with an aluminum frame on top would shield the nice!nano's antenna.
Pair a CNC tray with an FR4 or acrylic frame, or leave a window over the controller.

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

### E. Laser-cut stack (SendCutSend)

This is a different case, not a re-skin of the printed one. It's built from stock SendCutSend materials:

- Layers, bottom to top: 5052 aluminum floor, 0.040″ (1.0 mm), anodized black, with magnet through-holes
  → two black acrylic wall rings, 0.118″ (3.0 mm) each, plus one clear 0.063″ (1.6 mm) ring → top frame.
  M2 screws run through every layer into nuts or standoffs. That adds up to about the same 10 mm height.
- An aluminum floor doesn't affect the docking magnets or the hall sensors.
- Make the top frame from acrylic, or order it in 1.2 mm FR4 from JLCPCB. An aluminum frame over the
  controller would block the radio. SendCutSend's G10/FR4 starts at 3.2 mm, which is too thick for the
  frame.
- The rings are only 2 mm wide, which is fragile in acrylic. Trim the PCB outline by 1 mm so the rings
  can be 3 mm wide.
- The USB-C and switch openings become notches cut into the top ring.

### Optional switch plate

The current design has no switch plate: the Choc switches sit in hotswap sockets on the PCB, and the frame
covers only the border. A plate stiffens the board and reduces the risk of switches pulling out of the
sockets with the keycaps.

- Choc switches need a **1.2 mm** plate. It sits in the existing 5.6 mm gap above the PCB, so the case
  doesn't get any taller. Cut it back around the controller and battery.
- Use **FR4 from JLCPCB** (about $15–30 per split design or $35–60 mono, with duty) or **1.2 mm 5052
  aluminum from JLCCNC** (about $30–55 per part, with duty). SendCutSend doesn't stock aluminum at
  1.2 mm: its 0.040″ (1.0 mm) is too loose for the Choc clips, and its 0.063″ (1.6 mm) is too thick. Don't use steel. A steel plate a few millimetres above the docking magnets
  would pull them in, weakening the dock and distorting the field the laptop's hall sensors read.

## Getting real quotes

| Service | Upload | Settings to choose |
|---|---|---|
| Craftcloud | `case/stl/tray_*.stl`, `frame_*.stl` (after the thickening above) | MJF or SLS PA12, dyed black, filtered to US vendors |
| Xometry / Protolabs | Same STLs, or STEP | MJF PA12 black; for CNC, 6061-T6, black anodize |
| SendCutSend | DXF of each layer (see option E) | 5052 0.040″ or 0.063″ anodized black; acrylic 0.118″ |
| JLC3DP | Same STLs | MJF PA12 dyed black, or JLC Black resin |
| JLCPCB | KiCad board with the frame outline, no copper | 1.2 mm FR4, black mask, 5 pcs |
| JLCCNC | STEP of the tray | 6061-T6, black anodize, ISO 2768-m |

## The 4-row MX-spaced variant

That variant is being designed in a separate thread. The same comparison applies, with two differences.
MX switches are taller, so the tray walls are taller and hold more material: expect print prices about
20–40% higher and deeper CNC pockets. An MX plate is 1.5 mm instead of 1.2 mm, so SendCutSend's 0.063″
(1.6 mm) aluminum would work for it. The outer size stays at 295 × 113 mm, so the bed-size notes above
don't change.
