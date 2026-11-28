# Batch lit_312 report

Papers: lit:boes2023 (Science 2023 review), lit:luo2017 (Optics Express 25, 24531, 2017), lit:carmon2004 (Optics
Express 12, 4742, 2004). Distilled 2026-11-28. Validation: `merge_component_staging.py data/_staging/components/lit_312
--dry-run` -> +4 components, +16 metrics, 0 errors (the 2 warnings are in other batches: guo2024a, ni2025b).

Page-1 title check: all three cached texts match their source rows; none is a correction / erratum. boes2023 is the
accepted-manuscript version (32 p, enhanced abstract p.1-2, full review from p.3); `garbled_text_layer` flags only
p.31 (reference list). luo2017 and carmon2004 text layers clean; carmon2004 equations and the Fig. 1 / Fig. 5 caption
values are garbled in text.md and were read from the page renders (p.4, p.8). luo2017 Fig. 1(b, c) and Fig. 2(c, d)
read from 300-400 dpi renders of the PDF page (scratch folder).

## lit:boes2023 (0 components / 0 metric rows)

High-level review (history, platforms, engineering concepts, spectral coverage, outlook). Every quantitative statement
is either a material constant or a value credited to cited work (e.g. EO bandwidth over 100 GHz refs. 49, 64, 122,
123; THz pulse energy 1.4 mJ and 0.9 % efficiency refs. 76, 119; comb spans refs. 53, 100, 113; WGM Q of hundreds of
millions ref. 25): rule 3, D259 / D408. Figs. 1-5 are timelines, schematics and literature spectra (Fig. 4 caption
credits refs. 49, 53, 75-83). Uncited generic statements (weakly confining waveguide-fiber interface loss < 0.5 dB in
the near infrared, p.6; proton-exchange index contrasts, p.6) describe platform classes, not a device of this paper:
not entered. No fabrication, no facility.

## lit:luo2017 (2 components / 14 metric rows)

| component | class | platform | metrics |
|---|---|---|---|
| cmp_lit_luo2017_ln_microdisk_r45 | resonator.disk | suspended_lnoi | Q_i 1.7e6 at 1539.65 nm and 6.4e5 at 774.59 nm (quasi-TM, author_estimate, D403, p.3 / Fig. 1(b, c)); Q_L 1.2e5 at 1549.32 nm quasi-TE and 2.2e5 at 774.66 nm quasi-TM (measured, p.5 / Fig. 2(c, d)); linewidth 3.5 pm (derived from Q_L, p.5); notch depths ~15 / 3.5 / 1.5 / 1.0 dB (figure reads); radius 45 um, LN 300 nm, pedestal 2 um (design_target) |
| cmp_lit_luo2017_ln_microdisk_shg | frequency_converter.shg | suspended_lnoi | SHG efficiency 0.36 %/W (printed 3.6e-6 /mW, converted, derived; p.5, Fig. 3(b)) |

