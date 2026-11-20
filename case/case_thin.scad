// Thin case for the PG1316S build (ergogen-thin/, pcb-thin/). OpenSCAD, mm, y up, same coordinates
// as the ergogen config. Outlines come from case/outlines-thin/ (ergogen-thin's DXFs).
//
//   openscad -D 'variant="left"' -D 'part="tray"'  -o stl-thin/tray_left.stl  case_thin.scad
//   openscad -D 'variant="left"' -D 'part="frame"' -o stl-thin/frame_left.stl case_thin.scad
// variant: "left" | "right" | "mono"     part: "tray" | "frame" | "assembly"
//
// Stack-up (z = 0 on the laptop's lower screen). Everything stays inside the stock keyboard's 7.8 mm.
// The top is one flat plate with the keycaps 1.7 mm proud of it (thumb keys pressed with the side of
// the thumb), plus one raised bump over the nice!nano that still stays under the key tops.
//   0.0 - 1.0  floor; 0.6 mm under the cell
//   0.6 - 4.6  403040 cell (4 x 30 x 40 mm) through a notch in the PCB's front corner
//   2.8 - 3.6  PCB (0.8 mm), on standoffs; screws from the top
//   3.6 - 7.8  PG1316S switch + cap (4.2 mm): the key tops
//   3.6 - 6.8  nice!nano, soldered flat on top as usual (components facing the PCB)
//   5.3 - 6.1  flat top plate. Other top-side parts must stay under 1.5 mm (diodes, LEDs, side switch)
//   6.9 - 7.7  bump over the nice!nano

variant = "left";
part = "assembly";
odir = "outlines-thin/";

floor_t   = 1.0;
pcb_t     = 0.8;
key_top   = 7.8;                    // = the stock keyboard's overall thickness
cap_proud = 1.7;
pcb_top   = key_top - 4.2;          // 3.6
pcb_z     = pcb_top - pcb_t;        // 2.8
plate_t   = 0.8;
top_z     = key_top - cap_proud;    // 6.1: flat top
wall_top  = top_z - plate_t;        // 5.3: tray walls, plate underside
nano_h    = 3.2;
bump_z    = pcb_top + nano_h + 0.1; // 6.9: underside of the bump over the nice!nano
bump_top  = bump_z + plate_t;       // 7.7
bump_wall = 1.2;
wall      = 2.0;
pcb_gap   = 0.5;
cx        = 131;
cy        = 18.6;

// hardware
insert_d   = 3.2;  boss_d = 5.6;                          // M2 heat-set inserts in floor standoffs
dock_mag_d = 6.2;  dock_mag_h = 1.6;  dock_skin = 0.4;    // 6 x 1.5 mm N52 discs, as the standard case
join_mag_d = 4.2;  join_mag_h = 2.1;  join_mag_z = 3.0;   // 4 x 2 mm N52 discs, 4 per face
dowel_d    = 2.1;  dowel_h    = 5.2;  dowel_z    = 2.4;   // 2 x 10 mm steel pins, inside the 5.5 mm join wall
cell_floor = 0.6;                                         // 403040 cell: 0.6 - 4.6

function mx(x) = 2 * cx - x;
holes_left  = [[-8,66],[-8,-28],[40,-24],[47.5,69],[101.3,68],[122.5,-30]];
holes_right = [for (h = holes_left) [mx(h[0]), h[1]]];
dock_left   = [[-9,71],[20,71],[40,71],[75,71],[110,71],
               [-10.5,40],[-10.5,10],
               [-10.5,-20],[46,-32.5],[110,-32.5],   // the front-left corner holds the cell
               [119,2],[96,38]];                     // the controller pocket moved one site
dock_right  = [for (p = dock_left) [mx(p[0]), p[1]]];
join_mag_y  = [-12, 8, 42, 56];
dowel_y     = [-24, 66];
link_y      = 28;

side_x   = function(x) variant == "right" ? mx(x) : variant == "mono" ? x + 18 : x;
nano_x   = side_x(113);
switch_x = variant == "mono" ? 111 : side_x(93);
reset_xy = [side_x(118.3), 33];
led_xy   = [for (y = [3, 6.5, 10]) [side_x(119.5), y]];

holes = variant == "left" ? holes_left : variant == "right" ? holes_right : concat(holes_left, holes_right);
dock  = variant == "left" ? dock_left  : variant == "right" ? dock_right  : concat(dock_left, dock_right);
env_file = str(odir, variant == "left" ? "envelope_left.dxf" : variant == "right" ? "envelope_right.dxf" : "envelope.dxf");
pcb_file = str(odir, variant == "left" ? "pcb_left.dxf" : variant == "right" ? "pcb_right.dxf" : "pcb_mono.dxf");

