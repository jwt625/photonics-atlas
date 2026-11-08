# lit_111 batch report (2026-11-08)

All eight cached texts match their source rows (page-1 title). None is another paper, a correction or an erratum. li2023a carries the line "Corrected 4 April 2024" on p.1: the full article in its corrected version, not an erratum. No `garbled_text_layer` flags; no supplements are cached. Figure values were read from the cached page renders. Dry-run: +29 components, +239 metrics, 0 errors (the one warning, ni2025b m18 / m4, is on an existing merged row).

| paper | components | metrics |
|---|---|---|
| li2024 | 9 (waveguide_platform.straight 1; reflector.bragg 3; resonator.bragg 5) | 54 |
| li2023a | 3 (reflector.bragg 1; mode_converter.converter 1; fiber_chip_coupler.edge 1) | 22 |
| jiang2016 | 3 (wdm.other 1; waveguide_platform.straight 1; splitter.directional_coupler 1) | 26 |
| sun2013a | 2 (wdm.other 1; waveguide_platform.straight 1) | 19 |
| kervazo2025 | 5 (waveguide_platform.straight 1; resonator.ring 4) | 32 |
| qubaisi2020 | 2 (resonator.photonic_crystal 2, of which 1 design) | 23 |
| han2024 | 1 (resonator.ring) | 13 |
| spencer2014 | 4 (resonator.ring 3; waveguide_platform.straight 1) | 50 |

Fab orgs used (all in the registry): org_ligentec (li2023a), org_astar_ime (jiang2016), org_aluvia_photonics (kervazo2025, MPW service), org_globalfoundries (qubaisi2020, process 45SPCLO), org_chongqing_united_microelectronics_center (han2024, 180 nm platform MPW), org_lionix_international (spencer2014). Fab is empty for li2024 (passive process text; NanoLN supplied the Si-LNOI wafer, which goes in a note) and sun2013a (an unnamed 300-mm CMOS foundry). No facility orgs.

## Not entered, and why

li2024
- Seven of the ten uniform-grating spectra (N = 500: dW 40-70 nm; N = 1000: dW 50-70 nm, Fig. 6) have no printed value; only noisy curves are given. Not read.
- The Fig. 6(b) "11.9 nm" arrow: its long-wavelength end lies beyond the dW = 80 nm band edge, so it is not tied to one trace (D156). The Fig. 6(a) "12.3 nm" arrow is entered as `stopband_width_nm` (it is tied to dW = 80 nm by its left end). The level it is drawn at is not stated.
- The p.7 sentence "insertion losses of the devices ... less than 0.2 dB" gives no reference and no scope (spectra are normalized to their maximum), and it is said once for all devices. Kept in notes (D254 analogue).
- Simulated design-space values: Fig. 2 (dW 70 nm: 13.7 nm and 61.6 dB; N 900: 7.5 nm and 61.2 dB) and Fig. 3(c), (d) sweeps. They are not tied to a fabricated design and so are not entered. The design point of the fabricated PS grating (Q 2.3e4, 27.0 dB) is entered as `simulated`.
- Calculated Au-electrode absorption of about 0.5 dB/cm (p.5): a design value, in notes. There is no parameter for the electrode gap (3.4 um design, 3.2 um by SEM) or the phase-shift length dL (367 nm). Both are in notes.
- Table 1 rows for refs. [35] and [43]: cited (rule 3).

li2023a
- Group delay 2864 ps, delay-bandwidth product 65.87 ns nm, loss per delay 1.57 dB/ns, GD slope 84-158 ps/nm, ripple +/-30 ps (p.7), and the simulated GD 2920 ps, slope 88-161 ps/nm and ripple +/-25 ps: no parameters (registry gap). In notes.
- The drop-DC gap of 300 nm has no `gap_nm` on mode_converter (registry gap). In notes.
- The 1 um reference waveguide has no value. Table 1 rows of other works are cited.

jiang2016
- The two TE grating couplers have no row. The "~19-dB coupling loss introduced by a fiber coupling system" is a total for two couplers plus the setup, and its origin is not stated. It is used only in the de-embedded 6 dB row (`author_estimate`).
- Waveguide lengths l1-l4 and the MZI arm difference have no parameter: notes.
- The simulated common-mode tuning (1548.713 to 1548.871 nm for dn 3.6e-3 to 4.4e-3) and the Fig. 3 ER sweep ends: only the design-point ER of 18.43 dB and the bandwidth range are entered.
- The Group IV Photonics 2014 conference paper by the same authors (ref. [9]) is cited for the older bandwidth-only device. No value is taken from it.

