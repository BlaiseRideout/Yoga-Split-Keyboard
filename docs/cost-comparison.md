# Cost comparison: build routes, split vs monolithic, 1 or 2 builds

All prices are in USD for delivery to **Kirkland, WA**, as of November 2026. Where a figure comes
from a vendor page, it says so in *Sources*. Everything else is an estimate. JLCPCB shows the exact
PCB, assembly, shipping and tariff charges at checkout. Check those before you order.

## The two PCB routes

Both routes are in the repo and use the same layout, case and firmware.

| | **A. All through-hole** (default: `pcb/`, `pcb-mx/`) | **B. Hotswap + JLC assembly** (`hotswap-smd/`) |
|---|---|---|
| Switches | Soldered to the PCB (5-pin Choc holes) | Kailh hotswap sockets, so switches pull out |
| Diodes | 1N4148, DO-35 through-hole, one per key, body flat on the bottom | 1N4148W SOD-123, placed by JLC |
| Power switch, reset | C&K OS102011MA1QN1 right-angle THT slide; reset is 2 THT pads (short with tweezers, or fit a 2-pin tact switch; the keymap's `&bootloader` key covers normal use) | MSK-12C02 and SKQG, placed by JLC |
| Charge link (split) | THT pogo pair, radial PTC (Bourns MF-R010, bend flat), axial 10 Ω | SMD pogo, 1206 PTC and 10 Ω, placed by JLC |
| Battery | Leads go through two holes | Leads go on two SMD pads |
| **SMD parts you solder** | **None** (0 SMD pads on the boards) | **None** (JLC places them all) |
| THT joints you solder, split | ~220: 54 switches × 2, 54 diodes × 2, plus switch, fuse, resistor, pogo, battery and controller | ~60: controller, nice!view header, battery, pogo |
| Routing | Freerouting, 100%, 0 DRC errors on all six boards | Same |
| Thickness | Same case and stack-up | Same |

**Both routes give full n-key rollover in hardware.** Every key, including the thumb keys, has its
own diode, oriented anode-to-switch and cathode-to-row for ZMK's `col2row` scanning. No diodes are
shared or left out, and no two keys share a matrix position. `tools/check_matrix.py` checks this from
the netlist of every board. All 12 boards pass: 27 keys / 27 diodes / 27 positions per half, and 54
on each mono board. The firmware sends NKRO HID reports (`CONFIG_ZMK_HID_REPORT_TYPE_NKRO=y`), so the
host sees every key in a combo, not just the first six.

## Switches: prelubed, tactile, low-profile

| Spacing | Switch | Fits these boards? | Price |
|---|---|---|---|
| Choc 18 × 17 (`pcb/`) | **lowprokb Choc v1 Sunset**: tactile, 40 gf, factory-lubed | Yes, Choc v1 5-pin | $0.98 each in 5-packs (Beekeeb, HK); €0.66 ex VAT in 10-packs (splitkb, EU) |
| Choc 18 × 17 | Ambients Sunrise: silent tactile, Choc v1 | Yes | €0.85 ex VAT in 10-packs (splitkb). Lube not stated, and listed as "coming later" |
| MX 19.05 (`pcb-mx/`) | **Kailh Choc v2 Brown**: tactile, factory-lubed, MX-stem | Yes, Choc v2 uses the Choc contact pins (3-pin, no side posts) | ~$0.56–0.60 each |
| MX 19.05 | Kailh Deep Sea (Choc v2): silent tactile, factory pre-lubricated | Yes | $5.95 per 10 (Thock King, US) |
| — | Gateron KS-33 LP 2.0 Chocolate: tactile, factory-lubed, $12.96 per 36 (CannonKeys, US) | **No.** KS-33 has its own pin layout and socket. It would need a new footprint | |

The tables below use the bold picks. 60 switches cover one build plus spares, so that's ~$59 for
Sunset and ~$36 for Choc v2 Brown. The MX route also needs low-profile MX-stem keycaps, about
the same price as Choc caps.

## Cost per build

"First build" includes everything you can only buy in bulk: JLC's minimum of 5 PCBs per design,
assembly setup, and packs of magnets, diodes and inserts. "Second build" is what a second keyboard
adds. It reuses the spare PCBs (and, on route B, the second assembled board), so it's mostly
controllers, screens, switches and caps.

### Split (Choc spacing, nice!nano, two nice!views, Sunset switches, MBK caps, self-printed case)

| Item | Route A, THT | Route B, hotswap | Note |
|---|---|---|---|
| 2 × nice!nano v2 | 50 | 50 | US vendor |
| 2 × nice!view | 34 | 34 | US vendor |
| 2 × LiPo 402030 | 10 | 10 | |
| 60 × Sunset tactile switches | 59 | 59 | Choc v2 Brown on the MX route: 36 |
| 54 × Choc keycaps (MBK-style) | 40 | 40 | |
| JLC PCBs: 2 designs × 5 pcs, 2-layer, 1.2 mm | 30 | 30 | 2-layer is already the cheapest stack-up |
| JLC assembly: 2 of each design, setup, extended-part fees, parts | — | ~65 | Route A has no assembly at all |
| US tariff on the JLC order, ~35% DDP, collected at checkout | ~11 | ~33 | Rate per JLC's March 2026 notice |
| JLC shipping, DHL/UPS DDP to Kirkland | ~25 | ~25 | |
| THT parts: 100 × 1N4148, 2 slide switches, PTC + resistor | ~7 | — | Digikey/Mouser, domestic |
| Charge-link pogo pair | 3 | 3 | |
| Magnets (dock pack + join), dowels, inserts, screws | 20 | 20 | |
| Magnetic viewing film | 8 | 8 | Optional: blaise can map the magnets with `kbdock-test.sh` instead |
| Filament | 5 | 5 | Or a print service: MJF nylon from a US vendor, ~$80–150 delivered for the split and ~$70–140 for the mono. Resin, CNC and laser-cut options are in [case-fabrication.md](case-fabrication.md) |
| US vendor shipping (controllers, switches, caps) | ~15 | ~15 | |
| **First build** | **≈ $317** | **≈ $397** | |
| **Second build adds** | **≈ $230** | **≈ $230** | Spare PCBs, assembled boards and packs are reused |
| **Two builds, each** | **≈ $274** | **≈ $314** | |

### Monolithic (same parts, one controller and screen, needs a ≥ 300 mm printer bed)

| | Route A, THT | Route B, hotswap |
|---|---|---|
| **First build** | **≈ $255** | **≈ $300** |
| **Second build adds** | **≈ $170** | **≈ $170** |
| **Two builds, each** | **≈ $213** | **≈ $235** |

The mono has one 290 × 108 mm design (~$25 for 5), one assembly order on route B (~$35 plus
tariff), and one nice!nano and one nice!view. Its case is a single 295 mm part, so it needs a large
printer or a print service (about +$50).

### What MOQs leave over

| Item | Minimum you buy | One split build uses | Left over |
|---|---|---|---|
| PCBs | 5 per design | 1 left + 1 right | 4 + 4 (3 + 3 after a second build) |
| JLC assembly (route B) | 2 boards per design | 1 + 1 | 1 + 1 assembled boards, which the second build uses |
| 1N4148 (route A) | ~100 | 54 | 46 |
| Switches | 10-packs | 54 (+6 spare) | 6 |
| Docking magnets | 50-pack | ≤ 26 | 24+ |

## Where to order the PCBs (and assembly)

Route A needs **bare boards only**, since nothing is surface-mount. That leaves the fab as the only
thing to choose. Route B also needs SMD assembly. Prices are for one split set (left + right) or one
mono board, delivered to Kirkland.

| Source | Made in | Route A: bare boards | Route B: assembly | US tariff | Notes |
|---|---|---|---|---|---|
| **JLCPCB** | China | **≈ $66 split / ≈ $59 mono** (5 of each design, ~35% duty and DHL included) | ≈ $65 + 35% | ~35%, prepaid (DDP) | Cheapest even with the tariff. Instant quote |
| PCBWay | China | Similar to JLC, a little higher | Yes, from qty 1 | Same China rate | Alternative if JLC is out of stock |
| **OSH Park** | Oregon, USA | **≈ $234 split / ≈ $243 mono** for 3 copies ($5/in², free US shipping). Purple, 1.6 mm, ENIG | No | None | Cheapest US option. Boards are 1.6 mm, not 1.2: re-export the case with `-D pcb_t=1.6` (the case grows 0.4 mm taller) |
| Aisler | Germany | Quote needed (sets of 3) | Yes, from 1 board, THT and SMD | EU rate (lower than China) | Free worldwide shipping per its site. Upload the Gerbers for a price |
| MacroFab | Houston, USA | Via their platform | Yes, no minimum order | None | Instant quote from files. Expect well above JLC: forum reports put US assembly at $50–200 per board for tiny runs |
| CircuitHub / Screaming Circuits | MA / OR, USA | Via them | Yes | None | Same price bracket as MacroFab |

**Cheapest reputable choice: JLCPCB, route A.** The tariff adds about $11 per order on bare boards,
which is far less than the price gap to US fabs. **If you'd rather not order from China,
OSH Park** is the cheapest US source, at about $170 more for the split. It doesn't do assembly,
so that works only with route A. US assembly for route B (MacroFab, CircuitHub) would run several
hundred dollars for two boards, so route B makes sense only at JLC.

Two things to check at checkout, because they move often. The China tariff stack changed several
times in 2026: a Section 122 baseline expired in July, and PCB exclusions ended on November 10.
And for exact US prices, upload the Gerber zips to the vendors' instant quotes; they need an account.

## Alternative: a custom case around an off-the-shelf wireless PCB

| Board | Layout | What you get | Price | Fits 295.3 × 113? | Notes |
|---|---|---|---|---|---|
| **Typeractive Corne (Choc)**, partially assembled | 3 × 6 + 3 per half (42 keys, no number row) | PCB pair with diodes, hotswap sockets, battery jacks, power switches and reset buttons pre-soldered. You solder the nice!nano and nice!view headers (THT) | $35 (US vendor, no tariff). **Sold out when checked** | Yes, easily (3 rows) | Choc v1 only. Proven ZMK board |
| Keebmaker Sofle LP, prebuilt wireless | 6 × 4 + 5 per half (58 keys) | Fully built with their switches and caps | from $259 (built in the USA) | Unknown, needs PCB dimensions | Switch choice limited to their options |
| Beekeeb HSHS52, pre-soldered wireless | 52 keys | Soldered PCB, socketed nice!nanos | $227 | Unknown | No switches, caps or case |
| Kriscables Corne Choc PCB | 42 keys | Bare PCBs | €15.90 | Yes | All SMD left to you, so it breaks the no-SMD rule |
| Keebart Sofle Choc Pro | 58 keys | Built | $249+ | 132 × 106 mm per half | RP2040, **wired only** |

**Corne route, estimated:** PCB pair $35 + 2 nice!nano $50 + 2 nice!view $34 + 50 Sunset switches
$49 + 42 caps $32 + 2 LiPo $10 + case parts and magnets ~$30 + US shipping ~$15 ≈ **$255**, versus
≈ $317 for route A. It also avoids JLC and tariffs entirely.

What it gives up:
- **The number row.** It's 3 rows and 42 keys, against 54 here.
- **The charge link,** unless a pogo pair is wired to the battery jacks by hand.
- Nothing on docking, because the docking magnets live in the case either way. Thickness is about
  the same, since it's Choc v1 on a 1.6 mm PCB.

No mass-produced wireless 4-row Choc board was found that's both pre-soldered and confirmed to fit.
For the 4-row layout with charge pass-through, route A stays the cheapest.

## Ways to cut more (any route)

| Change | Split saves | Mono saves | Trade-off |
|---|---|---|---|
| Route A instead of B | ~$80 first build | ~$50 | No hotswap. ~220 THT joints, about 2 hours |
| nRF52840 "SuperMini" instead of nice!nano | ~$35 (2 × ~$6, plus tariff) | ~$17 | Same footprint and firmware target. Quality and battery-sense accuracy vary by seller |
| One nice!view, left only (`yoga_split_right_noscreen` firmware) | $17 | — | The right half has no screen; the left still shows layer, battery and connection status |
| Generic AliExpress Choc keycaps (~$0.30) | ~$24 | ~$24 | Thinner plastic, legends vary. Tariffs apply |
| Choc v2 Brown on the MX route instead of Sunset | ~$23 | ~$23 | MX spacing and MX-stem low-profile caps |
| Skip the viewing film, map the magnets with `kbdock-test.sh` | $8 | $8 | Needs the Linux setup from the dotfiles |
| **Leanest split** (A + SuperMini + one screen + generic caps + no film) | **≈ $233** first build, **≈ $150** second | | |
| **Leanest mono** (A + SuperMini + generic caps + no film) | | **≈ $206** first, ≈ $125 second | |

## Build complexity

| | Split | Monolithic |
|---|---|---|
| PCB designs | 2 | 1 |
| Routing | Easy: 27 keys, 5 × 6 matrix per half | Moderate: 54 keys packed into a 6 × 9 matrix (all 18 GPIOs) |
| Firmware | Two images and a pairing step | One image |
| Case parts | 4, each ~148 mm, fits any printer | 2, 295 mm, needs a ≥ 300 mm bed |
| Extra mechanical work | Join magnets (opposite poles), dowels, pogo charge connector | None |
| Charging | One cable charges both halves while joined | One cable |
| Desk use | Halves can sit shoulder-width apart | Fixed |

## Recommendation

For one or two keyboards with your no-SMD-soldering rule, **route A (all through-hole), split**.
It needs no JLC assembly, so there's nothing to pay tariff on beyond the bare PCBs. Every joint is
a through-hole joint, and the five PCBs per design already cover a second build. Go to route B only
if being able to swap switches is worth ~$40 per keyboard over two builds.

## Sources

- JLCPCB, [U.S. tariff policy FAQ](https://jlcpcb.com/help/article/us-tariff-policy-faq) (updated Oct 29, 2026) and [logistics update](https://jlcpcb.com/news/logistics-update-us-china-tariff) (March 17, 2026 rates: PCB 35%, SMT 35%; DDP for individual US orders). The FAQ also lists rate components that changed during 2026, so confirm at checkout.
- Switch prices: [splitkb Sunset](https://splitkb.com/products/sunset-kailh-low-profile-choc-switches), [kbd.news Sunset offers](https://kbd.news/switch/lowprokb-Choc-V1-Sunset-switch-65.html), [kbd.news Choc v2 Brown](https://kbd.news/switch/Kailh-Choc-V2-Brown-456.html), [Thock King Deep Sea](https://www.thockking.com/products/kailh-deep-sea-low-profile-choc-silent-tactile-switches), [CannonKeys KS-33 Chocolate](https://cannonkeys.com/products/gateron-ks-33-low-profile-2-0-chocolate-tactile-switch), [splitkb Ambients](https://splitkb.com/collections/all/products/ambients-kailh-low-profile-choc-switches).
- US fabs and assembly: [OSH Park 2-layer service](https://docs.oshpark.com/services/two-layer/) ($5/in² for 3 copies, made in the US), [Maskset tariff math](https://www.maskset.net/blog/2025/05/15/tariff-math-for-two-layer-prototype-pcbs-oshpark-vs-imported-fabs/), [lcamtuf vendor comparison](https://blog.coredump.cx/p/comparing-hobby-pcb-vendors) (Jan 2026 update), [Hackaday on US prototyping](https://hackaday.com/2025/07/06/does-made-in-america-make-sense-for-pcb-prototyping/), [Octopart 2026 tariff reset](https://octopart.com/pulse/p/tariff-reset-pcb-workarounds), [Aisler assembly](https://aisler.net/en/products/assembly), [MacroFab](https://www.macrofab.com/platform), [KiCad forum on US low-quantity assembly](https://forum.kicad.info/t/usa-single-low-amount-assembly-anyone-got-any-pointers-for-me/23048), [Contextual Electronics forum](https://forum.contextualelectronics.com/t/recommendations-for-pcb-assembly-in-usa/5638).
- Off-the-shelf boards: [Typeractive Corne](https://typeractive.xyz/products/corne-partially-assembled-pcb), [Keebmaker](https://keebmaker.com), [Beekeeb HSHS52](https://shop.beekeeb.com/products/pre-soldered-wireless-hshs52-choc-v2-split-keyboard), [Kriscables Corne Choc](https://kriscables.com/product/corne-choc-pcb/), [Keebart Sofle Choc Pro](https://www.etsy.com/listing/1754988054/sofle-choc-pro-split-keyboard-ergonomic).
- Everything else (controllers, screens, JLC fab and assembly, shipping, small parts) is an estimate from typical late-2026 hobby pricing and wasn't checked against live listings.
