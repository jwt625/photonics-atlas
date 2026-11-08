# cov_05 batch report (2026-11-07)

All eight cached texts match their source rows (page-1 title); none is another paper, a correction or an erratum.
None of the eight sources had rows in `data/components/components.csv` before this batch. Dry-run: +29 components,
+143 metrics, 0 errors (the one warning, ni2025b m18 / m4, is an existing merged row, not this batch).

| paper | components | metrics |
|---|---|---|
| chen2025a | 3 (amplifier.parametric; frequency_converter.shg; waveguide_platform.straight) | 21 |
| dean2025 | 9 (amplifier.parametric: 2; frequency_converter.shg: 2; wdm.other; waveguide_platform.straight; resonator.ring; resonator.other; fiber_chip_coupler.edge) | 40 |
| hazan2022 | 4 (amplifier.soa: 2; laser.other; fiber_chip_coupler.edge) | 14 |
| kashiwazaki2021 | 0 (see below) | 0 |
| kashiwazaki2021a | 3 (frequency_converter.shg; waveguide_platform.straight; amplifier.parametric) | 14 |
| li2025d | 5 (frequency_converter.sfg_dfg; frequency_converter.shg; wdm.other; waveguide_platform.straight; fiber_chip_coupler.edge) | 22 |
| stokowski2024 | 4 (frequency_converter.other; laser.comb; frequency_converter.shg; resonator.ring) | 26 |
| xin2024 | 1 (frequency_converter.shg) | 6 |

Text layers: li2025d is flagged garbled on p.5 only; that page's text layer holds figure labels, its prose is clean.
All li2025d values come from clean prose (p.2-6) and the p.4 render (Fig. 2 legend: the 20% absolute SHG point is
PPLN2). dean2025 Table I (p.6) was read from the page render (text layer drops the numbers). xin2024 has stray
bytes (read with `LC_ALL=C`). Versions: dean2025 and xin2024 are arXiv preprint texts (xin2024 row carries the
Communications Physics DOI; journal version unread). D411: all parts are chip-scale waveguide devices or
fiber-coupled modules; no bulk-crystal part entered.

## Fab / facility orgs

| paper | fab_org_ids | facility_org_ids | basis |
|---|---|---|---|
| chen2025a | - | - | 'We fabricate' (p.2), authors at six institutions, no named fabricator (D80b) |
| dean2025 | org_stanford_university | org_stanford_nano_shared_facilities; org_stanford_nanofabrication_facility | T.P. fabricated (p.15, D395); SNSF + SNF 'performed at' (p.15; 2025, pre-merger) |
| hazan2022 | org_smart_photonics | - | test structures 'fabricated by Smart Photonics' (p.3) |
| kashiwazaki2021a | - | - | 'we fabricated', NTT + UTokyo + RIKEN authors (D80b) |
| li2025d | - | - | 'We fabricate', CityU + Sun Yat-sen authors (D80b) |
| stokowski2024 | org_stanford_university | org_stanford_nano_shared_facilities | H.S.S., T.P., A.Y.H. fabricated (p.9, D395); SNSF (p.9) |
| xin2024 | org_harvard_university | org_center_for_nanoscale_systems | A.S., S.L., J.Y. fabricated (p.5; A.S. also DRS Daylight Solutions); CNS 'performed at' (p.5) |

Wafer / film suppliers kept as notes: NanoLN / NANOLN (dean2025, li2025d, stokowski2024, xin2024). No missing
registry org was needed.

## Not entered, and why

kashiwazaki2021 (NTT Technical Review overview)
- Every value reproduces the authors' earlier work (D259 / D408): Fig. 1(d) SHG 1200 %/W cites [9] (APL Photonics
  2020); Fig. 3 PSA (32.3 dB external gain at 1.35 W, 2.0 dB IL) cites [18] (NLO 2019); module section (0.5 / 0.7 dB
  coupling per side, 2.0 / 2.3 dB module IL, p.2-3) is introduced with [17] (JQE 2020); squeezing figures cite [8] /
  [9]. No component row. See question 1.

chen2025a
- Normalized gain 0.78 dB/(W mm), OSNR > 28 dB, idler within 0.2 dB of signal, BER / sensitivity of the module test,
  beta2 ~0.28 ps2/m (simulated): no parameter or link metrics.
- Edge coupler (double-layer inverse taper under SiO2): only the 4.1 dB fiber-to-fiber waveguide loss is printed;
  entered on the OPA row (scope fiber_to_fiber), no coupler row.
- 10-dB bandwidth: entered as gain_bandwidth_nm 110 (p.2); p.6 says 'over 100 nm'. The criterion (within 10 dB of
  the peak) is read from the Fig. 3(d) arrow.
- Thickness map (sub-10 nm centre, ~2 nm RMS along a centimetre): wafer metrology, no parameter.

dean2025
- FH pump suppression 26 dB (two couplers) / 52 dB (other device): amplifier has no suppression parameter; in notes.
- Facet reflectivity ~9% (transmission-ripple fit): chip-internal, not a fiber back-reflection; note only.
- Round-trip SH loss 0.3, 6x SH power enhancement, g/alpha ratios, projected curves: no parameter or projections.
- The L = 6 mm OPA of Fig. 6 and the L = 6 mm SHG device of Fig. 2 are not stated to be the same (D159): two rows.
- Phase-insensitive NF: 'quantum limited' across most of 1520-1630 nm, no number printed.

