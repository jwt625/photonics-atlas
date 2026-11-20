# Batch lit_214 report

Distilled 2026-11-20 (verified_on 2026-11-20). Five papers, all VCSELs (`laser.vcsel`). Dry run:
`merge_component_staging.py data/_staging/components/lit_214 --dry-run` -> +12 components, +65 metrics, 0 errors (one
WARN concerns an already merged row of another paper, cmp_lit_ni2025b_pimmwc).

All five cached texts match their source rows (page-1 titles; chang2008 title text has a missing space, goncher1996's
page-1 text layer cuts the first characters of each title line). No correction / erratum. Text layers clean; figure
values and the lu1996 p.9 temperature checked on the page renders. goncher1996 has no page_01 render (title page
read from text only).

## lit:lu1996 (IEEE JQE 32(8), 1996, 13 pages)

Components / metric rows: 5 / 21

| component | metrics |
|---|---|
| cmp_lit_lu1996_vcsel_16um_rt_design | 1: 13 mW maximum output at 90 K (Fig. 1(b)) |
| cmp_lit_lu1996_vcsel_20um_biparabolic | 5: Ith 1.7 mA minimum at 100 K, Vth 1.8 V at about 100 K (Sec. VI), Vth < 2.4 V over 80-300 K, series resistance 40 ohm (300 K) / 50 ohm (100 K) |
| cmp_lit_lu1996_vcsel_16um_subma | 2: Ith about 0.7 mA from 80 K to 5 K, Vth < 3 V |
| cmp_lit_lu1996_vcsel_16um_linear | 9: 12 mW at 6 K, Vth 4.5 V (150 K) / 6.5 V (6 K), Rth about 1000 K/W (derived), f3dB 8.1 GHz (100 K) / 10.8 GHz (10 K), power efficiency 23 % (77 K) / 20 % (6 K), pulsed lasing wavelength 798-808 nm (Fig. 12 read) |
| cmp_lit_lu1996_vcsel_10um_biparabolic | 4: Ith 3.5 mA / Vth 2.8 V at 75 K, Ith 4.1 mA / Vth 4.2 V at 6 K |

Values not entered and why:
- Fig. 5 (20 um biparabolic VCSEL at 80 K: Ith 2.2 mA, Vth 1.8 V, slope 75 %, 22 mW at 25 mA, peak PCE 32 %, > 28 %
  over 7-22 mA) and the abstract's 22 mW / 32 %: p.8 calls "32 % at 77 K for a 20-um VCSEL with biparabolically
  graded heterointerfaces" the authors' previous result, ref. [2] (Lu et al., IEEE PTL 7, 1995). D259a / D408. In
  component notes.
- Abstract "12 GHz for a 16 um diameter device at 80 K": no body sentence or figure supports it (Fig. 16 reads about
  8 GHz near 75-100 K); abstract "1.75 V" threshold voltage noted on the 1.8 V row.
- Slope efficiencies in % (> 90 % RT-design device below 100 K, approaching 100 % / > 70 % for the 16 um linear
  device): no %-slope-efficiency parameter (registry gap).
- Threshold current densities 540 / 350 A/cm2: no parameter (D431 candidate).
- Power dissipation at 100 K (Fig. 8: 3 mW at threshold, 6 / 9 / 32 mW at 1 / 2 / 10 mW output): no parameter
  (moser2011 precedent).
- Photoreflectance cavity mode 807 nm and PL peak about 845 nm at room temperature (Fig. 3): the sample is "the
  VCSEL" of the generic design section; not tied to one of the device rows (D159).
- Gain-peak / cavity-mode shift rates -2.5 / -0.5 A/K: estimated from GaAs material constants, not a device value.
- Free-space link results (2 Gb/s NRZ at 77 K, BER < 1e-13, stable 1 Gb/s eye 77-160 K at a fixed 7.0 mA): system
  level, no parameter.
- Threshold current vs temperature of the 16 um linear device (Fig. 10): no printed value (goncher1996 prints them).
- Fig. 13 doping series (three linearly graded VCSELs, I-V only): no performance metric, no rows.

Fab / facility: no fabrication statement; acknowledgment thanks one Sandia staff member for technical assistance
(staff thanks, D84b / D72). Fab and facility empty. No missing orgs.

## lit:goncher1996 (IEEE PTL 8(3), 1996, 3 pages)

Components / metric rows: 1 / 11

