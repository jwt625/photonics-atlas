# Batch lit_43 report (distill subagent, 2026-10-29)

Dry-run `batch lit_43: +22 components, +117 metrics; errors 0`. ASCII, no e-mail, no quotes (all six sources
`restricted_local_only`). Page-1 titles / authors match all six source rows; no cached text is a correction or erratum
(D409). No supplement cached for any paper.

## Per paper (components / metrics)

- akiyama2021 (6 / 24): 4-ch cascaded AMZ triplet (CAT) demux, wdm.cascaded_mzi (total crosstalk per port 57.6 / 52.1 /
  54.5 / 49.3 dB as crosstalk_cumulative_db; loss 5.0 dB worst port and 2.9 dB mean, de_embedded since the fiber
  couplers are excluded; total heater power 76 mW as tuning_power_mw; 2 stages, arm increments 25 / 50 um, 450 x 220 nm,
  footprint 900 x 500 um derived); simulated CAT design row (crosstalk -50 to -40 dB for 4-64 ch at 100 GHz, abstract /
  Fig. 11); doped-Si heaters 400 um and 200 um (phase_shifter.thermo_optic: P2pi 50.7 mW halved to p_pi_mw derived,
  2.2 / 1.1 kOhm derived); MMI coupler 0.45 dB (author_estimate, origin not stated); 15 % tap (author_estimate). Not
  entered: MMI 160 x 20 um (which is width not stated), Ge monitor PD 140 x 20 um (geometry only), heater response time
  about 100 us (no definition), projected 1.87 dB design, per-channel heater power about 12 mW (stated for round- and
  flat-top CATs together, D254). Journal extension of the authors' OECC / ECOC 2019 papers: Sec. 4 values kept (D408).
  Fab empty (MPW with a standard CMOS PIC process, no org named).
- ikeda2020 (6 / 23): 2x2 16-ch WSS, switch_fabric.wss (fiber-to-fiber IL 9.2 dB mean and 8.6 dB at 1550 nm; on-chip
  5.4 dB mean and 3.56 dB at 1550 nm as author_estimate since they rest on the 1.92 dB facet term; bar / cross extinction
  15.0 / 23.0 dB mean; 16 ch, 2 x 2); MZ switch element switch_fabric.other (D158; trimming 3.8 mW and switching 15.6 mW
  mean with std rows, as power_consumption_w derived); C-DC wdm.bragg_cdc (3-dB bandwidth 4.2 nm mean, measured through
  the WSS; Table 1 W 350 / 450 nm, gap 250 nm, L ~500 um, period 351-386 nm); inverse-taper SSC 1.92 dB per facet
  (author_estimate: waveguide 1.46 dB and polarizer 1.2 dB terms of unstated origin); DC polarizer 1.2 dB per path
  (scope unspecified); reference waveguide 6.5 dB fiber-to-fiber and 1.46 dB. Not entered: MZ switch loss 0.13 dB (cited
  ref. [4]) and C-DC loss 0.20 dB computed from it (rule 3); corrugation depths 40 / 60 nm (gap). Fab AIST (own 300-mm
  CMOS R&D foundry, D84a).
