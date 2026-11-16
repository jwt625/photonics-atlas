# lit_142 batch report

Distilled 2026-11-15. Papers: lit:zheng2020, lit:gao2022, lit:kita2021 (benchmark-citation papers, D577).
Validation: `merge_component_staging.py data/_staging/components/lit_142 --dry-run` -> +12 components, +64 metrics,
0 errors. The only warning concerns merged rows of another batch (ni2025b).

| paper | components | metric rows |
|---|---|---|
| zheng2020 | 4 | 24 |
| gao2022 | 4 | 10 |
| kita2021 | 4 | 30 |
| total | 12 | 64 |

Page-1 title check: all three cached texts are their source rows' papers. zheng2020 is arXiv v1 titled
"Nonvolatile electrically reconfigurable integrated photonic switch" (the Adv. Mater. title adds "Enabled by a Silicon
PIN Diode Heater"); same authors and content, accepted as the same work (D430 / D433). gao2022 is the arXiv v1 of the
Nat. Commun. paper (same title). kita2021 is the JLT article. No correction / erratum, no garbled text layer.

## zheng2020 (Adv. Mater. 2020, GST on Si PIN heaters, arXiv text with supplement)

Rows: 5 um / 10 nm GST waveguide switching unit and 4 um / 20 nm GST unit (`phase_shifter.phase_change`); R 20 um ring
switch (`resonator.ring`) and its 3 um GST switching unit (`phase_shifter.phase_change`, D396, fang2021 precedent).

- 5 um unit: total IL ~1.6 dB and ER ~1.2 dB from Fig. S2(a) (reference-device subtraction after each fabrication step,
  `per_component` / `reference_structure`, measured); endurance > 500 cycles (printed "more than 1,000 times (500
  cycles)"); Set ~10 mW / Reset ~110 mW pulse powers `derived` (authors' estimate from measured I-V curves, p.12;
  which device's I-V is not stated); 1/e cooling dead time 0.035-0.245 us read off the Fig. S3(b) inset
  (`extracted_from_figure`, +/- 0.01 us).
- 4 um / 20 nm unit: ER ~5 dB over Fig. 3(c) (1525-1565 nm axis, `wavelength_inferred`).
- Ring: ER up to 14.7 dB (`le`), wavelength about 1549.6 nm read off the Fig. 4(c) dip (`wavelength_inferred`); about
  5 dB contrast held during cycling at 1549.57 nm read off Fig. 4(d) (`extracted_from_figure`). Ring cell endurance
  > 500 cycles `derived` (printed 1,000 transitions halved with the paper's own p.3 equivalence).

Not entered: all per-length values (PIN loss ~0.02 dB/um, ring-extracted ~0.1 / 0.08 / 0.2 / 0.3 / 0.23 dB/um,
1.25 dB/um, resonance shift ~0.02 nm/um, loss modulation ~0.25 dB/um, Table S1 simulated attenuations, theoretical ER
~1.77 dB/um; D250 rejected per-length phase-shifter loss / extinction); the IL contributions of the 5 um unit (doping
< 0.4 dB, metal ~1 dB, aGST ~0.4 dB) are in component notes rather than rows; simulated neff values; "~10 kHz"
operating speed (not a measured bandwidth); grating couplers (pitch 744 nm, duty cycle 0.5, ~25 deg, optimized for
~1,550 nm; geometry only, no performance: not a row, rule 9); the 4 um / 10 nm device of Fig. 3(d) (only a
% transmission change trace: no row); Fig. S2(b) ring series and Fig. S4 ring (2 um unit, 330 nm gap; per-length or
transient-only data).

Judgment calls:
- Endurance: Fig. 3(e) and Fig. 4(d) axes are labelled "Number of Set/Reset cycles" up to 1,000, while p.3 equates
  1,000 transitions with 500 cycles; rows use 500 cycles with a D417 note.
- Ring platform `soi_rib` from the switching-unit cross-section (p.3); the ring's own etch is not restated.
- Fab `org_university_washington`: author contributions (p.15) say J.Z. fabricated the devices; J.Z. is at UW (D395).
  Stanford co-authors only "helped with GST deposition and process characterization" (not fab).

Missing orgs: Washington Nanofabrication Facility / Molecular Analysis Facility (University of Washington), facility,
p.14 Acknowledgements "Part of this work was conducted at ...". (Also reported for fang2021, D418 org-round list.)

## gao2022 (Nat. Commun. 2022, material-limited Q, arXiv text, no supplement)

Rows: SiO2 microdisk (`resonator.disk`, silica), Si3N4 Damascene ring (`resonator.ring`, sin), Al0.2Ga0.8As-on-insulator
ring (`resonator.ring`, algaas), Ta2O5 ring (`resonator.ring`, other).

- q_intrinsic (418 M, 30.5 M, 2.01 M, 2.69 M) and q_external (943 M, 43.9 M, 2.51 M, 7.75 M) from the Fig. 1(b) low-power
  fits: `author_estimate` (D403: the paper does not state how the coupling regime was determined; all fitted
  under-coupled). Band `c_band` inferred (no wavelength with the values; EDFA setup, Fig. 4(a) 1530-1570 nm).
- Geometry: SiO2 8 um wet oxide (`core_thickness_nm` 8000 derived, D157); AlGaAs 3 um thermal SiO2 under the bonded
  film. No ring / disk dimensions are stated.

Not entered: Table 1 Q_abs (3915 / 287 / 2.04 / 2.36 M), sigma_abs (0.0065 / 0.122 / 28.4 / 15.4 dB/m) and measured n2
(22.2 / 1658 / 27.3 x 1e-20 m2/W): material properties without a registry parameter (registry gaps below); Fig. 2(d)
resonance shift with chip temperature (-1.83 / -2.84 / -13.1 / -0.996 GHz/K; no GHz/K drift parameter, and a pm/K
conversion needs a wavelength the figure does not state); reported n2 column and the SiO2 n2 (cited, rule 3);
AlGaAs Q0 3.52 M (ref. 27) and Ta2O5 / TiO2:Ta2O5 material Q 5 M / 25 M (ref. 59), cited (rule 3); Fig. 3(d)
Kerr / thermal ratios (intermediate quantity); Eq. (4) parametric-threshold contours (calculated).

Judgment calls:
- Fab empty on all four rows: author contributions (p.9) say the co-authors "provided the samples" (SiO2: Caltech;
  Si3N4: EPFL; AlGaAs: UCSB; Ta2O5: NIST); Methods use passive verbs. Not a fabrication statement under D80b (white2024
  precedent, lit_07 audit). Coordinator may rule otherwise.
- D403 applied strictly although the Si3N4 / Ta2O5 fits include the facet Fabry-Perot background (Eq. 6), which could
  in principle fix the regime; the paper does not say it does.

Missing orgs: none (no fab or facility statement).

## kita2021 (JLT 2021, asymmetrically doped Si MZI thermo-optic switch)

Rows: non-doped and 1e18 cm-3 p-doped MMI current-injection phase shifters (`phase_shifter.thermo_optic`); MZI switch
without and with the TiN heat sink (`switch_fabric.other`, single switch element, D158).

- MMI phase shifters: IL 0.1 dB (non-doped, "over the entire C-band") and 0.24 dB (doped; C band inferred from the
  same sentence), `per_component`, method unspecified (isolation method not stated); MMI 1.24 um x 9.5 um, Si 210 nm.
- Switches: P_pi 15.0 / 22.6 mW and ER 38 / 41.7 dB at 1550 nm (Fig. 7, Table I); IL 0.9 / 1.0 dB (Table I assigns the
  Fig. 6 value 0.9 dB to the switch without heat sink; scope `unspecified`, C band inferred); 1/e thermal time constants
  (t_fall 3.28 / 0.50 us, t_rise 1.30 / 0.36 us; `thermal_time_constant_us`, the paper's definition is a 1/e
  temperature change, not 10-90 %); simulated P_pi 16 / 21 mW and time constants 1.64 / 1.63 and 0.64 / 0.65 us
  (`simulated`, D80e); footprint 1800 um2 derived from 60 x 30 um2; Si 400 x 210 nm waveguide.

Not entered: ER ~41 dB estimated from the measured MMI losses (p.4; stated once for the asymmetric design, D254, in
notes); FOM 34.4 / 9.7 mW us (no parameter); "0.4 us" switching speed (average of t_rise and t_fall, the FOM tau_s);
0.1-dB down-wavelength band ~100 nm (p.2; no phase-shifter bandwidth parameter, and the sentence does not say which
MMI); heat-sink geometry (TiN 200 nm, 0.8 um above the Si; in notes / cladding); 40 x 15 um2 and 0.5 dB projections;
directional couplers (5 um bend radius, no measured values: not a row); 14 % simulated speed-up; Table I rows of other
works and the authors' 10-electrode MMI switch (refs. [19], [20], [22], [23], [24]; rule 3).

Judgment calls:
- Table I lists the no-heat-sink time constants as Rise 3.28 / Fall 1.30 us, swapped against the text (t_fall 3.28 us
  = heating step, t_rise 1.30 us); rows follow the text with a D417 note on both rows. The heat-sink values agree.
- Fab and `process_name` empty: "fabricated using a CMOS foundry" names no foundry, node or flow (Contract v7).
- Platform `soi` (SOI layer stated, etch not stated).

Missing orgs: none (the foundry is not named).

## Registry gaps

- `q_absorption` (resonator, "1"): absorption-limited quality factor from photothermal spectroscopy; gao2022 Table 1
  (3915 +/- 177 M SiO2, 287 +/- 51 M Si3N4, 2.04 +/- 0.16 M AlGaAs, 2.36 +/- 0.28 M Ta2O5; p.4). Proposed definition:
  "material absorption-limited Q (Q_abs = omega / kappa_abs), method and modelled inputs in notes".
- `absorption_loss_db_per_cm` (resonator / waveguide_platform, dB/cm): propagation loss from material absorption only;
  gao2022 Table 1 sigma_abs 0.0065 / 0.122 / 28.4 / 15.4 dB/m (p.4). Distinct from total `prop_loss_db_per_cm`.
- `thermal_drift_ghz_per_k` (resonator, GHz/K; candidate already listed in D443): gao2022 Fig. 2(d) caption -1.83 /
  -2.84 / -13.1 / -0.996 GHz/K (p.3).
- `n2_m2_per_w` (material Kerr index measured in a device): gao2022 Table 1 (p.4). Likely out of scope (material
  property); listed for the coordinator.
- `bw_0p1db_nm` on phase_shifter (or a criterion bandwidth with the level in condition, D539 candidate
  `criterion_bw_nm`): kita2021 0.1-dB down band ~100 nm (p.2), device identity unclear.
- Per-length PCM loss / extinction (dB/um) and resonance shift per um (zheng2020 p.3, p.7, p.9, p.21-23): rejected in
  D250; listed only because this paper reports almost all its loss data per length.
