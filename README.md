# Yoga Split Keyboard

A ZMK-powered, low-profile, wireless columnar keyboard that drops onto the lower screen of a
**Lenovo Yoga Book 9i Gen 9 (13IMU9)** in place of the bundled keyboard. It has the same
295.3 × 113 mm footprint and magnet pockets for docking.

![split case render](docs/img/case_split.png)

* **Layout:** 6 × 4 columnar grid plus 3 thumb keys per side, 54 keys in total, Kailh Choc v1 at
  18 × 17 mm spacing. A 4-row layout fits, and the [fit study](docs/design.md#fit-study-4-rows-fit)
  shows why.
* **Controller and display:** a nice!nano v2 with a nice!view in the centre gap of each half.
  The monolithic version has one of each in the middle.
* **Two variants built from one ergogen config:**
  * **Split.** Two halves that join with 6 × 3 mm magnets and steel dowels for docking, or come
    apart for the desk.
  * **Monolithic.** One PCB and one controller, for comparison.
* **Cost and complexity:** see [docs/bom-comparison.md](docs/bom-comparison.md). Split is about
  $289 and monolithic about $216, both with a self-printed case.

## Repository layout

| Path | What |
|---|---|
| `ergogen/config.yaml`, `ergogen/footprints/` | Source of truth for key positions, outlines and all three PCBs (ergogen 4.2.1, KiCad 5 template) |
| `pcb/{left,right,mono}/` | KiCad boards (KiCad 7 format, opens in 7, 8 and 9) with footprints placed and netlisted. **Not routed yet**, see *Status* |
| `pcb/fab/` | JLCPCB BOM and CPL for the machine-assembled parts (diodes, hotswap sockets, power switch, reset button) |
| `case/case.scad`, `case/outlines/`, `case/stl/` | Parametric OpenSCAD case, its DXF inputs, and exported STLs (tray and frame for left, right and mono) |
| `config/`, `build.yaml` | ZMK v0.3 user config: shields `yoga_split_left/right` and `yoga_mono`, keymap, and build matrix. `.github/workflows/build-zmk.yml` builds the firmware on push |
| `docs/` | [Design notes and assumptions](docs/design.md), [BOM and complexity comparison](docs/bom-comparison.md), renders |
| `tools/` | Helper scripts: board prep / DSN export, ZMK generation from ergogen points, fab CSVs |

## Status

| Part | State |
|---|---|
| Fit study and layout | Done |
| PCB schematic / netlist and placement (left, right, mono) | Done. DRC is clean apart from unrouted nets and cosmetic silkscreen warnings |
| PCB routing | **To do.** Run Freerouting on the DSN from `tools/prep_dsn.py`, or route by hand. The 27-key halves are straightforward |
| Gerbers | After routing |
| Case | Done, but untested on a printer |
| Docking magnet positions | **Assumed.** Map them on the stock keyboard with magnetic viewing film (see [docs/design.md](docs/design.md#docking-assumption-the-magnet-positions-arent-published)) |
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
```

## Build notes

1. Order the PCBs at **1.2 mm** thickness. That's what the case stack-up assumes.
2. Hotswap sockets and diodes go on the **bottom** side. The controller, display, battery, power
   switch and reset button go on the **top**.
3. Mount the nice!nano with its components facing the PCB, matching the silkscreen labels. Solder
   it directly, without tall sockets, so the nice!view on top sits flush with the top frame.
4. Press M2 heat-set inserts into the tray standoffs, and screw the PCB down from the top with
   M2 × 4 low-head screws.
5. Glue the docking magnets into the pockets you mapped, and the joining magnets and dowels into
   the split faces.
