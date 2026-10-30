# Batch lit_45 report (distill subagent, 2026-10-29)

Dry-run `batch lit_45: +14 components, +62 metrics; errors 0` (the only warning printed is in another batch,
`cmp_lit_ni2025b_pimmwc`). ASCII only, no e-mail / street text, quotes from the two restricted sources (jankowski2020,
kittlaus2020a) limited to a few words. Not yet audited or merged. Build helper: scratchpad `lit_45/build.py`.

Page-1 title check: jankowski2020, kittlaus2020a, koyaz2026 match their source rows. xu2026: the cached arXiv v1 is
titled "High-gain optical amplification and lasing from erbium-doped single-crystal films ..." while the source row
carries the journal title ("Optical Amplification and Lasing From ..."); same arXiv id 2511.22820, same content: not a
wrong document (D397 / D409 not triggered), noted only. kittlaus2020a (26 pages: main p.1-12, Supplement p.13-26)
processed fully. No supplement cached for xu2026 (Supplement 1, Figs. S1-S16) or jankowski2020 beyond the 2-page
supplement inside text.md.

## Per paper (components / metrics)

- jankowski2020 (1 / 7): nanophotonic PPLN ridge waveguide on 700 nm x-cut MgO:LN, 6 mm
  (frequency_converter.shg, lnoi_rib): fitted peak CW normalized efficiency 1000 %/W-cm2 (measured, only fit
  parameter of the Eq. (3) fit), theory 1100 %/W-cm2 (simulated), 50 % femtosecond SHG efficiency at 60 fJ (measured),
  length 6000 um (derived), top width ~1850 nm and etch ~340 nm (stated for the fabricated waveguides, measured, method
  not stated), film 700 nm. Facilities: Harvard CNS (patterning, dry etch) and SNSF (electrodes, poling), p.6.
  Not entered: SHG transfer-function bandwidth > 250 nm between zeros (registry gap 1); < 0.1 dB/cm loss (stated as the
  outcome of the ref. [13] process of co-authors, no wavelength: D259); calculated Delta k', k'', A_eff, gamma_SPM,
  n2; poling period (only the simulated Fig. 1(b) map); supercontinuum sibling (same geometry, Delta k L = 3 pi: octave
  at 2 pJ, > 2.5 octaves at > 10 pJ; no parameter, no row). Fab empty (no fabrication sentence; authors over six orgs).
- kittlaus2020a (5 / 22): AlN-on-SOI SAW acousto-optic devices (all soi_rib, 220 nm Si, 90 nm etch, 700 nm SiO2,
  600 nm AlN, Al IDTs):
  - intra-modal phase modulator w 750 nm, Lao ~0.24 mm (phase_shifter.other): Vpi ~75 V derived from the printed
    VpiLao = 1.8 V cm and Lao ~0.24 mm (hosseini2015 precedent), width, length.
  - inter-modal single-sideband modulator / frequency shifter w 1500 nm (mode_converter.converter, sohn2018 /
    cheng2025 precedent): ~1 % sideband efficiency at 89 mW RF (1600 nm), FWHM 84 nm around 1604 nm as bw_3db_nm,
    width, length.
  - serpentine non-reciprocal modulator (mode_converter.converter): 13.5 % (-8.7 dB) at 120 mW RF, 1525.4 nm;
    0.8 nm FWHM operation bandwidth (printed around lambda_b 1523.7 nm); insertion loss < 0.6 dB (author_estimate,
    origin not stated, scope unspecified, wavelength inferred 1525.4 nm); Ltot 15300 um (derived); w 1500 nm.
  - Si ridge waveguide w 1.5 um (waveguide_platform.straight): < 0.15 dB/cm symmetric (TE0), < 0.35 dB/cm
    anti-symmetric (TE1), wavelength not stated (band unspecified); stack geometry.
  - grating coupler: < 6 dB/facet typical at 1535 nm (per_coupler, measured, D167).
  Not entered: ~15 dB forward / backward non-reciprocal contrast (Fig. 5(i) label ~16 dB): same quantity as sohn2018,
  ruled not isolation_db in the lit_33 audit (registry gap 3); hence no nonreciprocal row (the paper only says the
  device is a frequency-shifting four-port circulator in principle and that an isolator is within reach); single-
  sideband suppression ~30 dB / >= 30 dB (gap 4); phase-matched centre wavelengths 1604 / 1525.4 / 1523.7 / 1544 nm
  (gap 5); ~20 MHz FWHM RF response; acoustic power estimates; group indices 3.84 / 3.72 (waveguide width not stated,
  D159); IDT circuit values Rp / CT / LT / K2 (transducer, not photonic); design FWHM 75 nm (calculated); sibling
  serpentine (Lambda 721 nm, 6.28 deg, w 1.45 um, lambda_f 1544 nm, Supp. p.24: no performance parameter, no row).
