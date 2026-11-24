# lit_270 batch report

Papers: lit:samusenko2016, lit:zhuang2011, lit:chen2006a, lit:jin2017. Page-1 titles match the source rows; no garbled
text layer. Total 28 components / 165 metric rows. `merge_component_staging.py --dry-run`: +28 components,
+165 metrics, 0 errors (two pre-existing duplicate warnings on other batches: cmp_lit_guo2024a_exc02,
cmp_lit_ni2025b_pimmwc). verified_on 2026-11-24.

## lit:samusenko2016 (19 components / 119 metrics)

SiON (n 1.66) platform at 850 nm; three wafers BS1 / BS2 / BS3 (285 / 305 / 350 nm core after anneal) treated as
sibling cross-sections (one row per sample x nominal width).

- `cmp_lit_samusenko2016_wg_{bs1,bs2,bs3}_w{900,1000}` (6 x waveguide_platform.straight, sion, 7-8 metrics each):
  Table II propagation loss TE / TM (serpentine cutback fit, 0.79-1.36 dB/cm), nominal width, measured and
  as-deposited core thickness, 4 um BOX, 1 um TEOS cladding; BS3 1000 nm also the printed 350 x 950 nm width.
- `cmp_lit_samusenko2016_bends_{bs1,bs2,bs3}_w{900,1000}` (6 x waveguide_platform.bend, 3-9 metrics each): Table II
  R = 100 um bend loss TE / TM; Sec. IV.A multiple-bend values for 1000 nm TE (0.13 / 0.12 / 0.12 dB/90);
  BS3 Fig. 5 values at R = 50 / 75 / 100 um (extracted_from_figure, +/- 0.01 dB). Radius in condition (bend-series
  rows).
- `cmp_lit_samusenko2016_bend_fem_design` (waveguide_platform.bend, row_kind design, 3 metrics): simulated radiation
  loss < 1e-3 dB/90 above R = 100 um, > 1 dB/cm at R = 75 um, 300 nm design core.
- `cmp_lit_samusenko2016_dc_bs3_w1000_series` (splitter.directional_coupler, 5 metrics): 49/51 split at the 65 um
  coupling zone (measured), gap 600 nm, width, core 350 nm.
- `cmp_lit_samusenko2016_dc_bs3_w900_series` (splitter.directional_coupler, 5 metrics): Fig. 7 P1 about 0.42 at
  50 um (extracted), geometry.
- `cmp_lit_samusenko2016_ring_{bs2,bs3}_{teos,water}` (4 x resonator.ring, 7-9 metrics each): loaded Q 4.3e4 /
  4.6e4 (TEOS) and 9.5e4 / ~1.3e5 (water); intrinsic Q 4.5e5 / 3.8e5 (derived); ER 5 / 6.5 dB (water, printed) and
  ~1.8 / ~2.8 dB (TEOS, figure-read); FSR 0.67-0.70 nm range; BS3 TEOS ring 1.5 dB/cm from Eq. (5) (derived);
  R 100 um, 35 um coupling zone, 600 nm gap, measured core thickness.

Not entered: bulk sensitivity ~80 nm/RIU (BS2) / ~68 nm/RIU (BS3) and LOD ~3e-6 RIU (p.7; sensor metrics, no
parameter); fitted 3-dB coupling lengths L50/50 48 um (900 nm) and 65 um (1000 nm) for BS3 and the BS2 "18-20 %
smaller" (p.6; no parameter for a fitted 3-dB length, kept in notes); Table I calculated 3-dB coupling lengths
(design, geometry only); critical coupling lengths 22 / 35 um (design, resting on an assumed Q 5e4 and ref. [22]),
7 / 12 / 10 / 24 um (extracted, p.7; no parameter); Fig. 11 coupling-length test series (ER and Q per coupling
length; sample and cladding of the series not stated, points overlap at 0 um; only the red BS3 circuit label read);
FEM design FSR 0.7 nm (design value of the same rings, in notes); ring loss 0.1 dB / 0.4 dB estimates (p.7); TE / TM
confinement factors 59 % / 46 % and n_eff 1.513 / 1.502 (simulated, no parameter); Fig. 6 normalized transmittance
points (inputs of Table II); Fig. 7 points other than the one entered; water absorption 0.19 dB/cm and Q 6e4 of
earlier work (cited, refs. [14], [22]); ref. [28] 0.3 dB/cm (other work). VCSEL source and Si PIN detector are setup
equipment (rule 13).

