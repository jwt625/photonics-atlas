# Batch lit_19 report (distill subagent, 2026-10-29)

Dry-run `batch lit_19: +29 components, +172 metrics; errors 0`. ASCII only, no e-mail, no quotes (lahijani2026 is
open_license_ok, none used). Not audited or merged.

## Per paper (components / metrics)

- abdulla2011 (1 / 15): SOI racetrack add-drop ring tuned by an electrostatic SiNx/Au bimorph MEMS cantilever
  (resonator.ring): geometry (R 10 um, 12 um straight as coupling_length_um, gap 240 nm, 600 nm, 220 nm, BOX 2 um), FSR
  6.6 nm, Q ~8000 (q_loaded), FWHM ~195 pm, 20 dB dip, 122 pm reversible tuning at 9 V (tuning_range_nm 0.122 derived),
  18 dB modulation depth, 5 nm shift and Q 5000 at pull-in. Not entered: pull-in voltages (9.2 V / 4.8-4.9 V, Fig. 8) and
  off-state deflection (no parameter); 70 pm for 8.5 -> 9 V (would need a pm/V ratio over a nonlinear range); 20-25 dB
  system loss (fiber-to-fiber, GC-dominated); "< 3 dB" ring loss (cited [7]). Fab org_university_of_twente for the MEMS
  post-processing ("we could successfully etch", all authors UT); ring wafers by ePIXfab (missing org).
- hu2023a (2 / 21): sidewall-doped Ge-Si waveguide PD (dark current best / wafer range over 26 reticles, external and
  internal responsivity TE / TM, bw3db wafer > 50 / max ~57 / selected ~55 GHz, S11-fit C_j 16.6 fF, C_par 11 fF, R_s
  22 ohm, Ge 1 x 0.4 x 50 um, TEM width ~1.1 um); suspended Si SSC ~3.0 dB/facet (measured, D167). Fab empty (commercial
  90 nm foundry not named; authors at WRI / NOEIC / Peng Cheng). Not entered: eye-diagram data rates, simulated field /
  intrinsic width, TFLN modulator of the setup (equipment).
- lischke2021 (1 / 6): 'Ge-300' lateral in-situ-doped Ge PD, follow-up lot with 1310 nm GCs: dark current 20-100 nA at
  -2 V (text prints "nm", Fig. 3 confirms nA), external 0.39 / internal 0.8 A/W at 1310 nm (the sentence lists them in
  reversed order; Fig. 3 right and the conclusion fix the assignment), C 6.5-7.5 fF read off Fig. 2 right, 20 um length,
  ~300 nm average Ge width. Not entered (D259 / D80i, first lot = authors' IEDM 2020 [2]): >= 110 GHz 3-dB bandwidth at
  1550 nm, > 0.6 A/W at 1550 nm, 1-dB wafer map (Fig. 4 marked [2]); 1310 nm response only to 67 GHz (no 3-dB value).
- santini2017 (6 / 29): InP UTC PD 5 x 25 um2 (0.37 A/W lensed fiber, 0.5 A/W AR-corrected author_estimate, 58 fF, 16
  ohm, bw3db > 40 GHz test diode and in-receiver), coherent receiver without SOA (0.04 / 0.045 A/W), SOA-preamplified
  receiver (4-5 A/W, AR-corrected 5.5-6.8, LO path 0.008-0.01, > 1.25 A/W at 60 mA, 3-dB saturation input > -4 dBm),
  SOA (gain > 20 dB derived by the authors, 240 / 80 mW, 500 x 1.1 um, 120 nm bulk), 2x4 MMI 90-degree hybrid
  (imbalance < 1 dB, ~0.2 dB LO C-band, 4.9 dB MMI + waveguide excess author_estimate), InP SSC ~1.5 dB/facet. Not
  entered: PD PDL < 0.7 dB (pdl_db not allowed for photodetector), RC cut-off 41 GHz, NF 8.2 dB (cited [13,14]), Q
  factors, 8.9 dB total excess (ratio of entered values). Fab empty ("our SOA-PIN platform", passive fab, D84a).
- hung2020 (10 / 52): TSMC 90 nm bulk-CMOS polysilicon: fully etched GC (-8.5 dB peak, 1-dB BW > 80 nm, 920 nm / 0.5 /
  15 deg), strip waveguide (112 dB/cm, 93-142 dB/cm), SWG waveguide (38 dB/cm by cut-back and by ring cut-back, spectra
  22-50 / 29-46 dB/cm), strip-SWG converter (0.8 / 0.718 dB derived, 0.5-1 dB spectrum, 0.3 dB simulated), reference
  ring (Q 3000), five cladding-modulated Bragg reflectors (strip L 760 / 570 um; SWG d 850 nm L 1500, d 200 nm L 300 (set
  A), d 1050 nm L 1500 (set C)): FWHM and ER. Fab org_tsmc. Not entered: temperature sensitivities 76.5 / 27.3 pm/C (and
  17 pm/C simulated), converter reflection -24 dB (OFDR) / -21 dB (sim.), ring round-trip loss 1.56 dB, Wg / d / W2
  reflector geometry (no reflector parameters), set-B ER > 25 dB (figure reading only).
- jean2019 (2 / 16): slow-light SWG waveguide families #1 (W 1000 nm, DC 40 %, 347-359 nm) and #2 (W 800 nm, DC 50 %,
  351-363 nm) as family rows (D165): max ng ranges 38.93-43.21 / 34.89-47.74, ng 47.74 best near 1550 nm, loss ~12.5 and
  1.4 dB/mm (dB/cm derived) for #1, ng 4.10 at minimum loss, Table I geometry. Fab org_applied_nanotools. Not entered:
  slow-light bandwidth (ng >= 10 span) 8.24-8.82 / 7.24-7.47 nm, band-edge shift 2.63 / 2.55 nm/nm, loss-per-delay
  103.37 dB/ns (fit) / 32.15 dB/ns (raw), FDTD bandwidths and ng values.
