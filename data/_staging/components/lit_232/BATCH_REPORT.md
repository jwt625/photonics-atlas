# lit_232 batch report

Papers: lit:yen2020, lit:akiyama2021a, lit:xu2017a. Page-1 titles match the source rows. No existing component rows for
these ids. verified_on 2026-11-20. Dry run of `merge_component_staging.py`: +12 components, +152 metrics, 0 errors; the
one warning names the merged row cmp_lit_ni2025b_pimmwc, not in this batch.

| paper | components | metric rows |
|---|---|---|
| yen2020 | 2 | 65 |
| akiyama2021a | 1 | 8 |
| xu2017a | 9 | 79 |

## yen2020 (fabrication-tolerant CWDM (de)mux, four-stage cascaded MZIs, 220 nm SOI, JLT 2021)

Rows:
- `wdm.cascaded_mzi` fabrication-tolerant (FT) demux (650 / 450 nm arms): Table I per-channel IL and crosstalk mean and
  std over nine dies (16 rows, n_samples 9); one-die IL 0.89-2.45 dB, crosstalk >= 20 dB (all channels) and > 30 dB
  (1550 / 1570 nm channels); grid offset 0.3-1.1 nm (one die), 0.16-0.96 nm per-channel range and sigma 0.79-0.95 nm
  over nine dies, averaged shift 0.487 +/- 0.878 nm (`wavelength_spread_nm`, mean / std rows, deng2026a / cheung2019
  precedent); averaged channel spacing 19.91 nm (measured); FSR 40 / 80 nm (design, author_estimate); 4 channels,
  4 stages, w1 / w2 650 / 450 nm, L1 / L2 23.250 / 8.014 um (`length_um`), 220 nm core, 20 um bend radius, footprint
  1.68 x 0.87 mm (derived); simulated group index ~4.4 at 1550 nm (450 nm waveguide).
- `wdm.cascaded_mzi` regular-MZI reference demux (same chips): Table I mean / std (16 rows); one-die IL 2.8-6.1 dB,
  crosstalk >= 13.8 dB, shift ~15 nm; nine-die shift 14.2-16.3 nm, sigma 1.7-2.6 nm, average 15.398 +/- 2.5 nm; 4
  channels, 4 stages, 450 nm width, L1 - L2 13.822 um, FSR 40 nm (design).

Not entered:
- 0.5-dB bandwidth > 10 nm for all four channels (p.6): no wdm 0.5-dB bandwidth in nm (registry gap below).
- Simulated width sensitivities (0.75 nm/nm regular vs 6 pm/nm FT, Fig. 4(a)(b); 0.745-0.755 nm/nm and 5-6 pm/nm over
  210-230 nm Si thickness; 1.34 nm per nm thickness), maximum shifts +/-42 vs +/-18 nm, tolerable width +/-2.5 vs
  +/-10 nm, FSR variation +/-0.748 vs +/-0.125 nm, and the 800 / 900 nm wide-waveguide designs (Fig. 8: 0.15 nm/nm,
  +/-7.4 nm, L1 - L2 15.556 um, 54.218 / 38.752 um): no parameter for spectral shift per width error; the
  two-stage simulated demuxes of Figs. 4 and 8 have no other performance value, so no design rows.
- dneff/dw ~2e-3/nm and neff ~2.35 (p.2): no parameter.
- Abstract "insertion loss of less than 2.1 dB" and "crosstalk lower than -20 dB" (p.1): the bound conflicts with the
  0.89-2.45 dB one-die range and Table I CH1 3.7 dB; not entered (noted on the one-die IL row). Conclusion ranges
  1.6-3.7 dB / -16 to -28.6 dB and 2.2-7.3 dB / -7 to -21 dB (p.8) are the Table I mean ranges: not duplicated.
- Directional couplers (design cross coupling 0.5, 0.3, 0.23, 0.17, 0.05 at 1550 nm, Fig. 5(b), p.6): no geometry
  and no measured value; kept in component notes, no rows (see judgment call 3). Edge couplers: no values.

Fab / facility: foundry not named ("provided by a foundry", p.5); acknowledgment "chip fabrication support provided by
OCP Asia, MOLEX" (p.8) is the D398 MPW / fabrication-support role, but neither org is in the registry, so fab is empty
on both rows. TSMC appears only as a funder (Joint Development Project, p.1): not fab. `process_name` "CMOS-compatible
process with 193-nm DUV lithography (8-inch multi-project wafer)" (printed flow without a foundry).

