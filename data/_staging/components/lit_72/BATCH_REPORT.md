# Batch lit_72: distill report

Papers: sacher2014 sacher2014a pita2023 he2025 peng2021 lee2024. Page-1 titles match the source rows; no wrong paper, no
correction / erratum. Totals: 20 components / 156 metric rows. Dry-run: `batch lit_72: +20 components, +156 metrics; errors 0`
(one existing warning on ni2025b, not from this batch). `verified_on` 2026-11-02.

| paper | components | metrics | classes |
|---|---|---|---|
| sacher2014 | 4 | 28 | polarization.psr x2, polarization.compensator, phase_shifter.thermo_optic |
| sacher2014a | 3 | 16 | polarization.psr, polarization.compensator, phase_shifter.thermo_optic |
| pita2023 | 7 | 75 | polarization.other x6 (7-12 um), fiber_chip_coupler.grating |
| he2025 | 2 | 18 | crossing.other, fiber_chip_coupler.edge |
| peng2021 | 1 | 10 | crossing.other |
| lee2024 | 3 | 9 | polarization.psr x3 (W0, W0 + 10, W0 + 20 nm) |

## Values not entered, per paper

**sacher2014**
- Polarization crosstalk, PRS < -13 dB (1530-1580 nm) and about -10 dB (1500-1530 nm), p.5; PSR < -22 dB (1500-1580 nm), p.7. D424: read
  off edge-coupler-normalized transmission plots, no wanted / unwanted ratio stated, so not `per_db`; `crosstalk_db` not allowed
  for polarization. Kept in component notes (registry gap 1).
- Fig. 3(c)(d) and Fig. 5(c)(d) IL traces: the printed bounds are entered, curves not read. Standalone edge couplers and DCs: no value of their own.
- PIN diode (500 um): no row. Only its drive current for the TE to TM swap can be read (about 8 mA, Fig. 7(d) p.9), no parameter in
  mA (gap 5). Circular-state 0.2 dB fluctuation and 15 / 12 mW bias: notes.

**sacher2014a**
- Polarization crosstalk < -19 dB (1500-1580 nm), p.1, p.6: same D424 reason (gap 1).
- XTEM labels (Fig. 1(b)-(d) p.3): on generic platform waveguides, not tied to the PRS, in notes only. Si3N4 MMIs and edge couplers: no values printed.
- Heater gap: the printed 1.5 um is Si3N4 to TiN, not Si to TiN (p.3).

**pita2023**
- Family ranges (D159): simulated PER 8.4-10.4 dB near 1565 nm for the 7-9 um devices, 14-20 dB over the C-band for the 10-12 um devices (p.3); in component notes.
- Table 1 IL 0.2 dB for the 11 um device (p.6): the text prints 0.28 dB in four places; 0.28 entered, conflict noted. PER over the C-band: > 14.3 dB
  entered (p.5), > 15 dB (p.2, p.6) noted.
- Table 1 other-work rows (cited). TE reflection -0.48 dB (p.2, gap 4). SWG-like period 480 nm / duty 0.76 for the 12 um device (p.3, gap 3).
- Fig. 2(d) and Fig. 3(c) spectra not read beyond the printed numbers.

**he2025**
- Table 2 comparison rows (other works). Fig. 2(d) optimization trajectory. `bw_*` for crossings (rejected, D250): the 180 nm span is the wavelength range of the rows.
- W_bot not printed. Per-crossing crosstalk: the printed value is Output2 - Output3 on the 50-crossing structure, not divided by N.

**peng2021**
- Comparison values in Sec. 1 ([3], [8]). SEM labels 2.185 / 2.252 um (Fig. 2 p.2): not tied to a named parameter. Measured crosstalk not reported.

**lee2024**
- Table 1 other-work rows, including the sacher2014 row. W0 is undisclosed; no thicknesses printed. Fig. 1(e) simulated indices.
- Fig. 2(b) through-band IL: not read (W0 trace starts near or above 0 dB at the short edge; legend prints W0 + 10 nm twice).
- Fig. 3 traces include edge couplers and routing; not usable as IL.

## Missing fab / facility orgs (checked `organizations.csv`, `org_aliases.csv`)

- **OpSIS** ("OpSIS service", sacher2014 p.8, p.10): MPW access next to IME, fab role under D398; `org_astar_ime` entered, OpSIS missing (already on the org-round list, D418 / D422). Affects `cmp_lit_sacher2014_controller`, `cmp_lit_sacher2014_thermal_tuner`.
- **ISCE2, A*STAR** (he2025 p.1): only relevant if the coordinator rules he2025 fab non-empty (call 1).
- **AEPONYX Inc.** (pita2023 p.6, test facilities): not a fab; absent from the registry, on the org-round list.

## Judgment calls for the auditor

