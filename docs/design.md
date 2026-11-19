# Design notes

## Target envelope

| | Value | Source |
|---|---|---|
| Stock keyboard ("Yoga Book 9 Bluetooth KB") | **295.3 × 113 × 7.8 mm**, 850 mAh, USB-C charging, Bluetooth 5.2 | Lenovo *User Guide Yoga Book 9i (13", 9)*, model 13IMU9, p. 10 (same figures in the Gen 8 / 13IRU8 guide) |
| Laptop body | 299.1 × 203.9 × 15.95 mm | Lenovo spec page for 13IMU9 |
| Lower display | 13.3" 16:10, 2880 × 1800; active area ≈ 286.5 × 179.1 mm (calculated) | Lenovo PSREF |
| Docking behaviour | On the upper part of the bottom screen, a virtual touchpad appears below the keyboard. On the lower part, a widget bar appears above it. | User guide p. 23 |
| Hall sensors | "Hall sensor: 4" in the system sensor table; what they detect is not stated | User guide p. 9, PSREF |

This design matches the **295.3 × 113 mm footprint** exactly (6 mm corner radius, which is assumed).
It does **not** match the 7.8 mm thickness. Choc switches with hotswap sockets and a 3D-printed case
come out at about **10 mm to the frame top and ~13 mm to the keycap tops**. See *Stack-up* below.

## Fit study: 4 rows fit

![fit study](img/fit_study.png)

The layout per half is 6 columns × 4 rows, plus a 3-key thumb arc (10° splay per key). It uses Kailh
Choc spacing (18 × 17 mm) with Voyager-like column stagger (ring +6, middle +3, index −3, inner
−3 mm relative to the neighbouring column).

* Key block depth including thumbs: **99.2 mm**, against 113 mm available, leaving ~7 mm of border
  front and back.
* Width: outer edges sit 7.9 mm inside the envelope. The **centre gap between the two inner columns
  is 64.5 mm**. Each half uses its 32 mm of that gap for a nice!nano with a nice!view stacked on
  top, a 20 × 30 mm LiPo, the reset button and the join wall.
* At **19.05 mm (MX-style) spacing**, which you'd need for Choc v2 / Gateron KS-33 with MX keycaps,
  the same layout is ~111 mm deep. That leaves under 1 mm per side for walls, so it doesn't fit.
  A 3-row layout would fit at 19.05 mm spacing.

## Stack-up (z from the laptop screen up)

| Layer | Thickness | Top at |
|---|---|---|
| Case floor (docking magnets sit in blind pockets with a 0.4 mm skin) | 1.0 | 1.0 |
| Air gap for Choc hotswap sockets (1.85 mm) | 2.2 | 3.2 |
| PCB (order at 1.2 mm) | 1.2 | 4.4 |
| Controller, battery and nice!view under the top frame | 4.4 | 8.8 |
| Top frame | 1.2 | **10.0** |
| Choc v1 switch + low-profile keycap above the PCB | ~8.3 | **~12.7** |

Ways to get thinner, roughly in order of payoff:
1. Solder the switches directly with no hotswap sockets: −1.2 mm (gap shrinks to ~1 mm).
2. Kailh PG1316S ultra-low-profile switches (solder-only, own keycaps): roughly −3 mm. This
   needs a new footprint and isn't designed here.
3. Mount the nice!nano face-down without sockets and use a 1 mm FR4 frame instead of print: −1 mm.

## Docking (assumption: the magnet positions aren't published)

Lenovo's user guides, both hardware maintenance manuals (13IRU8 and 13IMU9), and reviews all say
the keyboard is "held in place by magnets". None of them gives magnet positions or says what the
four hall sensors detect. No teardown of the keyboard was found. What we know is the behaviour:
place the keyboard on the upper or lower half of the bottom screen, and Windows shows a touchpad
or a widget bar.

So the case has **11 candidate docking-magnet pockets per half** (22 total), each 6.2 mm in
diameter and 1.6 mm deep, for 6 × 1.5 mm N52 discs. They sit along the back edge, the front edge
and the outer edge, and they're opened from the inside so the bottom face stays smooth on the glass.

**How to map the real positions (≈10 minutes):**
1. Lay magnetic viewing film on the underside of the stock keyboard and trace the dark spots
   (pole boundaries) onto paper at 1:1.
2. Hold a compass over each spot and note N/S.
3. Overlay the tracing on `docs/img/case_bottom.png` (or print `case/outlines/envelope.dxf` 1:1)
   and fill the pockets that line up. If a spot falls between pockets, add its position to
   `dock_left` in `case/case.scad` and re-export.
4. Match polarity, so the hall sensors see the same field the stock keyboard gives them.

If the touchpad / widget-bar switch turns out to come from Lenovo's software detecting the stock
keyboard's Bluetooth ID, not from the magnets, this keyboard still docks and holds. You'd then
toggle the virtual touchpad with Lenovo's own gesture or hotkey.

## Split joining

Each half's inner wall is 5 mm thick. It carries:
* 3 × **6 × 3 mm N52** magnets, axis across the split, at y = −25, 18 and 62 mm. Glue them in
  with **opposite poles facing out** on the two halves.
* 2 × **3 × 6 mm steel dowel pins**, glued into one half, which locate in matching holes in the
  other half and stop shear when you type.

That gives the UHK / Dygma-style "click together" join. A mechanical alternative is a sliding
dovetail key printed separately. It's not modelled here, but it would replace the dowel holes.

## Electrical

* MCU: nice!nano v2 (or any Pro Micro-footprint nRF52840). Battery → MSK-12C02 switch → RAW.
* Display: nice!view on the standard ZMK pins (CS = D1, MOSI = D2, SCK = D3), header order
  MOSI, SCK, VCC, GND, CS.
* Matrix, split: rows D4–D8 (num, top, home, bottom, thumb), columns D21, D20, D19, D18, D15, D14
  (outer → inner), diodes col2row. The right half lists its columns inner → outer in firmware so
  matrix columns read left to right across the board.
* Matrix, monolithic: 54 keys packed into **6 rows (D4–D9) × 9 columns (D21, D20, D19, D18, D15,
  D14, D16, D10, D0)**. Left-half key *i* (row-major over 4 × 6, thumbs 24–26) goes to
  (i ÷ 9, i mod 9). The right half is the same, shifted down 3 rows. That uses all 18 Pro Micro
  GPIOs, with nothing spare.
