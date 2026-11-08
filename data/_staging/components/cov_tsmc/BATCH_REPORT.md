# Batch report cov_tsmc (TSMC-fabricated photonics, DevLog-015 stream S1, 2026-11-07)

Distilled under the pic-component-distill skill (contract v4-v6). Dry-run
`merge_component_staging.py data/_staging/components/cov_tsmc --dry-run`: +4 components, +13 metrics, 0 errors
(the one WARN printed concerns an existing lit row, not this batch). Research note values
(`DevLog/research/2026-11-07-tsmc-siph-values.csv`) were re-checked against the texts and figure renders; differences
are listed per paper.

| source | text | components | metrics |
|---|---|---|---|
| pk:ectc51687.2025.00015 (TSMC COUPE, ECTC 2025) | packaging atlas `references/ectc51687.2025.00015/text.md` + page renders | 2 | 7 |
| eo:song2026 (NVIDIA, ISSCC 2026 23.1) | EO atlas `references/song2026/text.md` + `figures/img_p03_1.png` | 2 | 6 |
| ofc2026:M4B.2 (NVIDIA, OFC 2026) | OFC extracted text (no figures) | 0 new (2 / 6 already merged) | 0 |
| ofc2026:M2A.7 = eo:patel2026 (NVIDIA, OFC 2026) | EO atlas `references/patel2026/text.md` + page renders | 0 | 0 |

Source ids: the ISSCC paper also exists as `pk:isscc49663.2026.11409081` with `same_as eo:song2026`, and
`ofc2026:M2A.7` has `same_as eo:patel2026`; rows use the canonical `eo:` ids (D23). Page-1 titles checked for all four
texts.

## pk:ectc51687.2025.00015 - Optical and Electrical Characterization of a Compact Universal Photonic Engine

Components
- `cmp_ectc51687_2025_00015_coupe_gc` (fiber_chip_coupler.grating; platform empty, GC layer not stated, D422):
  m1 insertion_loss_db 1.2 lt, loopback_half, loopback, measured (p.3 Sec. IV.A, Fig. 6, Abstract);
  m2 bw_1db_nm 25 approx, measured (COUPE level); m3 wavelength_spread_nm 1.7 lt (+/- across one 300 mm COUPE wafer,
  Fig. 7(b)); m4 bw_1db_nm 20 approx, derived (same GC on the PIC wafer: 25 - 5 nm, as printed "5 nm more");
  m5 pitch_um 127, design_target (FAU fiber spacing, p.3 Sec. III).
- `cmp_ectc51687_2025_00015_coupe_lens_path` (micro_optics.integrated_lens; 800 um support Si + ARC + embedded
  micro-lens, net of the Cu reflector gain): m1 insertion_loss_db 0, statistic mean, scope de_embedded,
  reference_structure (COUPE-GC minus PIC-wafer GC), measured (Fig. 7(a)); m2 same quantity 0.04, statistic std.

Fab evidence: all authors TSMC; the paper reports silicon results of "TSMC's COUPE wafer" (p.2 Sec. I) after
process optimization of the COUPE process (p.1 Abstract); PIC from the TSMC 300 mm SiPh PIC platform (p.1 Sec. I).
Entered fab_org_ids = org_tsmc on both rows (see Q1). No facility orgs (acknowledgment names internal TSMC
organizations only).

Not entered and why
- Metal reflector IL gain 0.5 dB (p.3 Sec. IV.A, Fig. 5(b)): figure is a simulation, text claims simulation and
  silicon; no registry parameter for a gain delta (gap G1).
- Beam-angle variation < +/-0.1 deg after FAU assembly (p.3 Fig. 8): no parameter (gap G2).
- TDECQ 1.61 -> 1.68 dB through a COUPE loopback at 53.125 GBd PAM4 (p.4 Fig. 9): link / signal metric, no
  parameter (gap G3).
- IL change < 0.25 dB after MR3x + TC-C 300, TC-G 1000, DH 85/85 1000 h, HTS 175 C 1000 h (p.4 Sec. V.A, Fig. 11):
  il_change_db gap already raised in pk_oi; belongs to the reliability-tests table if anywhere.
