# Batch lit_16 report (distill subagent, 2026-10-29)

Dry-run `batch lit_16: +33 components, +173 metrics; errors 0`. ASCII only, no e-mail, no quotes (he2026 is
open_license_ok, none used). Not audited or merged.

## Per paper (components / metrics)

- yoshida2023 (2 / 8): 3-mm GaAs double-lattice PCSELs (laser.pcsel). CW device with lattice-constant distribution:
  > 50 W (output_power_mw, W -> mW derived), Ith 25 A (derived), slope 0.72 W/A, 1/e2 divergence 0.05 deg, lasing peak
  943.4 nm read off Fig. 4(e) inset. Pulsed uniform device: Ith ~20 A, divergence 0.046 / 0.045 deg (x / y). Fab
  org_kyoto_university (author contributions p.8: M.Y., S.K. fabricated; Kyoto only). Not entered: R / I / mu coupling
  coefficients (see coordinator Q1), M2 2.36, brightness 1 GW cm-2 sr-1, 3 pm resolution-limited FWHM (D250), Fig. 3
  simulations. p.7 (garbled): Methods equations only, no value taken; no page_07 render exists.
- bernabe2012 (2 / 18): SOI 1D GC (period 632 nm, 70 nm etch, 14 deg): ~6 dB per coupler near 1560 nm, 1-dB / 3-dB
  widths read off Fig. 5 (27 / 52 nm), simulated 3 dB, 30 / 60 nm, geometry, fill factor 0.5 (316 / 632, tooth vs groove
  not stated). Grating-to-grating flip-chip interconnection (chip_chip_coupler.other): 6-8 dB per interface over
  1500-1580 nm (reference-path subtraction, derived; printed "dBm" typo noted), 1-dB lateral tolerance 3 um, GC MFD
  10 um, gap 30-35 um (author_estimate). Fab org_cea_leti ("we designed and processed", all authors CEA-LETI). Not
  entered: sub-2 dB GC [12], mode-mismatch 2-3 dB [13], +/-5 um at 3 dB, optimal offset 13-15 um, bump misalignment
  < 0.1 um (no parameters).
- mu2016 (7 / 48): flip-chip Si3N4-to-SU-8 adiabatic vertical couplers (chip_chip_coupler.evanescent), four fabricated
  taper angles 1.8 / 1.5 / 1.2 / 0.9 deg (sibling rows): average per-coupler loss bounds < 1 / < 1 / < 0.8 / < 0.8 dB
  (1480-1560 nm, cascade minus reference over N, derived), Fig. 4(b) ranges for 1.2 and 0.9 deg, full bilayer geometry
  (Si3N4 92.1 nm ellipsometry, SU-8 0.52 um, tips, widths, tapers, 15 um oxide). EME design row 0.1 deg (0.57 dB, < 0.9 dB
  within +/-1.4 um). Si3N4 (< 0.1 dB/cm) and SU-8 (3.5-5.5 dB/cm) waveguide rows (author_estimate, method not stated).
  Fab empty: LioniX B.V. fabricated the Si3N4 chip (missing org). Not entered: best ~0.5 dB (design not identified,
  D159), 2D FMM 0.40 dB multimode point, < 1 dB/m cited [2], thermal-shock change < 0.1 dB.
- dietrich2018 (7 / 30): 3D-printed facet optics (IP-Dip): lens on InP DFB facet 1.0 dB / 80 %, +/-1.9 um, +/-25 um
  (sim +/-2.4 um, best-achievable 0.6 dB author_estimate); lens on SMF 0.6 dB / 88 %, +/-0.7 um, 5.8 um (one-sided),
  0.2 dB theory; TIR mirrors SMF-SMF 0.6 dB / 87 %, on laser 2.9 dB / 51 %, SMF for VCSEL 1.1 dB / 78 %; two-lens
  expander pair 1.9 dB, +/-5.5 / +/-220 um, design MFD 23 um; LIMOS pair 1.0 dB / 80 % (sim 0.1 dB / 98 %, MFD 22 um).
  Laser / VCSEL MFDs as author_estimate, SMF 10 um specification. SMF-SMF and expander wavelengths inferred 1550 nm.
  Fab empty (fabricator P.-I. D. at KIT and Vanguard Photonics, place not stated, D83c); KNMF funding-only (D83e).
  Not entered: test lasers (setup sources), 35.6 dBm damage level (lens identity unclear, parameter not allowed), angular
  tolerance 1.5 deg, roughness 37 nm, > 100 nm bandwidth statement (no level).
