# lit_175 batch report

Distilled 2026-11-16 under the pic-component-distill skill (Contracts v4-v7, DevLog-007 rulings through D615).
Papers: lit:li2013b, lit:cherchi2014, lit:gondarenko2009, lit:zhou2024a. Page-1 titles of all four cached texts
match their source rows; no correction / erratum; no garbled text layer flagged.

Validation: `uv run --offline python scripts/merge_component_staging.py data/_staging/components/lit_175 --dry-run`
-> +20 components, +169 metrics, 0 errors, no warnings on these rows (re-run at the end of the batch).

| paper | components | metric rows |
|---|---|---|
| gondarenko2009 | 1 | 12 |
| li2013b | 6 | 46 |
| cherchi2014 | 12 (11 fabricated, 1 design) | 92 |
| zhou2024a | 1 | 19 |
| total | 20 | 169 |

## gondarenko2009 (Si3N4 high-confinement ring, Cornell)

- Row: `cmp_lit_gondarenko2009_sin_ring_r20` (resonator.ring, sin): defect-free ring of the R ~20 um series, 644 x 900 nm,
  4 um SiO2 above and below.
- Metrics: loaded Q 244,000 (measured); intrinsic Q 3e6 and 0.12 dB/cm (author_estimate, D403: the printed value
  reproduces only on the over-coupled branch, 2 x 244000 / (1 - sqrt(0.7)) = 2.99e6; the regime is not shown);
  extinction 1.55 dB derived from the printed 70 % on-resonance transmission; scattering < 0.065 dB/cm and absorption
  < 0.055 dB/cm as `prop_loss_db_per_cm` with the loss component in the condition (author_estimate, "We estimate";
  wang2023 / D575 absorption-only precedent); 6 geometry rows (design_target).
- Wavelength: no value is tied to a wavelength; C band from the abstract, `wavelength_inferred` true.
- Not entered: Fig. 1 inset ring (1.5e6 "coupled Q", 5.4e6 intrinsic Q, 0.065 dB/cm; p.2 Fig. 1 caption): the ring
  is not identified within the series and 5.4e6 conflicts with "intrinsic Q's up to 3,000,000 ... (Fig. 1)" on p.2
  (D159 / D417). ">20 dB" extinction of TE / TM resonances (p.3): family statement contradicted by the 70 %
  transmission ring (D254). Per-scatterer 0.15 +/- 0.05 dB/cm (p.4, defect-loaded siblings). Thermal coefficient
  C = 0.01 pm/uW (p.5). Nonlinear loss 2 % of total (p.4). n_eff ~1.75 (p.2).
- Fab: `org_cornell_university` ("We fabricate our devices", p.2; all authors Cornell). Facility: none named (JEOL /
  Oxford tools only; CMDITR / NSF center and DARPA in the acknowledgment are program support, D80c).

## li2013b (SiN microrings on SiO2 and vertically integrated on SOI, Georgia Tech)

- Rows (resonator.ring): SiN-on-SiO2 radius series R 20 / 40 / 60 / 120 / 240 um (8 um wide, 400 nm LPCVD SiN,
  platform sin) and `cmp_lit_li2013b_sin_on_soi_pulley_ring_r60` (platform si_sin_multilayer).
- R60 on SiO2: Q_i ~1.5e5 before / ~6e6 after anneal at 1530 nm TE and the printed 235 / 6 dB/m (as 2.35 / 0.06 dB/cm,
  author_estimate, D76 / D256a), Fig. 2(b) notch depths ~1.5 / ~11 dB (figure reads), printed mean 4.5e6 and the
  Fig. 3 spread 4-6e6, geometry incl. 1.2 um access waveguide and 700 nm gap.
- R240 on SiO2: Fig. 4 labelled Q_i ~18 / 17 / 20 M at 1567.41 / 1567.83 / 1568.23 nm (radial order as `mode`),
  ~2 dB/m, second device 16.7 M (continuous scan) and 16 M (wavelength-locked, FP-calibrated) at 1568.6 nm,
  approximate FSR ~800 pm, Fig. 3 spread 14-20 M.
