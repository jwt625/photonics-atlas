# Batch lit_213 report

Papers: lit:agazzi2010, lit:thomson2010, lit:umeki2011 (page-1 titles match the source rows; no garbled text layer).
Totals: 10 components (2 design), 62 metric rows. Validation: `merge_component_staging.py --dry-run` 0 errors
(the one WARN is a pre-existing merged row, cmp_lit_ni2025b_pimmwc). verified_on 2026-11-20.

## lit:agazzi2010 (5 components, 33 metrics)

| component | class | metrics |
|---|---|---|
| cmp_lit_agazzi2010_al2o3er_si_al2o3er_amp_13p5mm | amplifier.rare_earth | 11 (signal enhancement 7.2 dB at 1533 nm, Fig. 5 reads at 1525 / 1565 nm and 100 uW, model net gain 1.96 dB/cm, geometry) |
| cmp_lit_agazzi2010_si_al2o3er_inverse_taper | waveguide_platform.transition | 10 (measured ~2.5 dB per coupler, simulated 0.5 dB, taper geometry) |
| cmp_lit_agazzi2010_fiber_al2o3er_butt_facet | fiber_chip_coupler.edge | 5 (19 % measured at 1480 nm, 20 % calculated, facet cross-section) |
| cmp_lit_agazzi2010_al2o3er_taper_coupler_design | fiber_chip_coupler.edge (design) | 5 (76.9 % / 1.15 dB calculated, 800 x 325 nm2 tip) |
| cmp_lit_agazzi2010_al2o3er_spiral_amp_25cm_design | amplifier.rare_earth (design) | 2 (42 dB predicted over 25 cm) |

Not entered:
- Calculated signal enhancement 7.62 +/- 0.48 dB (p.8): uses the 6.06 dB/cm total loss extrapolated from ref. [25] (rule 3).
- Al2O3 loss 0.1 / 0.2 dB/cm, net gain 2.0 dB/cm, 80 nm bandwidth, bend radii (p.3-4): refs. [11], [23]-[25]. Si wire loss 2.4 dB/cm (p.4): ref. [2]. SOI GC 69.5 / 31.6 / 8.9 % (p.8): ref. [33]. Spiral footprint 6 x 6 mm2: ref. [25].
- Calculated loss into residual Si structures 70 / 105 / 190 dB/cm and 0.2 dB additional taper loss for 0.5 um misalignment (p.7): parasitic / excess terms with no matching parameter (component notes).
- 1 % coupling-efficiency variation 1480-1565 nm of the taper design (p.8): % variation, no parameter (notes). SiO2 > 4.6 um for < 0.01 dB/cm substrate leakage (p.8): design statement (notes).
- Straight Al2O3:Er3+ reference channels (p.5): no value of their own, no row. Er concentration, pump-signal overlap 97 %, confinement > 80 % (p.4): no parameter.

## lit:thomson2010 (3 components, 20 metrics)

| component | class | metrics |
|---|---|---|
| cmp_lit_thomson2010_er_bg_uli_amp_87mm | amplifier.rare_earth | 12 (16.0 dB fiber-to-fiber, 20.0 dB / 2.3 dB/cm internal, > 9 dB over 1530-1565 nm, >= 75 nm net-gain span, 63 dB relative gain, Psat ~14 dBm at 1530 / 1533 nm, NF 8 / 5.6 dB, 0 dB crossing ~350 mW from Fig. 4, length) |
| cmp_lit_thomson2010_er_bg_uli_waveguide | waveguide_platform.straight | 6 (IL 4.0 dB at 1618 nm, ~0.2 dB/cm, PDL 0.27 dB, MFD 12.2 / 10.4 um, length) |
| cmp_lit_thomson2010_fiber_butt_facet | fiber_chip_coupler.edge | 2 (0.9 dB measured per facet 1560-1600 nm, 0.8 dB calculated mode mismatch) |

Not entered:
- PDL about 0.6 dB at 1533 nm under maximum pumping (p.5): `pdl_db` is not allowed for `amplifier` (registry gap below); in amplifier notes.
- Zero-pump absorption ~42.0 dB at 1533 nm and population inversion ~75 % (p.6): no parameter (notes). Effective NA ~0.09 (p.4): no parameter.
- Fresnel ~0.1 dB per facet (p.4): estimate of unstated origin, notes only. Abstract breakdown 1.8 / 0.2 / 2.0 dB: the 1.8 dB is 2 x 0.9 dB (already on the facet row).
- Comparison values of refs. [6], [11] (p.2, p.7).

## lit:umeki2011 (2 components, 9 metrics)

| component | class | metrics |
|---|---|---|
| cmp_lit_umeki2011_ppln_dpa_module | amplifier.parametric | 7 (in-phase +11 dB, quadrature -10 dB, extinction 21 dB, 22 dBm max output, > 10 dB for 10 Gb/s NRZ, module IL 5.0 dB, length) |
| cmp_lit_umeki2011_ppln_shg_module | frequency_converter.shg | 2 (23.4 % power conversion derived from 31.5 dBm in / 330 mW SH out, length) |