## akiyama2021a (controller-integrated cascaded AMZ triplet demux, ECOC 2021)

Rows: one `wdm.cascaded_mzi` 4-ch 400 GHz O-band CAT with flip-chip EIC: crosstalk 50 dB relative to the signal peaks
(`crosstalk_db`, type not stated); IL 2.6-5.4 dB over the 4 ports (scope unspecified); il_nonuniformity 2.8 dB
(derived); 400 GHz spacing (author_estimate); 4 channels; 2 triplet levels; 0.07 nm/C spectral shift coefficient as
70 pm/K (author_estimate, origin not stated, D256a); heater power 74-93 mW (Tab. 1, derived from the 3.3 V current minus
the monitor intercept, D80a).

Not entered:
- PIC temperature change +23 / -3 C and error-free operation at 0.33 and -0.53 C/s (p.2): no parameter for a
  closed-loop temperature tolerance / rate.
- Monitor 70 mW, logic 23 mW, total 167-186 mW, 1.7-1.8 pJ/bit (Tab. 1, p.3): `power_consumption_w` is not allowed on
  wdm (registry gap below).
- PWM period 1 us, 100 levels, 2 ms CE interval, 0.096 mA per pulse-width unit (Fig. 5(b)), 21.3 mA monitor current:
  controller electronics, not component parameters.
- "similar to those obtained without integrating controller EIC [1,4]": cited comparison, not entered (rule 3).
- Monitor photodiodes and heaters: no performance values in this paper.

Fab / facility: PIC fab and process not stated; EIC in TSMC 180 nm CMOS is the controller IC, not a photonic part, so
TSMC is a note only; assembler not stated. No facility. Platform left empty: "Si nano-waveguide PIC", SOI / BOX never
stated (D422 / D423).

## xu2017a (flat-top CWDM (de)mux, MZIs with bent directional couplers, PTL 2018)

Rows:
- `wdm.cascaded_mzi` fabricated bent-DC demux: measured crosstalk at band centers (26.16 / 23.76 / 25.55 / 24.14 dB),
  > 20 dB over ~12 nm per channel, adjacent > 18 dB and non-adjacent > 19 dB isolation (`crosstalk_adjacent_db` /
  `crosstalk_nonadjacent_db`), excess loss 0.33 / 0.86 / 0.72 / 0.67 dB (de_embedded, reference_structure: straight
  waveguides of the same length with GCs), 1-dB ~16 nm and 3-dB ~19 nm; simulated values of the same design (crosstalk
  26.40 / 27.45 / 26.79 / 24.49 dB, > 20 dB over 12 nm, isolation > 20 dB, 1-dB ~16 nm, 3-dB ~20 nm); 20 nm spacing
  (design); 4 channels, 2 filter levels, L1-L9 arm length differences, 350 nm width, 220 nm core, 2 um BOX, 1 um SU-8,
  5 um sharp bends, footprint ~300 x 100 um (derived), simulated ng ~4.14.
- `splitter.directional_coupler` bent DC1, DC2 / DC2', DC3 (fabricated, D80e; design / simulated values only): design
  coupling 50 / 20 / 4 % (author_estimate), simulated coupling variation 0.07 / 0.04 / 0.01 over 1250-1350 nm,
  simulated excess loss < 0.1 dB on each (bound stated for all bent DCs, D552), Rin 20.5 / 15 / 11 um as
  `min_bend_radius_um` (cheung2019 / bayoumi2025 precedent), theta 22.5 / 31.5 / 40.5 deg, gap 125 nm, width 350 nm.
- `wdm.cascaded_mzi` straight-DC comparison demux (design): simulated crosstalk 10.39 / 15.85 / 20.23 / 16.39 dB.
- `splitter.directional_coupler` straight DC1 / DC2 / DC3 (design): simulated coupling variation 0.4 / 0.2 / 0.06,
  gap 200 nm.
- `fiber_chip_coupler.grating` TE GC: IL ~5 dB (scope unspecified), 70 nm shallow etch, 220 nm core.

