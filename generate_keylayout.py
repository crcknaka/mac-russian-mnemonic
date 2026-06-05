#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generate a macOS .keylayout file that reproduces the Windows
"Russian - Mnemonic" keyboard layout (kbdrum.dll) 1-to-1,
including its dead keys (y, j, s, c).

Source of truth: official KBDRUM mapping dumped from kbdlayout.info
(see kbdrum.klc in this repo).

Output: "Russian - Mnemonic.keylayout"
"""

LAYOUT_NAME = "Russian – Mnemonic"
LAYOUT_ID = "-19419"   # arbitrary unique negative id

def u(c):
    """char -> XML numeric entity (safe for all chars incl. & < > \")"""
    return "&#x%04X;" % ord(c)

# ---------------------------------------------------------------------------
# macOS ANSI virtual key codes
A,S,D,F,H,G,Z,X,C,V,B,Q,W,E,R,Y,T = 0,1,2,3,4,5,6,7,8,9,11,12,13,14,15,16,17
U,I,O,P,L,J,K,N,M = 32,34,31,35,37,38,40,45,46
K1,K2,K3,K4,K5,K6,K7,K8,K9,K0 = 18,19,20,21,23,22,26,28,25,29
MINUS,EQUAL,LBR,RBR,SEMI,QUOTE,BACKTICK,BSLASH,COMMA,DOT,SLASH = 27,24,33,30,41,39,50,42,43,47,44
ISO_BSLASH = 10
SPACE = 49

# ---------------------------------------------------------------------------
# Plain letter keys: code -> lowercase char (uppercase via .upper())
plain_letters = {
    D:'д', F:'ф', G:'г', Z:'з', X:'ж', V:'в', B:'б', Q:'я', W:'ш',
    R:'р', T:'т', I:'и', P:'п', L:'л', K:'к', N:'н', M:'м',
}

# US-QWERTY characters per physical key. Used for the Command/Control layer so
# that shortcuts (⌘C ⌘V ⌘A ⌘Z ...) resolve to their Latin letters — exactly what
# Apple's own non-Latin layouts and known-good layouts do.
us_qwerty = {
    A:'a', S:'s', D:'d', F:'f', H:'h', G:'g', Z:'z', X:'x', C:'c', V:'v',
    B:'b', Q:'q', W:'w', E:'e', R:'r', Y:'y', T:'t', U:'u', I:'i', O:'o',
    P:'p', L:'l', J:'j', K:'k', N:'n', M:'m',
    K1:'1', K2:'2', K3:'3', K4:'4', K5:'5', K6:'6', K7:'7', K8:'8', K9:'9', K0:'0',
    MINUS:'-', EQUAL:'=', LBR:'[', RBR:']', SEMI:';', QUOTE:"'", BACKTICK:'`',
    BSLASH:'\\', ISO_BSLASH:'\\', COMMA:',', DOT:'.', SLASH:'/', SPACE:' ',
}

# Standard non-printing keys (Backspace, Tab, Return, arrows, ...).
# These MUST be present or Chromium/Electron apps (most messengers) fail to
# generate the key events — e.g. Backspace stops working. Same in all layers.
# Values match Apple's own .keylayout convention.
system_keys = {
    36:0x0D,   # Return
    48:0x09,   # Tab
    51:0x08,   # Delete (Backspace)
    53:0x1B,   # Escape
    71:0x1B,   # Clear (numpad)
    76:0x03,   # Enter (numpad)
    114:0x05,  # Help
    115:0x01,  # Home
    116:0x0B,  # Page Up
    117:0x7F,  # Forward Delete
    119:0x04,  # End
    121:0x0C,  # Page Down
    123:0x1C,  # Left arrow
    124:0x1D,  # Right arrow
    125:0x1F,  # Down arrow
    126:0x1E,  # Up arrow
    # Function keys -> 0x10 (Ukelele default; keeps the layout "complete")
    122:0x10, 120:0x10, 99:0x10, 118:0x10, 96:0x10, 97:0x10, 98:0x10,
    100:0x10, 101:0x10, 109:0x10, 103:0x10, 111:0x10, 105:0x10, 107:0x10,
    113:0x10, 106:0x10, 64:0x10, 79:0x10, 80:0x10, 90:0x10,
}

# Symbol / digit keys: code -> (base, shift, caps_follows_shift)
symbols = {
    K1:('1','!',False), K2:('2','"',False), K3:('3','№',False), K4:('4',';',False),
    K5:('5','%',False), K6:('6',':',False), K7:('7','?',False), K8:('8','*',False),
    K9:('9','(',False), K0:('0',')',False),
    MINUS:('-','_',False), EQUAL:('=','+',False),
    LBR:('[','{',False), RBR:(']','}',False),
    SEMI:(';',':',False),
    QUOTE:('ь','Ь',True),        # soft sign (caps-affected, Cap=1)
    BACKTICK:('ъ','Ъ',False),    # hard sign (NOT caps-affected, Cap=0)
    BSLASH:('\\','/',False), ISO_BSLASH:('\\','/',False),
    COMMA:(',','<',False), DOT:('.','>',False), SLASH:('/','?',False),
}

# ---------------------------------------------------------------------------
# Dead-key states. Each state has a terminator char + arg->output table.
# States: yeru/yeruCap (y), shi/shiCap (j), es/esCap (s), tse/tseCap (c)
terminators = {
    'yeru':'ы','yeruCap':'Ы','shi':'й','shiCap':'Й',
    'es':'с','esCap':'С','tse':'ц','tseCap':'Ц',
}

# Argument keys and their per-state outputs.
# Each entry: code -> { 'low': {state:out,...}, 'up': {state:out,...} }
# 'none' value may be ('out', ch) or ('dead', state)
arg_keys = {
    A: {'low': {'none':('out','а'),'yeru':'я','yeruCap':'Я','shi':'я','shiCap':'Я'},
        'up':  {'none':('out','А'),'yeruCap':'Я','shiCap':'Я'}},
    E: {'low': {'none':('out','е'),'yeru':'э','yeruCap':'Э','shi':'э','shiCap':'Э'},
        'up':  {'none':('out','Е'),'yeruCap':'Э','shiCap':'Э'}},
    U: {'low': {'none':('out','у'),'yeru':'ю','yeruCap':'Ю','shi':'ю','shiCap':'Ю'},
        'up':  {'none':('out','У'),'yeruCap':'Ю','shiCap':'Ю'}},
    O: {'low': {'none':('out','о'),'yeru':'ё','yeruCap':'Ё','shi':'ё','shiCap':'Ё'},
        'up':  {'none':('out','О'),'yeruCap':'Ё','shiCap':'Ё'}},
    H: {'low': {'none':('out','х'),'es':'ш','esCap':'Ш','tse':'ч','tseCap':'Ч'},
        'up':  {'none':('out','Х'),'esCap':'Ш','tseCap':'Ч'}},
    C: {'low': {'none':('dead','tse'),'es':'щ','esCap':'Щ'},
        'up':  {'none':('dead','tseCap'),'esCap':'Щ'}},
}

# Pure dead keys (only enter a state)
dead_keys = {
    Y: ('yeru','yeruCap'),
    J: ('shi','shiCap'),
    S: ('es','esCap'),
}

# Space: consumes the dead state and emits its base letter (matches Windows)
space_states = {
    'none':('out',' '),
    'yeru':'ы','yeruCap':'Ы','shi':'й','shiCap':'Й',
    'es':'с','esCap':'С','tse':'ц','tseCap':'Ц',
}

# ---------------------------------------------------------------------------
# Build actions
actions = {}   # id -> list of (state, kind, value)  kind in {'out','dead'}

def state_map_to_action(aid, smap):
    entries = []
    for st, val in smap.items():
        if isinstance(val, tuple):
            kind, v = val
            entries.append((st, kind, v))
        else:
            entries.append((st, 'out', val))
    actions[aid] = entries

# arg keys -> two actions each (low/up)
for code, spec in arg_keys.items():
    state_map_to_action('k%d_l' % code, spec['low'])
    state_map_to_action('k%d_u' % code, spec['up'])

# pure dead keys -> low/up actions
for code, (st_lo, st_hi) in dead_keys.items():
    state_map_to_action('k%d_l' % code, {'none':('dead',st_lo)})
    state_map_to_action('k%d_u' % code, {'none':('dead',st_hi)})

# space
state_map_to_action('spc', space_states)

action_keys = set(arg_keys) | set(dead_keys) | {SPACE}

# ---------------------------------------------------------------------------
# Resolve the cell for a (code, variant) where variant in 'base','shift','caps'
def cell(code, variant):
    """return ('action', id) or ('output', char) or ('output_cp', codepoint)"""
    # non-printing system keys (same in every layer)
    if code in system_keys:
        return ('output_cp', system_keys[code])
    # Command/Control layer: plain Latin so shortcuts work, no dead keys
    if variant == 'latin':
        return ('output', us_qwerty[code])
    # space
    if code == SPACE:
        return ('action', 'spc')
    # action keys (args + dead)
    if code in action_keys:
        use_up = (variant == 'shift') or (variant == 'caps')
        suffix = '_u' if use_up else '_l'
        return ('action', 'k%d%s' % (code, suffix))
    # plain letters (caps follows shift)
    if code in plain_letters:
        lo = plain_letters[code]
        up = lo.upper()
        ch = up if variant in ('shift','caps') else lo
        return ('output', ch)
    # symbols
    if code in symbols:
        base, shift, caps_is_shift = symbols[code]
        if variant == 'base':
            ch = base
        elif variant == 'shift':
            ch = shift
        else:  # caps
            ch = shift if caps_is_shift else base
        return ('output', ch)
    return None

# ---------------------------------------------------------------------------
# Emit XML
all_codes = sorted(set(plain_letters) | set(symbols) | set(action_keys)
                   | set(system_keys) | {SPACE})

def keymap_xml(variant):
    lines = []
    for code in all_codes:
        kind, val = cell(code, variant)
        if kind == 'action':
            lines.append('      <key code="%d" action="%s"/>' % (code, val))
        elif kind == 'output_cp':
            lines.append('      <key code="%d" output="&#x%04X;"/>' % (code, val))
        else:
            lines.append('      <key code="%d" output="%s"/>' % (code, u(val)))
    return "\n".join(lines)

def actions_xml():
    lines = ['    <actions>']
    for aid in sorted(actions):
        lines.append('      <action id="%s">' % aid)
        for st, kind, v in actions[aid]:
            if kind == 'dead':
                lines.append('        <when state="%s" next="%s"/>' % (st, v))
            else:
                lines.append('        <when state="%s" output="%s"/>' % (st, u(v)))
        lines.append('      </action>')
    lines.append('    </actions>')
    return "\n".join(lines)

def terminators_xml():
    lines = ['    <terminators>']
    for st in sorted(terminators):
        lines.append('      <when state="%s" output="%s"/>' % (st, u(terminators[st])))
    lines.append('    </terminators>')
    return "\n".join(lines)

xml = f'''<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE keyboard SYSTEM "file://localhost/System/Library/DTDs/KeyboardLayout.dtd">
<!-- Russian Mnemonic layout for macOS. Reproduces Windows kbdrum.dll 1:1. -->
<keyboard group="0" id="{LAYOUT_ID}" name="{LAYOUT_NAME}" maxout="2">
  <layouts>
    <layout first="0" last="17" mapSet="ANSI" modifiers="commonModifiers"/>
    <layout first="18" last="18" mapSet="ANSI" modifiers="commonModifiers"/>
    <layout first="21" last="23" mapSet="ANSI" modifiers="commonModifiers"/>
    <layout first="30" last="30" mapSet="ANSI" modifiers="commonModifiers"/>
    <layout first="194" last="194" mapSet="ANSI" modifiers="commonModifiers"/>
    <layout first="195" last="195" mapSet="ANSI" modifiers="commonModifiers"/>
  </layouts>
  <modifierMap id="commonModifiers" defaultIndex="0">
    <keyMapSelect mapIndex="0"><modifier keys=""/></keyMapSelect>
    <keyMapSelect mapIndex="1"><modifier keys="anyShift caps?"/></keyMapSelect>
    <keyMapSelect mapIndex="2"><modifier keys="caps"/></keyMapSelect>
    <keyMapSelect mapIndex="3">
      <modifier keys="command anyShift? anyOption? anyControl? caps?"/>
      <modifier keys="anyControl command? anyShift? anyOption? caps?"/>
    </keyMapSelect>
  </modifierMap>
  <keyMapSet id="ANSI">
    <keyMap index="0">
{keymap_xml("base")}
    </keyMap>
    <keyMap index="1">
{keymap_xml("shift")}
    </keyMap>
    <keyMap index="2">
{keymap_xml("caps")}
    </keyMap>
    <keyMap index="3">
{keymap_xml("latin")}
    </keyMap>
  </keyMapSet>
{actions_xml()}
{terminators_xml()}
</keyboard>
'''

import io, sys
with io.open(LAYOUT_NAME + ".keylayout", "w", encoding="utf-8") as f:
    f.write(xml)
print("Wrote %s.keylayout (%d bytes)" % (LAYOUT_NAME, len(xml)))
