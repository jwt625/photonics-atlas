# lit_244 batch report

Batch lit_244 (family B, lasers), distilled 2026-11-22. Papers: lit:sato2007, lit:faugeron2011, lit:sato2008a,
lit:chen2002, lit:menna2001. Page-1 titles match the source rows. No paper had component rows before this batch.
Dry run of `merge_component_staging.py`: +10 components, +82 metrics, 0 errors. The one warning is about an existing
row (ni2025b) that this batch does not touch.

| paper | components | metric rows |
|---|---|---|
| sato2007 | 2 (BH-DFB `laser.dfb`, BH-FP `laser.other`) | 16 |
| sato2008a | 2 (BH-DFB `laser.dfb`, BH-FP `laser.other`) | 16 |
| faugeron2011 | 2 (DFB `laser.dfb`, laser-to-lensed-fiber `fiber_chip_coupler.edge`) | 20 |
| chen2002 | 1 (BH-DFB `laser.dfb`) | 17 |
| menna2001 | 3 (section A DFB, section B DFB, laser-to-fiber lens assembly `fiber_chip_coupler.edge`) | 13 |

All laser rows use platform `inp`. No `process_name` is entered: no paper names a process.

## sato2007 (2.1 um InGaAs MQW DFB, NTT)

- DFB: threshold 19 mA. Output 8 mW at 25 C and 3 mW at 55 C (both at 150 mA). T0 48 K. SMSR 30 dB. Lasing wavelength 2104 nm. Thermal drift 97 pm/K (printed 0.097 nm/C, derived). Tuning range 4 nm over 2103-2107 nm (derived from the printed span). Mesa 1.4 um, cavity 600 um.
- FP: threshold 18 mA (best). Output > 14 mW. Mode spacing 1.08 nm (`fsr_nm`). Emission peak 2127 nm. Mesa 1.4 um, cavity 600 um.
- Values not entered:
  - Current-tuning rate 0.005 nm/mA: no registry parameter (D83g).
  - Median lifetime > 1e5 h, extrapolated from 4500 h of aging on ten lasers: lifetime is not in the registry (D77 / D81).
  - PL, TEM and SIMS results: material values. Fig. 2 is reproduced from the authors' ref. [10] and was not used.
- Fab: left empty. The paper says "we fabricated", but five authors are at NTT Photonics Laboratories and one (T. Watanabe) is at Hirosaki University. His biography says he was at NTT until 2006. Judgment call (a).

## sato2008a (2.33 um InAs/InGaAs MQW DFB, NTT)

- DFB:
  - Threshold 61 mA and slope efficiency 0.054 W/A, both at 25 C.
  - Output 20 mW at 25 C (best) and 4 mW at 75 C.
  - SMSR about 30 dB. The text says "approximately"; the Fig. 3 label says "> 30 dB". The text value is kept.
  - Lasing wavelength 2337 nm. Thermal drift 148 pm/K (derived).
  - Tuning range > 13 nm over 2335-2348 nm.
  - Mesa 2.0 um, cavity 900 um.
- FP (cleaved facets): threshold 46 mA at 25 C and 94 mA at 75 C. T0 71 K. Gain-peak drift 1050 pm/K. Mesa 2.0 um, cavity 900 um.
- Values not entered:
  - Maximum operating temperature 95 C: no registry parameter (registry gap below).
  - Current-tuning rate +0.007 nm/mA (D83g).
  - Calculated band offsets 231 meV and 128 meV: material values.
  - The T0 of 40 K in a 3 nm InAs MQW is cited from ref. [12] (rule 3).
- Fab: `org_ntt` on both rows. The paper says "we fabricated" and all seven authors are at NTT Photonics Laboratories, Nippon Telegraph and Telephone Corporation. This follows the lit:sato2008 precedent, which also uses `org_ntt`.

## faugeron2011 (1.55 um high-power low-RIN DML DFB)

