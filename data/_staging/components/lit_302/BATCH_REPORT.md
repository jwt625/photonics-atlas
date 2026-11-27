# lit_302 batch report

Distilled 2026-11-27 under the pic-component-distill skill (Contracts v4-v7, DevLog-007 rulings). Validation:
`merge_component_staging.py data/_staging/components/lit_302 --dry-run` -> +20 components, +110 metrics, 0 errors.
Page-1 titles of all five cached texts match their source rows; none is a correction / erratum.

| paper | components | metric rows |
|---|---|---|
| li2019a | 4 | 22 |
| mehta2020 | 3 | 21 |
| skipper2025 | 5 | 18 |
| wang2021c | 6 | 45 |
| newman2019 | 2 | 4 |
| total | 20 | 110 |

## lit:li2019a (Optics Express 2019, lens-based 2D beam steering, SiN)

Rows: `beam_steerer_4x4` (free_space_emitter.other: FOV 2.07 / 4.12 deg, divergence 0.06 deg mean of 16, 16
channels, 250 / 125 um pitch), `grating_emitter` (divergence 10.5 / 9.3 deg, near-field diameter 10 um measured,
8 / 6 um simulated, 1.2 um pitch, emission angles 10 / 9 / 8 deg at 1540 / 1550 / 1560 nm as author_estimate),
`switch_1x16` (switch_fabric.other per D158: 27.1 us 10-90 % rise, 0.5 dB per 1x2 stage author_estimate, background
suppression 18 dB mean and > 20 dB near field as crosstalk_db, 16 outputs), `ti_heater_ps` (88.8 mW/pi, 1 mm).

Not entered: emitter size "approximately 10 x 8 um2" (axes not assigned to length / width); theoretical divergence
0.056 deg (calculation); Table 1 FOV 2.16 x 4.29 deg (conflicts with the text 2.07 x 4.12 deg, D417, text kept);
spot-position stability within 0.03 deg over 1550-1580 nm (no parameter); femtosecond-pulse bandwidths / widths /
pulse energies (estimates, p.12); simulated waveguide dispersion -720 ps/(nm km) (dispersion not in the registry,
D81 / D250); expected > 20 dB switch extinction "using optimized fabrication" (expectation); defocus shift 716 um
(computed). Input grating coupler: no value, not a row. Fig. 5(d) markers suggest x above y while the text gives
y 10.5 / x 9.3 deg (D417, text kept, noted).

Orgs: fab empty on all rows ("manufactured on a silicon-nitride platform", passive, D80b). No facility named.

Judgment calls: (1) the system row includes an off-the-shelf bulk glass lens (Thorlabs LA1116); kept in scope like
cmp_lit_chang2020_beam_steerer_4x4 (D411 targets polished crystalline parts; the lens defines the divergence and FOV).
Coordinator may prefer to drop the system row. (2) Background suppression (far field 18 dB, near field > 20 dB) put on
the switch row as crosstalk_db, since the paper attributes it to the 1x2 switch extinction; slsr_db on the system row
was the alternative.

## lit:mehta2020 (arXiv v2 2002.02258 of the Nature 2020 paper; values from the preprint only)

Rows: `fiber_edge_coupler` (fiber_chip_coupler.edge: 1.4 dB at 729 nm room temperature and 2.4 dB at 7 K
loopback_half, Fig. 6(b) range 1.37-2.3 dB over 730-890 nm extracted_from_figure, 1 dB simulated mode overlap with a
5.4 um MFD mode, 8 channels, 127 um pitch specification, 700 nm width, 25 nm core, 2.7 um BOX), `sin_wg_thick`
(2 dB/cm at 729 nm cutback, power handling > 24.77 dBm derived from 300 mW, 450 nm width, 25 + 170 nm layers, 2.7 um
BOX, 3.5 um cladding), `grating_emitter_729` (beam waist 6.5 / 3.7 um measured, emission angle 36 deg
author_estimate, designed radiation efficiency 50 % simulated, 300 nm period).

Not entered: -60 dB inter-zone crosstalk at the ion (chip-level, attributed to waveguide-waveguide coupling; no
parameter for free_space_emitter / waveguide_platform); loss-budget terms 3 dB grating emission and 1 dB waveguide
(duplicates of the 50 % design and 2 dB/cm); total input-to-ion loss 6.4 dB (system budget); wavelength-dependent loss
729-920 nm (no values); ring Q (no values); 0.2 deg emission-angle change on cooling (estimate); designed ~3 um
waists; 23 um label in Fig. 2(c) (span ambiguous); adiabatic thin-to-thick taper (~1 mm, no loss value; not a row).
All ion-trap metrics (fidelity, heating rate, Rabi frequencies) out of scope.