- ishii2003 (5 / 13): OptoBump design row (82 % VCSEL-to-PD ray trace, 1-dB tolerance 50 um = half of the printed
  ~100 um range, beam 208 um from the 104 um radius); 469 um dispensed microlens test (+/-50 um, VCSEL and fiber sides);
  352 um microlens (collimated beam 180 x 167 um); 45 deg TIR-mirror waveguide (1.31 dB mean of 8, device_total incl.
  fiber input); epoxy 50 um MM waveguide (~0.1 dB/cm author_estimate). Many +/- values were lost in text extraction and
  were read from the page renders. Fab empty (NTT authors only "developed" the techniques, D80b). Not entered: Microlens
  2 placement tolerance +16/-21 / +/-19 um, NA 0.25, solder-bump misalignment +/-20 um, 365 um VCSEL lens (geometry only).
- wang2023c (3 / 16): double-sided GaN metasurface on a GaN green LD (micro_optics.metalens): focusing efficiency
  72.8 % (coupling_efficiency_pct, device_total), focal-spot FWHM 0.738 um (beam_diameter_um, see Q3), SEM geometry;
  50 um FDTD design row (90.5 %, 0.495 um); GaN green LD (laser.other): Ith 30 mA, 10 mW and 5.18 V at 55 mA, 520 nm
  (author_estimate). Fab empty ("we fabricated", authors at four orgs). Not entered: nanograting transmittance ~80 %
  (tied to own earlier work [39], D259), DOP > 0.99, focal distance 149.7 um, NA 0.55, imaging line width.
- he2026 (3 / 14): freeform TIR reflector on an AIM Si taper (free_space_emitter.other; FDTD 83 % / 0.8 dB, Si / taper
  widths, BOX 2 and upper oxide 5.26 um from Fig. 2(a) labels), fab org_mit (L.R., MIT only, fabricated, p.17);
  ultrawide-FOV a-Si metasurface (free_space_emitter.metasurface): FOV 161 deg at 1550 nm, angular FWHM 0.27 deg at
  0 deg and 0.74 deg at 69 deg, effective aperture 214 um (author_estimate, definition ambiguous), a-Si 997 nm, SU-8
  2 um, fab empty (H.L. at MIT and 2Pi Inc.); AIM switch tree path loss 22.8 dB excluding the metasurface
  (switch_fabric.other, device_total, fab org_aim_photonics). Facility org_center_for_nanoscale_systems on the reflector
  and metasurface; MIT.nano missing. Not entered: 0.31 deg diffraction limit, 1575 nm curves (no printed values), Fig. 6
  relative power.