- DFB, all at 25 C regulated:
  - Output 98 mW at 350 mA, > 123 mW at 450 mA, 140 mW at 550 mA, and 146 mW at 600 mA (maximum).
  - Differential efficiency 0.340 W/A at 350 mA and 0.233 W/A at 450 mA. It is dP/dI from a pulsed L-I at the estimated junction temperature, entered as `measured`.
  - Threshold about 72 mA, read from the Fig. 1 knee (+/- 5 mA, `extracted_from_figure`). No threshold is printed.
  - SMSR > 55 dB at 1552.1 nm.
  - RIN < -157 dB/Hz (450 mA, 0.1-20 GHz) and about -165 dB/Hz (550 mA, 0-3.5 GHz).
  - Relaxation frequency 7 GHz, from the RIN peak.
  - Modulation bandwidth > 7 GHz above 400 mA. The photodiode response was not corrected.
  - Far-field FWHM 12 deg horizontal and 33 deg vertical.
  - R_L 1.5 ohm (`author_estimate`, origin not stated).
  - Kappa about 14 /cm (`author_estimate`, from the design kappa L of about 1.4 over 1 mm).
  - Ridge 3.5 um, cavity 1000 um (printed 1 mm, `derived`).
- Lensed-fiber coupling > 65 % `per_coupler`. Wavelength inferred from the DFB peak.
- Values not entered:
  - Design internal loss 3.5 /cm and confinement factors (effective-index calculation): no internal-loss parameter (registry candidate since D433).
  - Link gain -7.1 dB and the assumed 70 % coupling in Eq. (2): link-level estimate and assumed input.
  - The values in the introduction come from refs. [4]-[8] (rule 3).
- Fab: left empty. The conclusion says "we have fabricated", but the authors are at Thales Air Systems, III-V Laboratory and SUPELEC (D154). The acknowledgment thanks a III-V lab member for "technical support", which is not a fabrication statement. `org_iii_v_lab` exists in the registry. Judgment call (b).

## chen2002 (1.3 um uncooled linear DFB, Ortel)

- Population:
  - Room-temperature thresholds 1.5-4.5 mA (range).
  - Slope 0.50-0.65 W/A, printed in mW/mA (`derived` under D256; same number).
- Fig. 1 laser: thresholds 1.4 mA at 20 C, 7.2 mA at 80 C and 11.4 mA at 95 C. The 1.4 mA lies below the printed population range. It is kept, with a note.
- Fig. 2 / 3 laser:
  - Maximum output from the AR facet: 90 mW at 20 C, 38 mW at 80 C, 18 mW at 110 C.
  - Slope 0.65 / 0.53 / 0.48 W/A at 20 / 80 / 95 C.
  - SMSR > 40 dB from -50 to 110 C.
  - Wavelengths 1310.4 nm (20 C) and 1315.4 nm (80 C), from the Fig. 3(d) / 3(e) marker labels.
- RIN < -155 dB/Hz. The paper prints "better than 155 dB/Hz" with no sign. Judgment call (c).
- Stripe about 1 um, cavity 250 um.
- Values not entered:
  - Single-mode operating range -50 to 110 C (registry gap below).
  - CSO < -45 dB, CTB < -65 dB and SFDR > 108 dB Hz^(2/3): link-level values.
  - Fig. 3 wavelength labels at -50, -20 and 0 C are cut off in the render. The 110 C label (1.31800 um) has an ambiguous digit count.
  - T0: not printed.
- Fab: left empty. The fabrication sentence is passive and all authors are at Ortel Corporation (D80b).

## menna2001 (1550 nm 440 mW DFB, Princeton Lightwave)

- Section A DFB:
  - Ex-facet output 440 mW on a Cu C-block at 1.6 A, and 370 mW on a T-cBN submount.
  - 340 mW in fiber (`ref_plane` fiber).
  - SMSR about 30 dB. Wavelength 1548 nm.
  - Ridge about 3 um, cavity 2000 um (`derived`).
- Section B DFB (detuned grating):
  - Slope about 0.3 W/A in both the FP and DFB regimes.
  - DFB line 1578 nm.
  - Linewidth minimum 1.6-2 MHz above 100 mW (two lasers, 45 C from the Fig. 3 inset label; MHz -> Hz `derived`).
  - Ridge about 3 um, cavity 2000 um.