hazan2022
- T0 75 K / T1 294 K are fitted to transparency current density and internal efficiency across many lasers, not to
  one laser's threshold current: characteristic_temperature_k not used (question 3).
- Threshold current density (350 A/cm2), transparency density (140 / 310 A/cm2), internal loss (5-16 /cm), model
  parameters (eta_i, N0, J0, FCA): no parameter.
- Ridge width of the 600 um SOA and of the modal-gain series not printed for those devices (2 um is the platform's
  single-mode width, p.2): not entered.
- 2.5 W in the conclusion (p.10) vs 1.25 W single-facet in the results: no basis stated, not entered.
- PL peak 1290 nm, 70 nm 3-dB width (wafer photoluminescence): material, not a component metric.

kashiwazaki2021a
- Squeezing levels (6.4 dB, 6.3 dB at 6 THz sideband, 10.3 dB estimated): no parameter.
- OPA2 gain 20 dB: OPA2 is 'another PPLN waveguide module', identity with this design not stated (D159).

li2025d
- AOWC 3-dB conversion bandwidth 110 nm (estimate by reciprocity), crosstalk suppression 25 dB, signal-to-crosstalk
  40 dB vs < 11 dB: frequency_converter has no bandwidth / crosstalk parameter (question 4).
- SH port contrast -7 dB through one ADC: port ratio, not an extinction or loss definition; note.
- Simulated 96% ADC telecom coupling efficiency: no wdm efficiency parameter; note.

stokowski2024
- On-chip SHG pump waveguide: '140 mW FH -> about 100 mW SH' has no stated origin; no row for the pump SHG.
- Dispersion zeta2, g, EO coupling M0, escape efficiency 0.36: no parameter (notes).
- EO phase modulator inside the cavity: only M0 (no Vpi / bandwidth); not entered.

xin2024
- Wavelength-accuracy yields (73% of 84 within 737 +/- 5 nm; ~96% within thermal range), 12.1 nm thermal red shift,
  ~50 nm / > 100 nm cladding trimming: no frequency_converter parameter (question 5).
- Wafer A (periodic) design: no registry metric, so no row (rule 9). Conversion efficiency not reported.

## Judgment calls

- Classes follow merged precedent: OPA gain -> amplifier.parametric; wavelength converter -> frequency_converter.
  sfg_dfg with conversion in dB stored as % (abe2025); OPO -> frequency_converter.other (ji2017). stokowski2024
  also gets a laser.comb row (D396) because pump_to_comb_efficiency_pct, n_channels and channel spacing exist only
  for laser (question 2).
- Dichroic directional couplers (dean2025) and the cascaded ADC multiplexer (li2025d) are band (FH / SH)
  multiplexers: wdm.other.
- Efficiencies equated with pump depletion (chen2025a ~90% SHG, stokowski2024 93% internal / 34% total) are
  author_estimate (the depletion is measured; the equality is an assumption).
- kashiwazaki2021a platform `other` (bonded ZnO:LN ridge on LiTaO3, no enum value); the module row is
  amplifier.parametric with only insertion loss (no OPA1 gain printed).
- dean2025 gain values: Table I labels 17.36 / 23.63 dB as on-off gain while text and Fig. 3(c) say on-chip net
  gain; entered with Table I values and a note.
- hazan2022 Pin,sat: text range 0.5-2 mW entered; Fig. 11(c) points span about 0.9-2.3 mW (noted).
- stokowski2024 q_intrinsic 1.6e6 (Table) is author_estimate (D403; coupling regime of the FM-OPO cavity not
  shown); the 2 mm snail test resonator's Qi 2.5e6 is measured (regime determined across 1500-1580 nm).

## Questions for the coordinator

1. kashiwazaki2021 (NTT Technical Review overview): drop all values as reproduced own work (D259 / D408), as done
   here, or keep the module coupling / IL numbers (0.5 / 0.7 dB per side, 2.0 / 2.3 dB) that the text does not
   attach to a specific reference? Recommendation: keep dropped.
2. stokowski2024: keep the D396 laser.comb row for the FM-OPO comb (pump-to-comb 34%, ~200 lines, 5.8 GHz, 11 mW),
   or allow these parameters on frequency_converter and drop the laser row? Recommendation: keep.
3. hazan2022: should characteristic_temperature_k accept a T0 fitted to transparency current density (definition in
   condition), or stay threshold-only? Recommendation: threshold-only (as done).
4. Registry gap, frequency_converter: conversion / phase-matching bandwidth (li2025d 110 nm 3-dB; also SHG
   acceptance bandwidths generally) and crosstalk (li2025d 25 dB suppression, 40 dB signal-to-crosstalk). Proposed:
   allow bw_3db_nm and crosstalk_db for frequency_converter (definition in condition).
5. Registry gap, frequency_converter: wavelength accuracy / spread (xin2024 73% within +/- 5 nm) and tuning range
   (xin2024 12.1 nm thermal, > 100 nm trimming; akin2024 precedent). Proposed: allow wavelength_spread_nm and
   tuning_range_nm for frequency_converter.
6. Registry gap, amplifier: pump suppression of an integrated parametric amplifier (dean2025 26 / 52 dB) and
   length- and power-normalized gain (chen2025a 0.78 dB/(W mm); chang2026 precedent). Proposed:
   pump_suppression_db and gain_db_per_w_mm for amplifier.parametric.
7. Registry gap, conversion efficiency in dB (li2025d -15.6 / -25.6 dB stored as 2.754 / 0.2754 %): add a
   conversion_efficiency_db parameter for frequency_converter so the printed dB value is kept?
