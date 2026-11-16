# lit_136 batch report

Distilled 2026-11-15 (verified_on). Papers: stokowski2023, kim2021a, bonneville2020, vu2010, zhou2021a (amplifier /
frequency_converter / nonreciprocal family, benchmark-citation round D577). Totals: 21 components, 90 metric rows.
`merge_component_staging.py data/_staging/components/lit_136 --dry-run`: +21 components, +90 metrics, 0 errors, no
warnings on lit_136 rows. Privacy grep of both CSVs (e-mail, street, P.O. box, local paths): clean.

Page-1 identity: all five texts match their source rows. stokowski2023, kim2021a and zhou2021a are arXiv v1
preprints of the journal papers (same title words; journal versions unread, D430 / D433). No correction / erratum.

## stokowski2023 (4 components / 16 metrics)

- `ppln_diag_shg_8p1mm` (frequency_converter.shg, test structure): ~1000 %/W/cm2 measured (linear fit of on-chip SH
  vs on-chip FH, Fig. 2(d)), 4000 %/W/cm2 simulated ideal, length 8.1 mm, poling ~3.7 um, width / film / etch.
- `dc_fh_sh_filter` (wdm.other): three cascaded directional couplers as FH / SH dichroic filter; extinction ~18 dB
  author_estimate (from the fitted 4.0 % FH leakage, arithmetic not shown).
- `rib_waveguide` (waveguide_platform.straight): ~0.7 dB/cm author_estimate (ring Q, ng and wavelength not printed,
  D76; C band inferred), full cross-section.
- `lensed_mmf_output_facet` (fiber_chip_coupler.edge): 5.40 dB per facet (Table I, coupling test to a straight
  waveguide), measured, method unspecified (D167).
- Not entered: EO phase modulators / MZIs (LO phase shifter Vpi 28.6 +/- 0.3 V fitted, tunable splitter 47 V bias,
  2.5 mm electrodes, 1.6 um gap, simulated VpiL and metal loss) -> EO-atlas candidate (stokowski2023 is not in the EO
  atlas). Squeezing 2.7 +/- 0.2 % measured, 1.5 +/- 0.1 dB on-chip estimate, anti-squeezing 12.3 %, SNR improvement
  4 +/- 1 % (no parameter). Device SHG estimate 3.4 mW SH from 18.4 mW FH (estimate; no converter output-power
  parameter). Table I waveguide 0.80 dB (path length not printed; note only), detector QE 0.80 dB and RF 1.22 dB
  (setup). Fig. 2(c) phase-matching peak near 1545 nm (no centre-wavelength parameter on frequency_converter). Fig. 6
  projections (model).
- Fab / facility: org_stanford_university (author contributions name the three fabricators, all Stanford; Methods
  first person); org_stanford_nano_shared_facilities + org_stanford_nanofabrication_facility (p.6 "performed at";
  pre-merger, D80d). NanoLN wafer supplier in notes.
- Judgment calls: (1) efficiency kept `measured` following the audited same-group stokowski2024 test-waveguide row
  although the on-chip power referencing is not described (D460 franken2025 would argue author_estimate). (2) Filter
  classed wdm.other (band multiplexer of FH / SH).

## kim2021a (2 components / 6 metrics)

- `aln_synthetic_hall_isolator` (nonreciprocal.isolator): maximum forward / backward contrast ~3 dB at ~1550 nm,
  TE00, 1.25 GHz / 16 dBm drive, modulation depth ~2.5 GHz, measured.
- `aln_coupled_racetracks` (resonator.coupled_rings, D396 twin): Q_loaded ~50,000 (fit), ridge 1.2 um, bus 1.1 um,
  AlN 350 nm, 200 nm trench.
- Not entered: inter-resonator coupling rate lambda ~1.9 GHz (not the supermode splitting; registry gap), IDT S11
  dips (RF), Fig. 5(c) projected contrast (model), normalized transmissions (no IL printed).
