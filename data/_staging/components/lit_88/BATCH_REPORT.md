# lit_88 batch report (photodetector, waveguide_platform), 2026-11-06

Page-1 titles: tzu2019, govdeli2025, yanikgonul2021 match their source rows. ji2024 is the arXiv preprint (2406.14296, the source row's `arxiv_id`). Its page-1 title is different ("Foundry compatible, efficient wafer-scale manufacturing of ultra-low loss, high-density Si3N4 photonic integrated circuits"), but it is the same work as the journal source row, so it was not stopped (stern2018 / oser2019 precedent, D427 / D430 / D433). The journal version was not read. govdeli2025 and yanikgonul2021 are also arXiv texts of their journal papers. No paper is only a correction or erratum, and no text layer is garbled. Dry-run: +46 components, +271 metrics, 0 errors (the one warning is on merged row `cmp_lit_ni2025b_pimmwc-m18`, not this batch).

| paper | components | metrics |
|---|---|---|
| tzu2019 | 12 (photodetector.ge_waveguide x8, phase_shifter.thermo_optic, fiber_chip_coupler.edge, waveguide_platform.straight, splitter.y_branch) | 48 |
| govdeli2025 | 7 (photodetector.apd x3 PN, photodetector.other x4 PIN) | 77 |
| yanikgonul2021 | 18 (photodetector.apd x4, waveguide_platform.straight x7, fiber_chip_coupler.edge x4, waveguide_platform.transition x3) | 93 |
| ji2024 | 9 (resonator.ring x5, waveguide_platform.straight, laser.comb x3) | 53 |

## Not entered, and why

tzu2019
- RF output power at 1-dB compression (2.5 / -4.7 / 9 / 13 / 8 / 14.3 / 10 / -7 dBm; -0.4 dBm at 18 GHz, abstract and Table I): no parameter (`saturation_power_dbm` is an input power). The photocurrents are entered as `saturation_photocurrent_ma`, and the RF powers are in the condition text.
- OIP3 values (p.5, Fig. 11) and CMRR > 37 dB / 38 dB (p.8, p.9): no parameter. CMRR was rejected in D81.
- Values not entered: the 8-PD saturation current "expected as high as 70 mA" (a projection), the phase-shifter consumed power of 0.028 W (operating point not stated), and the spiral inductor's 380 pH / 2 ohm / 10 fF (no parameter). The MZ DLI FSR of 38 GHz is also out, because `fsr_ghz` is not allowed on photodetector; 0.8 nm is entered. The link gain (Fig. 21) is a system value.
- Table I values of other works and the intro values for refs [11]-[20] are cited values. The authors' earlier 4-PD conference paper (ref. [22]) is extended by this journal paper, so its values are kept (D408).
- Grating couplers: no isolated value.

govdeli2025
- Interlayer transition losses (0.8-2.0, 0.3-0.6, < 0.3, < 0.15 dB, p.3): cited from the authors' ref. [26] (rule 3).
- Several EQE values are not entered because the junction (PN or PIN) is not stated (D159): 32 % (7.5 um) vs > 70 % at 487 nm, 75-85 % at 650-700 nm, about 20 % / 80 % at 600 nm (20 / 400 um), 40 % / 56 % at 785 nm (200 / 400 um), and peak > 84 %. These are in the component notes where relevant.
- Simulated absorbed fractions (Fig. 1(c), 1(d), Fig. 9): no parameter.
- Not entered for lack of a parameter: linear dynamic range > 50 dB; TE/TM EQE ratios (< 0.48 / < 2 / < 1.4 / < 3 dB); 5.6 kOhm um resistance per length; 0.0114 fF/um estimated capacitance per length; built-in voltage 0.85 V.
- Edge couplers were used only for de-embedding, with no values.
- Bandwidths at biases other than 10 V (Fig. 5) and lengths other than 200 / 400 um: no row per length was created for figure-only data.

yanikgonul2021
- Expected SiN-Si end-fire loss <= 1 dB is from the authors' ref. [25] (rule 3).
- Not entered for lack of a parameter: dynamic range > 50 dB; drift and reset behaviour (Supp. S4, S5); junction offset Delta_j (120 / 150 nm); doping levels.
- Table 1 values of other works: cited.
- The total fiber-to-Si-rib insertion loss of 7.1 +/- 0.4 dB (Eq. (S3)) is a path total, so it is in the APD notes.

ji2024
- Not entered for lack of a parameter: dispersion D2 / D3 values; thickness uniformity (9 nm / 1.1 % vs 42 nm / 6.1 %); RMS roughness (0.3 nm film, 0.25 nm top, 1-1.5 nm sidewall upper limit, 0.76 nm annealed SiO2); thermal absorption rates kappa_abs; Cu concentration.
- WDM couplers (Fig. 4(e), (f)): design statement only, no measured number. Damascene comparison wafer: no component values.
- Soliton figure label lambda_0 (undefined) and phase noise (figure only): not entered. Fig. 1(b) survey: cited.
- The Fig. 2(c) 100 GHz ring (230 um radius) has no performance metric (rule 9).

## Missing orgs (registry)

None needed by a row. Used: `org_aim_photonics`, `org_amf`, `org_astar_ime`, `org_epfl`, `org_center_of_micronanotechnology`.

## Registry gaps (skipped value, locator, proposed definition)

- `rf_output_power_dbm` (photodetector; candidate since lit_68): tzu2019 p.4-8 (2.5, 9, 13, 14.3, 8, 10, -4.7, -7 dBm). Definition: RF output power at the stated compression criterion, frequency, bias and photocurrent.
- `oip3_dbm` (photodetector): tzu2019 p.5 Fig. 11 (27.5, > 20, 22.5, 18 dBm). Definition: output third-order intercept point at the stated frequency and photocurrent.
- `dynamic_range_db` (photodetector; lit_68 candidate): govdeli2025 > 50 dB (p.7), yanikgonul2021 > 50 dB (p.4). Definition: linear dynamic range of the photocurrent vs input power.
- `pdl_db` widened to photodetector: govdeli2025 p.13 (< 0.48 / < 2 / < 1.4 / < 3 dB, TE/TM EQE ratios).
- `absorbed_fraction_pct` (photodetector, simulated; D417 candidate): govdeli2025 Fig. 1(c), (d).
- `kappa_abs_mhz` (resonator): ji2024 Supp. Fig. S3 (7.9, 8, 6.2, 4, 3.6 MHz) and p.7-8 (2.8-7 MHz, +3.5 MHz after UV). Definition: thermal absorption loss rate kappa_abs / 2 pi.
- `d2_khz` (resonator): ji2024 Fig. 3(g) (45.86, 25.26, -6.277, -43.47 kHz). Definition: second-order integrated dispersion D2 / 2 pi.
- `fsr_ghz` on photodetector: tzu2019 38 GHz (p.8).
- `rms_roughness_nm` (D418 candidate): ji2024 p.3, Supp. p.16, p.18.

## Judgment calls for the auditor

1. tzu2019 fab `org_aim_photonics`: the abstract says the PDs use the AIM Photonics foundry, and the acknowledgment names AIM's MPW run (rule 12 foundry clause, D398). The UCSB staff who assembled and submitted the layouts are thanks, not fab. Platform is left empty on all rows: SOI or BOX is never stated (D423).
2. tzu2019 5.7 dB edge-coupler loss is `author_estimate` per_facet + loss_breakdown, because it rests on the nominal 0.85 A/W internal responsivity. The 0.85 A/W itself is entered as `author_estimate` with ref_plane on_chip (nominal, origin not stated). Delete it if nominal PDK values are held to be out of scope.
3. tzu2019 wavelengths: bandwidth and saturation rows carry 1550 nm with `wavelength_inferred` true. The 21 GHz single-PD saturation point sits at -5 V, taken from the Fig. 10(b) summary condition. The balanced-PD saturation point has no bias, because Fig. 17 shows several biases.
4. tzu2019 metal-line 4-PD array: 31 mA / 10 dBm stays on this row (p.4 explicit). The conclusion and Table I say "4-PD array with 12 GHz bandwidth", and Fig. 7 gives this array 12 GHz at 30 mA, so there is no D159 conflict. The 2-PD responsivity follows the text (0.21) rather than Table I (0.22).
5. tzu2019 Y-junction "nominal insertion loss < 0.35 dB" is stored as `excess_loss_db` lt (rule 6), `author_estimate`.
6. govdeli2025 subtypes: PN-junction designs are `photodetector.apd` because avalanche was characterized on PN devices. PIN designs are `photodetector.other`, following the virot2014 precedent. Platform `si_sin_multilayer` (hu2021a precedent), test_structure true.
7. govdeli2025 family statements: breakdown "approximately 13.5 V for PN devices" and "> 20 V for PIN devices" are entered on every row of that junction type. "< 1.5 nA / < 150 pA below 12 V" is entered on the VIS / NIR rows of Fig. 3. "< 1 pA for PN NIR-PDs across 20-400 um" is entered on both PN NIR rows. "< 20 nA in avalanche mode" (Table 2 NIR row) is entered on both NIR PN rows. These are bounds that hold for each named device, unlike the D254 typical-value case. Move them to notes if D254 is read to cover them.
8. govdeli2025 linear-mode bandwidths at 10 V are figure reads (`extracted_from_figure`) per length, because the printed "up to 18 GHz (PIN)" / "13 GHz (PN)" are not tied to a length. The 400 um PIN reads about 17.4 GHz against the printed 18 GHz.
9. govdeli2025 dark-current conflicts are kept with notes (D417). p.12 prints about 200 pA (200 um PIN) and > 500 pA (400 um PIN), but p.9 prints 5 +/- 0.5 pA and Fig. 4(e) is on a pA scale. The 200 um PIN value is figure-read at about 2.4 pA. The 200 um avalanche bandwidth is printed as 11 GHz (p.14, Table 2) vs 10 GHz (p.15); 11 GHz is entered.
10. Gains and GBPs computed by the paper's Eq. (1) or as M x BW are `derived` (srinivasan2020 precedent). Responsivities and EQEs referenced to a de-embedded on-chip input are `measured` with method reference_structure / cutback and ref_plane on_chip. Downgrade them to derived if D394 / D166 is extended to de-embedded PD input powers.
11. yanikgonul2021 fab `org_astar_ime`: the foundry is unnamed (p.8), and the author contributions say H.T. (IME) "contributed to the device fabrication" (D395 / D399). Empty it if that wording is held too weak.
12. yanikgonul2021 Supp. Fig. S1(c) values are read per width (`extracted_from_figure`, mean over several devices). These cover SiN loss, fiber-SiN per-facet loss, SiN-Si end-fire loss and Si absorption loss for W = 450 / 600 / 900 nm. W = 750 has no Si test structures (S1). The SiN-Si butt junction in the same layer is `waveguide_platform.transition` with platform `si_sin_multilayer`. The Si "propagation loss" (about 6.4-8.3 x 10^4 dB/cm) is absorption-dominated; doping of the test waveguides is not stated.
13. yanikgonul2021 G > 10^5 and G about 10: bias -15 V is taken from the same sentence (p.4).
14. ji2024 D403: q_intrinsic and dB/m losses from kappa_0 are `author_estimate`. kappa_0 itself stays `measured` (ye2023 m13 precedent), but it has the same coupling-regime ambiguity, so rule on both together. Figure-printed labels (histogram mean / median, field map, width series) are `measured` with "printed figure label" in notes, not `extracted_from_figure`. The conclusion's average Q of 24.17 million is kept with its conflict against the 9.4 MHz mean.
15. ji2024 fab `org_epfl` + facility CMi (koyaz2026 / D419 construction). Soliton microcombs are `laser.comb` (girardi2025 precedent). Soliton pulse widths from figure labels are `author_estimate` (origin not stated). Core thicknesses: 720 nm `measured` (film, 1.2 % variation) on the process rings and spiral; 820 nm `design_target` on the soliton rings (wafer not stated).
16. ji2024 RTA-study rings: one population row (D165 analogue) with the pre- and post-RTA kappa_0 statistics. Cross-section and band are not stated (band unspecified).
