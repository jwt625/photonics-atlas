# lit_194 batch report

Distilled 2026-11-18 (contract v4-v7, DevLog-007 rulings through D646). Papers: wang2020, pruessner2016, li2025f,
ikeda2010. Page-1 titles match the source rows. Totals: 12 components, 71 metric rows. Validation:
`merge_component_staging.py data/_staging/components/lit_194 --dry-run` -> +12 / +71, 0 errors (one unrelated warning
on merged ni2025b).

## lit:wang2020 (IEEE Access 2020, "Overview of Phase-Change Materials Based Photonic Devices") - 0 rows

- A review (abstract p.1 "we provide a comprehensive review"; p.2 "this paper presents a comprehensive review"). No
  first-person result, measurement, simulation or fabrication of the authors anywhere in the 35 pages; the data
  figures are reprinted from other groups' papers and Figs. 1, 6, 13 are schematics without values. Rules 1 / 3 (errandoherranz2019 precedent, D587): no rows.
- The authors' own earlier papers appear only as refs. [67], [71] (optical-disc history, p.6-7): cited, not entered.

## lit:pruessner2016 (Opt. Express 2016, opto-electro-mechanical neff tuning) - 5 components / 38 metrics

Components (all `phase_shifter.mems`, platform `sin`, Si3N4 175 nm rib with a suspended SiNx microbridge):
- `es_bridge_family` (5 devices, L_MEMS 50-120 um, Fig. 4(c), (d)): FOM 1.5 dB per 2 pi (0.75 dB/pi), simulated
  metal loss < 0.08 dB (L = 100 um), length range, stack geometry.
- `es_bridge_l120`: phase shift > 2 pi at 4.2 V.
- `es_bridge_l75`: mechanical resonance 2.3 MHz (2300 kHz derived), rise / fall about 400 ns (0.4 us derived).
- `dep_bridge_l100` / `dep_bridge_l40` (uncoated bridge, gradient-field actuation): about 1.5 pi at 36 V / > 0.5 pi
  at 60 V; transmittance drop 0.1 dB at 1.5 pi / 0.4 dB at 0.75 pi.

Not entered (why):
- Waveguide loss "as low as 0.7 dB/cm [27]" (p.4): cited (rule 3).
- delta neff > 0.02 measured, 0.01-0.1 claimed (p.7, p.10), mechanical Q 103 (p.9), pull-in voltage trend (Fig. 2(d)),
  "> 1 MHz" sinusoidal response (Fig. 7(a), not a stated 3-dB bandwidth): no registry parameter / not a defined width.
- Capacitance <= 1 pF, 12.5 pJ switching energy, 125 uW per pi at 10 MHz (p.9): model estimates for a generic device,
  stated once for the family (D254), notes only.
- Fig. 4(a) highest point about 470 deg (beyond the printed "> 2 pi"): note only.

