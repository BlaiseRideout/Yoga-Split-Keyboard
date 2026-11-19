# Split vs monolithic: BOM cost and build complexity

Prices are rough single-build estimates in USD (late 2026 hobby-vendor pricing, before shipping and tax).
They were not checked against live listings, so treat them as a guide for comparing the two
variants, not as quotes.

## Bill of materials

| Item | Split (2 halves) | Monolithic | Unit price | Split $ | Mono $ |
|---|---|---|---|---|---|
| nice!nano v2 (nRF52840 Pro Micro) | 2 | 1 | ~$25 | 50 | 25 |
| nice!view display | 2 | 1 | ~$17 | 34 | 17 |
| Kailh Choc v1 switches (+6 spares) | 60 | 60 | ~$0.55 | 33 | 33 |
| Choc keycaps (MBK / CFX, 1u) | 54 | 54 | ~$0.75 | 40 | 40 |
| Kailh Choc hotswap sockets | 54 | 54 | ~$0.20 | 11 | 11 |
| 1N4148W SOD-123 diodes | 54 | 54 | ~$0.02 | 1 | 1 |
| MSK-12C02 power switch, SKQG reset button | 2 + 2 | 1 + 1 | ~$0.40 | 2 | 1 |
| LiPo pouch cell, 402030 (~200 mAh) per controller | 2 | 1 (or a 403040 for ~500 mAh) | ~$5 | 10 | 5–7 |
| PCB fab, JLCPCB, 5 pcs, 1.2 mm FR4 | 2 designs, ~140 × 108 mm | 1 design, 290 × 108 mm | — | ~30 | ~25 |
| PCB assembly (diodes + sockets, bottom side, 2 boards) | 2 orders | 1 order | — | ~45 | ~30 |
| Case print (PLA/PETG ~120 g, or a service: see [case-fabrication.md](case-fabrication.md)) | 2 trays + 2 frames | 1 tray + 1 frame | — | 5 (self) / 80–150 (service, delivered) | 5 (self, needs ≥300 mm bed) / 70–140 (service, delivered) |
| Docking magnets, 6 × 1.5 mm N52 (pack of 50) | ≤ 26 used | ≤ 26 used | — | 8 | 8 |
| Joining magnets, 6 × 3 mm N52 | 6 | 0 | ~$0.40 | 3 | 0 |
| Alignment dowels, 3 × 6 mm steel | 2 | 0 | — | 3 | 0 |
| M2 heat-set inserts + M2 × 4 screws | 12 | 12 | — | 6 | 6 |
| Magnetic viewing film (one-off, for mapping the stock keyboard) | 1 | 1 | ~$8 | 8 | 8 |
| **Total, self-printed case** | | | | **≈ $289** | **≈ $216** |
| **Total, service-made case** (MJF nylon from a US vendor, delivered to Kirkland, WA) | | | | **≈ $365–435** | **≈ $280–350** |

The split version costs about **$70 more**. Almost all of that is the second nice!nano and
nice!view ($42) plus the second PCB design and assembly order (~$20). Cheap nRF52840 "SuperMini"
clones (~$6 each) bring both totals down by about $19 per controller.

Hand-soldering the 54 diodes and sockets instead of paying for assembly saves $30–45. That's
about 216 SMD joints, which takes 2–3 hours with a fine iron.

For resin, CNC aluminum and laser-cut options, with US import duty, lead times to Kirkland, WA, and the design
changes each one needs, see [case-fabrication.md](case-fabrication.md).

## Build complexity

| | Split | Monolithic |
|---|---|---|
| PCB designs to route and check | 2 (left, right) | 1 |
| Routing difficulty | Easy: 27 keys, 5 × 6 matrix per half | Moderate: 54 keys packed into a 6 × 9 matrix, with columns that run across both halves |
| Controller pins used | 14 of 18 per half | 18 of 18 (no spare GPIO) |
| Firmware | Two images, plus a central/peripheral split pairing step | One image |
| Battery life | Peripheral half lasts longer; central half (with BLE to the laptop) drains faster | One battery, one radio |
| Case parts | 4 (2 trays, 2 frames), each ~148 mm wide: fits any 180 mm printer bed | 2 (tray, frame), 295 mm wide: needs a ≥300 mm bed (Bambu H2D, Prusa XL, Ender 5 Plus) or a print service, or cut and glue at the centre line |
| Extra mechanical work | Glue 3 joining magnets per side with **opposite** polarity facing out, glue 2 dowels into one half | None |
| Docking | Halves must be joined before docking; magnets and dowels keep them aligned | Drops straight on |
| Desk use | Halves can sit shoulder-width apart; ZMK keeps them paired | Fixed |

## Recommendation

Build the **split** version unless the desk use doesn't matter to you. It costs more and has more
parts, but every piece prints on a normal printer, and each PCB is easy to route. The monolithic
board is cheaper and simpler to flash. In return it uses every controller pin, needs a large-format
printer for the case, and can't be pulled apart for the desk.
