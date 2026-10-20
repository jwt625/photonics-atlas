# Batch report bt_01 (weak-tail, 2026-10-20)

Transcribed by the coordinator. Dry-run 0 errors: 9 components, 17 metrics from 5 of 15 papers.

- hillier2025 (1/1, fab SMART Photonics JePPIX PDK): facet to lensed fiber 2.5 dB per facet (5 um MFD; author_estimate subtracted term; no wavelength); hosts 1 mm rows only.
- wang2026b (2/5, fab CityU: co-authors who fabricated all there): edge facet ~5 dB per facet author_estimate (1540-1595 nm inferred); TO add-drop MRR (wdm.mrr) FSR ~280 GHz, 6.7 pm/mW, thermal crosstalk 0.36 pm/mW at ~700 um, OBRR > 20 dB as crosstalk_db. Not entered: solder-joint electrical loss, 2x8 switch crosstalk (EO).
- gaier2025 (2/3): butt-coupled facet 9 dB per facet at 1550 nm TE measured; racetrack linewidth 220 MHz (1550 nm pump, inferred), design FSR 30.79 GHz. Fab empty (Harvard + EPFL authors). EO follow-up: the mmWave EO comb racetrack has no EO row.
- sabatti2024 (3/5, facilities FIRST, BRNC, IBM Research Zurich): fundamental GC 4 dB at 1550 nm and SH GC 7 dB at 775 nm (author_estimate, design section); PPLN SHG (frequency_converter.shg) 35 %/W at 1536 nm (inferred), poling 2.48 um, 7 mm. Not entered: cited 4280 %/W/cm2 and the ideal value computed from it.
- okuda2026 (1/3): BH DFB threshold 8 mA, 19 mW at 100 mA (ref plane not stated), ~1310 nm, 55 C (EO notes only). fab_org_ids = Mitsubishi Electric although the paper does not state who fabricated it (coordinator: violates D72, to remove in the audit patch).
- No rows: arabjuneghani2022, qi2024, liu2026c, valdez2026, chen2024 (no EO rows), heidari2022, yang2026, gao2024, kawahara2026, suceava2025 (no EO rows).

Orgs missing: ScopeM (ETH Zurich; sabatti2024 p.4), SJTU-Pinghu Institute of Intelligent Optoelectronics (wang2026b p.8, not used).
Gap: rejection_ratio_db for wdm (OBRR) instead of crosstalk_db.