- lahijani2026 (5 / 19): electronic-photonic circuit crossings (crossing.other) on suspended 240 nm Si: tapered
  topology-optimized EPCC (92.9 % mean measured -> 0.3198 dB derived; simulated T > 90.9 % / peak 93.6 %), curve-fitted
  EPCC (simulated T > 88.2 %; measured 80-89 % read off Supp. Fig. S10, extracted_from_figure), three single-wavelength
  design rows (gaps 100 / 60 / 20 nm: 96.6 / 99.2 / 99.8 %, > 99 % over 35 nm). Fab org_technical_university_of_denmark
  (author contributions). Not entered: simulated reflections R < 1.4 % / 1.2 % (back_reflection_db not allowed for
  crossing), Phi_b values, naive-gap and tapered-only references (Supp. Figs. S1-S2, simulated comparisons), 2x2 NEMS
  add-drop switch network (Fig. 3e-h has no stated values: no row), 25 V isolation (cited).
- luke2020 (2 / 14): DUV wafer-scale x-cut TFLN: lowest-loss ring (R 80 um, 2.0 um, 400 nm etch: Q_i 1.8e6, 0.21 dB/cm
  author_estimate per D76), wafer-level rib waveguide row (mean 0.27, std 0.05, range 0.21-0.36 dB/cm). Fab org_hyperlight
  (D72, "we deposited ... etched", all authors HyperLight); facilities CNF and CNS. Not entered: etch-depth uniformity
  (std 5.9 / 3.2 nm on another wafer).

## Organizations missing from the registry

- ePIXfab (abdulla2011 p.4 Sec. 3.1: SOI rings fabricated by the silicon photonics platform ePIXfab).

## Judgment calls for the coordinator

1. abdulla2011 MEMS-tuned ring as resonator.ring (not wdm.mrr / phase_shifter.mems): single tuned ring, channel-filter use
   only proposed.
2. lischke2021 fab org IHP kept borderline (D84b: thanks to IHP's cleanroom staff, no explicit fabrication statement); the
   1550 nm headline values excluded under D259 although the abstract presents them as results.
3. lischke2021 internal responsivity author_estimate (coupler de-embedding not described); santini2017 SSC 1.5 dB as
   author_estimate (stated in the design section without method) rather than D167 measured.
4. santini2017 receiver rows as photodetector.other (precedent ofc2026 M4D.3); hybrid imbalance measured through the PDs.
5. lahijani2026 EPCC as crossing.other with crossing_loss_db (dB from printed %, derived; simulated stays simulated) and
   the isolation trench in gap_nm.
6. hung2020 polarization TE on all rows inferred from the TE-only grating couplers; platform `other` (polysilicon gate on
   field oxide, substrate removed).

## Registry gaps (value actually skipped, locator, proposed definition)

- thermal_drift_pm_per_k for reflector: hung2020 76.5 / 27.3 pm/C measured, 17 pm/C simulated (p.9-10 Fig. 6(b), (d)).
  "Bragg / stopband centre wavelength drift per kelvin".
- pdl_db for photodetector: santini2017 UTC PD PDL < 0.7 dB (p.3 Sec. 3). "polarization-dependent loss of the PD
  responsivity".
- back_reflection_db for mode_converter and crossing: hung2020 strip-SWG converter -24 dB OFDR (p.7), lahijani2026 R < 1.4
  % / 1.2 % simulated (p.3, p.16). "power reflected back into the input, positive dB".
- slow_light_bandwidth_nm for waveguide_platform: jean2019 8.24-8.82 / 7.24-7.47 nm (p.5 Sec. IV-B). "span between the
  band edge and the wavelength where ng falls to the stated threshold (threshold in condition)".
- loss_per_delay_db_per_ns for waveguide_platform: jean2019 103.37 dB/ns fitted, 32.15 dB/ns raw (p.7 Fig. 11). "alpha c /
  ng".
- pull_in_voltage_v for phase_shifter / resonator (MEMS tuners): abdulla2011 9.2 V (40 um), 4.8-4.9 V (60 um) (p.7-9).
  "electrostatic pull-in (collapse) voltage of the actuator".
