# lit_230 batch report

Papers: lit:dong2017, lit:geng2014, lit:gao2025b, lit:bernard2021, lit:ozdemir2020. Page-1 titles match the source
rows; none is a correction or another paper. No existing component rows for these sources. verified_on 2026-11-20.
Dry run of `merge_component_staging.py`: +11 components, +66 metrics, 0 errors (the one warning names the merged row
cmp_lit_ni2025b_pimmwc, not in this batch).

| paper | components | metric rows |
|---|---|---|
| dong2017 | 1 | 14 |
| geng2014 | 2 | 12 |
| gao2025b | 4 | 14 |
| bernard2021 | 2 | 8 |
| ozdemir2020 | 2 | 18 |

## dong2017 (Ge0.9Sn0.1 MQW p-i-n photodiode for 2 um, Optics Express 2017)

The text layer of p.4-p.9 is column-scrambled (figure text interleaved); every value was read from the page renders
(page numbers align with the text markers).

Rows: `photodetector.vertical` 20 um diameter mesa, platform `other` (Ge-on-Si vertical PD precedent: kang2008,
duan2012).
- Dark current density 31 mA/cm2 at -1 V, room temperature (printed 0.031 A/cm2, derived); dark current < 1000 nA for
  -2 to 0 V (printed "sub-1 uA", derived; temperature not stated with the bound).
- Responsivity at -1 V, Pin 0.24 mW, ref_plane fiber: 0.216 A/W at 1530 nm and 0.023 A/W at 2003 nm (measured); 1570 /
  1630 / 1742 / 1877 nm read off log-scale Fig. 5(b) (0.14 / 0.09 / 0.053 / 0.032, +/- 10 %, extracted_from_figure;
  the read-out reproduces the two printed end points).
- 3-dB bandwidth about 1.2 GHz at 2 um (measured, -1 to -4 V); theoretical about 1.5 GHz (simulated, Eq. (2) + SPICE).
- Rs 34 ohm (forward-bias I-V fit, measured); Cj about 66.1 fF and Cpar about 2070 fF (calculated, simulated; printed in
  F); mesa diameter 20 um.

Not entered: activation energies 0.206-0.333 eV (no parameter); forward / reverse ratio about 5 orders; calculated
cutoff about 2.2 um and gap 0.56 eV; fT 39.7 GHz and fRC 1.5 GHz (model terms, chen2019 precedent for limits); > 10 GHz
projection for a double-mesa design (not fabricated); Fig. 4 literature points (rule 3); layer thicknesses (in
core_material: absorber is 10 x 15 nm wells, no single absorber thickness printed).

Fab / facility: none. Passive growth / processing; authors at NUS and NTU (both in the registry). Ge-on-Si virtual
substrate "commercially available", supplier not named. Acknowledgment is discussion thanks only.

## geng2014 (selective-area MOCVD InGaAs PDs on SOI, JSTQE 2014)

Rows: `photodetector.vertical` NIPD (growth-well center, 314 um2) and `photodetector.iii_v_on_platform` WGPD (edge,
64 um2, butt-coupled from a Si waveguide), both `iii_v_on_si_epi` (song2021 precedent).
- Dark current 130 / 8 nA and density 40 / 12 mA/cm2 at -1 V; responsivity 0.6 / 0.02 A/W at -1 V, 1550 nm
  (ref_plane unspecified); 3-dB bandwidth 2.5 / 15 GHz (NIPD) and 4 / 14 GHz (WGPD) at -1 / -5 V; absorber 650 / 850 nm.

