# lit_235 batch report

Distilled 2026-11-20. Papers: lit:bimberg2009, lit:juodawlkis2009, lit:park2007b, lit:resan2005, lit:kim2004. Page-1
titles match the source rows. Totals: 8 components, 51 metric rows. `merge_component_staging.py --dry-run`: 0 errors
(the one warning, cmp_lit_ni2025b_pimmwc-m18, is a merged row outside this batch).

| paper | components | metrics |
|---|---|---|
| bimberg2009 | 4 | 23 |
| juodawlkis2009 | 2 | 15 |
| park2007b | 2 | 13 |
| resan2005 | 0 | 0 |
| kim2004 | 0 | 0 |

## bimberg2009 (ICTON 2009, p-doped vs undoped 1.3 um QD SOAs)

Rows: p-doped 2 mm SOA (8), undoped 3 mm SOA (7), p-doped 4 mm SOA (7), facet of the 4 mm device
(`fiber_chip_coupler.edge`, 1). Platform `gaas` (InGaAs/GaAs QDs in an AlGaAs/GaAs laser structure).

- Fiber-to-fiber gains `measured` (13 / 14.5 / up to 26 dB); chip gains 22 / 23.5 / 35 dB `author_estimate` (4.5 dB per
  facet stated only for the 4 mm devices, origin not stated; D437 / D462).
- XGM small-signal bandwidths as `bw3db_ghz` (first use on `amplifier`; the -3 dB level is drawn in Fig. 4(b), p.3):
  undoped > 40 GHz at 4.38 kA/cm2, p-doped 25-30 GHz at 4.38 kA/cm2 and > 40 GHz at 6.25 kA/cm2, 4 mm about 40 GHz at
  550-700 mA. 40 GHz is the network-analyzer limit (p.2).
- p-doped NF 9 dB `derived` (printed only as "10 dB ... is 1 dB larger than for the p-doped ones").
- Psat 15 (le) / 12 dBm: compression level and reference plane not stated (noted); 4 mm 3-dB Psat in fiber 8 dBm.
- Static wavelengths inferred from the stated peak-gain / peak-emission wavelengths (1310 / 1290 nm, p.1 Sec. 2).
- Not entered: gain per length 10 / 7 dB/mm (p.1 Abstract, p.1 Sec. 3.1; sample identity not stated, the 2 / 3 mm
  lengths were chosen from it: D159 / D254, in component notes); ASE spectra (Fig. 1); AR reflectivity R < 1e-3, gain
  ripple < 0.3 dB, 8 deg tilt (no parameter); 4.38 / 6.25 kA/cm2 current densities stay in conditions.
- Printed conflict: text cites "Fig. 4" for the 6.25 kA/cm2 XGM traces (p.2-3); they are Fig. 3 (noted).
- Fab: SOA processing passive, no org (D80b). Acknowledgment thanks two staff of "FhG Heinrich-Hertz-Institute,
  Berlin" for assistance with the AR coating (p.4): entered as borderline fab `org_fraunhofer_heinrich_hertz_institute`
  on the facet row only (D84b, per-component fab, Contract v7). Facility: none.

## juodawlkis2009 (IEEE PTL 2009, packaged SCOWA)

Rows: packaged SCOWA `amplifier.soa` (10), SCOWA facet to lensed SMF-28 `fiber_chip_coupler.edge` (5). Platform `inp`.

- Packaged values with `ref_plane module` (starnault2024 packaged-SOA precedent): G0 13.8 dB at 1540 nm, peak 14.9 dB
  at 1500 nm, 3-dB gain bandwidth > 100 nm, 3-dB Psat 29 dBm (printed 0.8 W / +29 dBm), Pmax 29.7 dBm (printed
  0.93 W / +29.7 dBm), NF 5.5 dB (5 A) / 4.6 dB (2 A) at 1540 nm, NF 6.7-7.5 dB at shorter wavelengths (1460 nm
  inferred from Fig. 4, read). Baseplate 16 C.
