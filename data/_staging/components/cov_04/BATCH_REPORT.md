# cov_04 batch report (2026-11-07)

All five cached texts match their source rows (page-1 title). None is a correction or erratum, and none has a garbled text layer. li2019 and gatkine2022 are arXiv v1 texts: li2019's title wording differs slightly from the journal title (Laser Photonics Rev.), and gatkine2022 is the arXiv version of the SPIE paper. wu2023a is a preprint. None of the five had rows in `data/components/components.csv` before this batch. Dry-run: +18 components, +106 metrics, 0 errors. The one warning (ni2025b m18 / m4) is on an existing merged row, not from this batch.

| paper | components | metrics |
|---|---|---|
| gatkine2022 | 3 (wdm.awg 1; waveguide_platform.straight 1; fiber_chip_coupler.edge 1) | 21 |
| hu2021b | 6 (resonator.coupled_rings 4; phase_shifter.thermo_optic 1; fiber_chip_coupler.edge 1) | 37 |
| li2019 | 3 (resonator.photonic_crystal 2; frequency_converter.shg 1) | 12 |
| shim2026 | 3 (phase_shifter.thermo_optic 1; resonator.ring 1; waveguide_platform.straight 1) | 28 |
| wu2023a | 3 (switch_fabric.mzi_mesh 1; splitter.directional_coupler 1; waveguide_platform.straight 1) | 8 |

## EO values kept out (rule 2), for the EO atlas

hu2021b: two-resonator EO frequency shifters (Ext. Data Table 1, p.23; text p.4, p.11)

| device | eta | CSR | shift ratio | on-chip loss alpha | microwave power (full conversion) |
|---|---|---|---|---|---|
| 12.5 GHz | 80 % (up and down) | 33 dB (up), 27 dB (down, p.4) | 0.993 (table); 0.994 up / 0.993 down (p.4) | 0.92 dB | 102 mW (20.1 dBm, 3.2 V peak) |
| 11.0 GHz | 73 % | 23 dB | 0.977 | 1.25 dB | 288 mW (24.6 dBm, 5.4 V peak) |
| 28.2 GHz | 89 % | 20 dB | 0.987 | 0.45 dB | 316 mW (25 dBm, 5.6 V peak) |

- Microwave bandwidth: shift ratio drops from 0.977 to 0.784 as the drive goes from 11 to 8 GHz at 228 mW. The paper calls this a 3-dB bandwidth > 3 GHz, limited by the amplifier (p.4, Fig. 2(e)).
- Modulation 3-dB bandwidth: 2.2 GHz (4.4 GHz optical) at 126 mW, and 4.1 GHz at 398 mW. Low-frequency S21 loss 1.15 dB; loss from the eye diagrams about 1 dB (p.8, Ext. Data Fig. 3; 12.5 GHz device at 1560 nm).
- Other measured values:
  - d.c. tuning of the 12.5 GHz device to a 16 GHz shift with shift ratio 0.991 (p.4, Ext. Data Fig. 6)
  - 50:50 frequency beam splitter at 10 mW on the 28.2 GHz device
  - swap crosstalk about -35 dB at a few hundred MHz, rising to about -25 dB at 2.8 GHz (p.9, Ext. Data Fig. 5)
  - parasitic sidebands > 25 dB below the shifted line (p.12)
- Simulated electrode: 0.11 pF, 0.12 nH, 1.5 ohm; V_C / V_0 = 1.72 at 28.2 GHz (p.12). The 0.5 GHz/V EO coefficient is cited (ref. 33).
- Three-resonator cascade (p.6, Ext. Data Table 2): 119.22 GHz down-shift with a 29.805 GHz drive; eta 19 %, CSR 10 dB, shift ratio 0.809, alpha 6.17 dB (1.54 dB per mode), 550 mW.

wu2023a: TFLN EO phase shifters / MZI units
- V_pi 4.64 V, measured on the MZI unit (5) internal phase shifter (p.4, Fig. 3(b)). Mean V_pi 5.38 V from Table 1 (p.5).
- Rise time 500 ps and fall time 1.7 ns with a 100 MHz, 4.4 Vpp square wave (p.4, Fig. 3(c)-(e)).
- Calculated values: capacitance 21 fF and 304 fJ per pi shift (p.5).
- Estimated power: 0.6 per shifter and 15 for the mesh at 1 MHz (p.5). The unit symbol is missing in the text layer at p.5. The conclusion (p.8) prints 15 uW, and the figure matches 304 fJ x 24 shifters x 1 MHz with charge and discharge.
- The abstract calls the 0.15 dB per MZI unit "insertion loss for each modulator". It is entered as the per-unit switch-fabric loss (question 3).