Missing orgs:
- U.S. Naval Research Laboratory (fab): first-person fabrication, p.11-12 Appendix A2 ("We start with ...", "We etch
  110 nm ..."), p.7 ("we fabricated and measured"); all authors NRL. Fab left empty on all 5 rows until registered.
- NRL Nanoscience Institute (NSI) (facility candidate, borderline): p.14 acknowledgment thanks NSI staff "for
  cleanroom access and fabrication assistance". Staff thanks, so not entered (D72 / D84b); listed for the coordinator.

Judgment calls:
- (a) The paper's loss FOM (transmittance drop at the fringe maxima vs induced phase) is entered as
  `insertion_loss_db`, scope `per_component`, `excludes` the static 0 V loss, at the printed phase-shift point (1.5 dB
  at 2 pi; 0.1 dB at 1.5 pi; 0.4 dB at 0.75 pi). No dB/pi parameter exists; the FOM wording is in the condition.
- (b) The electrostatic FOM is stated for "the devices" of Fig. 4(d): one population row (D165, n_samples 5) instead
  of copies on each device row (D254); the L = 120 / 75 um devices are separate rows for their own values.
- (c) Wavelength not printed with any phase / loss value: `wavelength_inferred` with the measured spectrum spans
  (1490-1545 nm, Fig. 3(a) inset, electrostatic; 1470-1510 nm, Fig. 6(a), gradient-field); Fig. 7 values carry the
  printed 1502.0 / 1525.4 nm.

## lit:li2025f (Optica 2026, "Versatile wavelength-selective PZT photonic chips") - 4 components / 17 metrics

Components (platform empty: the guiding stack is only in the uncached Supplement 1, D422 / D423; fab
org_zhejiang_university from "we design and fabricate ... FP cavities", p.8, all authors ZJU):
- `fp2x1_cavity` (`resonator.bragg`, D539): excess loss < 1 dB (GC-pair reference), FSR about 20 nm, 19 pm/V DC
  tuning, non-volatile trimming range up to 3.4 nm.
- `fp2x1_nv_trim` (`phase_shifter.ferroelectric_nonvolatile`, same device, D396): 40 levels, 10,000 set / erase cycles
  at 120 C.
- `dwdm_40ch_fp_array` (`wdm.other`, array-level row): 40 channels, 1.6 nm spacing after trimming, max offset < 0.15 nm
  after / up to 1.9 nm before trimming, footprint about 1.54 mm2, design periods 400-418 nm, W = 2 um, N = 70.
- `equalizer_8ch` (`wdm.other`): 8 channels, attenuation about 18 dB (aligned resonances) and > 30 dB (overlapped).

Not entered (why):
- Modulator values: about 50 GHz EO bandwidth, 3.6 dB dynamic ER at 50 Gbps, 450 fJ/bit, 40 x 40 Gbps / 1.6 Tbps,
  3.2 Tbps/mm (p.3, p.6): rule 2, EO-atlas candidate (no EO-atlas row exists for this DOI).
- Threshold voltage about 9 V, Vth spread 2 V, trimming energy about 50 pJ, index change 5.3e-3, post-trimming std
  40 pm over four channels (p.3-5): no registry parameter, or meaning not defined in the main text.
- About 30 pm/K thermal coefficient (p.5) "based on our previous measurements [50]": rule 3 / D259.
- > 10^10 cycles for thin-film PZT (p.4): cited from ref. [55].
- 1x1 WSS of Fig. 5 (four 2x2 FP cavities, channels 1551.7-1556.5 nm): no printed performance value (linear plot,
  "high ER" only); `channel_spacing_nm` is not allowed on switch_fabric. No row (rule 9).
- Fifth grating period printed "42 nm" (p.5): misprint, not entered; the period row covers 400-418 nm.
- Equalizer "sub-dB" residual variation: no number.

Judgment calls:
- (d) 19 pm/V "modulation efficiency" kept as `tuning_efficiency_pm_per_v` on the resonator row (DC resonance shift,
  Fig. 2(d); D643 guarino2007 precedent), although the paper frames the cavity as a modulator.
- (e) Fig. 2(c), (d), (g) show resonances at different wavelengths (about 1552 / 1556 / 1574 nm); the text describes
  one 2x1 test element, so all are on one row with the ambiguity in notes (no D159 split: no second candidate row).
- (f) Endurance entered as 10000 with no qualifier: "Over 10,000 switching cycles, the device maintained ..." reads as
  the duration of the test and Fig. 2(h) prints "After 10,000 cycles" (merged adya2024 used `gt` for "over 10,000
  cycles"; flag if the coordinator prefers consistency).
- (g) Equalizer and array classed `wdm.other` (FP-cavity channel filters / channel attenuators in a WDM path, D400
  analogue); the external box CWDM module is setup, not a row.
- (h) Fig. 4 caption says the equalizer peaks were "trimmed thermally" while the text says non-volatile trimming:
  conflict noted (D417).

Missing orgs: none (org_zhejiang_university exists).

## lit:ikeda2010 (Opt. Express 2010, MEMS delay-line phase shifter) - 3 components / 16 metrics

Components (platform `soi`, freestanding 300 x 260 nm Si wire; fab empty: passive "designed and fabricated by silicon
micromachining", all authors Tohoku University, D80b):
- `mems_delay_ps` (`phase_shifter.mems`): 3.0 pi at 31 V (1.0 um displacement, 1459 nm, TE), device IL about 1 dB
  (IR-image reading), mechanical resonance about 153 kHz, footprint 4250 um2 (50 x 85 um), widths 300 nm design /
  245 nm SEM, coupler gap 250 nm design / about 280 nm SEM, 260 nm Si, 2 um BOX.
- `freestanding_si_wire` (`waveguide_platform.straight`): about 10 dB/cm.
- `elliptical_bridge` (`waveguide_platform.other`): about 0.1 dB per bridge (author_estimate, origin not stated).

Not entered (why):
- Air-gap couplers: only kappa*l (design 5 pi/4, fitted 1.36 pi, FDTD 1.34 pi; p.6); no registry parameter, geometry
  only -> no splitter row (rule 9); values in the phase-shifter notes.
- Response time "roughly 10 usec" (p.7): an estimate from the resonance, not a rise time.
- 0.1 dB modulation-contrast decrease (p.6): calculation. neff 1.1 (extracted) / 1.17 (BPM): no parameter.
- Silicon thermo-optic coefficient and heater power figures (p.2): cited background.

Judgment calls:
- (i) Device IL about 1 dB kept `measured` (own IR-image reading; "roughly estimated" quoted) with scope
  `unspecified` (reference level and facet inclusion not stated) and 1459 nm inferred from the Sec. 4 experiment.
- (j) 10 dB/cm and 0.1 dB rows carry 1500 nm `wavelength_inferred` from the setup laser "around 1.5 um" (p.4).

Missing orgs: none needed (fab not stated).

## Registry gaps (skipped value + locator + proposed definition)

- `delta_neff` (phase_shifter): pruessner2016 > 0.02 measured (p.7, Fig. 4(c)); li2025f 5.3e-3 (p.4). "Effective /
  material index change reached by the actuator, as stated" (already a candidate, D417).
- `mech_q` (phase_shifter, switch_fabric): pruessner2016 Q0,m = 103 in air (p.9, Fig. 7(c)) (candidate D438).
- `switching_energy_pj` (phase_shifter): li2025f about 50 pJ non-volatile trimming energy (p.3, Table 1); pruessner2016
  12.5 pJ estimate (p.9) (candidate D417 "switching energy").
- `threshold_voltage_v` (phase_shifter.ferroelectric_nonvolatile): li2025f Vth about 9 V (p.3), spread 2 V (p.5).
  "Voltage above which a non-volatile state change occurs".
- `pull_in_voltage_v` (phase_shifter.mems): pruessner2016 Fig. 2(d) (no printed number; candidate D440).
- `loss_per_pi_db` (phase_shifter): pruessner2016 FOM 0.75 / 0.07 / 0.53 dB/pi (p.7); now entered as
  `insertion_loss_db` at the printed phase point (call (a)). "Actuation-induced loss per pi of phase shift".
- `channel_spacing_nm` on switch_fabric: li2025f WSS 1.6 nm (p.7, Fig. 5(b)).