module envelope() import(env_file);
module pcb2d()    import(pcb_file);
module caps2d()   offset(delta = 0.5) import(str(odir, "caps.dxf"));
// battery notch in the PCB (see ergogen-thin pcb_mono): the cell drops through it onto the floor
module cell2d() {
    if (variant != "right") translate([-4.5, -35.5]) square([41, 32.5]);
    if (variant != "left")  translate([mx(36.5), -35.5]) square([41, 32.5]);
}
module cavity2d() offset(delta = pcb_gap) union() { pcb2d(); cell2d(); }
// the nice!nano on the PCB (18 x 33 mm, USB end at the back edge)
module nano2d() translate([nano_x - 9.5, 35.5]) square([19, 39.5]);

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
    // the bump over the nice!nano runs out to the back edge, rounded the same way
    intersection() {
        translate([0, 0, top_z - rt]) linear_extrude(bump_top - top_z + rt) bump2d();
        union() {
            translate([0, 0, top_z - rt]) linear_extrude(bump_top - top_z) env_inset(0);
            for (i = [0 : n - 1]) translate([0, 0, bump_top - rt + i * rt / n])
                linear_extrude(rt / n + 0.001) env_inset(fillet_inset(rt, rt - (i + 0.5) * rt / n));
        }
    }
}
// the bump's outline, kept clear of the keycap openings and the reset hole (thinner wall at those corners)
module bump2d() difference() {
    intersection() { envelope(); offset(delta = 0.3 + bump_wall) nano2d(); }
    offset(delta = 0.2) caps2d();
    translate(reset_xy) circle(d = 2.9, $fn = 24);
}

module tray() difference() {
    union() {
        linear_extrude(floor_t) envelope();
        linear_extrude(wall_top) difference() { envelope(); cavity2d(); }
        for (p = dock) translate([p[0], p[1], 0]) cylinder(d = dock_mag_d + 2.4, h = dock_skin + dock_mag_h, $fn = 32);
        for (h = holes) translate([h[0], h[1], 0]) cylinder(d = boss_d, h = pcb_z, $fn = 32);
    }
    for (h = holes) translate([h[0], h[1], floor_t - 0.4]) cylinder(d = insert_d, h = 10, $fn = 24);
    for (p = dock) translate([p[0], p[1], dock_skin]) cylinder(d = dock_mag_d, h = dock_mag_h + 0.01, $fn = 32);
    // pocket for the cell through the PCB notch
    translate([0, 0, cell_floor]) linear_extrude(floor_t) offset(delta = 0.3) cell2d();
    usb_cut();
    // side slide switch lever (top side of the PCB)
    translate([switch_x, 80, pcb_top + 0.75]) cube([6, 20, 2.0], center = true);
    if (variant != "mono") join_features();
}

// USB-C opening (nice!nano soldered flat on the PCB, mid-mount port), through the wall and the bump
module usb_cut() translate([nano_x, 80, pcb_top + 1.6]) cube([10, 20, 3.8], center = true);

module join_features() {
    s = variant == "left" ? -1 : 1;
    for (y = join_mag_y) translate([cx, y, join_mag_z]) rotate([0, s * 90, 0])
        translate([0, 0, -0.01]) cylinder(d = join_mag_d, h = join_mag_h, $fn = 32);
    for (y = dowel_y) translate([cx, y, dowel_z]) rotate([0, s * 90, 0]) {
        translate([0, 0, -0.01]) cylinder(d = dowel_d, h = dowel_h, $fn = 24);
        translate([0, 0, -0.01]) cylinder(d1 = dowel_d + 0.8, d2 = dowel_d, h = 0.4, $fn = 24);
    }
    // pogo connector slot, open at the top; the plate above is pocketed to 0.3 mm (see frame)
    translate([s < 0 ? cx - 6.1 : cx - 0.01, link_y - 3.3, pcb_top - 0.2]) cube([6.11, 6.6, top_z]);
}

module frame() difference() {
    union() {
        translate([0, 0, wall_top]) linear_extrude(plate_t) difference() { envelope(); caps2d(); }
        // the bump over the nice!nano: walls up from the plate, and its lid
        translate([0, 0, top_z - 0.01]) linear_extrude(bump_z - top_z + 0.01) difference() { bump2d(); offset(delta = 0.3) nano2d(); }
        translate([0, 0, bump_z]) linear_extrude(plate_t) bump2d();
        // locating rim inside the walls
        translate([0, 0, wall_top - 0.8]) linear_extrude(0.8) difference() {
            offset(delta = -0.15) cavity2d(); offset(delta = -1.15) cavity2d(); caps2d();
            offset(delta = 0.5) nano2d(); offset(delta = 0.5) cell2d();
            if (variant != "mono") translate([variant == "left" ? cx - 9 : cx, link_y - 4.5]) square([9, 9]);
        }
    }
    // room for the nice!nano under the bump
    translate([0, 0, wall_top - 1]) linear_extrude(bump_z - wall_top + 1) offset(delta = 0.3) nano2d();
    usb_cut();
    for (p = led_xy) translate([p[0], p[1], wall_top - 1]) cylinder(d = 2.2, h = 5, $fn = 24);   // LED light holes
    translate([reset_xy[0], reset_xy[1], wall_top - 1]) cylinder(d = 2.5, h = 5, $fn = 24);   // reset access
    // room for the pogo connector's body under the plate (2.2 mm above the PCB)
    if (variant != "mono") translate([variant == "left" ? cx - 7 : cx - 0.01, link_y - 3.5, wall_top - 1])
        cube([7.01, 7, 1 + top_z - wall_top - 0.3]);
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