- Fab: org_university_of_illinois_urbana_champaign ("we fabricate", p.6; all authors UIUC, D72). No facility (the
  arXiv text has no acknowledgements). Platform `other` (suspended AlN; sohn2018 precedent).
- Judgment call: classed `nonreciprocal.isolator` by function (two-port transmission contrast, otterstrom2019 /
  sohn2021 precedents) although the paper calls it a non-reciprocal device; `nonreciprocal.other` is the alternative.

## bonneville2020 (7 components / 32 metrics)

- `edwa_film3_3cm` (amplifier.rare_earth): internal net gain 4.3 dB at 1533 nm, 1.4 dB/cm, figure reads 3.2 dB
  (1550) / 1.8 dB (1570) at ~190 mW, positive gain up to ~-8.5 dBm launched signal (psat_in_dbm, 0-dB definition as
  cai2021), geometry. All gain rows author_estimate: they rest on the 0.5 +/- 0.3 dB/cm loss estimate and the
  estimated -4.5 dB facet loss.
- `wg_film3` (waveguide_platform.straight): 0.5 +/- 0.3 dB/cm at 1640 nm author_estimate (bounded estimate).
- `ring_r3000_film2` (resonator.ring): Q 2.6e5 TE / 2.5e5 TM as q_intrinsic author_estimate (text: fits extract the
  internal Q; regime sweep data not shown, D403), 0.9 / 1.0 dB/cm, FSR 92 / 82 pm, R 3000 um, 3.0 um mask gap.
- `cleaved_facet` (fiber_chip_coupler.edge): 4.5 dB per facet author_estimate, wavelength unspecified.
- `film1_slab`, `film2_slab`, `film3_slab` (waveguide_platform.other, prism-coupled planar films): 847 nm film loss
  (measured) and 1550 nm "background" loss (author_estimate: separation from Er absorption not described); Film 1 also
  1070 nm thickness and fitted background 2.3 / 0.6 dB/cm at 980 / 1550 nm (cited cross sections, author_estimate;
  0.6 vs 0.4 conflict noted, D417).
- Not entered: Er / Yb concentrations (notes), etch rate 27 nm/min, simulated min bend radius ~2.4 mm, refractive
  indices, Fig. 3 absorption spectra.
- Missing orgs: McMaster University (fab, all 7 rows; first-person fabrication p.2-5, all authors McMaster) - fab left
  empty until the org round. CEDT, McMaster University (p.10: staff thanked for assistance with fabrication; staff
  thanks, not entered as facility, D84b). Western University Tandetron facility (p.3: RBS of calibration films;
  characterization only, not entered; listed for the coordinator).
- Judgment calls: film slabs entered as waveguide_platform.other (D428 slab precedent); unqualified Fig. 4 Q labels
  entered as q_intrinsic because the text names the internal Q.

## vu2010 (4 components / 18 metrics)

- `er_teo2_amp_5cm` (amplifier.rare_earth): peak internal gain 14 dB at 1530 nm and 2.8 dB/cm (derived, D166), 3-dB
  width ~40 nm, gain span > 110 nm (1520-1630 nm, derived from the printed bounds), saturation input 0.4 mW = -4.0 dBm
  and output > 10 dBm (author_estimate: in-waveguide powers / plane not stated), geometry.
- `er_teo2_rib_5cm` (waveguide_platform.straight): 6 dB fiber-to-fiber at 1400 nm (measured), ~0.6 dB/cm background
  (author_estimate, loss_breakdown), PDL 0.3 dB (author_estimate: sentence cites ref. [12], width tie unclear).
- `er_teo2_rib_7cm_2p7pct` (waveguide_platform.straight): minimum IL ~2.5 dB (scope unspecified; wavelength span of
  the minimum read from Fig. 2, inferred), width 3.5 um, length 7 cm.