## Not entered, and why

gatkine2022
- Resolving power: about 12,000, and > 10,000 over 1400-1570 nm (p.7, Fig. 6). No registry parameter (gap below). A FWHM channel width derived from it would be an inversion of an approximate number, so it is not entered.
- Design values in notes only: channel spacing 0.12 nm and FSR 2.88 nm (p.3).
- Simulated overall throughput -9 dB: the simulation plus the measured 2.5 dB per facet.
- Waveguide mode diameters and neff (simulated, Fig. 1).
- The 1200-1700 nm broadband dispersion (Fig. 7) is qualitative, with no value.
- Cited: < 0.1 dB/cm SiN loss (refs. 14, 15). Future-work numbers (< 0.5 dB/facet, > 50 %) are projections.

hu2021b
- Ext. Data Fig. 1a cross-section (w 1.2 um, slab 250 nm, cladding 0.8 + 0.8 um) belongs to "one of the two-resonator devices", and the device is not named. D159: kept in notes only.
- Loaded Q about 80,000 is stated for the two-resonator devices in general (p.11). Notes only.
- Inter-ring coupling rates mu1 / mu2 (2 pi x 2.49 / 6.86 GHz): no parameter. kappa_aux: notes only.
- Simulation and projection values are not entered: assumed intrinsic Q 1.8e6, the 1.1 dB / 0.15 dB-per-mode cascade simulation, and the Q = 1e7 projections (0.04 dB, 0.1 dB, 0.2 dB).
- Cited: the 50 W ring power handling (ref. 46) and the facet-loss options of 1.7 / 1.1 dB (refs. 34, 35).

li2019
- Hole radius 145 nm and simulated bandgap 28.1 THz: no parameter (core_material / notes).
- Line-defect width w is not tied to the Fig. 3 devices.
- Sidewall angle about 85 deg is in core_material; whether it was SEM-measured is not stated.
- Simulated mode volumes: notes only.
- o-cavity SHG "about 4 times lower" is a ratio only. THG has no efficiency.
- The thermo-optic and thermal-expansion coefficients are cited material constants.
- TE0_10 "about one order lower" is entered from the Fig. 3(b) label (3.54e4).

shim2026
- Supp. Sec. 7 loaded Q values:
  - TE0: 2.29e5 at 1597.02 nm, ER 13.38 dB
  - TM0: 2.17e5 at 1591.92 nm, ER 11.06 dB
  - Intrinsic Q about 4.58e5 / 4.34e5 from Q_i = 2 Q_L (assumed critical coupling)
  - The text says "the fabricated racetrack resonators" and does not name Device A or B. D159: notes only (question 1).
- Device A thermoreflectance (about 160 C at about 619.6 mW): no parameter.
- Simulated heater excess loss: 0.10 / 0.25 dB/m.
- Fitted dn/dP material coefficients, confinement factors, and the bend equivalent-angle model are model outputs.
- FSR is fitted as a linear function of wavelength, so there is no single value.
- Simulated geometry and cladding studies (Supp. Secs. 10, 12, 13).

wu2023a
- Matrix fidelity: max deviation about 8 % (Fig. 4(f)). No parameter.
- Table 3 values for other works are comparison rows (rule 3).
- The 3 dB/m, 27 dB/m and 2.5 dB/m waveguide losses on p.2 are cited.
- Waveguide cross-section not printed: platform left empty (D422 / D423).

## Fab / facility orgs

- Found and used:
  - org_ligentec: gatkine2022, 3 rows (p.3, "fabricated at Ligentec"; AN800).
  - org_harvard_university (fab) and org_center_for_nanoscale_systems (facility): hu2021b, 6 rows. Author contributions name Y.H. as the fabricator; the acknowledgment says fabrication was performed at CNS (p.12-13).
  - org_university_of_rochester (fab) and org_cornell_nanoscale_facility (facility): li2019, 3 rows. Fabrication is described in the first person and all authors are at Rochester; the acknowledgment says the work was performed in part at CNF (p.9).
- Missing from the registry: BRIGHT Photonics (gatkine2022 p.8 acknowledgment). It is thanked with Ligentec for "design and fabrication of one of the chips" as part of their MPW service. Not in organizations.csv / org_aliases.csv (question 4).
- Fab left empty:
  - shim2026: "we fabricated" with authors at Harvard and KAIST, and no site named (D80b / D395).
  - wu2023a: a passive fabrication sentence (PLACE) with no org named (D80b).