- PIC-wafer GC loss: only said to match the COUPE value, no number.
- SoIC / TDV daisy-chain resistance and RF 3-dB bandwidth > 100 GHz (simulated): electrical, out of scope.
- 800 um support Si thickness: geometry without a fitting micro_optics parameter; kept in the component text.

Differences from the research CSV: the text says "less than 1.2 dB", so qualifier lt (the CSV had le from the Fig. 6
label); the "net COUPE loss 0 dB" is entered as a de_embedded micro-optics row rather than per_interface (Q4).

## eo:song2026 - 32 Gb/s/lambda clock-forwarding DWDM link, 7 nm EIC / 65 nm PIC (ISSCC 2026)

Components
- `cmp_song2026_gc` (fiber_chip_coupler.grating, soi, host song2026-a): m1 insertion_loss_db 3.8 approx, scope
  unspecified, extracted_from_figure: off-resonance envelope of the PIC TX bus sweep (Fig. 23.1.5 top left, p.3),
  flat from about 1300 to 1316 nm; line centre -3.8 dB, top edge -3.6 dB, inset baseline -3.8 dB; reading
  uncertainty +/-0.2 dB (main plot 9.2 px/dB, inset 5.1 px/dB on the 1784 px embedded image). m2 insertion_loss_db
  1.9 le, loopback_half, author_estimate: m1 / 2 (range 1.8-2.0), resting on the unstated assumption that the sweep
  is an un-normalized fiber-in / fiber-out path through two identical GCs with all off-resonance loss assigned to
  the GCs; upper bound because bus and ring off-resonance loss stay in.
- `cmp_song2026_rx_mrr_filter` (wdm.mrr, soi, host empty: the EO row song2026-a is the TX modulator):
  m1 q_loaded 4000 (unqualified "4K"), author_estimate (Q3); m2 radius_um 5 approx, design_target (stated for the
  PIC's rings generally); m3 n_channels 9, design_target; m4 channel_spacing_ghz 200, author_estimate (design grid,
  D82a).

Fab evidence: none. The paper says only "65nm SiPh process" (p.1 Abstract) and "65nm SOI SiPh" (p.3 Fig. 23.1.6);
no foundry named, TSMC appears nowhere in the text. fab_org_ids empty (NVIDIA affiliation rule of the benchmark
applies, per the task).

Not entered and why
- GC 1-dB bandwidth from the envelope: the envelope is cut by ring dips and steps by about 1.3 dB at about 1298 and
  1317 nm (ring-related, not a GC shape); read spans were 1-dB about 19 nm (1298-1317 nm) and 3-dB about 31 nm
  (1291-1322 nm), but a two-coupler width is not a single-GC width.
- RX / TX PDs (drop-port monitor PDs and high-speed RX PDs): no PD metric; RX sensitivity -16.0 dBm OMA is a
  receiver figure.
- Ring heaters: tuning shown only as heater DAC code vs a 0.1 nm laser step (Fig. 23.1.5 top right, no physical
  unit); heater energy 0.76 pJ/b (measured with the bench laser) and 0.49 pJ/b (estimated from measured heater
  efficiency) cover TX + RX rings of the link (Fig. 23.1.6 notes e, f); no per-ring power or efficiency.
- FAU and lens carrier chip (Fig. 23.1.7): no metrics.
- TX ring values (Q ~4.5K, dip depths, 200 GHz spacing): modulator, EO atlas (rule 2); song2026-a already holds
  Q 4500 and ER 17 dB.

Differences from the research CSV: envelope read 3.8 dB (line centre) vs CSV 3.6-3.9; half 1.9 le vs CSV 1.8-2.0 le;
consistent. The research CSV scoped the raw envelope fiber_to_fiber (assumed); entered as unspecified because the
paper does not state what the sweep includes (rule 6).

EO-atlas candidates (song2026-a, not in its columns or notes): heater energy 0.49 pJ/b estimate (Fig. 23.1.6 note f,
3 sigma ring and modeled laser variation); TX ring channel spacing about 200 GHz on the TX bus (p.1, now a tag only).
The TX ring FSR could be read from the full sweep (dip pattern repeats) but was not read.

## ofc2026:M4B.2 - A 256 Gb/s DWDM Optical I/O in a 3D-Stacked EIC/PIC Silicon Photonics Platform