| component | metrics |
|---|---|
| cmp_lit_goncher1996_vcsel_16um_linear | 11: 10 mW at 6 K, Ith about 2.2 mA (100 K) / 2.8 mA (6 K) / < 4 mA over 200-6 K, Vth about 5 V (100 K) / 4.5 V (150 K) / 6.5 V (6 K), Rth about 1000 K/W (derived), f3dB 10.8 GHz (10 K) / 8.1 GHz (100 K) at 7.5 mA, pulsed lasing wavelength 798-808 nm (Fig. 3 read) |

Values not entered and why:
- External slope efficiency 70 % (100 K), 80 % (6 K), > 70 %, > 100 % near 150 K near threshold: no %-slope parameter.
- Abstract "about 70 % to 11 GHz at 6 K": body and Fig. 4 give 10.8 GHz at 10 K (lowest measured temperature);
  note on the 10.8 GHz row.
- Printed conflict kept as note (D417): Ith "~2.2 mA" minimum at 100 K vs "2.3 mA at 100 K" in the next paragraph.
- Fig. 4 inset points other than the printed 10 / 100 K values; self-heating shares < 10 % / < 20 % (model).

Fab / facility: "grown by MOCVD" (passive); staff thanks to one Sandia staff member only. Fab and facility empty.

## lit:fu2020 (IEEE Photonics Conference 2020, 2 pages)

Components / metric rows: 1 / 13

| component | metrics |
|---|---|
| cmp_lit_fu2020_cryo_vcsel_6p8um | 13: f3dB at 100 K: 50 GHz (10 mA), 36.7 GHz (2 mA), > 20 GHz (1 mA), about 45 GHz (4 mA, Fig. 1 read); at 82.1 K: 48 GHz (2 mA), 50 GHz saturated from 3 mA; Ith 0.188 mA minimum at 40 K, 4.1 mA (295 K), 0.5 mA (100 K), 0.3 mA (82.1 K); 8.9 mW at 7.5 K / 40 mA; fundamental mode 887.2 nm (200 K) / 882.5 nm (100 K) at 3 mA |

Values not entered and why:
- 6 GHz at 295 K and 26.7 GHz at 200 K ("As previously reported", ref. [4]) and the RT-VCSEL comparison (29 GHz at
  12 mA, 57 Gb/s; ref. [6]): rule 3.
- Sub-100 fJ/bit, "10 times more efficient", "100 Gb/s NRZ achievable" (Fig. 1 right axis): estimates / projections,
  no parameter.
- 1 mA bandwidth figure reads: the Fig. 1 points (about 22.7 / 32.5 GHz) and the Fig. 4 / Fig. 5 1 mA traces
  disagree by a few GHz; only the printed "over 20 GHz" (100 K) is entered.
- "Emission wavelength around 880 nm": the two printed Fig. 3 peaks are entered instead.

Platform empty: the material system is not stated (D422 / D423; merged UIUC cryo-VCSEL rows of OFC Th1A.3 also
empty). Fab / facility: "The fabricated devices" (passive), authors at UIUC and sdPhotonics, LLC, grants only. Empty.

## lit:chang2008 (ISLC 2008, ThA1, 2 pages)

Components / metric rows: 1 / 8

| component | metrics |
|---|---|
| cmp_lit_chang2008_vcsel_980_3um | 8: Ith 0.144 mA, slope 0.67 W/A, Vth 1.47 V, series resistance about 250 ohm at 4.4 mA, peak WPE 31 %, Pmax 3.1 mW, thermal impedance 3300 K/W (derived from 3.3 C/mW), f3dB > 20 GHz above 2 mA |

Values not entered and why:
- Fig. 4(b) BER at 35 Gb/s (4.4 mA, 0.84 Vpp, ER 5.4 dB, 10 mW dissipation, 3.5 Gbps/mW): the text assigns the
  curve to the authors' ref. [1] (Electron. Lett. 2007); D259a / D408.
- MCEF 16.7 GHz/mA^1/2: no parameter (registry gap, below).
- Simulated scattering loss / effective mode radius (2.64 -> 2.01 um), 1.73x mode volume, predicted 31 % fR gain:
  design simulation, no parameter. Long-taper (original) aperture: simulated only, no row.
- 980 nm emission: design statement, no spectrum; note only.

Platform gaas from the GaAs / AlGaAs layer labels of Fig. 1(b) / Fig. 2(a). Fab: none stated (structure and
fabrication referred to refs. [1], [2]); both authors UCSB; fab empty (D80b).

## lit:shi2010 (IEEE Photonics Journal 2(6), 2010, 8 pages)

Components / metric rows: 4 / 12