- koyaz2026 (2 / 13): periodically poled (1425 nm, third-order QPM) fully etched 800 nm X-cut TFLN waveguides
  (lnoi_strip), 4.5 mm poled length:
  - w 1.26 um backward-wave DFG (frequency_converter.sfg_dfg): CE up to 0.6 %/W (le, derived: powers scaled with
    path / edge-coupler losses, D166 / D394, stone2022 precedent), idler thermal tuning 2250 pm/K (printed 2.25 nm/C,
    derived), poling 1.425 um, length, width, film, 75 deg sidewall (simulated cross-section label).
  - w 1.30 um backward-wave SHG (frequency_converter.shg): CE up to 1.8 %/W (le, derived), same geometry rows.
  Facility: EPFL CMi (fabrication carried out there, p.7). Not entered: BWSHG of the 1.26 um waveguide (no
  text-stated value; Fig. 5(b) raw peak ~0.8 %/W), BWSHG 3-dB bandwidth < 0.1 nm (gap 1), idler tuning 1244-1290 nm
  (gap 2), QPM wavelengths (gap 5), DFG slopes, simulated bandwidths / coverage. Fab empty (authors EPFL + Q.ANT).
- xu2026 (6 / 20): Er:Gd2O3 epitaxial single-crystal film on SOI (111), SiN strip-loaded (platform other):
  - amplifier 1.5 mm (amplifier.rare_earth): net modal gain 23.9 dB/cm (derived, D166), material gain 78.3 dB/cm
    (author_estimate: rests on the simulated confinement factor 0.35), length, width; 1535.7 nm, 2.3 K.
  - amplifier 6 mm: total internal gain 13 dB (derived), length, width.
  - waveguide_platform.straight (same cross-section, D396): <= 2.11 dB/cm room-temperature cutback upper bound
    (wavelength range = Fig. 1(d) axis, inferred), 3.37 dB/cm background passive loss at 2.3 K / 1535.7 nm.
  - focusing grating coupler: ~26 % per coupler (band c_band inferred).
  - microring R 150 um (resonator.ring): loaded Q 4.23e4 at 1538.3 nm, 2.3 K; radius, ring / bus width 1080 nm,
    gap 300 nm.
  - microring laser (laser.other): threshold ~8.5 mW on-chip pump, SMSR 36.5 dB, ~1536 nm, on-chip emission ~22 uW
    read off Fig. 4(b).
  Not entered: room-temperature net modal gain 1.06 dB/cm (waveguide length not stated, D159); room-temperature
  material gain > 9.4 dB/cm (estimate); Er absorption 63.6 dB/cm and cross sections (material / resonant absorption);
  ~1.2 mW transparency pump; laser linewidth (OSA-limited, D250); expected 70 K lasing; side peaks +/-1.16 nm; CDC
  arc 15 deg (no resonator parameter); 9.0 dB/cm effective ring loss (from Q incl. coupling, group index not stated).
  Fab empty (NTT + Nihon University authors).

## Fab / facility orgs missing from the registry (as printed + locator)

- Jet Propulsion Laboratory, California Institute of Technology (kittlaus2020a p.1 affiliation; p.11 author
  contributions: the three fabricating authors are all JPL). Would be fab_org_ids of all 5 kittlaus2020a rows
  (parent org_caltech exists; no JPL row or alias).
