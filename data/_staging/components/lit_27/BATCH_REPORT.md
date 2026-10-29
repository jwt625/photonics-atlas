# Batch lit_27 report (distill subagent, 2026-10-29)

Dry-run `batch lit_27: +27 components, +196 metrics; errors 0`. ASCII, no e-mail, no quotes (gao2026 and
amirtharaj2025 are open_license_ok, none needed). Page-1 check: all nine cached texts match their source rows;
gao2026 is arXiv v1 with a different title from the journal title in the row (same authors and work, like lapointe2025).

## Per paper (components / metrics)

- zhang2025 (1 / 17): inverse-designed PSO Si crossing (crossing.other, AMF 220 nm SOI). Per-crossing loss from 50
  cascaded crossings vs reference ((P_dev - P_ref)/50, derived) full band and S / C / L values; cutback slope 0.09 dB
  (measured); wafer histogram mean 0.08 dB n = 208; crosstalk (P_xt - P_ref, derived); simulated loss / crosstalk;
  length 8 um, footprint, W1, 220 nm. Fab org_amf (fabricated at AMF, p.5). Not entered: simulated crosstalk below
  -65 dB at unnamed wavelengths, wafer box plot, Table 2 (other works).
- atsumi2018 (5 / 17): elephant coupler 9 um taper (fiber_chip_coupler.other; 4.2 dB min near 1600 nm loopback_half,
  includes ~0.5 dB of 2.5 mm waveguide; best-angle 0 deg; geometry), 7 um-taper FFP device (mfd_chip_um 5 um from the
  Gaussian fit), SMF design variant (0.6 dB/facet simulated, row_kind design), Si waveguide (~2 dB/cm derived from 0.5 dB
  / 2.5 mm), Ar+-implanted waveguide absorption 800 / 300 dB/cm before / after anneal (derived from dB/um). Fab
  AIST. Not entered: 0.5-dB bandwidth > 150 nm, FFP 14 / 23 deg widths, 0.5-dB angle window 6 deg, dome size, design 0.8
  dB / 420 nm and TM 2.4 dB (restated from the authors' design paper [12], D259).
- he2019 (3 / 21): bilayer TFLN SSC (3.4 dB fiber-to-fiber best, < 1.7 dB/facet derived, 3-5 dB span, 88% simulated,
  +/- 1 um 1-dB tolerance, 1 W / 30 dBm for > 1 h, MFD, full two-layer geometry with tip_width 30 / lower_tip 340 nm),
  bare rib reference facet 11-14 dB fiber-to-fiber, ring Q_L 1.5e6 and < 0.125 dB/cm (author_estimate). Fab
  org_harvard_university (authors fabricated; all six list Harvard SEAS first), facility CNS. Not entered: Fig. 5(a)
  efficiencies vs tip width, simulated MFD / n_eff curves, SMF28 route (cited).
- korcek2023 (9 / 74): single-etch Si3N4 GCs, air-clad, 400 nm LPCVD: uniform Lambda 860 nm DC 65 / 70 / 60%, periods
  830 / 890 nm, SWG GCs DC 60 / 70%, apodized 7-period GC (2.9 dB at 1561 nm), Si3N4 strip waveguide 3.0 dB/cm. Per-GC
  losses loopback_half derived (set-up / waveguide / bend losses subtracted, Methods); centre wavelengths; FDTD loss,
  1-dB bandwidth, back-reflections (% -> dB); back-reflection from FP ripple (~7%, ~3%) derived; geometry. Fab empty,
  facility C2N. Not entered: Figs. 7 / 9 / 10(c) library summaries (plotted), directionality / overlap (no parameter),
  bend loss 0.25 dB/bend (bend angle not stated), SWG gap +/- 20 nm deviations.
- zhou2023 (1 / 15): center-symmetric multi-cavity focusing GC on imec poly-Si overlay SOI: best 3.0 dB (loopback_half
  derived: averaged pair, waveguide neglected), 1-dB bandwidth 108 nm (1519-1627 nm), mean 3.35 dB / 105.6 nm (16 GCs),
  bandwidth range 96-112 nm (8 chips), simulated 2.91 dB / 109 nm, footprint, pitch, stack. Fab org_imec (MPW, p.4-5).
  Not entered: foundry library GC 30 nm (not measured here), minimum feature 181 nm.
- amirtharaj2025 (0 / 0): fs-laser U-groove glass fiber array. Only performance number is the fiber-to-fiber
  misalignment angle 1.51 +/- 0.23 deg (p.6 Sec. 3.2), which has no parameter; geometry alone (pitch ~128 um measured,
  groove depth ~77 um measured vs 62.5 um design, 3 um wall) is not a row (D49). Fab would be IIT Madras (S.S. Ram
  fabricated, p.7; in registry).
- kopp2023 (1 / 13): Chiral Photonics four-core MCF pump-signal combiner (wdm.other, silica, fiber-only, D80f): signal IL
  0.4 dB C-band, pump IL < 0.4 dB at 980 nm, crosstalk 63 dB headline, > 70 dB adjacent counter-propagating pairs,
  pump / signal crosstalk matrices as ranges (64.5-72.1, 55.9-70.7 dB, n = 12), dip spread +/- 8 nm, pitches, lengths.
  Fab org_chiral_photonics. Not entered: return loss > 70 dB (gap), PDL (plot only), package size.
- aamer2012 (4 / 18): two-etch SOI polarization rotator 25 um (polarization.other; IL 1-2.5 dB de_embedded derived over
  1545-1575 nm; geometry), DC polarization splitter (per_db > 25 dB), TE focusing GC (~5 dB) and TM GC (~6 dB),
  author_estimate (origin not stated). Fab empty (passive description, authors at UPV, Ghent-IMEC, CEA-Leti, DAS).
  Not entered: PCE > -0.85 dB over 30 nm (gap), 21 / 23 um rotators (plot only), splitter gap 300 nm.
- gao2026 (3 / 21): TFLT adaptive polarization controller (polarization.compensator: on-chip IL < 4 dB, PDL < 0.3 dB
  (abstract), mean PER 19.6 dB in closed loop, footprint, stack), PSR (measured ER > 20 dB and PDL < 0.3 dB over C+L;
  simulated ER > 40 dB, IL < 0.05 dB), SiON / bilayer-TFLT edge coupler (measured PDL < 0.3 dB; simulated IL < 0.35 dB,
  PDL; tip widths). Fab org_huazhong_university_of_science_and_technology (S.L., G.Y. fabricated; all authors HUST),
  facility org_wuhan_anpi_optoelectronics (fabrication performed at the cleanroom of Wuhan ANPI Corporation). Not
  entered: tracking speeds 2 / 1 Mrad/s (gap); EO metrics (MZI V_pi 2.46 V, ER ~24.6 dB, ~1 GHz packaged bandwidth,
  TW modulator 86 GHz projected): EO-atlas candidate.

## Fab / facility organizations missing from the registry

- Advanced Micro-Nano Fabrication Center, HUST (gao2026 p.27 acknowledgments, listed among supporters; not entered).
- "Wuhan ANPI Corporation" (gao2026 p.27) mapped to registry org_wuhan_anpi_optoelectronics (Wuhan ANPI
  Optoelectronics Company Ltd) by name; confirm.
- RENATECH network (korcek2023 p.9, support statement, program; not entered).

## Judgment calls (coordinator to confirm)

1. korcek2023 fab empty (fabricators at Zilina, CEA-Leti, C2N per author contributions); C2N entered as facility
   (work done within the C2N platforms). Alternative: fab C2N (ronn2019 precedent).
2. gao2026 fab HUST + facility ANPI (company cleanroom where the HUST authors fabricated); alternative fab ANPI.
3. he2019 fab Harvard: all authors list Harvard as first affiliation, fabrication at Harvard CNS.
4. korcek2023 period +30 nm device: text prints 830 nm for both period variants; entered as 890 nm per the +/- 30 nm
   wording and the Fig. 6(b) legend (890 nm curve peaks near 1580 nm).
5. korcek2023 FDTD design values on the DC 70% row (the design point), although the paper compares them with the DC 65%
   device (-5% bias).
6. kopp2023 class wdm.other (pump-signal WDM, garciablanco2025 precedent); fiber_interface.other would admit the 70 dB
   return loss.
7. zhang2025 cascade values (P_dev - P_ref)/50 and crosstalk differences entered derived (wang2026 / lit_05 ruling).
8. atsumi2018 4.2 dB scope loopback_half measured (per-coupler value stated directly, halving not shown, D167).
9. zhou2023 / he2019 best values without a stated peak wavelength: measured span entered with wavelength_inferred.

## Registry gaps

| gap | skipped value | locator | proposed definition |
|---|---|---|---|
| bw_0p5db_nm for fiber_chip_coupler | atsumi2018 0.5-dB-loss bandwidth > 150 nm | p.7 Sec. 4 | full width within 0.5 dB of peak transmission (also proposed for wdm in lit_11) |
| beam_divergence_deg for fiber_chip_coupler | atsumi2018 far-field FWHM ~14 deg, 1/e2 23 deg | p.6 Fig. 5(b) | far-field divergence of an out-of-plane coupler (level in condition) |
| back_reflection_db for wdm | kopp2023 return loss > 70 dB, all channels (OFDR) | p.4 Sec. 3 | as the existing definition, for fiber-pigtailed WDM parts |
| fiber_misalignment_angle_deg (fiber_interface) | amirtharaj2025 1.51 +/- 0.23 deg between adjacent fibers | p.6 Sec. 3.2 | angle between the optical axes of fibers in an array |
| polarization_conversion_efficiency_db (polarization) | aamer2012 PCE > -0.85 dB over 30 nm (25 um rotator) | p.3 Sec. IV | 10 log10(P_converted / (P_converted + P_unconverted)), magnitude in dB, definition in condition |
| tracking_speed_rad_per_s (polarization) | gao2026 2 Mrad/s transient, 1 Mrad/s continuous reset-free | p.2 Abstract; p.14 | highest SOP rotation rate tracked within the stated error criterion |
| crosstalk_db for polarization | gao2026 PSR simulated through-port crosstalk -30 dB (TM0) / -24 dB (TE1) | p.5-6 | as the existing definition |
| gap_nm, coupling_length_um, taper_length_um for polarization | aamer2012 splitter gap 300 nm; gao2026 PSR gap 0.6 um, L1 380 um, Lc 180 um | p.2 Sec. III; p.5 | role geometry of DC-based PBS / PSR |
| lens_radius_um for fiber_chip_coupler.other | atsumi2018 SiO2 dome diameter 5.4 um; SMF design dome radius 6.5 um | p.3 Sec. 2; p.8 | radius of an integrated lens / dome cap of an out-of-plane coupler |
| bend loss per bend of unstated angle | korcek2023 0.25 dB/bend, R 80 um | p.5; p.6 Fig. 5(e) | not proposed (bend_loss_db_per_90 needs the angle) |
