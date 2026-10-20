# Batch report bt_02 (weak-tail, 2026-10-20)

Transcribed by the coordinator. Dry-run 0 errors: 7 components, 8 metrics from 5 of 15 papers.

- shen2021 (1/1, fab AMF): inverse-taper EC ~6 dB per facet, 2 um band (EO notes only). Not entered: TiN heater 6 nm/V (no per-volt parameter).
- yu2026 (1/1): 1310 nm DFB 70 mW, basis specification (nominal TOSA parts-list value; drive and reference plane not stated).
- holzgrafe2020 (2/3, facility CNS "performed in part at"; no EO rows): focusing GC ~10 dB per coupler (L band inferred from ~1586 nm modes); photonic molecule (coupled_rings) Qi ~1.4e6 at 1586 nm, -20 V bias, linewidth_mhz ~1000 (total loss rate of the bright mode). Not entered: coupler IL variation < 0.4 dB, 3.1 GHz splitting (now mode_splitting_ghz, D73), intrinsic loss rate 130 MHz (now kappa_intrinsic_mhz), projected Q 1e7. EO follow-up: holzgrafe2020 has no EO device row.
- navarro2026 (1/1 design): bare Si3N4 waveguide simulated ~0.056 dB/cm at 1550 nm TE 300 K (no cap vs the EO rows' 300 nm cap, noted); hosts all six EO rows.
- xu2026b (1/1): EC 4.8 dB loopback_half derived ((12 - 2.4) / 2, equal facets assumed).
- yue2025 (1/1, fab AMF p.11): GC ~4.8 dB per coupler, C band inferred, hosts -a to -d. Supplement S2-S4 not cached.
- No rows: bao2026a, liu2021, sayem2026c, chen2025, karakida2026, sayem2026, gui2022, lin2026, yeh2026.

Gaps: tuning_efficiency_nm_per_v; il_variation_db; mode_splitting_ghz (added D73).