- `lensed_fiber_facets` (fiber_chip_coupler.edge): 3 dB two-facet mode overlap / reflection (scope fiber_to_fiber with
  includes / excludes, feyisa2022 precedent), author_estimate.
- Not entered: lifetimes (Table 1, Fig. 4-5; 1.3 ms gain film) - no parameter; 1290 nm OH dip 0.02 dB/cm (absorption
  feature, not a propagation loss); net fiber-to-fiber gain (no number printed); lensed fiber 2.5 dB and WDM 2.1 dB
  (setup); model gain curves and 35 dB 980 nm-pump prediction; amplifier width (the 2 um single-mode width is not tied
  explicitly to the 5 cm amplifier).
- Fab empty (passive / design sentences, two ANU authors, D80b); no facility. Platform `other` (tellurite).
- Registry gap: `lit:vu2010` title prints "28dB/cm"; page 1 prints "2.8dB/cm" (decimal point lost) - fix the
  registry title.

## zhou2021a (4 components / 18 metrics)

- `er_tfln_spiral_amp_3p6cm` (amplifier.rare_earth): ~18 dB internal net gain at 1530 nm (~40 mW pump) and ~5 dB/cm
  (derived), figure reads 7.3 dB at 1550 nm (Fig. 4(d)) and 12.9 dB at 1545 nm (Fig. 6, 20 mW), > 40 nm net-gain
  bandwidth, printed > 40 nm 3-dB bandwidth kept with a conflict note (Fig. 6 does not support it, D417), geometry.
- `er_tfln_microring_d400` (resonator.ring): Q_L ~2.6e6 at 1554.13 nm, FSR ~0.8 nm, ng 2.4 (derived), 0.16 dB/cm
  (derived from the loaded Q), R 200 um.
- `er_tfln_straight_wg_300um` (waveguide_platform.straight): 6.28 dB/cm around 980 nm from upconversion-fluorescence
  decay (derived; proportionality assumption stated).
- `lensed_fiber_facet` (fiber_chip_coupler.edge): 10 dB (980 nm) and 7.3 dB (1550 nm) per facet, author_estimate
  (equal-facet assumption stated, D462 / D514).
- Not entered: min bend radius 800 um (no amplifier parameter; in notes), bottom width ~4 um (no parameter; in
  notes), Fig. 5 gain vs signal (no saturation value printed), Er 1 mol%.
- Fab empty (passive "was fabricated using PLACE", multi-institution authors, D80b); no facility.
- Judgment call: platform `lnoi_strip` from Fig. 1(d) SEM / Fig. 1(e) geometry (no slab visible); the text does not
  state the etch depth (merged li2025 PLACE rows use lnoi_rib). Fig. 4(b) (~15 dB near 20 mW at 1530 nm) vs Fig. 6
  (11.6 dB at 1530 nm, 20 mW) inconsistency noted on the amplifier row.

## Registry gaps (skipped value + locator + proposed definition)

1. `squeezing_db` / `squeezing_pct` (frequency_converter): stokowski2023 2.7 +/- 0.2 % measured, 1.5 +/- 0.1 dB on-chip
   estimated (p.5) - quadrature-noise reduction below shot noise, detection efficiency in condition.
2. `coupling_rate_ghz` (resonator.coupled_rings): kim2021a lambda ~1.9 GHz (p.8 Fig. 4(c)) - inter-resonator coupling
   rate as fitted (not the supermode splitting).
3. `upper_state_lifetime_us` (amplifier; D429 candidate): vu2010 1.3 ms gain film, Table 1 0.19-0.56 ms (p.6-7).
4. `output_power_mw` / SH output power on frequency_converter: stokowski2023 ~3.4 mW SH (estimate, p.5).
5. `center_wavelength_nm` on frequency_converter (D419 widening not yet in the registry): stokowski2023 Fig. 2(c) peak
   ~1545 nm.
6. `min_bend_radius_um` on amplifier: zhou2021a 800 um spiral (p.2).
