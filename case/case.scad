// Yoga Book 9i Gen 9 low-profile keyboard case (OpenSCAD).
// Coordinates match the ergogen config (mm, y up). Outlines are imported from ergogen DXFs.
//
// Render one part at a time, e.g.:
//   openscad -D 'variant="left"'  -D 'part="tray"'  -o tray_left.stl  case.scad
//   openscad -D 'variant="right"' -D 'part="frame"' -o frame_right.stl case.scad
//   openscad -D 'variant="mono"'  -D 'part="tray"'  -o tray_mono.stl  case.scad
// variant: "left" | "right" | "mono"     part: "tray" | "frame" | "assembly"
// spacing: "choc" (18 x 17 mm, ergogen/) | "mx" (19.05 mm, ergogen-mx/)

variant = "left";
part = "assembly";
spacing = "choc";
is_mx = spacing == "mx";
odir = is_mx ? "outlines-mx/" : "outlines/";

/* ---------- stack-up (z = 0 is the bottom face that sits on the laptop's lower screen) ---------- */
floor_t      = 1.0;   // case floor
gap_under    = 2.2;   // room under the PCB for the DO-35 diode bodies (1.9 mm), laid flat on the bottom
pcb_t        = 1.2;   // order the PCB at 1.2 mm to save height
pcb_z        = floor_t + gap_under;          // PCB bottom
pcb_top      = pcb_z + pcb_t;                // 4.4
deck_h       = 5.6;   // frame top sits this far above PCB top (clears nano + battery + nice!view headers)
frame_t      = 1.2;   // top frame thickness
wall_top     = pcb_top + deck_h - frame_t;   // tray wall height where the frame drops in
frame_top    = pcb_top + deck_h;             // overall case height (keycaps rise ~3 mm above this)
wall         = 2.0;   // outer wall thickness
pcb_gap      = 0.5;   // PCB to wall clearance (PCB outline already inset 2.5 from envelope)
cx           = is_mx ? 131.15 : 131;   // split line / board centre x
cy           = is_mx ? 22.2 : 18.6;

/* ---------- hardware ---------- */
insert_d     = 3.2;   // M2 heat-set insert hole (M2 x 3 mm insert, OD 3.2-3.5)
boss_d       = 5.6;
dock_mag_d   = 6.2;   // docking magnets: 6 x 1.5 mm N52 discs, pressed/glued from below
dock_mag_h   = 1.6;
dock_skin    = 0.4;   // plastic left under each docking magnet
join_mag_d   = 6.2;   // joining magnets: 6 x 3 mm N52 discs, axis across the split face
join_mag_h   = 3.1;
dowel_d      = 3.1;   // 3 x 6 mm steel dowel pins for alignment (glue into one half)
dowel_h      = 3.2;

/* ---------- per-variant data (kept in sync with ergogen/config.yaml and ergogen-mx/config.yaml) ---------- */
function mx(x) = 2*cx - x;  // mirror across split line

holes_left  = is_mx ? [[-11.5,72],[0,-25],[40,-22],[47.6,73.6],[123.4,73.9],[123.4,-27]]
                    : [[-8,66],[-8,-28],[40,-24],[47.5,69],[101.3,68],[122.5,-30]];
holes_right = [for (h = holes_left) [mx(h[0]), h[1]]];

// Candidate docking-magnet sites. Exact positions of the stock keyboard's magnets are NOT published:
// map them with magnetic viewing film and fill only the matching pockets (see docs/docking.md).
dock_left   = is_mx
            ? [[-9,74],[10,74],[25,74],[95,74],[112,74],      // back edge, clear of the hotswap sockets
               [-12,40],[-12,10],
               [-6,-29.5],[20,-29.5],[46,-29.5],[110,-31],
               [119,2],[121,38]]
            : [[-9,71],[20,71],[40,71],[75,71],[110,71],
               [-10.5,40],[-10.5,10],
               [-6,-32.5],[20,-32.5],[46,-32.5],[110,-32.5],
               [119,2],[121,38]];   // last two: centre area, under the battery / controller
dock_right  = [for (p = dock_left) [mx(p[0]), p[1]]];

nano_x      = is_mx ? (variant == "left" ? 115 : variant == "right" ? 147.3 : 131.15)
                    : (variant == "left" ? 113 : variant == "right" ? 149 : 131);
switch_x    = is_mx ? (variant == "left" ? 100 : variant == "right" ? 162.3 : 115)
                    : (variant == "left" ? 93  : variant == "right" ? 169 : 114);
reset_xy    = is_mx ? (variant == "left" ? [107,27] : variant == "right" ? [155.3,27] : [118,30])
                    : (variant == "left" ? [104,28] : variant == "right" ? [158,28] : [118,28]);
view_y      = is_mx ? 51.6 : 49.6;   // nice!view centre (display window)
usb_z       = pcb_top + 3.0;