- Coupler: coupling efficiency about 90 % and about 0.5 dB per facet `author_estimate` (rests on the pre-packaging
  0.9 W in a sentence citing the authors' ref. [12]; D429 precedent); 1/e^2 near-field widths 5.6 / 7.5 um
  `measured`; lensed-fiber spot size 6.5 um `specification` (diameter vs radius not stated, noted).
- Geometry: length 10 mm, InGaAsP waveguide 5 um (`derived`, D157).
- Not entered: 11 % electrical-to-optical conversion efficiency at Pmax (no amplifier wall-plug parameter; registry
  gap below); TE/TM gain ratio 17-18 dB (registry gap); confinement factor 0.5 % (calculated; candidate); several
  hundred hours without degradation; pre-packaging Psat 0.9 W (cites ref. [12], D259 / D80i); bench-top 0.63 W / 12 dB,
  alpha_i about 0.5 cm-1, Gamma 0.3-0.5 % (authors' ref. [10], rule 3); other groups' Psat values (refs. [8], [9]).
- Fab empty: "The device fabrication was similar to that described in [10]" and packaging are passive; all authors
  MIT Lincoln Laboratory (D80b). Facility: none.

## park2007b (OFC 2007 OTuD2, hybrid Si evanescent amplifier)

Rows: hybrid SOA `amplifier.soa` (12), angled AR-coated facet `fiber_chip_coupler.edge` (1). Same device and figures
as merged lit:park2007 (IEEE PTL 2007, D583); rows built from this text only and mirror the merged precedent.

- Fiber-to-fiber gain 3 dB and NF 10-13 dB `measured`; chip gain 13 dB, chip Psat 11 dBm, internal NF 5-8 dB and the
  5 dB per-facet coupling loss `author_estimate` (this text prints neither the total insertion loss nor its split;
  D437 / D462 / D583); Psat 11 dBm also lies just past the Fig. 4(a) data (D435). Gain FWHM 62 nm at 200 mA in
  `gain_bandwidth_nm` (criterion in condition, D33). Series resistance 7.5 ohm `author_estimate` (origin not stated).
- Geometry: Si strip 2 um x 0.76 um, BOX 2 um, length about 1.36 mm, mesa 75 um.
- Not entered: thermal impedance 40 K/W (laser-only parameter, gap); facet reflectivity 5e-4 (no parameter); gain fit
  g0 972 cm-1 / Jtr 544 A/cm2; injection efficiency 70 % and waveguide loss 15 cm-1 (cited ref. [2], rule 3);
  confinement 3.4 % (calculated); > 20 dB projected chip gain; Fig. 4(b) calculated curves. Polarization of the gain
  data is not stated in this text (the merged PTL rows carry TE from that paper; not copied, rule 1).
- Fab empty (passive; authors at UCSB and Intel; acknowledgment funding / discussions only). Facility: none.

## resan2005 (IEEE PTL 2005, dispersion-managed breathing-mode semiconductor MLL): 0 rows

The laser is a free-space sigma-ring cavity built from a purchased SOA ("Sarnoff Corp. for providing us with SOAs",
p.3), a chirped MQW saturable-absorber mirror (described in the authors' ref. [7]) and intracavity dual-grating
double-pass stretcher / compressor with telescopes (p.1, Fig. 1); the output is externally amplified with a second
SOA and compressed in a bulk grating compressor. Treated as a bench-top bulk-optic assembly out of scope (D411; D642
fontaine2019 precedent). No standalone SOA value is reported (Fig. 2 shows only its spontaneous-emission spectrum, and
`center_wavelength_nm` is not allowed for amplifiers). Values that a `laser.comb` row would carry if the coordinator
rules it in scope (all system-level, after the external SOA and bulk compressor):
- pulse duration 185 fs FWHM from SHG-FROG retrieval (p.3 Fig. 6; FROG error 0.006, 128 x 128 grid) - `pulse_width_fs`
  measured;
- repetition rate 323 MHz (p.1 Abstract, p.3) - `repetition_rate_ghz` 0.323 derived (D256);
- average output power 14 mW (p.3) - `output_power_mw` measured; spectrum about 9 nm in the down-chirping regime
  (p.2, width definition not stated);
- not enterable: peak power about 230 W, focused intensity about 4.6 GW/cm2 (calculated; no parameter), autocorrelation
  FWHM 310 fs (1.7x the bandwidth limit), intracavity compression ratio 50, about 11 ps intracavity chirped pulses
  (cites ref. [7]).
Missing org (vendor of the purchased SOAs, would be fab on an SOA row): "Sarnoff Corp." (p.3 Acknowledgment). CREOL /
UCF are author affiliations only.

## kim2004 (LEOS 2004 WFF2, all-semiconductor X-CPA system): 0 rows

Text layer of p.1 is OCR-like (e.g. "L62ps", "4ldR"); p.1 has no page render, values checked on the p.2 render and the
clean p.1 passages. Components and why none is entered:
- Colliding-pulse mode-locked laser (free-space external cavity with an inverse-bowtie SOA and a transmission MQW
  saturable absorber, 285 MHz, 654 fs after a dual bulk grating compressor assuming sech, 30 pJ per pulse, 6 nm
  spectrum; p.1, Fig. 1): bench-top bulk-optic laser, out of scope (D411 / D642), as resan2005.
- Chirped fiber Bragg grating stretcher / compressor (2000 ps/nm: 1.62 ps -> 8 ns -> 1.80 ps, p.1-2, Fig. 2; 4000 ps/nm
  for 16 ns, p.2): fiber-only passive part (in scope by D80f) but no registry parameter for dispersion or stretch
  factor (dispersion rejected, D81 / D250; "dispersion-compensator parameters" candidate, D697).
- Second-stage amplifiers, 3 mm inverse-bowtie SOA and 4 mm broad-area amplifier (100 um stripe), pulse-biased at up
  to 50 A / 80 A peak: 154 nJ and 238 nJ output energy per 16 ns stretched pulse (p.2, Fig. 3) - no `pulse_energy`
  parameter (recurring candidate, D695 / D697); no per-amplifier gain or power is printed.
- Total system gain > 41 dB (> 13000x, 17.5 pJ oscillator input; p.1-2) is a chain value across pulse picker,
  preamplifier and two amplifier stages, not one component.
Missing orgs (vendors of purchased parts): "Sarnoff" (SOAs) and "Naval Research Laboratory" (MQW saturable absorber),
p.2 acknowledgment; neither in `organizations.csv` / `org_aliases.csv`. Only relevant if rows are added.

## Missing fab / facility orgs

- "Sarnoff Corp." - vendor (fab role on a purchased-SOA row), resan2005 p.3 Acknowledgment; "Sarnoff", kim2004 p.2.
- "Naval Research Laboratory" - supplier of the MQW saturable absorber, kim2004 p.2 (fab role only if a laser row is
  added).
No missing org for the 8 entered rows (`org_fraunhofer_heinrich_hertz_institute` exists).

## Registry gaps (skipped value + locator + proposed definition)

- `wpe_pct` (or `power_conversion_efficiency_pct` definition) on `amplifier`: juodawlkis2009 11 % electrical-to-optical
  conversion efficiency at Pmax, neglecting TEC power (p.2 Sec. III). Proposed: "electrical-to-optical (wall-plug)
  conversion efficiency of an electrically pumped amplifier, output optical power over electrical input as defined
  by the paper (cooler power included or not in condition)".
- `polarization_dependent_gain_db` on `amplifier`: juodawlkis2009 TE/TM gain ratio 17-18 dB (p.2 Sec. III). Proposed:
  "ratio of TE to TM (or max to min over polarization) gain, positive dB" (pdl_db on amplifier already a candidate,
  D674).
- `thermal_resistance_k_per_w` on `amplifier`: park2007b 40 K/W thermal impedance (p.2 Sec. 3; also merged park2007).
- `pulse_energy_nj` on `amplifier` / `laser`: kim2004 154 / 238 nJ (p.2), 30 pJ / 17.5 pJ oscillator (p.1-2);
  recurring candidate (D695 / D697).
- `confinement_factor_pct` (calculated; candidate D581): juodawlkis2009 0.5 % (p.1), park2007b 3.4 % (p.1).
- Amplifier facet reflectivity: park2007b 5e-4 (p.3), bimberg2009 R < 1e-3 (p.1) (as noted in merged park2007).

## Judgment calls for the auditor

1. resan2005 and kim2004 at 0 rows (bench-top free-space mode-locked lasers and X-CPA chains of purchased SOAs; D411 /
   D642). If ruled in scope, the candidate values are listed above (resan2005 185 fs / 0.323 GHz / 14 mW).
2. bimberg2009 HHI borderline fab on the facet row only (AR-coating assistance thanks, D84b) vs on all three SOA rows
   vs empty.
3. bimberg2009 gain per length 10 / 7 dB/mm left in notes (D159 / D254) rather than entered on the 2 mm / 3 mm rows.
4. XGM small-signal bandwidth entered as `bw3db_ghz` on `amplifier` (first amplifier use of this parameter).
5. juodawlkis2009 packaged values with `ref_plane module` (vs `fiber`); 90 % coupling efficiency `author_estimate`
   (cited 0.9 W input, D429) rather than not entered (rule 3 "computed from cited values").
6. park2007b 5 dB per-facet loss `author_estimate` although this text says "measured" without printing the total
   (D167 would give `measured`; kept consistent with the merged PTL precedent, D583, since an insertion-loss
   measurement needs an unstated facet / waveguide split). park2007b duplicates the merged PTL device; a lit-to-lit
   `same_as` or dedup is the coordinator's call.
