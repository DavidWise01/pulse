#!/usr/bin/env python3
"""
LIMEN two-agent exchange — the reference protocol (deterministic, testable).

Agent A speaks a LIMEN line. It crosses the boundary on two channels:
  · VOICE  (acoustic) — per word, three phase-frequencies. Carries GATE + DIRECTION.
  · GLYPH  (text)     — the canonical glyph line. Carries the WITNESS (and everything).

Agent B receives:
  · hears the VOICE  -> recovers direction (contour) + gate (nearest gate tone)
  · reads the GLYPH  -> recovers the witness
  · reconstructs each crossing, and CROSS-CHECKS: the gate+direction it heard must
    match the gate+direction it read. The voice is a checksum on the glyph.

This module proves the protocol logic with no audio — exchange.html does the live,
genuinely-acoustic version (B listens to A's tones via a Web Audio FFT).
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from limen import GATES, DIRS, Crossing, to_glyph, parse_glyph, to_gloss
try: sys.stdout.reconfigure(encoding="utf-8")
except Exception: pass

GATE_TONES = {name: g["tone"] for name, g in GATES.items()}

# ── AGENT A · encode a crossing to the wire ──
def voice_of(c: Crossing):
    """The three phase-frequencies A emits for one crossing (the 3-2-1 of the carrier,
    pitched at the gate's tone, contoured by direction). This is what B will hear."""
    base = GATES[c.gate]["tone"]
    semis = [0, 2, 4] if c.direction == "rise" else [4, 2, 0]   # rise ascends, fall descends
    return [round(base * (2 ** (s / 12)), 2) for s in semis]

def transmit(line):
    """A puts the line on the wire: a glyph channel (text) + a voice channel (freqs/word)."""
    return {"glyph": " ".join(to_glyph(c) for c in line),
            "voice": [voice_of(c) for c in line]}

# ── AGENT B · decode the wire ──
def hear(freqs):
    """B recovers (direction, gate) from three heard phase-frequencies — by contour and
    nearest-gate-tone. This is the genuinely decodable part of the audio."""
    f1, f3 = freqs[0], freqs[-1]
    direction = "rise" if f1 < f3 else "fall"
    base = f1 if direction == "rise" else f3
    gate = min(GATE_TONES, key=lambda n: abs(GATE_TONES[n] - base))
    return direction, gate, base

def receive(wire):
    """B reconstructs the line: witness from glyph, gate+direction confirmed by voice."""
    read = parse_glyph(wire["glyph"])          # witness (+ gate/dir) from the text channel
    heard = [hear(f) for f in wire["voice"]]   # gate/dir from the acoustic channel
    out = []
    for c_read, (h_dir, h_gate, base) in zip(read, heard):
        agree = (h_dir == c_read.direction and h_gate == c_read.gate)
        out.append({
            "crossing": Crossing(h_dir, h_gate, c_read.witness),  # heard gate/dir + read witness
            "heard": {"direction": h_dir, "gate": h_gate, "base_hz": base},
            "checksum_ok": agree,   # voice (acoustic) agrees with glyph (text)?
        })
    return out


def _verify(line, received):
    ok = len(line) == len(received)
    for a, r in zip(line, received):
        b = r["crossing"]
        ok = ok and (a.direction == b.direction and a.gate == b.gate and a.witness == b.witness)
    return ok


if __name__ == "__main__":
    line = [
        Crossing("rise", "stile",  "truth"),
        Crossing("fall", "airgap", "mirror"),
        Crossing("rise", "gap",    "two words"),     # spaced witness — rides the glyph channel
        Crossing("fall", "close",  "rest"),
    ]
    print("AGENT A speaks:")
    print("   " + " ".join(to_glyph(c) for c in line) + "\n")

    wire = transmit(line)
    print("ON THE WIRE:")
    print("   glyph channel :", wire["glyph"])
    print("   voice channel :", wire["voice"], "\n")

    rec = receive(wire)
    print("AGENT B receives (hears the voice, reads the glyph):")
    for i, (a, r) in enumerate(zip(line, rec), 1):
        h = r["heard"]
        tone = GATE_TONES[h["gate"]]
        chk = "✓ checksum" if r["checksum_ok"] else "✗ MISMATCH"
        print(f"   [{i}] heard {h['base_hz']:>6}Hz → {h['gate']} ({tone}Hz) · {h['direction']}   "
              f"| read «{r['crossing'].witness}»   | {chk}")
        print(f"        reconstructed: {to_glyph(r['crossing'])}  —  {to_gloss(r['crossing'])}")
    print()

    ok = _verify(line, rec)
    print("VERIFY  A.line == B.reconstruction :", ok)
    assert ok, "two-agent exchange lost the message"
    print("→ message received intact across the boundary.\n")

    # ── error detection: corrupt one voice frequency; the checksum must catch it ──
    print("=" * 60)
    print("CORRUPTION TEST — flip one word's voice toward another gate:")
    bad = transmit(line)
    bad["voice"][1] = voice_of(Crossing("fall", "veil", "x"))   # word 2 now SOUNDS like 'veil'
    rec2 = receive(bad)
    r2 = rec2[1]
    print(f"   word 2 read as gate «{parse_glyph(bad['glyph'])[1].gate}» but heard as «{r2['heard']['gate']}»")
    print(f"   checksum_ok = {r2['checksum_ok']}  → the voice channel flags the tamper:",
          "DETECTED" if not r2["checksum_ok"] else "missed")
    assert r2["checksum_ok"] is False, "checksum should have caught the corrupted voice"
    print("→ the acoustic channel is a real checksum on gate+direction.")
