# cov_01: platform papers (TSMC IEDM 2024, GF 45RFSOI, AIM MPW, COBRA InP, IQA Si3N4, TriPleX x2)

Date: 2026-11-07. Contract: pic-component-distill skill (v4-v6). Locators `p.N` = page of `references/<paper_id>/text.md`;
`p.N Supp. <label>` for the supplementary parts that sit in the same text.md (kramnik2024 p.22-45, chen2026c p.12-26).
Page-1 title check: all 7 cached texts are their source rows' papers (no corrections or errata).
Existing rows: `data/components/components.csv` had 0 rows for these 7 sources.

Result: 61 components, 151 metric rows. `merge_component_staging.py --dry-run`: 0 errors (+61 / +151).

| paper | components | metric rows | fab_org_ids | facility_org_ids |
|---|---|---|---|---|
| yeh2024 (TSMC, IEDM 2024) | 12 | 22 | org_tsmc (borderline, Q1) | - |
| kramnik2024 (UC Berkeley / BU / Northwestern, arXiv 2024) | 8 | 37 | org_globalfoundries | org_marvell_nanofabrication_laboratory (45RFSOI rows) |
| fahrenkopf2019 (AIM Photonics MPW, JSTQE 2019) | 17 | 24 | org_suny_polytechnic_institute; org_aim_photonics | - |
| dagostino2015 (COBRA TU/e, OE 2015) | 6 | 20 | - (D80b) | - (NanoLab@TuE missing, Q6) |
| chen2026c (IQA Shenzhen, arXiv 2026) | 5 | 16 | - (org missing, Q5) | - |
| roeloffzen2018 (LioniX TriPleX, JSTQE 2018) | 12 | 30 | - (D80b, Q7) | - |
| worhoff2015 (LioniX TriPleX, AOT 2015) | 1 | 2 | - (D80b, Q7) | - |

## yeh2024: TSMC silicon photonics platform (IEDM 2024)

Components: Ge waveguide PD; Si single-mode and multimode rib WG; PECVD SiN single-mode and multimode WG; SiN edge
coupler; SPGC design family (Fig. 6(c)); PSGC; COUPE GC with embedded micro-lens; MRR and SPGC process-monitor rows
(Table 1 within-wafer 3 sigma); 16-channel DMRR DWDM filter.

Check of the earlier web-research values (all verified at the locators):

| value | paper | entered as |
|---|---|---|
| PD ~1.0 A/W | 'close to 1A/W' at 5 mW in the WG, wafer-level data; wavelength and bias not stated | 1 A/W approx, on_chip, o_band inferred (PDK is O-band), measured (p.2, Fig. 8(a)) |
| PD ~110 GHz at -1.75 V | 110 GHz at 200 uA photocurrent, -1.75 V (Fig. 8(c) caption); > 50 GHz at 1 mA (bias not stated) | two bw3db_ghz rows |
| dark 4.5 nA median at -1.5 V | confirmed (median across the wafer); Fig. 8(b) label < 20 nA up to -2.5 V | two dark_current_na rows |
| ring modulator 76 GHz | 63 / 76 GHz S21 at 6 / 4 dB IL, 0.35 V-cm phase efficiency (Fig. 7) | not entered (EO-atlas scope) |
| Si WG 0.67 / 0.20 dB/cm | 'offered as part of the PDK', no method, structure, wavelength or data | author_estimate (origin not stated), o_band inferred, method unspecified |
| SiN EC 1.2 dB | 1.2 dB IL, PDL 0.18 dB at 1270-1330 nm, 'is demonstrated'; per-coupler vs per-facet-pair, fiber and method not stated | measured, scope unspecified |

Also: SiN WG 0.21 / 0.14 dB/cm at 1310 nm ('yielded', measured, method unspecified); COUPE FAU coupling loss 0.3 dB
(author_estimate, scope per_coupler, O-band; +/- 10 um alignment tolerance without a loss criterion kept in notes);
SPGC peak loss < 1.3 dB, 1-dB BW ~20 nm; PSGC peak loss ~2 dB, 1-dB BW ~25 nm (both scope unspecified); DMRR 200 GHz
design spacing, measured spacing 1.11 nm (+/- 0.26) over 16 channels, WiW resonance 1 sigma <= 0.7 nm.

Not entered: 2x2 MMI curves (Fig. 6(a), simulation only); SPGC sweet-spot map (simulation); CD 3 sigma < 2 nm, CD /
trench-depth 3 sigma percentages (process statistics); 0.5-2 nm wavelength shift per nm of CD / depth / thickness (no
parameter); DMRR in-band loss (normalized spectra); PDK library items without values (crossing, Y-junction, VOA, PBSR,
Si-to-SiN transition, APD, temperature sensor).

