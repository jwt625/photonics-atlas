# lit_177 batch report

Distilled 2026-11-16. Papers: lit:bundalo2022, lit:zhong2014, lit:gui2021, lit:larrea2018, lit:doerr2010 (selected because other papers cite them in benchmark tables; only values each paper reports itself are entered). Page-1 titles match the source rows; no garbled text layer, no correction-only file. `merge_component_staging.py --dry-run`: +16 components, +74 metrics, 0 errors.

Totals: 16 components, 74 metric rows.

## lit:doerr2010 (3 components / 21 metrics)

Wide-bandwidth Si3N4 grating coupler (IEEE PTL 2010).

- `cmp_lit_doerr2010_sin_gc_400nm` (fiber_chip_coupler.grating, sin; 18 rows): 4.2 dB peak (`loopback_half`, derived: the paper plots the square root of the pair transmission, D516 / D542), 1-dB width 67 nm (derived, same curve), peak about 1570 nm (Fig. 4 read), TM > 18 dB over the Fig. 4 span, back reflection > 22 dB (pair, both polarizations, measured), simulated 3.9 dB / 67 nm (with substrate) and 5.7 dB / 74 nm (grating alone), geometry (400 nm SiN fully etched, 2.25 um BOX, about 2.0 um cladding, 1.2 um pitch derived, 13 periods, fill factor 0.5, 8 deg, 17.5 um grating width).
- `cmp_lit_doerr2010_sin_gc_bragg_mirror_design` (design; 2 rows): simulated 1.9 dB / 90 nm with a Bragg mirror.
- `cmp_lit_doerr2010_sin_waveguide` (waveguide_platform.straight, sin; 1 row): about 1.5 dB/cm TE at 1550 nm, method not stated.

Not entered: Eq. (3) analytic 1-dB bandwidths (55 nm generic SOI, 95 nm generic 400 nm SiN; not this design); 0.2 dB per 1 um fiber shift (no 1-dB tolerance); 0.6 um minimum feature (no parameter; fill factor covers it); cited values (SiN 0.02 nm/C ref. 8, 36 / 50 nm prior bandwidths refs. 5 / 9); 127 um grating spacing (test-pair spacing, not a pitch).

Judgment calls: fab `org_astar_ime` borderline (D84b): acknowledgment thanks two named staff of the Institute of Microelectronics, Singapore, "for discussions and fabrication" (p.3); authors at Bell Labs, Alcatel-Lucent. Peak wavelengths of measured and simulated curves read off Figs. 2(b) / 4 (`wavelength_inferred`, uncertainty in notes).

## lit:larrea2018 (2 components / 14 metrics)

O-band SOI parabolic inverted-taper SSC with lateral air trenches (IEEE PTL 2019).

- `cmp_lit_larrea2018_parabolic_taper_ssc` (fiber_chip_coupler.edge, soi; 13 rows): about 2 dB per facet at 1310 nm (`author_estimate`: Eq. (4) subtracts a 5 dB/cm x 0.5 cm propagation term measured on a different sample, +/-1 dB/cm, and assumes equal facets), Fig. 7 measured range 1.6-3.5 dB over 1280-1340 nm (figure read), simulated 0.5 dB (BPM) and 1.1-1.2 dB (FDTD, Fig. 7), simulated 1-dB tolerances (horizontal +/-1.4 um; vertical -1.2 / +1.8 um as value / value_max with the axis in the condition, D460 practice), geometry (70 nm tip, 130 um, 500 nm W_Si, 220 nm / 3 um BOX, 3.5 um cladding, 8 um cover width).
- `cmp_lit_larrea2018_si_wire_waveguide` (waveguide_platform.straight, soi; 1 row): about 5 dB/cm, cutback on the sister sample, O band inferred.

Not entered: Fig. 2-3 design trends (about 1 dB without trenches, facet-distance curves); "below 1.5 dB for gaps below 20 um" (not a 1-dB tolerance); "60 nm bandwidth with losses mostly below 3 dB" (criterion bandwidth, no parameter; the Fig. 7 row covers the span); SMF core 8.2 um (core diameter, not MFD).

Judgment calls: polarization `te` from the TE design plus the polarizer-set "correct polarization" (p.3), noted. Fab `org_upv` borderline (D84b): "proposed, designed, fabricated and demonstrated" + thanks to "the fabrication team of the Nanophotonics Technology Center"; all authors at NTC-UPV (D533 / D553 precedent).

## lit:zhong2014 (3 components / 21 metrics)

Focusing-curved subwavelength grating couplers, 220 nm SOI (Optics Express 2014).