join_mag_y  = is_mx ? [-25, 22, 68] : [-25, 18, 62];
dowel_y     = is_mx ? [-5, 45] : [-8, 42];
link_y      = is_mx ? 29.5 : 28;   // charge-link pogo connector (centre), see ergogen chg_link

env_file    = str(odir, variant == "left" ? "envelope_left.dxf"
            : variant == "right" ? "envelope_right.dxf" : "envelope.dxf");
pcb_file    = str(odir, variant == "left" ? "pcb_left.dxf"
            : variant == "right" ? "pcb_right.dxf" : "pcb_mono.dxf");
holes       = variant == "left" ? holes_left : variant == "right" ? holes_right
            : concat(holes_left, holes_right);
dock        = variant == "left" ? dock_left : variant == "right" ? dock_right
            : concat(dock_left, dock_right);

module envelope() import(env_file);
module pcb2d()    import(pcb_file);
module caps2d()   offset(delta = 0.5) import(str(odir, "caps.dxf"));

// cavity = PCB outline grown by the PCB clearance; walls are what's left of the envelope
module cavity2d() offset(delta = pcb_gap) pcb2d();

module tray() {
    difference() {
        union() {
            // floor
            linear_extrude(floor_t) envelope();
            // walls up to the frame ledge
            linear_extrude(wall_top) difference() { envelope(); cavity2d(); }
            // bosses around docking magnet pockets (top stays below the hotswap-socket gap)
            for (p = dock) translate([p[0], p[1], 0]) cylinder(d = dock_mag_d + 2.4, h = dock_skin + dock_mag_h, $fn = 32);
            // PCB standoffs with heat-set inserts
            for (h = holes) translate([h[0], h[1], 0]) cylinder(d = boss_d, h = pcb_z, $fn = 32);
        }
        // insert holes
        for (h = holes) translate([h[0], h[1], floor_t - 0.4]) cylinder(d = insert_d, h = 10, $fn = 24);
        // docking magnet pockets: blind, opened from the inside so the bottom face stays smooth on the screen
        for (p = dock) translate([p[0], p[1], dock_skin]) cylinder(d = dock_mag_d, h = dock_mag_h + 0.01, $fn = 32);
        // USB-C opening above the nice!nano
        translate([nano_x, 80, usb_z]) cube([12.5, 20, 6.5], center = true);
        // power switch lever slot
        translate([switch_x, 80, pcb_top + 1.9]) cube([6, 20, 3.6], center = true);   // C&K OS102011MA1Q lever
        // split-face features
        if (variant != "mono") join_features();
    }
}

// magnets + dowels on the split face (x = cx)
module join_features() {
    s = variant == "left" ? -1 : 1;  // direction into the half
    zc = wall_top / 2;
    for (y = join_mag_y)
        translate([cx, y, zc]) rotate([0, s * 90, 0]) translate([0,0,-0.01]) cylinder(d = join_mag_d, h = join_mag_h, $fn = 32);
    for (y = dowel_y)
        translate([cx, y, zc]) rotate([0, s * 90, 0]) translate([0,0,-0.01]) cylinder(d = dowel_d, h = dowel_h, $fn = 24);
    // slot for the 2-pin magnetic pogo connector that carries battery charge across the join.
    // Open at the top so the PCB drops in with the connector fitted; its face sits flush with x = cx.
    translate([s < 0 ? cx - 6.1 : cx - 0.01, link_y - 3.3, pcb_top - 0.2]) cube([6.11, 6.6, wall_top]);
}

module frame() {
    // sits on top of the tray walls, flush with the outside; a 1 mm rim drops inside the walls to locate it.
    // Covers controller, battery and the border; keycaps rise through the key opening.
    translate([0,0,wall_top]) linear_extrude(frame_t) difference() {
        envelope();
        caps2d();
        // nice!view: the whole 14 x 36 mm module sits in this opening, flush with the frame top
        translate([nano_x - 7.3, view_y - 18.3]) square([14.6, 36.6]);
        // reset button access
        translate(reset_xy) circle(d = 3, $fn = 24);
    }
    // locating rim
    translate([0,0,wall_top - rim_h]) linear_extrude(rim_h) difference() {
        offset(delta = -0.15) cavity2d();
        offset(delta = -1.15) cavity2d();
        caps2d();
        translate([nano_x - 7.3, view_y - 18.3]) square([14.6, 36.6]);
    }
}
rim_h = 1.0;

module assembly() {
    color("#555") tray();
    color("#bbb", 0.6) frame();
    color("green", 0.5) translate([0,0,pcb_z]) linear_extrude(pcb_t) pcb2d();
}

if (part == "tray") tray();
else if (part == "frame") translate([0,0,-wall_top]) frame();
else assembly();