## kramnik2024: feedback-stabilized SFWM sources, GF 45RFSOI (+ 45SPCLO preview)

Fab: 'fabricated as part of an MPW ... on GlobalFoundries' 45RFSOI process sponsored by Ayar Labs' (p.7) and
'fabricated in GlobalFoundries' 45RFSOI CMOS process' (p.3) -> org_globalfoundries. Facility: handle removal by XeF2 in
the Marvell Nanofabrication Laboratory (p.7) -> org_marvell_nanofabrication_laboratory on all 45RFSOI rows (every
photonic device needs it). 45SPCLO rings: 'designed and fabricated in 45SPCLO' (p.30) -> GF, no facility.

Components (45RFSOI): SFWM ring (R_out 19.1 um, W 2.8 um; die B9 system site: Q_o / Q_e for signal, pump, idler,
mean Q_o,p over 12 measurements, FWHM 4.54 GHz and mean 4.69 GHz, FSR_sp / FSR_pi, pump-resonance std 1.74 nm over
6 dies x 2 sites, tuning 0.62 nm at 5.1 mW); in-ring p-i-n photodiode (~1 mA/W, D396 cross-note); bi-layer VGC
(3.0 dB, loopback_half, derived); 6th-order Vernier pump-rejection filter (> 100 dB, ~95 dB ASE-limited, ~60 dB at
sub-filter FSRs); 2nd-order cleanup filter (40 dB, author_estimate). 45SPCLO: full-rib ring (Q_o,p 878.2k, Q_e,p
120.0k, FSR 654.75 GHz, R 19.45 um, gap 435 nm, bus 0.5 um), half-rib ring (Q_o,p 332.2k, Q_e,p 95.0k, FSR 646.06 GHz,
R 19.2 um, gap 290 nm; tuning 3.32 nm at 22.5 mW with the 4-point heater, Supp. Fig. 7), single-mode WG < 2 dB/cm
(C and O band, author_estimate).

Basis calls: all q_intrinsic / q_external author_estimate (D403: all-pass Lorentzian fits, regime not determined from
the data; 45SPCLO 'overcoupling' is stated, not shown). FWHM GHz -> MHz derived.

Not entered: 4.6 dB/cm 45RFSOI waveguide loss (cited, ref. 6); 6th-order filter IL < 1 dB (cited from the authors'
earlier paper, ref. 74, D259); all packaging losses in Supp. S5 (refs. 55, 63, 68, 70: 10 / 15 dB, ~5 / ~7 dB,
< 1 dB / 2 dB edge coupling, < 1 dB GC); design targets Q_o 116.5k / Q_e 87.4k (simulated); PGR / CAR / g2 and FSR
mismatch (no parameter); 18.8 um / 2.0 um ring variants (no separate data); 400 nm single-mode WG (geometry only);
W_full / W_partial of the 45SPCLO rings (roles undefined); heater DAC / TIA / ADC electronics.

## fahrenkopf2019: AIM Photonics MPW, APSUNY PDK

Fab: circuits fabricated at the SUNY Polytechnic Institute 300 mm fab (p.1, p.3) for the AIM Photonics MPW service
(rule 12 / D398) -> both orgs. Analog Photonics designed the PDK (designer, noted). MOSIS aggregates runs (not entered).

Components: Si, FN, SN, FN+SN waveguides (Fig. 3(a) loss ranges, author_estimate, wavelength not stated); low-loss
Si rib WG 0.8-1.05 dB/cm over 1460-1640 nm; escalators FN-SN, FN-FNSN, FN-Si (Fig. 3(c) read, < 0.1 dB text bound;
FN-Si reads 0.08-0.11 dB, slightly above the text bound below ~1520 nm); SiN 3-port splitter loss 0.07-0.15 dB over
runs 3-6 (Fig. 7(b) read); TE edge coupler ~2.5 dB/facet; TE GC ~2.8 dB at 1550 nm, 1-dB BW ~30 nm, 8 deg; TE/TM
edge coupler ~1.8 dB/facet (3.5 um MFD lensed fiber); PSR 0.2-0.9 dB, PDL < 0.45 dB; microdisk switch 1.0 dB IL, 16 dB
dynamic ER; microring filter < 0.2 dB, 1 nm/mW (-> 1000 pm/mW derived), FSR ~26 nm; microdisk modulator resonance
std 2.14 nm across the wafer (resonator.disk row, D396; modulator metrics left to the EO atlas); digital Ge PD > 1 A/W
at 1550 nm / -1 V, ~50 GHz.

