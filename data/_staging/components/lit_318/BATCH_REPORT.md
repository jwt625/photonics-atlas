# Batch lit_318 report

Papers: lit:ferdous2011, lit:cheng2018, lit:green2007, lit:zhuang2015, lit:li2012. Distilled 2026-11-28.
Validation: `merge_component_staging.py data/_staging/components/lit_318 --dry-run` -> +16 components, +52 metrics,
0 errors (the 2 warnings are in other batches: guo2024a, ni2025b).

Page-1 title check: all five cached texts are their source rows' papers; none is a correction / erratum; no
`garbled_text_layer`. ferdous2011 and li2012 are arXiv preprints of the listed journal papers (Nature Photonics 2011;
Phys. Rev. Lett. 2012): values come from the preprint only and every row of these two papers says so in its notes
(the ferdous2011 preprint title is the singular "...of an On-Chip Microresonator Frequency Comb"). cheng2018,
green2007 and zhuang2015 are Optica open-access publisher copies.

Totals: ferdous2011 3 components / 19 metrics; li2012 7 / 19; zhuang2015 6 / 14; cheng2018 0; green2007 0.

## lit:ferdous2011 (3 components / 19 metric rows)

| component | class | platform | metrics |
|---|---|---|---|
| cmp_lit_ferdous2011_sin_ring_r40 | resonator.ring | sin | linewidth 1.2 pm, Q_L 1.3e6 at 1556.43 nm TM (measured); Q_i 2.0e6 author_estimate (D403); FSR ~4.7 nm; R 40 um, width 2000, bus 1000, gap 700, Si3N4 430 nm, etch 430 nm, BOX 3 um, clad 3 um |
| cmp_lit_ferdous2011_kerr_comb | laser.comb | sin | repetition rate 595 GHz (p.1, p.3); 26 lines incl. pump (pump ~1543 nm, ~27.5 dBm estimated in the waveguide); 9 lines after months of air exposure |
| cmp_lit_ferdous2011_vgroove_edge_coupler | fiber_chip_coupler.edge | sin | per-facet loss ~6.4 dB (bare SMF in V-groove) / ~3 dB (lensed fiber), measured (D167), C band inferred; tip 100 nm; oxide region ~10 um wide |

Values not entered and why:
- Pulse durations ~300 fs (abstract), 270 fs +/- 4 % and 312 fs +/- 7 % (p.7-8): produced only after the off-chip
  fiber-coupled line-by-line pulse shaper (LCM) and calculated from the spectrum with flat phase; not a chip property
  (D411 chip-plus-bulk precedent). Autocorrelation widths 411 / 460 fs (setup traces).
- Relative frequency-shift bound of order 1e-4 Hz (p.9): no parameter.
- Comb spacing "about 4.7 nm" (p.5): same quantity as the 595 GHz repetition rate, entered once.
- Transmission contrast Delta T = 0.9 of the 1556.43 nm mode: printed linear, no dB value; not converted.

Fab: `org_center_for_nanoscale_science_and_technology` borderline on all 3 rows (D84b): "We fabricated silicon
nitride ring resonators" (p.4) with authors at Purdue and NIST CNST / UMD, so the own org is ambiguous (D154); the
acknowledgment thanks the CNST Nanofab staff for help with e-beam lithography (p.9), which places the fabrication at
CNST. No facility (staff thanks never set a facility, D72 / D84b). Missing orgs: none.

## lit:li2012 (7 components / 19 metric rows)

| component | class | platform | metrics |
|---|---|---|---|
| cmp_lit_li2012_silica_disk_2mm | resonator.disk | silica | Q_i 2.7e8 author_estimate (D403), C band inferred; FSR 33 GHz; radius 1000 um derived |
| cmp_lit_li2012_comb_33ghz | laser.comb | silica | threshold ~2 mW (Fig. 1(b)); ~200 lines at 7.5 mW and ~1900 lines at 200 mW coupled; repetition rate 33 GHz |
| cmp_lit_li2012_comb_66ghz | laser.comb | silica | repetition rate 66 GHz (Fig. 2(a)) |
| cmp_lit_li2012_silica_disk_25mm | resonator.disk | silica | Q ~1.1e8 (unqualified -> q_loaded, author_estimate, origin not stated); FSR 2.6 GHz; radius 12500 um derived |
| cmp_lit_li2012_comb_2p6ghz | laser.comb | silica | repetition rate 2.6 GHz; threshold ~28 mW extracted_from_figure (Fig. 3, +/- 1 mW) |
| cmp_lit_li2012_comb_22ghz | laser.comb | silica | repetition rate 21.953 GHz (beat note); ~80 phase-locked lines |
| cmp_lit_li2012_comb_diameter_series | laser.comb | silica | threshold as low as 1 mW (best); < 5 mW over 4.4-220 GHz; repetition rates 2.6-220 GHz (range); radius 150-12500 um |

