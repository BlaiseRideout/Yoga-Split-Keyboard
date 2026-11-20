// Thin case for the PG1316S build (ergogen-thin/, pcb-thin/). OpenSCAD, mm, y up, same coordinates
// as the ergogen config. Outlines come from case/outlines-thin/ (ergogen-thin's DXFs).
//
//   openscad -D 'variant="left"' -D 'part="tray"'  -o stl-thin/tray_left.stl  case_thin.scad
//   openscad -D 'variant="left"' -D 'part="frame"' -o stl-thin/frame_left.stl case_thin.scad
// variant: "left" | "right" | "mono"     part: "tray" | "frame" | "assembly"
//
// Stack-up (z = 0 on the laptop's lower screen):
//   0.0 - 1.4  floor (6 x 1 mm docking magnets in 1.0 mm pockets, 0.4 mm skin)
//   1.4 - 2.2  PCB, ordered at 0.8 mm. Nothing on its bottom side: it rests on the floor
//   2.2 - 6.4  PG1316S switch + cap (4.2 mm)
//   4.8 - 5.6  top frame over the keys: caps stand 0.8 mm proud of it
//   5.6 - 6.4  raised deck over the controller, battery and LEDs (nice!nano 3.2 mm, cell 3.0 mm)
// Overall 6.4 mm, against 7.8 mm for the stock keyboard.

variant = "left";
part = "assembly";
odir = "outlines-thin/";

floor_t   = 1.4;
pcb_t     = 0.8;
pcb_z     = floor_t;
pcb_top   = pcb_z + pcb_t;          // 2.2
low_z     = 4.8;                    // underside of the frame over the keys (= tray wall top)
low_t     = 0.8;                    // frame over the keys: 4.8 - 5.6
deck_z    = low_z + low_t;          // 5.6: underside of the raised deck
deck_t    = 0.8;                    // raised deck: 5.6 - 6.4
top_z     = deck_z + deck_t;        // 6.4 overall
lip       = 1.2;                    // the deck's edge wall where it meets the low frame
wall      = 2.0;
pcb_gap   = 0.5;
cx        = 131;
cy        = 18.6;

// hardware
dock_mag_d = 6.2;  dock_mag_h = 1.05;  dock_skin = 0.4;   // 6 x 1 mm N52 discs
join_mag_d = 4.2;  join_mag_h = 2.1;  join_mag_z = 2.8;   // 4 x 2 mm N52 discs, 4 per face
dowel_d    = 2.1;  dowel_h    = 5.2;  dowel_z    = 3.0;   // 2 x 10 mm steel pins, inside the 5.5 mm join wall
post_d     = 4.6;  insert_d   = 3.2;                      // frame posts with M2 x 2.5 heat-set inserts
screw_d    = 2.3;  csk_d      = 4.2;                      // M2 countersunk screws from below

function mx(x) = 2 * cx - x;
holes_left  = [[-8,66],[-8,-28],[40,-24],[47.5,69],[101.3,68],[122.5,-30]];
holes_right = [for (h = holes_left) [mx(h[0]), h[1]]];
dock_left   = [[-9,71],[20,71],[40,71],[75,71],[110,71],
               [-10.5,40],[-10.5,10],
               [-6,-32.5],[20,-32.5],[46,-32.5],[110,-32.5],
               [119,2],[121,38]];
dock_right  = [for (p = dock_left) [mx(p[0]), p[1]]];
join_mag_y  = [-12, 8, 42, 56];
dowel_y     = [-24, 66];
link_y      = 28;

side_x   = function(x) variant == "right" ? mx(x) : variant == "mono" ? x + 18 : x;
nano_x   = side_x(113);
switch_x = variant == "mono" ? 111 : side_x(93);
reset_xy = [side_x(118.3) - (variant == "right" ? 0 : 0), 33];
led_xy   = [for (y = [3, 6.5, 10]) [side_x(119.5), y]];

holes = variant == "left" ? holes_left : variant == "right" ? holes_right : concat(holes_left, holes_right);
dock  = variant == "left" ? dock_left  : variant == "right" ? dock_right  : concat(dock_left, dock_right);
env_file = str(odir, variant == "left" ? "envelope_left.dxf" : variant == "right" ? "envelope_right.dxf" : "envelope.dxf");
pcb_file = str(odir, variant == "left" ? "pcb_left.dxf" : variant == "right" ? "pcb_right.dxf" : "pcb_mono.dxf");

module envelope() import(env_file);
module pcb2d()    import(pcb_file);
module cavity2d() offset(delta = pcb_gap) pcb2d();
module caps2d()   offset(delta = 0.5) import(str(odir, "caps.dxf"));

// the raised deck: controller, battery, charge parts and LEDs. Keys stay open through it.
module deck2d() difference() {
    intersection() {
        envelope();
        if (variant == "left")  translate([103, -1.5]) square([cx - 103 + 1, 100]);
        if (variant == "right") translate([cx - 1, -1.5]) square([mx(103) - cx + 1, 100]);
        if (variant == "mono")  translate([121, -1.5]) square([20, 100]);
    }
    caps2d();
}
// inside of the deck, where parts rise above the low frame's underside
module deck_inner2d() intersection() { offset(delta = -lip) deck2d(); cavity2d(); }

