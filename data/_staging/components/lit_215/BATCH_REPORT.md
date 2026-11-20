# lit_215 batch report

Distilled 2026-11-20. Five VCSEL papers (all `laser.vcsel`, plus 4 `reflector.bragg` DBR rows for nishiyama2005).
Page-1 titles match the source rows. Validation: `merge_component_staging.py data/_staging/components/lit_215 --dry-run`
-> +26 components, +121 metrics, 0 errors (the one warning printed belongs to an existing ni2025b row, not this batch).

| paper | components | metrics |
|---|---|---|
| chaw2025 | 6 | 43 |
| nishiyama2005 | 16 | 46 |
| wu2025b | 1 | 21 |
| babic1995 | 2 | 7 |
| imai2010 | 1 | 4 |
| total | 26 | 121 |

## chaw2025 (JSTQE 2025, cryogenic oxide VCSEL aperture scaling, UIUC)

- Rows: one per oxide-aperture size with values (6.8, 4.5, 2.9, 2.5, 1.8 um) plus a population row (Fig. 4(b) 15
  devices, Fig. 5 threshold scans). Platform `gaas` (AlAs / AlGaAs DBRs, InGaAs QWs).
- Values: Ith at 293 K (Fig. 3(a) labels), 2.9 K (Fig. 3(b) and Fig. 4(a) labels), 40 K (p.6 list, Fig. 9 labels);
  Pmax before rollover and max slope at 2.9 K (Fig. 4(a) labels, text rounds), slope at 40 K (p.6); SMSR 28 / 38.5 dB
  (RT); RT lasing peaks of the 2.9 / 1.8 um devices read off Fig. 3(a) (+/-0.2 nm); intrinsic f3dB at 40 K (Table I,
  p.7 text, abstract).
- Not entered: Table I 6.8 um column (Ith 0.19 mA, 39.2 / 40.5 GHz) and TDECQ 2.56 dB, attributed to ref. [15] (D259);
  Table II energy per bit (calculated; no parameter); power densities (kW/cm2); threshold current densities (Fig. 5);
  optical-mode diameters (Fig. 6 / 7, calculated); resonance-peak amplitudes 12 / 6 / 4.5 dB (no parameter); 2.3 um
  device (112 / 120 Gb/s PAM-4, TDECQ 3.30 dB, outer OMA 73.96 / 54.26 mV): no registry-parameter value, so no row;
  cryostat cooling power (setup).
- Fab: `org_university_of_illinois_urbana_champaign` on all rows (first-person process statements: p.2 "We
  investigated the scaling ... by reducing the oxide-aperture size using carefully controlled process parameters" in
  the wet-oxidation furnace; p.4 "our 14-year oxide-VCSEL process experience"; all authors UIUC). Facility empty.
- Missing orgs: IntelliEpi (epitaxial wafer supplier, p.2, "grown by MBE from IntelliEpi"): wafer supplier, note only
  (not a fab role). Holonyak Micro and Nanotechnology Laboratory (UIUC) appears only as the author affiliation (p.1),
  not as a facility statement; not in the registry.
- Judgment calls:
  1. Fab UIUC from the process sentences above (D84a "our process" analogue). Auditor to confirm.
  2. Intrinsic bandwidths after RC-parasitic de-embedding entered as `measured` (alasio2024 "pads de-embedded"
     precedent); "> 50 GHz" = measurement limit, qualifier gt.
  3. Ith printed three ways per aperture (spectrum device Fig. 3, L-I-V device Fig. 4(a), 40 K list / bandwidth
     device): each entered with its own locator and condition; 1.8 um at 40 K: 0.30 mA (p.6) vs 0.29 mA (Fig. 9(b),
     Table I), both kept with cross-notes.
  4. Fig. 4(a) Pmax / slope labels (14.08 / 10.01 / 8.35 / 5.21 mW) entered as printed in the figure (`measured`),
     text rounds noted; ref_plane `chip` (large-area PD).
  5. Population row: figure-read ranges (differential resistance 163-372 ohm, n = 15; RT Ith 1.3-4.2 mA; 2.9 K Ith
     0.20-0.27 mA). Drop if array-level figure ranges are not wanted.

