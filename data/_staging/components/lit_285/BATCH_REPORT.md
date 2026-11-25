# lit_285 batch report

Distilled 2026-11-25. Papers: lit:wang2015, lit:xue2021, lit:wan2017, lit:yu2020, lit:gassenq2012 (all Optica Publishing
Group journals; III-V photodetectors on Si / Si3N4). Page-1 titles match the source rows; no correction / erratum; no
garbled text layer. Total 22 components / 125 metric rows. `merge_component_staging.py --dry-run`: 0 errors (2 warnings
belong to other batches: guo2024a, ni2025b).

Fab / facility: fab_org_ids is set on one row (wang2015 grating coupler, org_imec). facility_org_ids is set on the six
xue2021 rows (org_nanosystem_fabrication_facility). Every other row has both empty (passive fabrication sentences,
authors at several orgs, D80b / D154).

## lit:wang2015 (3 components / 32 metrics)

- `cmp_lit_wang2015_t2qw_pd` (photodetector.iii_v_on_platform, platform other: bonded III-V on SOI): fiber-referred
  0.1 A/W (2.3 um) and 0.12 A/W peak (2.32 um), waveguide-referred 1.2 A/W (both), QE 65 %, 0.6 A/W (2.4 um), > 0.5 A/W
  over 2.2-2.42 um, two Fig. 6(b) reads at -5 V; dark current 12 nA / 0.17 mA/cm2 (-0.5 V), < 100 nA (-3.5 V); 150 um
  mesa, 3.5 um top width.
- `cmp_lit_wang2015_iii_v_si_taper` (waveguide_platform.transition, other): simulated mode-to-mode coupling about 91 %
  (0.3 um tip, 150 um taper, Fig. 3(c) read); design geometry (tip 300 nm, end 2.5 um, Si 6 um, BCB 100 nm gap, 400 nm
  Si, 180 nm etch, 2 um BOX, 150 um taper).
