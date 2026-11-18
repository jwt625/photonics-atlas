# lit_189 batch report

Papers: lit:guarino2007, lit:logan2018, lit:liao2024, lit:gu2020. verified_on 2026-11-18. All four cached texts match
their source rows (page-1 titles checked); none is a correction or erratum. Cached copies: guarino2007 is the arXiv v1
preprint (0705.2392) of the Nature Photonics paper, with Methods and Supplementary Information in the same file;
logan2018 is the arXiv v1 preprint (1810.06393) of the Optics Express paper; gu2020 is the arXiv v1 preprint
(1907.02186) of the APL Photonics paper; liao2024 is the published Chinese Optics Letters article (its Supplementary
Material is not cached). Values are from the cached copies; journal versions unread. Dry-run: +20 components,
+118 metrics, 0 errors (the one warning printed concerns cmp_lit_ni2025b, not this batch). Generator script:
session scratchpad `lit_189/build.py`.

## lit:guarino2007 (Nature Photonics 2007, EO-tunable LN thin-film microring)

Components 1 / metric rows 19:

| component | metrics | content |
|---|---|---|
| cmp_lit_guarino2007_ln_ring_r100 (`resonator.ring`) | 19 | FSR about 1.66 nm (plus 1.65 / 1.67 nm simulated TE / TM), finesse about 5, Q 4e3, extinction about 7 dB, loss 17.37 dB/cm (from 4 cm^-1), EO tuning 1.05 pm/V (TM), simulated group indices 2.323 / 2.286, geometry (R 100 um, w about 4 um, gap about 0.2 um, 0.6 um film, 0.4 um ridge, 0.2 um slab, 0.85 um SiO2, 2.5 um BCB) |

Not entered:
- AFM RMS surface roughness 4 nm after Ar+ smoothing (p.7): no parameter (registry gap below). In notes.
- Supp. Fig. 5 bending-loss Q vs index contrast and the R = 10 um / 16 nm FSR example (p.8-9): generic calculations,
  not this device.
- Projections (tunability > 1 GHz/V, Q 2e4, switching voltage < 10 V, 10 Gbit/s; p.6): not results.
- r33 / r13, refractive indices, eps33: cited material constants (rule 3).
- "About 50 % reduction of EO activity vs bulk" (p.5-6): a comparison, not a component parameter; in notes.

Judgment calls:
- Platform `other`: the LN film sits on BCB polymer bonded to an LN substrate, not on oxide; `lnoi_rib` would imply an
  oxide insulator. Stack in core_material.
- Fab `org_eth_zurich`: first-person fabrication ("We have improved the ... thin film fabrication technique", p.3; "we
  lithographically define the waveguides and the rings", p.4) and all five authors at one ETH Zurich laboratory (D72 /
  D80b). He+ implantation by the AIM team at the Research Center Rossendorf (acknowledgment, p.6) kept as a note
  (film-preparation step, wafer / film supplier analogue); the coordinator may rule it a D448 processing place (fab).
- 4 cm^-1 read as a power attenuation coefficient (definition not printed; sun2022 precedent D420) -> 17.37 dB/cm
  `derived`, with the field-coefficient alternative in notes; wavelength 1550-1570 nm inferred; put on the ring row
  (same ridge cross-section as the bus; the paper does not say which structure).
- EO tuning: printed 105 pm at 100 V (TM) -> 1.05 pm/V `derived`; printed 0.14 GHz/V in notes. Kept on the resonator
  row (merged precedents herrmann2022, churaev2023); the device is an EO-atlas candidate.
- Unqualified Q 4e3 -> `q_loaded` `measured` (from the measured finesse and FSR).

## lit:logan2018 (Optics Express 2018, GaP-on-oxide doubly resonant SHG rings)

Components 4 / metric rows 21:

| component | metrics | content |
|---|---|---|
| cmp_lit_logan2018_shg01 (`frequency_converter.shg`) | 7 | 175 %/W at 1523.1 nm, Q1 26 500 (TE00), Q2 13 600 (TM03, 761 nm), ring width 847 nm (SEM), 427 nm GaP, 10 um SiO2, sidewall about 85 deg |
| cmp_lit_logan2018_shg02 (`frequency_converter.shg`) | 8 | 400 %/W at 1549.1 nm, 0.84 % peak power conversion (one SHG port, up to 3 mW), Q1 40 700, Q2 16 800 (774 nm), width 847 nm, stack, sidewall |
| cmp_lit_logan2018_gc_telecom (`fiber_chip_coupler.grating`) | 3 | design 33 %, 22 % at 1523 nm (SHG01 circuit), 19 % at 1549 nm (SHG02 circuit) |
| cmp_lit_logan2018_gc_shg (`fiber_chip_coupler.grating`) | 3 | design 24 %, 3.2 % at 761 nm, 7.5 % at 774 nm |

