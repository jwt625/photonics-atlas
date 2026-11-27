# Batch lit_303 report (distill subagent, 2026-11-27)

Dry-run `batch lit_303: +20 components, +83 metrics; errors 0`. ASCII only, no e-mail or postal addresses, no quotes
beyond a few words. Page-1 title checked for all 5 cached texts: each matches its source row (trocha2018 and suh2018
are the arXiv preprints of the Science papers: trocha2018 arXiv 1707.05969 v2, suh2018 arXiv 1705.06697 v3; values
from the preprint only, journal versions not read). None of the 5 papers had rows in `data/components/`. Builder:
session scratchpad `lit_303/build.py`.

## Per paper (components / metric rows)

- tan2022 (4 / 22): InP 32-channel OPA with non-uniformly spaced output waveguides.
  - `phase_shifter.other` reverse-biased p-i-n EO phase shifter, 3.5 mm (gagino2024 precedent): 2 pi at 5.84 V
    (MZI test structure, measured) and 5.9 V (simulated); about 0.2 mW per 2 pi (derived by the authors from
    < 0.035 mA at -6 V); length, width, etch depth, InGaAsP core 0.4 um.
  - `fiber_chip_coupler.edge` cleaved facet with 2 -> 4 um taper: about 3.8 dB per facet (lensed fiber, MFD 2.5 um,
    test structure).
  - `waveguide_platform.straight` deep-etched InP ridge: about 8.7 dB/cm (test structure), etch 4.7 um.
  - `free_space_emitter.other` OPA: 35 deg steering (measured, camera-limited), SLSR > 8.2 dB (-17.5 to 17.5 deg) and
    about 10 dB (-3 to 3 deg), divergence 0.46 deg FWHM and > 30 deg vertical, about 16.7 dB fiber to OPA output;
    simulated > 60 deg range, 0.46 deg, 10 dB SLSR; 32 channels; chip footprint.
  - Not entered: OPA power consumption 7.1 mW at 0 deg and < 7.5 mW at every angle (registry gap below); reverse
    current < 0.035 mA at -6 V (no parameter); "< 0.6 mW" per shifter in the intro (no phase range stated); beam
    resolution about 0.5 deg (no parameter); uniform-spacing comparison designs (hypothetical); Table 1 / Table 2
    values of other works; 1x32 MMI tree (no reported performance, no row).
- zhang2019f (11 / 41): UC Davis / Lockheed Martin Si OPA with SiN-assisted gratings. The PDF text layer is
  column-fragmented (text.md unreadable from p.2 on, although `garbled_text_layer` is false): all values read from
  the page renders (p.2-p.10) and a p.11 render made in the scratchpad.
  - `splitter.directional_coupler` crosstalk test structures, 5 mm: 1.3 um pitch > 12 dB (SEM width 502.4 nm, gap
    814.2 nm), 1.5 um pitch > 20 dB.
  - `splitter.mmi` 1x2 stage: 0.08 dB minimum excess loss (printed +/- 0.05 dB) at L = 16 um; SEM width 3.99 um;
    500 nm Si.
  - `waveguide_platform.transition` LOCOS vertical taper 500 -> 300 nm Si: < 0.1 dB per transition (cascaded
    structures).
  - `waveguide_platform.straight` fully etched Si: 2.6 dB/cm.
  - `fiber_chip_coupler.edge` 200 nm SiN coupler with vertical SiN-Si coupler: < 3 dB (measured) and 2.5 dB (loss
    breakdown term, author_estimate).
  - `phase_shifter.thermo_optic` Ti/Au 120 nm tuner: P_pi 11 mW (22 mW per 2 pi halved) at 1550.8 nm.
  - `reflector.other` thin-film a-Si/SiO2 DBRs on Si: 2-pair > 94 %, 1-pair > 82 % (1500-1600 nm, FTIR).
  - `free_space_emitter.grating_emitter` grating over DBR, row_kind design: about 95 % upward emission (FDTD).
  - `free_space_emitter.other` 24-element OPA, 1.3 um pitch: > 40 deg lateral steering, 3.3 deg axial over 20 nm,
    0.15 deg/nm, SLSR about 7 dB measured / about 13 dB and about 7 dB simulated, 13.7 dB estimated total loss,
    70 deg simulated sidelobe-limited range; 24 channels, pitch, 5 mm grating, 574 nm period (SEM), 60 nm etch,
    300 nm Si.
  - Not entered: grating emission rate 23 dB/cm (abstract about 20 dB/cm; registry gap); thermal crosstalk 5 % at
    38 um (no parameter); 46 % upward emission without DBR (simulated baseline of another stack); Fig. 6(a) taper
    SEM labels and the Fig. 9(a) 280 nm label (roles not stated, D156); simulated MMI excess-loss curve and FEM
    coupling-length curves; 0.6 dB etched-taper transition (cited ref. [13]); foundry PDK loss values (cited
    ref. [17]); 120-element 2.0 um pitch OPA (2D demo, geometry only, no row); loss-breakdown terms other than the
    coupler (in OPA notes).