- `cmp_lit_wang2015_gc` (fiber_chip_coupler.grating, soi, fab org_imec, process "imec's CMOS pilot line, 200 mm SOI, 193
  nm deep UV lithography"): about 9.5 dB peak at 2.35 um, 11 dB at 2.3 um, 150 nm 3-dB bandwidth, 1 um period, 20 x 20 um.
- Not entered: simulated > 95 % absorption over 150 um at 1000 cm-1 (p.4, no parameter); Fig. 3(c) 0.1 / 0.5 um tip
  curves (design siblings, in notes); Fig. 5(b) linearity (no parameter); GaSb comparison values in Sec. 1 (cited, refs.
  [11, 12]).
- Judgment calls: (1) waveguide-referred responsivities `derived` (GC efficiency measured, D517); (2) bias -0.5 V on the
  0.12 / 1.2 A/W peak rows taken from the Fig. 6(a) trace (text names no bias); (3) 0.6 A/W at 2.4 um entered as
  on_chip by inference from the abstract sentence pairing it with the waveguide-referred 1.2 A/W, bias not stated
  (value is strongly bias dependent, Fig. 6(b)); (4) 0.17 mA/cm2 kept as printed although 12 nA over the 150 x 3.5 um
  mesa top gives about 2.3 mA/cm2 (normalizing area not stated, flagged in notes); (5) fab org_imec only on the GC row
  ("The SOI waveguide fabrication is carried out in imec's CMOS pilot line", p.5); PD and taper rows empty (bonding and
  III-V processing passive, Contract v7 per-component fab); (6) the GC efficiency scope `per_coupler` with method
  `unspecified` (isolation method not stated).

## lit:xue2021 (6 components / 30 metrics)

- Five fabricated top-illuminated PDs (photodetector.vertical, iii_v_on_si_epi; geng2014 NIPD precedent): bulk InGaAs
  0.5 / 1.0 / 2.0 / 5.0 um long and InP/InGaAs QW 0.5 um. Values: lowest dark currents 0.55 nA (bulk) / 0.12 nA (QW) at
  -1 V; Fig. 3(b) reads for 1.0 / 2.0 / 5.0 um; responsivities 0.8 / 0.3 A/W (bulk), 0.6 / 0.2 A/W (QW), 0.3 A/W at 1.6
  um; saturation photocurrent > 0.3 mA (2 um), > 0.7 mA (5 um); bandwidth about 40 GHz (2 um, impulse + FFT) and > 40 GHz
  (Table 1, 0.5 um bulk and QW); lengths, i-InGaAs width about 300 nm.
- `cmp_lit_xue2021_si_iii_v_butt_coupler` (waveguide_platform.transition, row_kind design): simulated butt coupling
  up to 80 % (100 nm gap) and about 30 % (1000 nm gap); band unspecified (simulation wavelength not stated).
- Not entered: 10 / 15 / 40 Gb/s eye diagrams (no data-rate parameter; D534 gap already listed); operation span
  1240-1650 nm (no parameter; the 1600 nm point is entered); "QW PD dark currents all lower than 2 nA" (family statement,
  D254); Fig. 3(c) photocurrents (excitation power not stated); linearity fits (no parameter).
- Judgment calls: (1) responsivities `author_estimate` (photocurrent divided by an effective incident power from a
  beam-overlap calculation with assumed centring, p.3), ref_plane on_chip; (2) the 0.8 / 0.3 A/W pair is printed for the
  0.5 um bulk device in Table 1 and for the 2.0 um device in the p.3 text with Fig. 3(f) ("PD length: 2.0 um"): entered on
  both rows with a conflict note (D417) rather than dropped (D159 needs an ambiguous identity; here each tie is explicit);
  auditor please confirm; (3) the 2.0 um bandwidth kept `measured` approx 40 GHz (FFT of the measured pulse) although the
  printed TBP arithmetic 0.441 / 10 ps gives 44 GHz; (4) fab empty ("we then designed and fabricated", authors at HKUST and
  CUHK; xue2022 precedent).
- Missing org: "MCPF" of HKUST (facility; p.5 Acknowledgment "The authors thank the MCPF and NFF of HKUST for technical
  support"); not in organizations.csv / org_aliases.csv (also missing for xue2022).

## lit:wan2017 (3 components / 18 metrics)

- `cmp_lit_wan2017_qd_wgpd_20x50` (photodetector.iii_v_on_platform, iii_v_on_si_epi): dark current 0.8 nA at -1 V plus the
  Fig. 3(b) labels 4.8 / 18 / 69 nA at -3 / -5 / -7 V, 0.08 mA/cm2; fiber-coupled 0.33 A/W at 1250 nm; internal 0.94 A/W
  and 90 % (author_estimate: estimated 3 dB coupling loss); Cj 963 fF and Rs 8.8 Ohm (S22 fit, measured, D76); 3-dB
  bandwidth about 2.3 GHz (1550 nm, S12); mesa 20 x 50 um.
- `cmp_lit_wan2017_qd_wgpd_device2`: 1.5 GHz at -4 V, 1300 nm (heterodyne) and an inset read about 1.65 GHz at -8 V.
- `cmp_lit_wan2017_qd_microring_laser` (laser.other): threshold about 21 mA (from the on-chip PD photocurrent, Fig. 7(b));
  outer radius 50 um, mesa 4 um.
- Not entered: RC-limited bandwidth about 2.9 GHz and hole escape time about 30 ps (model calculations); Rp 1 MOhm (no
  parameter); "fiber coupled responsivity values in excess of 0.3 A/W in 1240-1340 nm" (p.5) because Fig. 4(a) exceeds
  0.3 A/W only near 1250 nm (in notes); Ge-on-Si comparison (cited, ref. [9], [32]).
- Judgment calls: (1) the second bandwidth device is a separate row ("a different device", size not stated; D159);
  (2) the 0.1-20 nA text range (-1 to -5 V) conflicts at its low end with the 0.8 nA label at -1 V: labels entered, range
  in notes (D417); (3) the micro-ring laser is entered although the platform's lasers were reported before (ref. [29]):
  the threshold comes from this paper's own Fig. 7(b) measurement; (4) fab / facility empty: passive fabrication; the
  acknowledgment thanks the UCSB nanofabrication clean room staff "for helpful discussions and assistance" (staff thanks,
  D72; not a fabrication statement, so no D84b borderline fab). SUNY Poly supplied the nano-patterned Si substrates
  (note only).

## lit:yu2020 (6 components / 26 metrics)

- `cmp_lit_yu2020_mutc_pd_family` (population row, D165 / gao2025b precedent; platform sin): external 0.8 / 0.33 A/W
  (30 um long, 1550 / 1064 nm), 0.68 A/W (10 um long), internal 0.94 / 0.83 A/W and QE 75 / 96 % (author_estimate:
  simulated coupling loss), typical dark current about 20 nA at -8 V; 450 nm absorber, 400 nm Si3N4, 60-70 nm window
  cladding, 4 um lower cladding.
- Sized single PDs: 10 x 30 um2 (20 GHz at -8 V / 2 mA, 69 fF measured, 50 Ohm author_estimate), 15 x 30 um2 (about
  11 GHz, Fig. 5 read), 10 x 70 um2 (about 6.5 GHz, Fig. 5 read); balanced 10 x 30 um2 pair (10 GHz differential, about
  20 nA at -8 V).
- `cmp_lit_yu2020_sin_inverse_taper` (fiber_chip_coupler.edge, sin): simulated mode-mismatch loss 0.7 dB (1550 nm) and
  4 dB (1064 nm) per facet with a 2.5 um tapered fiber.
- Not entered: PDL 0.67 dB (1550 nm) / 0.26 dB (1064 nm) (p.4; pdl_db not allowed for photodetector, registry gap
  below); CMRR > 40 dB (D81 rejected); 40 Gbit/s eye (no parameter); simulated transit-time-limited 40 GHz and RC-limited
  23 / 25 GHz (model); simulated 0.07 dB scattering loss at the bonded-layer edge (simulation input, no component);
  Table 1 values of other works (cited).
- Judgment calls: (1) responsivities put on a family row because "a 30 um-long PD" fits both the 10 x 30 and 15 x 30
  um2 devices (D159); (2) platform sin as gao2025b (same group, SU-8 bonded MUTC on Si3N4), not other; (3) fab empty
  (passive sentences; LIGENTEC and NIST authors but no fabrication statement naming an org, D80b); (4) 50 Ohm series
  resistance `author_estimate` (origin not stated, used in the RC estimate); (5) the 20 nA dark current entered both as a
  typical family value and on the balanced pair (Summary "Balanced PDs have 20 nA", Fig. 2); (6) QE "1060 nm" in the text
  stored at 1064 nm with a note.

## lit:gassenq2012 (4 components / 19 metrics)

- `cmp_lit_gassenq2012_evanescent_pd` (photodetector.iii_v_on_platform, other): waveguide-referred 1.4 A/W (2.3 um, TE)
  and 0.3 A/W (1.65 um, TM), derived on the measured GC efficiency; system responsivity peak about 0.1 A/W (Fig. 5(a)
  read); dark current density 300 mA/cm2 (room temperature) and 0.06 mA/cm2 (80 K) at -1 V; Rs 100 Ohm (Fig. 6(a)
  label); 500 nm absorber, 60 x 10 um mesa.
- `cmp_lit_gassenq2012_grating_pd` (photodetector.iii_v_on_platform, other): system 25 mA/W, intrinsic about 0.4 A/W
  (2.2 um, on the measured -12 dB GC), dark current about 4 uA / 0.4 A/cm2 at -1 V; 50 x 20 um mesa.
- Input grating couplers (fiber_chip_coupler.grating, soi): `..._input_gc_evanescent` 10 dB max around 2.2 um TE and a
  TM read about 9.5 dB near 1.67 um; `..._input_gc_grating_pd` 12 dB at 2.2 um.
- Not entered: R0A 0.1 Ohm cm2 (no parameter); minimum evanescent coupling efficiency (Fig. 5(c), a bound assuming 100 %
  collection, no photodetector parameter); epi-stack "intrinsic" dark current density about 10 mA/cm2 and 95 % sidewall
  share (fit over a population of test-mask and integrated devices); BCB absorption spectrum (material, Fig. 2);
  simulated absorbed-power fractions of designs 1 / 2-A / 2-B (Fig. 3(c), no parameter); design 2-B (simulated only, no
  performance parameter, no row); 0.35 A/W of the authors' earlier devices (cited, ref. [6]).
- Judgment calls: (1) the evanescent responsivity kept on the single evanescent row although its device size is not
  printed (only the dark-current device is 60 x 10 um; flagged in notes); (2) 80 K for "liquid nitrogen temperatures"
  from the Fig. 6(a) legend, bias -1 V from the same paragraph; room-temperature rows have temperature_k empty (Fig. 6(a)
  shows 300 K); (3) two separate GC rows (-10 dB vs -12 dB at 2.2 um; same design not confirmed); (4) grating geometry of
  design 2-A in PD notes (no photodetector parameter; chen2018a precedent); (5) fab empty: "standard CMOS technology" with
  no org; ePIXfab is named only as the MPW scheme the grating is "compatible with" (not a fabrication statement).

## Registry gaps

- `pdl_db` on photodetector: yu2020 PDL of the PD responsivity 0.67 dB at 1550 nm and 0.26 dB at 1064 nm (p.4 Sec. 3).
  Proposed: allow `pdl_db` for photodetector, definition "polarization dependence of the responsivity, max / min in dB".
- `data_rate_gbps` (already listed in D534): xue2021 40 Gb/s NRZ eye (p.4, Fig. 4(e)); yu2020 40 Gbit/s NRZ eye (p.5,
  Fig. 6).

## Missing orgs

- "MCPF" of HKUST (facility; lit:xue2021 p.5 Acknowledgment).