/* rounded outer edges, as on the standard case */
edge_r_bottom = 1.0; edge_r_top = 1.2; edge_steps = 6;
module env_inset(d) {
    if (variant == "mono") offset(r = -d) import(str(odir, "envelope.dxf"));
    else intersection() {
        offset(r = -d) import(str(odir, "envelope.dxf"));
        translate([variant == "left" ? cx - 500 : cx, -500]) square([500, 1000]);
    }
}
function fillet_inset(r, h) = r - sqrt(max(0, r*r - (r - h)*(r - h)));
module round_mask() {
    n = edge_steps; rb = edge_r_bottom; rt = edge_r_top;
    for (i = [0 : n - 1]) translate([0, 0, i * rb / n])
        linear_extrude(rb / n + 0.001) env_inset(fillet_inset(rb, (i + 0.5) * rb / n));
    translate([0, 0, rb]) linear_extrude(top_z - rb - rt + 0.001) env_inset(0);
    for (i = [0 : n - 1]) translate([0, 0, top_z - rt + i * rt / n])
        linear_extrude(rt / n + 0.001) env_inset(fillet_inset(rt, rt - (i + 0.5) * rt / n));
}

module tray() difference() {
    union() {
        linear_extrude(floor_t) envelope();
        linear_extrude(low_z) difference() { envelope(); cavity2d(); }
        // under the deck the walls carry on up to the deck
        linear_extrude(deck_z) difference() { intersection() { envelope(); deck2d(); } cavity2d(); }
    }
    // countersunk screw holes: M2 screws from below, through the PCB, into inserts in the frame posts
    for (h = holes) translate([h[0], h[1], 0]) {
        translate([0, 0, -0.01]) cylinder(d = screw_d, h = floor_t + 0.02, $fn = 24);
        translate([0, 0, -0.01]) cylinder(d1 = csk_d, d2 = screw_d, h = (csk_d - screw_d) / 2, $fn = 24);
    }
    // docking magnets: blind pockets opened from the inside, under the PCB
    for (p = dock) translate([p[0], p[1], dock_skin]) cylinder(d = dock_mag_d, h = dock_mag_h + 0.01, $fn = 32);
    // USB-C opening (nice!nano soldered flat on the PCB, mid-mount port)
    translate([nano_x, 80, pcb_top + 1.6]) cube([10, 20, 3.8], center = true);
    // side slide switch lever
    translate([switch_x, 80, pcb_top + 0.75]) cube([6, 20, 2.0], center = true);
    if (variant != "mono") join_features();
}

module join_features() {
    s = variant == "left" ? -1 : 1;
    for (y = join_mag_y) translate([cx, y, join_mag_z]) rotate([0, s * 90, 0])
        translate([0, 0, -0.01]) cylinder(d = join_mag_d, h = join_mag_h, $fn = 32);
    for (y = dowel_y) translate([cx, y, dowel_z]) rotate([0, s * 90, 0]) {
        translate([0, 0, -0.01]) cylinder(d = dowel_d, h = dowel_h, $fn = 24);
        translate([0, 0, -0.01]) cylinder(d1 = dowel_d + 0.8, d2 = dowel_d, h = 0.4, $fn = 24);
    }
    // pogo connector slot, open at the top
    translate([s < 0 ? cx - 6.1 : cx - 0.01, link_y - 3.3, pcb_top - 0.2]) cube([6.11, 6.6, deck_z]);
}

module frame() difference() {
    union() {
        // low frame over the keys
        translate([0, 0, low_z]) linear_extrude(low_t) difference() { envelope(); caps2d(); deck_inner2d(); }
        // raised deck
        translate([0, 0, deck_z]) linear_extrude(deck_t) deck2d();
        // the deck's edge wall, from the low frame up to the deck
        translate([0, 0, low_z]) linear_extrude(deck_z - low_z) difference() { deck2d(); deck_inner2d(); }
        // posts down to the PCB for the screws' inserts
        for (h = holes) translate([h[0], h[1], pcb_top + 0.1]) cylinder(d = post_d, h = low_z - pcb_top, $fn = 32);
        // locating rim inside the walls, over the keys only
        translate([0, 0, low_z - 0.8]) linear_extrude(0.8) difference() {
            offset(delta = -0.15) cavity2d(); offset(delta = -1.15) cavity2d(); caps2d(); deck2d();
        }
    }
    for (h = holes) translate([h[0], h[1], pcb_top]) cylinder(d = insert_d, h = 3.0, $fn = 24);
    for (p = led_xy) translate([p[0], p[1], deck_z - 1]) cylinder(d = 2.2, h = 5, $fn = 24);   // LED light holes
    translate([reset_xy[0], reset_xy[1], deck_z - 1]) cylinder(d = 2.5, h = 5, $fn = 24);   // reset access
}

module tray_r()  intersection() { tray();  round_mask(); }
module frame_r() intersection() { frame(); round_mask(); }
if (part == "tray") tray_r();
else if (part == "frame") frame_r();
else {
    color("#555") tray_r();
    color("#bbb", 0.7) frame_r();
    color("green", 0.5) translate([0, 0, pcb_z]) linear_extrude(pcb_t) pcb2d();
}