Values not entered and why:
- Q up to 875 million and the surface-roughness data (p.1): cited from ref. [19], the authors' earlier paper (D259).
- Comb spans 62 THz / 1320-1820 nm (2 mm disk) and 106 THz / 1180-2020 nm (66 GHz device): no comb-span parameter
  (D81 rejected).
- Phase noise -113 dBc/Hz at 10 kHz offset of the 21.953 GHz beat note, 20-30 dB below the unlocked states (p.4,
  Fig. 5): no parameter (registry gap below).
- Fig. 3 threshold points for 0.3-15 mm devices: several pump modes per device, mode of each point not identified;
  only the single 25 mm point is entered.
- Mode area ~30 um2 and n2 (p.2): model inputs. Brillouin coincidence at ~6 mm / 10.8 GHz (p.4): cited to [19, 24].

Fab empty: "a series of devices ... were fabricated" (p.3) is passive (D80b). Facility: `org_kavli_nanoscience_institute`
borderline on all 7 rows (D80c), see judgment call 2. Missing orgs: none.

## lit:zhuang2015 (6 components / 14 metric rows)

| component | class | platform | metrics |
|---|---|---|---|
| cmp_lit_zhuang2015_mesh_2cell | switch_fabric.mzi_mesh | sin | IL ~9 dB fiber_to_fiber; 0.25 W mean per heater during operation (power_consumption_w); chip 3.5 x 8.5 mm (Fig. 2(a) labels) |
| cmp_lit_zhuang2015_mz_coupler | splitter.other | sin | power coupling 0-99 % (range, derived from 0-0.99); length 3450 um; DC length 675 um |
| cmp_lit_zhuang2015_heater_ps | phase_shifter.thermo_optic | sin | phase-shift range 2 pi |
| cmp_lit_zhuang2015_dual_ring_rf_filter | wdm.other | sin | FSR 14 GHz (author_estimate); RF extinction > 17 dB (band-stop and bandpass), 55 dB notch (best), 25 dB flat-top with kappa1 = kappa2; RF 1-dB bandwidth up to 1.6 GHz (le) |
| cmp_lit_zhuang2015_edge_coupling | fiber_chip_coupler.edge | sin | ~4 dB per facet, loss_breakdown, author_estimate (zhuang2016 precedent) |
| cmp_lit_zhuang2015_sin_wg | waveguide_platform.straight | sin | group index 1.71 (author_estimate) |

Values not entered and why:
- RF centre-frequency tuning 1.6-6 GHz (31 % of the FSR, Fig. 4(c)-(d)): no RF tuning-range parameter in GHz
  (registry gap below). Passband dispersion < 2 ps/MHz (p.3): no parameter.
- Fig. 2(b) optical responses of the four programmed circuits (notch, Hilbert transformer, bandpass, delay line): no
  printed values (axis readings only; D156).
- Mesh-cell area ~0.35 x 0.35 cm (p.4): derived by the authors from the coupler length; kept in notes.
- Heater section 2100 um: `heater_length_um` is not allowed on `splitter` and the dedicated phase shifters' heater
  length is not printed; kept in notes.
- System gain / noise figure values (p.5) are cited work.

Fab empty, `process_name` "TriPleX" on all rows: "fabricated in a commercial Si3N4 waveguide technology (TriPleX
[33]; see Supplement 1)" (p.2, Fig. 2 caption) names no org (Contract v7). Supplement 1 is not cached, so any
fabrication statement there was not seen. LioniX BV is an author affiliation only (D80b); SATRAX B.V. supplied the
control electronics (setup). No wavelength is printed anywhere: loss and group-index rows carry `band: unspecified`.
Missing orgs: none.

## lit:cheng2018 (0 components)

Review (Optica 2018, data-center optical technologies). Every device value is credited to cited work, including the
authors' own: Fig. 6(e) [76], Fig. 6(f) [77, 78], the 4 x 4 S&S switch on-chip loss 1.8 dB and -50 dB crosstalk (p.12,
[182], D259 / D408). The microring design-space metrics (IL < 1 dB, BW 10-50 GHz, FSR > 10 nm, extinction > 30 dB,
p.7) are design targets, not results. Fig. 12 (AIM Photonics-fabricated S&S and Clos switches) and Fig. 13 (packaged
switches) are photos with no values. Modulator content would be EO-atlas data (rule 2). No rows.

