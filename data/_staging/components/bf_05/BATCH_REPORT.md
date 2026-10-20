# Batch report bf_05 (2026-10-20)

Transcribed by the coordinator. Dry-run 0 errors: 21 components, 42 metrics; every paper has rows.

- schwarzenberger2026a (4/6): GC 4.6 dB per coupler (center 1326 nm; measured, method unspecified); 2x2 MMI excess 0.12 dB (cascades of 8-48, cutback); strip-to-slot converter 0.51 dB (mode_converter, soi_slot); 420 nm strip 0.32 dB/mm -> 3.2 dB/cm (derived). Not entered: slot 4.44 dB/mm (EO row), simulated FCA loss, "optimized" values (cited / projections), ~9 dB total fiber-chip loss (no scope for two couplers), edge couplers (no value).
- lee2026 (2/8): suspended and reference waveguides at 2.4 / 2.7 / 2.8 / 3.6 um; facility John O'Brien Nanofabrication Laboratory. Not entered: active-region losses (EO), simulated metal loss; Y-splitter and crossing without values.
- niels2026 (2/6): Si to SiN/LiTaO3 transition 0.3 dB per transition at 1310 nm (2 vs 28 transitions), simulated ~100 %, taper/tip/gap; 1x2 MMI (imec PDK) 0.8 dB scope unspecified. Not entered: 0.6 dB for two (= 2 x 0.3), hybrid 1.0 dB/cm (EO), Si routing 3.0 dB (no length), simulated misalignment loss. No fab on the transition (imec layers, authors printed the LiTaO3).
- witmer2020 (2/4): metasurface GC ~30 % typical peak, taper ~300 um; fishbone PhC mirror (design stopband ~60 nm, 5-10 full-strength periods). Not entered: GC FWHM ~40 nm (gap: bw_fwhm_nm), designed extrinsic Q ~50k, measured band edge, microwave CPW resonator. EO follow-up: cavity intrinsic Q 93,100 and extrinsic Q 25,300 not in the EO row.
- aihara2026 (1/4; OFC, restricted): membrane DFB: fiber-coupled -3.7 dBm at 43 mA through the EAM, 55 C; lasing ~1310 nm and SMSR ~33 dB from Fig. 2(a); length 300 um. Not entered: SOA gain 8 dB (cited), 93 mW electrical power (no parameter). No fab statement.
- xu2020 (3/5): a-Si/LN GC 3.4 dB per coupler; single-mode LN waveguide 0.3 dB/cm; TO heater 760 ohm, 160 um, P_pi ~107 mW from Fig. 2(a). Not entered: 4 um waveguide 0.15 dB/cm (EO), MMI (supplement not in text).
- wang2024a (1/1): lensed-fiber facet ~7 dB per facet at 1550 nm; facilities EPFL CMi + IPHYS cleanroom.
- saxena2023 (1/1, fab AIM Photonics): microdisk heater 8 kohm (author_estimate, compact-model parameter). Not entered: 251 pm/mW, 15 us (no parameters).
- wang2022 (2/3): SOI GC 3.6 dB (derived, half of 7.2 dB for two; loopback_half); Si-to-TFLN taper < 0.03 dB simulated, 300 um. Not entered: hybrid 1.6 dB/cm (EO), "negligible" MMI / taper losses, DP-IQ 2D couplers / heaters (no values).
- lotkov2024 (3/4, facility FMN Laboratory): Si3N4 TM waveguide 1.29 dB/cm; facet to SM15 fiber 3.5 dB (per_facet, not written as such); photonic-plasmonic junction 0.6 dB measured / 2.2 dB simulated (platform other). Not entered: 1.2 / 4.4 dB totals (two junctions).

Orgs missing: Stanford Nano Shared Facilities and Stanford Nanofabrication Facility (witmer2020 p.28; not mapped to the later merged org_nano_stanford).
Gaps: bw_fwhm_nm; tuning_efficiency_pm_per_mw; thermal_time_constant_us; platform for dielectric-plasmonic hybrids. Note: some text.md files contain stray bytes (use grep -a).