Orgs: fab org_lionix_international on all rows ("Fabrication was performed by LioniX International", p.6, and the
acknowledgment). org_eth_zurich added on the fibre edge-coupler row only: facet polishing and fibre-array attach by
the authors ("We have performed three attachments", p.7; author contributions), all authors at ETH Zurich (Contract
v7 assembly step). No facility: the ETH FIRST cleanroom staff thanks do not set a facility (D72, D84b). OZ Optics
(V-groove array vendor), Nufern S630-HP fibre and EPO-TEK epoxies are notes only (supply scan territory).

Judgment calls: (1) 7 K value scope loopback_half with method unspecified (the cryogenic path is not described
separately; the room-temperature value is explicitly loop-derived). (2) Beam waists entered at 730 nm (Methods: 730 nm
diode laser for profiling; caption says 729 nm beam). (3) process_name left empty: TriPleX appears only in the title of
cited ref. 14, not as the stated process.

## lit:skipper2025 (Optical Materials Express 2025, selective-area MBE for in-pocket QD lasers on AIM wafers)

Rows: `qd_laser_selective` (threshold 205 mA best at 20 C, 240 mA spectrum device, ground state ~1300 nm, 6 um ridge,
3 mm), `qd_laser_standard` (360 mA, ~1300 nm, 6 um, 3 mm), `laser_sin_coupling_selective` / `_standard`
(waveguide_platform.transition, platform other as koscica2025: 9.07 / 12.05 dB measured, 7.17 / 8.80 dB simulated at
1310 nm, final gaps ~6 / ~10 um from the Fig. 3(c)(e) labels, growth-limited minimum gaps 2.9 / 5.2 um),
`ring_filtered_laser` (laser.other: fibre-coupled peak 1206 nm at 800 mA).

Not entered: output powers "typical over 10 mW at 1 A, best over 16 mW" (stated for both growths together; curves of
both growths pass 16 mW in Fig. 4(a): D254 / D159); threshold current density 1.14 kA/cm2 (no parameter; candidate
already listed under D431 / D433); 1.48 um vertical offset for 1 dB excess loss (no tolerance parameter on transitions,
D250 / D448 candidate); generic Fig. 1 statements (> 20 % below 4 um gap, 50 % at 1 um) and the BCB gap-fill estimate
(not tied to a device); "over 6 %" theoretical efficiency gain (relative); ring resonances in the Fig. 5(c) inset (no
values, no ring row); IV curves (no values printed).