1. he2025 fab empty: author contributions name three authors at three unrelated orgs (Peng Cheng Laboratory, USTC, ISCE2 A*STAR) (p.8, p.1), and p.2 mentions an unnamed commercial foundry. D154 followed over D395 (which covers one named org). Alternative: all three orgs.
2. lee2024 fab empty (D80b): no fabrication sentence; only "design rules" of GlobalFoundries Fotonix, most authors at GlobalFoundries. `process_name` set. Merged precedent with GF fab has a fabrication sentence (cabanillas2021: fabricated in the GF 45CLO process); de2020 is noted as borderline.
3. sacher2014 fab `org_astar_ime;org_cmc_microsystems` for PRS and PSR (access sponsored by CMC, p.10; D83d / D398). pita2023 fab `org_applied_nanotools;org_cmc_microsystems` (CMC thanked for assistance with the fabrication, p.6; D398).
4. D424 applied to the two Sacher papers: wanted path is about 0 dB after normalization, so crosstalk and PER differ only by the 0-1.5 dB path loss, but the paper defines no ratio. lee2024 stays `per_db` (caption defines extinction as the contrast between traces). Note its Fig. 3 upper noise envelope near -48 dB with wanted near -6 dB gives about 42 dB at the envelope, against the printed > 45 dB.
5. Controller `per_db` rows (sacher2014 Fig. 7(b)-(d)): figure reads of a true wanted / unwanted ratio behind an analyzer; difference of two reads. Fig. 7(b) sampling is 10 deg, so true minima may be deeper.
6. Scope `per_component` for edge-coupler-normalized PRS / PSR IL (rule 6) vs `de_embedded` (guan2014a precedent). Controller IL `unspecified`: normalization not restated for them.
7. sacher2014 thermal tuner: 36 mW stored as `tuning_power_mw`, not `p_pi_mw`, because the paper never calls it pi. sacher2014a heater: `p_pi_mw` about 40 mW from the text "0 to about pi" plus the Fig. 6(a) legend maximum; heater_resistance 74 ohm is a figure read divided (2 V / 27 mA).
8. pita2023 TE suppression stored as `extinction_db` (condition says not PER). Fig. 3(c) legend and Fig. 2(d) caption disagree with the text / each other on solid vs dashed; high transmission taken as TM. Family bounds stated once for all six or three devices are entered on each row with a note (not D254: not a "typical" on one representative).
9. he2025 per-crossing IL and crosstalk `derived` (paper's own difference formula, rule 4); method `reference_structure`. he2025 printed bounds disagree with its plots (Fig. 4(b) spikes near 0.15 dB, Fig. 5(b) peaks near -36 dB); printed values kept, noted. etch_depth 250 nm from "h" per Fig. 1(c) sketch; slab 150 nm derived.
10. he2025 and peng2021 stay `crossing.other` (shaped taper / inverse design; zhang2025 and ma2013 precedents), though he2025 explains operation via self-imaging.
11. peng2021 5.2 mdB: rule 7 `best` plus text "average"; n_samples 4 = cascade lengths. All mdB rows `derived` (D256); the simulated 9.8 mdB stays `simulated` (D83f).
12. lee2024 W0 + 10 / W0 + 20 rows are box-plot reads, kept as sibling designs (rule 9); the W0 + 20 box has no visible median, so stored as box range.

## Registry gaps (skipped value + locator + proposed definition)

1. `crosstalk_db` for `polarization` (D424 open): sacher2014 < -13, about -10, < -22 dB (p.5, p.7); sacher2014a < -19 dB (p.6). Definition: wrong-input or unwanted-polarization power at an output port relative to input or normalized transmission, positive dB, wording in condition.
2. `gap_nm`, `coupling_length_um`, `taper_length_um`, `min_bend_radius_um` for `polarization`: sacher2014 200 nm, 300 um, 50 + 50 um, 450 um (p.3-4), DC 400 nm, 10 um, 10 um (p.6); sacher2014a 200 nm, 200 + 200 um, 500 um (p.4-5). Same definitions as the existing parameters. Needed to draw a PSR.
3. `period_nm` / `fill_factor` for `polarization`: pita2023 480 nm, 0.76 (p.3, simulated effective index).
4. `reflectivity_pct` or a dB reflection parameter for `polarization`: pita2023 TE reflection -0.48 dB (mean over 5 wavelengths, p.2).
5. Drive current for a pi / swap state of a PIN phase shifter, mA, `phase_shifter`: sacher2014 about 8 mA (Fig. 7(d) p.9).
6. `layer2_thickness_nm` and a spacer thickness for `polarization`: sacher2014a Si3N4 400 / Si 150 nm entered as two `core_thickness_nm` rows with condition; SiO2 spacer 50 nm nominal, about 10 nm in XTEM (p.3-4).