- xiao2008 (2 / 10): NIST timing-jitter study of a purchased waveguide-type LiNbO3 Fabry-Perot optical frequency
  comb generator (OptoComb WTEC-01).
  - `laser.comb`: residual timing jitter (1 Hz-10 MHz) 94 / 20 fs (DFB seed, without / with servo) and 8.4 / 6.4 fs
    (fiber-laser seed), repetition rate about 10 GHz (one half-spectrum pulse train) and about 20 GHz (x = 0, both
    trains), output about -10 dBm, maximum transmission 30 % (about 5.2 dB, author_estimate: reproduces from the
    manufacturer R = 0.97 and calibrated eta).
  - `resonator.photonic_crystal` (Fabry-Perot subtype) cavity: effective finesse 60 and FSR 2.5 GHz (both
    author_estimate, origin not stated; the printed formula gives about 56 for the finesse).
  - Not entered: comb span about 40 nm (5 THz) and 2.44 dB/nm slope (comb span rejected in D81); phase noise
    -105 dBc/Hz at 1 Hz; calculated jitter contributions 0.4 fs / 177 fs (model estimates); measurement floor 3.9 fs;
    cavity frequency jitter 25 kHz; mode-spacing temperature slope about 0.02 MHz/deg; coating R = 0.97 (spec,
    reflectivity_pct not allowed for resonator); round-trip loss 0.208 dB (no cavity length, no per-length value).
- trocha2018 (1 / 5): KIT / EPFL dual-DKS-comb ranging (arXiv v2).
  - `laser.comb` pair of Si3N4 Damascene microring DKS combs: line spacings 95.646 GHz (signal) and 95.549 GHz (LO)
    as channel_spacing_ghz (printed as resonator FSR / line spacing, pulses not characterized, D83b); > 100 carriers
    per comb (about 115 usable, EDFA-limited); cross-section 1.65 um x 0.8 um.
  - Not entered: comb span about 11 THz (EDFA-limited, D81); ranging metrics (Allan deviation, 97.7 MHz rate,
    188 nm accuracy; system-level); Supplementary Information (not in the cached text); vision-figure parts (PWB,
    microlens, LIDAR PIC: concept only).
- suh2018 (2 / 5): Caltech counter-propagating soliton dual comb in one silica wedge disk (arXiv v3).
  - `resonator.disk` 7 mm wedge disk: unloaded Q about 3e8-5e8 (author_estimate, method not stated, D403), FSR
    9.36 GHz (stated as corresponding to the diameter, author_estimate), radius 3500 um derived.
  - `laser.comb`: repetition rate about 9.36 GHz (ESA), soliton pulse width 200 fs (sech^2 spectral fit, derived,
    D84c).
  - Not entered: repetition-rate difference tuning (up to about 20 kHz; no parameter); ranging precision 200 nm and
    26 km ambiguity range (system-level).

## Fab / facility orgs

- tan2022: fab empty (passive process steps, no named org, p.7 Sec. 3.1). Authors at HUST, Ori-Chip, Zhejiang
  University and CUST; no fabrication statement names any of them.
- zhang2019f: facility org_marvell_nanofabrication_laboratory + org_center_for_nano_micro_manufacturing (p.11
  Acknowledgments: fabrication utilized the facilities at both). Fab empty: "We fabricated our devices" (p.7 Sec. 3)
  with authors at UC Davis and Lockheed Martin, so the fabricating org is not unambiguous (D80b, D154). Coordinator
  may prefer org_university_of_california_davis (both named facilities are UC sites; fu2023 precedent had all
  authors at UC Davis).
