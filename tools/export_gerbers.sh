#!/bin/sh
# Export JLCPCB-ready Gerbers + Excellon drill files for a routed board and zip them.
# usage: tools/export_gerbers.sh board.kicad_pcb out.zip      (needs kicad-cli, KiCad >= 7)
set -e
b="$1"; out="$2"; tmp=$(mktemp -d)
kicad-cli pcb export gerbers --output "$tmp/" --layers F.Cu,B.Cu,F.Paste,B.Paste,F.SilkS,B.SilkS,F.Mask,B.Mask,Edge.Cuts --no-x2 --subtract-soldermask "$b" >/dev/null
kicad-cli pcb export drill --output "$tmp/" --format excellon --excellon-separate-th --generate-map --map-format gerberx2 "$b" >/dev/null
rm -f "$out"; (cd "$tmp" && zip -q -r - .) > "$out"
rm -rf "$tmp"
echo "$out"
