# Batch lit_63 report (distill subagent, 2026-11-02)

Dry-run `batch lit_63: +25 components, +157 metrics; errors 0` (one WARN about another batch's row,
cmp_lit_ni2025b_pimmwc-m18). All six sources are `restricted_local_only`: facts and locators only. ASCII only; no e-mail,
street or postal text. No `garbled_text_layer`, no correction / erratum, no paper stopped on. Rows built by a scratchpad
script from one spec. Renders checked: stern2018 p.9; hamaguchi2018 pp.6-7; song2025 pp.4-5; hiratani2024 pp.3, 5, 6;
szelag2017 p.4.

## Document identity

- stern2018: cached text is the arXiv version, titled "Fully integrated ultra-low power Kerr comb generation"; source row
  title "Battery-operated integrated frequency comb generator" (DOI 10.1038/s41586-018-0598-9, arXiv id 1804.00357 on the
  same source.json). Same work: integrated III-V / Si3N4 Kerr soliton comb, 98 mW electrical power from a AAA battery; the
  five authors on page 1 match the DOI metadata count (`n_authors_meta` 5, lit_h20; the source row holds no author names, so
  names were not compared). Distilled from the arXiv text only; journal values may differ and were not consulted.
- qiu2026: cached text is arXiv v1, titled "...lasers based on a Mamyshev oscillator"; source row "...laser using a Mamyshev
  oscillator" (Nature 2026). Same work; arXiv values only. Values carry the v1 numbers (e.g. 175.5 MHz).
- szelag2017: the source row title is garbled ("220 mm", "silionn photonlcsplotform"); page 1 prints "200 mm ... silicon
  photonics platform". Same paper; registry title worth correcting.

## Per paper (components / metrics)

- qiu2026 (5 / 31): Mamyshev MLL laser.comb (off-chip 136 / 138 mW, on-chip 182 / 184 mW derived, pump-to-output 27.5 %,
  175.5 MHz, AC FWHM 187 / 147 fs, simulated 90 / 130 fs, jitter 59.1 fs, comb-line linewidth 31.4 kHz Lorentzian, 174 kHz at
  10 ms); WBG pair reflector.bragg (3 dB ~5 nm, 950 periods); UHNA7 edge coupler (2.52 dB fiber-to-fiber, 1.26 dB
  loopback_half, 1.45 dB simulated, taper / fiber geometry; test_structure, 2 cm dummy); Er waveguide straight (OFDR 9.5 and
  165 dB/m as dB/cm, geometry); lensed-fiber coupling of the supercontinuum chip (2.5 dB author_estimate).
- stern2018 (8 / 41): dual-cavity comb laser.comb (9.5 mW on-chip, > 60 dB, 49 mA, 52 mW/A, 3.4 %, 40 kHz, operating points
  78 / 98 / 130 / 277 mW electrical); modular comb (4.9 mW, 1582 nm, > 60 dB, 162 mW); Vernier rings R 20 / 22 um as
  resonator.ring (D400); R 120 um microresonator resonator.ring (Q 8e6, 32 MHz, geometry) + reflector.other (40 %, D396);
  Sagnac mirror (about 20 %); RSOA coupler chip_chip_coupler.butt (2 dB measured, < 1 dB simulated, 280 nm).
- hamaguchi2018 (3 / 10): GaN VCSEL current injection 6 um (40 mA, 1.27 nm mode spacing, ~454.7 nm figure, 28.3 um, 4 sigma
  spot 2.892 um simulated) and 8 um (70 mA); optically pumped 49.8 um (0.2 mW, ~441 nm figure, 0.7 nm calculated).
- song2025 (1 / 38): 1.5 mm DFB: 424 / 368 / 517 mW, 40 mA, 0.329 / 0.349 W/A, 1.69 ohm, SMSR, peak wavelength from Fig. 5,
  10 x 20 deg, Table 2 linewidths (9), Lorentzian 50 kHz, Table 3 RIN (5) + -166 dB/Hz over temperature, relaxation 2.38 / 5.13
  GHz, geometry, kappa 6 /cm from kappa L.
- hiratani2024 (6 / 21): tunable laser with Si slab (11.3 mW, 39 mA, 56 nm, > 53 / 57 dB, < 60 / 39 kHz); three Fabry-Perot
  rows (Si slab, conventional, aging) with Figs 2 and 8 readings; front / rear loop mirrors (design 30 %, > 90 %).
- szelag2017 (2 / 16): DFB family DFB_A-G (50 dB, 1300 nm, 0.15 / 0.4 mW fiber, 1.5 / 4 mW in waveguide, 50-65 mA, ~10 ohm,
  geometry); output grating coupler (~10 dB at 1300 nm, peak 1320 nm).

## Values not entered and why

- qiu2026: Table S1 and refs (other works). Table S2 simulation inputs (10 dB/m, ng 2.0023, gamma, cross-sections, Delta n).
  Linear-cavity FSR 175.5 MHz, same number as the repetition rate (p.3). 0.62 dB splice loss and < 0.2 dB dummy-waveguide
  propagation are in `includes` (setup splices, unspecified split; rule 13). Supercontinuum spiral: geometry only, 736-2331 nm,
  279 THz, -20 dB 18.7 THz, assumed 5 dB/m: no row.
- stern2018: comb span and SNR (D81 comb span); filter tuning of Fig. 2(a) (no laser tuning range stated); RSOA 93 %
  reflection (purchased part, in core_material).
