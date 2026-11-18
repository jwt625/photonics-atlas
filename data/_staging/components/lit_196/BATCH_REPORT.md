# lit_196 batch report

Date: 2026-11-18. Papers: lit:chen2025b, lit:xiang2018, lit:zhu2020, lit:liu2021c (all IEEE copies; institutional
download stamp ignored; page-1 titles match the source rows). Validation: `merge_component_staging.py
data/_staging/components/lit_196 --dry-run` -> +25 components, +189 metrics, 0 errors (one pre-existing warning on
cmp_lit_ni2025b_pimmwc, not from this batch). No acknowledgment section in any of the four papers; no fab / facility
org set on any row.

## chen2025b (JLT 2025, side-coupled pi-phase-shifted ASBG add-drop filter): 9 components / 59 metric rows

- Rows: headline ADF wg 195 nm / Lg 300 um / Ld 2.5 um (wdm.bragg_cdc, sun2026a DC-FPR precedent); siblings wg 220 /
  Lg 300, wg 270 / Lg 300, wg 220 / Lg 200, wg 220 / Lg 100; Fano device Ld 0; design row Ld 5 um (Fig. 11(c),
  simulated, plus the simulated 0.058 nm/C thermal drift); grating coupler (~7 dB per coupler); 450 nm Si waveguide
  (~2.5 dB/cm).
- Not entered: fitted k13 / k14 / rt (model-fit parameters); grating corrugation width 50 / ~49 nm, duty cycle 0.65 and
  Ld offsets (no registry parameter for wdm); corrugation trapezoid angle ~45 deg (not a film sidewall angle); Fano
  slope rate 34 dB/nm (no parameter); FSR: Table I prints "Free" and the text a single peak in the 100 nm window (no
  numeric bound); simulated design noise floor -45 dB; Fig. 15 / 16 fabrication-error sweeps (curves, no device);
  Table I / II rows of other works (rule 3); ref. [23] 6.7 dB / 8.4 dB of the authors' earlier device (rule 3).
  Ld 0.5 um device (Fig. 13(h)): no printed value, no row.
- Printed conflicts (D417, in notes): the p.8 Lg-series sentence lists ER 4 / 11.2 / 13.4 dB, 3-dB width 0.44 / 0.22 /
  0.27 nm and IL 9 / 3 / 2 dB for Lg 300 / 200 / 100 um, the reverse of Fig. 14(b) and of the paper's own trend
  statement; 13.4 dB / 0.27 nm match no Lg-series point. Fig. 14 caption swaps the held parameters (and labels Lg in
  nm). p.7 prints rt 0.0117 and 0.117 for the same TMM run.
