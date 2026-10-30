# Batch lit_47 report (distill subagent, 2026-10-29)

Dry-run `batch lit_47: +16 components, +99 metrics; errors 0` (the one warning printed, cmp_lit_ni2025b_pimmwc-m18,
belongs to another batch). ASCII only, no e-mail or street text. Page-1 titles of all 4 cached texts match their
source rows; no correction / erratum, no garbled text layer. adya2024 is restricted (facts and locators only); chang2026a,
tamura2026, tossoun2024 are CC BY (open_license_ok), quotes still kept to a few words. Table / figure values checked on
page renders (adya2024 Fig. 1(b); chang2026a Fig. 3-4; tamura2026 Table 2; tossoun2024 Fig. 2, S1, S2, S5).
tossoun2024 processed fully (main p.1-29 incl. references, supplement p.30-44). chang2026a Supplementary Material is not
cached (values the main text defers to it are flagged).

## Per paper (components / metrics)

- adya2024 (4 / 17): GST on AMF zero-change PIN micro-heaters (amplitude-only, `phase_shifter.phase_change` per D155):
  8 um opening with 10 nm GST (ER 2.4 dB mean), 8 um with 12.5 nm GST (ER 8 dB; endurance > 10,000 cycles / 20,000
  events with ER 9.91 +/- 0.53 dB as mean + std rows; IL ~1.5 dB de-embedded), two cascaded heaters LSB 4.5 / MSB 9 um
  (4 levels, inter-level ER ~1.5 / 2.5 / 1.25 dB); AMF grating coupler 4 dB per coupler. Geometry: opening lengths
  (design), rib width 500 nm from the Fig. 1(b) label. Fab org_amf + org_cmc_microsystems (MPW, D398) + UW (authors
  sputtered / capped the GST themselves, all authors UW); GC row AMF + CMC only.
  Not entered: switching energies (RESET 108.35 / 103 nJ, SET 4.07e3 / 3.38e3 nJ) and pulse parameters (no parameter);
  amorphization ~1.5 us / crystallization ~80 us switching times (no parameter; rise_time_us is 10-90 %); heater
  effective resistance 256 ohm (measured device not identified among the variants, D159); SEM opening 1.5 x 7 um (sample
  not identified); simulated 0.03 / 3.32 dB/um a-/c-GST loss (per-length phase-shifter loss rejected, D250); Table 1
  rows of other works; Fig. 6 section-wise ER averages (overall mean entered).
- chang2026a (4 / 34): non-Hermitian Au side-heater TO phase shifter on 220 nm SOI in two sibling designs: MZI arm
  (~100 um heater: P_pi 10.18 mW derived from FSR / 2 eta, simulated 7.9 mW, V_pi 2.73 V from the Fig. 3(e) label,
  55 pm/mW, rise / fall 0.464 / 0.496 us, 729 kHz derived, own loss 0.042 dB author_estimate) and racetrack straight
  (80 um: cavity "P_pi" 1.72 mW entered as tuning_power_mw, 73 pm/mW, 0.60 / 0.80 us, 500 kHz derived); the asymmetric
  MZI as `switch_fabric.other` (IL < 1 dB vs reference waveguide, ER ~23 dB); the racetrack as `resonator.ring` (IL
  < 0.5 dB, ER ~8 dB, FWHM ~0.04 nm, thermal drift 75 pm/K, bend radius 30 um). Cross-section geometry (W1 500 nm,
  220 nm Si, 50 nm slab, 170 nm trench, 300 nm gap, Au 250 x 150 nm) on both phase-shifter rows. Fab
  org_shanghaitech_university (contributions: T.L. fabricated; affiliation ShanghaiTech only); facility
  org_shanghaitech_material_and_device_lab.
  Not entered: measured metal-induced additional loss ~1.95 dB/cm and simulated 0.3 / 0.4 / 0.9 dB/cm (no per-length
  phase-shifter loss parameter, D250); MZI FSR 1.12 nm and 1-dB bandwidth 0.3 nm (not allowed for switch_fabric);
  racetrack V_pi 1.21 V / I_pi 1.42 mA labels (cavity-detuning definition, not a pi phase shift); FOM values; W2 =
  300 nm heater-loaded Si width (no role parameter); Fig. 5 / Supp. Note 9 comparison of other works; photonic-crystal
  grating couplers and the 50:50 Y-junction (no stated metric).