Not entered: MZM / microdisk-modulator EO metrics (EO-atlas scope); analog MZM / PD SFDR > 90 dB/Hz^(2/3) (no
parameter); SiN splitter imbalance std ~0.7 % (registry gap R1); TE edge coupler 3-dB alignment tolerance 6.2 / 4.6 um
(registry gap R2); 13 deg GC 1-dB penalty (no parameter).

## dagostino2015: Zn-diffused low-loss passives in the COBRA InP generic process

Components: shallow undoped WG (FP array 0.3 TE / 0.4 TM; ring ER fits 0.34 / 0.44; Q fits 0.39 / 0.49 dB/cm);
shallow Zn-doped WG (2.0 / 2.2 dB/cm); deep undoped WG (1.4 / 2 dB/cm); 73 mm spiral ring (Q 1.2 million, ER 9.7 dB,
TE, 1510 nm); 2x2 MMI ring coupler (0.1 dB excess, r2 = 72 %, 11 x 512 um); 1x1 MMI mode filter (~0.3 dB per device
from up to 16 in cascade; 30 dB first-order suppression simulated).

Basis calls: Fabry-Perot losses rest on a calculated facet reflectivity (0.34 / 0.28) that the paper flags as the
uncertainty of the absolute value -> author_estimate; ring-fit losses rest on the assumed 0.4 dB coupler + filter loss
-> author_estimate (Q 1.2 million and ER stay measured). Locators use page + figure only (the extracted text drops
section numbers).

Not entered: simulated loss Table 1 (p.4); FSRs 8.2 / 11.9 / 24.1 pm (TE) listed against 25 / 55 / 73 mm in an order
that contradicts FSR ~ 1/L (D159 ambiguous assignment); diffusion depth / doping profiles (process data); 0.45 dB/cm
InP ring (cited, ref. 4).

## chen2026c: ultralow-loss Si3N4 platform for DV quantum photonics (IQA, arXiv v3)

Components: source microring (kappa_0 30.5 MHz and kappa_ex 132.3 MHz measured: over-coupled regime determined from
the data, so not D403; loaded ~160 MHz; FSR 199.97 GHz; R 114.5 um, 2 um x 800 nm, bus 1.4 um, gap 500 nm); 1x2 MMI
(0.053 dB); 2x2 MMI (0.052 dB, 48.0 % cross after normalization); MMI crossing (0.023 dB, from the 6-crossing unit);
inverse-taper edge coupler to UHNA-4 (~70 %, 1.55 dB/facet, 240 nm tip).

Not entered: no numeric propagation loss is reported in this paper (the 'ultralow-loss' claim cites refs. 24-25);
loss-budget component efficiencies (90 % on-chip, 80 % extraction, etc.: independently estimated, system level);
UMZI FSR (Fig. S3c shows ~400 GHz for 'a representative UMZI', p.17 calls the demux UMZIs 800-GHz-FSR: identity
ambiguous, D159); MZI heater (> 2 pi, no P_pi); simulated coupling ideality 0.995 and TE10 suppression > 15 dB;
film thickness 800-805 nm and CD std 0.010 um (process statistics, in component notes).

## roeloffzen2018 and worhoff2015: TriPleX overviews (LioniX)

Rule applied (judgment call, Q7): values entered only when their sentence carries no citation and the example is not
introduced with a citation (D80i / D408). roeloffzen2018: SDS HIC WG < 0.1 dB/cm (author_estimate), SDS SSC < 0.5
dB/facet, ADS < 0.1 dB/cm ('reproducibly measured'), heater P_pi ~300 mW (author_estimate), PZT stress-optic actuator
V_pi 18 V and 14.5 V with glass cover (two rows) + < 0.01 dB calculated loss, single-stripe ring Q ~700k + 0.07 dB/cm
(author_estimate from Q), stress-optic MZF > 30 dB / FSR 14.5 nm, zero-order AWG switch > 12 dB crosstalk / < 2 dB IL,
4-bit switched delay line (15-25 dB coupler suppression, < 0.4 ms, ~1.5 W), two-ring wavemeter FSR 43 nm, InP-TriPleX
butt interface ~1.8 dB measured / ~0.3 dB theoretical. worhoff2015: SDS SSC < 0.5 dB (per facet by the review's
definition), 600 um taper.