Existing merged rows checked at their locators: `cmp_ofc2026_m4b2_vgc` (1.3 dB unspecified author_estimate, 1-dB
20 nm, central-wavelength spread < +/-1.7 nm) and `cmp_ofc2026_m4b2_rx_mrr_filter` (Q 4200, 200 GHz, 9 channels)
match the text. No new component with a quantitative result: high-speed PDs and heaters have no metrics; the DFB-array
external laser source (230 GHz, 3 dBm per wavelength) is setup equipment (rule 13). 0 rows added.

Fab evidence: none in the text; the 65 nm PIC platform is only cited as [2] (Yeh et al., IEDM 2024) and the
cross-section in Fig. 1(d) is cited from [3]. fab_org_ids stays empty.

EO-atlas candidates (M4B.2 is not in the EO atlas): MRM Q about 4500 (doping-mask limited, below the modeled
optimum); driver sinks up to 300 uA MRM photocurrent at 0-3 dBm per wavelength; RX sensitivity about -17 dBm OMA at
BER 1e-11, 32 Gb/s PRBS31; 2.02 pJ/b link energy excluding the laser (Sec. 2-3). Same chip family as song2026; the
ISSCC paper prints RX filter Q 4K where M4B.2 prints 4200.

## ofc2026:M2A.7 / eo:patel2026 - Si Microring Resonator Modulators at >200Gb/s

Review / tutorial paper: no device of its own is characterized. Table 1 and Fig. 3 (p.3) list MRM results of cited
works (rule 3, not entered); Fig. 1-2 are models and illustrations. The TSMC COUPE mention (p.1 Sec. 1) concerns
MRMs of a product announcement, not a device measured in the paper. 0 rows; the EO atlas already records this paper
as "no device rows". EO-atlas candidates: none (all tabulated values belong to the cited papers).

## Judgment calls

- COUPE fab from the foundry's own wafer / process statements rather than an explicit "fabricated by" sentence (Q1).
- The PIC-wafer GC is the same GC before COUPE processing: entered as a condition on the COUPE-GC row (m4), not a
  sibling component.
- Half-envelope GC loss for song2026 kept as author_estimate loopback_half with qualifier le (Q2).
- The COUPE lens-path row carries a net value that includes the reflector gain; its inherent loss is not stated.

## Registry gaps

- G1 `il_gain_db` (micro_optics, fiber_chip_coupler): IL improvement from an added feature (reflector, ARC), positive
  dB; skipped: 0.5 dB, pk:ectc51687.2025.00015 p.3 Sec. IV.A / Fig. 5(b) (simulated).
- G2 `beam_angle_variation_deg` (micro_optics, fiber_chip_coupler): +/- spread of the output beam angle across
  samples; skipped: < +/-0.1 deg, p.3 Fig. 8.
- G3 `tdecq_penalty_db` (fiber_chip_coupler, micro_optics, fiber_interface): TDECQ increase through the component
  path at a stated rate / format; skipped: 1.61 -> 1.68 dB at 53.125 GBd PAM4, p.4 Fig. 9.
- (repeat of pk_oi) `il_change_db` after stress tests: < 0.25 dB, p.4 Sec. V.A / Fig. 11.

Missing orgs: none (org_tsmc exists; no other fab or facility org named).

## Questions

1. COUPE fab_org_ids = org_tsmc rests on "TSMC's COUPE wafer" (p.2 Sec. I) and the COUPE process wording (p.1),
   not on a "fabricated by" sentence; contract v4 asks for an explicit statement. Recommendation: accept (a
   foundry reporting its own process wafer), or strip both rows' fab and the benchmark loses its only measured
   loopback_half TSMC GC value.
2. song2026 GC m2 (1.9 dB le, loopback_half, author_estimate) exists only to make the envelope usable as a per-coupler
   bound. Keep it, or keep only m1 (scope unspecified)? Recommendation: keep; the benchmark can exclude
   author_estimate if needed.
3. song2026 RX filter Q 4K: author_estimate (design selection, test-chip validation without data) vs measured with
   test_structure true. Recommendation: author_estimate, consistent with M4B.2's 4200 row.
4. COUPE net path loss 0 dB (mean) / 0.04 dB (std): de_embedded on a micro_optics.integrated_lens row, vs
   per_interface as used for the 00284 micro-lens link. Recommendation: de_embedded (it is a difference against
   the PIC-wafer GC, not an interface measurement).
