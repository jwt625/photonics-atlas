# lit_260 batch report

Papers: lit:guo2024a, lit:chen2021c, lit:zhang2015a, lit:ma2017. Page-1 titles match the source rows. verified_on 2026-11-23.
Totals: 11 components, 118 metric rows. `merge_component_staging.py --dry-run`: errors 0, 1 warning in this batch
(guo2024a exc02-m11 vs m7: same value 0.69 dB at 1550 nm, but the conversions differ: TM2 -> TM0 vs TM0 -> TM2; both kept).

## lit:guo2024a (2 components / 51 metrics)

- `cmp_lit_guo2024a_exc01` (mode_converter.converter, TE0/TE1 and TM0/TM1 mode exchanger): measured IL / CT per conversion
  at 1550 nm (4 + 4), measured bound IL < 1.6 dB and CT < -15 dB over 1524-1555 nm, simulated IL / CT per conversion at
  1550 nm (8), simulated bounds over 1520-1570 nm and 1500-1590 nm (relaxed), geometry (length, footprint, I/O widths, stack).
- `cmp_lit_guo2024a_exc02` (TE0/TE2 and TM0/TM2): measured 1550 nm IL and CT as ranges, measured bound over 1520-1569 nm,
  simulated per-conversion IL / CT (8), simulated bound over 1520-1580 nm, simulated CT into the first-order mode > 80 dB,
  geometry.
- Not entered: EXC02 measured per-conversion 1550 nm values (five IL (CT) pairs printed for four conversions, p.8:
  mapping ambiguous, D156 / D159; entered as ranges only); SWG period Lambda / duty cycle a, taper lengths LT1-LT4, arm widths
  (Table I; no SWG-period parameter for mode_converter, cabo2024 precedent); dual-period grating couplers (geometry only, no
  performance stated, p.6-7); MUX / DeMUX reference structures (no values stated).
- Fab / facility: passive fabrication sentence, no org (p.6 Sec. IV): fab empty. No acknowledgment section. No missing orgs.
- Judgment calls: (1) EXC02 range rows (statistic range over the five printed values) instead of no entry. (2) Measured
  rows `measured` with method reference_structure (normalized transmittance, majority precedent), although the MUX
  normalization halves the reference-pair transmittance (p.7).

## lit:chen2021c (3 components / 26 metrics)

- `cmp_lit_chen2021c_te10_te00_converter` (fabricated): measured conversion loss < 0.83 dB over 1500-1600 nm and best
  0.095 dB near 1555 nm (`derived`: L_conv = L3 - L1 - Lmux, Eq. 1), simulated transmission and conversion efficiency
  (dB as insertion_loss_db, % as coupling_efficiency_pct, as printed), geometry (Table 1 widths, P10 length, footprint, stack).
- `cmp_lit_chen2021c_te10_dc_mux` (mode_converter.mdm_mux, test structure): Lmux < 3.69 dB over 1500-1600 nm (`derived`,
  (L2 - L1)/2), Table 2 widths and coupling length.
- `cmp_lit_chen2021c_te20_te00_converter` (row_kind design, simulated only): transmission, conversion efficiency, Table 3 geometry.
- Not entered: simulated TE00 mode purity (99.77 % / 99.84 %) and its degradation (no parameter); spline widths P1-P9;
  measured-vs-simulated 0.4 dB discrepancy; DC gap 100 nm (gap_nm not allowed for mode_converter); values in the
  introduction from refs. [8]-[11] (rule 3).
- Fab / facility: passive sentence, no org, no acknowledgment section: fab empty. No missing orgs.
- Judgment calls: (3) converter / mux measured values `derived` (explicit subtraction / halving formulas printed) rather than
  `measured`. (4) Measured direction recorded as TE00 -> TE10 (the measurement structure is converter then TE10 demux, p.5);
  design optimized for TE10 -> TE00. (5) Mux kept as `mode_converter.mdm_mux` (DC design from refs. [21], [22], measured here).

## lit:zhang2015a (3 components / 14 metrics)

- `cmp_lit_zhang2015a_lcwbg_500_550` (reflector.bragg, soi_rib): measured bandwidth 11 nm (1533-1544 nm), geometry
  (12.54 mm, 300 nm period, 50 % duty cycle, rib width 500-550 nm, 220 / 150 nm rib / slab, 2 um BOX).
- `cmp_lit_zhang2015a_lcwbg_500_600` / `_500_650`: bandwidth 20 nm / 29 nm `derived` from the stated group-delay windows
  (1534-1554 / 1533-1562 nm), rib width range, period.
