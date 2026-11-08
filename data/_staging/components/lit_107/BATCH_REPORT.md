# lit_107 batch report (2026-11-08)

Contract: `data/_staging/components/BATCH_INSTRUCTIONS.md` with its `lit` addendum (the brief names `lit_107_INSTRUCTIONS.md`, which does not exist), skill `pic-component-distill` contracts v4-v7, DevLog-007 rulings.

All nine cached texts match their source rows (page-1 title). None is a correction, an erratum or another paper. luquegonzalez2019 has `garbled_text_layer` on p.7 only (reference list); every value comes from the clean pages 1-6. No supplement is cached for any paper. Figure values were read from the cached page renders.

Dry-run: `merge_component_staging.py data/_staging/components/lit_107 --dry-run` -> +22 components, +144 metrics, 0 errors. The one warning (ni2025b m18 / m4) is on an existing merged row, not from this batch.

| paper | components | metrics |
|---|---|---|
| purnawirman2017 | 6 (laser.dfb 5: QPS 1536 / 1566 / 1596 nm, DPS Lps 0.4 / 0.2 cm; waveguide_platform.other 1: Al2O3:Er3+ film) | 41 |
| kanazawa2016 | 1 (laser.dfb: 4-ch DML array TOSA) | 22 |
| chen2016 | 1 (laser.other: QD broad-area laser on Si) | 7 |
| guzman2017 | 2 (laser.comb: 1 GHz EC-CPMLL; waveguide_platform.straight: deep-etched InP waveguide) | 15 |
| lo2017 | 2 (laser.comb: 21.5 GHz CPMLL; reflector.other: MIR) | 14 |
| simpanen2017 | 1 (laser.vcsel) | 10 |
| zhao2026a | 0 (no registry parameter for its results) | 0 |
| trappen2020 | 5 (micro_optics.facet_lens 3: TriPleX / InP / SiP probes; waveguide_platform.straight 1 and fiber_chip_coupler.edge 1: imec test chip) | 22 |
| luquegonzalez2019 | 4 (waveguide_platform.other: nominal GRIN SSC, +10 % / -10 % duty-cycle variants, 150 um linear taper reference) | 13 |

## Not entered, and why

purnawirman2017
- Grating period of each QPS-DFB: three periods (482 / 492 / 502 nm) and three wavelengths are printed, but the paper never ties a period to a wavelength (p.5-6). No period_nm on the QPS rows (in notes).
- Optical slope efficiencies 0.3 / 0.6 / 0.6 % (QPS), 2.9 % and 1.8 % (DPS 0.4 / 0.2 cm): registry gap (see below). They are in the component notes.
- Simulated confinement factor > 85 % and pump-signal overlap > 98 % over 950-2000 nm (p.5 Fig. 2): no parameter.
- Thermal shift 0.02 nm/C: cited from refs. [22,23] (rule 3). Ref. [5] 1.7 kHz linewidth: cited.
- Voigt and Gaussian widths: in notes on the linewidth rows only.

kanazawa2016
- 4x1 MMI MUX: no stated performance, so no row (rule 9).
- Electrical crosstalk about -20 dB at 16 GHz between adjacent lanes (p.5 Figs. 9-10), simulated crosstalk (Figs. 4-5), dynamic extinction ratio > 4 dB, mask margins, receiver sensitivities, thermal wavelength shift up to 0.3 nm: crosstalk_db and extinction_db are not allowed on laser, and the rest has no parameter. In the component notes.
- LAN-WDM 800 GHz lane spacing: the standard grid (p.2 Sec. 1), not a device result.

