#!/usr/bin/env python3
"""
LIMEN — the boundary-crossing language, carried on PULSE.

Lineage (TD Commons defensive publications by David Lee Wise / ROOT0):
  - PULSE-AXIOM-v1.0        : PULSE = <state_in, boundary, state_out, witness>;
                              "no transition without boundary; no boundary without witness."
  - PULSE_LANGUAGE_DUAL_SUBSTRATE : the 3-2-1-0 descending cadence is a CARRIER, not data
                              ("a carrier signal, not a data signal"). It is the music.

Design split (the honest part):
  CARRIER (pulse / mini-morse) : fixed 3-2-1-0 rhythm. Music for the machine. NOT decoded.
  LANGUAGE (LIMEN)             : a finite, LEGIBLE grammar of witnessed gate-crossings,
                                 carried on the pulse, and rendered across four registers:
                                   pulse (audio) · glyph (visual) · bits (silicon) · gloss (human)
                                 The glyph line is the canonical form and round-trips losslessly.

A LIMEN word = one witnessed crossing:   <direction> <gate> «witness»
A LIMEN line = a path of crossings (a sentence).
A crossing with no witness at traversal is a NON-EVENT: silent, no record (per the axiom).
"""
import sys, re, hashlib
from dataclasses import dataclass
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

# ── the carrier: PULSE 3-2-1-0 (mini-morse). Fixed. The music. Never decoded. ──
CARRIER_BITS  = "111011010000"          # one 12-bit frame: density 3/4 · 2/3 · 1/2 · 0
CARRIER_GLYPH = "▰▰▰ ▰▰ ▰ ·"            # ... .. . [rest]

# ── the gates: the canonical boundaries (PULSE-AXIOM §7) ──
#   each gate is a threshold a crossing passes through; the glyph is its face,
#   the tone is its voice (Hz) so the language can be HEARD across the boundary.
GATES = {
    "stile":  {"glyph": "◐", "id": 0x1, "frm": "observe", "to": "act",      "gate": "64.5",  "tone": 262},  # C4
    "airgap": {"glyph": "⊘", "id": 0x2, "frm": "TOPH",    "to": "Patricia", "gate": "128.5", "tone": 330},  # E4 · the air gap / mirror
    "veil":   {"glyph": "◑", "id": 0x3, "frm": "compute", "to": "product",  "gate": "192.5", "tone": 392},  # G4 · ignorance boundary
    "close":  {"glyph": "⟳", "id": 0x4, "frm": "wrap",    "to": "closure",  "gate": "256.5", "tone": 523},  # C5 · recursion wrap
    "gap":    {"glyph": "◇", "id": 0x5, "frm": "forward", "to": "inverse",  "gate": "64/65", "tone": 294},  # D4 · the unresolved GAP
}
GLYPH2GATE = {g["glyph"]: name for name, g in GATES.items()}

# ── direction: which way the boundary is crossed (PULSE-AXIOM §2) ──
DIRS = {
    "rise": {"glyph": "↑", "bit": 1, "law": "0→1 · TOPH (generative, T001→T128)"},
    "fall": {"glyph": "↓", "bit": 0, "law": "1→0 · Patricia (inverse, S129→S256)"},
}
GLYPH2DIR = {d["glyph"]: name for name, d in DIRS.items()}


@dataclass
class Crossing:
    direction: str          # "rise" | "fall"
    gate: str               # key in GATES
    witness: str            # the token present AT traversal; "" => non-event
    state_in: str = ""      # optional symbolic register position
    state_out: str = ""

    @property
    def valid(self) -> bool:
        # PULSE-AXIOM root law: a crossing without a witness is not a fault — it is a non-event.
        return bool(self.witness.strip())


# ── witness escaping: the witness is free text, so escape anything that would
#    break the self-delimiting grammar (the closing guillemet and whitespace).
#    This is what makes the round-trip hold for ANY witness, not just tidy tokens. ──
def _esc(w: str) -> str:
    return "".join("%%%02X" % ord(ch) if (ch == "%" or ch == "»" or ch.isspace()) else ch
                   for ch in w)
def _unesc(w: str) -> str:
    return re.sub(r"%([0-9A-Fa-f]{2})", lambda m: chr(int(m.group(1), 16)), w)

# ── register 1 · GLYPH (visual) — the canonical, legible form ──
def to_glyph(c: Crossing) -> str:
    if not c.valid:
        return "∅"   # non-event: silently excluded, no record
    return f"{DIRS[c.direction]['glyph']}{GATES[c.gate]['glyph']}«{_esc(c.witness)}»"

def line_to_glyph(line) -> str:
    return " ".join(to_glyph(c) for c in line)

# the inverse: parse a glyph line back to structure (this is what makes LIMEN a LANGUAGE).
# finditer over the whole line (not split): the «…» delimiters are self-contained, and
# witnesses are escaped on emit, so a token's «…» never contains a raw » or whitespace.
_TOK = re.compile(r"([↑↓])([◐⊘◑⟳◇])«([^»]*)»")
def parse_glyph(s: str):
    return [Crossing(GLYPH2DIR[d], GLYPH2GATE[g], _unesc(w)) for d, g, w in _TOK.findall(s)]