Not entered:
- SH conversion efficiency over 2000 %/W (p.3, p.4): cited to the authors' ref. [10] (rule 3, D259); Fig. 3 calculated curve built on it.
- Pump leakage 50 dB below the signal / 87 dB below the 31.5 dBm pump input (p.4): property of the two-module configuration, notes only.
- Fig. 3 / Fig. 4 curves beyond the printed values; eye-diagram results (qualitative).

## Missing fab / facility orgs

- ePIXfab (MPW access provider, D398): "chips ... produced in a multi-user run of the epixfab CMOS line" (lit:agazzi2010 p.4 Sec. 2.2; p.5 Sec. 3 "200-mm CMOS pilot line"). Fab role on cmp_lit_agazzi2010_si_al2o3er_inverse_taper (Si taper part). Not in organizations.csv / org_aliases.csv (same gap as cabezon2012, lindenmann2012, acoleyen2012).

## Judgment calls for the auditor

1. agazzi2010 fab: only ePIXfab is named (missing from registry, so fab empty everywhere). The Al2O3:Er3+ deposition / etching org is not named; "the tolerance of our lithographic equipment" (p.5) is first-person but the authors are at two orgs (University of Twente MESA+, Ghent University), so no own-org fab was set (D80b, D395). Recommend: keep empty; after the org round, ePIXfab on the transition row only (the amplifier row's gain sections are not from the epixfab run).
2. agazzi2010 transition 2.5 dB `measured` with method `reference_structure` (D167: no subtracted numbers printed). The comparison structures differ in Er-doped length (9.5 vs 13.5 mm presumably) and include a 4 mm Si section; how that was handled is not stated (noted). Alternative: `author_estimate`.
3. agazzi2010 signal enhancement stored as `gain_db` `measured` with ref_plane empty and the condition saying it includes Er absorption and is not net gain (ahmadi2022 / chang2026 on-off precedent). The 1.96 dB/cm rate-equation model value entered as `simulated` `gain_db_per_cm` (the model is the authors' manuscript in preparation, ref. [32]; the computation is this paper's).
4. agazzi2010 design rows: the optimized taper coupler (76.9 %) and the 25 cm spiral (42 dB) are design-only rows (row_kind design). The spiral gain wavelength is not stated: `c_band` inferred.
5. thomson2010 internal gain 20.0 dB and 2.3 dB/cm `author_estimate` (assumption that the 1618 nm IL represents the non-Er IL at 1533 nm; D429). Propagation loss 0.2 dB/cm `author_estimate` (estimated Fresnel term).
6. thomson2010 NF: text says measured over 1525-1580 nm but places the ~8 dB maximum at 1505 nm; Fig. 5(b) starts near 1505 nm. Entered at 1505 nm as printed with a D417 conflict note. NF reference plane not stated (`unspecified`).
7. thomson2010 `pump_threshold_mw` 350 read off Fig. 4 (0 dB fiber-to-fiber net-gain crossing at 1533 nm; nykolak1993 gain-threshold precedent, D665). `gain_bandwidth_nm` 75 `ge` derived from "net gain across the entire 1505-1580 nm measurement range". Relative gain 63 dB as `gain_db` (on/off) `measured`. Psat 14 dBm entered at both 1530 and 1533 nm (one sentence, two wavelengths; 3-dB compression definition in condition).
8. thomson2010 fab empty (passive inscription sentences, all authors at Heriot-Watt; D80b). Asahi Glass Company supplied the glass (note); Fianium Ltd supplied the inscription laser (setup, note).
9. umeki2011 fab org_ntt: "We fabricated 5-cm-long PPLN ridge waveguides using the direct bonding method" (p.2) and all authors in NTT Corporation laboratories (p.1; two now elsewhere, stated as current affiliations). Platform `other` (kazama2021 precedent; substrate not stated, not inferred).
10. umeki2011 module 1 (SHG) and module 2 (DPA) are two physical devices of one stated design; rows split by class (D396). The 5.0 dB signal IL is stated for the module type and entered on the DPA row only (wavelength 1537.6 nm inferred). The 23.4 % SHG power conversion is my ratio of two printed powers (`derived`), with output reference plane not stated. Quadrature-phase deamplification stored as `gain_db` -10 (foster2006 negative-gain precedent).

## Registry gaps

- `pdl_db` on `amplifier` (polarization-dependent gain / loss under pumping): thomson2010 ~0.6 dB at 1533 nm under maximum pumping (p.5). Proposed: widen `pdl_db` classes to amplifier, definition "polarization-dependent loss / gain of the pumped amplifier, pump state in condition".
- Er absorption at the gain peak (zero pump): thomson2010 ~42.0 dB at 1533 nm over 87 mm (p.6). Proposed `absorption_db` (amplifier; total small-signal absorption at the stated wavelength, zero pump, length in condition). Low priority.
