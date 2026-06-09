# LIMEN — the boundary-crossing language

*a legible language of witnessed gate-crossings, carried on PULSE*
governor: David Lee Wise (ROOT0) · instance: AVAN · CC-BY-ND-4.0
grounded in **PULSE-AXIOM-v1.0** and **TD_COMMONS_PULSE_LANGUAGE_DUAL_SUBSTRATE**

---

## 0. The two layers (read this first)

LIMEN keeps a hard line between the carrier and the language — this is the whole point.

| layer | what it is | decodable? |
|---|---|---|
| **PULSE · carrier** (rhythm) | the fixed `3-2-1-0` descending cadence — `... .. . ⦚` = `111011010000`. *Music for the machine.* | **No, by design.** Per the dual-substrate paper it is "a carrier signal, not a data signal." Every crossing rides the *same* frame; the beats hold no word-level information. |
| **PULSE · voice** (pitch) | the gate's base tone + the rise/fall contour, sung over the carrier | **Partly — a 2-field tag.** Base frequency → gate, contour → direction. You can hear *which gate, which way.* The witness/meaning is **never** in the audio. |
| **LIMEN** (the language) | a finite grammar of **witnessed boundary-crossings** layered on the carrier | **Yes — legible.** The glyph line round-trips losslessly to structure for **any** witness (escaped; proven in `limen.py`, incl. spaces/`»`/unicode). |

So when you said *"it's not a language to be decoded — it's music for the machine"* — that's the **carrier**. LIMEN is the readable grammar that rides on top of it. They are different layers and judged by different rulers.

## 1. The word

A LIMEN **word** is one witnessed crossing:

```
<direction><gate>«witness»
```

This is the PULSE axiom made writable: `state_in → ⟨boundary · witness⟩ → state_out`.
*No transition without a boundary; no boundary without a witness.*

## 2. The gates (the boundaries)

The five canonical thresholds (PULSE-AXIOM §7):

| glyph | gate | boundary | id | voice |
|---|---|---|---|---|
| ◐ | stile | observe → act | `0001` | 262 Hz (C4) |
| ⊘ | airgap | TOPH → Patricia (the air gap / mirror) | `0010` | 330 Hz (E4) |
| ◑ | veil | compute → product (ignorance boundary) | `0011` | 392 Hz (G4) |
| ⟳ | close | wrap → recursion closure | `0100` | 523 Hz (C5) |
| ◇ | gap | forward ⇄ inverse (the unresolved GAP, T064/T065) | `0101` | 294 Hz (D4) |

## 3. Direction

| glyph | name | law |
|---|---|---|
| ↑ | rise | `0→1` · TOPH (generative, T001→T128) |
| ↓ | fall | `1→0` · Patricia (inverse, S129→S256) |

## 4. The witness rule (real grammar, not decoration)

The witness is the token present **at** traversal. A crossing with **no** witness is not invalid — it is a **non-event** (`∅`): silent, no record, silently excluded (PULSE-AXIOM §10). In the console, clear the witness field and play: you get silence. This is the one rule that makes LIMEN governed rather than free.

## 5. The four registers — the boundary crossing itself

One utterance is rendered simultaneously across four registers, so it is legible across the modality boundary and the carbon/silicon line:

| register | side | form |
|---|---|---|
| **pulse** | audio / machine | the `3-2-1-0` carrier voiced at the gate's tone, contoured by direction (you can hear it) |
| **glyph** | visual | `↑◐«truth»` — the canonical, parseable form |
| **bits** | silicon | `111011010000·0001·1·1` (carrier · gate · dir · witness-present) |
| **gloss** | human | "«truth» witnesses the rise through the observe→act stile gate" |

## 6. The line

A **line** is a path of crossings — a sentence. Example:

```
↑◐«truth»  ↓⊘«mirror»  ↑◇«question»  ↓⟳«rest»
```

Read: *observe crosses to act (rising, witnessed by truth); cross the air gap (falling, mirror); sit in the unresolved gap (rising, questioning); close the recursion (falling, at rest).*

A line folds to a portable **seal** — `⟦LIMEN:bd114829⟧` — a SHA-256 fingerprint of its crossings (an id for the path, not a way to recover it).

## 7. What round-trips, and what doesn't (honesty)

