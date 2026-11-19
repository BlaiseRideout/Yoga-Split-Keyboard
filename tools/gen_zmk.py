#!/usr/bin/env python3
"""Generate the ZMK shields (split + monolithic) from ergogen's points.yaml.

usage: python3 tools/gen_zmk.py            (reads tools/points.yaml, writes config/boards/shields/)
Refresh points.yaml with:  ergogen ergogen -o build/ergogen -d   then copy build/ergogen/points/points.yaml
"""
import os, math, yaml

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SH = os.path.join(ROOT, 'config', 'boards', 'shields')
pts = yaml.safe_load(open(os.path.join(HERE, 'points.yaml')))

U = 18.0  # mm per key unit for the physical layout (Choc spacing)

# ---- ordering of keys, as seen from above, left to right, top to bottom ----
ROWS = ['num', 'top', 'home', 'bottom']
COLS = ['outer', 'pinky', 'ring', 'middle', 'index', 'inner']
THUMBS = ['tucky', 'home', 'reachy']
order = []  # (point name, split row, split col, mono row, mono col)
for ri, r in enumerate(ROWS):
    for ci, c in enumerate(COLS):
        order.append(f'matrix_{c}_{r}')
    for ci, c in reversed(list(enumerate(COLS))):
        order.append(f'mirror_matrix_{c}_{r}')
order += [f'thumb_{t}_one' for t in THUMBS] + [f'mirror_thumb_{t}_one' for t in reversed(THUMBS)]

def split_rc(name):
    m = pts[name]['meta']
    row, col = m['row_i'], m['col_i']
    if m.get('mirrored'):
        col = 6 + (5 - col)   # right half: col-gpios listed inner->outer, col-offset 6
    return row, col

def mono_rc(name):
    m = pts[name]['meta']
    return int(m['mono_row'][2:]), int(m['mono_col'][2:])

def transform(fn, rows, cols, label):
    lines, cur = [], []
    for i, n in enumerate(order):
        r, c = fn(n)
        cur.append(f'RC({r},{c})')
        if len(cur) == 12 or i == len(order) - 1:
            lines.append(' '.join(cur)); cur = []
    body = '\n'.join('            ' + l for l in lines)
    return f'''    {label}: {label} {{
        compatible = "zmk,matrix-transform";
        columns = <{cols}>;
        rows = <{rows}>;
        map = <
{body}
        >;
    }};'''

def physical(label, tname):
    xs = [pts[n]['x'] for n in order]; ys = [pts[n]['y'] for n in order]
    x0, y1 = min(xs) - 9, max(ys) + 9
    keys = []
    for n in order:
        p = pts[n]
        cxu, cyu = (p['x'] - x0) / U, (y1 - p['y']) / U
        x, y = cxu - 0.5, cyu - 0.5
        r = -p['r']
        def n(v):  # devicetree cells: negative numbers must be parenthesised
            v = round(v * 100)
            return f'{v:>7}' if v >= 0 else f'{f"({v})":>7}'
        keys.append(f'<&key_physical_attrs 100 100 {n(x)} {n(y)} {n(r)} {n(cxu)} {n(cyu)}>')
    body = '\n            , '.join(keys)
    return f'''    {label}: {label} {{
        compatible = "zmk,physical-layout";
        display-name = "Default";
        transform = <&{tname}>;
        keys  //                     w   h     x     y   rot    rx    ry
            = {body}
            ;
    }};'''

PIN = {  # nets -> pro_micro pin numbers (must match ergogen/config.yaml)
    'R': [4, 5, 6, 7, 8], 'C': [21, 20, 19, 18, 15, 14],
    'MR': [4, 5, 6, 7, 8, 9], 'MC': [21, 20, 19, 18, 15, 14, 16, 10, 0],
}

def gpios(pins, flags):
    return '\n            '.join(('= ' if i == 0 else ', ') + f'<&pro_micro {p} {flags}>' for i, p in enumerate(pins)) + '\n            ;'

ROWF = '(GPIO_ACTIVE_HIGH | GPIO_PULL_DOWN)'
LIC = '/*\n * SPDX-License-Identifier: MIT\n */\n'

