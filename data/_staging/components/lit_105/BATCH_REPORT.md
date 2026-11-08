# lit_105 distill report (2026-11-08)

Papers: gu2015, yulaev2019, abediasl2015, lai2025. All four cached texts match their source rows (page-1 title);
none is a correction / erratum. Rights: all `restricted_local_only`: facts and locators only.
Totals: 17 components (2 design), 53 metric rows. `merge_component_staging.py --dry-run`: 0 errors (+17 / +53; the
only warning concerns an existing ni2025b row, not this batch).

Note: `data/_staging/components/lit_105_INSTRUCTIONS.md` named in the brief does not exist; the generic
`BATCH_INSTRUCTIONS.md` (incl. the `lit` addendum and D531) was followed. Report file name per the brief
(`lit_105_REPORT.md`, not `BATCH_REPORT.md`).

## gu2015 (PWB between III-V chips on Si; Optics Express 2015)

Components / metrics: 5 / 14.
- `pwb_lci_link` (chip_chip_coupler.photonic_wire_bond, polymer): ~10 dB device_total and ~5 dB per_interface
  (author_estimate), simulated 3.5 dB (no bonding angle) and 4.5 dB (10 deg) per_interface, width 2500 nm (SEM),
  height 8000 nm (author_estimate, twice the 4.0 um pier).
- `pwb_sim_ar1to1_1um`, `pwb_sim_ar1to3_1um` (design): simulated coupling 55 % / 52 % at 1 um width (p.5).
- `lci_fp_laser` (laser.other, inp): threshold ~26 mA and P1 ~0.76 mW at 40 mA, both extracted_from_figure (p.9
  Fig. 8(a)).
- `lci_pd` (photodetector.other, inp): responsivity ~0.09 A/W at -1 V (p.9, Fig. 8(b)), band unspecified.

Not entered: chip gap 140 um and bonding angle 10 deg (no parameter for chip_chip_coupler; notes); facet
reflectivities 0.27 / 0.11 (no parameter for laser); photocurrent at zero laser current (paper does not call it dark
current); dummy-chip PWB widths 1.7-2.5 um vs exposure power (geometry only); Fig. 2 sweep points other than the
1 um values printed in text.

Fab / facility: fab empty (first-person "we fabricated", but authors at Tokyo Institute of Technology, RIKEN,
Okayama University, Hokkaido University: not unambiguous, rule 12). No facility. No missing orgs to request.

## yulaev2019 (metasurface-integrated EMC; ACS Photonics 2019, Just Accepted manuscript)

Components / metrics: 2 / 9.
- `emc_780` (free_space_emitter.grating_emitter, sin): beam FWHM 195 um (mean of 5, +/- 20 um), polar angle
  5.2 deg (+/- 0.1), stack geometry from Methods (Si3N4 ~250 nm, 300 nm waveguide, ~85 nm grooves, BOX ~2.9 um,
  cladding ~2.8 um; design_target).
- `ms_focusing` (micro_optics.metalens, other): additional focusing loss <~1.9 dB (author_estimate, origin not
  stated), poly-Si 660 nm nominal.

Not entered: EMC coupling loss <~4.5 dB (cited from ref. 32, p.12; rule 3) and the <~6.4 dB overall (sum with the
cited value); focal spot FWHM 473 +/- 71 nm / 480 +/- 35 nm, focal distance 75 +/- 2.5 um (sim 72.7 um), NA ~0.8,
aberration-free range ~780 +/- 4 nm (no parameters); polarization-converting metasurface (second device): only
polarization-contrast visibility 0.46 +/- 0.02 (10x) and 0.40 +/- 0.01 (100x) (p.13, p.15): no row (rule 9, no
performance parameter); inverse-taper edge coupler: no performance stated.

Fab / facility: fab empty (passive voice only, p.8 and p.17; D433). Acknowledgement names the UMD-NIST CNST
cooperative research agreement (award): not a facility (D83e). Contrast: ropp2021 (same group) had a first-person
fabrication account and a CNST facility statement; this paper has neither.

## abediasl2015 (monolithic 8x8 OPA transceiver in SOI CMOS; Optics Express 2015)