- Note only: NANOLN, the wafer supplier for hu2021b, shim2026 and wu2023a.

## Judgment calls

- gatkine2022 on-chip 4 dB is `derived` (de_embedded): 9.6 dB fiber-to-fiber minus the stated 5.5 dB coupling.
- gatkine2022 Ligentec values have basis `specification`: the < 0.2 dB/cm process figure and the 2.5 um taper mode diameter.
- hu2021b q_intrinsic, kappa_int and gamma are `author_estimate` (D403). The loaded linewidth kappa is `measured`.
- hu2021b gamma is entered in `kappa_ext_mhz` as printed. The condition notes that the S / AS external rate is gamma / 2.
- hu2021b 250 GHz ring FSR is `author_estimate` because its origin is not stated.
- hu2021b heater tuning power 350 mW is `derived` from I^2 R with both printed values approximate.
- hu2021b facet loss of 5-10 dB per facet is `author_estimate` (method unspecified, no wavelength).
- li2019 Q0 labels are treated as intrinsic and entered as `author_estimate` (D403).
- li2019 Fig. 3(e) bound "> 1.5e5" is entered as q_loaded (unqualified Q, per the skill pitfall). Its conflict with a few figure points is noted.
- li2019 SHG row follows D396.
- shim2026 p_pi_mw = 4 x printed P_pi/4, `derived`, one row per orientation and polarization (14 rows; question 2). The heater geometry and the rib cross-section are on the heater row.
- wu2023a extinction of the MZI unit (5) routes and the 0.15 dB per-unit loss budget (`derived`, loss_breakdown) are on the switch_fabric row (question 3).

## Registry gaps

- `resolving_power` (wdm): lambda / FWHM of a channel as reported. Skipped value: gatkine2022 about 12,000, and > 10,000 over 1400-1570 nm (p.7 Fig. 6).
- `inter_resonator_coupling_mhz` (resonator): coupling rate mu / 2 pi between resonators of a coupled-resonator device, distinct from mode_splitting_ghz = 2|mu|. Skipped values: hu2021b mu1 2490, mu2 6860 MHz (p.24 Ext. Data Table 2).
- `p_pi_over_4_mw` is not needed if question 2 is accepted.
- `hole_radius_nm` (resonator.photonic_crystal / reflector; the hole_diameter_nm candidate from D431). Skipped value: li2019 145 nm, design (p.2).
- `mode_volume_lambda_n3` (resonator): simulated effective mode volume. Skipped values: li2019 2.43 / 3.06 / 4.63 (lambda/n)^3 (p.2).

## Questions for the coordinator

1. shim2026: should the Supp. Sec. 7 loaded Qs (2.29e5 TE0 / 2.17e5 TM0) go on the octagonal racetrack (Device B) row? The text names neither device. Recommendation: keep them out (D159). Device B is the device the coupler section designs for, but that does not tie the Q section to it.
2. shim2026: is p_pi_mw = 4 x P_pi/4 acceptable as `derived`, or should the printed P_pi/4 wait for a registry parameter? Recommendation: accept. The paper treats Delta n_eff vs P as linear, and the 4x values (183-474 mW) lie inside the measured power range (up to about 620 mW).
3. wu2023a: do the route extinctions (36 / 34 dB) and the 0.15 dB per-MZI-unit loss stay on the switch_fabric row, or do they go to the EO atlas as modulator IL / ER? The abstract calls them modulator figures. Recommendation: keep them on the switch fabric. They describe switch states of the mesh, and V_pi / speed / energy are already in the report.
4. gatkine2022: should BRIGHT Photonics be registered and added as a fab org (D398, MPW provider)? The acknowledgment says "one of the chips tested", and the body names only Ligentec as the fabricator. Recommendation: register it as a design / MPW-service org, as a note only on these rows.
5. hu2021b: should the two-resonator q_intrinsic stay `author_estimate`? A four-parameter fit of a doublet in the strongly over-coupled regime may have fixed the regime, but the paper does not say how. Recommendation: keep `author_estimate` (D403).
6. li2019: the cached text is arXiv v1, and the source row is the Laser Photonics Rev. journal version. Accept as the same work (D433 precedent)? Recommendation: accept, and re-check the values if the journal version is cached.