- xiao2008: purchased device; vendor missing from the registry: "OptoComb" (product "WTEC-01"), p.2 Sec. 2 and
  ref. [10] (vendor web page); role fab (vendor of the device under test, rule 12). Fab left empty until the org
  exists.
- trocha2018: fab org_epfl, facility org_center_of_micronanotechnology ("Si3N4 devices were fabricated and grown in
  the Center of MicroNanoTechnology (CMi) at EPFL", p.8 Acknowledgments; lit precedents ji2022a, liu2020b).
- suh2018: fab org_caltech (author contributions "MGS fabricated devices", p.5; all authors Caltech). Facility
  org_kavli_nanoscience_institute is borderline: the p.5 Acknowledgments only "thank the Kavli Nanoscience
  Institute", no stated role (D80c); remove if the coordinator reads it as generic thanks.

## Judgment calls

1. tan2022 EO phase shifter as `phase_shifter.other`, not an EO-atlas modulator row (gagino2024 InP OPA precedent);
   tuning_power_mw 0.2 derived (the "about 0.2 mW" follows arithmetically from the measured current bound).
2. tan2022 MZI test-structure wavelength set to 1550 inferred (set-up laser 1.55 um); facet / waveguide test-structure
   losses likewise inferred; OPA rows use 1550 nm as stated for the OPA set-up.
3. zhang2019f crosstalk test structures classed `splitter.directional_coupler` (the paper names them directional
   coupler test structures; crosstalk_db allowed there).
4. zhang2019f MMI 0.08 dB entered as printed with L = 16 um although the Fig. 5(b) measured minimum sits at the
   16.5 um axis position (conflict in notes, D417 style).
5. zhang2019f LOCOS Si 500 -> 300 nm taper as `waveguide_platform.transition` (Si3N4 vertical-taper precedent,
   chrysostomidis2021) with core_thickness_nm 500 / layer2_thickness_nm 300 for its two ends.
6. zhang2019f thin-film DBRs as `reflector.other`, platform `other` (normal-incidence planar mirror samples, not a
   waveguide); kept in scope as chip-scale deposited stacks intended under the grating layer.
7. zhang2019f grating geometry (period 574 nm SEM, 60 nm etch, 300 nm Si, 5 mm length) placed on the OPA row, since
   the grating test structure itself has no allowed performance parameter (its only metric, 23 dB/cm, is a registry
   gap).
8. xiao2008 included under D411 as a fiber-pigtailed waveguide (chip-scale) device, not a bulk crystal; one row per
   class (comb + F-P cavity, D396); `resonator.photonic_crystal` because the subtype covers Fabry-Perot cavities.
9. xiao2008 30 % / 5.2 dB transmission is author_estimate: the printed value reproduces from the cavity formula with
   the manufacturer's R (specification input), and it excludes the fiber coupling the measurement would include.
10. trocha2018 one laser.comb row for the two same-design combs (signal / LO on separate chips) with the two spacings
    as conditions; no separate resonator rows (the FSR is the same number as the line spacing).

## Registry gaps (skipped value + locator + proposed definition)

- `power_consumption_w` for `free_space_emitter`: tan2022 OPA 7.1 mW at 0 deg (p.8 Sec. 3.2) and < 7.5 mW at each
  steering angle (p.11, Fig. 10(c)). Proposal: widen power_consumption_w to free_space_emitter ("electrical power of
  the steering actuators of an OPA at a stated beam angle").
- `emission_rate_db_per_cm` (new, free_space_emitter): zhang2019f weak SiN-assisted grating 23 dB/cm measured from
  loss vs grating length on a test structure (p.6 Sec. 2.3, Fig. 9(b)). Definition: "radiated-power decay per unit
  length of a waveguide grating emitter (fit of loss vs grating length)".
- Thermal crosstalk of phase shifters (fraction of the neighbour's phase shift): zhang2019f 5 % at 38 um (p.7,
  Fig. 11(b)). Candidate `thermal_crosstalk_pct` (phase_shifter, switch_fabric); single value, low priority.
- Reverse leakage current of a reverse-biased phase shifter: tan2022 < 0.035 mA at -6 V (p.8). Candidate: allow
  `dark_current_na`-like `leakage_current_ua` for phase_shifter (bias required); single value, low priority.
