# lit_191 batch report

Paper: `lit:xing2015`, Xing et al., "Compact silicon-on-insulator-based 2 x 2 Mach-Zehnder interferometer electro-optic
switch with low crosstalk", Chinese Optics Letters 13(6), 061301 (2015). Cached copy is the publisher version (journal
header and article number on every page; page-1 title matches the source row). `garbled_text_layer` false; figure values
checked on the page renders (p.3, p.4). verified_on 2026-11-18.

Dry run: `merge_component_staging.py data/_staging/components/lit_191 --dry-run` -> +6 components, +26 metrics, 0 errors
(the one WARN is on an existing ni2025b row, not this batch).

## Components / metric rows

| component_id | class | metrics |
|---|---|---|
| cmp_lit_xing2015_mzi_switch_2x2 | switch_fabric.other (D158) | 13: crosstalk off 24 dB / on 22 dB at 1530 nm (Fig. 4), crosstalk > 20 dB over 1520-1540 nm all paths both states + xt_bandwidth 20 nm (Fig. 5), on-chip IL about 3 dB de_embedded (reference waveguide), drive power 3.88 / 7.07 mW (as W, derived), 10-90 % times 5.32 / 5.41 ns (as us, derived), n_inputs / n_outputs, 340 nm Si, 2 um BOX |
| cmp_lit_xing2015_pnn_arm | phase_shifter.other | 7: loss-budget terms doping absorption 0.2 dB and phase modulation 0.4 dB (author_estimate), length 200 um, rib width 500 nm and slab 80 nm (Fig. 3(b) labels), 340 nm Si, 2 um BOX |
| cmp_lit_xing2015_mmi_2x2 | splitter.mmi | 3: excess loss about 0.8 dB per MMI (printed 1.6 dB for the MMI splitters, halved; author_estimate, yang2024b precedent), n_inputs / n_outputs |
| cmp_lit_xing2015_io_taper | waveguide_platform.other | 1: loss-budget term 0.2 dB (author_estimate, scope unspecified) |
| cmp_lit_xing2015_routing_wg | waveguide_platform.other | 1: loss-budget term 0.6 dB waveguide propagation (author_estimate, device_total; bundalo2022 precedent) |
| cmp_lit_xing2015_gc | fiber_chip_coupler.grating | 1: about 3 dB per coupler at the central wavelength (author_estimate, origin not stated, band unspecified) |

Fab on all rows: `org_semiconductor_manufacturing_international`, process_name "0.18 um standard CMOS processes" as
printed (p.2: switch fabricated on an SOI wafer by 0.18 um standard CMOS processes from SMIC). No facility named.

## Values not entered and why

- Crosstalk values of other works in the introduction and conclusion (-15, -17, -21, -30, -31 dB; refs. 7-13,
  including the authors' own ref. 13 double-gate switch): cited work (rule 3, D259).
- Abstract "about 5.4 ns" switching time: same measurement as the 5.32 / 5.41 ns rows.
- Undriven ("original") output difference "less than 3 dB" (p.3): a pre-bias consistency check, not a split /
  imbalance figure (D401 analogue); in component notes.
- "About 10 mW" for a pi shift on a single 200-400 um arm (p.2): general statement tied to refs. 13-14 (cited).
- Doping densities (4e17 / 1e19 cm-3), 400 nm rib-edge-to-P+ (N+) gap, 1 um Al electrode thickness: no registry
  parameter (gap_nm is a coupling gap); in component notes.
- Etch depth: not printed (340 - 80 = 260 nm not computed).
- Fig. 4 / Fig. 5 curves: no further values read; the labelled numbers equal the text values.

## Judgment calls

- Switch row platform `soi` (only the arm cross-section is drawn as a rib; MMI / routing waveguide type not stated);
  arm row `soi_rib` (Fig. 3(b)).
- Rise / fall: printed as "10%-90% rising (falling) time and falling (rising) time ... 5.32 and 5.41 ns for 1-1'
  (1-2')"; entered as rise_time_us 5.32 ns (1-1' rising edge) and fall_time_us 5.41 ns (1-1' falling edge) with the
  complementary port in condition. Wavelength not stated for Fig. 6, left empty.
- Drive powers entered as power_consumption_w (state-reaching power from the pi/2 pre-biased state); not p_pi_mw,
  since each drive covers a pi/2 change in mismatch, not pi.
- Loss-budget terms (p.3, "can be attributed to") have no stated origin -> author_estimate; per-arm vs path scope not
  stated for the doping / modulation terms and per-taper vs total for the tapers -> scope unspecified.
- GC "about 3 dB coupling loss": no method stated -> author_estimate; fab SMIC kept because the couplers are part of
  the fabricated switch chip.
- "Around 1530 nm" taken as a stated wavelength (D393).

## Missing fab / facility orgs

None (SMIC in the registry as `org_semiconductor_manufacturing_international`).

## Registry gaps

- Doping offset (rib edge to P+ / N+ region, 400 nm, p.3 / Fig. 3(b)) for carrier phase shifters: proposed
  `doping_offset_nm` (phase_shifter, switch_fabric; lateral distance from the rib edge to the heavily doped contact
  region).