- li2023 (2 / 13): TFLN dynamic polarization controller, polarization.compensator (fiber-to-fiber 5 dB, on-chip < 2 dB,
  recovery time 1.6 us measured / 0.6 us emulated as tracking_time_us, footprint 1.8 cm x 4 mm derived, stack geometry);
  bilayer suspended edge coupler (coupling loss < 1.8 dB scope unspecified, PDL about 0.5 dB; platform empty). Not
  entered: tracking speed 100 krad/s, loop delay 420 ns, excursion std, DOP (no parameter, gao2026 / lin2022 precedent);
  EO phase shifter Vpi 2.75 V and simulated VpiL 4.1 V cm (EO-atlas candidate, skill rule 2); PSR IL < 0.5 dB over
  110 nm (sentence cites the authors' earlier paper [31], D259 / D259a); PSR and MMI geometry (no performance: not rows);
  about 7 dB "entire DPC" (contents not stated). Fab empty (NanoLN wafer only, passive "fabricated"). li2023 was a D397
  re-fetch: the cached text is the right paper.
- zheng2023 (3 / 24): visible SiN ridge PBS, polarization.pbs (PER >= 20 dB 624-657 nm TM0 through, peak 27.3 dB at
  648 nm, > 15 dB over 100 nm; >= 18 dB 580-630 nm TE0 cross, peak 22.5 dB at 610 nm; simulated about 40 / 30 dB; on-chip
  IL <= 1 dB both ports and 0.85 / 0.83 dB from the printed overall losses, all derived vs the straight reference;
  fiber-to-fiber 13.67 / 14.79 dB; length 43 um, 500 nm film, W 220 nm, 4.7 um SiO2); multi-arc bent TE filter
  (waveguide_platform.bend, simulated: TM0 < 3 dB / TE0 > 13 dB over 400-1200 nm, bend loss 0.03 / 1.507 dB/um at
  R = 3 um as 300 / 15070 dB/cm, simulated); straight reference waveguide 12.82 / 13.96 dB fiber-to-fiber. Not entered:
  DC gap 400 nm, coupling length 25 um, taper 220 -> 500 nm, bend radius on the PBS row (not allowed for polarization).
  Table 1 says 590-645 nm vs text bands (text entered, noted). Fab empty (authors at four orgs, no fab statement naming
  them).
- kwon2020 (1 / 16): EAM-integrated heater-tuned DBR-LD, laser.dbr, InP (threshold 12-14 mA range, slope about 0.22 W/A,
  > 25 mW at 150 mA, peak about 1304 nm, SMSR > 35 dB at 80 mA / over tuning / under modulation, tuning about 15 nm within
  2 V, 16 ch at 0.55 nm, kappa about 25 /cm design, section lengths). Not entered: EAM bandwidth > 20 GHz, static ER
  about 10 dB, DER 7.2-8.1 dB (modulator metrics, EO-atlas candidate); heater 6 x 200 um (gap). Fab ETRI ("we fabricate",
  all authors ETRI).
- skandalos2026 (4 / 17): monolithic InAs/GaAs QD DBR laser on Si with SiN DBRs, laser.dbr / iii_v_on_si_epi (Ith 213 mA
  at 25 C, 133.25 mA at 15 C, 90 mA pulsed; 2.08 mW single-port on-chip derived; 1298.2 nm; T0 51.81 K pulsed; 7 x
  3000 um); QD SOA amplifier.soa (net gain 5.18 dB at 1320 nm 20 C and -3.41 dB at 40 C derived, 3-dB bandwidth about
  46 nm, about 2.5 V and 0.625 W at 250 mA, 15 x 1350 um); III/V-SiN DLARC interface waveguide_platform.transition
  (1.45 dB best, cut-back, platform other); SiN waveguide 3.04 dB/cm mean (spread +/- 1.37 dB/cm in notes, kind not
  stated). Not entered: interface back-reflection -14.8 dB (std 3.04 dB) and angled < -60 dB simulated (gap); threshold
  current densities (gap); cited [41, 42, 44] values. Fab Southampton on all rows, plus UCL on laser / SOA (UCL author
  performed the metallization, UCL grew the QD material; borderline, D80b).

## Missing fab / facility orgs

- "TIA Super Clean Room of AIST" (ikeda2020 p.8 Acknowledgments, device fabrication supported): facility, not in the
  registry (also seen in earlier batches' notes).
- "Southampton Nanofabrication Center part of the ORC, at the University of Southampton" (skandalos2026 p.8
  Acknowledgment, fabrication carried out at): facility, not in the registry.

## Judgment calls for the coordinator

1. ikeda2020: WSS channel 3-dB bandwidth put on the C-DC row (wdm.bragg_cdc) because bw_3db_nm is not allowed for
   switch_fabric; alternative is notes only (D407 style).
2. skandalos2026: UCL as second fab org on the laser / SOA rows (metallization by a UCL author, epitaxy at UCL).
3. akiyama2021: the simulated 4-64 ch design row; heater P2pi halved to p_pi_mw (derived) rather than tuning_power_mw
   per 2 pi.
4. li2023 edge coupler platform left empty (facet stack ambiguous); zheng2023 IL bounds normalized to a reference
   waveguide entered as derived (D80a).

## Registry gaps

- bw_3db_nm for switch_fabric: ikeda2020 WSS 16-ch average 4.2 nm (p.5 Fig. 5); def "drop / pass-band full width at
  -3 dB of a WSS channel".
- corrugation_depth_nm (wdm, reflector): ikeda2020 C-DC dW1 / dW2 40 / 60 nm (p.3 Table 1); def "sidewall corrugation
  (modulation) depth of a grating".
- back_reflection_db for waveguide_platform: skandalos2026 III/V-SiN interface -14.8 dB mean (p.6 Fig. 5(b)); def as
  existing, per interface.
- threshold_current_density_a_per_cm2 (laser): skandalos2026 1015 / 634 / 428.6 A/cm2 (p.3, Table 1).
- heater_width_um / heater_length_um for laser: kwon2020 DBR heater 6 / 200 um (p.4).
- gap_nm, coupling_length_um, min_bend_radius_um for polarization: zheng2023 400 nm, 25 um, 3 um (p.4-6) (also gao2026
  / lin2022).
- tracking_speed_krad_per_s (polarization): li2023 100 krad/s (p.6); def "highest SOP scrambling speed tracked within
  the stated error criterion".
- heater response time (phase_shifter): akiyama2021 about 100 us (p.12), definition not stated; no proposal.