Fab / facility: passive "The devices were fabricated" (p.4); acknowledgment "MNF Facility of Fondazione Bruno
Kessler, Centre for Materials and Microsystems, for device fabrication" (p.8 Acknowledgment), a stated place of
fabrication (D448). Neither org is in `organizations.csv` / `org_aliases.csv`: fab and facility left empty.

## lit:zhuang2011 (6 components / 29 metrics)

- `cmp_lit_zhuang2011_double_stripe_wg` (waveguide_platform.straight, sin, 5 metrics): 0.095 dB/cm mean over the
  six ORRs with R >= 70 um (derived, ring_extraction, 1550 nm TE), group index 1.72 (author_estimate), 1.5 um width,
  2 x 170 nm stripes, 500 nm SiO2 between (design).
- `cmp_lit_zhuang2011_orr_radius_series` (resonator.ring, 12 metrics): 0.12 dB/cm at R = 50 um (printed, derived),
  Fig. 4 points for R = 60-125 um (extracted), FSR 20 GHz (author_estimate), circumference 8783 um, radius range,
  width.
- `cmp_lit_zhuang2011_orr_mzi_coupler` (splitter.other, 1 metric): MZI extinction > 15 dB (design statement,
  author_estimate).
- `cmp_lit_zhuang2011_osbf_mzi_1ring`, `cmp_lit_zhuang2011_osbf_mzi_2ring` (wdm.interleaver, 5 metrics each): design
  FSR 6.7 GHz, stopband suppression ~25 dB read off each curve, -1 dB passband 50 % FSR = 3.35 GHz
  (author_estimate), mask footprints 0.3 x 1.5 / 0.4 x 1.5 cm, 125 um bend radius.
- `cmp_lit_zhuang2011_cleaved_facet_smf` (fiber_chip_coupler.edge, 1 metric): ~10 dB per facet to SMF
  (author_estimate, origin not stated).

Not entered: Fig. 5 transition-band labels 4.5 % / 10 % FSR (the device names on the labels contradict the curve
colours of the inset frames; D156); stopband widths 30 % / 41 % FSR (no wdm stopband parameter; tied to curves only
by arrow position); taper "in theory" 0.5 dB/facet (proposed remedy, no design, not fabricated); birefringence 0.053;
Fig. 4 theory curve; Sec. 5 beamformer chip (mask layout only: 16 inputs, 40 ORRs, 0.7 x 2.2 cm footprint, 4.5 GHz /
290 ps requirements; no performance result, so no row); 8-9 dB/m and 0.17 dB/cm of ref. [25] and other cited losses.

Fab: none. "produced using TriPleX technology" / "fabricated in the TriPleX technology [24]" (p.3) name a process,
no org; `process_name` "TriPleX technology" kept, fab empty (D433, v7). Authors at the University of Twente and
LioniX BV (affiliation only; LioniX BV has no alias to org_lionix_international, a2011 precedent). No facility.

## lit:chen2006a (1 component / 6 metrics)

- `cmp_lit_chen2006a_ddc_12ring` (wdm.other, glass, 6 metrics): fiber-to-fiber IL < 4.2 dB over 90 C-band channels
  at one set point, per-channel IL non-uniformity ~0.4 dB (Fig. 4, extracted), average clear-channel PDL 0.5 dB,
  measured FSR 49.96 GHz, 90 channels, chip 9 x 11 mm.

Not entered: dispersion tuning range -3000 to +2000 ps/nm (abstract +/- 3000 ps/nm), group-delay ripple < 5 ps
(conclusion "below 4 ps"), clear-channel bandwidth 20 GHz (no level), worst-case in-channel IL ripple (Fig. 4 right
axis), BER / Q-factor transmission results (system level), design ring FSR 50 GHz. PBS, PBC and thin-film heaters have
no separate values (no rows). The text layer of p.2-3 figures is garbled; values were taken from the text paragraphs
and the p.2 page render.

Fab: none ("is fabricated", "The PLC is fabricated from Hydex", passive; authors at Little Optics Division, Nomadics
Inc and the University of Maryland Baltimore County). No facility.

## lit:jin2017 (2 components / 11 metrics)

