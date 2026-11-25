# lit_277 batch report

Papers: lit:zheng2018, lit:colbourne2018, lit:takenobu2008. Distilled 2026-11-25 (verified_on). Totals: 7 components,
37 metric rows. `merge_component_staging.py data/_staging/components/lit_277 --dry-run`: +7 components, +37 metrics,
0 errors (the two warnings it prints are on merged rows of other batches).

Title check: page 1 of each text.md / render is the source row's paper; no correction or erratum. takenobu2008: the text
layer of p.1 starts with the Table 2 and Fig. 1 contents before the title; the p.1-p.3 renders show the normal page
order (title / abstract / Sec. 1-2.1 / Tables 1-2 on p.1, Sec. 2.2-3 and Figs. 2-5 on p.2, Figs. 6-8 / Sec. 4 /
references on p.3), so the text.md page markers are correct and locators use them.

## lit:zheng2018 (Optical Materials Express 2018, GST-on-Si microrings) - 4 components / 18 metrics

| component | class | metrics |
|---|---|---|
| cmp_lit_zheng2018_gst_hybrid_wg | waveguide_platform.straight | 8: attenuation aGST 2700 dB/cm, cGST 76000 dB/cm, reset state 6200 dB/cm (all derived from printed dB/um), GST 20 nm, width 500 nm, Si 220 nm, etch 190 nm, BOX 3 um |
| cmp_lit_zheng2018_gst_mode_mismatch | waveguide_platform.transition | 1: mode-mismatch loss < 0.5 dB (both states) |
| cmp_lit_zheng2018_ring_r20_series | resonator.ring | 7: Q ~11,000 near 1550 nm, R 20 um, gap 100 nm, width, core, etch, BOX |
| cmp_lit_zheng2018_ring_gst2um_switch | resonator.ring | 2: extinction 33 dB at 1551.5 nm, R 20 um |

Not entered:
- Resonance shift per GST length 0.444 / 1.14 nm/um and the attenuation modulation ~7.3 dB/um (p.7-8): per-length phase-shifter quantities (D250, D586 zheng2020).
- Simulated 7.7 / 0.08 dB/um and 0.98 / 2.76 nm/um (p.7-8), simulated neff values (p.4 Fig. 1): comparison simulations of the platform, not device rows.
- Estimated refractive indices of nano-patterned GST and ellipsometry indices (p.8), ITO extinction coefficient < 0.002 (p.5): material properties.
- Wavelength dependence of attenuation and shift over 1525-1565 nm (Fig. 4(d)-(e)): plot only, values not printed.
- ~7 dB/um after five 25-pulse excitations (p.10, Fig. 6(c)): consistency check against the fitted value, stated with "~" only for the comparison.
- Switching pulse energies ~620 pJ (reset) / ~200 pJ (set) per pulse, ~9 / ~3 aJ/nm3, fluences ~31 / ~10 mJ/cm2 (p.9): no registry parameter (switching energy, D81 rejected); in component notes.
- Number of intermediate states: not stated (Fig. 6(c) shows 0-5 excitations); n_levels not entered.
- Residual ~0.2 nm shift after deposition (p.8): process artefact.
- Focusing sub-wavelength grating couplers (design of ref. [34]): no performance printed, no row.
- No phase_shifter.phase_change row: the only phase-change performance values are per-length (D250) or the ring-level extinction, which follows the zheng2020 precedent (ring switch as resonator.ring).

Judgment calls:
- GST-loaded hybrid-waveguide attenuation stored as waveguide_platform.straight prop_loss_db_per_cm (blundell2025 Sb2Se3-loaded rib precedent; the paper calls it the attenuation coefficient of the hybrid waveguide). Basis derived: regression slope of ring loss computed from Q before / after deposition with an assumed unchanged intrinsic loss (model extraction, D80a) plus the dB/um -> dB/cm conversion. If the coordinator reads D250 as covering these too, delete the three prop_loss rows and the row falls back to geometry only (then delete the component, D49).
- Mode-mismatch alpha_0 entered as transition_loss_db < 0.5 dB with a note that it covers one GST section (entry + exit together), scope per_component.
- Q ~11,000 (Fig. 4(a) caption) placed on the series row: the ring (GST length, state) is not identified; the value stands for one ring of the 40-ring design.
- Fig. 6 switch ring kept as a separate row (different GST length from the series rings); its gap and width are not restated, radius from the general R = 20 um statement.
- Polarization te from the quasi-TE input statement (p.5); stage 20 C kept in condition text only.

Orgs: fab org_university_washington (first-person "We fabricated" p.4 + acknowledgment that all fabrication processes were performed at the Washington Nanofabrication Facility at the University of Washington, p.11; D448). Missing org: Washington Nanofabrication Facility (WNF), facility role, lit:zheng2018 p.11 Acknowledgments (already reported by earlier batches).

## lit:colbourne2018 (OFC 2018 Th4A.1, contentionless twin 8x24 WSS) - 1 component / 4 metrics

