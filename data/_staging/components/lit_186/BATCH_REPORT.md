# lit_186 batch report

Distilled 2026-11-18. 5 papers, 18 components, 108 metric rows. `merge_component_staging.py --dry-run`: 0 errors,
no warnings on this batch. All five cached copies are arXiv versions of the listed papers (page-1 titles match the
source rows): ji2022a arXiv v1 of the Communications Physics paper, xu2021d arXiv v1 of the Optics Express paper,
gu2021 arXiv v1 of the APL Photonics paper, dong2019 arXiv copy of the IEEE MEMS 2018 paper (the source row's DOI),
deotare2009 arXiv v2 of the Applied Physics Letters paper. The values are from those copies; the journal versions
were not read.

## lit:ji2022a (4 components, 23 metrics)

- Components: Euler-bend racetrack (p = 1), partial-Euler racetrack (p = 0.6), circular-bend racetrack (p = 0), all
  `resonator.ring`, `sin`; single-soliton comb in the Euler racetrack (`laser.comb`, D396 cross-note).
- Fab `org_epfl` (contributions p.8: J.L. and R.N.W. fabricated), facility `org_center_of_micronanotechnology`
  ("fabricated in the EPFL center of MicroNanoTechnology (CMi)", p.8); `process_name` "photonic Damascene reflow
  process (ref. 24)".
- Judgment calls:
  - kappa_0 most-probable values 15.5 / 34.5 MHz entered as `author_estimate` (D403): the fit (ref. 75 model)
    assigns kappa_0 / kappa_ex; no doublet or other regime-fixing data is shown. Fig. 2(a) total linewidth stays
    above kappa_0 over 1350-1630 nm, which is consistent with under-coupling; coordinator may upgrade to `measured` if
    that counts (ji2024 precedent needed a split doublet). Q0 about 13 M and 2.4 dB/m follow the same basis
    (dB/m converted to 0.024 dB/cm, D256a).
  - Circular-bend FSR 20.04 GHz kept as printed in Fig. 3(e) although p.6 says Dint could not be fitted for this
    device (D417 conflict note).
  - Geometry: fabricated 2.2 x 0.90 um rescaled to nm `derived` (D157); bus width = ring width (Supp. p.17);
    footprint 0.21 mm2 -> 210000 um2 on each racetrack row; circular-bend radius 30 um (Supp. p.14). Euler minimum
    radius for p = 1 / 0.6 not printed (plot only): not entered. Straight length L = 3500 um and span d = 60 um in
    notes (no parameter fits).
  - Comb: repetition rate 19.8 GHz `measured` (approx), soliton spectrum 3-dB width 16.3 nm `measured` (fit),
    pulse 156 fs `derived` (D84c).
- Not entered: dispersion D2 / D3 / D4 (no parameter, D81), AMX 90 % deviation intervals 25 / 930 MHz and the
  Supp. p.20 replicas (40 / 49.2 / 1100 / 1313 MHz), mode-interaction strength 25 MHz, soliton step 0.5 ms, SSB phase
  noise and quiet-point data, FDTD / FEM bend transmissions (no numbers printed), the circular-bend kappa_0 histogram
  (no printed value), loaded linewidths (no printed value).

## lit:xu2021d (3 components, 11 metrics)

- Components: oxide-clad (600 nm PECVD) x-cut TFLN ring R 80 um (`resonator.ring`, `lnoi_rib`), air-clad annealed
  ring of the second batch (`resonator.ring`), surface grating coupler (`fiber_chip_coupler.grating`).
- Fab `org_yale_university`: "We then fabricated the second batch of devices" (p.4), first person, all authors at
  Yale (D72); applied to both batches and the GC (same process). Cleanroom staff thanked by name without an org: no
  facility.
- Judgment calls: Q 2.0e5 at 1557.61 nm TE and Q about 1.0e6 (all air-clad devices) entered as `q_loaded`
  (unqualified). Air-clad ring: dimensions not restated for the second batch, so no geometry on that row; band
  `c_band` inferred. GC: pair transmission "tuned to 1.0 %" -> 10 % per facet `loopback_half` (authors' arithmetic,
  `derived`) and 20 dB `fiber_to_fiber` (`derived`); wavelength not stated (`c_band` inferred); grating design and
  etch not stated (platform from the chip's rib waveguide, noted).
- Not entered: PR characteristic time "10 ms scale", fitted PR rates (not printed), Fig. 5 PR frequency shifts vs
  intracavity power per process step (no parameter).

## lit:gu2021 (3 components, 20 metrics)

- Components: fabricated 1D topological photonic crystal (SSH-type) cavity in a 500 nm Si bus waveguide
  (`resonator.photonic_crystal`, `soi`); FDTD design variant (period 400 nm, 10 cells per side, `row_kind design`);
  2D air-hole grating coupler with 200 um taper (`fiber_chip_coupler.grating`, design center ~1575 nm only).
- Measured: Q 1950 at 1574.7 nm (`q_loaded`, unqualified), Fano extinction about 33 dB (detection-limited, approx),
  20.5 dB (+Delta) and 21 dB (-Delta) as `extinction_db` with the fiber-offset condition; geometry (390 nm period,
  20 cells per side, 500 nm / 220 nm / 2 um BOX, footprint 16 x 0.5 um2 -> 8 um2 derived).
- Judgment calls: the Fano ER is entered in `extinction_db` (resonator notch / contrast) with the lineshape in the
  condition; the GC row carries only the design-stated ~1575 nm center (`author_estimate`, D82a) and the taper
  geometry, since no coupler efficiency is reported.
- Not entered: stopband background over 90 nm (stopband_width_nm is reflector-only), slope ratios 10.78 / 10.07
  dB/nm, Fano asymmetry factors, mode volume 0.53 (lambda/n)^3, transfer-matrix spectra (assumed inputs), SEM hole
  diameters 154 / 94 nm (no hole-diameter parameter; in notes).
- Fab / facility orgs missing from the registry (fab left empty):
  - "Northwestern Polytechnical University" (p.1 affiliation; fab role, borderline D84b plus first-person "we
    fabricate", p.4; one of seven authors is at the Qian Xuesen Laboratory of Space Technology, China Academy of
    Space Technology, so the first-person statement alone does not name one org).
  - "Analytical & Testing Center of NPU" (p.5 acknowledgment: "for the assistances of device fabrication"; facility
    role, parent NPU).

## lit:dong2019 (2 components, 12 metrics)

- Components: Si3N4 ring R 119 um, 0.8 x 1.8 um2, in a released SiO2 membrane (`resonator.ring`, `sin`); PORT AlN
  piezo actuator (`phase_shifter.other`, liu2020a precedent), D396 cross-notes.
- Ring: Q 64,000 loaded (abstract, across the tuning range), Q 68,022 released and 360,100 before release (Fig. 3
  labels; wavelengths read from the axes, inferred), 3-dB bandwidth 25 pm in `linewidth_pm`, design FSR 187 GHz
  `author_estimate` (stated as the comb wafer repetition rate), radius / thickness / width (width from the Fig. 2
  label, `derived`).
- Actuator: 0.33 pm/V TM (20 pm / 60 V, `derived`), about 0.12 pm/V TE read off Fig. 5 (`extracted_from_figure`),
  tuning power <= 30 nW (`tuning_power_mw` 3e-5, `le`, `derived`), membrane mode 1.1 MHz -> 1100 kHz (`derived`).
- Judgment calls: `tuning_power_mw` used for the piezo DC leakage power (registry allows it on phase_shifter;
  liu2020a did not enter its < 300 nW, so the coordinator may prefer notes for consistency). Released vs unreleased Q
  kept as conditions on one ring row (the paper does not say the unreleased trace is the same ring).
- Fab empty: passive fabrication sentences; Si3N4 wafer process cited to refs. [7] (Damascene) and [8] (LIGENTEC
  technology page); acknowledgment is a DARPA program (D80c). No facility.
- Not entered: simulated 55 nm displacement / 1 nm radius change, mechanical Q 100, "tuning speed < 1 us" (potential,
  not measured), "2pm/3nW" (no parameter), TE vs TM Q difference beyond printed values, electrode geometry labels.

## lit:deotare2009 (6 components, 42 metrics)

- Components: one `resonator.photonic_crystal` row per cavity length s = 116, 126, 136, 146, 156, 176 nm of the
  suspended Si nanobeam series (`soi`, air-bridge precedent asano2017 / ashida2017).
- Fab `org_harvard_university` ("We fabricated a range of structures", p.2, all authors Harvard) and facility
  `org_center_for_nanoscale_systems` ("Device fabrication was performed at the Center for Nanoscale Systems at
  Harvard", p.3; D448).
- s = 146: Q 750,000 at 1561.13 nm and 2.1 pm linewidth (`measured`), simulated Q 1.4e7 at 1560 nm (Fig. 3(b)
  simulation peaks at s = 146) and simulated second-order-mode Q 120,000 (wavelength not stated, `band
  unspecified`). Other s: released Q and resonance wavelength read off Fig. 3(b,c) (`extracted_from_figure`, about
  +/- 20 % on the log axis, +/- 1 nm); on-substrate (before release) Q 18,000 / 27,500 / 17,000 for s = 136 / 156 /
  176 from the Fig. 4 caption with wavelengths read off the Fig. 4 axis. Shared design geometry (220 nm, 500 nm,
  pitch 330-430 nm, 2 um BOX) on every row.
- Judgment calls:
  - Measured Q stored as `q_intrinsic` `measured`: the paper states the resonant-scattering method measures the
    intrinsic Q without coupling-waveguide loading (p.2); no regime extraction (D403 not triggered). Coordinator may
    prefer `q_loaded` (liu2022a stored a similar unqualified nanobeam Q as q_loaded).
  - On-substrate values kept as conditions on the same-s rows; whether they come from the -3 % scaled set is not
    stated (noted on every row).
  - Simulated per-s Q values (Fig. 3(b) red curve) not read; only the printed optimum entered.
- Not entered: mode volumes 0.39 / 0.71 (lambda/n)^3 (no parameter), photonic bandgap 1200-1700 nm (stopband_width_nm
  is reflector-only), hole radius r = 0.28a (no parameter).

## Registry gaps (with skipped values)

- `stopband_width_nm` on `resonator`: gu2021 stopband background over 90 nm (p.4), deotare2009 1D bandgap
  1200-1700 nm (p.1 Fig. 1 caption). Proposed: allow stopband_width_nm for resonator.photonic_crystal (mirror stopband
  of the cavity, level in condition).
- `mode_volume_lambda_n3` (resonator): deotare2009 0.39 / 0.71 (lambda/n)^3 simulated (p.1), gu2021 0.53 simulated
  (p.3). Proposed: mode volume in units of (lambda/n)^3, basis usually simulated.
- `hole_diameter_nm` (resonator, reflector): gu2021 SEM-measured 154 / 94 nm (p.4). Proposed: air-hole diameter of a
  photonic-crystal cell (role in condition).
- `mech_q` (phase_shifter): dong2019 mechanical Q 100 in air (p.3); already a registry candidate (D438).
- Dispersion (D2 / D3 / D4) for ji2022a stays out (D81 rejection stands).