- UNIL Cellular Imaging Facility (CIF) (koyaz2026 p.7 Acknowledgement: two-photon imaging of the poling test);
  characterization only, would not be entered on the waveguide rows.
- NANOLN (jankowski2020 p.3, thin-film supplier; note only). If NANOLN is the trade name of
  org_jinan_jingzheng_electronics, an alias would help; not verified here.

## Judgment calls (for the audit)

1. kittlaus2020a: no nonreciprocal row; the serpentine device is entered as mode_converter.converter with its
   conversion efficiency and bandwidth, the ~15 dB forward / backward contrast left out, following the lit_33 audit
   ruling on sohn2018 (same physics, same kind of number).
2. kittlaus2020a: printed "FWHM" bandwidths stored as bw_3db_nm because Supp. Sec. IV (p.21) defines the FWHM at the
   half-power point of the modulated-power envelope; for the serpentine the 0.8 nm is tied by the text to the lobe
   around lambda_b = 1523.7 nm (wavelength_nm as printed).
3. kittlaus2020a: "insertion losses < 0.6 dB" entered on the serpentine converter row as author_estimate (origin not
   stated), scope unspecified, wavelength inferred (device lambda0).
4. kittlaus2020a: acousto-optic phase modulator as phase_shifter.other with Vpi 75 V derived from VpiL / Lao (Lao is
   approximate, qualifier approx).
5. koyaz2026: "up to 1.8 %/W" (stated for both waveguides) attributed to the w 1.30 um waveguide from the Fig. 5(b)
   render (blue trace peak near 1981.5 nm); "up to" -> qualifier le (skill rule 7); CE basis derived (powers corrected
   with path / dichroic / edge-coupler losses).
6. xu2026: net modal gain 23.9 dB/cm attributed to the 1.5 mm waveguide (Fig. 3(b) names no length; its highest pump
   point equals the 41.6 mW of the 1.5 mm Fig. 3(a) measurement). If the audit rejects this, the value moves to notes
   (D159).
7. xu2026: polarization left empty on metric rows (the design / simulated mode is TM; the measured polarization is not
   stated); jankowski2020 measured rows likewise without TE00 (only the simulated row keeps it).
8. jankowski2020: "fabricated waveguides have a top width of ~1850 nm and an etch depth of ~340 nm" entered as
   measured (differs from the 350 nm design; method not stated) rather than design_target.
9. xu2026: lasing ring and passive Q ring as two rows (laser.other / resonator.ring, D396), cross-noted; the paper does
   not say the lasing ring is the Fig. 2 device, so no geometry on the laser row.

## Registry gaps (proposed definitions)

1. Phase-matching bandwidth for frequency_converter: widen `bw_3db_nm` to frequency_converter or add
   `pm_bandwidth_nm` = full width of the phase-matching / SHG transfer-function response in fundamental (pump)
   wavelength, criterion (3-dB, FWHM, between zeros) in condition. Values: jankowski2020 > 250 nm between zeros (p.4);
   koyaz2026 BWSHG < 0.1 nm 3-dB (p.6); lit_33 carpenter2020 0.28 / 0.18 nm.
2. Tuning range for frequency_converter: widen `tuning_range_nm` to frequency_converter (generated-wave tuning range,
   mechanism in condition). Values: koyaz2026 idler 1244-1290 nm (p.7); lit_33 wang2026c OPO 1205-1378 nm.
3. `conversion_contrast_db` (already proposed in the lit_33 audit): kittlaus2020a ~15 dB (p.9, p.10) as a second
   confirmed value.
4. `sideband_suppression_db` (mode_converter, nonreciprocal): suppression of the unwanted frequency-shifted sideband
   relative to the wanted one, positive dB. Values: kittlaus2020a ~30 dB / >= 30 dB (p.6 Fig. 4(g) caption, p.7,
   p.10); lit_33 sohn2018 45 dB.
5. Centre (phase-matched) wavelength for mode_converter and frequency_converter: widen `center_wavelength_nm`.
   Values: kittlaus2020a 1604 nm (SSB), 1525.4 nm (serpentine); koyaz2026 BWSHG ~1980.4 nm, BWDFG signal ~1983.4 nm.
