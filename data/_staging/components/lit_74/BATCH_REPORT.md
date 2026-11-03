# Batch lit_74 report (distill subagent, 2026-11-02)

Class wdm (plus fiber_chip_coupler.grating / edge, waveguide_platform.straight, splitter.y_branch rows the papers hold).
Papers: mason2025, pathak2014a, wijk2020, wang2023e, jia2025. Page-1 titles match the source rows; no wrong paper, no
correction. Totals: 35 components, 411 metric rows. Dry run: 0 errors.

## Per paper

| paper | components | metrics | contents |
|---|---|---|---|
| mason2025 | 10 | 119 | Si 2-channel Fig. 2(g), Fig. 3(a) N = 100 / 300, Fig. 3(d) sim; Si 3-channel sim; SiN WDM 1 sim, WDM 2 N = 100 / 300; WDM grating coupler; WDM with reflectors |
| pathak2014a | 9 | 129 | Table 1: 2 box and 2 S-shaped AWGs, 4 echelle gratings; curved GC |
| wijk2020 | 9 | 88 | flat-top primary, 3 secondaries, cascade, proposed small-AWG primary; rib waveguide, facet, blunt Y coupler |
| wang2023e | 4 | 48 | 1 x 8 and 1 x 5 test PEGs, cascaded 1 x 40; SiN-coated facet |
| jia2025 | 3 | 27 | 8 x 8 polymer AWGR; straight waveguide; two-facet coupling |

## Values not entered, and why

- mason2025: "below -40 dB" bound (abstract, p.7): the p.7 sentence points to Fig. 3(a), plotted floor about -37 dB, and SiN measures -34.5 dB; D159 note, only the 41 dB label of Fig. 2(g) is a row. Fig. 2(f) C / L-band simulations and Fig. 3(f) IL vs N (unlabelled points). Fig. 3(c) 1.38 dB reflection delta and p.10 pooled 1.21 dB port delta (no parameter, pooled over measured and simulated). Frequency comb and inverse-design GC of Fig. 2(e) / 4 / 5(e): no value. Comparison values in Sec. 1 (other works).
- pathak2014a: Delay L of the AWGs (center waveguide length, no parameter; notes). Min array gap 0.35 um (p.5; not a coupling gap). Side-channel IL up to 3 dB at the FSR edge (family statement, D254). Fig. 6 simulated maps. Angles 41 / 34 deg in notes.
- wijk2020: 0.5-dB bandwidth 45 nm (registry gap below). Abstract 4 dB central-channel optical loss: same number as the simulated primary loss of p.4, measured AWG 2 centre about 6.3 dB; entered on the primary as simulated, not on the cascade. Conventional 18 um input design and 1 x 7 + 7 x (1 x 30) comparison (Fig. 4(a), Fig. 7: no row). Optical bandwidth 190 nm (no operating-span parameter). AWG 1 / AWG 3 per-channel data absent; Table 1 values only.
- wang2023e: average noise floors -31 / -35 / -50 dB (registry gap below). 92 -> 98 % Al reflectivity (carries ref. [14], rule 3). 1.1 dB double-filtering penalty, BER and power penalties (system level, notes). Table III other works.
- jia2025: measured 6.20 x 6.05 um section (order of width / height not stated). Fig. 7 per-port reads (mean and min printed). Fig. 9 tolerance sweep. Table II other works. Taper width 15 um on the array side (no parameter; 10 um port taper entered as port_width_um).

## Missing fab / facility orgs (checked organizations.csv and org_aliases.csv)

- wang2023e: "VTT Technical Research Centre of Finland Ltd." (p.1 affiliation; p.4 Sec. III MPW run of the VTT 3 um SOI platform). fab empty on 4 rows; add org and set fab org_vtt (proposed id).
- jia2025: "Shandong University" (p.1 affiliation; p.2 designed and fabricated; all authors there). fab empty on 3 rows; add org and set fab (`org_shandong_normal_university` is a different institution).
- wijk2020: no fab statement naming an org; "VU University Amsterdam" (p.1) not needed. Rogue Valley Microdevices (p.2) wafer supplier, note only.