- Not entered: group delay (228 / 236 / 241 ps), dispersion (20.7 / 11.8 / 8.3 ps/nm), chirp rate (0.88 / 1.59 / 2.31 nm/mm)
  and the simulated 220 ps / 11 ps/nm / 1.59 nm/mm (no registry parameters); spectral shapers (MZI with two opposite-chirp
  LC-WBGs, offset 0 and offset = grating length): the only stated loss, 'around 30 dB' (fiber-to-fiber incl. Y-branch
  splitting, p.4), is stated once for 'the fabricated spectral shaper' while two shapers were fabricated (D159), FSR only
  qualitative, footprint 12.70 x 0.081 mm (1.03 mm2) geometry only, so no shaper rows; microwave waveform results (chirp rate,
  TBWP, compression ratio: system-level); strip-rib tapers 50 um and 12 um bends (geometry only); setup instruments.
- Fab: org_imec ('at IMEC, Belgium, accessed via ePIXfab', p.4 Sec. II) + org_cmc_microsystems (Acknowledgment 'enabling the
  fabrication of the device', p.7; zhang2015 precedent, D398). process_name 'CMOS-compatible 193-nm deep UV lithography at
  IMEC, accessed via ePIXfab'.
- Journal extension of the authors' conference paper (ref. [21], p.2): values kept (skill Contract v6).
- Judgment calls: (6) 500-600 / 500-650 bandwidths entered as `derived` from the delay windows (the paper treats the window as
  the bandwidth for the 500-550 design and computes dispersion = delay / window for all three); otherwise these two rows would
  have no registry metric and drop out. (7) Grating length 12.54 mm entered only on the 500-550 row (stated for the shaper
  grating; not restated for the other two). (8) CMC as fab org for 'enabling the fabrication'.

## lit:ma2017 (3 components / 27 metrics)

- `cmp_lit_ma2017_sbgw_uniform` / `_sbgw_gauss_apod` (reflector.bragg, soi_strip, TM): measured minimum SLSR 0.9 / 13.2 dB,
  simulated SLSR 1.8 / > 62 dB and transmission ER ~60 / ~32 dB, figure-read measured transmission notch depth (>= 49 dB, axis
  clipped / ~24 dB, Fig. 6(b)), simulated peak kappa 46 /cm (printed 4600 m^-1), geometry (3 mm, 440 nm period, corrugation
  45 nm, average width 500 nm, 220 nm Si, 2 um SiO2).
- `cmp_lit_ma2017_csbgw_uniform` (period-chirped, 4 mm, dW 60 nm): measured passband 8.8 nm, geometry.
- Not entered: apodized C-SBGW (only value: measured delay 31.2 ps vs simulated 32 ps; no registry parameter, so no row);
  group-delay slope -11 ps/nm (measured and simulated); spiral R0 15 um, waveguide gap 2 um, max radius 59 um (no
  reflector-class bend / gap parameter); apodization index alpha = 3 (design); Fig. 7(b) 18.1 dB long-side label (text gives
  the minimum); simulated phase-noise sigma 1.3 nm; GCs and Y-junction (cited, no values).
- Fab: org_applied_nanotools ('fabricated by Applied Nanotools Inc.', p.2 Sec. III). CMC Microsystems and Lumerical
  acknowledged for design / simulation software only (p.4): not entered. process_name empty (no PDK named).
- Judgment calls: (9) figure-read transmission notch depths on both 3 mm gratings (uniform as `ge` 49 dB because the curve
  hits the -50 dB axis limit). (10) SLSR rows C band inferred from the 1554 nm design Bragg wavelength (spectra plotted vs
  detuning only). (11) 440 nm starting period on the uniform C-SBGW from the C-SBGW design sentence.

## Missing orgs

- ePIXfab: printed 'accessed via ePIXfab' (lit:zhang2015a p.4 Sec. II), fab role (MPW access broker). Not in
  organizations.csv / org_aliases.csv (only ePIXfab member pages appear as homepages of other orgs).

## Registry gaps (skipped value + locator + proposed definition)

- `group_delay_ps` (reflector, wdm): zhang2015a 228 / 236 / 241 ps (p.4), ma2017 31.2 ps (p.3). Definition: group delay of a
  dispersive grating / filter at the stated wavelength or over the stated window.
- `dispersion_ps_per_nm` (reflector): zhang2015a 20.7 / 11.8 / 8.3 ps/nm (p.4), ma2017 -11 ps/nm (p.3). Definition: group-delay
  slope of a chirped grating over its passband (sign as printed). D81 / D250 rejected waveguide dispersion beta2; this is a
  device-level delay slope.
- `chirp_rate_nm_per_mm` (reflector): zhang2015a 0.88 / 1.59 / 2.31 nm/mm (p.4).
- `mode_purity_pct` (mode_converter): chen2021c 99.77 % at 1553 nm, 99.84 % (p.5, p.7). Definition: fraction of the output
  power in the target mode.
- `gap_nm` for mode_converter: chen2021c DC mux gap 100 nm (p.5 Table 2).
- `subwavelength_period_nm` for mode_converter: guo2024a Lambda 0.24 / 0.2 / 0.25 um (p.5 Table I) (as cabo2024).
- `min_bend_radius_um` / `gap_nm` for reflector: ma2017 spiral R0 15 um, gap 2 um (p.1-2).