# ------------------------------------------------------------------ keymap
L = {}
L['base'] = [
 'ESC','N1','N2','N3','N4','N5',            'N6','N7','N8','N9','N0','BSPC',
 'TAB','Q','W','E','R','T',                  'Y','U','I','O','P','BSLH',
 'LCTRL','A','S','D','F','G',                'H','J','K','L','SEMI','SQT',
 'LSHFT','Z','X','C','V','B',                'N','M','COMMA','DOT','FSLH','RSHFT',
 'LGUI','&mo 1','SPACE',                     'RET','&mo 2','RALT']
L['lower'] = [
 'GRAVE','F1','F2','F3','F4','F5',           'F6','F7','F8','F9','F10','DEL',
 '&trans','F11','F12','&trans','&trans','&trans',  'PG_UP','HOME','UP','END','INS','&trans',
 '&trans','LGUI','LALT','LCTRL','LSHFT','&trans',  'PG_DN','LEFT','DOWN','RIGHT','PSCRN','&trans',
 '&trans','&trans','&trans','&trans','&trans','&trans',  'C_MUTE','C_VOL_DN','C_VOL_UP','C_PREV','C_PP','C_NEXT',
 '&trans','&trans','&trans',                 '&trans','&trans','&trans']
L['raise'] = [
 'TILDE','EXCL','AT','HASH','DLLR','PRCNT',  'CARET','AMPS','STAR','LPAR','RPAR','&trans',
 '&trans','N1','N2','N3','N4','N5',          'N6','N7','N8','N9','N0','PIPE',
 '&trans','&trans','&trans','&trans','&trans','&trans',  'MINUS','EQUAL','LBKT','RBKT','LBRC','RBRC',
 '&trans','&trans','&trans','&trans','&trans','&trans',  'UNDER','PLUS','&trans','&trans','QMARK','&trans',
 '&trans','&trans','&trans',                 '&trans','&trans','&trans']
L['adjust'] = [
 '&bt BT_CLR','&bt BT_SEL 0','&bt BT_SEL 1','&bt BT_SEL 2','&bt BT_SEL 3','&bt BT_SEL 4',  '&none','&none','&none','&none','&none','&bootloader',
 '&out OUT_BLE','&none','&none','&none','&none','&none',  '&none','&none','&none','&none','&none','&sys_reset',
 '&out OUT_USB','&none','&none','&none','&none','&none',  '&none','&none','&none','&none','&none','&none',
 '&none','&none','&none','&none','&none','&none',  '&none','&none','&none','&none','&none','&none',
 '&trans','&trans','&trans',                 '&trans','&trans','&trans']

def binding(b):
    return b if b.startswith('&') else f'&kp {b}'

def keymap_text(name):
    out = [LIC, '#include <behaviors.dtsi>', '#include <dt-bindings/zmk/keys.h>',
           '#include <dt-bindings/zmk/bt.h>', '#include <dt-bindings/zmk/outputs.h>', '',
           '/ {', '    conditional_layers {', '        compatible = "zmk,conditional-layers";',
           '        adjust { if-layers = <1 2>; then-layer = <3>; };', '    };', '',
           '    keymap {', '        compatible = "zmk,keymap";']
    for i, (ln, keys) in enumerate(L.items()):
        assert len(keys) == 54, (ln, len(keys))
        rows = [keys[k:k+12] for k in range(0, 48, 12)] + [keys[48:]]
        out.append(f'        {ln}_layer {{')
        out.append(f'            display-name = "{ln.capitalize()}";')
        out.append('            bindings = <')
        for r in rows[:4]:
            l = '  '.join(f'{binding(b):<14}' for b in r[:6]); rr = '  '.join(f'{binding(b):<14}' for b in r[6:])
            out.append(f'                {l}    {rr}')
        t = rows[4]
        out.append(' ' * 64 + '  '.join(f'{binding(b):<14}' for b in t[:3]) + '    ' + '  '.join(f'{binding(b):<14}' for b in t[3:]))
        out.append('            >;')
        out.append('        };')
    out += ['    };', '};', '']
    return '\n'.join(out)

