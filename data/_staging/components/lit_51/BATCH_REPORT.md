# lit_51 batch report (amplifier, nonreciprocal; 2026-10-30)

Papers: bi2011 lira2012 foster2006 shoji2008 keyvaninia2012 kuyken2011. All six texts read in full; page-1 titles match
the source rows; none is a correction / erratum; no `garbled_text_layer` flags. Renders opened: bi2011 p.2, p.3, p.5;
lira2012 p.4 and the Fig. 1(a) image; foster2006 p.2; shoji2008 p.3; keyvaninia2012 p.2, p.3; kuyken2011 p.2.
None of the papers had rows in `data/components/` before this batch.

Dry run: `merge_component_staging.py data/_staging/components/lit_51 --dry-run` -> "batch lit_51: +20 components,
+88 metrics; errors 0" (only the pre-existing WARN on cmp_lit_ni2025b_pimmwc-m18).

| paper | components | metrics |
|---|---|---|
| bi2011 | 2 (nonreciprocal.isolator, resonator.ring) | 16 |
| lira2012 | 1 (nonreciprocal.isolator) | 6 |
| foster2006 | 8 (3 amplifier.parametric, 3 frequency_converter.other, waveguide, edge coupler) | 22 |
| shoji2008 | 3 (nonreciprocal.isolator, waveguide, edge coupler) | 17 |
| keyvaninia2012 | 2 (amplifier.soa) | 12 |
| kuyken2011 | 4 (amplifier.parametric, frequency_converter.other, waveguide, edge coupler) | 15 |
| total | 20 | 88 |

## Per paper

### bi2011 (monolithic Ce:YIG/YIG racetrack isolator, MIT)

- Isolator: isolation 19.5 dB best, TM, 1542 nm, 25 C (p.2; abstract "up to"; ±2.9 dB over repeated field reversals in
  notes); insertion loss 18.8 dB as `on_chip_excess` (Fig. 1(c) defines it from the off-resonance level to the
  transmitting curve at the operating wavelength; wavelength inferred = operating resonance); length 290 um, width,
  Si / BOX / cladding thickness.
- Resonator row for the same racetrack (D396): FSR 0.9009 nm measured and 0.9016 nm simulated at 1542 nm (p.4), R 45
  um, gap 200 nm, widths 450 nm, stack.
- Fab org_mit: author contributions (p.5) say L.B. (MIT) did the device fabrication (D395). No facility. SOI wafer
  "SOI Tech." = supplier note.
