# Batch lit_13 report (distill subagent, 2026-10-29)

Dry-run `batch lit_13: +29 components, +160 metrics; errors 0`. ASCII only, no e-mail, no personal identifiers, no quotes
(only vandekerckhove2025 is open_license_ok; none used). Builder: session scratchpad `distill_lit_13/build.py` + `p_<paper>.py`.

## Per paper (components / metrics)

- cai2021 (4 / 22): Er:LNOI Z-cut ridge spiral amplifier 2.58 cm (internal net gain 16.0 dB / 6.20 dB/cm at 1531.6 nm and
  2.66 dB at 1550 nm, derived per D166; 0-dB-net-gain "saturation" -8.84 / -22.47 dBm as psat_in_dbm with the paper's
  definition in condition; NF 4.49 / ~6 / 8 dB derived; SEM-annotated 600 / 410 / 190 nm geometry), Er:LNOI waveguide
  (cutback total loss 4.63 / 3.08 dB/cm measured; ~2.5 dB/cm background author_estimate), microring (Q-analysis loss
  4.20 / 3.1 dB/cm, author_estimate: Q and ng not printed), FIB facet 7.2 dB/facet (D167). Not entered: signal enhancement
  27.94 / 10.61 dB, PCE 4.59 dB/mW (no parameter), calculated Er absorption 1.78 / 0.56 dB/cm, lifetime 2.3 ms, Table 1
  2.8 cm row (own OECC paper, ref. 35, D259), 1.38 / 1.94 / 2.8 cm siblings (curves only). Fab empty (passive, D80b);
  facility org_center_for_advanced_electronic_materials_and_devices (p.7). Pump printed 17.34 vs 17.31 mW (noted).
- qiu2025 (3 / 14): p.1 garbled layer = figure area; Fig. 1 read from the render. Er-implanted Si3N4 30 cm amplifier
  (180.8 / 241 mW output converted to 22.57 / 23.82 dBm, derived; 13.5 dB off-chip / 16 dB on-chip small-signal gain,
  peak wavelength not stated -> band unspecified; > 8 dB over 1556-1575 nm at 10 dBm in; 28.4% on-chip conversion
  efficiency derived), background loss 10 dB/m at 1275 nm by OFDR (0.1 dB/cm derived), inverse-taper edge coupler 75% per
  facet (dummy waveguide, measured). Prior-work 72 / 144 mW not entered. Facility CMi + HZDR (see decisions).
- starnault2024 (3 / 16): commercial packaged QD SOA (Innolume, D72 vendor), QW SOA and bulk SOA (InPhenix, missing org):
  Table I small-signal gain, 3-dB input / output saturation (psat_*, 3-dB noted), NF at -5 dBm / 1302 nm, 3-dB gain
  bandwidth; QD NF < 5.5 dB at -9 dBm. Peak-gain wavelengths not printed -> o_band inferred. Not entered: PDFA (fiber
  amplifier, out of scope D80f), GRT, alpha factor, QD PDG 7 dB (no parameters), TFLN MZM / DFB setup equipment.
- abe2025 (1 / 5): polarization-diversity PPLN OPA wavelength converter (C/L <-> U band) as amplifier.parametric: Tx
  conversion gain 10 dB / NF ~6 dB (1624.23-1675.99 nm), Rx gain > 13 dB / NF ~5 dB, beyond-U-band NF 6-8 dB
  (1675.99-1719.24 nm). Not entered: gain flatness <= 3 dB, ~16 dBm input power tolerance (sentence cites [26]; not a
  saturation definition), transmission results (system). Fab empty (own development stated, no fabricator, D80b).
- umeki2010 (2 / 15): direct-bonded PPZnLN-on-LiTaO3 ridge waveguide (loss <= 0.3 dB/cm author_estimate, near-field MFD
  5.3 x 6.6 um at 1560 nm and 5.0 x 6.4 um at 780 nm, 5 x 4 um ridge, 80 deg sidewall SEM) and the fiber-pigtailed DFG
  module (2200 %/W SHG at 1583.4 nm, 4 dB fiber-to-fiber IL over 20-60 C and over 1550-1610 nm, poling 17 um design). Fab
  org_ntt (authors state they fabricated it; single org). Not entered (D259 / D259a): 2400 %/W, 0.2 nm FWHM, 148 mW / 92% (Figs. 4 and 8,
  reproduced from own ref. [20]; headline of the abstract); +8 / +9 / +4 dB conversion and parametric gains (no
  frequency_converter parameter).
- vandekerckhove2025 (2 / 16): transfer-printed PPLN on SiN SHG waveguides, in-house (2500 %/W/cm2 at 1620 nm; fab
  org_ghent_university) and imec foundry (1000 %/W/cm2 at 1560 nm; fab org_imec;org_ghent_university, niels2026
  precedent), simulated ~3000 %/W/cm2, poling 3.5 um, SiN / LN 300 nm, interaction 0.9 mm; 0.18 nm/K -> 180 pm/K derived
  on the foundry row. Not entered: 3-dB phase-matching bandwidths 15 / 8 nm (no parameter), SPDC CAR / PCR (D250),
  roughness, simulated sensitivities, trimming range 1520-1590 nm, angled-transition IL (simulated curves only).
