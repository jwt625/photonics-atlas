# lit_83 batch report (2026-11-04)

Classes: wdm, switch_fabric. verified_on 2026-11-04. All five cached texts are the source-row papers (page-1 titles checked; melati2022 prints a slightly different preprint title). No wrong document or correction-only file.

| Paper | Components | Metric rows |
|---|---|---|
| melati2022 | 7 | 114 |
| rizzo2020 | 4 | 22 |
| song2021b | 6 | 37 |
| huang2019b | 7 | 36 |
| konoike2022 | 5 | 31 |
| Total | 29 | 240 |

## melati2022

Rows: basic echelle, athermal, super-thermal and tunable MZI-echelle (`wdm.eg`), TiW heater (`phase_shifter.thermo_optic`, D396), 9 mm reference waveguide, MZI test structure (FSR 50 nm).

Not entered:
- Theoretical DC2 loss 0.4 dB and 250 GHz on the MZI rows (p.4, attributed to the authors' ref. [13]; D259). The 250 GHz on the basic row stays as a design value (p.3).
- Insertion loss variation vs temperature (p.11, p.13): no parameter (`il_nonuniformity_db` is across channels). Kept in component notes.
- Measured 3-dB widths and crosstalk: the paper prints none, and the overlapping multi-temperature traces in Fig. 7 were not read for them.
- Edge-coupler loss: not separately printed. 10 dB minus 2 dB minus 2.7 dB was not computed (the terms are of unstated origin).
- DC2 separation dc = 950 nm, Rowland radius 250 um, mounting angle 45 deg: no matching parameter, in notes.

Judgment calls:
- Family design values (spacing, order, facets, stack) are entered on all four echelle rows (D254).
- Simulated center wavelengths are on the three rows of Fig. 5 only.
- Conflict: the MZI arm width / length pairing differs between p.4, p.6 and p.8-9. Widths and lengths are entered unpaired, conflict in notes.
- Athermal < 10 pm/K is `measured` as printed; condition cites channels 2-3 (p.11), the outer channels shift up to 500 pm.
- Fig. 7 peak fiber-to-fiber powers entered as `extracted_from_figure` IL, using the stated 1 mW source.
- Fab empty (no named org).

## rizzo2020

Rows: RMZI interleaver (`wdm.interleaver`), TiN phase shifter, phase-control coupler test structures, 2 x 2 PDK MMI.

Conflict for the audit: the printed 400 GHz FSR (kept, `author_estimate`) vs Fig. 4(b) / 5(b), which read about 3.45 nm (about 428 GHz at 1557 nm). The figure value is a separate `fsr_nm` row. The 78-channel capacity assumes the printed spacing.

Not entered:
- Projected > 20 dB extinction and > 150 nm scaling (p.4, projection).
- kappa = 0.89 (ref. [9]).
- Absolute device IL (not printed, spectra normalized; reference not stated).

Judgment calls:
- Platform empty on all rows: SOI or a buried oxide is never stated (D422 / D423).
- MMI per-port -3.15 to -3.95 dB entered as `excess_loss_db` 0.15-0.95 from the figure (all values below the ideal split, rule 6). D401 kept in mind: if the audit reads it as a split deviation, delete m1 and keep `imbalance_db`.
- Coupler "better than 1 dB of uniformity" entered as `il_nonuniformity_db`; meaning (ports vs wavelength) is not stated, in condition.
- Envelope decay 1.5 dB over 125 nm entered as `il_nonuniformity_db`.
- Fab org_amf on all rows (p.3, p.4). The coupler test structures rest on the acknowledgment only.

## song2021b

Rows: Design A 2 x 2 MZS (`switch_fabric.other`, D158), simulated 2 x 2 MZS (`row_kind` design, phase-shifter width of the simulation not stated, D159), 4 x 4 Benes (`mzi_mesh`), MMI, TES-bend, bent-ADC filter (`mode_converter.other`; the last three simulated values only, stay `fabricated`, D80e).

Not entered:
- Designs B (1 um arms) and C (conventional 0.45 um): their only performance value is the phase imbalance, so no rows (values in Design A notes).
- Phase imbalance and 0.66 mW compensation power: no parameter (see gaps).
- All-bar values (stated only as similar).
- Eye diagrams (synthesized, no number).
- Supplement 1 values: not cached.

Judgment calls:
- Figure conflict: Fig. 5(c) leakage about -27 to -30 dB near 1520 nm with about -2 dB signal, vs printed > 30 dB over 1520-1580 nm. Kept as printed (D417), in notes.
- Signal-path levels read from Figs. 5 and 6 entered as `insertion_loss_db` scope unspecified (normalization not stated).
- 1550 nm on the Fig. 5(b) rows is inferred from "central wavelength" (p.4).
- p_pi_mw 34 taken from the ON-state power.
- Fab empty: foundry not named.

## huang2019b

Rows: 8 x 8 Omega switch and dual-MRR element (`switch_fabric.other`, D407), racetrack MRR (`resonator.ring`, D396 / D400), doped heater (`phase_shifter.thermo_optic`), routing waveguide, grating coupler, 1 % tap.

Not entered:
- Table I other-work rows and Fig. 2 (based on ref. [11]).
- Power penalty < 2 dB and < 1 dB variation at 32 Gbps (no parameter).
- 48.85 GHz/mW (no parameter on any class; in resonator notes, the nm/mW form is entered).
- PD responsivity (not printed).

Judgment calls:
- All on-chip path losses are `author_estimate` + `loss_breakdown` (D428): grating coupler 3.6 dB/facet is a Table II term of unstated origin and the paper compensates it at injection. Same for 0.67 / 2 dB per element ("estimated", p.5). Audit may revisit against D167.
- Rise / fall are 0-100 %, in condition; the row definition is 10-90 %.
- Conflicts kept (D417), in notes: fall 0.5 us (text) vs 0.4 us (Fig. 7 label, Table I); all-Bar mean 8.4 dB vs Fig. 11 bars about 8.5-9.1 dB; all-Cross bars reach about 4.1 dB vs printed lower bound 4.4 dB.
- 147 / 96 / 55 GHz entered as `bw_3db_ghz` though that sentence prints no level; 120 GHz likewise.
- Platform empty (SOI never stated; D423).
- Fab org_elenion rests on "process and design flow at Elenion" and "taped out" (p.2, p.7), with Elenion co-authors: borderline D80b / D398, coordinator to confirm. No separate foundry named.

## konoike2022

Rows: 8 x 8 PILOSS switch and (7,7) MZI cell (`switch_fabric.mzi_mesh`, D158), TiN heater, routing waveguide, SSC edge coupler.

Not entered:
- 1.27 mW and 1.4 dB per facet (ref. [12]).
- 32 x 32 < 6 dB projection.
- 50 ohm TiN terminator (electrical, separate sample).
- 530 ohm / 1 V model values.
- d_pn = 0.55 um (no parameter, in notes).
- Measured leakage levels in Fig. 3(d) (no printed value; plot too dense for a single value).

Judgment calls:
- 3.80 and 3.30 dB are `author_estimate` + `loss_breakdown` (about 3 dB per facet subtracted, origin not stated; D428). The 3 dB row is `author_estimate` (only a subtraction term, D444).
- Crosstalk > 20 dB and > 31 nm are `derived` (integrated own spectra, caption "calculated"); wavelength columns are read from the Fig. 4(c) shading.
- Band c_band inferred from the Fig. 4 axis where no wavelength is printed.
- All switching times in ns converted to us, `derived` (D256). Maximum-of-60 rows have qualifier le.
- Fab org_national_institute_of_advanced_industrial_science_and_technology ("we fabricated", all authors AIST, p.2, p.6).

## Missing organizations

- AIST SCR (printed "AIST SCR", konoike2022 p.6 Acknowledgment): facility left empty on all 5 rows. Not found in `organizations.csv` / `org_aliases.csv`. DevLog-007 line 259 mentions "TIA SCR AIST" in an org round, but no registry row exists; add it, then fill `facility_org_ids`.

All other orgs used are in the registry: org_amf, org_elenion, org_national_institute_of_advanced_industrial_science_and_technology.

## Registry gaps (skipped value, locator, proposed definition)

- `phase_imbalance_pi` (switch_fabric, unit pi): random phase imbalance compensation of an MZI element. song2021b p.6 Fig. 5(d): (0.016 +/- 0.045) pi, (0.0019 +/- 0.077) pi, (0.70 +/- 0.50) pi. This is the headline result of the paper and would allow Design B and C rows.
- `tuning_efficiency_ghz_per_mw` (resonator, phase_shifter, wdm): huang2019b p.3 Sec. III, 48.85 GHz/mW.
- `power_penalty_db` (switch_fabric): huang2019b p.7, < 2 dB at 32 Gbps and 1e-9 BER.
- Temperature-dependent IL variation `il_variation_temperature_db` (wdm): melati2022 p.11 and p.13, < 1 / < 1.5 / up to 3 dB over stated spans.
- `gap_nm` on mode_converter (existing D428 candidate): song2021b p.4, 200 nm.
- `heater_resistance_ohm` on wdm / switch_fabric (existing D440 candidate): the melati2022 value went on the phase-shifter row instead.
- `tuning_power_mw` on switch_fabric: konoike2022 p.3, 11.0 mW trim per MZI (entered on the TiN heater row instead).