- hamaguchi2018: 3.2 nm / 36.5 nm emission widths (resolution-limited, D250; no lasing in cavity (1)); roughness; family
  wavelength 441-455 nm stated once (D254, notes only; two rows carry their own figure readings).
- song2025: Table 1 other works (rule 3); turn-on voltage 0.8 V (forward_voltage_v needs a current); 0.005 nm/mA static tuning
  (D83g); linewidth-power product; FP test lasers (see gaps).
- hiratani2024: ref. [24] device numbers (rule 3); confinement ratios (calculated, no parameter); Fig. 12 per-wavelength
  linewidth points; Fig. 11 peak level (labelled light intensity, OSA level, not an output power statement).
- szelag2017: contact resistivities (TLM, no parameter); per-device Fig. 14 bars (text range entered, reading in notes).

## Missing fab / facility orgs (registries checked)

- Sony Corporation (hamaguchi2018 p.1 affiliation, p.9 author contributions name the fabricators): not in `organizations.csv` /
  `org_aliases.csv` (only Sony Semiconductor Manufacturing / Solutions). fab_org_ids left empty on 3 rows; add the org, then
  fab = Sony Corporation.
- Ion Beam Center of HZDR (qiu2026 p.8): no separate org; the parent is in the registry and entered as fab for the implantation.

## Registry gaps (skipped value + locator + proposed definition)

- `pulse_energy_pj` (laser): qiu2026 p.4 on-chip 1.04 / 1.05 nJ and 397 / 347 pJ. Energy per pulse at the stated plane. This is
  the paper's headline metric.
- `threshold_current_density_ka_per_cm2` (laser): hamaguchi2018 p.1, p.4, 139 / 141 kA/cm2. Threshold current per aperture
  area. The text pairing is inconsistent (below).
- `rep_rate_linewidth_hz`, `ssb_phase_noise_dbc_per_hz` (laser): qiu2026 p.5, 0.012 mHz RF beatnote Lorentzian and -134 dBc/Hz at
  10 kHz. Kept out of `linewidth_hz` on purpose: an RF value would sit at 1e-5 Hz among optical linewidths.
- `center_wavelength_nm` for reflector, plus a filter offset: qiu2026 p.4, near 1557 nm, 8.9 nm separation.
- `mirror_radius_of_curvature_um` (laser): hamaguchi2018 p.5 74 um, lenslets 37.7-56.6 um p.3 (`lens_radius_um` is micro_optics).
- `internal_loss_per_cm`, `internal_quantum_efficiency_pct` (laser): song2025 p.3, 6.8 /cm and 86 % from FP cavity-length series.
- Lesser: comb / supercontinuum span (D81 deferred; qiu2026 p.4, p.6; stern2018 p.3-4); linewidth-power product (song2025 p.2,
  p.6); specific contact resistivity (szelag2017 p.2).

## Judgment calls for the auditor

1. qiu2026 fab = EPFL + HZDR on doped rows (contributions name an HZDR author for the implantation, D80b / D83c); EPFL only on
   masked WBG and edge coupler rows. Facility = CMi; HZDR is not also a facility.
2. qiu2026 27.5 % in `pump_to_comb_efficiency_pct` as derived; the planes of the ratio are not printed. The off-chip powers give
   15.4 %, on-chip outputs over off-chip pumps 20.6 %, so the printed value implies on-chip pump power; not entered as such.
3. qiu2026 lensed-fiber 2.5 dB as `fiber_chip_coupler.edge`, per_coupler: coupler not described on that chip. Supp. S3 A swaps
   the pump labels against the main text (959 mW Pump 1 on p.4, "959 mW pump 2" on p.20); the total is unaffected.
4. stern2018 rows use one laser.comb row per design with lasing and comb points as conditions (no separate laser.tunable row).
   Inferred wavelength 1580 nm on microresonator and linewidth values, `cl_band` on the coupler (rule 8, reason in notes).
5. stern2018 q_intrinsic author_estimate (D403). The caption ties Q 8e6 to the 32 MHz bandwidth; 32 MHz near 1580 nm would be a
   loaded Q nearer 6e6, so the two numbers are not the same quantity; 32 MHz is entered as printed.
6. hamaguchi2018 Jth: p.4 prints 40 / 70 mA with 139 / 141 kA/cm2, while abstract pairs 40 mA with 141; aperture area gives 141
   for 6 um and 139 for 8 um, so p.4 order looks reversed. Not entered either way (gap).
7. hamaguchi2018 mfd_chip_um 2.892 = 4 x theoretical sigma (paper's 4 sigma definition), basis simulated; 1/e^2 equivalence is
   not asserted by the paper beyond that definition.
8. song2025: Table 3 and p.6-7 call 171.64 mW fiber output while Table 2 lists the same power for the unpackaged measurement;
   powers remain in `condition`, not as separate rows. Beam axes 10 / 20 assigned from Fig. 6 curve widths. ref_plane `chip` on
   L-I rows from the AlN-carrier mounting (lu2024 precedent). kappa 6 /cm is author_estimate from kappa L around 0.9 / 0.15 cm.
9. hiratani2024: figure readings for Fabry-Perot rows have no text value; text only confirms the 1.4 ratio (11.3 / 7.6 = 1.49 as
   read). The reflector rows are design only. Fab empty: passive voice, three author orgs.
10. szelag2017: one row for seven devices (no design difference stated, D165); subtype laser.heterogeneous (vaskasi2022,
    ramirez2022 precedents). Fab empty under D84a though the paper names the CEA LETI platform as the process and Fig. 11 carries
    its logo; the closest call in this batch. Grating coupler method `unspecified`; "per grating" taken as per_coupler.