- Lens-fiber assembly: coupling 75-77 %, `per_coupler`. Band `c_band`, inferred.
- Values not entered:
  - Far-field divergence: fast axis 31 deg, slow axis 11.5-14.0 deg. The paper prints it for "the laser" without naming section A or B. It is kept in notes on both rows (D159). Judgment call (d).
  - The 165 mW and 1 W comparison values are cited (rule 3).
  - The FP gain peak of 1525 nm is a property of the base structure (kept in `core_material`).
- Temperature conflict: the abstract says 20 C, but the Fig. 1 / 2 labels say Tc = 18 C. The text value is used for the 440 / 340 mW rows and the conflict is noted (D417).
- Fab: left empty. The paper says the lasers were "fabricated using conventional techniques as described elsewhere", which is passive (D80b).

## Missing fab / facility orgs

None needed. No row has a fab or facility org that is missing from the registry. Orgs printed in the papers that are not in the registry, for the header batches only: Ortel Corporation (chen2002 p.1), Princeton Lightwave, Inc. and Sarnoff Corporation (menna2001 p.1), Thales Air Systems (faugeron2011 p.1), Hirosaki University (sato2007 p.1). None of them has a fab role.

## Judgment calls

- (a) sato2007: fab is left empty despite the first-person "we fabricated", because one of six authors is at Hirosaki University (D154 / D433). The alternative is `org_ntt`: the Hirosaki author was at NTT until 2006 and the paper thanks NTT Photonics Laboratories members.
- (b) faugeron2011: fab is left empty despite "we have fabricated", because the authors are at three orgs (D154). The likely fabricator, III-V Lab, is not stated.
- (c) chen2002: RIN "better than 155 dB/Hz" is stored as -155 with `lt` and `measured`. This is sign normalization with the printed form in notes. The alternative is `derived` under D82d.
- (d) menna2001: far-field divergence is not entered on either section row (D159), because the paper does not tie it to section A or B.
- (e) Laser facet to lensed fiber / lens assembly coupling is entered as `fiber_chip_coupler.edge` rows on platform `inp` (cao2025 and juodawlkis2009 facet precedents; D554 coupling to the setup fiber). The faugeron2011 wavelength is inferred from the 450 mA DFB peak.
- (f) "As high as" / "as low as" on single-device values are entered as `statistic: best` (rule 7): sato2007 FP threshold, DFB 8 mW and SMSR 30 dB; sato2008a 20 mW.
- (g) menna2001 sections A and B are separate rows: they have different grating periods (D32 sibling designs). The two section-A lasers on different mounts are one row, with the mount in `condition`.
- (h) faugeron2011 threshold about 72 mA is read off the Fig. 1 curve, because the paper prints no threshold.

## Registry gaps

- `max_operating_temperature_c` / operating temperature range (laser): sato2008a, lasing and single-mode operation up to 95 C (p.2 Sec. III; p.1 Abstract); chen2002, single-mode -50 to 110 C (p.1 Abstract, p.2 Fig. 3). Proposed definition: highest (or range of) heatsink temperature at which CW lasing / single-mode operation is shown.
- `current_tuning_pm_per_ma` (laser, static DFB wavelength shift per mA): sato2007 0.005 nm/mA (p.3 Sec. IV); sato2008a +0.007 nm/mA (p.2 Sec. III). D83g keeps it out of `fm_efficiency_ghz_per_ma`.
- `internal_loss_per_cm` (laser): faugeron2011 design 3.5 /cm (calculated, p.1-2). This is an existing candidate (D433).
- Lifetime: sato2007 median lifetime > 1e5 h, extrapolated (p.3-4, Fig. 9). It is a rejected parameter (D77 / D81) and is listed only for the record.

## Registry / source issues

- lit:chen2002: the registry year is 2002, but the DOI is 10.1109/islc.1996.558791 and the newest reference is 1995. The paper is likely from ISLC 1996. The year is left for the coordinator.
- lit:faugeron2011: the registry year is 2011 (published online 2011-10-25), but the journal issue is January 2012 (vol. 24, no. 2). This is recorded for information only.