- tyler2019 (4 / 26): LETI SiN 2D OPA circuit at 905 nm (free_space_emitter.other): steering 17.6 deg (phi, phase) and
  3 deg (theta, switching 7-9 deg), FWHM 4.3 / 0.7 deg (sim 0.6 deg), design emission 7-10 deg, 4 channels at 3 um, period
  670-700 nm, 750 periods, FF 0.5; SiN waveguide 1.0 dB/cm median cutback; input GC 4.9 dB; Ti/TiN heater P_pi 87.6 mW
  median (MZI), heater geometry (gap 0.8 um, 10/100 nm derived). Fab org_cea_leti ("fabricated using LETI's 200 mm
  platform"). Text layer of pp.2-4 is column-scrambled: values read from the page renders. Not entered: simulated 90 um
  effective aperture, Discussion projections (256-channel OPA 0.12 deg, 10x heater efficiency).

## Orgs missing from the registry (needed)

- "LioniX B.V." - mu2016 p.1 affiliation, p.3 Sec. III (fabricated the Si3N4 chip); D278 kept it out as affiliation-only,
  here it has a fab role (time-aware vs org_lionix_international).
- "MIT.nano" - he2026 p.17 acknowledgements (facility used).
- Not needed (no fab / facility role): Vanguard Photonics GmbH (dietrich2018 p.1), 2Pi Inc. (he2026 p.1), Jiangsu
  Institute of Advanced Semiconductors Ltd. and Suzhou Laboratory (wang2023c p.1).

## Judgment calls / questions for the coordinator

1. yoshida2023 PCSEL coupling coefficients R, I, mu (cm-1, fitted; p.4 and p.5) not entered: kappa_per_cm is allowed for
   laser but R = Re[(kappa_1D + kappa_2D-) e^-i theta] and mu (non-Hermitian) are not a single grating kappa. Enter as
   kappa_per_cm with the coefficient in condition, or add a parameter?
2. ishii2003 tolerances entered as tol_1db_lateral_um although the experimental text gives "about +/-50 um" without the
   level; the 1-dB criterion comes from the paper's own tolerance definition (p.3) and the Fig. 14 / 15 -1 level.
3. wang2023c focal-spot FWHM (0.738 um measured, 0.495 um simulated) stored as beam_diameter_um with the definition in
   condition; no focal-spot parameter exists.
4. bernabe2012 GC loss: wavelength 1560 nm read off Fig. 5 on a measured row (text gives no wavelength).
5. dietrich2018 SMF-SMF mirror and expander losses use wavelength 1550 nm inferred from the design wavelength (Methods).
6. he2026 and dietrich2018 platform `polymer` for printed reflectors / lenses (precedent ofc2026 W4B.1, Th3C.3); metasurface
   rows (a-Si, GaN) and mu2016 SiN-polymer couplers use `other`.

## Registry gaps (value actually skipped, locator, proposed definition)

- beam_quality_m2 (laser): yoshida2023 M2 ~2.36 at 110 A CW, p.6. "Beam quality factor M2 (axis and method in condition)."
- brightness_w_per_cm2_sr (laser): yoshida2023 1 GW cm-2 sr-1 at 110 A CW, p.6. "Radiance from output power and
  emission area / divergence as reported."
- aperture_diameter_um (laser, free_space_emitter): yoshida2023 3 mm resonant diameter, p.1-2; tyler2019 simulated 90 um
  effective aperture, p.4. "Emitting / resonant aperture diameter or length as stated."
- focal_length_um (micro_optics, free_space_emitter): wang2023c 149.7 um measured, p.7; ishii2003 Microlens 2 780 um design,
  p.3; he2026 effective 1.63 mm design, p.8. "Focal length / working distance of a lens or metasurface."
- numerical_aperture (micro_optics, waveguide_platform): wang2023c NA ~0.55 (calculated), p.7; ishii2003 waveguide NA 0.25
  (estimated), p.3. "Numerical aperture as stated (calculated / measured in notes)."
- power_handling_dbm for micro_optics: dietrich2018 printed lens destroyed at 35.6 dBm (1550 nm), p.12 (lens design
  ambiguous; would still need a row decision).
- tol_1db_angular_deg (micro_optics, fiber_interface, chip_chip_coupler): dietrich2018 1.5 deg estimated for the expander
  pair, p.7. "Angular misalignment for 1 dB excess loss (+/-)."
- subwavelength_period_nm for micro_optics (metasurface lattice): wang2023c nanobrick period 250 nm and nanograting period
  220 nm (SEM), p.5.
- steering_efficiency_deg_per_nm for fiber_chip_coupler: bernabe2012 optimum-angle shift about 6 deg per 50 nm, p.6.
- surface_roughness_nm (micro_optics): dietrich2018 37 nm rms (AFM, 25 x 25 um), p.11.