- tamura2026 (5 / 30): five Sb2Se3-cladded (~29 nm + 10 nm SiO2) AMF Si rib microrings of a weight bank, one
  `resonator.ring` row per ring radius (8.0000-8.04852 um, design): Table 2 extinction per ring before PCM deposition
  (300 K), amorphous (300 / 4 K) and crystalline (300 / 4 K) with temperature_k; radius. Fab org_amf ("fabricated by
  Advanced Micro Foundry"); who sputtered the PCM not stated.
  Not entered: Table 1 room-temperature Delta n_eff 0.0560-0.0635 (no parameter); n_eff reproducibility 0.0010 /
  0.0023 over 3 thermal cycles (no parameter); Q factors (plots only, Fig. 7 / S5); n_eff(T), dn/dT of Sb2Se3 and Si
  (material properties, Fig. 3-6, S3); FEMWELL cross-section 500 x 220 nm rib / 90 nm slab / 3 um BOX (Fig. S2,
  simulation geometry); bare-Si chip thermo-optic data (Fig. S3, plot only). No phase_shifter row: the Sb2Se3 cladding
  has no registry-expressible performance value (phase shift in pi not printed).
- tossoun2024 (3 / 18): memresonator (bonded n-GaAs / ~10 nm Al2O3 / p-Si memristor in a 20 um-diameter III-V/Si ring)
  as `phase_shifter.other` (phase shift ~0.18 pi derived, retention 12 h = 43200 s derived, endurance 1,000 cycles,
  3 levels HRS / IRS / LRS, IL 0.047 / 0.048 dB HRS / LRS from the ring fit) and as `resonator.ring` (Q ~9933, FSR
  2.808 nm, FWHM 0.13 nm, finesse 21.5 derived, radius 10 um derived from the 20 um diameter, ring / bus width 500 nm,
  gap 200 nm, Si 300 nm, BOX 2 um, etch ~170 nm); grating coupler ~6 dB per coupler at peak. Platform `other` (bonded
  III-V/Si, cheung2023 precedent from the same group). Fab empty (no explicit fabrication statement, contract v4).
  Not entered: switching energies 0.15 / 0.36 pJ and SET / RESET pulse widths 300 / 900 ps (no parameter); read
  energies ~5 fJ / ~2 aJ; electroforming 9 V, set ~5 V, reset ~-4 V; HRS leakage < 10 nA; HRS/LRS resistance ratio
  ~1e3; read transmission ~0.27 vs ~0.1 (approximate linear values); L_pi ~0.35 mm (estimate); "extinction ratio is
  27.55" (no unit); Fig. S2 coupling / loss vs bias for 10 / 20 / 25 um radius rings (plots); Table 1 values of other
  technologies; cited 28 GHz III-V/Si MOS ring modulator bandwidth.

## EO-atlas candidates

None. tossoun2024's n-GaAs/Al2O3/p-Si SIS stack is the HPE MOS ring-modulator stack, but this paper uses it only as a
non-volatile memory phase shifter (no EO bandwidth / Vpi measured; the 28 GHz figure is cited).

## Missing orgs (name as printed + locator)

- Washington Nanofabrication Facility (WNF), University of Washington, Seattle, US (adya2024 p.3 and acknowledgements
  p.10: post-processing "conducted at"); facility_org_ids left empty. Already reported for chen2024a.
- Core Facility Platform of Electronics, ShanghaiTech University, Shanghai, CN (chang2026a acknowledgements p.10, device
  fabrication and characterization support); not entered.

## Judgment calls for the auditor

1. adya2024 IL ~1.5 dB is stated once in the general measurement text (p.5); entered on the 12.5 nm row because Table 1
   ties IL 1.5 dB to "This work" (8 um, 1.4 dB/um, 20,000 events). Alternative: note only (D254).
2. adya2024 heater resistance 256 ohm (Fig. 4(a), "the PIN micro-heater") kept as a note (D159): the heater design is
   common to all variants, so entering it on both 8 um rows is the alternative.
3. adya2024 fab orgs: AMF + CMC (D398, "providing MPW fabrication services") + UW (authors did the GST post-process).
4. chang2026a racetrack "P_pi" (P = FWHM x pi / eta) entered as `tuning_power_mw`, not `p_pi_mw`, because it is not a pi
   phase shift; MZI V_pi 2.73 V from a figure label entered `derived` (point on the measured I-V at the derived P_pi).
5. chang2026a bandwidths 729 / 500 kHz entered as `bw3db_khz` `derived` from rise / fall times (hess2026, kim2019
   precedents); not small-signal measurements (condition says so).
6. chang2026a phase-shifter own loss 0.042 dB `author_estimate` (derivation only in the uncached Supp. Note 14).
7. chang2026a: the same cross-section is entered on both phase-shifter rows (sibling designs differ in heater length).
   Racetrack heater length not entered as heater_length_um ("straight sections with the heater aside" does not state
   the heater spans 80 um): `length_um` 80 with condition instead.
8. tamura2026: "Before PCM deposition 300K" extinction entered on the Sb2Se3-ring rows (read as the same chip before
   sputtering); the paper also had a separate bare-Si chip of identical rings, so the alternative is note only (D159).
   CMC Microsystems ("provision of products and services", FABrIC) not entered as fab org.
9. tossoun2024 IL 0.047 / 0.048 dB entered as printed (`derived`, ring_extraction, per_component), but the printed
   formula IL = 10 log10(alpha) with alpha 0.945 / 0.937 gives 0.25 / 0.28 dB, not 0.047 / 0.048 dB. Flagged in notes.
10. tossoun2024 ring consistency: FSR 2.808 nm for a 10 um radius implies n_g ~9.7 near 1320 nm (implausible for a Si /
    III-V rib); Fig. S5 broadband spacing is ~3.5 nm; Fig. S2 shows 10 / 20 / 25 um radius rings. The S2 values (Q,
    FSR, FWHM, finesse) and the 0.18 pi phase shift (which uses FSR 2.808 nm) may come from a different ring than the
    20 um-diameter device. Entered as the paper attributes them, with a note; alternative: drop radius or the S2 values
    (D159).
11. tossoun2024 fab empty although all authors are HPE (no "we fabricated" or contribution statement); the merged
    cheung2023 rows from the same group carry org_hewlett_packard_enterprise because that paper states in-house
    fabrication (its supplement).

## Registry gaps (proposed)

| parameter / enum | class | skipped value, locator | proposed definition |
|---|---|---|---|
| switching_energy_nj | phase_shifter, switch_fabric | adya2024 RESET 108.35 / 103 nJ, SET 4.07e3 / 3.38e3 nJ (p.5-6); tossoun2024 SET 0.15 pJ, RESET 0.36 pJ (p.16, Supp. S1); earlier proposals shoaa2025 / li2026b (switching_energy_uj, programming_energy_uj) | electrical energy per state change of a non-volatile actuator (SET / RESET, pulse amplitude and width in condition; one unit for all rows) |
| switching_time_us | phase_shifter, switch_fabric | adya2024 amorphization ~1.5 us, crystallization ~80 us (p.6-7 Fig. 5); tossoun2024 SET 300 ps, RESET 900 ps pulse widths (p.4, p.16) | time to complete a non-volatile state change as defined by the paper (programming pulse width vs optical settling in condition); not a 10-90 % rise time |
| delta_neff | phase_shifter | tamura2026 0.0560-0.0635 amorphous -> crystalline Sb2Se3 cladding, 300 K (p.4 Table 1) | effective-index change of the guided mode between two non-volatile states (states, wavelength, temperature in condition) |
| fsr_nm, bw_1db_nm (allow) | switch_fabric | chang2026a asymmetric MZI switch FSR 1.12 nm, 1-dB bandwidth 0.3 nm (p.6) | as for wdm / splitter: FSR and 1-dB passband of an interferometric switch element |
| per-length phase-shifter loss (D250 rejected, listed only) | phase_shifter | chang2026a measured metal-induced loss ~1.95 dB/cm (p.6); adya2024 simulated 0.03 / 3.32 dB/um (p.3) | - |
| leakage_current_na (low priority) | phase_shifter | tossoun2024 HRS leakage < 10 nA (p.8, Supp. S3) | DC leakage current of an electrically programmed non-volatile actuator at the stated state and bias |
