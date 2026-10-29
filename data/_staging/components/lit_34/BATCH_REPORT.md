# Batch lit_34 report (distill subagent, 2026-10-29)

Dry-run `batch lit_34: +49 components, +172 metrics; errors 0`. ASCII only, no e-mail addresses, no quotes. Page-1 title
and authors match the source row for all 9 papers. Not audited or merged.

## Per paper (components / metrics)

- barwicz2017 (14 / 31): garbled text layer. `references/barwicz2017/figures/` holds no page_NN.png (only img_pNN files),
  so the 3 pages were rendered from source.pdf into the scratchpad and read there. Nothing taken from text.md.
  - Rows: Si metamaterial and Si nanotaper chip-chip butt couplers (chip_chip_coupler.butt). Simulated 1 dB tolerances:
    ~1.7 um horizontal from the text; vertical and nanotaper values read off Fig. 2(d), +/-0.05 um.
  - 12 mode_converter.converter rows, one per length (rule 9): metamaterial converter 62.5 / 125 / 250 / 500 um at design
    feature size (Fig. 4(b)) and with ~13 nm reduced feature size (Fig. 4(c)); nanotaper converter 37.5 / 75 / 150 /
    250 um (Fig. 4(a)). Each has one IL read at the labelled marker (+/-0.05 dB) and its length.
  - Text peak -0.9 dB put on the 250 um converter (top curve of Fig. 4(b)); the text gives no length.
  - Fab org_ibm_watson: chips fabricated in the IBM Watson Microelectronics Research Laboratory (p.3). No facility: own
    lab (D404).
  - Not entered: > 95% simulated mode overlap (overlap, no parameter); < 0.35 dB spectral penalty over 120 nm (gap);
    rod spacing 400 nm (gap); de-embedding method not stated (scope per_component, method unspecified).