- R20 / R40 / R120: only the Fig. 3 spread (1.3-2.7 / 2.8-4.5 / 7.0-10.0 M, read off the raster figure, +/-0.2 M);
  rows added because each radius is a sibling design (rule 9).
- SOI ring: Q_i ~2 M at ~1542.13 nm (inset axis, `wavelength_inferred`), notch ~18 dB (figure read 17-20 dB),
  Si bus 450 nm, vertical oxide gap ~700 nm, pulley length ~10 um, 400 nm SiN, 3 um BOX.
- Not entered: radiation-limited Q > 1e9 (simulation of the film, p.3 / p.5); scattering-Q ratio 5.54 (simulated);
  mode splitting "on the order of 0.3 pm" (p.12); Fig. 9 normalized FSRs (no labelled values); Fig. 6(c) coupling
  coefficients (design simulation); Si waveguide thickness 110 nm and offset delta r ~ -2000 nm (no resonator
  parameter, in notes); SOI vs SiO2 Q ratio "about half" (p.10).
- Fab: `org_georgia_institute_of_technology` on the SOI row only (borderline): p.3 "we integrate high-Q SiN
  microresonators into the SOI platform by depositing SiN on top of SOI wafers", p.6 "we have adopted a vertical
  integration approach by depositing SiN films"; all authors Georgia Tech (west2019 / D590 "we realize"
  precedent). SiN-on-SiO2 rows empty (passive "are fabricated", p.4). Facility: none (staff thanks for EBL help, D72).

## cherchi2014 (double-MMI couplers with unconstrained splitting ratio, VTT)

- Rows: 10 fabricated `splitter.other` rows, one per phase-shifter length L = 28-46 um (2 um steps, rule 9), one
  `row_kind: design` row for the simulated 70/30 L = 35.5 um design (Fig. 1(c),(d)), one `splitter.mmi` row for the
  2x2 50/50 MMI building block (5 x 112 um; only simulated 1-dB bandwidth ~200 nm, fabricated per D80e).
- Per-device values from the vector data of Fig. 5 (p.6), `extracted_from_figure`: total-output excess loss for input
  port 1 and port 2 (scope per_component, method reference_structure, normalized to a single-mode rib waveguide;
  reads reproduce the legend averages -0.35 / -0.41 dB and the printed 0.2-0.6 dB span) and bar-port fractions
  T11 / T22 (1550 nm, TE). The paper's +/-0.5 dB loss uncertainty is in the notes.
- Simulated (p.7): L = 32 um 1-dB bandwidth ~124 nm and in-band imbalance 2.5-4.3 dB; L = 46 um ~135 nm and
  11.2-16.0 dB.
- Not entered as rows (family-level, D552 / D592): "average losses about 0.4 +/- 0.5 dB", "0.2 dB and 0.6 dB",
  "splitting ratios ranging from 56/44 to 96/4" (abstract / p.6; the endpoint ratios do not match either port's
  Fig. 5(b) point exactly: L = 28 um reads 57.5 / 53.1 %). Measured spectral responses of Fig. 7 / 8 bottom rows
  (in-band imbalance variation "+/-1 dB" to "+/-2 dB", p.9: approximate, not read). Polarization shift > 80 nm and
  the 14 um MMI alternative (p.3). Setup ripple 0.3 dB / 12 nm FSR (p.8, setup artefact).
- Fab: empty. p.4 "We have fabricated the designed structures ... based on the well assessed VTT silicon waveguide
  technology", all authors VTT; VTT is not in the registry (still open since D434 / D444). `process_name`
  "VTT silicon waveguide technology, 4 um SOI (double-masking multi-step process)" as printed. SOITEC (SOI wafer
  supplier) in notes.

## zhou2024a (tunable Fabry-Perot filter, multimode rib cavity + Sagnac loop mirrors, CUMEC)

- Row: `cmp_lit_zhou2024a_fp_filter_mmwg_slm`, `resonator.photonic_crystal` (Fabry-Perot cavity; her2022 / wu2018
  precedent; not a WDM channel filter, D400), platform soi.