sun2013a
- Channel-spacing variation below 10 pm (1.25 GHz): no parameter (registry gap). In notes.
- Grating duty cycle 0.5: `fill_factor` is not allowed on wdm (registry gap). In notes.
- The calculated design Bragg wavelength 1542.4 nm and neff 1.60: in notes. The sampling periods (142.8 / 72.94 / 49.0 / 36.9 um) have no parameter (`period_nm` is the grating period): notes. Channel-to-sampling-period mapping is not printed, so channel conditions only give the order of the resonances.

kervazo2025
- Per-gap Fig. 5 points (Q_L and contrast) for the 14 gaps other than 375 nm and 400 nm, and the Fig. 7 Qc / kappa^2 per gap (derived from Q_L and Q_int): not entered as rows. The population row holds the printed range and mean (D165).
- Add-drop ring geometry and other values are in Supplement 1, which is not cached. Only the main-text Q_L of 1.4e5 is entered.
- Heater layer dimensions are not printed.
- The Fig. 6 literature comparison and the p.1-2 Q / loss values of other platforms are cited.

qubaisi2020
- Reflection levels (detuned -1.63 dB; reduced by about 10 dB and by 7.2 dB when synchronized; Fig. 6(d), (f) labels 11.6 / 8.1 dB) and the transmission increases (12.4 / 24.4 dB): there is no reflection parameter on resonator (registry gap). In notes.
- FWHM mode length 4.28 um: no parameter (a mode-volume candidate is already listed in D430). In notes.
- The first-order detuned dip depth (about 26 dB in Fig. 6(e)) is not printed. Not read.
- The Ref. [37] heater efficiency of 0.63 nm/mW and the microring 0.29 nm/mW are cited.

han2024
- Mode splitting (Fig. 5(c)) has no printed value. A reading of about 3 pm would be a scale estimate, so it is not entered.
- The CUMEC library grating coupler has no value.
- The simulated higher-order-mode excitation (below or near -40 dB) has no parameter.
- Table 1 rows of other works are cited.

spencer2014
- RTL (round-trip loss) per ring and mode (Table 1): no parameter (`roundtrip_loss_db` is already a candidate from D420). In notes.
- Beat wavelength 73 +/- 2 nm and the measured TE0 / TE1 group-index ratio 1.00039 +/- 0.00002: no parameter. In notes.
- The FSR of 3.3 GHz near 1580 nm (p.2) is stated as "consistent with" the radius. Whether it is measured or computed is not stated, so it goes in notes and is not entered.
- Cited from the authors' earlier work (refs. 15, 22; rule 3): 0.045 dB/m, 55 million Q_int, and the 0.05 dB/m record.
- The Fig. 1 state of the art is cited.

## Missing fab / facility orgs (aliases)

- "LioniX BV" (spencer2014 p.4 acknowledgments: devices partially fabricated at LioniX BV). Fab, mapped to `org_lionix_international` (former company name). The alias is missing in `org_aliases.csv`.
- "IME Singapore" (jiang2016 p.6 acknowledgments: IME Singapore acknowledged for device fabrication). Fab, mapped to `org_astar_ime`. The alias is missing; the registry has "IME", "Institute of Microelectronics" and "Institute of Microelectronics, A*STAR".
- No new org ids are needed.

## Judgment calls