## nishiyama2005 (JSTQE 2005, 1.3 / 1.55 um InP BTJ VCSELs, Corning)

- Rows: 1.55 um and 1.3 um VCSELs with 5 / 7 / 10 / 12 um tunnel-junction apertures (8), the 1.55 um 5 um
  zero-detuning sibling (Ith 0.2 mA), the 1.3 um 5 um higher-reflectivity-top-DBR sibling (Fig. 19), two family rows
  (max slope about 0.4 W/A, device not named), and four `reflector.bragg` rows (bottom AlGaInAs / InP DBR 99.9 %
  measured with an absolute reflectivity system; top a-Si / Al2O3 DBR 99.4 %, method not stated -> author_estimate)
  with cross-notes (D396, heermeier2025 precedent). Platform `inp`; top DBR `other`.
- Values: RT thresholds and max powers per aperture (p.3 / p.4), 5 um resistance at 5 mA (110 / 100 ohm), SMSR at
  25 / 55 / 85 C and lasing peaks read off Fig. 7 / Fig. 11 (+/-0.1 nm), 0.6 mW at 85 C, single-mode 2.0 / 1.7 mW at
  25 C, 1.3 um Ith 1 mA at 85 C, Fig. 19 0.8 / 0.3 mW.
- Not entered (no parameter): maximum lasing temperatures 105 / 115 / 125 C; aging (3000 h / 2500 h at 8 mA, 85 C);
  differential quantum efficiency 50 / 43 %; chirp about 40 GHz p-p and alpha about 2-3 (Fig. 14); BER / receiver
  powers / transmission distances (link level); DBR center-wavelength uniformity < 1 % std over 2 in; temperatures of
  minimum threshold 35 / 15 C (Fig. 18); AlGaInAs:C hole concentration 7e19 cm-3 (material).
- Fab: empty (passive growth / processing; all authors at Corning Inc., `org_corning` exists).
- Judgment calls:
  6. Fab empty despite "Recent improvements in MOCVD ... allow us to achieve such precise control" (p.2, first-person
     about DBR growth control). If the auditor reads this as a growth statement, fab = `org_corning` on all 16 rows.
  7. Single-mode power 2.0 / 1.7 mW at 25 C (abstract, conclusion; aperture not named) assigned to the 5 um rows (only
     device with SMSR data; matches the Fig. 6 25 C curve). D159 alternative: move to notes.
  8. 1.3 um room-temperature values: temperature_k left empty (about 20 C is printed only for the 1.55 um series).
  9. DBR reflectivity rows use band + `wavelength_inferred` (wavelength of the maximum not printed; DBRs designed for
     1.3 / 1.55 um). Top DBR basis author_estimate (Fig. 3 method not stated).

## wu2025b (PTL 2025, 1/2-lambda cryogenic VCSEL, 5 um aperture, UIUC)

- One row, platform `gaas`. Values: Ith 1.54 mA, Pmax 35 mW and slope 1.13 W/A at 2.9 K, Fig. 1 label block at 4 mA
  (2.17 mW, 2.46 V, 107 ohm), differential resistance about 57 ohm at 10 mA (2.9-77 K), forward voltage about 1.8 V at
  threshold / 3.85 V (2.9 K) / 3.62 V (77 K) at 40 mA, PCE 32.5 / 35.8 % at 10 mA and 23.7 / 24.4 % at Pmax, fundamental
  mode 849.36-852.20 nm at 2-25 mA, intrinsic f3dB 32.7 GHz (I/Ith 1.2), 45.2 GHz (1.33), > 50 GHz at 2.5 mA and above.
- Not entered: projected intrinsic bandwidth about 100 GHz / > 100 GHz (model projection; ofc2026 Th1A.3 precedent);
  photon / recombination lifetimes 0.89 / 8.85 ps; 50 kA/cm2; TDECQ, PAM-4 rates and fJ/bit (link level); thermal
  cycling; the unetched reference device (only relative statements: 2x rollover, 0.04 mA Ith).
- Fab: empty ("designed and fabricated", passive; D80b). Same group as chaw2025, where a first-person process sentence
  exists; consistent per-paper rule.