| component | class | metrics |
|---|---|---|
| cmp_lit_colbourne2018_twin_wss_8x24 | switch_fabric.wss (platform other, D424) | 4: IL 3.3-6.8 dB fiber_to_fiber (all port pairs, C band, 50 GHz grid), same-wavelength port isolation > 45 dB (crosstalk_db), 8 Common / 24 Add-Drop ports |

Not entered:
- Channel width typically 38 GHz at -1 dB for a 50 GHz channel (p.3): bw_1db_ghz is not allowed for switch_fabric (registry gap below).
- Earlier-work IL values 20.5 / 10.7 / 9 / 8.4 dB and the 8 dB EDFA-free threshold (p.1-3): cited or system-level.
- Number of measurements "nearly 40,000" left in condition (not exact, no n_samples).

Judgment calls:
- Fab org_lumentum: abstract passive "designed and manufactured in prototype quantities" plus first-person "We constructed a Twin WSS" (p.1 Sec. 2), all five authors at Lumentum. Entered by the own-construction precedent (D80b own-process statement; D971 smit1988; earlier "we have built" row); flagged for the auditor. Remove if "constructed" is read as a design statement.
- IL scope fiber_to_fiber (LCOS WSS precedents iwama2015, xie2017, yang2020): module IL between Common and Add/Drop fibers.
- MEMS mirror array and LCOS panel are internal parts without own metrics: no separate rows.

Orgs: org_lumentum in the registry; no missing org.

## lit:takenobu2008 (OFC 2008, all-polymer 8x8 AWG router) - 2 components / 15 metrics

| component | class | metrics |
|---|---|---|
| cmp_lit_takenobu2008_awg_8x8_pcy | wdm.awg (polymer) | 14: IL 2.5-3.9 dB (center to edge ports, scope unspecified), crosstalk > 25 dB, thermal drift +15 pm/K, channel spacing 200 GHz (design, author_estimate), 8 in / 8 out, order 121, focal length 2035 um (fpr_length_um), min bend radius 10 mm, chip 45 x 14.5 mm, core 7.4 x 6.4 um, claddings ~18 um |
| cmp_lit_takenobu2008_awg_on_si | wdm.awg (polymer) | 1: thermal drift about -58 pm/K (comparison AWG on Si substrate) |

Not entered:
- TE-TM polarization wavelength shift < 0.15 nm (p.2 Sec. 3, Fig. 7; p.3 Sec. 4): no registry parameter (registry gap below; jeong2020 precedent moved such a value out of wavelength_spread_nm).
- Table 2 straight / 1.8 m waveguide IL and propagation losses 0.027 / 0.022 / 0.032 dB/cm at 1310 / 1550 / 1650 nm (p.1 Sec. 2.1): the table and its sentence cite the authors' own ECOC 2007 paper (ref. [5]); D259 / D80i.
- PBVE dn/dT -5e-5 /K (p.3): material property derived from the AWG-on-Si shift.
- Refractive indices 1.3335 / 1.3260 and delta 0.57 % (p.1 Table 1, p.2): material data, kept in core_material.
- Water absorptivity < 0.01 % (p.1): material property.

Judgment calls:
- IL scope unspecified (reference plane and fiber coupling not stated); wavelength range 1546-1558 nm from the Fig. 6 axis, wavelength_inferred.
- Crosstalk entered as crosstalk_db (type not stated) with the printed "well below -25 dB" as > 25 dB.
- Thermal drift: text prints +15 pm/K twice, the Fig. 8 label +14 pm/K; text value kept with a conflict note (D417).
- Core 7.4 um = width, 6.4 um = height from the Fig. 4 label placement (7.4 above the core, 6.4 beside it); um -> nm derived (D157). Cladding / buffer thickness entered from the text ("chosen to be some 18 um", design_target approx), Fig. 4 labels 18.5 / 18.2 um in notes.
- Focal length f = 2.035 mm entered as fpr_length_um (akca2018 / wang2014a "focal length" precedents), derived for the unit conversion.
- AWG on Si substrate as its own row (different substrate = sibling design); no geometry restated for it.

Orgs: fab empty (first-person "designed and fabricated" by authors at Asahi Glass Co., Ltd. and Fraunhofer HHI, no fabricator named; D80b / D154). Asahi named as the polymer material owner (note only). No missing org.

## Registry gaps (proposed, with skipped values)

| parameter | class | skipped value + locator | proposed definition |
|---|---|---|---|
| bw_1db_ghz on switch_fabric | switch_fabric | colbourne2018 typically 38 GHz at -1 dB for a 50 GHz channel (p.3) | 1-dB passband width in frequency of a WSS channel (as bw_0p5db_ghz / bw_3db_ghz) |
| polarization_shift_nm (polarization-dependent wavelength shift) | wdm | takenobu2008 TE-TM shift < 0.15 nm (p.2 Sec. 3, Fig. 7) | channel-centre wavelength difference between TE and TM inputs, positive nm (already raised by the jeong2020 audit) |
| switching_energy_pj | phase_shifter | zheng2018 ~620 pJ reset / ~200 pJ set per pulse (p.9) | optical or electrical energy per switching pulse for the stated transition (D81 rejected; reported as a confirmed skipped value) |