- `cmp_lit_zhong2014_fc_swgc` (fiber_chip_coupler.grating, soi; 13 rows): 6.4 dB near 1550 nm and 1-dB width > 100 nm (measured, `loopback_half`: per-coupler curve from the pair, halving not printed, D452), simulated 2.72 dB / 122 nm (no air gap), design geometry (period 1.16 um and SWG period 0.3 um derived, ff_G 0.5, 220 nm / 3 um / 1.975 um stack, 20 deg, 20 um taper, footprint 800 um2 derived).
- `cmp_lit_zhong2014_fc_swgc_tapered` (fiber_chip_coupler.grating, soi; 5 rows): headline 4.7 dB near 1550 nm, 1-dB width > 100 nm, footprint, stack (Table 1).
- `cmp_lit_zhong2014_swgc_custom_stack_design` (design; 3 rows): simulated 1.91 dB with 2.84 um BOX / 1.837 um cladding.

Not entered: subwavelength fill factors 0.67 / 0.13 and effective indices 2.79 / 1.71 (no parameter; notes); Fig. 5 air-gap simulation (about 70 um gap reproduces 6.4 dB; explanatory fit); Fabry-Perot ripple FSRs 1.1 / 18 nm and the about 50 % ripple-extinction reduction (no component parameter); Table 1 rows for refs. 7-9 (other works); straight-line SWGC comparison (values in the authors' OFC paper, ref. 20).

Judgment calls: fab `org_university_washington` from "The devices were fabricated at the University of Washington - Washington Nanofabrication Facility (WNF)" (p.8; D448, lu2015a precedent). Measured rows use the printed "near 1550 nm" (D393); figure peaks (about 1555 / 1557 nm) in notes.

## lit:gui2021 (1 component / 2 metrics)

Homodyne coherent BiDi DCI system with a polarization-tracking SiP coherent receiver (JLT 2021).

- `cmp_lit_gui2021_pt_icr_thermal_ps` (phase_shifter.thermo_optic, platform empty; 2 rows): insertion loss < 0.3 dB and phase tuning speed about 20 kHz (`bw3db_khz`, criterion not stated; both `author_estimate`, no measurement shown; velha2016 precedent). Band `unspecified`: the paper prints no wavelength at all.

Not entered: tracker speed up to 300 rad/s without penalty (Fig. 5(a); no registry parameter, see gaps; the tracker as a `polarization.compensator` row would have no performance metric, rule 9); ITLA (about 100 kHz) and DFB (about 500 kHz, about 1.5 MHz Lorentzian-equivalent) linewidths, SBS thresholds about 9 / 15 dBm (lasers are external sources injected into the transceivers, rule 13; system-level); link budget, reach, BER results (system-level); PSRs, hybrids, BPDs (no values).

Judgment calls: platform empty (only "SiP" printed, D422 / D423); fab empty (no fabrication sentence; "real product", authors at Huawei, D80b).

## lit:bundalo2022 (7 components / 16 metrics)

PIXAPP Datacom demonstrator: single-chip SOI transceiver with flip-chip EICs, micro-optical-bench laser and pluggable microlens connector (JSTQE 2022).

- `cmp_lit_bundalo2022_tx_output_gc` (fiber_chip_coupler.grating, soi; 3 rows): 2.57 dB (Table II), 10 deg emission, MFD 9.2 um at 1310 nm (stated design property, `author_estimate`).
- `cmp_lit_bundalo2022_tx_laser_input_gc` (fiber_chip_coupler.grating, soi; 2 rows): 2.6 dB (Table II), 10 deg MOB beam.
- `cmp_lit_bundalo2022_tx_splitter` (splitter.other, soi; 1 row): 6.10 dB as printed (split order not stated, ideal split not separated).
- `cmp_lit_bundalo2022_tx_routing_wg` (waveguide_platform.other, soi; 2 rows): 1.7 dB (GC to splitter), 0.67 dB (MZM to GC).
- `cmp_lit_bundalo2022_mob_coupling` (micro_optics.other; 4 rows): measured laser-to-GC loss 8.9-9.5 dB on test structures (multiple MOBs), about 0.5 dB placement / gluing, Table II 2.0 dB, 10 deg beam.
- `cmp_lit_bundalo2022_mob_laser` (laser.other; 2 rows): spectral peaks 1308.2-1310.2 nm (80-100 mA), module output -13.2 to -12.1 dBm at 80 mA (`ref_plane module`, whole Tx path in `includes`).
- `cmp_lit_bundalo2022_pluggable_microlens_connector` (fiber_interface.connector, polymer; 2 rows): about 1.5 dB additional loss per interface relative to direct fiber-GC coupling (IMEC + KIT lenses), expanded MFD about 30 um at about 2 mm.

All Table II terms: `author_estimate` + `loss_breakdown` (origin not stated; D428 / D437), O band inferred from the 1310 nm laser specification. process_name "iSiPP50G (Europractice imec Si-photonics offering, ref. 15)" on the imec PIC rows, fab `org_imec` ("IMEC designed and fabricated PICs in SOI platform [15]", p.3).

Not entered: MZM loss at quadrature 7.30 dB (Table II), modulator optimum wavelength 1289 nm and 28 / 56 Gb/s eyes (modulator metrics stay in the EO atlas, rule 2; EO-atlas candidate); Table II total 22.94 dB (path total, not a component); RF line losses (about 3 dB / 2.5 dB simulated / about 5 dB with PIC at 42 GHz, LTCC 0.29 dB/cm at 10 GHz, PCB about 1 dB; electrical); thermal simulation (laser 36 C average, 77 C active region); laser saturation 80-100 mA (no parameter); working distance 2 mm (no parameter, registry candidate D437); 980 um glass block thickness (no parameter); PIC footprint 5.1 x 5.1 mm (chip, not a component); EIC bump counts.

Judgment calls: (1) Table II "Micro optical bench 2.0 dB" vs measured 8.9-9.5 dB laser-to-GC loss plus a separate 2.6 dB input GC term do not reconcile; both kept with a D417 note (scope `unspecified` on the 2.0 dB row). (2) Laser peaks "1308.2 nm and 1310.2 nm respectively" follow the 80 / 100 mA saturation sentence; pairing implied but not explicit, entered as one range row. (3) Input and output GCs kept as separate rows (design identity not stated). (4) Connector loss is for the IMEC + KIT version; the tested module used IMEC lenses on both sides with no separate loss value. (5) Fab per component: MOB placement Tyndall + Argotech (p.5-6), connector imec (PIC lenses) + KIT (fiber lenses) + Tyndall (connector); Argotech fixing the receptacle (Table I) noted only.

## Missing fab / facility orgs (not in organizations.csv / org_aliases.csv)

| Name as printed | Role | Paper, locator | Rows waiting |
|---|---|---|---|
| Washington Nanofabrication Facility (WNF), University of Washington | facility | lit:zhong2014 p.8 Acknowledgments (also co-author affiliation p.1) | cmp_lit_zhong2014_fc_swgc, cmp_lit_zhong2014_fc_swgc_tapered (queued since D420 / D454) |
| Nanophotonics Technology Center, Universitat Politecnica de Valencia | fab (unit of org_upv) | lit:larrea2018 p.1 affiliation, p.4 Acknowledgments | cmp_lit_larrea2018_parabolic_taper_ssc, cmp_lit_larrea2018_si_wire_waveguide (open since D533 / D553) |
| Cordon Electronics Italia (Cordon Electronics Italy) | fab (MOB assembly) | lit:bundalo2022 p.5 Sec. III-C; p.3 Table I; p.8 Table III | cmp_lit_bundalo2022_mob_coupling |
| Eblana Photonics Ltd. | fab (laser supplier, vendor of the laser die) | lit:bundalo2022 p.5 Sec. III-C; p.3 Table I; p.8 Table III | cmp_lit_bundalo2022_mob_laser |
| US Conec | supplier note only (MTP/MPO receptacle components) | lit:bundalo2022 p.4, p.9 Acknowledgment | none |
| VTT Technical Research Centre of Finland Ltd | LTCC interposer maker (electrical, no component row) | lit:bundalo2022 p.6, Table III | none |

"Institute of Microelectronics, Singapore" (lit:doerr2010 p.3) mapped to `org_astar_ime` (alias "IME Singapore" ruled in D540; this exact string may need an alias).

## Registry gaps

- `polarization_tracking_speed_rad_per_s` (polarization.compensator, switch_fabric): highest polarization rotation speed tracked without penalty; lit:gui2021 300 rad/s, p.5-6 Sec. IV-B, Fig. 5(a).
- `working_distance_um` (fiber_interface, micro_optics; D437 candidate): lit:bundalo2022 2 mm between lens surfaces, p.4 Sec. III-B, Fig. 8.
- Criterion bandwidth (`criterion_bw_nm`, D539 candidate): lit:larrea2018 60 nm over which losses stay "mostly below 3 dB", p.1 Abstract / p.4.