## Judgment calls for the auditor

1. mason2025 wdm_gc_cooptimized / wdm_reflector_cooptimized: values only in the p.4 summary, Supplement VII is not in the cached file. Entered as author_estimate (origin not stated), row_kind design, platform empty. Alternative: drop them until the supplement is available.
2. mason2025 crosstalk: paper does not type it, crosstalk_db everywhere. The 41 dB label is a contrast; printed SiN -34.50 / -34.48 dB match the absolute blocked-port floor in Fig. 5(g). Figure reads for Fig. 3(a) and Fig. 5(g) N = 100 use the deepest absolute level (condition says so), to stay comparable with the printed SiN values.
3. mason2025 Fig. 2(g) and Fig. 3(a) treated as different devices (passbands differ; p.7 says N = 100 / 300 are the same design). Bragg periods not stated for either. Shared 2-channel geometry of p.4-6 is repeated on all Si 2-channel rows.
4. mason2025 row_kind: SiN WDM 1 design (only simulated values shown, though p.9 implies it was fabricated). fab Stanford + SNF / SNSF from p.12.
5. pathak2014a fab org_imec: "we ... fabricated" (p.5) + "IMEC's passive SOI platform", as merged pathak2014 / bogaerts2006 (borderline D80b); authors also hold UC Davis / Luceda affiliations. Conflicts in the paper: 4 x 32 IL 2.1 (Table 1) vs 2.0 (text), 4 x 6.4 echelle size 700 x 420 (Table 1) vs 275 x 245 (p.6); table values entered, noted. Table 1 FSR author_estimate (origin not stated). Wavelength columns are plot-axis spans, inferred. Echelle Delay L entered as fpr_length_um from the table's "slab length" wording.
6. wijk2020 Fig. 5(b) primary losses scope unspecified (normalization is stated only for the cascade, p.5); Fig. 6(c) AWG 2 de_embedded with the primary in the path. Cascade 7 dB excess author_estimate + loss_breakdown (sum of budget terms, partly simulated), printed ">-7 dB" -> lt. The same-length reference normalization would remove the 3 dB propagation term the budget still counts: flagged in notes. Facet 7 dB and Y-coupler loss sit on fabricated rows with simulated values (the part exists; only the value is computed).
7. wijk2020 3 dB/cm author_estimate (no method). Delta-lambda = 1 nm stored as channel_spacing_nm with "spectral resolution" in condition (p.7 equates delta-lambda with channel spacing for the primary).
8. wang2023e cascade IL author_estimate + loss_breakdown (2 dB per facet subtracted, no reference structure, D428 precedent), while the facet value itself stays measured (D167); test PEG IL scope unspecified. Abstract "< -35 dB" vs body -30 to -35 dB: body entered. Journal extension of own ECOC 2022 paper, values kept (D408).
9. jia2025 drift -2.23 pm/K derived (unit, D256). Text prints 0.78 nm shift for 25-60 C, Fig. 10(a) labels 0.08 nm: only the latter gives -2.23 pm/C; printed value kept, conflict in notes. IL reference: straight waveguide de-embedding with bend loss assumed negligible, basis measured. Facet total 1.58 dB kept as a two-facet fiber_to_fiber value, not halved.

## Registry gaps (skipped value + proposed definition)

- `bw_0p5db_nm` (wdm): wijk2020 45 nm, p.1 Abstract, p.2 Sec. 1. "0.5-dB passband width in wavelength" (bw_0p5db_ghz exists only for switch_fabric, GHz).
- `noise_floor_db` (wdm): wang2023e -31 / -35 / -50 dB, p.5 Sec. IV, Fig. 9. "Average out-of-band transmission floor of a channel, positive dB, as stated." Distinct from crosstalk (same paper gives both).