Not entered (cited, D80i / D259 / D408): single-stripe 0.03 / 0.007 / 0.001 / 0.0005 dB/cm, Vernier delay lines (ref.
34), RF filter (36), RAMZI interleaver (38), 8th-order filter and 1.4 dB/m (39), programmable mesh (41), MWP notch
filter (45), MRR-ECL lasers (48, 51-53), OBFN (24); worhoff2015: box-shell, SDS ORR, ADS 0.015 / 0.15 dB/cm (ref. 47
example), filled-box, ultra-high-Q rings (65-67), AWGs (68), MWP delay lines, OCT chips, Er DBR / DFB lasers (98-99),
WECSL (100), calibration module (21, 103). Generic '~1 dB fiber-to-TriPleX' claim (roeloffzen p.14) not entered
(spans two geometries and bands, no data).

## Missing organizations (not in organizations.csv / org_aliases.csv)

| name as printed | role | locator |
|---|---|---|
| International Quantum Academy (Shenzhen; with Shenzhen Futian SUSTech Institute for Quantum Technology and Engineering) | fab ('our CMOS foundry'; fabricating authors in the author contributions all at this affiliation) | chen2026c p.1 affiliation 1; p.8 Methods, Author contributions |
| NanoLab@TuE | facility ('provide the facilities for fabrication') | dagostino2015 p.15 Acknowledgments |
| Analog Photonics | PDK designer (not a fab role) | fahrenkopf2019 p.1, p.2 Sec. II-B |
| The MOSIS Service | MPW aggregator (not entered) | fahrenkopf2019 p.2 Sec. II-C |

## Registry gaps

| id | gap | skipped value + locator | proposed definition |
|---|---|---|---|
| R1 | percent power imbalance spread of a splitter | SiN 3-port splitter imbalance std ~0.7 % over 1530-1605 nm, 3 chips (fahrenkopf2019 p.4, Fig. 3(d)) | `imbalance_pct` (%, splitter): output power imbalance in percent as reported; statistic in `statistic` |
| R2 | 3-dB alignment tolerance | TE edge coupler 6.2 um horizontal / 4.6 um vertical (fahrenkopf2019 p.4, Fig. 3(e)) | `tol_3db_lateral_um` / `tol_3db_vertical_um` (um, couplers): misalignment for 3 dB excess loss, full or half width as printed in condition |
| R3 | 3-sigma statistic | yeh2024 Table 1 MRR / SPGC 3 sigma entered with empty statistic | statistic enum value `three_sigma` (or `std` with a multiplier column) |

## Questions for the coordinator

1. yeh2024 fab: org_tsmc assigned from the platform description (TSMC's 300 mm SOI wafer fabrication operation, p.1)
   plus thanks to TSMC's fabrication teams (D84b borderline). Keep, or empty under strict D80b?
2. yeh2024 Si rib WG 0.67 / 0.20 dB/cm entered as author_estimate (PDK value, no method) while SiN WG 0.21 / 0.14
   dB/cm and the SiN EC are measured ('yielded', 'is demonstrated'). Same basis for all PDK-paper values instead?
   Recommendation: keep the split (verb-based).
3. kramnik2024: Ayar Labs sponsored the GF MPW run (p.7). Under D398 an MPW access provider named for fabrication
   support is a fab org; a sponsor is not clearly one. Recommendation: not a fab org (note only, as entered).
4. kramnik2024 45SPCLO WG < 2 dB/cm (foundry-level figure, details under NDA): author_estimate with fab GF, or drop as
   a foundry specification not measured by the authors?
5. chen2026c fab: add International Quantum Academy to the registry and set it as fab_org_ids on all 5 rows (author
   contributions + 'our CMOS foundry' satisfy D80b / D83c)? Recommendation: yes.
6. dagostino2015: add NanoLab@TuE (facility, parent TU/e) and set facility_org_ids on all 6 rows? Recommendation: yes.
7. TriPleX overviews: fab empty (no fabrication sentence; all authors LioniX). The uncited-sentence rule leaves out the
   headline single-stripe 0.03 dB/cm (its paragraph introduces the stripe study with a citation in both papers).
   Confirm the rule, or enter 0.03 dB/cm as author_estimate with a D408 note?
8. fahrenkopf2019: the two edge couplers, the PSR and the microring filter have no stated guiding layer (the stack
   has Si plus two SiN layers): platform left empty (D422 / D423). The TE GC, microdisks and Ge PD keep `soi` (p.3:
   the patterned Si forms the couplers and the active devices). Confirm.