Not entered:
- Ring radius 7.14 um (design, p.3): `radius_um` is not allowed on frequency_converter (registry gap; D553 listed the
  same gap). In notes.
- On-resonance transmissions T1 / T2 (Table 1: 0.44 / 0.50 SHG01, 0.81 / 0.52 SHG02): no transmission / extinction
  parameter on frequency_converter (registry gap). In notes.
- SEM coupling-region dimensions per device (App. B Fig. 1 table, p.9: telecom / SHG bus widths, ring widths, gaps,
  min-max): `gap_nm` / `bus_width_nm` not allowed on frequency_converter (registry gap). In notes by reference.
- Designed and simulated coupling Q (Q1c about 2e5, Q2c about 2e4; App. B ranges 1.5e5-5e5 / 1.2e3-1e6): no
  q_external on frequency_converter, and the paper cannot settle the regime; no q_intrinsic (D403). In notes.
- Theory efficiencies 230 / 425 %/W (overcoupled assumption) and the > 8000 %/W projection (p.7-8): model values; in
  notes. Temperature acceptance FWHM about 4 C (Fig. 4(a)): no parameter. Nonlinear overlap beta 1.43e-4: design value,
  no parameter.
- Wrap angles 51 / 44 deg: no parameter; in notes.

Judgment calls:
- SHG efficiencies 175 / 400 %/W and 0.84 % `author_estimate`: the on-chip powers rest on grating efficiencies computed
  with an assumption of identical input / output gratings and negligible on-chip loss (p.5, App. A; D462 / D514).
- Grating efficiencies `loopback_half` + `derived` (single-grating value from a two-grating circuit, D542 / D554);
  design efficiencies `author_estimate` ("designed for", not said simulated, D82a). The gratings couple to a microscope
  objective, not a fiber (class kept as fiber_chip_coupler.grating, noted). Polarization TE / TM from App. A.
- Q2 wavelengths 761 / 774 nm = the experimental resonances printed with the near-infrared grating efficiencies (p.5).
- Ring width 847 nm `measured` (Table 1, SEM, uncertainty = measured range); the 840 nm final design and the 839-847 nm
  array in notes.
- Fab empty: passive fabrication sentences and authors at four unrelated orgs (D80b). The membrane-transfer process and
  the MBE growth are described without an org.

## lit:liao2024 (Chinese Optics Letters 2024, inverse-designed mode splitter)

Components 3 / metric rows 45:

| component | metrics | content |
|---|---|---|
| cmp_lit_liao2024_mode_splitter (`mode_converter.mdm_mux`) | 27 | measured IL < 0.6 / < 0.9 dB and CT > 17 / > 16 dB (TE0 / TE1, 1500-1600 nm); simulated 1550 nm and band values; simulated +/-20 nm width-tolerance bounds; footprint 35 um2, length 14 um, W1 / W2 / W3 widths, 3 um taper, ports, 220 nm / 2 um / 1 um stack |
| cmp_lit_liao2024_mode_demux (`mode_converter.mdm_mux`) | 17 | measured IL < 1 dB, CT > 23 dB (TE0 and TE1); simulated 1550 nm, band and tolerance values; outputs, stack |
| cmp_lit_liao2024_gc_te (`fiber_chip_coupler.grating`) | 1 | 5 dB/facet (origin not stated) |

Not entered:
- Table 1 rows of refs. [13]-[17]: other works (rule 3). The "this work" row repeats the measured bounds.
- ADC-based mode (de)MUX of the test circuit (ref. [20] design): no value reported for it (its loss is deducted).
- Mode (de)MUX footprint and boundary coordinates: only in the uncached Supplementary Material (Fig. S1, Table S1).

Judgment calls:
- Mode splitter classed `mode_converter.mdm_mux` (merged yu2025 mode-splitter precedent).
- Measured IL `measured`, scope `per_component`, method `reference_structure`, `excludes` the GCs and the ADC test
  circuitry (back-to-back ADC reference deducted; no subtracted numbers printed).
- Widths stored with the role in `condition` (input W1, Port-1 W2 = taper end, Port-2 W3) rather than `port_width_um`
  (the 3 um Port-1 taper starts at 1 um at the optimization region; never guess which width).
- Tolerance bounds stated once for TE0 and TE1 inputs -> one row each with mode "TE0;TE1".
- GC 5 dB/facet `author_estimate` (origin not stated; velha2016 precedent), wavelength 1500-1600 nm inferred.
- Fab and process_name empty (passive "are fabricated on a standard SOI platform", 193 nm DUV + ICP, no org; Contract v7).

## lit:gu2020 (APL Photonics 2020, air-hole-enabled Fano lineshapes in a microring)

Components 12 / metric rows 33:

| component | metrics | content |
|---|---|---|
| cmp_lit_gu2020_ring_airhole_d300 (`resonator.ring`) | 9 | ER > 20 dB (best, 1599.03 nm), Q about 31 000 (Fano fit), FSR about 3 nm, R 30 um, 500 nm ring / bus, 120 nm gap, 220 nm / 2 um stack |
| cmp_lit_gu2020_ring_control (`resonator.ring`, test structure) | 8 | Q > 35 000, FSR about 3 nm, same geometry |
| cmp_lit_gu2020_airhole_d180 ... d480 (`phase_shifter.other`, 6 rows) | 12 | phase shift 0.01 / 0.12 / 0.24 / 0.37 / 0.50 / 0.63 pi (Fig. 5(b) labels); insertion loss 0.35 / 2.36 / 3.49 dB (Fig. 5(c) reads), about 5 dB (360 nm, printed), > 10 dB (480 nm, printed) |
| cmp_lit_gu2020_airhole_d300_dl0p0 ... dl2p5 (`phase_shifter.other`, 4 rows) | 4 | phase shift 0.30 / 0.28 / 0.24 / 0.0 pi for hole offsets 0.0 / 0.5 / 1.5 / 2.5 um (Fig. 4(b) labels) |

Not entered:
- Fano slope rates 404.9 dB/nm (air-hole device) and about 100 dB/nm (control) (p.3): no parameter (registry gap).
- Fano asymmetry q values (p.3, Figs. 4(b), 5(b)): no parameter; in notes.
- Air-hole diameters 180-480 nm: no hole-diameter parameter (registry gap); in labels and core_material.
- Model spectra of Figs. 1 and 2 (t = a = 0.95, Delta phi = pi / 3): illustrations.

Judgment calls:
- The air-hole is characterized as a passive phase shifter of the bus mode with its insertion loss, so the diameter and
  location siblings are `phase_shifter.other` rows (rule 9: one row per design). Phase shifts are Eq. (4) fit
  parameters with a stated lossless-coupling assumption -> `derived` (D80a).
- Fig. 5 diameter series and Fig. 4 location series kept apart: the Fig. 5 series does not state the hole position,
  and its d = 300 nm value (0.24 pi) differs from the Fig. 4 mid-plane value (0.30 pi); the Fig. 3 headline device
  (q about -1) matches the Fig. 4 Delta l = 0 labels, identity not stated (cross-notes, D159 not triggered: each value
  has a clear device).
- Fig. 5(c) losses read from the PDF vector data (marker centres against the 0 / -10 dB ticks, about +/-0.1 dB):
  `extracted_from_figure` for 180 / 240 / 300 / 420 nm; 360 nm and 480 nm keep the printed "about 5 dB" and "> 10 dB"
  (`measured`); the 480 nm marker reads 9.7 dB, below the printed bound (D417 note). Wavelength 1547-1555 nm inferred
  (Fig. 5(a) window; none printed with the losses).
- Unqualified Q -> `q_loaded`; the fitted resonance of the 31 000 value is not identified (range 1540-1600 nm).
- Control FSR row from "the resonant wavelengths and FSR are the same" (p.3).
- Fab empty: "we fabricate" with authors at three unrelated orgs (D154). Platform `soi` (etch depth not stated).

## Missing fab / facility orgs

- Washington Nanofabrication Facility (facility; logan2018 p.10 acknowledgment, "Part of this work was conducted at");
  would go on all 4 logan2018 rows. Already queued in earlier rounds (D420, D579, D586, D597).
- Research Center Rossendorf (printed name; former name of `org_helmholtz_zentrum_dresden_rossendorf`; alias missing):
  He+ implantation of the guarino2007 LN wafers (p.6). Note only in this batch; fab only if the coordinator rules the
  implantation a D448 processing step.

## Registry gaps (skipped value + locator + proposed definition)

- `rms_roughness_nm` (any class): guarino2007 AFM RMS film roughness 4 nm (p.7). "RMS surface / sidewall roughness as
  measured (method and surface in condition)". Candidate already listed in D432 / D434.
- frequency_converter allowances: `radius_um` (logan2018 7.14 um, p.3; D553), `extinction_db` or an on-resonance
  transmission parameter (Table 1 T1 / T2), `gap_nm` and `bus_width_nm` (App. B Fig. 1 table, p.9), `q_external`
  (designed Q1c / Q2c, p.3).
- `slope_rate_db_per_nm` (resonator): gu2020 404.9 dB/nm at 1599.03 nm and about 100 dB/nm (control), p.3. "Maximum
  transmission slope of a resonance lineshape (Fano / Lorentzian) as stated".
- `hole_diameter_nm` on phase_shifter (and resonator): gu2020 air-hole diameters 180-480 nm, p.3-5 (candidate already
  listed in D430 / D431 for other classes).
- `temperature_acceptance_c` (frequency_converter): logan2018 about 4 C FWHM of the efficiency vs stage temperature,
  p.6. "FWHM of the conversion efficiency vs temperature".