- wang2026b (7 / 28): triple-resonant PPLN double-pulley MRR for SFG QFC (intrinsic / loaded Q at signal, pump, SF;
  386,000 %/W derived; on-chip QE 57% and Q-derived max ~70% in power_conversion_efficiency_pct; 600 / 420 nm, ring width
  1.73 um), signal / pump DC combiner (98% / 1.2% cross, geometry), DFB-to-TFLN butt coupling ~20%, DFB laser 85.5 pm/K,
  lensed-fiber edge ~30% (loopback_half), abrupt SF taper 0.24 dB and Euler bend 0.01 dB (simulated, fabricated rows,
  D80e). Not entered: ring radius 74 um, coupler gaps 700 / 390 nm, bus widths 600 / 300 nm (not allowed for
  frequency_converter), noise ~7k cps, simulated kappa^2, design 73%. Fab empty (passive; three USTC-linked units).
- liu2023 (2 / 15): polarization-independent Ce:YIG-on-Si MO isolator (isolation 20 dB TE at 1577.1 nm / 12 dB TM at
  1576.3 nm, IL 4.6 / 8.2 dB de_embedded vs S-bend reference (derived), 10-dB isolation bandwidths 0.35 / 0.45 nm,
  theoretical 17.3 / 4.0 and 12.3 / 10.0 dB simulated), MO junction 0.2 / 1.5 dB per edge (author_estimate, design
  section). Not entered: FSR ~2 / ~6 nm (fsr not allowed for nonreciprocal), NRPS 5.2 rad/mm, 3 dB coupler SEM widths
  (no metric). Fab empty (D80b).
- pintus2019 (5 / 29): TE MZI circulators (FSR 10.7 nm: 30 dB best near 1555 nm, > 18 dB over C band, IL 18-21 dB;
  broadband Delta L0 1 um: > 18 dB at 1560 nm, IL 14-18 dB, > 14 nm with IR(BW) >= 15 dB), adiabatic 50/50 coupler
  (~50% +/- < 3% over 1460-1560 nm, simulated 45-55%, 2.2 dB breakdown term, Table I geometry), TE-TM rotator (PER > 17 dB,
  IL 2.0 dB and 0.5-3 dB author_estimate), Ce:YIG/Si waveguide (~30 dB/cm at 1550, 44 -> 16 dB/cm 1520-1580,
  author_estimate on a cited 0.6 dB/facet; 8.6 dB/cm and ng 3.2 simulated). Not entered: electromagnet drive (50 mA,
  10 mA / 30 ohm / 3 mW; no nonreciprocal power parameter), cited 0.6 dB facet, 6 dB projection. Fab / facility empty.

## Organizations missing from the registry

- InPhenix Inc. (starnault2024 p.3 Sec. III): vendor of the purchased QW and bulk SOAs (D72 fab role, left empty).
- Instrumental analysis center of Shanghai Jiao Tong University (cai2021 p.7 acknowledgment): XPS / SIMS of the wafer
  only; not needed for these rows.

## Judgment calls for the coordinator

1. abe2025 classed amplifier.parametric (gain / NF), umeki2010 module frequency_converter.sfg_dfg (%/W, IL) although
   both are NTT PPLN wavelength converters; a frequency_converter conversion-gain parameter would unify them.
2. wang2026b on-chip QE 57% (photon-number efficiency) stored in power_conversion_efficiency_pct with the definition in
   condition.
3. qiu2025 HZDR in facility_org_ids (implantation performed at HZDR; samples fabricated in CMi and at HZDR, p.2), not fab.
4. vandekerckhove2025 0.18 nm/K put on the foundry row by wavelength (Fig. 5(d) ~1565 nm vs in-house 1620 nm); D159
   would drop it if judged ambiguous.
5. umeki2010 headline 2400 %/W excluded under D259a (Fig. 4 / Fig. 8 captions cite ref. [20]); the pigtailed 2200 %/W
   kept.
6. cai2021 / starnault2024 "saturation power" entered with the source definitions (0-dB net gain point; 3-dB compression).

## Registry gaps (values skipped)

- amplifier `signal_enhancement_db` (pump on / off contrast): cai2021 27.94 dB at 1531.6 nm, 10.61 dB at 1550 nm (p.3-4).
- amplifier `gain_efficiency_db_per_mw` (net gain per launched pump power): cai2021 4.59 dB/mW (p.5).
- amplifier `gain_recovery_time_ps` (10-90% pump-probe): starnault2024 93.4 / 182.9 / 192.0 ps (p.4 Table I).
- amplifier `alpha_factor` (linewidth enhancement, range): starnault2024 0.86-1.2 / 4.0-4.55 / 3.8-4.3 (p.4 Table I, p.5).
- `pdl_db` for amplifier (polarization-dependent gain): starnault2024 QD SOA 7 dB (p.5).
- amplifier `gain_flatness_db` (max - min gain over the band): abe2025 <= 3 dB (p.2).
- frequency_converter `conversion_gain_db` (signal-to-idler, internal / fiber-to-fiber in condition): umeki2010 +8 dB
  internal, +4 dB external, +9 dB signal parametric gain (p.6-7); would also host abe2025.
- `bw_3db_nm` for frequency_converter (phase-matching 3-dB width): vandekerckhove2025 15 / 8 nm (p.4).
- `radius_um`, `gap_nm`, `bus_width_nm` for frequency_converter (resonant converters): wang2026b 74 um, 700 / 390 nm,
  600 / 300 nm (p.7).
- frequency_converter `noise_count_rate_hz` (QFC output noise, on-chip): wang2026b ~7000 cps (p.11).
- `fsr_nm` for nonreciprocal (interferometric isolators): liu2023 ~2 / ~6 nm (p.4).
- `power_consumption_w` for nonreciprocal (electromagnet drive): pintus2019 3 mW at 10 mA (p.8).
- `output_power_mw` for amplifier (printed mW, now converted to dBm): qiu2025 180.8 / 241 mW (p.2); convenience only.