- Not entered: non-reciprocal resonance shifts 18.2 / 3.5 pm (TM / TE), 21.7 -> 18.4 pm dispersion, Bi:YIG device
  14.8 pm at 1549.5 nm (no parameter; Bi:YIG device has no other value, so no row); 10 dB isolation bandwidth 1.6 GHz
  (frequency unit, otterstrom2019 precedent: gap below); material values and the ~9 cm-1 / 5.3 dB/cm losses from ref.
  16 (authors' earlier work, D259); projected 5-6 dB IL.

### lira2012 (electrically driven interband-transition isolator, Cornell / Stanford)

- Isolator: isolation 3 dB best at 1558 nm, 10 GHz drive at 25 dBm RF (p.4, Fig. 4); IL ~70 dB (p.4, scope
  unspecified); rail width 450 nm, etch 215 nm, slab 35 nm, 1 um cladding.
- Fab org_cornell_university + facility org_cornell_nanoscale_facility: "We fabricate the device" (p.5) with the work
  performed in part at CNF (D83c; authors at Cornell and Stanford).
- Not entered: 200 GHz bandwidth of "significant" nonreciprocity (no level, frequency unit); expected 16 dB dopant loss
  for a 1.0 cm device (design expectation); rail separation d 500 nm (no gap parameter for nonreciprocal); diode /
  period / inductor geometry; simulation-only cases.

### foster2006 (Si FWM parametric gain, Cornell)

- 300 x 550 nm, 6.4 mm OPA: on/off gain 1.9 dB best (11.0 W), net on/off gain span 23 nm (derived from 1512-1535 nm);
  17 mm OPA: on/off 2.9 dB (4.2 W), span 15 nm (1525-1540), 4.2 dB at 1530 nm (Fig. 3(b) legend), net 1.8 dB
  (paper's arithmetic, derived); 215 x 445 nm, 8 mm comparison: on/off -1.7 dB.
- Frequency_converter rows (D396) for the same three waveguides: on/off idler conversion efficiency +2.4 dB -> 174 %,
  +5.2 dB -> 331 %, -13.2 dB -> 4.8 % (derived, % per the registry and the ye2021 precedent).
- Waveguide row: 1.1-1.4 dB/cm at 1550 nm (cutback, 7.4 mm difference, six waveguides). Edge coupler row: 12.3-13.3 dB,
  scope unspecified (per facet vs both not stated).
- Fab empty ("fabricated as previously described", ref. 29). Center for Nanoscale Systems = funding, not a facility.
- Not entered: abstract 28 nm net-gain span (union of two waveguides, D254); +3 to -2 dB peak conversion efficiencies
  for 1511-1545 nm (waveguide not identified, D159); 300 x 600 nm waveguide (figure only); 9.7 dB nonlinear absorption
  and the "at least 13.9 dB" FWM-only gain (difference of values at different wavelengths); simulated GVD / gain.

### shoji2008 (Ce:YIG / Si MZI isolator by direct bonding)

- Isolator (one design, samples (a) / (b) as conditions): isolation 21 dB at 1559 nm (b), 17 dB at 1546 nm (a), > 10 dB
  over 1530-1565 nm (a), 10-dB isolation bandwidth >= 35 nm (derived, limited by the ASE source range; yan2024
  precedent); IL 8 dB de-embedded (derived: transmission minus the 37 dB coupling from an adjacent reference
  waveguide), interferometer excess 4 dB (loss_breakdown); length 4000 um, Si 2.0 um x 0.3 um, 10 nm rib, 1 um BOX.
- Waveguide row 6.3 dB/cm (printed 0.63 dB/mm, derived). Facet / PMF coupler row: 37 dB for both facets, scope
  `device_total` (fard2021 precedent), not halved.
- Fab empty (passive; authors at Tokyo Tech, Shibaura, Columbia). No facility.
- Not entered: 1.3 dB bonding-interface scattering (number of interfaces not stated) and 0.2 dB Ce:YIG absorption (only
  as excludes of the 4 dB row); MMI geometry (0.15 mm, no metric); 70 dB noise floor; calculated spectra.

### keyvaninia2012 (heterogeneous III-V-on-SOI SOA, GROUP4 2012)

- 2 um / 400 um SOA: 13 dB chip gain best at 1560 nm, 40 mA (derived, reference-waveguide extraction, D166); 3 um /
  200 um SOA: about 8.5 dB at 1560 nm, 40 mA, `extracted_from_figure` (Fig. 4 trace; the only value for that design;
  axis printed "dBm", a typo). Geometry: mesa width, length, Si 400 nm / 180 nm etch / 2 um BOX. Platform `other`
  (davenport2016 precedent).
- Fab empty (no fabrication statement; authors at Ghent-imec, III-V Lab, CEA-LETI, TU/e). SOITEC wafer = supplier note.
- Not entered: gain FWHM 70 nm at 40 mA (gap below); taper widths / lengths (no amplifier parameter); 40 nm BCB;
  ASE ripple < 0.05 dB.

### kuyken2011 (mid-IR Si-wire OPA, 50 dB on-chip gain)

- OPA: on-chip gain 39.5 dB at 2356 nm (Fig. 4(a)), ~50 dB Raman-assisted at ~2445 nm, on-chip gain bandwidth > 580
  nm, off-chip ~30 dB (Raman) and > 20 dB (FWM only), off-chip gain bandwidth ~550 nm, saturated output ~20 dBm; all
  derived (on-chip from OSA spectra and the cutback coupling loss, D166; off-chip = on-chip minus ~20 dB). Length,
  BOX.
- Frequency_converter row (D396): idler conversion gain 42.3 dB -> 1.698e6 % at signal 2356 nm, ~50 dB -> 1e7 % at
  ~1950 nm (derived). Waveguide row < 2.8 dB/cm, 2000-2500 nm. Coupler row ~10 dB/facet (cutback, per Fig. 3(b)).
- Fab empty (unnamed CMOS pilot line, passive). No facility.
- Not entered: beta2 / beta4 / gamma (D81), differential gain dB/W, ~8 W off-chip transparency pump power, MI span,
  ref. [4] results (D259).

## Judgment calls

1. lira2012 `isolation_db` 3 dB entered: the measured quantity is the backward / forward transmission ratio between the
   two single-mode waveguides at the input frequency (the MMIs radiate the converted odd mode, p.3-4; Fig. 4 axis
   "Isolation"). This is a port-to-port transmission contrast, unlike the sideband-efficiency contrast of sohn2018 /
   kittlaus2020a, so those rulings do not apply.
2. lira2012 IL 70 dB as `measured` (stated for "this specific device"), scope unspecified; author_estimate would be the
   alternative (kittlaus2020a precedent was a generic, unmeasured statement).
3. bi2011 IL scope `on_chip_excess` from the Fig. 1(c) definition; resonator.ring row added for the same racetrack
   (D396) to hold FSR and ring geometry.
4. Frequency_converter rows for foster2006 / kuyken2011 (D396, ye2021 precedent); riemensberger2022 left an idler
   efficiency out. Kuyken values in % are very large (1.7e6, 1e7 %) because the registry stores conversion efficiency
   linearly.
5. foster2006 on/off gains `measured` with ref_plane empty (pump-on / pump-off ratio, coupling cancels); the 215 x 445
   nm comparison waveguide kept as an amplifier row with gain -1.7 dB (net loss as printed).
6. Cross-sections "300 nm x 550 nm" (foster2006) and "900 nm x 220 nm" (kuyken2011) not split into width / thickness
   (ye2021 ruling: the text does not say which is which).
7. Peak-gain wavelengths not printed: stored as the stated gain span with `wavelength_inferred` (foster2006); Fig. 3(b)
   / 3(c) legend wavelengths (1530 nm) used where the figure labels them.
8. keyvaninia2012 3 um design: gain read off Fig. 4 at the stated 1560 nm (the design has no printed performance value).

## Organizations

No fab / facility org missing: org_mit, org_cornell_university, org_cornell_nanoscale_facility exist. Supplier names
only in notes (SOI Tech., SOITEC = org_soitec exists).

## Registry gaps (proposals with the skipped values)

- `isolation_bw_ghz` (nonreciprocal): full width in frequency over which isolation exceeds the stated level. bi2011 1.6
  GHz at 10 dB (p.2); otterstrom2019 2.5 MHz at 10 dB (merged notes); lira2012 200 GHz has no level (would stay out).
- `nr_resonance_shift_pm` (nonreciprocal; resonance shift between propagation directions / field polarities): bi2011
  18.2 +/- 0.7 pm TM at 1542 nm (p.2, p.4), 3.5 pm TE, Bi:YIG device 14.8 pm at 1549.5 nm; ghosh2012a 1.1 nm (merged
  notes, in nm).
- `bw_fwhm_nm` widened to amplifier (gain spectrum FWHM as printed): keyvaninia2012 70 nm at 40 mA (p.2, 3 um / 200 um
  SOA).
- `gap_nm` for nonreciprocal (coupled-rail / slot separation): lira2012 d 500 nm (p.2 Fig. 1(a)); single value, defer.

## Top open questions

1. Accept lira2012 isolation_db (transmission contrast, not sideband contrast)?
2. foster2006 / kuyken2011 frequency_converter rows with % values of 1.7e6 / 1e7: keep, or leave the idler gain in
   notes (riemensberger2022 style)?
3. bi2011 1.6 GHz isolation bandwidth: add `isolation_bw_ghz`, or convert to nm (0.0127 nm at 1542 nm, derived)?