Orgs: fab org_aim_photonics on the two transition rows (PIC wafers "fabricated by AIM Photonics", p.4), process_name
"AIM Photonics, 300 mm SOI wafers" (koscica2025 style). Laser rows fab empty: first-person growth ("we utilize
selective area growth") but authors at UCSB and SUNY Polytechnic Institute (not unambiguous, D80b) and laser
processing passive; koscica2025 precedent. Facility org_ucsb_nanofabrication_facility on every row ("A portion of this
work was performed in", D604). NAsPIII/V GmbH (GaP / GaAs MOCVD template, p.4) is a film step: note only; not in the
registry (name as printed: "NAsPIII/V GmbH", p.4 Sec. 2) if the org round wants it as a supplier.

Judgment calls: (1) the 205 mA best threshold is assigned to the selective-buffer row from Fig. 4(a) (lowest-threshold
curve is solid = selective; dashed curves start above ~280 mA); the sentence itself does not name the growth.
(2) Coupling losses entered as printed -> measured although called "approximate" (D167 / D448, koscica2025 D656);
band unspecified because the measurement current (ground vs excited state) is not stated. (3) Two gap_nm rows per
transition (final device vs growth-limited minimum), distinguished in condition.

## lit:wang2021c (Optics Express 2021, SiN-assisted 1x64 OPA on SOI)

Rows: `sin_mmi_1x2` (excess 0.18 dB at 1550 nm from the cascade slope 3.18 dB, Table 1 geometry, 300 nm SiN),
`si_mmi_1x2` (excess 0.04 dB, slope 3.04 dB, Table 1 geometry, 220 nm Si, 2 um BOX), `sin_si_converter`
(transition 0.07 dB per transition, cutback over 10-40; Fig. 4 geometry: 50 um, 0.18 um Si tip, 0.5 um Si, 1.4 um SiN,
150 nm gap, 220 / 300 nm layers), `ps_si_tin` (17.5 mW/pi, 1.42 kOhm, 1 um heater gap), `grating_emitter_series`
(family row: Fig. 7(b) FWHM divergence for lengths 600-2000 um, 8 rows extracted_from_figure; 630 nm period, duty 0.5,
700 nm SiN / 500 nm Si widths), `opa_1x64` (64 channels, 2.5 um pitch, 1.5 mm emitters, FOV 35.5 deg (phi, 1540 nm) and
22.72 deg (theta, 1500-1630 nm), spot 0.69 / 0.075 deg at 1540 nm).

Not entered: Table 2 and Table 3 values of other works; 87.6 mW/pi SiN phase shifter (cited, ref. 20); phase-shifter
array spacing 50 um (no pitch parameter for phase_shifter); heater length (not stated); 1x64 MMI tree as a whole (no
value). Fig. 7(b) x axis prints "(mm)" with ticks 600-2000; read as um because the text says the length "can be at
least 2 mm" (noted on the row).

Orgs: fab empty on all rows except the grating-emitter series: "We fabricated several grating emitters with different
length" (p.4) is first-person; all six authors at SIMIT (two also UCAS) -> org_shanghai_institute_of_microsystem_and_information_technology
(borderline, D83c: fabrication place not stated). "The OPA is fabricated on SOI integrated with silicon nitride" is
passive (D80b). No facility named.

Judgment calls: (1) one family row for the length series instead of eight sibling rows (D165 analogue, series-row
precedents). (2) p_pi 17.5 mW/pi band c_band inferred from the Fig. 6(b) window (about 1528-1572 nm). (3) MMI values
as excess_loss_db (printed "insertion loss" is the cascade slope minus 3 dB, D43).

## lit:newman2019 (Optica 2019, optical-clock architecture)

Rows: `sin_dks_comb_1thz` (laser.comb: repetition rate 1000 GHz derived from 1 THz, radius 23 um derived from the
46 um diameter), `silica_dks_comb_22ghz` (laser.comb: 22 GHz measured, radius ~1000 um derived from ~2 mm diameter).

Not entered: clock laser (778.1 nm DBR, off-the-shelf, vendor not named): its only number is the ~475 kHz
"contribution from the laser linewidth" to the two-photon line width, not the laser's own linewidth (ambiguous, not a
row); microfabricated Rb vapor cell (3 x 3 x 3 mm, rear-window coating R = 99.8 %) and microfabricated PMT (not
photonic component classes); clock stability / phase noise / frequency shift (system-level); comb span, Q and pump
thresholds (not printed in the main text; Supplement 1 not cached).

Orgs: fab empty on both rows (no fabrication statement in the main text; multi-institution author list, D80b); no
facility. Cell-fabrication staff thanks concern the vapor cell (not a row).

## Missing orgs

None missing from the registry for the entered fab / facility roles (org_lionix_international, org_eth_zurich,
org_aim_photonics, org_ucsb_nanofabrication_facility, org_shanghai_institute_of_microsystem_and_information_technology
exist). Not entered, for the org round if wanted: "NAsPIII/V GmbH" (skipper2025 p.4 Sec. 2, film / template supplier,
note only).

## Registry gaps (skipped value, locator, proposed definition)

- `crosstalk_db` (or an inter-channel crosstalk parameter) for free_space_emitter: mehta2020 -60 dB relative intensity
  at a non-addressed trap zone (p.5, p.11 Methods Sec. 6) - "relative emitted intensity at a non-addressed emitter
  position when another channel is driven, positive dB".
- `tol_1db_vertical_um` (or tol_1db on waveguide_platform.transition): skipper2025 1.48 um vertical offset for 1 dB
  (simulated, p.2) - already a D448 candidate.
- `threshold_current_density_a_per_cm2` (laser): skipper2025 1.14 kA/cm2 (p.6) - existing D431 / D433 candidate.
- `pitch_um` for phase_shifter: wang2021c 50 um phase-shifter array spacing (p.2) - "center-to-center spacing of
  phase shifters in an array".
- `pointing_deviation_deg` (free_space_emitter): li2019a spot positions within 0.03 deg over 1550-1580 nm (p.11) -
  "largest change of far-field beam direction over the stated wavelength range".