- `cmp_lit_jin2017_pzt_actuator` (phase_shifter.other, sin, 3 metrics): 0.5 mW at 16 V (30 uA leakage, measured);
  tuning slopes ~25 pm/V (86 um undercut) and ~21 pm/V (72 um) read off Fig. 3.
- `cmp_lit_jin2017_sin_ring_r580` (resonator.ring, sin, 8 metrics): FSR 0.412 nm (Fig. 3 label, author_estimate),
  full-FSR tuning range 0.412 nm at 16 V (derived), TM extinction ~4.5 dB (Fig. 4), R 580 um, 175 nm x 2.2 um core,
  4 um / 1.5 um oxide (Fig. 1 labels).

Not entered: v_pi_v / phase_shift_pi (results text says "pi phase shift" at 16 V, abstract / Fig. 3 / conclusion say a
full FSR; inconsistent); breakdown from ~7 V/um; simulated 20 V full-FSR tuning at 70 um undercut and ~21 %
stress-optic counteraction (COMSOL, p.2); Fig. 3 simulation curves; > 120 um undercut projection; Fig. 4
off-resonance level ~-16.5 to -17 dB (couplers not described); 300 mW thermal tuning of other work (cited).

Fab: none (passive "is fabricated"; authors at UCSB, US Army Research Laboratory, Keysight Laboratories and Morton
Photonics). No facility; acknowledgments name funding only.

## Missing orgs (fab / facility)

| name as printed | role | locator |
|---|---|---|
| Fondazione Bruno Kessler, Centre for Materials and Microsystems | fab (acknowledged as place of device fabrication, D448) | lit:samusenko2016 p.8 Acknowledgment |
| MNF Facility of Fondazione Bruno Kessler | facility | lit:samusenko2016 p.8 Acknowledgment |

## Judgment calls for the auditor

1. samusenko2016 rows split per wafer (BS1 / BS2 / BS3, different core thickness) and per nominal width; bends as
   bend-series rows with radius in condition; TEOS-covered and opened rings as separate rows (different physical
   rings of the circuit, Fig. 8(b) / Fig. 11 inset).
2. samusenko2016 q_intrinsic `derived` (not author_estimate, D403): the over-coupled regime is determined from the
   paper's own coupling-length series (Fig. 11).
3. samusenko2016 FSR range 0.67-0.70 nm entered on all four ring rows (stated jointly for the measured rings).
4. samusenko2016 TEOS-ring ERs are figure readings (BS2 from the Fig. 9 dip depth with 10log10, BS3 from the Fig. 11
   red label); 850 nm with `wavelength_inferred` for Table II values (VCSEL source).
5. zhuang2011 OSBF class `wdm.interleaver` (ring-assisted MZI half-band filter used for sideband filtering; rizzo2023
   RMZI precedent); `wdm.other` is the alternative. Stopband suppression ~25 dB read per curve; -1 dB passband
   3.35 GHz rests on the design FSR (author_estimate) and is entered on both filters.
6. zhuang2011 per-radius losses on one ORR series row (resonator.ring) and the 0.095 dB/cm average on the waveguide
   row; the 0.12 / 0.095 printed values `derived` (extraction model with an assumption, D76).
7. chen2006a class `wdm.other` and platform `glass` for Hydex (alternative `other`); IL non-uniformity read off Fig. 4.
8. jin2017 "pi phase shift" vs "full FSR" inconsistency: neither v_pi nor phase_shift entered; tuning range as the
   full FSR (derived) and figure-read pm/V slopes (field axis V/um = V for the 1 um PZT).

## Registry gaps (proposed, with the skipped value)

- `dispersion_tuning_range_ps_per_nm` (wdm): chen2006a -3000 to +2000 ps/nm (p.1); merged doerr2005 460 ps/nm also
  waiting. Definition: range of the adjustable chromatic dispersion setting as stated.
- `group_delay_ripple_ps` (wdm): chen2006a < 5 ps over the 20 GHz clear channel (p.1). Definition: peak-to-peak
  group-delay ripple over the stated passband.
- `wdl_db` for wdm (in-channel IL ripple): chen2006a worst-case IL ripple per 20 GHz channel (Fig. 4 right axis).
- `stopband_width_ghz` / transition-band width for wdm filters: zhuang2011 30 % / 41 % FSR stopbands (p.7 Fig. 5).
- `bulk_sensitivity_nm_per_riu` (resonator): samusenko2016 ~80 / ~68 nm/RIU (p.7); possibly out of component scope.