| component | metrics |
|---|---|
| cmp_lit_shi2010_zn_vcsel_device_a | 6: Ith about 0.8 mA, Pmax 9.7 mW, about 1.7 V at 2 mA, differential resistance 65 ohm at 10 mA, far-field FWHM about 9 deg, lasing peak about 840.6 nm at 1 mA (Fig. 3(b) read) |
| cmp_lit_shi2010_zn_vcsel_device_b | 3: Pmax 7.7 mW, f3dB 18 GHz at 7 mA (RT) / 13 GHz at 7 mA (85 C) |
| cmp_lit_shi2010_control_deep_zn | 2: Pmax 7.3 mW, about 2.1 V at 2 mA |
| cmp_lit_shi2010_control_shallow_zn | 1: Pmax 5.4 mW |

Values not entered and why:
- DQE about 90 % at about 1.2 mA (device A): no %-slope parameter.
- D-factor 9.5 (device B) / 6 GHz/mA^1/2 (control): no parameter. Comparison 7.7 GHz/mA^1/2 and about 100 ohm of
  refs. [1]-[8]: rule 3.
- Error-free 12.5 / 25 / 32 Gb/s operating points and 5.25 Gbit/s/mW: link-level, no parameter.
- Calculated diffraction-limited divergence about 8 deg; device A low-frequency roll-off near 3 GHz (no 3-dB value).

Fab: "details of the fabrication process have been given in our previous work [9]"; epi "was grown" (passive);
IQE (Europe) co-authors are not stated as the grower. Fab empty, IQE in notes only. No missing orgs.

## Judgment calls for the auditor

1. lu1996 20 um biparabolic row: Fig. 5 values removed under D259a because p.8 assigns the 32 % / 77 K result of a
   20 um biparabolic VCSEL to ref. [2]; Fig. 6 / Fig. 4 / Sec. VI values kept (no citation; D408), although Fig. 6
   at 75-80 K (about 2.3 mA) matches Fig. 5's 2.2 mA and may be the same earlier device. Alternative: remove the
   whole row.
2. lu1996 power efficiency 23 % (77 K) / 20 % (6 K) placed on the 16 um linearly graded row: the sentence follows the
   Fig. 13 highest-doping device, but only the 16 um linear device was measured at 6 K. Alternative: D159, notes only.
3. lu1996 and goncher1996 report the same 16 um linearly graded design (likely the same device: same Fig. 3 / Fig. 12
   wavelength plot, same 8.1 / 10.8 GHz) with different 6 K output (12 vs 10 mW) and slope statements; each paper's
   own values are entered on its own row with cross-notes; lu1996 does not cite goncher1996.
4. fu2020 50 GHz values (100 K at 10 mA; 82.1 K from 3 mA) entered as printed and `measured`, with the 50 GHz-rated
   probes / cables in the condition; no `ge` qualifier added.
5. chang2008 Fig. 3 / Fig. 4(a) values kept although the authors' ref. [1] 35 Gb/s device is a 3 um device of the same
   design (only Fig. 4(b) is attributed to ref. [1]).
6. shi2010 non-strained control VCSELs entered as rows (heermeier2025 reference-group precedent).
7. Platform: gaas on chang2008 (figure layer labels only) and lu1996 / goncher1996 / shi2010 (text states AlGaAs-GaAs);
   fu2020 empty.

## Registry gaps (skipped value + locator, proposed definition)

- `slope_efficiency_pct` (laser): external / differential quantum (slope) efficiency in %, as printed. Values:
  goncher1996 70 % at 100 K / 80 % at 6 K (p.2); lu1996 > 90 % below 100 K (p.2 Fig. 1(b)), approaching 100 % below
  100 K (p.6); shi2010 about 90 % at about 1.2 mA (p.4). Also listed in D538.
- `d_factor_ghz_per_sqrt_ma` (laser): slope of fR vs (I - Ith)^1/2 (D-factor) or of f3dB vs (I - Ith)^1/2 (MCEF), which
  in condition. Values: shi2010 9.5 / 6 GHz/mA^1/2 (p.6, Fig. 4(c)); chang2008 MCEF 16.7 GHz/mA^1/2 (p.2).
- `threshold_current_density_a_per_cm2` (laser, D431 candidate): lu1996 540 A/cm2 (20 um, 100 K, p.4-5) and 350 A/cm2
  (16 um, 80 K, p.5).
- `dissipated_power_mw` (laser): electrical power dissipated at the stated output power. lu1996 Fig. 8 at 100 K: 3 mW at
  threshold, 6 / 9 / 32 mW at 1 / 2 / 10 mW output (p.5).

## Missing fab / facility orgs

None: no paper states a fabricating org or a facility.