- Metrics at 1552.19 nm: 3-dB bandwidth 2.7 pm as `linewidth_pm` (printed unit; OVA resolution 1.6 pm noted),
  Q_L 0.6e6 (derived, "corresponding to"), ER 29.0 dB, FSR 0.28 nm, 0.27 nm tuning with 0-26 mW, 10.3 pm/mW
  (derived), bandwidth tuning 2.0-25.1 pm with 38.6-242.1 mW total heater power, Q 0.06-0.8e6 (derived), ER
  18.6-29.0 dB; simulated 1.7 pm and 1.7-22.6 pm (assumed 750 um cavity, 0.17 dB/cm, R 0.809-0.998); geometry
  (2 um multimode rib, 220 nm core, 70 nm slab, 2 um BOX, 1.06 mm length, footprint derived).
- Not entered: microwave photonic filter results (system level); simulated single-mode-cavity comparison;
  Table I values of other works (rule 3); SLM DC coupling length 35 um / gap 0.3 um and the 50 um taper (role-specific
  geometry without a resonator parameter, in notes); no insertion loss printed (normalized spectra).
- Fab: `org_chongqing_united_microelectronics_center`, `process_name` "CSiP180Al" (p.3 "completed using the
  CSiP180Al process at CUMEC, China").

## Judgment calls

1. D403 applied per resonance: intrinsic Qs whose notch dips to near zero (li2013b R240 1567.41 nm, SOI ring with
   an ~18 dB dip and a stated critical-coupling design) entered as `measured` (D463 analogue: the regime choice does
   not change Q_i); all other printed Q_i (shallow dips, doublets, unprinted lineshape) `author_estimate`.
2. Figure-read intrinsic Qs (li2013b Fig. 3) keep the underlying basis `author_estimate` (D454 logic for a
   derived-quantity plot), with the figure read and its uncertainty in notes, rather than `extracted_from_figure`.
3. li2013b SOI ring platform `si_sin_multilayer` (SiN ring, Si bus, vertical coupling) rather than `sin`.
4. li2013b fab: first-person "we integrate ... by depositing SiN" read as a fabrication statement for the SOI row
   only; the SiN-on-SiO2 rows stay empty (passive voice).
5. cherchi2014 per-device rows with figure reads instead of one family row (D552 / D592); the family ranges and
   printed averages live in notes. Values read from PDF vector coordinates (axis labels as calibration).
6. zhou2024a simulated bandwidths kept on the fabricated row (D80e) although the fabricated cavity length is not
   printed (noted on the rows).

## Missing fab / facility orgs

- VTT Technical Research Centre of Finland (printed "VTT Technical Research Centre of Finland, Espoo"; fab;
  lit:cherchi2014 p.4 Sec. 3 "We have fabricated ... VTT silicon waveguide technology"): would fill fab on the 11
  fabricated cherchi2014 rows (same org already requested for cherchi2013, D434, and wang2023e, D444).

## Registry gaps (no row entered for these)

- `bus_thickness_nm` / `bus_offset_um` on resonator: li2013b SOI pulley ring, Si access waveguide 110 nm thick placed
  at delta r ~ -2000 nm from the ring edge (p.10, Fig. 8 caption). Proposed: thickness of the access waveguide when
  it lies in another layer; lateral offset of the access waveguide inner edge from the ring radius (sign as printed).
- Mirror-coupler geometry on resonator.photonic_crystal (Fabry-Perot with loop mirrors): zhou2024a SLM directional
  coupler coupling length 35 um and gap 0.3 um (p.2), access taper 50 um (p.2). Proposed: allow `coupling_length_um`,
  `gap_nm` with the role "mirror coupler" in condition, and `taper_length_um` for resonator.
- `self_heating_shift_pm_per_mw_optical` (resonator): gondarenko2009 C = 0.01 pm/uW of dropped optical power (p.5,
  fitted); proposed definition: resonance shift per unit optical power dropped in the cavity (fit range in condition).
