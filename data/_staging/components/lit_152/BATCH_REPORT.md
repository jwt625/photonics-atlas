# lit_152 batch report

Papers: lit:catalalahoz2026, lit:vagionas2021, lit:zou2020, lit:tu2024, lit:ning2022 (benchmark-citation round,
D577). Fresh start after the infrastructure outage (staging directory created new). Page-1 titles match the source
rows; none is a correction / erratum; no `garbled_text_layer`. catalalahoz2026 is the arXiv text of the Nature
Photonics paper (24 pages, Supplementary Information from p.16). Table and figure values were checked on the page
renders (zou2020 Tables I-II and Figs. 4 / 8, tu2024 Table I, ning2022 Table II and Fig. 8).

Validation: `uv run --offline python scripts/merge_component_staging.py data/_staging/components/lit_152 --dry-run`
-> +34 components, +194 metrics, 0 errors (the one warning concerns merged ni2025b rows, not this batch).

Totals: 34 components, 194 metric rows.

| paper | components | metric rows |
|---|---|---|
| catalalahoz2026 | 11 | 27 |
| vagionas2021 | 7 | 21 |
| zou2020 | 4 | 67 |
| tu2024 | 2 | 21 |
| ning2022 | 10 | 58 |

## lit:catalalahoz2026 (Si-BTO non-volatile FPPGA)

| component | class | rows | content |
|---|---|---|---|
| bto_nv_phase_shifter | phase_shifter.ferroelectric_nonvolatile (test) | 9 | Vpi 5 V, 560 nW/pi, rise / fall ~82 ns, non-volatile pi shift, ER 12 dB, 16 levels, 1.2 min hold, 350 um |
| nv_puc | switch_fabric.other (test) | 2 | IL 1.48 dB per PUC, 950 um |
| hex_mesh | switch_fabric.mzi_mesh | 8 | 34 ports, 2 x 10 mm2, ~25 dB desired / undesired ratio (4x4 transformer), 42 dB MZI rejection at 25 C, Si waveguide SEM 512.6 x 242.5 nm, top oxide 365.7 nm, BOX 3 um |
| grating_coupler | fiber_chip_coupler.grating | 1 | peak window 1565 nm (+/- 15 nm) |
| umzi_2lpuc / 4lpuc / 8lpuc | wdm.other | 1 each | FSR 43.65 GHz / 19.02 GHz / 78.1 pm |
| ring_6lpuc / 10lpuc / 14lpuc | resonator.ring | 1 each | FSR 13.27 GHz / 7.95 GHz / 44.5 pm |
| ramzi_2ring | wdm.other | 1 | FSR 13.14 GHz |

Not entered: switching energy 44.8 fJ and 60 us state-setting pulse train (no parameter); 600 random transitions
(reproducibility test, not stated as endurance); router normalized output powers 0.892-0.954 and 4x4 normalized
powers > 0.98 (normalized, no loss parameter); 1x8 splitter (no value); thermal Vpi-point shifts 0.45 / 0.24 V (no
parameter); Table 1 rows of other technologies and the intro values (cited, rule 3); ref. 37 earlier BTO values
(rule 3); < 0.5 dB future loss (projection); Si-to-Si-BTO taper loss (no number printed).

Judgment calls: Vpi and switching times entered on the phase-shifter row (lit source, no EO-atlas host; shu2026 /
poulton2019 precedent, D582 / D589); flag as an EO-atlas candidate. Platform `bto_on_si` on the PUC, mesh and
configured-filter rows (Si passives with Si-BTO actuator sections), `soi` on the grating couplers. 560 nW/pi
`derived` (nW -> mW), origin of the static power (leakage) not stated. C band inferred for the PUC tests (GC window
1565 +/- 15 nm, mesh spectra around 1560 nm). The 42 dB Supp. Note 4 rejection was measured on "a representative MZI
within the mesh", so it sits on the mesh row, not on the NV-PUC test-structure row. The Supp. Note 5 SEM geometry is
on the mesh row (which waveguide was sectioned is not stated). Configured filters as separate rows (zhang2026d,
D574).

Fab: `org_cea_leti` (base wafers "fabricated at CEA-Leti", p.11; contributions p.12) + `org_lumiphase` (BTO layer
transfer, p.11-12) on all BTO-containing rows; grating couplers `org_cea_leti` only (per-part fab). No facility.
No missing orgs.

## lit:vagionas2021 (lossless 1x4 Si3N4 ROADM + Al2O3:Er EDWA)

