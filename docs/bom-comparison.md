# Split vs monolithic: BOM cost and build complexity

Prices are rough single-build estimates in USD (late 2026 hobby-vendor pricing, before shipping and tax).
They were not checked against live listings, so treat them as a guide for comparing the two
variants, not as quotes.

**Shipping to Kirkland, WA (USA):** the totals leave out shipping, sales tax and import duties.
Budget roughly $20–35 per JLCPCB order for express shipping (DHL/UPS/FedEx) to the US. The split
build is one combined order if both PCB designs go in the same cart. On top of that, expect US
import duties and tariffs on goods made in China, plus Washington sales tax. The duty rates have
changed several times since 2025 and weren't checked for this estimate. JLCPCB and most vendors
show them at checkout. nice!nano, nice!view, switches and keycaps from US keyboard vendors ship
domestically, with no import duty on your side.

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
| Case print (PLA/PETG ~120 g, or JLC3DP resin) | 2 trays + 2 frames | 1 tray + 1 frame | — | 5 (self) / ~45 (service) | 5 (self, needs ≥300 mm bed) / ~55 (service) |
| Docking magnets, 6 × 1.5 mm N52 (pack of 50) | ≤ 26 used | ≤ 26 used | — | 8 | 8 |
| Joining magnets, 6 × 3 mm N52 | 6 | 0 | ~$0.40 | 3 | 0 |
| Alignment dowels, 3 × 6 mm steel | 2 | 0 | — | 3 | 0 |
| M2 heat-set inserts + M2 × 4 screws | 12 | 12 | — | 6 | 6 |
| Charge link: 2-pin magnetic pogo pair + 1206 PTC + 1206 10 Ω per half | 1 pair + 2 + 2 | 0 | ~$3 pair, parts < $0.50 | 4 | 0 |
| Magnetic viewing film (one-off, for mapping the stock keyboard) | 1 | 1 | ~$8 | 8 | 8 |
| **Total, self-printed case** | | | | **≈ $293** | **≈ $216** |
| **Total, service-printed case** | | | | **≈ $333** | **≈ $266** |

The charge link adds about **$4** if you hand-solder the two 1206 parts per half. If JLCPCB places
them instead, the PTC is an "extended" part, which adds a ~$3 setup fee per order, or ~$10 in total
for the split pair.

**MX-spaced variant:** the BOM is the same apart from the switches and keycaps. Kailh Choc v2 or
Gateron KS-33 switches cost about the same as Choc v1. Low-profile MX-stem keycaps run ~$0.50–1.00
each, so the totals stay within a few dollars.

The split version costs about **$75 more**. Almost all of that is the second nice!nano and
nice!view ($42) plus the second PCB design and assembly order (~$20). Cheap nRF52840 "SuperMini"
clones (~$6 each) bring both totals down by about $19 per controller.

Hand-soldering the 54 diodes and sockets instead of paying for assembly saves $30–45. That's
about 216 SMD joints, which takes 2–3 hours with a fine iron.

## Build complexity

| | Split | Monolithic |
|---|---|---|
| PCB designs to route and check | 2 (left, right) | 1 |
| Routing difficulty | Easy: 27 keys, 5 × 6 matrix per half. Freerouting finishes each half in seconds | Moderate: 54 keys packed into a 6 × 9 matrix, with columns that run across both halves. Freerouting still finishes it |
| Controller pins used | 14 of 18 per half | 18 of 18 (no spare GPIO) |
| Firmware | Two images, plus a central/peripheral split pairing step | One image |
| Battery life | Peripheral half lasts longer; central half (with BLE to the laptop) drains faster | One battery, one radio |
| Case parts | 4 (2 trays, 2 frames), each ~148 mm wide: fits any 180 mm printer bed | 2 (tray, frame), 295 mm wide: needs a ≥300 mm bed (Bambu H2D, Prusa XL, Ender 5 Plus) or a print service, or cut and glue at the centre line |
| Extra mechanical work | Glue 3 joining magnets per side with **opposite** polarity facing out, glue 2 dowels into one half, fit the pogo charge connector | None |
| Charging | One cable charges both halves while joined; each half charges on its own when apart | One cable |
| Docking | Halves must be joined before docking; magnets and dowels keep them aligned | Drops straight on |
| Desk use | Halves can sit shoulder-width apart; ZMK keeps them paired | Fixed |

## Recommendation

Build the **split** version unless the desk use doesn't matter to you. It costs more and has more
parts, but every piece prints on a normal printer, and each PCB is easy to route. The monolithic
board is cheaper and simpler to flash. In return it uses every controller pin, needs a large-format
printer for the case, and can't be pulled apart for the desk.
