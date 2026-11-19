# lit_207 batch report

Distilled 2026-11-18. Validation: `merge_component_staging.py data/_staging/components/lit_207 --dry-run` -> +1 components, +9 metrics, 0 errors (the one warning concerns an existing ni2025b row, not this batch).

## lit:cezar2024 (Fabrication of Y-Branch Power Splitters using Additive Manufacturing, ICTON 2024)

Page-1 title matches the source row. 4 pages, clean text layer.

Components / metrics: 1 component, 9 metric rows.

- `cmp_lit_cezar2024_y_branch` (`splitter.y_branch`, platform `polymer`, fabricated): DLP 3D-printed 1x2 Y-branch, PMMA resin doped with 5 % v/v PFeBSe core on a printed pristine PMMA substrate, 30 mm long, multimode, measured at 635 nm.
  - m1 `excess_loss_db` 8.04-10.66 dB, range over 3 samples, `device_total`, measured (p.4 Table I; p.3 Sec. IV). Per-sample values in notes.
  - m2 `imbalance_db` 0.27-0.60 dB, derived: per-sample |left - right| of the Table I per-port coupling ratios; the text prints 0.6 dB worst case.
  - m3 / m4 `split_ratio_pct` right port 47.10-53.46 %, left port 46.56-52.97 %, derived (10^(-CR/10) of the printed dB coupling ratios).
  - m5-m9 geometry: `length_um` 30000 (printed 30 mm), `pitch_um` 2000 (printed 2 mm), `width_nm` 800000 (printed 800 um, design model), all derived by rescaling (D157); `n_inputs` 1, `n_outputs` 2 design_target.

Values not entered and why:

- Expected minimum excess loss 6 dB for a 30 mm structure (p.3-4): computed from the 0.1 dB/mm propagation loss the authors cite from their earlier work ref. [10] (rule 3).
- 6.8 dB excess loss (p.4): another group's work, ref. [11] (rule 3).
- Core index 1.515 and cladding index 1.491 at 635 nm (p.2): cited from ref. [10]; in component notes only, no parameter.
- Fig. 1 BPM simulation: no number.
- Angle of 9.5 deg between the arms at the branch tip and design-model length 33 mm (p.2 Sec. II): no splitter angle parameter; the 33 mm model length differs from the printed 30 mm device, so only the printed length is a row; both in notes.
- Fig. 2 labels 0.50 and 1.00 (mm): not tied to a named dimension in text or caption (could be guide height above the substrate and a groove / guide width); not entered.
- Input-guide cross-section diameter about 1 mm (p.3 Sec. IV): stated only to justify the beam size and conflicts with the 800 um arm width of the design model; in notes.
- Print parameters (0.05 mm layer height, exposure times, 405 nm source): process data, no parameter; layer height in `core_material`.

Missing fab / facility orgs (not in `organizations.csv` / `org_aliases.csv`):

- "Fed. Univ. of Technology - Parana" (printed with an acute accent on the a; UTFPR): fab role. p.2 Sec. III "The DLP printer ... is employed in our fabrication process", all six authors at this institution (p.1). Fab left empty until the org exists. Already requested as the parent of Multi-Foton in D428 (lit_71 audit).
- "Multi-Foton facility of UTFPR in Curitiba": facility role, p.4 Acknowledgment ("the use of the Multi-Foton facility"). Already requested in D428 as "UTFPR-CT Multi-Foton".
- Not entered as orgs: ITA / CTA (p.4, thanked for guidance and use of the RSoft simulation package: simulation software, not fabrication); Anycubic (printer maker, equipment, p.2); Fibracem Teleinformatica Ltda, CNPq, Fundacao Araucaria (funding, p.1 footnote).

Judgment calls:

- (a) Scope: a mm-scale, free-space-coupled 3D-printed polymer splitter kept in scope as a planar integrated-optic splitter, following the same group's merged moralesalvarado2026 Y-branch (D428: D411 unchanged).
- (b) Excess loss scoped `device_total`: the paper defines it as input power over the sum of both outputs, so it includes input coupling, face reflections, propagation and scattering; plane of the input-power measurement not stated (note).
- (c) Table I "coupling ratio" read as each port's power relative to the summed output in dB (each sample's two ports sum to 100 % within rounding), so the left-right difference is a true imbalance (D401 does not apply); imbalance entered as a derived per-sample range, with the printed 0.6 dB worst case in notes instead of a separate row (no `worst` statistic).
- (d) `split_ratio_pct` per port added as derived dB-to-% conversions of the printed per-port ratios.
- (e) Fab empty despite a first-person fabrication statement with all authors at one institution: the org is missing from the registry (report above); wavelength 635 nm taken from the characterization setup (p.3 Sec. IV), not inferred.
- (f) Arm width 800 um entered from the RSoft design model (the text gives no other arm width for the printed part), with the 1 mm input-guide diameter in notes.

Registry gaps:

- Branch / junction angle for `splitter.y_branch` (here 9.5 deg between arms, p.2 Sec. II; moralesalvarado2026 has 9.4 deg in notes): proposed `branch_angle_deg` (geometry, unit deg, classes [splitter]): "full angle between the two output arms at the Y-junction tip".
- Waveguide core / cladding refractive index (1.515 / 1.491 at 635 nm here, cited): proposed `core_index` / `cladding_index` (unit 1, classes "*"), only when the source measures them.