- Judgment calls: (a) per-device values for Lg 100 / wg 220-Lg 300 / wg 270 taken from Fig. 14 (extracted_from_figure,
  500 dpi render, uncertainties in notes) instead of the order-conflicted p.8 list; the Lg 200 device keeps the printed
  11.2 dB / 0.22 nm / 3 dB (middle entry, either order). (b) Table II "This work" (IL 1.2 dB, Q 6x10^3, ER > 52 dB)
  assigned to the Ld 0 device (paper calls it the apparent-Fano device; 0.25 nm width gives Q ~6.1e3). (c) Headline
  Q 6821 `derived` (printed as lambda / FWHM); Table II Q 6000 kept `measured` (no arithmetic shown). (d) Grating
  coupler ~7 dB and waveguide ~2.5 dB/cm entered `measured`, method unspecified (the paper's own chip, D167 / D632),
  1550 nm `wavelength_inferred` (design wavelength; values printed without wavelength). (e) Drop-port IL in
  `drop_loss_db` (normalization reference not stated, so no scope-bearing insertion_loss_db).

## xiang2018 (JSTQE 2018, Si3N4 SCISSOR tunable true-time delay): 3 components / 19 metric rows

- Rows: Si3N4 90 nm x 2.8 um waveguide (group index ~1.57); 8-ring Balanced-SCISSOR TTD, kappa 0.715, gap 2.1 um
  (resonator.ring, array as one row, D165): 1.6 dB on-resonance excess loss, ~1 dB at 1 GHz detuning, 4.65 dB/m total
  ring loss (derived), FSR ~25 GHz, geometry, 90 mm2 footprint; prior-run TTD with type-I couplers (gap 560 nm): 10 dB
  loss, ~8 dB/m waveguide loss, ~2.5 dB lossless-coupler calculation.
- Not entered: all delay metrics (peak delay 1800 ps, delay FWHM 3 / 5 / 3.66 / 12 GHz, 1.2 ns flat top, 0-1800 ps
  tuning, 3.4 ns max delay of kappa 0.56, ~520 ps flat top of kappa 0.91, loss per delay 0.89 dB/ns, power efficiency
  0.13 mW/ps, GDD in Fig. 15): no registry parameter. kappa values (definition amplitude vs power not printed). Sec. II
  Morton Photonics / LioniX TTD results (Figs. 1-5, refs. [36]-[38]) and the 0.1 dB/m waveguides of [31], [43] (rule
  3). Calculated Fig. 7 / 8 curves.
- No wavelength is printed anywhere: band `unspecified` with a note on every wavelength-bearing row.
- Printed conflict (D417): prior-run "total loss as high as 10 dB" vs the Fig. 14 measured normalized-loss dip of
  about 13.5 dB.
- Judgment calls: (f) the 8-ring TTD is classed `resonator.ring` (no delay-line class; SCISSOR rings are not mutually
  coupled, so not coupled_rings); (g) ring FSR and waveguide group index are stated once for the ring design shared by
  all four kappa designs: FSR on the kappa 0.715 row only (identical dimensions), group index on a separate waveguide
  row; kappa 0.56 / 0.82 / 0.91 designs have only delay values and no row; (h) the 1.6 / ~1 dB losses scoped
  `on_chip_excess` (Fig. 9(b) / 10 normalized to the off-resonance level); (i) prior-run row platform left empty (stack
  not restated, D422); (j) fab empty despite "We design, fabricate" (authors at three orgs, D154).

## zhu2020 (JLT 2020, Ge11.5As24Se64.5 chalcogenide microdisks): 8 components / 51 metric rows

- Rows: four cut-back waveguides (H 1 / 0.5 um x W 2 / 0.5 um; 0.55 / 2.6 dB/cm TM, 0.48 / 4.85 dB/cm TE at 1550 nm);
  four microdisks by BHF release time 0 / 15 / 20 / 25 min (Table II: Q_L, FWHM measured; Q_i and alpha
  author_estimate, D403), 0-min row also simulated Q_i ~3.49e6, FSR 2.7 nm (author_estimate, "estimated"), R 60 um.
- Not entered: Table II ER (linear dip fraction, no definition; no linear notch-depth parameter), Q_s and alpha_s
  (scattering Q / scattering loss share: no parameter), "50 %-60 %" scattering increase (derived narrative), simulated
  mode-confinement factors (Fig. 4(a)), Fig. 6 suspension-depth simulations (not tied to a sample), etch rates (process
  data), radius of the suspended samples (only the Fig. 5 example is R 60 um; D159).
- Judgment calls: (k) Table II wavelengths `c_band` inferred (no resonance wavelength printed; 1550 nm simulation /
  cut-back wavelength and 1.1e6 x 1.4 pm ~1.54 um); (l) platform `other` (chalcogenide not in the enum), fab empty
  (first-person fabrication, authors at SYSU and Jinan University, D154).

## liu2021c (JLT 2021, high-order adiabatic elliptical-microring filters): 5 components / 60 metric rows

- Rows: 2nd-, 3rd-, 4th-order single-channel AEM filters (wdm.mrr; FSR ~37 nm, 3-dB width 2.6 / 1.3 / 1.4 nm, ER ~35 /
  > 45 / > 45 dB, excess loss ~0.5 / ~1 / ~1.5 dB from Table I, de_embedded against the on-chip straight reference);
  2nd-order design values (FDTD FSR 38 nm, ER 35 dB, < 0.2 dB, 2.8 nm); 8-channel 2nd-order AEM WDM filter (3.1 nm
  measured / 3.2 nm design spacing, adjacent ~18 dB, non-adjacent ~25-30 dB, ~0.8 dB); AEM bend row with the simulated
  < 0.009 dB/90 deg and < 0.1 dB/cm.
- Not entered: roll-off rates 6.8 / 13.2 / 21.9 dB/nm (no parameter); ellipse half-axes La / Lb 2.8 / 2.3 um and the
  8.87 nm per-channel increment (no parameter; in notes); bent-DC angle 80 deg (coupling_angle_deg only on splitter);
  bent-DC coupling loss ~0.07 dB and ring-ring kappa values (sub-element / design, notes); Reff 2.556 um (equivalent
  radius, not a physical one); Table I rows of other works and the authors' earlier [11] / [22] results (rule 3).
- Printed conflicts (D417): 4th-order Table I excess loss ~1.5 dB vs "excess loss less than 1 dB" for all orders
  (p.2); demonstrated channel spacing ~3.2 nm (abstract / conclusion) vs measured ~3.1 nm (p.5).
- Judgment calls: (m) `wavelength_nm` 1550 on excess-loss rows from "operating around 1550 nm" (D393, not inferred);
  (n) kappa1 = 25 % entered as simulated `power_coupling_pct` (the paper defines kappa_i as power coupling ratios);
  (o) min_bend_radius 1.89 um kept `design_target` with `approx` as printed (Ra = Lb^2 / La).

## Missing fab / facility orgs

None: no paper names a fabricating org or a facility; no acknowledgment sections.

## Registry gaps (skipped value + locator; proposed definition)

- `group_delay_ps` (resonator / delay structures): xiang2018 peak delay 1800 ps (p.5 Fig. 9(a)), 1.2 ns flat top (p.5
  Fig. 10), 3.4 ns (p.6 Fig. 12). Definition: peak or flat-top group delay of a delay structure at the stated tuning
  state.
- `loss_per_delay_db_per_ns`: xiang2018 0.89 dB/ns (p.5; Table I 8.9E-4 dB/ps). Candidate already listed in D434.
- `delay_bw_ghz`: xiang2018 delay FWHM 3 / 5 / 12 / 3.66 GHz (p.5-7). Full width at half maximum of the group-delay
  spectrum (distinct from a transmission 3-dB width).
- `rolloff_db_per_nm` (wdm): liu2021c 6.8 / 13.2 / 21.9 dB/nm (p.5); chen2025b Fano slope rate 34 dB/nm (p.10 Table
  II). Passband edge steepness as defined by the paper.
- `extinction_ratio_linear` or a dB rule for undefined linear ER: zhu2020 Table II 0.72 / 0.92 / 0.7 / 0.3 (p.6).
- `q_scattering` / scattering-loss share: zhu2020 Table II Q_s 1.02e7 / 1.16e6 / 6.12e5 / 1.02e6 and alpha_s 0.04 /
  0.36 / 0.68 / 0.41 dB/cm (p.6) (Q_scat candidate already in D558).
- wdm grating geometry: corrugation width (chen2025b 50 nm design / 49 nm fabricated, p.5 / p.8) and fill_factor on
  wdm (duty cycle 0.65, p.5) (D540 / D552 candidates).
- `coupling_angle_deg` widened to wdm / resonator bent couplers: liu2021c alpha 80 deg (p.3).