Not entered:
- 0.5-dB bandwidth ~13 nm measured and ~15 nm calculated (p.3-4, Table I): no wdm 0.5-dB nm parameter.
- Ideal-splitter filter spectra (crosstalk < -20 dB over 12 nm, Fig. 2(a)(c)(e)): idealized calculation, not a
  component.
- Simulated tolerance "wavelength deviation < +/-5 nm and coupling ratio variation < 0.01 for width error < 10 nm"
  (p.3): no parameter for a shift per width error (same gap as yen2020).
- Simulated neff ~2.43; "excess losses calculated to be negligible" (no number); Table I summary (~-20 dB XT, ~1 dB EL)
  duplicates the measured rows; other works in Table I (rule 3).

Fab / facility: "We fabricated" (p.3), both authors at Zhejiang University: fab org_zhejiang_university on the
fabricated rows (demux, bent DCs, GC). No facility named. No process_name (EBL in-house flow, nothing printed as a
named process).

## Judgment calls for the auditor

1. yen2020 Table I channel-to-wavelength mapping: CH1 = 1510 nm everywhere, but Fig. 5(a) / Fig. 6 label 1550 nm as
   CH2, 1570 nm as CH3 and 1530 nm as CH4, while the Fig. 7(c) legend maps CH2 / CH3 / CH4 to 1530 / 1550 / 1570 nm.
   Table I CH2-CH4 rows carry wavelength_nm 1530 + wavelength_max_nm 1570 with the channel label in condition and a
   note, not one wavelength (D159 spirit). Alternative: adopt the Fig. 7(c) legend (Table I is its companion).
2. yen2020 IL scope `unspecified`: the spectra are clearly normalized (peaks near 0 dB) but the reference is never
   stated. Same for akiyama2021a 2.6-5.4 dB and the xu2017a GC ~5 dB ("insertion losses of the grating couplers"; per
   coupler likely but not stated).
3. yen2020 directional couplers not entered as rows (design coupling coefficients only, no geometry); xu2017a bent DCs
   entered because the paper gives simulated performance and geometry. cheung2019 precedent would allow yen2020 DC rows
   with split_ratio_pct author_estimate.
4. xu2017a design coupling ratios 0.5 / 0.2 / 0.04: the sentence cites ref. [10] (flat-top scheme); kept as
   author_estimate design values (D80i borderline).
5. akiyama2021a crosstalk 50 dB entered without qualifier ("suppressed down to -50 dB relative to the signal peaks");
   heater power 74-93 mW as `tuning_power_mw` derived; 400 GHz spacing author_estimate (spacing of the input signal).
6. akiyama2021a platform empty (no SOI statement), unlike the merged lit:akiyama2021 rows, whose paper states 220 nm
   SOI; the PIC here may be a different process (akiyama2022 used 200 nm SOI), so nothing is carried over.
7. n_stages: yen2020 4 (paper's "four-stage"), xu2017a 2 (filter levels), akiyama2021a 2 (triplet levels, akiyama2021
   precedent).

## Missing orgs

- "OCP Asia" (fab role, D398 "chip fabrication support"), lit:yen2020 p.8 Acknowledgment; rows
  cmp_lit_yen2020_ft_mzi_cwdm_demux, cmp_lit_yen2020_regular_mzi_cwdm_demux.
- "MOLEX" (fab role, same sentence), lit:yen2020 p.8 Acknowledgment; same rows. Printed as "OCP Asia, MOLEX" (one
  entity or two not stated).

## Registry gaps

- `bw_0p5db_nm` on wdm: yen2020 > 10 nm (p.6), xu2017a ~13 nm measured / ~15 nm calculated (p.3-4). Proposed: full
  width where transmission stays within 0.5 dB of its peak (already a D443 candidate).
- `power_consumption_w` on wdm: akiyama2021a controller-integrated demux 167-186 mW total (Tab. 1, p.3; scope in
  condition).
- Spectral shift per waveguide-width error (nm/nm) on wdm / splitter: yen2020 0.75 nm/nm vs 6 pm/nm (p.3, Fig. 4,
  simulated), xu2017a < +/-5 nm for < 10 nm width error (p.3); D561 already lists width sensitivity of centre
  wavelength.
- Closed-loop temperature tolerance of a controlled filter (temperature excursion and rate with error-free operation):
  akiyama2021a +23 / -3 C, 0.33 / -0.53 C/s (p.2).