1. li2024 PS-grating siblings (dW 34 / 37 / 43 / 46 nm): treated as measured fabricated designs. The text does not say measured or simulated, but the dW = 40 nm point in Fig. 7(b), (c) equals the measured device (0.50, 20 dB, 3.4e4) and not the simulated design (2.3e4, 27 dB). Their transmittances become `insertion_loss_db` = -10 log10 T (`derived`), and their 3-dB widths are read off Fig. 7(c) (consistent with the printed Q at about 1510 nm). The fifth point is printed as both 44 and 46 nm; the figure axes print 46, so the row uses 46 with a conflict note (D417).
2. li2024 PS-grating `insertion_loss_db` 3 dB = the printed peak power penalty dP, scope `per_component` with the normalization in `excludes`. The class is `resonator.bragg` (phase-shifted Bragg resonance used as a bandpass filter). Uniform gratings are `reflector.bragg`.
3. li2023a delay line as `reflector.bragg` (stopband width, SLSR, peak reflectivity, de-embedded IL). The drop DC is `mode_converter.converter`: its reported metric is the TE1-to-TE0 conversion efficiency. D165 (splitter for coupling-ratio use) is read as not applying. The per-DC -1.5 dB comes from the paper's 20-DC cascade, so it is `measured` + `cutback`. The 0.6 peak reflectivity is `author_estimate`, because the evaluation is not shown.
4. jiang2016 comb filter as `wdm.other` (a comb filter for WDM channel blocking). The 0.019 nm/mW is `derived` (printed in nm/mW); it matches the summed power of the four heaters, and the note gives the per-heater value. The fit outputs (alpha 10.16 dB/cm, ng 4.31) are `measured` (standard fit of own data, D80a) on a waveguide row. The DC split ratio 77.4 % is `derived` from the fitted t = 0.88.
5. sun2013a: one `wdm.other` array row (D165 array-level row), with the channel-3 extinction and width as conditions. The width is stored from the printed 32.5 GHz (32500 MHz, `derived`); the printed "0.26 pm" conflicts with it and is noted (D417). The kappa of 5.6 /cm comes from a model fit and is `derived` (itoh2024 / D468 precedent). The 2.4 dB/cm is `author_estimate` (origin not stated).
6. kervazo2025 D403: the gap-series mean Q_int (3.6e5, gaps 425-575 nm) is `derived`, because the under-coupled branch is identified from the data (maximum contrast at 400 nm; lee2012 / D425). The 400 nm ring's Q_int of 3.4e5 = 2 Q_L is `author_estimate`: its resonance transmission is 11 %, not zero (D463). The 2.8 dB/cm from Eq. (7) is `derived`. The heated ring is gap 375 nm per the Fig. 8(b) legend. 1.64 pm/mW (p.9, Fig. 8(b)) is entered; 1.63 (abstract, conclusion) is in a note. For the 400 nm ring, the Fig. 4(b) linewidth (Q_L about 2.1e5) conflicts with its Fig. 5 point (about 1.7e5); the Fig. 5 read is entered and the conflict is noted.
7. qubaisi2020: Q_int "around 200,000" is `author_estimate` (extraction method not stated, D403). The notional 2D-FDTD unit is a `design` row with platform empty (Si n = 3.5 in vacuum is not a physical stack). Tuning powers go in `tuning_power_mw` with the voltage in `bias_v`.
8. han2024: `bus_width_nm` 450 is entered from the p.4 statement that w2 = 0.45 um equals the single-mode bus width (noted). `radius_um` 20 is the paper's effective radius (condition says so). Platform `soi_strip` (full 220 nm etch).
9. spencer2014: Table 1 Q_int, alpha and kappa are `author_estimate`. They rest on gamma = 0 (assumed), and the under-coupled regime follows from the identical-coupler layout rather than from the data (D403 strict reading). Q_load and ER are `measured`. Radii, gaps and widths are printed in mm / um, so they are `derived` (D157). Fab is LioniX only ("partially fabricated"). No org is named for the rest, so UCSB is not added (no fab from affiliation).

## Registry gaps (skipped value + locator + proposed definition)

- `group_delay_ps` (reflector / waveguide_platform): li2023a 2864 ps, p.7 Fig. 6(b). "Total group delay across the operating band of a delay line or chirped grating."
- `loss_per_delay_db_per_ns` (reflector / waveguide_platform): li2023a 1.57 dB/ns, p.7. "Insertion-loss increase per ns of delay increment." This is already a candidate in D434.
- `gap_nm` on mode_converter: li2023a 300 nm, p.6. Already a candidate in D418 / D428.
- `channel_spacing_variation_nm` (wdm, laser): sun2013a < 0.010 nm (1.25 GHz), p.3. "Max minus min (or stated bound) of adjacent-channel spacing across an array."
- `fill_factor` on wdm: sun2013a 0.5, p.2. Same definition as for reflector.
- `reflection_db` / `back_reflection_db` on resonator: qubaisi2020 -1.63 dB detuned, reduced by about 10 dB synchronized, p.7, Fig. 6(d). "Peak reflection of a side-coupled resonator at resonance, positive dB below the input."
- `roundtrip_loss_db` (resonator): spencer2014 Table 1, e.g. 0.019 dB (3.8 um tapered gap, TE0). Already a candidate in D420.
- `group_index_ratio` (waveguide_platform): spencer2014 1.00039 +/- 0.00002, p.3. Low priority, a single value.