| component | class | rows | content |
|---|---|---|---|
| roadm_1x4 | wdm.cascaded_mzi | 8 | 3-dB width 0.66 nm, crosstalk > 18 dB, FtF 2.55 dB (mean Drop 2-4), 0.6 dB on-chip propagation (estimate), 100 GHz, 4 ch, DL 872.1 / 436 um |
| roadm_fiber_interface | fiber_chip_coupler.edge | 1 | 0.975 dB per facet (author_estimate, loss breakdown) |
| edwa_5p9cm | amplifier.rare_earth | 6 | net gain 3.6 dB, 0.6 dB/cm (derived), EDWA PIC fiber-to-fiber 27.4 dB, 5.9 cm, 1.4 um x 800 nm |
| edwa_waveguide | waveguide_platform.straight | 1 | 1.4 dB/cm absorption + propagation (unpumped) |
| si3n4_al2o3_adiabatic_coupler | waveguide_platform.transition | 1 | 0.5 dB per transition (author_estimate) |
| edwa_fiber_interface | fiber_chip_coupler.edge | 2 | 10 dB (C band) / 12 dB (980 nm) per interface, estimated |
| pump_signal_mmi | wdm.other | 2 | 1.7 dB signal port / 8.3 dB pump port for signal light (calculated) |

Not entered: signal enhancement 15 / 13.16 / 9.27 / 5.7 dB and 11.8 dB (no registry parameter; in notes); ASE
baseline differences; up to 30 dB enhancement / 18 dB gain (ref. 35, rule 3); TriPleX < 0.1 dB/cm (ref. 39) and
Si3N4 0.12 dB/cm (ref. 36), cited; two-stage-bus suppression ratios 18 / 15 / 12 / 22 dB (link-level with data
signals, D542; in notes); BER penalties, eye ER; aggregate path estimates 18.8 / 18.3 / 12.2 / 11.7 dB (sums of the
facet, MMI and coupler estimates; in notes); required -20.975 dBm per channel (hypothetical single-chip case).

Judgment calls: net gain 3.6 dB `derived` (the "As ... 1.4 dB/cm were measured" sentence ties it to enhancement minus
measured loss, D166); the alternative route through the estimated coupling losses (-27.4 + 18.8 + 12.2) would make it
`author_estimate` (D429 / D583) - auditor may prefer that. 27.4 dB fiber-to-fiber `measured` (printed net loss of
the pumped PIC). ROADM 0.6 dB and 0.975 dB/facet `author_estimate` (budget terms; the 0.6 dB origin is not stated).
ROADM DL1 / DL2 colour assignment conflicts between the p.3 FSR sentence and the Fig. 2(b) caption (D417 note).
EDWA fiber interfaces classed `fiber_chip_coupler.edge` ("facet", butt coupling); MMI as `wdm.other` (980 / 1550
pump-signal multiplexer). Transition platform `other` (garciablanco2025 precedent).

Fab: empty on all rows. ROADM: "relies on a Si3N4/SiO2 TriPleX platform", no fabrication sentence naming an org
(process_name "TriPleX" kept, Contract v7 named process without a named foundry); LioniX International co-authors
are affiliation only. EDWA: "fabricated following the process described in [35]" (passive, no org; MESA+ / Twente
co-authors affiliation only). No facility. No missing orgs.

## lit:zou2020 (edge-input SOI AWGs and bidirectional AWG spectrometers)

| component | class | rows | content |
|---|---|---|---|
| awg1_confocal | wdm.awg | 16 | FSR 52.34 nm measured / 52.56 nm design, 200 GHz, 32x32, Table I geometry |
| awg2_rowland | wdm.awg | 17 | same + on-chip loss ~5 dB (outer-most input, de-embedded) |
| spectrometer1 | wdm.awg | 17 | on-chip loss 7-8.7 dB, crosstalk 6-10 dB, 1570 nm / 0.4 nm / FSR 37.82 nm design, 64 ch, Table II geometry |
| spectrometer2 | wdm.awg | 17 | on-chip loss 5.6-8 dB, crosstalk 9-12 dB, same design values, FPR 243.6 um |

Not entered: AWG #1 on-chip loss and both AWGs' crosstalk (figure only, no printed value; the AWG #1 peaks range
widely across channels); simulated aberrations (no parameter); side-input angles 0.1412 / 0.1396 rad and n_gs / n_ga
(no parameter / design, in notes); FDE index sensitivities (no parameter); ~3 dB edge-input extra loss (ref. 32);
projected < -18 dB crosstalk on 340 nm SOI (other design).

Judgment calls: platform `soi_strip` (channel waveguides etched through the 220 nm layer, D459). Table I FSR 52.56 nm
vs text 32 x 1.6 = 51.2 nm (D417 note, Table kept). Spectrometer #2 loss printed "8 dB to -5.6 dB" (sign missing),
entered 5.6-8 dB, matches Fig. 8(b). Measured wavelength spans set from the figure axes (`wavelength_inferred`).
Array pitch on the tangent line (2 um) kept in notes so `pitch_um` holds only the output-waveguide pitch.