- theurer2020 (3 / 10):
  - Rows: InP gain chip to SiN TriPleX flip-chip interface, Sec. IV. Values: theoretical 0.3 dB (simulated), 1-1.5 dB
    (author_estimate), gain-chip MFD 5.1 x 4.2 um (derived from far field), 6 um gap.
  - Hybrid Vernier tunable laser: threshold 10 mA, > 60 mW, 39 nm, SMSR > 50 dB.
  - Intracavity ring#2 (D400): group index 1.549 from OFDR peak spacing (derived).
  - Not entered (D259a): all Sec. III DFB results (Figs. 2-8 marked [16], the authors' ECOC 2019 paper): 2.1 dB mean /
    0.35 dB std over 18 lasers, 1.6 dB, > 60 mW, SMSR, 4-array 2.25 +/- 0.1 dB. Also not entered: the TriPleX MFDs
    (cited from [16]) and the 1.3 dB DFB theoretical loss. So the abstract's headline 2.1 dB is not in the table.
  - Ring round-trip losses 0.19 / 0.27 dB not entered (gap). Ring#1 has no other value, so no row.
  - Relative power variation 1.5 dB over tuning not entered. Fab empty: no org stated for chips or assembly.
- xu2021 (8 / 27):
  - Rows: hybrid ECL (laser.tunable): 30 mA, 0.035 W/A, 50 nm, SMSR > 40 dB, ~3 dBm operating level, 105 kHz Lorentzian.
  - Intra-cavity PWB: 2.1 dB from own ASE before / after assembly (derived), Si tip 180 nm.
  - RSOA: Psat 12.5 dBm at 3 dB compression, 23 dB gain, both on-chip corrected (D166 derived).
  - Rings R1 / R2 (D400): FSR 368.2 / 340.7 GHz, Q ~28,000, radius from diameter, 180 nm gap, P_pi 24.4 / 24.1 mW as
    tuning_power_mw.
  - Vernier reflector (reflector.other): 1.7 dB calculated from fitted parameters (derived). Cavity phase tuner:
    P_pi ~24 mW (author_estimate). Output GCs >= 5 dB (origin not stated).
  - Fab org_karlsruhe_institute_of_technology on the ECL and PWB only (module jointly fabricated by two KIT authors,
    D399). SiP chip: standard 248 nm DUV process with no org named.
  - "U.T. and M.M. contributed the InP-based components" is not a fab statement. Not entered: RIN (measurement floor),
    T = 13.4, f_min, 73 GHz gain ripple (fsr_ghz not allowed for amplifier), PWB 2.4 x 2.0 um cross-section (axis order
    ambiguous, kept in core_material).
- chen2025 (4 / 8):
  - Rows: OPA SOA chain (amplifier.soa): 15.4 dBm at 1534 nm, 10 C (derived; corrected for own 13.3 dB free-space link
    loss) and 10.3 dB net on-chip gain. The gain is author_estimate because the on-chip input was measured with the
    booster SOA and a foundry-provided responsivity. Also 8 channels and 2.2 um pitch.
  - Edge coupler ~4 dB (author_estimate, same reason). Star coupler 0.3 dB (simulated). 85/15 MMI design split
    (author_estimate, D82a).
  - Fab org_smart_photonics (MPW).
  - No free_space_emitter row: no emitter performance value.
  - Not entered: 12 MHz system modulation bandwidth (EOPM, an EO-atlas quantity); < 3 dB output drop across the C-band;
    EOPM IL / 8 GHz bandwidth (cited [19] / foundry).
- sotirova2024 (3 / 11):
  - Rows: 8-channel SPIM-WG glass pitch reducer, 127 to 8 um (fiber_interface.fan_out). Chip nearest-neighbour
    crosstalk ~5e-4 entered as 33.0 dB (derived 10 log10). System-level crosstalk with the trapped ion: below 1e-3 for
    all channels (30 dB gt) and O(1e-5) at best (50 dB approx, best).
  - Coupling efficiency 45(3)% average and ~80% with mode matching. Scope unspecified: evaluated at the chip output.
    Also pitch, channel count, VGA MFD 3.5 um and core width.
  - Sibling rows: design without input mode matching (< 60%) and the conventional laser-written chip (3e-2, 15.2 dB).
  - Fab org_oxford on the SPIM rows (B.S. designed and fabricated the chips). The conventional chip's fabrication is not
    attributed, so its fab is empty.
  - Not entered: 0.67 um waist and 3.95 um spacing at the ions (after the relay optics, system values).
- andreou2019 (4 / 23):
  - Rows: InP monolithic Vernier ring laser. Tuning 34 nm (32 simulated), threshold ~56 mA, 1.8 mW in fiber, ~7 ohm,
    SMSR > 50 / 59 dB (> 45 simulated).
  - Linewidths: 109 kHz, < 110 kHz, 95 kHz best, ~140 kHz at 1555 nm, 230 kHz free-running DSH, < 1 kHz PDH-locked
    (< 1 ms observation, derived).
  - Also 1.4 mW mean tuning power per ring and 2.32 pm/V (derived from the printed 0.29 GHz/V at 1548.6 nm). Calculated
    13.5 GHz cavity FSR and ~35 nm Vernier FSR (simulated); radius ~200 um; footprint.
  - Output edge coupler typical ~4 dB (author_estimate). 85/15 out-coupler and 2x1 50% ring MMIs (design splits).
  - Fab org_smart_photonics (MPW).
  - Not entered: 15 deg/V/mm (foundry spec [26]); 0.1 dB/90 deg bend (stated for the technology, no source); PDH control
    range / loop bandwidth.
- kumar2024 (5 / 20):
  - Rows: standalone III-V/Si Vernier laser: 13 mA, > 20 mW, > 50 nm, < 16 kHz, RIN < -150 dB/Hz; closed loop
    SMSR > 55 dB, > 10 dBm, < 30 kHz; super-FSR > 50 nm.
  - SOA-integrated laser: > 50 mW, > 17 dBm over 27.5-47.5 C, SMSR > 50 dB, 80 pm fine tuning at ~4 pm/mW.
  - Two intracavity rings (FSR ~1.36 / ~1.39 nm, 9.1% coupling). The paper does not map the FSRs to Ring 1 / Ring 2, so
    the rows are labelled by FSR.
  - Sagnac front mirror 42.5%.
  - Fab org_intel (Intel's own 300-mm heterogeneous process, all authors Intel; D84a). Platform `other` (bonded
    III-V/Si; iii_v_on_si_epi is for grown epi).
  - Not entered: wafer-level medians over ~300 lasers (design under test not stated, D159); < 1 GHz locked frequency
    error; Table I (comparison image).
- hassan2020 (3 / 9):
  - Rows: Si strip pseudo-GRIN metalens (micro_optics.metalens; works as a 3 um to 350 nm on-chip mode converter).
    0.6 dB / 85% TM at 1310 nm vs reference waveguides (derived), 90% FDTD, L 2.3 um, W 3 um, Si 310 nm, BOX 1 um.
    SEM and design strip widths are in core_material.
  - Design-only EMT lens: 65% at 2.193 um. Abrupt multimode-to-single-mode junction: 5 dB (mode_converter.other).
  - Fab org_cea_leti. The fabrication was also done by a Vistec Electron Beam GmbH author, an org missing from the
    registry.
- maier2022 (5 / 33):
  - Rows (micro_optics.facet_lens): VCSEL-to-MM-FA (0.35 dB mean / 0.25 std / 0.05 best active; 0.5 dB passive
    author_estimate; +/-17 / 13 um).
  - MM-FA-to-PD (0.70 / 0.06 / 0.63; +/-62 / 54 um).
  - VCSEL-to-MCF-cores (0.67 / 0.79 active, 1.0 dB passive; +/-18 / 13 um).
  - MCF-cores-to-PD (0.63 / 0.56 / 0.30; +/-23 / 25 um).
  - Design beam MFDs, pitch, channel counts.
  - SMF loopback FaML damp-heat structure (Table 1: 1.2-1.5 dB initial, 1.3-1.5 dB after 3960 h at 85/85).
  - Bases: Tx means are derived (array-average VCSEL power). Tx per-channel and std values are author_estimate (they
    assume equal VCSEL powers). All Rx values are author_estimate (datasheet PD responsivity).
  - Fab empty: printing on an in-house and a commercial Vanguard system, mixed-org authors, no fab statement.
  - Not entered: angular tolerance 1.3 deg (gap), VCSEL M2 4.2 / 5.4 (gap), the unphysical -0.16 dB channel, focal spot
    MFDs 12 / 15 um (not beam_diameter_um), link metrics (TDEC, ER, OMA).

## Missing orgs

- Vistec Electron Beam GmbH, Jena (hassan2020 p.1 affiliation 2; p.6 author contributions: fabrication by J.-A.D.).
  Not mapped to org_vistec_lithography (different entity, no name-only mapping).

## Judgment calls for the audit

1. barwicz2017 class split: chip_chip_coupler.butt for the coupler ends (tolerances) and mode_converter.converter for the
   measured routing-to-coupler converters, one row per length and feature-size variant. All converter losses are figure
   readings except the text peak.
2. theurer2020 D259a applied to the whole DFB section because every DFB figure carries [16]. The paper's headline
   coupling loss is therefore not entered.
3. hassan2020 classed micro_optics.metalens rather than mode_converter.converter.
4. sotirova2024 classed fiber_interface.fan_out (glass pitch reducer). Coupling-efficiency scope unspecified.
5. Intracavity Vernier rings as resonator.ring (D400) in xu2021, theurer2020 and kumar2024. The xu2021 Vernier
   double-ring mirror is also entered as reflector.other for its calculated reflection loss.

## Registry gaps

- `wdl_db` for mode_converter / chip_chip_coupler: barwicz2017 < 0.35 dB spectral penalty over 1510-1630 nm (p.1, p.3).
- `subwavelength_period_nm` for chip_chip_coupler / mode_converter / micro_optics: barwicz2017 rod spacing 400 nm
  (Fig. 3(a)); hassan2020 strip period 250 nm (p.3). `fill_factor` for micro_optics: hassan2020 0.2-0.8 (p.3).
- `roundtrip_loss_db` (resonator): ring round-trip loss incl. coupler outcoupling, from OFDR peak decay. theurer2020 0.19
  / 0.27 dB (p.5).
- `tol_1db_angular_deg` (micro_optics, fiber_interface): angular misalignment for 1 dB excess loss. maier2022 1.3 deg
  (p.7, Fig. 3(b)).
- `beam_quality_m2` (laser, micro_optics): beam quality factor M2 per axis. maier2022 VCSEL 4.2 / 5.4, effective 4.8 (p.4,
  p.18 App. B).
- `fsr_ghz` for amplifier: facet-ripple periodicity of an RSOA. xu2021 73 GHz (p.3 Fig. 2(b)).