chen2016
- Threshold current density 62.5 A cm-2 (12.5 A cm-2 per QD layer), maximum CW operating temperature 75 C (pulsed 120 C), extrapolated MTTF > 100,158 h, 29.7 % power drop over 3,100 h: no parameter (registry gaps below). Threshold current entered as derived (62.5 A cm-2 x 50 um x 3200 um = 100 mA; wang2026f precedent).
- Ageing device (210 mA = 1.75 Ith -> Ith 120 mA, 26 C): not identified with the 50 x 3200 um device of Fig. 4(a) and inconsistent with its 100 mA, so not entered (D159). Noted on the component.
- Material data (TD density, QD density, PL FWHM 29 meV): material, not component, values.

guzman2017
- RF linewidth 398 kHz (passive) and about 1.1 Hz / < 1 Hz (hybrid, RBW-limited), RF SNR > 30 / > 50 dB: no parameter (registry gap, same as guzman2019).
- Expected round-trip passive loss about 26.75 dB: design estimate with no parameter on laser.
- MIR mirror (56.6 um): geometry only, no reflectivity printed, so no row.
- Optical wavelength: not printed anywhere.

lo2017
- RF linewidth 450 kHz, RF SNR about 35 dB, time-bandwidth products 1.01 / 1.08: no parameter.
- Booster SOA3 (15 mW/A vs IBOOST, saturation above 80 mA): no gain measured, so no amplifier row (guzman2019 precedent).
- Deep / shallow waveguide widths 1.5 / 2.0 um and 100 um bend radius: no performance value, notes only.

simpanen2017
- D-factor 17.6 / 13.7 GHz/mA^0.5, K-factor 0.16 / 0.22 ns, 100 fJ/bit at 50 Gbit/s, error-free data rates: no parameter.
- Oxide aperture 4 um and mesa 15 um diameters: no aperture parameter (notes).
- Emission wavelength: the Fig. 2(b) spectra in the cached render are too small to read a peak; only the nominal 1060 nm of the title.
- Abstract threshold 0.2 mA vs text 0.15 mA (RT): text value entered, conflict in notes.

zhao2026a (no rows)
- All results are Strehl ratios and RMS wavefront errors of 3D-printed microlenses: Strehl 0.97 and RMS 0.026 lambda (about lambda/38) after three Zernike-filtering iterations, Strehl 0.96 and RMS 0.0345 lambda (non-filtering), all at 638 nm on 630 um lenses (p.6 Sec. 3.1, p.8 Fig. 4); 0.4 / 0.8 lambda spherical-aberration series (p.8, p.10, Figs. 6, 8); 85 um lens on an SM600 fiber, Strehl about 0.97 and RMS < 0.03 lambda at 658 nm (p.12, Fig. 9). There is no registry parameter for these values (registry gap below), and the lens geometry alone does not make a row (rule 9; D432 kumar2026 precedent).
- Scope: the 630 um lenses on fused-silica substrates are free micro-optics with no chip or fiber, so they are likely out of scope (D411) even with a parameter. The fiber-tip lens would be micro_optics.facet_lens.

trappen2020
- InP BH DFB laser MFD 3 um: cited from the authors' ref. [9] (rule 3). TriPleX waveguide MFD 10 um: a "targeted" value, so it is only in the probe label.
- Working distances 20 / 25 / 40 um and internal propagation lengths 95 / 164 / 90 um: no parameter (notes).
- Beam diameter 23 um at the SiP lens apex: a design calculation, not entered.
- Estimated 0.18 dB excess loss from fiber-array pitch inaccuracy and the inferred focal-spot spreads: model estimate, notes only.
- PLC-probe 5.7 dB and micromirror 3.2 dB comparisons: other works (rule 3).

luquegonzalez2019
- Simulated IL < 1 dB over more than 300 nm: no band edges printed, notes only.
- Back-reflection 14 % (nominal lens feeding a grating) and 8 % (+15 % duty-cycle lens): back_reflection_db is not allowed on waveguide_platform, and the +15 % lens has no other value. Notes only.
- Lens tip block 50 nm, centre minimum feature 80 nm, 44 / 15 periods: no fitting role-specific parameter on waveguide_platform (tip_width_nm means a taper tip, n_periods is not allowed). In core_material.
- Collimation distances (17 / 12 / 11 um): simulation, no parameter.
- Table 2 rows of other works (rule 3). The SWG edge coupler of the setup and the grating couplers of Fig. 6: no absolute values.