## lit:green2007 (0 components)

Si p+-i-n+ carrier-injection MZM (IBM Watson). Every value is a modulator metric that stays with the EO atlas
(rule 2; pfeifle2012 precedent): Vpi 1.8 V and VpiL 0.36 V-mm (L = 200 um, 9 MHz drive, Vbias 1.8 V, p.5), on-chip
loss 12 dB and extinction 6-10 dB (p.4), FSR 7.3 nm from the 80 um path imbalance (p.4), forward resistance 49 ohm,
reverse leakage < 10 nA, reverse capacitance 200 fF / RC cutoff ~16 GHz (p.4), 5 / 10 Gb/s with pre-emphasis,
DC 230 / 287 uW and RF 41 / 51 mW, ~5 pJ/bit (p.7-8). The polymer spot-size converters (p.4) and Y-junctions (cited
[18]) have no values; the rib geometry (550 x 220 nm, 35 nm slab, 2 um BOX) is geometry-only (rule 9).
EO-atlas candidate. Fab: "MZM devices ... were fabricated" (p.4) is passive with no org; not applicable here.

## Judgment calls (coordinator questions)

1. ferdous2011 fab: CNST staff thanks for e-beam lithography -> borderline `org_center_for_nanoscale_science_and_technology`
   (D84b). Alternative: leave fab empty because the authors span Purdue and NIST (D154). Recommendation: keep the
   borderline fab, as in D84b xie2024 / bhasker2026.
2. li2012 facility: the arXiv acknowledgment is cut off after "the authors thank the Kavli Nanoscience Institute
   (KNI)" (p.5), so the purpose is not printed. Entered as borderline facility (D80c: a named facility thanked).
   Alternative: leave it empty until the journal acknowledgment can be read. Recommendation: keep it as borderline;
   a bare thanks to a shared nanofabrication facility of the authors' own institution reads as facility use.
3. li2012 rows: one resonator row and one comb row per characterized disk (D396), plus a family row for the Fig. 3
   diameter series (D165). The 2 mm and 25 mm members are also covered by the family range values.
4. li2012 and ferdous2011 comb spacing entered as `repetition_rate_ghz`: both papers call it a repetition rate
   (D83b); ferdous2011 also characterizes pulses (after an external shaper).
5. zhuang2015 RF-domain responses (extinction, 1-dB width) entered on the programmed dual-ring `wdm.other` row with
   the microwave-photonic link in the condition (qiu2018a MPF precedent; catalalahoz2026 programmed-filter class).
6. zhuang2015 MZ coupler as `splitter.other` (lit:zhuang2011, same group and TriPleX coupler; D74), not
   `switch_fabric.other`, because the paper characterizes it as a tunable-ratio coupler (0-0.99).
7. zhuang2015 per-heater power (0.25 W, stated once for all heaters) on the mesh row as `power_consumption_w`, not on
   a heater row (D254).
8. zhuang2015 FSR: abstract / p.2 print a chip FSR of 14 GHz; p.3 says the maximum RF coverage is half the ring FSR,
   "that is, 14 GHz". The 31 % / 11 % ratios match a 14 GHz ring FSR, so 14 GHz is entered with the wording noted (D417).

## Registry gaps

- `phase_noise_dbc_per_hz` (laser / comb; offset frequency and carrier in condition): li2012 -113 dBc/Hz at 10 kHz
  offset on the 21.953 GHz beat note, phase-locked state (p.4, Fig. 5). Proposed definition: single-sideband phase
  noise of the repetition-rate / beat-note signal at the stated offset.
- RF tuning range in frequency for programmable / microwave-photonic filters (e.g. `tuning_range_ghz`, wdm): zhuang2015
  centre frequency 1.6-6 GHz (p.3, Fig. 4(c)-(d)). Proposed definition: span over which the filter centre frequency is
  tuned without shape change, in GHz.
- Comb span (laser.comb): li2012 62 THz and 106 THz (p.2); already rejected in D81, listed only for the record.

## Missing fab / facility orgs

None: CNST (`org_center_for_nanoscale_science_and_technology`) and KNI (`org_kavli_nanoscience_institute`) are in the
registry.
