# Batch report bf_09 (2026-10-20)

Transcribed by the coordinator. Dry-run 0 errors: 16 components, 28 metrics. Locators spot-checked (two fixed by the agent).

- ummethala2021 (1/1): GC ~5 dB per coupler, measured, C band inferred. Not entered: 6 dB/mm phase-shifter loss (EO), 3 dB lumped "other passive Si structures", cited converter 0.02 dB and MMI 0.2 dB.
- cai2025 (3/7): EC ~5 dB at 1550 nm (per_facet from "fiber-to-chip coupling loss"; hosts -a, -b); 2 um ring 0.142 dB/cm (derived from 14.2 dB/m), FSR 112 GHz, width; Si3N4-LiTaO3 taper 0.28 dB simulated 1500-1640 nm, length, tip (row_kind fabricated). Not entered: intrinsic linewidth 72 MHz (now linewidth_mhz, D71), simulated metal loss, Y-splitters / heater (no values).
- tobing2026 (4/8): SiN:D waveguide 0.41 / 0.21 dB/cm at 1550 / 1310 nm before processing, 0.4 after; TFLN waveguide mean 2.4 / best 1.2 dB/cm; 70 um TFLN ring Q_L 5.5e4 best, radius; SiN-TFLN SSC 0.4 dB per transition (lnoi_loaded_sin). Fab empty ("in-house 200 mm facilities", two affiliations). Not entered: LER, ~40 dB unbalanced-MZI extinction, GCs / MMIs (no values).
- zhou2026 (0): electrical / simulated / cited only.
- powell2024a (3/5): GC 7.9 dB per coupler; 2x2 DC split 53 % author_estimate (simulation from the second-port extinction); uncladded racetrack Qi 4.04e6, 0.09 dB/cm (derived from 9 dB/m), FSR 0.185 nm (derived from 185 pm). Not entered: electrode misalignment 0.7 dB (modulator), FWHM 47.2 MHz (now linewidth_mhz), dn/dT 2.47e-5 /K (no parameter).
- behzadfar2026 (0): simulation-only. chaudhury2024 (0): racetrack test chip (Applied Nanotools) without component numbers.
- valdez2023a (2/4): SiN EC 3.4 dB per facet cutback at 784 nm; SiN feeder 1.6 dB/cm cutback TE (Fig. 1(b) reference read as a typo for 1(c)), width 500 nm, thickness 180 nm. Not entered: 2x2 MMI and 100 um taper (geometry only). Sandia staff thanked by name: not entered.
- yue2023 (2/2): GCs SMIC 4.1 dB, AMF 3.8 dB per coupler, C band inferred.
- tanaka2026 (1/1): TOPS P_pi 20 mW, band unspecified; host empty (device not stated). Not entered: > 30 dB extinction (interferometer), InP-Si taper (no number).

Judgment calls: loss-extraction rings unlinked (not EO devices); unit conversions derived; values held only in EO notes / il_onchip_excludes entered (rule 2).
Orgs missing: Karlsruhe Nano Micro Facility (ummethala2021 p.6, funding); ARIM (MEXT, tanaka2026 p.3).
Gaps: linewidth in Hz (covered by linewidth_mhz, D71); thermo_optic_coeff_per_k.