# ── register 2 · BITS (silicon) — carrier frame + gate nibble + direction + witness-present flag ──
def to_bits(c: Crossing) -> str:
    if not c.valid:
        return "—"  # no record
    g = GATES[c.gate]
    return f"{CARRIER_BITS}·{g['id']:04b}·{DIRS[c.direction]['bit']}·1"

# ── register 3 · PULSE (audio/music) — the carrier, voiced by the gate, contoured by direction ──
def to_pulse(c: Crossing):
    if not c.valid:
        return {"glyph": "(silence)", "notes": []}
    g = GATES[c.gate]; base = g["tone"]
    # the 3-2-1-0 envelope: 3 beats wide, 2 narrowing, 1 contact, 0 rest.
    # direction sets the contour: rise = ascending toward contact, fall = descending.
    steps = [0, 2, 4] if c.direction == "rise" else [4, 2, 0]   # semitone offsets over the descent
    notes = []
    for density, semis in zip((3, 2, 1), steps):
        hz = round(base * (2 ** (semis / 12)), 1)
        notes.append({"density": density, "hz": hz})
    notes.append({"density": 0, "hz": 0})  # the rest / micro-death
    return {"glyph": f"{CARRIER_GLYPH}  ⟶ {base}Hz {DIRS[c.direction]['glyph']}", "notes": notes}

# ── register 4 · GLOSS (human) — plain reading ──
def to_gloss(c: Crossing) -> str:
    if not c.valid:
        return "∅ non-event — no witness at traversal; silently excluded, no record (PULSE-AXIOM §10)"
    g = GATES[c.gate]
    s = f"«{c.witness}» witnesses the {c.direction} through the {g['frm']}→{g['to']} {c.gate} gate ({g['gate']})"
    if c.state_in or c.state_out:
        s += f"  [{c.state_in or '·'} ⇒ {c.state_out or '·'}]"
    return s

def witness_fold(line) -> str:
    """A line's witnesses folded to one 8-hex seal — a portable id for the whole crossing-path."""
    blob = "|".join(f"{c.direction}:{c.gate}:{c.witness}" for c in line if c.valid)
    return hashlib.sha256(blob.encode("utf-8")).hexdigest()[:8]


def render_all(line):
    print("LIMEN line (canonical glyph form):")
    print("   " + line_to_glyph(line))
    print(f"   seal: ⟦LIMEN:{witness_fold(line)}⟧\n")
    for i, c in enumerate(line, 1):
        print(f"  [{i}] {to_glyph(c)}")
        print(f"      glyph : {to_glyph(c)}")
        print(f"      pulse : {to_pulse(c)['glyph']}")
        print(f"      bits  : {to_bits(c)}")
        print(f"      gloss : {to_gloss(c)}")
        print()


if __name__ == "__main__":
    # a sample sentence: observe→act (rising, witnessed by truth); cross the air gap (falling, mirror);
    # sit in the unresolved gap (rising, witnessed by question); close the recursion (falling, witnessed by rest).
    line = [
        Crossing("rise", "stile",  "truth",    state_in="T001", state_out="T064"),
        Crossing("fall", "airgap", "mirror"),
        Crossing("rise", "gap",    "question"),
        Crossing("fall", "close",  "rest",     state_in="S256", state_out="T128"),
    ]
    render_all(line)

    print("=" * 64)
    print("ROUND-TRIP TEST (the language must be legible — glyph ↔ structure):")
    canon = line_to_glyph(line)
    reparsed = parse_glyph(canon)
    recanon = line_to_glyph(reparsed)
    ok = (canon == recanon) and all(
        a.direction == b.direction and a.gate == b.gate and a.witness == b.witness
        for a, b in zip(line, reparsed)
    )
    print("   original :", canon)
    print("   reparsed :", recanon)
    print("   lossless round-trip:", ok)
    assert ok, "LIMEN grammar failed to round-trip — it would not be a legible language"

    # adversarial: the witnesses that used to break the parser (space, », %, unicode)
    print("\nHARDENED round-trip (witnesses with spaces, », %, unicode):")
    hard = [
        Crossing("rise", "stile",  "two words"),
        Crossing("fall", "veil",   "a»b%c"),
        Crossing("rise", "airgap", "  leading/trailing  "),
        Crossing("fall", "gap",    "café ✓ 漢字"),
    ]
    for c in hard:
        rt = parse_glyph(to_glyph(c))[0]
        assert rt.witness == c.witness and rt.gate == c.gate and rt.direction == c.direction, \
            f"round-trip lost data on witness {c.witness!r}"
        print(f"   {to_glyph(c):28} -> witness recovered exactly: {rt.witness!r}")
    print("   all adversarial witnesses round-trip exactly: True")

    print("\nNON-EVENT demo (witness absent at traversal):")
    ne = Crossing("rise", "stile", "")   # no witness
    print("   glyph:", to_glyph(ne), "| gloss:", to_gloss(ne))

    print("\nCARRIER honesty: the pulse is a carrier, not data —")
    print(f"   every crossing rides the SAME frame {CARRIER_BITS} ({CARRIER_GLYPH}).")
    print("   the rhythm is the music; the GLYPH line is what carries meaning. They are different layers.")