Fab: empty (passive fabrication text, no org; SOITEC wafer as a supplier note). No facility. No missing orgs.

## lit:tu2024 (100-channel z-cut TFLN AWG)

| component | class | rows | content |
|---|---|---|---|
| awg_100ch | wdm.awg | 20 | IL ~13 dB (de-embedded), adjacent crosstalk ~6 dB, FSR 20 nm, 50 pm spacing, Table I design, widths 2.0 design / 2.1 um SEM, etch 150 / 400 nm, ng 2.279 (sim.), footprint ~0.9 x 1.8 cm |
| lensed_fiber_facet | fiber_chip_coupler.edge | 1 | 8 dB coupling loss (scope unspecified: per facet or both not stated) |

Not entered: Rowland radius 7892.90 um (the FPR length is not stated separately; never guess R vs R/2); transition
taper / interval geometry (no parameter or ambiguous roles; in notes); simulated spectra (Fig. 4, no printed values);
Table II and p.1 literature values (cited).

Judgment calls: IL `measured` with method `reference_structure` (normalized to a straight waveguide with the same
lensed fibers); the printed -2.6 dBm / 8 dB / -23.6 dBm chain is consistent and noted. Facet row platform empty
(straight-waveguide etch not stated, D422). 25 C entered as 298.15 K.

Fab: empty (passive, no org; HUST and Ningbo Ori-Chip authors affiliation only). No facility. No missing orgs.

## lit:ning2022 (O-band 1x8 lattice-filter demultiplexers, AMF MPW)

| component | class | rows | content |
|---|---|---|---|
| demux_flat | wdm.cascaded_mzi | 15 | IL 1.5-2.5 dB (8 ch), crosstalk > 11 dB, 1-dB / 3-dB ~3 / ~3.9 nm, heaters 149 mW, simulated ~1 dB / 12.5 dB, 4.4 nm, footprint, stack |
| demux_gaussian | wdm.cascaded_mzi | 15 | IL <= 1.1 dB, crosstalk > 13 dB, ~1.8 / ~2.9 nm, 62 mW, simulated ~1 dB / ~25 dB, footprint, stack |
| lattice_stage1_ref / 2 / 3 | wdm.interleaver (test) | 3 / 2 / 2 | measured FSR 8.4 / 17 / 35.2 nm vs design 8.8 / 17.6 / 35.2 nm |
| dc_k050 / k020 / k004 / k029 / k008 | splitter.directional_coupler | 5 / 4 / 4 / 4 / 4 | design kappa (simulated), FDTD coupling lengths 70.1 / 40 / 15.2 / 49.31 / 24 um, 200 nm gap, 500 nm strips; kappa 0.5 measured 34-51 % read off Fig. 8 |

Not entered: heater resistance ~466 ohm (`heater_resistance_ohm` not allowed on wdm; registry gap, D440 list);
~1 dB passband ripple (no parameter); recalculated Fig. 9 values (calculations on measured DC ratios; in notes);
improved-design estimates; Fig. 8 curves of the four low-kappa DCs (overlapping, D156); Table III other works.

Judgment calls: design kappa values `simulated` (digital filter synthesis, D82a); stand-alone lattice filters
`wdm.interleaver` (2x2 band de-interleavers); demux crosstalk printed as "worst channel -11 dB" / Table II "<-11"
-> 11 `gt`; simulated device IL scoped `device_total`.

Fab: `org_amf` on all rows ("by utilizing the silicon photonics multi-project wafer (MPW) service of Advanced Micro
Foundry (AMF)", p.3). process_name empty (no named process / PDK printed). No facility. No missing orgs.

## Missing fab / facility orgs

None. All named fabricators are in the registry (`org_cea_leti`, `org_lumiphase`, `org_amf`).

## Registry gaps (skipped value + locator + proposed definition)

- `signal_enhancement_db` (amplifier): vagionas2021 15 / 13.16 / 9.27 / 5.7 dB and 11.8 dB (p.5, Fig. 3(c)-(d)):
  pumped-minus-unpumped signal transmission at the stated input power.
- `switching_energy_fj` (phase_shifter): catalalahoz2026 44.8 fJ (p.9 Table 1); already listed in earlier audits.
- `write_time_us` / `write_pulse_us` (phase_shifter, D438 candidate): catalalahoz2026 60 us pulse train (p.6).
- `heater_resistance_ohm` on wdm (D440 candidate): ning2022 ~466 ohm (p.3).
- `passband_ripple_db` (wdm): ning2022 ~1 dB flat-passband ripple (p.3).
- `delay_ps` (switch_fabric unit cell): catalalahoz2026 basic delay unit 12.73 ps (p.5).
