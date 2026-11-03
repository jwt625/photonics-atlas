# Batch lit_68 report (distill subagent, 2026-11-02)

Dry-run: `batch lit_68: +22 components, +166 metrics; errors 0` (the only warning is pre-existing, ni2025b, another batch).
ASCII only, no e-mail / street / postal text, no quotes beyond a few words. Page-1 title of all six cached texts matches the
source row; no correction-only or wrong document; no garbled text layer. Supplements are not in the cached texts (xue2026
Notes 1-3, xue2022 Supplement 1, wang2025b S1-S5). Figure values read from page renders and zoomed crops.

## Per paper (components / metrics)

- xue2026 (3 / 27): lateral SACM Si-Ge APD (`photodetector.apd`, soi): 0.75 A/W internal at -3.5 V (derived, on-chip via own
  6 dB/facet GC + reference PD), 8.4 uA at -12.5 V, breakdown 13 V, bandwidth 31 / 8 / 36 / 30 GHz at the stated bias and input
  power, seven gains 36-244 (-12 to -24 dBm), GBP 7564 / 2628 GHz (derived, gain x bandwidth), F(M) two figure reads, Ge
  9.1 x 0.5 x 0.26 um, Si 220 nm, etch 70 nm, 8-channel array. GC 6.0 dB (loopback_half, D167). Rear DBR (`reflector.bragg`):
  > 90 % at 5 periods, simulated, row_kind fabricated.
  Not entered: effective k 0.05, simulated ORL -22.5 dB, +35 % responsivity from DBR + taper, Wp / delta W, doping, sensitivities,
  DBR 1100-1700 nm range (level not stated), 1.06 A/W theoretical, comparison Table 1 rows, slab thickness (not printed).
- xue2022 (4 / 30): InGaAs lateral p-i-n PDs on (001) SOI (`photodetector.iii_v_on_platform`, platform `iii_v_on_si_epi`, D252).
  0.5 um row: 60 pA at -1 V, < 1 nA at 85 C, 0.002 and 0.03 A/cm2 (2 / 30 mA/cm2 derived). 1.0 um row: responsivity 0.4 / 0.16 /
  0.44 / 0.12 A/W (derived, 10 dB fiber coupling removed), 0.6 / 0.2 (author_estimate, simulated 70 % coupling), 52 GHz (FFT) and
  50 GHz (0.441 / 9 ps), 0.7 fF, 1.5 kOhm, dark current figure read. Si inverse taper across the air gap
  (`waveguide_platform.transition`): about 70 % simulated, tip 150 nm, 500 nm, 100 um, 480 nm, gap 400 nm. Flat polished edge coupler
  10 dB per_facet (`band: unspecified`, stated for O and C).
  Not entered: saturation photocurrent > 1 mA (D159, see calls), 2.0 and 5.0 um PDs (geometry and eye diagrams only, no row),
  no-taper curve about 38 % (no such row), RC 190 GHz / transit 74 GHz limits, PL peak, eye diagrams, comparison statements.
- beckerwerth2021 (4 / 27): InAlAs APD 5 x 20 um2 and InP APD 4 x 50 um2 (`photodetector.apd`, inp), fab Fraunhofer HHI
  ("we designed, fabricated"): responsivity and external QE at the unity-gain voltage (0.65 / 52 % at 9 V; 0.85 / 68 % at 19 V),
  breakdown < 17 / 27 V, dark current 1 uA at 16 V / < 60 nA at 25.5 V, bandwidth and gain vs bias at 50 uW, saturation 5 / 3 mA.
  PIC balanced APD + 2x2 MMI (> 0.26 A/W, 14 GHz) and the MMI (17 % -> 0.81 dB, author_estimate, origin not stated).
  Not entered: RF output power, dynamic range, minimum input power, CMRR, gain "up to M = 25" (no bias; Fig. 6 reads about 34),
  M = 2 in the linearity section (no bias), mesa width / length rows (orientation not stated, muthuganesan2023 precedent), Table I
  material parameters, 2x3 MMI PIC (no metric).
- alasio2024 (8 / 56): six VPIN variants (`photodetector.ge_waveguide`, soi, Table II): measured bandwidth ranges at -3 / -0.8 / 0 V read
  off Fig. 6 (`extracted_from_figure`, +/- 1 GHz), simulated responsivity (Table II), geometry; Device 2 also Fig. 2 dark current
  reads. Two simulated design rows: HGe 0.3 um (Table I 64 GHz, 0.76 A/W; 45 GHz at 0 V) and HGe 0.4 um (> 40 GHz at 0 V, 0.81 A/W
  read, 61 GHz read).
  Not entered: Table I "this work, experiments" 0.9 A/W / 39.8 GHz (D159), coupling and waveguide losses (type / length not stated),
  family statements (40 GHz at -2 V "with two exceptions", about 10 GHz at 0 V; D254), -1.5 V Fig. 6 points, 35 fJ/bit, simulated
  Fig. 7 sweep points, Wdoping / Wmetal / Wtaper (no parameter, in core_material), comparison rows of Table I.