def write(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w') as f:
        f.write(text.rstrip() + '\n')

# ------------------------------------------------------------------ split shield
d = os.path.join(SH, 'yoga_split')
write(f'{d}/Kconfig.shield', '''config SHIELD_YOGA_SPLIT_LEFT
    def_bool $(shields_list_contains,yoga_split_left)

config SHIELD_YOGA_SPLIT_RIGHT
    def_bool $(shields_list_contains,yoga_split_right)
''')
write(f'{d}/Kconfig.defconfig', '''if SHIELD_YOGA_SPLIT_LEFT

config ZMK_KEYBOARD_NAME
    default "Yoga Split"

config ZMK_SPLIT_ROLE_CENTRAL
    default y

endif

if SHIELD_YOGA_SPLIT_LEFT || SHIELD_YOGA_SPLIT_RIGHT

config ZMK_SPLIT
    default y

endif
''')
write(f'{d}/yoga_split.dtsi', f'''{LIC}
#include <dt-bindings/zmk/matrix_transform.h>
#include <physical_layouts.dtsi>

/ {{
    chosen {{
        zmk,kscan = &kscan0;
        zmk,physical-layout = &yoga_split_layout;
    }};

{transform(split_rc, 5, 12, 'default_transform')}

{physical('yoga_split_layout', 'default_transform')}

    kscan0: kscan {{
        compatible = "zmk,kscan-gpio-matrix";
        wakeup-source;
        diode-direction = "col2row";
        row-gpios
            {gpios(PIN['R'], ROWF)}
    }};
}};
''')
write(f'{d}/yoga_split_left.overlay', f'''{LIC}
#include "yoga_split.dtsi"

&kscan0 {{
    col-gpios
        {gpios(PIN['C'], 'GPIO_ACTIVE_HIGH')}
}};
''')
write(f'{d}/yoga_split_right.overlay', f'''{LIC}
#include "yoga_split.dtsi"

&default_transform {{
    col-offset = <6>;
}};

&kscan0 {{
    col-gpios   // inner -> outer, so matrix columns read left to right across the whole board
        {gpios(list(reversed(PIN['C'])), 'GPIO_ACTIVE_HIGH')}
}};
''')
write(f'{d}/yoga_split.conf', '''# nice!view
CONFIG_ZMK_DISPLAY=y
# deep sleep after 15 min idle; wake on any key
CONFIG_ZMK_SLEEP=y
CONFIG_ZMK_IDLE_SLEEP_TIMEOUT=900000
''')
write(f'{d}/yoga_split.keymap', keymap_text('split'))
write(f'{d}/yoga_split.zmk.yml', '''file_format: "1"
id: yoga_split
name: Yoga Split
type: shield
url: https://github.com/BlaiseRideout/yoga-split-keyboard
requires: [pro_micro]
features: [keys, display, studio]
siblings: [yoga_split_left, yoga_split_right]
''')

# ------------------------------------------------------------------ monolithic shield
d = os.path.join(SH, 'yoga_mono')
write(f'{d}/Kconfig.shield', '''config SHIELD_YOGA_MONO
    def_bool $(shields_list_contains,yoga_mono)
''')
write(f'{d}/Kconfig.defconfig', '''if SHIELD_YOGA_MONO

config ZMK_KEYBOARD_NAME
    default "Yoga Mono"

endif
''')
write(f'{d}/yoga_mono.overlay', f'''{LIC}
#include <dt-bindings/zmk/matrix_transform.h>
#include <physical_layouts.dtsi>

/ {{
    chosen {{
        zmk,kscan = &kscan0;
        zmk,physical-layout = &yoga_mono_layout;
    }};

    // 54 keys packed into a 6 x 9 matrix (see docs/matrix.md)
{transform(mono_rc, 6, 9, 'default_transform')}

{physical('yoga_mono_layout', 'default_transform')}

    kscan0: kscan {{
        compatible = "zmk,kscan-gpio-matrix";
        wakeup-source;
        diode-direction = "col2row";
        row-gpios
            {gpios(PIN['MR'], ROWF)}
        col-gpios
            {gpios(PIN['MC'], 'GPIO_ACTIVE_HIGH')}
    }};
}};
''')
write(f'{d}/yoga_mono.conf', '''CONFIG_ZMK_DISPLAY=y
CONFIG_ZMK_SLEEP=y
CONFIG_ZMK_IDLE_SLEEP_TIMEOUT=900000
''')
write(f'{d}/yoga_mono.keymap', keymap_text('mono'))
write(f'{d}/yoga_mono.zmk.yml', '''file_format: "1"
id: yoga_mono
name: Yoga Mono
type: shield
url: https://github.com/BlaiseRideout/yoga-split-keyboard
requires: [pro_micro]
features: [keys, display, studio]
''')

# sanity: every matrix position used exactly once
for fn, nm in ((split_rc, 'split'), (mono_rc, 'mono')):
    rc = [fn(n) for n in order]
    assert len(set(rc)) == 54, nm
print('ok: wrote', SH)
