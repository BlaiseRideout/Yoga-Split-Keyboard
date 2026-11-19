# Yoga Split Keyboard

A ZMK-powered, low-profile, wireless columnar keyboard that drops onto the lower screen of a
**Lenovo Yoga Book 9i Gen 9 (13IMU9)** in place of the bundled keyboard. It has the same
295.3 × 113 mm footprint and magnet pockets for docking.

![split case render](docs/img/case_split.png)

* **Layout:** 6 × 4 columnar grid plus 3 thumb keys per side, 54 keys in total, Kailh Choc v1 at
  18 × 17 mm spacing. A 4-row layout fits, and the [fit study](docs/design.md#fit-study-4-rows-fit)
  shows why.
* **Controller and display:** a nice!nano v2 with a nice!view in the centre gap of each half, or
  three cheap status LEDs instead of the screen ([details](docs/design.md#status-leds-instead-of-screens)).
  The monolithic version has one of each in the middle.
* **Two variants built from one ergogen config:**
  * **Split.** Two halves that join with 6 × 3 mm magnets and steel dowels for docking, or come
    apart for the desk.
  * **Monolithic.** One PCB and one controller, for comparison.
* **MX-spaced variant:** the same layout at 19.05 mm for Choc v2 / KS-33 switches with MX-stem
  keycaps also fits ([details](docs/design.md#mx-spaced-variant-ergogen-mx-pcb-mx-case-mx)). It uses
  the same firmware.
* **Wired or wireless:** USB-C on the left half (or the mono) works as a wired keyboard, with
  Bluetooth otherwise. `&out OUT_TOG` switches by hand ([details](docs/design.md#wired-usb-mode)).
* **One cable charges both halves** while they're joined, through a magnetic pogo link in the join
  wall ([how](docs/design.md#charging-both-halves-from-one-cable-split-only)).
* **Two PCB builds, THT and SMT:** all through-hole (default, no SMD soldering and no JLC assembly) or
  hotswap with JLC assembly (`hotswap-smd/`). Both are fully diode-per-key for n-key rollover.
* **Cost:** see [docs/cost-comparison.md](docs/cost-comparison.md). A first split build is about
  $319 (through-hole) or $400 (hotswap), delivered to the US including tariffs. The leanest split is about $233.

## Repository layout

| Path | What |
|---|---|
| `ergogen/config.yaml`, `ergogen/footprints/` | Source of truth for key positions, outlines and all three PCBs (ergogen 4.2.1, KiCad 5 template) |
| `pcb/{left,right,mono}/` | KiCad boards (KiCad 7 format, opens in 7, 8 and 9), placed and autorouted with Freerouting |
| `pcb/gerbers/` | Gerber + drill zips, ready to upload to JLCPCB |
| `ergogen-mx/`, `pcb-mx/` | The MX-spaced (19.05 mm) variant: config, boards, Gerbers. `ergogen-mx/footprints` links to `ergogen/footprints` |
| `hotswap-smd/` | SMT build: hotswap sockets and SMD parts placed by JLC. Its ergogen configs, KiCad boards, Gerbers, and JLC BOM/CPL (`fab/`), for Choc and MX |
| `case/case.scad`, `case/outlines/`, `case/stl/` | Parametric OpenSCAD case, its DXF inputs, and exported STLs (tray and frame for left, right and mono). `-D 'spacing="mx"'` builds the MX variant from `case/outlines-mx/` into `case/stl-mx/` |
| `case/stl-open/`, `case/stl-mx-open/` | The frameless style (`-D 'style="open"'`): a low tray with the PCB screwed in, plus a small cover over the controller. See [case styles](docs/design.md#case-styles-full-frame-or-tray--cover). `*_leds.stl` frames and covers have status-LED holes instead of the nice!view window |
| `config/`, `build.yaml` | ZMK user config: shields `yoga_split_left/right` and `yoga_mono`, plus blaise's Cannonkeys Link keymap ported to 54 keys (home row mods, NUM/NAV/FUN/MOUSE/BOARD layers; `tools/port_link_keymap.py`) and build matrix. Builds against the same `caps-word-v0.3` ZMK fork as the Link. `.github/workflows/build-zmk.yml` builds the firmware on push |
| `docs/` | [Design notes and assumptions](docs/design.md), [cost comparison](docs/cost-comparison.md), renders |
| `tools/` | Helper scripts: board prep / DSN export, ZMK generation from ergogen points, fab CSVs |

## Status

| Part | State |
|---|---|
| Fit study and layout | Done |
| PCB schematic / netlist and placement (left, right, mono; Choc and MX) | Done |
| PCB routing | Done with Freerouting 2.1. All six boards are 100% routed with 0 DRC errors (only cosmetic silkscreen warnings). Worth a look in KiCad before ordering: there's no ground pour, and track widths are 0.25 mm signal / 0.4 mm power |
| Gerbers | Done (`pcb/gerbers/`, `pcb-mx/gerbers/`), untested at a fab |
| Case | Done, but untested on a printer |
| Docking magnet positions | **Assumed.** The laptop's EC detects the keyboard magnetically (two positions, no Bluetooth check), so the magnets have to match the stock ones. Map them with viewing film or the dotfiles' `kbdock-test.sh` (see [docs/design.md](docs/design.md#docking)) |
| ZMK firmware | Written, and built by the workflow in CI |

## Regenerating

```sh
npm i -g ergogen@4.2.1
ergogen ergogen -o build/ergogen -d          # PCBs + outlines + points
cp build/ergogen/points/points.yaml tools/   # then:
python3 tools/gen_zmk.py                     # ZMK shields from the key positions
cp build/ergogen/outlines/*.dxf case/outlines/
openscad -D 'variant="left"' -D 'part="tray"' -o case/stl/tray_left.stl case/case.scad
# KiCad python: upgrade the board, set rules, export a DSN for Freerouting
python3 tools/prep_dsn.py build/ergogen/pcbs/left.kicad_pcb pcb/left/yoga_left.kicad_pcb left.dsn
java -jar freerouting-2.1.0.jar --gui.enabled=false -de left.dsn -do left.ses -mp 200
python3 tools/import_ses.py pcb/left/yoga_left.kicad_pcb left.ses left-drc.txt   # adds tracks, runs DRC
tools/export_gerbers.sh pcb/left/yoga_left.kicad_pcb pcb/gerbers/yoga_left-gerbers.zip
python3 tools/check_matrix.py pcb/*/*.kicad_pcb                 # one diode per key, col2row (NKRO)
# SMT build only: python3 tools/gen_fab.py hotswap-smd/pcb/left/yoga_left.kicad_pcb hotswap-smd/pcb/fab/yoga_left
# MX variant: same steps with ergogen-mx -> build/ergogen-mx, pcb-mx/, case/outlines-mx, -D 'spacing="mx"'
```

## Build notes

1. Order the PCBs at **1.2 mm** thickness. That's what the case stack-up assumes.
2. THT (default, all through-hole): fit the 1N4148 diodes first, with their bodies flat on the
   **bottom**, the banded end on the square pad. Solder them from the top and trim the leads flush,
   because the gap under the PCB is 2.2 mm. Then fit the switches from the top and solder them from
   the bottom, trimming their pins too. Bend the PTC flat before you solder it. The controller,
   display, battery, power switch and pogo connector go on the **top**.
   SMT (`hotswap-smd/`): JLC places the sockets and diodes on the bottom, and the switches
   push in from the top.
3. Mount the nice!nano with its components facing the PCB, matching the silkscreen labels. Solder
   it directly, without tall sockets, so the nice!view on top sits flush with the top frame.
   For status LEDs instead of a nice!view, fit the three 3 mm LEDs flat on the PCB (flat side and
   short lead on the square pad) and their resistors on the bottom, and leave the display header empty.
4. Press M2 heat-set inserts into the tray standoffs, and screw the PCB down from the top with
   M2 × 4 low-head screws.
5. Fit the magnetic pogo connector on the split edge of each half: spring pins on the left, flat
   targets on the right. Before closing the case, check both pins line up and that GND matches GND.
6. Glue the docking magnets into the pockets you mapped, and the joining magnets and dowels into
   the split faces.