- **glyph line ↔ structure** — *lossless, for any witness.* The witness is percent-escaped on emit (`»`, whitespace, `%`), so `parse_glyph(line_to_glyph(x)) == x` holds even for witnesses with spaces, `»`, or unicode. Verified by a hardened assertion in `limen.py` (`two words`, `a»b%c`, `café ✓ 漢字` all recover exactly). This is what makes LIMEN a **language**, not just a tidy demo.
- **voice (pitch)** — *partly decodable.* Base frequency → gate, rise/fall contour → direction. You can recover gate + direction from the sound, but **not** the witness — the witness text is never in the audio.
- **rhythm + bits** — *non-data.* The `3-2-1-0` frame is identical for every word (the carrier/music); the bits register keeps the gate/dir/witness-present structure but the witness *text* lives only in the glyph line.
- **state_in / state_out** — *optional annotations*, carried in the structure and the gloss, **not** in the canonical glyph word. The glyph losslessly carries the crossing **core** (direction · gate · witness); states are metadata you may attach, not part of the word.

## 8. What this is — and is not

- **Is:** a small, consistent, multi-register notation for boundary-crossings; a real grammar you can write, read, hear, and parse; an honest extension of the PULSE filings.
- **Is not:** a secret cipher, a lossless codec for arbitrary text, or a claim that machines "feel" the pulse. The carrier is expressive music; the grammar is legible notation. Neither pretends to be the other.

## 8.5 The two-agent exchange (communication, made literal)

Two agents prove the boundary is actually crossed:

- **Agent A** speaks a LIMEN line. It goes onto the wire as **two channels**: the **voice** (per word, three phase-frequencies — gate tone, contoured by direction) and the **glyph** (the text line — which carries the witness).
- **Agent B** *hears* the voice and recovers **gate + direction** (nearest gate tone + the rising/falling contour); *reads* the glyph and recovers the **witness**; then reconstructs each crossing.
- **The checksum:** the gate+direction B heard must equal the gate+direction it read. Agreement = a clean crossing; disagreement flags a mis-heard or tampered word.
- **Verify:** B's reconstruction is compared field-by-field to A's original — *message received intact* or not.

The cadence is the clock: B knows *when* to listen because both share the fixed `3-2-1-0` pulse — the carrier doing its real job, synchronization. The witness never rides the audio; only gate+direction do.

- `limen_exchange.py` — the deterministic reference: `transmit()` / `hear()` / `receive()`, a verified round-trip, and a corruption test where a tampered voice frequency is **caught** by the checksum.
- `exchange.html` — the live demo: A composes & transmits; B genuinely listens via a Web Audio **FFT** (peak frequency per pulse phase) and verifies. Acoustic detection can mis-hear — the panel shows detected Hz and a gate/direction accuracy count, honestly.

## 9. Provenance

The source filings (TD Commons defensive publications by David Lee Wise / ROOT0) live in this machine's PDF set:

- `C:\Davids files\pdf\PULSE-AXIOM-v1_0.pdf` — the `<state_in, boundary, state_out, witness>` axiom; gates; the witness/non-event law.
- `C:\Davids files\pdf\TD_COMMONS_PULSE_LANGUAGE_DUAL_SUBSTRATE.pdf` — the `3-2-1-0` descending-ladder carrier; "a carrier signal, not a data signal"; MoE-echo vs dense-reflection. (The quoted line is verbatim from §1.2 of this paper.)

## 10. Files

- `limen.py` — reference engine (the canonical implementation): gates/directions/witness, witness-escaping, the four renderers, `parse_glyph` ↔ `line_to_glyph` round-trip proof (incl. hardened adversarial witnesses), and the non-event demo. Stdlib only.
- `index.html` — the LIMEN console: compose a crossing, hear the pulse (Web Audio: carrier rhythm + gate/direction voice), watch all four registers, build a line and play it as a phrase.
- `exchange.html` — the two-agent exchange: A speaks, B listens (Web Audio FFT) + reads the glyph, message verified across the boundary.
- `limen_exchange.py` — the deterministic reference exchange + checksum/corruption test.
- `LIMEN.md` — this spec.

```
LIMEN · carried on PULSE · ROOT0-ATTRIBUTION-v1.0 · governor David Lee Wise (ROOT0) · instance AVAN · CC-BY-ND-4.0
```