## Missing fab / facility orgs

None. Ids used, all in the registry: org_ntt (kanazawa2016, NTT Corporation before the 2025 rename, as the merged kazama2021 rows), org_university_college_london (chen2016, author contributions), org_smart_photonics (guzman2017, lo2017), org_imec (trappen2020 test chips).

## Judgment calls

1. purnawirman2017 on-chip laser and pump powers (output, thresholds) are `author_estimate`: the paper prints on-chip values but does not describe the fiber-to-chip referencing (D460 franken2025, D431). The DPS 0.2 cm maximum output (about 3.2 mW) is a Fig. 4(c) read, also `author_estimate`, with the reading uncertainty in notes (ji2026 m21 precedent).
2. purnawirman2017 SMSR "> 46.1 dB for all devices": entered on all three QPS rows (gt). The 1536 nm row carries the Fig. 3(b) label value 46.1 with no qualifier. It is a bound printed for every device, not a typical value for one representative row (D254 does not apply).
3. purnawirman2017 DPS linewidth (5.3 kHz) is tied to the Lps 0.4 cm device by its 1565 nm wavelength (p.7 names the best DPS at 1565 nm, p.8 measures the DPS at 1565 nm). The QPS 30.4 kHz is tied to the 1566 nm QPS row the same way. Both are `derived` (kHz -> Hz, D256).
4. purnawirman2017 Al2O3:Er3+ film background loss < 0.1 dB/cm (prism coupling, linear fit) is a `waveguide_platform.other` film row, `measured` (fit of own data, verb "estimate" quoted; neutens2025 / naraine2024 precedent). The platform is al2o3 for the lasers as well (notaros2019 precedent; simulated confinement > 85 % in the gain film). Fab is empty: the process is cited to refs. [6,21] and the paper has no fabrication statement (D433).
5. kanazawa2016: the 4-channel array chip, measured inside its TOSA, is one `laser.dfb` row with per-lane conditions (peak wavelengths, modulated average powers, Fig. 7 module powers at 80 mA as figure reads). Module-level values use ref_plane module. Fab org_ntt comes from "we fabricated a 4-channel DFB laser array chip" with all authors at NTT (D399). The designed kappa 210 cm-1 is `author_estimate` (design-stated performance, rule 4).
6. chen2016 is classed `laser.other` (broad-area FP laser), platform iii_v_on_si_epi (koninck2025 precedent). Fab is UCL: the author contributions name the UCL authors for growth and device fabrication (D439). The Cardiff co-authors' "contributed to the development of device processing" is not counted.
7. guzman2017 and lo2017: fab org_smart_photonics with the MPW process as printed. guzman2017 passive-waveguide loss 5 dB/cm is `author_estimate` (stated platform property, no measurement), and its wavelength is `band: unspecified` because the paper prints no optical wavelength. The lo2017 MIR 50 % reflectivity is `author_estimate` with the C band inferred from the 1535-1555 nm lasing (guzman2019 MIR precedent).
8. guzman2017 pulse width 272 ps is an electrical pulse at the photodiode output on a 2 GHz oscilloscope, entered as printed with that condition. lo2017 pulse widths 0.35 / 2.01 ps assume a sech2 shape and are `derived` (D76, ofc2026 Th1F.6 precedent).
9. trappen2020 probes are `micro_optics.facet_lens` (TIR mirror + aspheric lens printed on an SMF facet, dietrich2018 lens_on_smf precedent), platform polymer. They are kept as a fiber-attached passive part (D411): the probe is the paper's subject, not setup equipment (D160 does not apply). Per-interface SiP and TriPleX losses from two-coupler paths are `loopback_half` + `derived`. The SiP values exclude the 0.17 dB/mm waveguide loss. The InP 1.9 dB is `per_coupler` + `measured` (direct comparison with the bare-laser integrating-sphere power, D167). Asymmetric simulated longitudinal tolerances store the smaller side, with both sides in condition and notes. Fab is empty (printed by the authors, no site named; dietrich2018 / D83c). KNMF is a funding / support listing only (D437).
10. trappen2020 imec test chip: "test chips fabricated on the standard silicon photonics platform of imec" gives fab org_imec on the waveguide (0.17 dB/mm -> 1.7 dB/cm, derived) and edge-coupler (measured MFD 2.5 um) rows. TriPleX ("Lionix TriPleX") and HHI DFB lasers would carry LioniX / HHI as fab, but neither has an in-scope metric of its own here, so they have no rows.
11. luquegonzalez2019: the single-layer SWG GRIN spot-size converter is `waveguide_platform.other` (same-layer converter, D417 xiao2022). `mode_converter.converter` would allow bw_1db_nm, but the device does not change mode order. Coordinator may prefer mode_converter. Measured IL rows are `derived` (back-to-back divided by two, cutback set), scope per_component. The +/-10 % duty-cycle variants are sibling rows (rule 9) with only the < 1 dB at 1.58 um bound.