- Judgment calls:
  10. Fig. 1 label-block values have no temperature tag: temperature_k empty with a condition note (caption ties only
      1.13 W/A and > 35 mW to 2.9 K).
  11. Pmax entered as 35 mW without qualifier (Fig. 1 label "Pmax = 35 mW", abstract "35 mW"); caption / conclusion say
      "exceeding" / "> 35 mW" (noted).

## babic1995 (PTL 1995, double-fused 1.54 um VCL, UCSB / KTH / HP Labs)

- Rows: 8 um device (CW 2.3 mA and pulsed 1.8 mA lowest thresholds, 23 C) and a family row (1542 nm, +/-2 nm spread,
  CW threshold voltage 3.1-3.6 V, T0 CW 28-37 K and pulsed about 37 K). Platform `other` (InGaAsP / InP active fused
  between AlAs-GaAs / AlGaAs-GaAs mirrors).
- Not entered: Jth 2.5 / 1.4 kA/cm2 (no parameter); 0.32 nm linewidth (multi-transverse-mode limited, D250
  analogue); 33 C maximum CW temperature of two 12 um devices (no parameter; no 12 um row since no performance value
  is printed for it); thermal resistance formula (rests on ref. [6] measurements, cited); active-layer temperature
  estimates; Fig. 2 / Fig. 4 L-I powers (tens of uW, kinked multimode curves; not read); Fig. 3 per-size thresholds
  (log axis, not read).
- Fab: empty (passive; acknowledgment thanks individuals for help with wafer fusion and fabrication, no org).
- Judgment call 12: T0 placed on the family row (the paper does not name the device; CW value follows the 12 um
  Fig. 4 series). D159 alternative: notes only.

## imai2010 (ISLC 2010, 1060 nm DIC VCSEL, Furukawa Electric)

- One row, platform `gaas` (judgment call 13: from the printed InGaAs / GaAs MQW; substrate and mirrors not stated;
  D422 alternative: empty). Values: Ith 0.40 mA, slope 0.41 W/A, series resistance 78 / 67 ohm at 1.2 / 4.0 mA (RT).
- Not entered (no parameter): 0.14 mW/Gbps power dissipation per data rate (energy per bit) at 1.4 mA, 10.3125 Gb/s,
  75 mVpp; BER, ER 6.5 dB, total jitter < 45 / 60 ps (eye-level). Nominal 1060 nm only.
- Fab: empty ("our 1060 nm VCSELs", "The fabricated DIC VCSEL"; D80b). `org_furukawa_electric` exists if the auditor
  reads it otherwise.

## Registry gaps (skipped values, proposed definitions)

- `threshold_current_density_ka_per_cm2` (laser): babic1995 2.5 / 1.4 kA/cm2 (p.2); chaw2025 Fig. 5 Jth; recurring
  (hamaguchi2018, heermeier2025 precedents).
- `max_operating_temperature_c` (laser): highest temperature with lasing / CW operation: nishiyama2005 105 / 115 / 125 C
  (p.4, p.5, p.7); babic1995 33 C (p.3); recurring in merged notes.
- `energy_per_bit_fj` (laser, link-level as stated): imai2010 0.14 mW/Gbps = 140 fJ/bit (p.2, computed by the authors);
  chaw2025 Table II; wu2025b 140.8 / 119.5 fJ/bit. Possibly better kept as system metrics.
- `oxide_aperture_um` (laser geometry): aperture diameters are only in labels here (6.8-1.8 um, 5 um, 5-12 um, 8 um).
- `differential_quantum_efficiency_pct` (laser): nishiyama2005 about 50 / 43 % (p.3 / p.4).
- Photon / carrier lifetime (wu2025b 0.89 / 8.85 ps): model-extracted; low priority.

## Missing orgs (name as printed + locator)

- "IntelliEpi" (chaw2025 p.2): epitaxial wafer supplier (note role, not fab).
- "Nick Holonyak Micro and Nanotechnology Laboratory", UIUC (chaw2025 p.1, wu2025b p.1): affiliation only; no
  facility statement in either paper.