Fab: empty (passive process sentences, p.3; D80b). Facility `org_cornell_nanoscale_facility` ("performed in part at
the Cornell NanoScale Facility", p.9). `process_name` empty.

Values not entered and why:
- SPDC bandwidth about 400 nm (inferred by energy conservation from the 1370 nm signal / 1783 nm idler, p.6, abstract):
  no parameter (registry gap 1).
- CAR 20.1 (single mode pair 1517.85 / 1582.12 nm) and 43.1 (two 16 nm bands at 1531 / 1571 nm) (p.8-9): no
  parameter (registry gap 2). Coincidence FWHM 810 / 850 ps is detector jitter (Fig. 5), not a device property.
- SHG output (about 6 nW at about 1.4 mW, Fig. 3(b)): no converter output-power parameter; the efficiency row holds the
  fit.
- Doublet splitting of the Fig. 1(b) resonance (about 2.7 pm read off the plot, not printed): not entered.
- Setup parts (780/1550 WDM, Fabry-Perot TBPFs with 60 nm FSR / 1.4 nm linewidth, SPDs with 15 % QE): measurement
  equipment (rule 13).
- Comparison statements ("highest reported in on-chip LN microresonators", "lower than ... [25-27]"): cited work.

Judgment calls:
1. Platform `suspended_lnoi` for an undercut LN microdisk on a silica pedestal (no LN-microdisk precedent in the
   atlas; li2019 suspended LN PhC of the same group uses it). Alternative: `lnoi_strip` (fully etched film).
2. Two rows for one disk (D396): resonator row holds Q, notch depths and geometry; SHG row holds only the efficiency.
3. Q_i rows `author_estimate` (D403): the text calls them intrinsic and Fig. 1 labels Q0 from fits, but the coupling
   regime is not determined in the text (shallow dips 0.71 / 0.80). Both marked `statistic: typical` ("two typical
   examples", p.3).
4. Linewidth 3.5 pm `derived`: the paper prints it as what Q_L 2.2e5 corresponds to (774.66 / 2.2e5 = 3.52 pm).
5. SHG efficiency reference plane `unspecified` (Fig. 3(b) axes "fundamental input" / "second-harmonic output", no
   on-chip calibration printed).
6. Pedestal height entered as `box_thickness_um` 2 (condition says it is the pedestal under the undercut disk).

## lit:carmon2004 (2 components / 3 metric rows)

| component | class | platform | metrics |
|---|---|---|---|
| cmp_lit_carmon2004_silica_toroid | resonator.disk | silica | Q 2e7 at 1545 nm (unqualified -> q_loaded, author_estimate; p.4 Fig. 1 caption) |
| cmp_lit_carmon2004_silica_microsphere_d260 | resonator.disk | silica | Q 2e6 (unqualified -> q_loaded, author_estimate, band unspecified; p.8 Fig. 5 caption); radius 130 um (derived from 0.26 mm diameter) |

Fab / facility: empty (no fabrication statement; acknowledgment names only funding: Lee Center, DARPA).

Values not entered and why:
- Thermal-model fit parameters I_h/K = 7.16 C and I_h/Cp = 18000 C/s (p.4 Fig. 1 caption): no parameter (registry gap
  3). Their ratio Cp/K (about 0.4 ms) would fit `thermal_time_constant_us`, but the paper never states a time
  constant; not computed.
- Resonance temperature coefficient a = 6e-6 /C: calculated from cited fused-silica constants (ref. [24]); rule 3.
- Thermal drift about 0.6 Angstrom and about 6 C at 1.8 mW (Fig. 1(a)): model curves fitted to the transmission, not a
  stated device value; no per-K drift printed.
- Fig. 1(b) (Q = 5e5), Figs. 3-4 equilibria (0.56 Angstrom pump offset; 0.58 / 0.52 / 0.01 Angstrom drift, 6.3 / 5.7 /
  0.1 C): calculations, not devices.
- 0.14 mm sphere fast / slow thermal times (few us / tens of ms, p.4): from Il'chenko, ref. [21]; rule 3.

Judgment calls:
1. Q values `author_estimate`: printed as properties of the cavities, but no cold-cavity spectrum or extraction is shown
   (the Fig. 1(a) data are thermally broadened at 1.8 mW). bino2018 precedent; alternative `measured`.
2. Material silica for both cavities from the general p.2 sentence and the fused-silica model constants (p.3); the
   Fig. 5 caption says only "spherical cavity". Toroid diameter and substrate are not stated (no geometry row).
3. Microsphere kept in scope as a sub-mm passive resonator (D411, ilchenko1999 precedent).

## Missing fab / facility orgs

None (Cornell NanoScale Facility is `org_cornell_nanoscale_facility`).

## Registry gaps

1. `spdc_bandwidth_nm` (frequency_converter): full span of the down-converted spectrum as stated (inferred / measured
   in condition). Skipped: luo2017 about 400 nm, p.6.
2. `car` (frequency_converter, unit 1): coincidence-to-accidental ratio of a photon-pair source at the stated pump
   power and filtering. Skipped: luo2017 20.1 and 43.1, p.8-9.
3. Thermal-nonlinearity fit parameters (resonator), e.g. `thermal_absorbed_heating_k` (steady-state temperature rise
   per absorbed-power normalization, I_h/K) and a heating-rate parameter (I_h/Cp). Skipped: carmon2004 7.16 C and
   18000 C/s, p.4 Fig. 1 caption. Low priority; the time constant they imply is not printed.