Not entered: transit-time-limited 36 / 28 GHz (calculated); capacitances 12 / 20 / 14 / 22 fF ("estimated ... [13]",
authors' earlier paper, rule 3 / D259); 20 Gb/s open eyes; buffer AFM RMS, XRD FWHM and dislocation densities
(material, not component); Table II rows of other works.

Fab: `org_the_hong_kong_university_of_science_and_technology` on both rows (borderline, see judgment call 2).
Facility: none entered. Missing orgs (facility role), p.6 Acknowledgment: "Nanoelectronics Fabrication Facility" of
HKUST, and "materials characterization and preparation facility of HKUST" (technical support). The registry's
`org_nanosystem_fabrication_facility` (HKUST) has no alias for the printed name (yang2014 precedent left it empty);
proposed: alias "Nanoelectronics Fabrication Facility (HKUST)" -> org_nanosystem_fabrication_facility if the org round
confirms the rename, and a new facility org for the materials characterization and preparation facility.

## gao2025b (heterogeneous MUTC PD with Si3N4 microcavity solitons, Optica 2025)

Rows (all `sin`):
- `resonator.ring` Si3N4 ring 1.55 x 0.8 um, R 228 um: Q_L 1.5e6 and through-port coupling Q 4.2e6 (`q_external`;
  wavelength inferred 1550 nm from the pump), FSR about 100 GHz (author_estimate, origin not stated), geometry, nominal
  6.3 um cladding.
- `fiber_chip_coupler.edge` SSC: 3.85 dB per facet from a lensed fiber (D167 measured).
- `waveguide_platform.transition` cladding step into the thinned bonding window: 0.4 dB (author_estimate, origin not
  stated); thinned cladding about 0.1 um.
- `photodetector.iii_v_on_platform` MUTC PD population row: typical dark current 170 nA and capacitance 42 fF at -2 V,
  responsivity 0.76 A/W at 1550 nm (bias and ref_plane not stated), 250 nm absorber.

Not entered: Fig. 4(c) 3-dB point (noisy trace, D156); RC-limited 69 GHz estimate; -7 dB at 100 GHz estimate for the
8 x 15 um2 device; mmWave -18 dBm, 0.19 / 2.28 kHz linewidths, phase noise (system level, no parameter);
transit-limited 167 GHz, 81 GHz bandwidth, 3.8 mA compression (cited refs. [25] / [14], rule 3); SOA numbers of ref.
[28]; intrinsic Q (not stated).

Fab: `org_ligentec` on ring, SSC and transition ("fabricated by a foundry (LIGENTEC)", p.2);
`org_university_of_virginia` + `org_ligentec` on the PD ("J.G. performed the PD fabrication", p.4, on the foundry chip;
D440). No facility named. No missing orgs.

## bernard2021 (SiON PIC coupled to Si substrate-integrated detectors, Optica 2021)

Rows (`sion`):
- `waveguide_platform.straight` SiON 700 x 500 nm: 1.72 dB/cm at 850 nm (cutback, 5 spiral lengths); insertion loss
  8.5 dB (scope unspecified); width, thickness, 1.5 um bottom SiO2.
- `photodetector.other` substrate p-n PD fed by the wedge-descending waveguide: responsivity about 0.3 A/W and external
  QE 44.3 % at 850 nm, -3 V, ref_plane on_chip (derived, see judgment call 4); simulated 46 % absorbed fraction.

Not entered: 9.15 dB fiber-to-detector loss (an arithmetic intermediate, in notes); 26 deg refraction angle and n_eff
1.594 (model); 8 deg wedge slope measured by SEM (no fitting parameter: `sidewall_angle_deg` is a waveguide sidewall);
90 % predicted coupling for a 20 um epi / back-etched design (not fabricated); 10 um epi thickness and 25 um coupling
length (in core_material; the 25 um is stated as a simulation input).

Fab / facility: none. Passive fabrication; authors at Fondazione Bruno Kessler and University of Trento. The
acknowledgment is a scholarship / program line (not a facility).

## ozdemir2020 (InGaAs/GaAs MQW nano-ridge waveguide PD on 300 mm Si, IPC 2020)

Rows (`iii_v_on_si_epi`, fab `org_imec`: "grown ... in imec's 300-mm CMOS line", "fully processed on a 300mm Si
wafer", p.1):
- `photodetector.iii_v_on_platform` population row (21 devices, 7 dies): median dark current 10 pA at -1 V (derived)
  and 1.7 nA at -5 V; Fig. 3(a) medians at -2 / -3 / -4 V (about 0.04 / 0.18 / 0.6 nA, extracted); density
  0.0143 mA/cm2 (derived from 1.43e-5 A/cm2); median internal responsivity 0.25 / 0.48 A/W and internal QE 30 / 58 %
  at -1 / -5 V (author_estimate: simulated 0.175 coupling); Fig. 3(b) medians 0.28 / 0.34 / 0.40 A/W at -2 / -3 / -4 V;
  0.2585 A/W fit (Fig. 3(c) inset); 100 um length, 0.7 um width.
- `fiber_chip_coupler.edge` cleaved nano-ridge facet: simulated 17.5 % coupling of a 2.0 um MFD beam (TE) and simulated
  NR mode MFD 0.37 um (row_kind fabricated, D80e).

Not entered: > 7 orders rectification; QW bandgap 1.12 eV; 2.0 um lensed-fiber MFD (test fiber, condition only).
No process name printed. The acknowledgment names an imec R&D program (not a facility). lit:ozdemir2021 (merged) is the
later journal paper on other device sets (this conference paper is the earlier work, so D259 does not remove its
values).

## Judgment calls for the auditor

1. geng2014 Fig. 9: caption (a) NIPD / (b) WGPD, but the -3 dB crossings (a: about 5 / 14 GHz, b: about 3.3 / 16 GHz at
   -1 / -5 V) match the printed values (NIPD 2.5 / 15, WGPD 4 / 14 GHz; text, Table II, conclusion) only with the panels
   exchanged, and even then the -1 V values differ by 1-2 GHz. Printed values entered as measured with the conflict in
   notes (D417 style).
2. geng2014 fab HKUST on both PD rows from "a fabrication issue we encountered when fabricating the Si waveguide" (p.5)
   plus the shared, co-processed substrate and all authors at HKUST. Alternative: WGPD only, or empty (D80b strict).
3. gao2025b PD as one population row (D165): dark current / capacitance / responsivity are given for "the PDs without
   microring resonators" with no size, while the frequency response (8 x 10 um2) and the mmWave device (8 x 15 um2) have
   sizes but no registry-fit value. Per-size rows would be empty (D541 / chen2019 precedent).
4. bernard2021 responsivity / QE `derived`: the 9.15 dB "estimated" input loss equals 8.5 dB + 1.72 dB/cm x 0.38 cm
   from the paper's own cutback (D669 / D394). It may include an output-facet share if 8.5 dB covers two facets (not
   stated), so `author_estimate` is the alternative. Also the 8.5 dB insertion-loss scope is left `unspecified`.
5. gao2025b 0.4 dB cladding-discontinuity loss as `waveguide_platform.transition` (same core, cladding step) with
   author_estimate (method not stated); alternative `waveguide_platform.other`.
6. ozdemir2020 Fig. 3(b) medians entered as `extracted_from_figure` although the quantity is an internal
   (author_estimate) responsivity; the note says so.
7. dong2017 theoretical bandwidth 1.5 GHz and calculated Cj / Cpar entered as `simulated` (Eq. (4) / (5) and SPICE);
   fT / fRC (component-limit terms) left out.

## Registry gaps

- Activation energy of the dark current (dong2017 p.5, Fig. 3(c): 0.206-0.333 eV at -2 to -0.5 V); proposed
  `dark_current_activation_energy_ev` (photodetector, bias required). Single paper; low priority.
- RF output power of a photodiode at a stated frequency and photocurrent (gao2025b -18 dBm at 98 GHz, 2 mA, -2 V;
  chen2019 precedent notes the same gap); proposed `rf_output_power_dbm` (photodetector, frequency and photocurrent in
  condition).
- Roll-off at a stated frequency (gao2025b -6 dB at 100 GHz, 8 x 10 um2, Fig. 4(c)); proposed `rf_rolloff_db`
  (photodetector, frequency in condition). Low priority.