Components / metrics: 9 / 28. All rows fab `org_ibm`, process_name "IBM 7RF-SOI (180 nm SOI CMOS)" ("fabricated
in the IBM 7RF-SOI commercial CMOS process without any additional post processing", p.3).
- `opa_8x8` (free_space_emitter.other): 64 elements, 33 um pitch, SLSR 12 dB (uniform) / 11 dB (Gaussian), steering
  1.6 deg per axis, receive-mode fiber-to-fiber loss 23.6 dB, ~3 dB passive loss per element (author_estimate).
- `si_wg`: 1.27 dB/mm -> 12.7 dB/cm (derived), Si 145 nm, BOX 1 um.
- `si_bends`: 0.71 / 0.2 dB per U-turn halved to 0.355 / 0.1 dB per 90 deg (derived; chung2017 precedent).
- `io_gc` (fiber_chip_coupler.grating): 30 % per coupler.
- `tr_switch` (switch_fabric.other, D158 / D407): P_pi 14.2 mW, isolation 30 dB as crosstalk_db.
- `voa` (phase_shifter.thermo_optic, D155): 16 dB range at 14.9 mW, 1.18 kOhm, 29 x 7 um.
- `ps_meander` (phase_shifter.thermo_optic): 2 pi at 27.2 mW (P_pi 13.6 mW derived), 1 kOhm (author_estimate,
  not stated as measured), 94.4 um.
- `antenna` (free_space_emitter.grating_emitter): 50 % radiation efficiency (author_estimate: "designed with"),
  3.55 x 1 um.
- `schottky_pd` (photodetector.other): 1 mA/W at -1 V.

Wavelength: 1550 nm is the stated demonstration wavelength (p.3, p.11); OPA-level values and the VOA (Fig. 2(c) at
1550 nm) carry it as stated; component values without a printed wavelength have `wavelength_inferred: true`.

Not entered: T/R switch heater 814 ohm and 0.5 um heater margin (heater params not allowed for switch_fabric);
receive-mode null 14.5 dB below the peak (no parameter for free_space_emitter); PD minimum detectable power 1.5 uW;
sidewall roughness 7.5 nm / 10 nm (estimate); bus / row residues 11 % / 1.2 %; VOA phase response (Fig. 2(c)).

Missing org (fab role): **MOSIS** (printed "MOSIS", thanked for supporting the chip fabrication, p.11
Acknowledgments; MPW access provider, D398 / D470). Same gap already reported for chung2017.

## lai2025 (GaN homogeneous circular-polarizer metasurface; Optics Express 2025)

Components / metrics: 1 / 2.
- `hcp_75deg_g11` (micro_optics.metalens, other): power efficiency 40 % measured (mean over incident LP angle,
  Eq. (11), reference window) and 50 % simulated; fab `org_national_yang_ming_chiao_tung_university` (conclusion
  "we designed and fabricated", all authors NYCU Department of Photonics, D399).

Not entered: degree of circular polarization S3 0.88 measured / 0.95 simulated (no parameter); G10 and G23 75-deg
siblings (fabricated, only normalized far fields in Fig. 5(d): no metric, no row); Table 2 simulated eta_L / eta_R
for six designs (which beam each refers to is not stated unambiguously, D159); wavelength-dependence simulations
(supplement, not cached). ITRI support for GaN epitaxy materials: material supplier, note only (D428).

## Judgment calls

1. gu2015 ~10 dB is `author_estimate` (rests on P2 ~ 2 P1 from Eq. (3) with facet reflectivities of unstated
   origin), scope `device_total`; the per-side 5 dB is `author_estimate` (equal sides assumed, D462 analogue).
2. gu2015 wavelength: lasing wavelength never printed; 1550 nm `wavelength_inferred` on the PWB rows from the SU-8
   index / transparency stated at 1550 nm for this PWB; the PD responsivity stays `band: unspecified`.
3. gu2015 simulated 1 um points as two `design` rows (different width / aspect ratio = sibling design, rule 9).
4. yulaev2019 1.9 dB metasurface loss kept as `author_estimate`: the sentence opens "As previously reported [32]",
   but ref. 32 is the earlier EMC paper and the metasurface is new here; coordinator may prefer to drop it (D259).
5. lai2025 classed `micro_optics.metalens` ("metasurface optic") rather than `polarization.other`, because its only
   measured performance is a linear power efficiency (coupling_efficiency_pct is not allowed for polarization).
6. abediasl2015 antenna 50 % `author_estimate` (caption "designed with"; no simulation of efficiency shown);
   chung2017 recorded the same antenna as `simulated` from its own Fig. 17.
7. abediasl2015 "isolation 30 dB" of the MZI T/R switch entered as `crosstalk_db` (port state not stated).

## Registry gaps (proposed)

- `polarization_contrast_visibility` (unit 1; polarization, micro_optics): (Imax - Imin) / (Imax + Imin) of the
  output vs analyzer angle. Skipped: yulaev2019 0.46 +/- 0.02 / 0.40 +/- 0.01 (p.13, p.15).
- `degree_of_circular_polarization` (unit 1; polarization, micro_optics, laser): Stokes S3 as reported. Skipped:
  lai2025 0.88 measured / 0.95 simulated (p.1, p.7 Fig. 5(e)).
- `focal_spot_fwhm_nm` (nm; micro_optics, free_space_emitter): intensity FWHM of a focused spot. Skipped: yulaev2019
  473 +/- 71 nm (p.12). `focal_length_um` (um; micro_optics): measured working / focal distance. Skipped: yulaev2019
  75 +/- 2.5 um (p.11). Both already raised for wang2023c / lim2026.
- `min_detectable_power_uw` (uW; photodetector): stated minimum detectable optical power. Skipped: abediasl2015
  1.5 uW (p.5).
- `null_depth_db` or allow `extinction_db` for free_space_emitter: receive-pattern null below peak. Skipped:
  abediasl2015 14.5 dB (p.11).
- Allow `heater_resistance_ohm` / `heater_gap_um` for switch_fabric. Skipped: abediasl2015 814 ohm, 0.5 um (p.5).
- Allow `gap_um` / a bond-angle parameter for chip_chip_coupler.photonic_wire_bond (chip gap, bonding angle).
  Skipped: gu2015 140 um, 10 deg (p.9).