- wang2025b (1 / 21): ultra-thin lateral Ge PD 60 um x 600 nm x 100 nm: 1.05 A/W at 1550 nm, about 1.2 at 1525 nm, > 0.8 over
  1525-1580 nm (all -2 V, GC to fiber loss excluded, derived), 7 nA at -1 V, < 20 nA at -3 V, 100 / 70 / 40 GHz at -3 / -2 / -1 V,
  photocurrent series up to 3.13 mA (ge), capacitance 12.5 fF read from Fig. 1(b), 105 GHz simulated, design and STEM geometry.
  Not entered: other Fig. 3(b) points (text values enough), eye diagrams, 200 nm width extrapolation beyond 200 GHz, I-region width,
  doping, pad pitch, 14.3 % capacitance reduction (in note), absorption efficiency Fig. 1(f).
- bian2025 (2 / 5): ultra-fast Ge PIN PD: median about 0.96 A/W at 1310 nm, mean < 20 nA at -1 V (> 400 devices), > 135 GHz at -2 V.
  Enhanced designs row: > 1 A/W, QE > 95 % (preliminary).
  Not entered: ORL -36 / -23 dB, BW degradation < 10 GHz at 3 mW, BW-responsivity product, eyes, Table 1 literature rows.

## Missing orgs (name as printed + locator)

- "MCPF of HKUST" (xue2022 p.7 Acknowledgment, "NFF and MCPF"): facility not in `organizations.csv` / `org_aliases.csv`; NFF entered
  (`org_nanosystem_fabrication_facility`).

## Judgment calls for the auditor

1. Fab orgs left empty under D80b / D154: bian2025 (all authors GlobalFoundries, "in a 300-mm CMOS silicon photonics foundry", no
   fabrication sentence; recommend audit decide `org_globalfoundries`); alasio2024 ("manufactured", Cisco platform named in the title,
   no fabricator sentence); wang2025b ("we proceed to analyze and fabricate" p.3, 13 of 14 authors at Zhangjiang Laboratory, one
   only at Fudan University); xue2022 (first-person fabrication, authors across HKUST, SYSU, CUHK); xue2026 (no statement).
2. xue2022 NFF as facility from "thank ... for technical support" (the facility, not named staff).
3. xue2022 60 pA tied to the 0.5 um row through Fig. 5(a) (sentence names no length); the printed 0.002 A/cm2 implies 3 um2, while
   0.5 x 0.48 um = 0.24 um2: density values entered as printed, flagged in notes.
4. xue2022 saturation > 1 mA kept out (D159): Fig. 5(c) 1.0 um curves stay below 1 mA and the text says it grows with length.
5. xue2022 printed 0.44 A/W at 1.3 um vs Fig. 5(d) highest symbol about 0.41 near 1340 nm: printed value kept, flagged.
6. Responsivity basis `derived` when fiber or GC loss is removed (xue2026, xue2022, wang2025b; liao2011 / D394 analogue); wang2025b
   GC loss is not printed in the main text. bian2025 and beckerwerth2021 `measured` with ref_plane unspecified (no de-embedding
   described; beckerwerth "including all coupling losses", input plane not stated).
7. xue2026 GBP `derived` (D80a, factors printed in the same sentence) although merged kang2008 / tossoun2019 rows use `measured`.
8. beckerwerth2021 wavelength 1550 nm `wavelength_inferred` on responsivity and QE (design wavelength; R / QE ratio only fits about
   1550 nm). M = 40 InP: bias -26.3 V read from Fig. 6 (validator requires a bias; reading in notes). M = 10 and M = 12 at 16 V
   both kept (different stated conditions).
9. alasio2024 Fig. 6 ranges are figure reads over nominally identical samples; only Device 2 has a stated sample count (5). Platform
   soi from the paper's family statements (p.6, p.7); Fig. 1 shows only a Si substrate. Table I "this work, optimized" tied to HGe 0.3
   um through Fig. 7(b) and Fig. 8(b). HGe 0.4 um text > 40 GHz at 0 V vs Fig. 7(b) about 37.5 GHz: flagged.
10. Row kind `fabricated` for the xue2026 DBR and xue2022 taper (physically on the chip, simulated performance only; 80 merged
    precedents), with basis `simulated`.
11. wang2025b `saturation_photocurrent_ma` 3.13 with `ge`: highest eye-series photocurrent, no saturation reached.
12. bian2025 statistics, BW are not stated per Ge shape (flat vs chamfered): one row, label without "chamfered", note says so.
13. wang2025b page footer "Corrected 02 February 2026": whole article, not a correction-only file; no erratum text in the cache.

## Registry gaps (skipped value + locator, proposed definition)

- `back_reflection_db` for photodetector: bian2025 p.1 (36 dB chamfered, 23 dB flat reference, OFDR), xue2026 p.3 (22.5 dB simulated). Widen
  the class list.
- `ionization_ratio_k` (photodetector, effective k): xue2026 p.5 (about 0.05). Definition: effective impact-ionization ratio from an F(M) fit.
- `rx_sensitivity_dbm` (photodetector): xue2026 p.5 (-20.8 / -17.1 / -14.2 / -9.6 dBm at HD-FEC, no TIA). Definition: optical input at a stated
  BER and bit rate.
- `rf_output_power_dbm` and `dynamic_range_db` (photodetector): beckerwerth2021 p.5-7 (-6 and -25.8 dBm; 34 / 36 and 30 dB).
- `cmrr_db` (photodetector, balanced pairs): beckerwerth2021 p.7, Fig. 11-12.
- `bw_responsivity_product_ghz_a_per_w` (photodetector): bian2025 p.1-2 (> 130).