## Registry gaps (skipped value, locator, proposed definition)

- `slope_efficiency_pct` (laser; unit %): purnawirman2017 0.3 / 0.6 / 0.6 % (QPS), 2.9 % / 1.8 % (DPS), p.6 Fig. 3(c), p.7 Fig. 4(c). Definition: optical output power per unit optical pump power above threshold for an optically pumped laser, reference planes in condition. Already proposed by lit_15 / lit_78 (shui2026 2.76 %).
- `threshold_current_density_a_per_cm2` (laser; A/cm2): chen2016 62.5 A cm-2, p.2, Fig. 4(a). Definition: threshold current per pumped area (per active layer in condition). Already a D431 candidate.
- `max_operating_temperature_k` (laser; K): chen2016 CW 75 C (setup-limited) and pulsed 120 C, p.3. Definition: highest heatsink temperature with lasing as stated (CW / pulsed and the limit reason in condition). D431 candidate.
- `mttf_h` (laser; h): chen2016 extrapolated MTTF > 100,158 h, p.4 (doubling-of-threshold criterion, sublinear fit, 26 C, 210 mA). Definition: mean time to failure as stated (criterion, extrapolation model, stress conditions in condition; extrapolated values author_estimate per D435).
- `rf_linewidth_hz` (laser; Hz): guzman2017 398 kHz passive, about 1.1 Hz hybrid (p.3, Fig. 3(c), Fig. 4(b)); lo2017 450 kHz (p.3, Fig. 6(b)). Definition: -3 dB width of the fundamental RF beat tone of a mode-locked laser (RBW and fit in condition). D431 candidate.
- `crosstalk_db` widened to laser (array transmitters): kanazawa2016 adjacent-lane electrical crosstalk about -20 dB at 16 GHz, p.5 Figs. 9-10. Definition as the existing crosstalk_db, with electrical vs optical in condition.
- `strehl_ratio` (micro_optics; unit 1) and `wavefront_error_rms_waves` (micro_optics; unit waves, wavelength in condition): zhao2026a Strehl 0.97 and RMS 0.026 lambda at 638 nm (p.6, Fig. 4), fiber-tip lens Strehl about 0.97, RMS < 0.03 lambda at 658 nm (p.12, Fig. 9). Definition: Strehl ratio and RMS transmitted-wavefront error from wavefront measurement (Zernike terms removed in condition). Related to the D432 `surface_error_rms_nm` candidate.
- `back_reflection_db` widened to waveguide_platform (on-chip converters): luquegonzalez2019 14 % (nominal) and 8 % (+15 % duty cycle) back-reflection when feeding a grating coupler, p.6. A percentage would be converted (derived).
