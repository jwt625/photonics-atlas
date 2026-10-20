# Batch report ofc_03 (OFC 2026, facts only, 2026-10-20)

Transcribed by the coordinator from the batch agent's final report. Dry run: 0 errors; 19 components, 84 metrics from
12 papers (10 with rows, 2 without). No e-mail addresses, quotes a few words at most, no same_as.

## Per paper (components / metrics)

- W3E.4 (1/4): inverse-designed 4-channel mode/polarization multiplexer (mode_converter.mdm_mux, 220 nm SOI): IL
  < 1.5 dB and crosstalk > 18 dB over 1520-1580 nm, 9 chips (IL scope unspecified: test configuration not stated);
  footprint 36 um2 (derived 6 x 6); thickness 220 nm. Not entered: IL std < 0.15 dB (no parameter), MRM EO bandwidth
  (EO atlas). Fab empty ("300-mm CMOS platform", foundry not named).
- Th2A.1 (2/15): PLC-SiN SSC to InP SOA (chip_chip_coupler.butt) ~2.0 dB per_interface incl. ~0.5 dB SMF packaging
  loss, ~1.5 dB excluding it, both author_estimate (rest on a ~2.5 dB lensed-fiber reference of unstated origin);
  widths 1.6-3.0 um, SiN 0.2 um. InP SOA array: measured MFD mean 2.52 x 2.31 um (24 facets) plus ranges, simulated
  TE/TM MFDs, geometry. fab TU/e (D72). Not entered: simulated loss variation < 0.1 dB over 100 nm; Fig. 3(g) box plot.
- M1E.1 (1/5): MZI-coupled Si microring: 3-dB bandwidth 110 GHz (C band inferred from FWM wavelengths); Q_loaded
  ~4.0e4; propagation loss ~12 dB/cm (derived); FSR 1.28 nm (design); ring length 406 um. fab HUST (D72). Not
  entered: spectral-utilization 0.68, coupling coefficients, simulated FWM efficiency.
- W2A.55: no rows (fiber sensing system; DFB is a setup source).
- Th1K.2 (3/6): uncooled TO-can DFB SMSR > 50 dB, 8 MHz intrinsic linewidth (author_estimate), 55 pm/K (derived from
  0.055 nm/C); SVR on-chip PD 55 GHz (origin not stated), 0.9 A/W at "5V" as printed; double-lens SOA-to-SVR
  packaging ~6 dB, scope unspecified. No wavelength anywhere.
- M2E.4 (1/2): DFB + Si3N4 MRR SIL intrinsic linewidth 72 Hz (pi * f0, f0 = 23 Hz^2/Hz) at 1563 nm.
- Tu2J.5 (2/10): five- and ten-mode SiN edge couplers to the highly elliptical-core fiber. fab Applied Nanotools
  (MPW); facility CMC Microsystems (fabrication support acknowledged). Five-mode measured at 1560.5 nm 2.4-3.8 dB for
  four modes, TE04 5.5 dB; intro 2.4-5.1 dB (conflicts with 5.5 dB, both kept with cross-notes); simulated 1.9-2.8 dB
  and 1.5-2.5 dB (intro). Ten-mode simulated 1.1-2.1 dB at 1550.8 nm. Measured scope unspecified.
- W4E.3 (1/3): 1060 nm coupled-cavity VCSEL > 3 mW single-mode, SMSR > 40 dB, > 45 GHz at 6 mA B2B. Not entered:
  link bandwidth after 500 m OM4, 50 GHz lateral resonance. Fab not stated.
- Th1D.5 (2/7): fab imec ("IMEC The Netherlands" via the Stichting imec Nederland alias). Laser-trim permanent phase
  shifter (phase_shifter.other) 0.2 dB best at 4 rad, 0.08 dB per ring; SiN double-ring Vernier Q ~7800 / ~12500,
  ~7 dB main-to-side extinction, main resonance 1549.56 to 1549.98 nm. Not entered: 0.16 dB sum, phase range 3.9-11
  rad, dB/rad, 125 C / 1000 h stability.
- Th3F.2 (2/22): Ge/Si SACM APDs, L = 10 um O band and L = 30 um C band, fab imec. Dark current < 1 uA to -8.5 V
  (derived, in nA); primary responsivity 1.0 / 0.55 A/W at -2 V; max ~100 A/W on_chip after GC loss; bandwidth and
  responsivity pairs per bias; C band > 100 GHz from -3 V. Sec. 2 gives 90 GHz at 1.5 A/W (-7 V), Sec. 3 / abstract /
  conclusion 100 GHz: both entered. Most locators pNA (Sec. 2 before the first page image).
- W4J.3: no rows (electronic SiGe ADeMUX chip).
- Th1D.7 (4/10): Ge-silica 3 mm ring Q_i > 180M over 458-1550 nm, best 463M at 1064 nm; propagation loss 0.0008 dB/cm
  and < 0.01 dB/cm (derived); FSR 21.2 GHz (origin not stated); radius 1500 um (derived); thickness 4 um. SIL FP
  lasers 15 Hz at 632 nm, 12 Hz at 512 nm, 90 Hz at 444 nm. Fab empty (UCSB and KNI staff thanks only).

## Judgment calls

J1 purchased / commercial lasers that are part of the demonstrated system and characterized are rows (Th1K.2,
M2E.4, Th1D.7); setup lasers, PDs, amplifiers are not. J2 Th1D.5 trimming as phase_shifter.other; trimming-system
supplier in notes only. J3 CMC Microsystems ("fabrication ... supported by") in facility_org_ids (earlier geravand2025
listed CMC as fab when worded "via CMC"). J4 Th2A.1 chip_chip_coupler.butt. J5 conflicting values both entered with
cross-notes. J6 unit conversions basis derived.

## Registry gaps reported

il_std_db; wdl_db and crosstalk_db for fiber_chip_coupler / chip_chip_coupler; breakdown_voltage_v (photodetector);
phase_shift_rad, loss_per_rad_db (phase_shifter); spectral_utilization (resonator); surface_roughness_nm;
n_channels for amplifier. No missing orgs.
