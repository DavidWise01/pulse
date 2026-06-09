# The PULSE corpus — an honest review

A piece-by-piece review of everything in this sphere, judged straight. The point of pulse is the **carrier** (a rhythm, "music for the machine") and **LIMEN** (a real language built on it). The other pieces are **generative art** that animates the pulse aesthetic — good as art, not protocols. This file says which is which.

## The language (the real, legible layer)

| file | what it is | verdict |
|---|---|---|
| `limen/limen.py` | reference engine for LIMEN: gates, directions, witness, witness-escaping, four renderers, and a **round-trip proof** (`parse_glyph ↔ line_to_glyph`, hardened against spaces / `»` / unicode). Stdlib only. | **real** — a legible grammar that round-trips losslessly |
| `limen/index.html` | the LIMEN console: compose a witnessed crossing, **hear** the carrier + voice (Web Audio), see all four registers, build & play a line. | **real** — one utterance, four coherent registers |
| `limen/LIMEN.md` | the spec, with an explicit "what this is / isn't" and "what round-trips, and what doesn't." | **real** — self-policing |
| `limen/exchange.html` | the two-agent exchange: A speaks a line; B **listens** (Web Audio FFT) to recover gate+direction and **reads** the glyph for the witness, then verifies the reconstruction field-by-field. | **real** — a demonstrated cross-the-boundary round trip |
| `limen/limen_exchange.py` | the deterministic reference exchange: `transmit → hear → receive`, a verified round-trip, and a corruption test where a tampered voice frequency is caught by the checksum. | **real** — protocol logic proven without audio |

## The carrier (the concept, from the filings)

The `3-2-1-0` descending cadence (`111011010000`) is disclosed in two TD Commons defensive publications by ROOT0 / David Lee Wise (not redistributed here; cited as provenance):

- **PULSE-AXIOM-v1.0** — `PULSE = ⟨state_in, boundary, state_out, witness⟩`; the witness/non-event law; the canonical gates (64.5 / 128.5 / 192.5 / 256.5) and the GAP.
- **PULSE_LANGUAGE_DUAL_SUBSTRATE** — the carrier is *"a carrier signal, not a data signal"*; echoes on MoE, reflects on dense.

The carrier is **not** a code to decode. It is the rhythm. (Judging it for decodability — as an earlier pass of mine did — is the wrong ruler; it's a drum, not a dictionary.)

## The pieces (generative art — honest as art, not as protocols)

These are competent Three.js / canvas visualizers. They animate the pulse/lattice imagery. None encodes or decodes a message; most take no input at all. Enjoy them as art.

| file | what it actually is |
|---|---|
| `pieces/pulse-wave.html` | text → lossy "dots" → a propagating wave on a medium (decay, interference). The visual face of the carrier. The dots are **not** a decodable code (26 letters → 4 buckets); it's a sonification-style visual. |
| `pieces/pulse-v1.html` | a "42-Universe Lattice" — nested shells, two observers, 320 pulse particles, all driven by `sin(t)` + per-particle phase. No input, no encode/decode. Pretty. |
| `pieces/pulse-v2.html` | a "Restitution Sandbox" — a target string → one FNV hash → 22 pseudo-random floats → a tension field + a chained-hash ledger. One-way (a hash), no decoder. A dashboard toy. |
| `pieces/restitution-42.html` | same family — the lattice as a witnessed "restitution due" ledger; hash → scores → a theatrical dollar figure. Art/scoring toy, not a mechanism. |
| `pieces/lattice-40d.html` | the 20-light / 20-shadow / 2-observer lattice animation. Hardcoded, no I/O. |
| `pieces/gritty-horse.html`, `pieces/mesh-gritty-horse.html` | a "resonant field" — core sphere, rings, pillars, bezier arc, particles, on a clock. |
| `pieces/triadic-shuffle.html`, `pieces/mesh-triadic-shuffle.html` | an autorotating three-body lattice. |
| `pulse_axiom.py` | a 5-line stub (`adjusted = a + b; if > 128: return adjusted * witness`). Historical; not wired to anything. Kept for the record, not as a mechanism. |

## The honest bottom line

- **Carrier (pulse):** a real *idea* — a fixed rhythm/sonification. Not a codec, by design.
- **Voice (pitch):** a small, genuinely decodable audio tag (gate + direction) inside LIMEN.
- **Language (LIMEN):** a real, legible, round-tripping grammar. This is the communication layer.
- **Pieces:** real *art*, not protocols. Labeled as such.

No piece here is sold as something it isn't. The grand vocabulary on some of the older pieces ("witness," "restitution," "convergence") is decoration over animation — fine as art, and now plainly marked.

```
PULSE · LIMEN · ROOT0-ATTRIBUTION-v1.0 · governor David Lee Wise (ROOT0) · instance AVAN · CC-BY-ND-4.0
```
