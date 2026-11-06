# Batch report: lit_91 (amplifier, laser, chip_chip_coupler)

Date: 2026-11-06. Result: 18 components, 110 metric rows; `merge_component_staging.py --dry-run`: "+18 components, +110
metrics; errors 0". The only warning is on merged row cmp_lit_ni2025b_pimmwc-m18, not this batch. Page-1 titles of all four
cached texts match their source rows. None is a correction or erratum (D409), and none has a garbled text layer.

| paper | components | metric rows |
|---|---|---|
| tsakyridis2020 | 1 | 3 |
| itoh2024 | 8 (4 size-series CW devices, 4 cladding-phase-series devices) | 52 |
| maeda2024 | 5 | 37 |
| moscosomartir2017 | 4 (2 fabricated, 2 design) | 18 |

Fab / facility: empty on all 18 rows (reasons per paper below). No org is missing from the registry for any fabrication
statement. For the record, the author orgs present in the registry are: org_aristotle_university_of_thessaloniki,
org_sumitomo_electric_industries, org_kyoto_university, org_ntt, org_the_university_of_tokyo, org_keio_university,
org_iii_v_lab and org_mellanox. Not in the registry: RWTH Aachen University (Institute of Integrated Photonics) and Almae
Technologies (moscosomartir2017 p.1 affiliations). They would matter only if a coordinator ruling assigns fab on that paper.

## tsakyridis2020 (theory + experiment, JLT)

Row: differentially biased SOA-MZI used as a burst-mode wavelength converter and power equalizer (`amplifier.other`, platform
empty). Vendor, platform and fabrication of the device are not stated anywhere. Rule 4 separation: theory results are not
entered (they have no parameter). The only modelled number tied to the device is Gcw1 = 2. The paper prints it in the
experimental section, but it is also the theory input, so it is author_estimate.

Rows: gain_db 3.0 (from the printed linear Gcw1 = 2, SOA1 in deep saturation, author_estimate after the conversion, D256a).
extinction_db 6.5 / 6.4 dB: measured ER of the converted output eye after 14 / 25 km, with the full operating point in the
condition.

Not entered:
- Theory: equalization of more than 9 dB loud/soft ratio; ERVout about -2.5 dB (Gcw1 = 2), below -4 dB (Gcw1 < 10) and -6 dB (B = 0.9) (p.6 Fig. 3). Simulated, and there is no parameter.
- Measured system values: equalization up to 8 dB loud/soft ratio at 10 Gb/s; BER improvement of 2.3 / 2.2 dB (14 / 25 km) and at least 2.39 dB (20 Gb/s); error-free 20 Gb/s NRZ over input wavelengths 1541-1549.3 nm (8.3 nm span); 10 / 20 Gb/s data rates. There is no amplifier parameter for these.
- Experimental ERVout points in Fig. 3(b), (c): no parameter.
- Drive currents and assist / control powers: entered as conditions.

## itoh2024 (JSTQE, 1.55 um InP double-lattice PCSELs)

Rows: four CW devices with p-electrode diameter L = 100 / 150 / 200 / 300 um (`laser.pcsel`, `inp`). Each has its own PC
design (rule 9). Each row carries 11 metrics:
- Pmax 124 / 258 / 318 / 511 mW (text).
- WPE: 20.8 % for L = 150 um, and "> 18 %" (gt) for the other three, as the paper states it.
- SMSR > 60 dB.
- Divergence FWHM 0.55 / 0.41 / 0.32 / 0.23 deg and 1/e2 1.1 / 0.70 / 0.59 / 0.58 deg (Fig. 6 table).
- Threshold about 75 / 155 / 245 / 495 mA, read off Fig. 4(b) (+/-15 mA).
- kappa1D 696 / 632 / 476 / 405 and kappa2D 228 / 212 / 176 / 120 cm-1 (Fig. 3 table). These are derived: model extraction from the measured band-edge frequencies (D80a).
- 0.11 nm/K, stored as 110 pm/K and derived. The paper states it "for all device sizes", so it is on all four rows.
- Lattice constant about 480 nm (design_target).
- p-InP cladding 1.98 um (1.8 um + 180 nm, derived).

Four further rows cover the cladding-phase series at L = 200 um, pulsed, with cladding +0 / +60 / +120 / +180 nm. These are
sibling designs (rule 9). Each has slope efficiency (Fig. 2(b) reads 0.15-0.18 / about 0.07 / 0.26-0.29, and the text value
> 0.35 W/A at +180 nm) and the cladding thickness.

Fab empty. "We fabricated" (p.2-3) has authors at Sumitomo Electric Industries and Kyoto University, and no fabricating org
is named (D154, D395). The candidate would be org_sumitomo_electric_industries: the regrowth process is theirs per refs.
[17], [18], but no sentence places the fabrication.

Not entered:
- Air-hole test sample (depth > 500 nm, hole diameters 135 / 79 nm, p.2 Fig. 1(b)). It was a regrowth test before device fabrication, the PC design differs per size (D159), and there is no hole parameter.
- Metal-mirror reflectivity about 40 % (no laser parameter).
- Theory slope-efficiency curve and its inputs (eta_i, R, alpha_0, alpha_//, alpha_V; the last two calculated).
- Earlier results of the authors: 300 mW / 17.3 % (ref. [15]) and kappa1D 400-550 cm-1 (refs. [15], [23], [24]) (rule 3).
- Printed kappa1D L and kappa2D/kappa1D (in notes).
- Lasing wavelength "around 1.55 um" (no printed peak value, so no center_wavelength row).
- Thresholds of the pulsed series (overlapping curves in Fig. 2(a)).

## maeda2024 (JLT, post-deadline; open access CC BY-NC-ND, facts and locators only)

Rows:
- Membrane DR laser with DFB 200 um on TFLN (`laser.heterogeneous`, `inp_membrane`, maeda2023 precedent): threshold 1.7 / 2.8 / 5.7 mA at 25 / 50 / 80 C; about 2.7 mW maximum into a large-area PD; design kappa 350 / 370 cm-1 (author_estimate, D82a); section lengths, MQW core width and InP slab thickness.
- Membrane DR laser with DFB 140 um integrated with the TFLN MZM: about 1298 nm, SMSR about 50 dB at 18 mA (Fig. 13); -8 dBm coupled to the fiber through the MZM (ref_plane fiber, includes MZM); same design geometry.
- Membrane SOA, 140 um (`amplifier.soa`, `inp_membrane`):
  - Fig. 11 on-chip gain read at the lowest input: about 8.7 dB at 10 mA and 6.6 dB at 5 mA (extracted_from_figure).
  - "> 6 dB at -1.5 dBm" (derived, D166).
  - Psat_in about -10 dBm (derived, D166; the current is not stated).
  - Geometry.
- InP channel inverse taper to the TFLN waveguide (`waveguide_platform.transition`, `other`; maeda2023 / niels2025a coupon-transition precedent):
  - Coupling loss 0.5-1.0 dB: measured with method reference_structure, from the LD-on-TFLN vs reference-LD-on-BOX comparison (D167 / D441: subtracted powers not printed, "estimate" quoted). Band O inferred (reason in notes).
  - Simulated 0.1 dB at zero misalignment, read off Fig. 4.
  - Figure-labelled taper lengths 150 / 50 um.
  - Tip and widths (derived from um). TFLN film, InP slab and BOX thicknesses.
- TFLN chip facet of the reference waveguide (`fiber_chip_coupler.edge`, platform empty because rib vs strip is not stated, D423): 6 dB per facet at 1280 nm (measured, D167; printed with a minus sign).

Fab empty on all 5: first-person fabrication, but the authors are at NTT, the University of Tokyo and Keio (maeda2023
precedent, D154). The acknowledgment thanks named people only.

Not entered:
- D259 / D408: the figures whose captions cite the authors' ECOC 2023 paper [13] (Fig. 8 lasing spectra with SMSR 35-40 dB at about 30 mA; Fig. 10 SOA gain vs current with the 8.3 dB maximum at 10 mA, also in the abstract and conclusion; Fig. 14 eyes). Table I (comparison of other works, cited [13]) is out anyway. This is a journal extension of [13], and D408 keeps its values except where a figure is attributed to the earlier paper. Here the captions attribute these figures. See question 1.
- MZM Vpi 2.5 V, EO bandwidth about 80 GHz (reference sample) and 128 Gb/s NRZ BER: modulator / link metrics (rule 2). EO-atlas candidate.
- Simulated misalignment tolerance about 1.0 um within 0.5 dB (Fig. 4): a 0.5-dB criterion with no parameter on transitions.
- TEM misalignment about 150 nm (notes).
- TFLN facet FSR about 0.35 nm (a parasitic cavity).
- Reference LD on BOX (no printed values).
- MZM waveguide width 0.8 um / etch 0.4 um and the MMIs (no performance metric).

## moscosomartir2017 (CLEO-PR, 4 pages)

Rows:
- Flip-chipped single-section MLL (`laser.comb`, platform empty: the III-V material is not stated, D422): more than 3 mW inside the SiP waveguide (author_estimate, on_chip: the GC loss is de-embedded and its value is not printed, D394 / D428); threshold about 15 mA read off Fig. 5; FSR about 100 GHz (design statement, author_estimate); chip length about 400 um; stripe width 1.5 um (from the printed 1500 nm; the Fig. 6 caption says 1.4 um, D417).
- Laser-to-SiP butt interface (`chip_chip_coupler.butt`, `soi`): 7 dB per_interface (author_estimate, loss_breakdown: it rests on a de-embedded GC term and a nominally identical ceramic-mounted laser); simulated 3.3 dB (dy = 1.5 um) and 6.1 dB (dy = 5 um) read off Fig. 6; Si taper tip 180 nm and Si layer 220 nm.
- Two design rows with the laser stripe tapered to wT = 300 / 500 nm. Simulated 3.0 / 3.5 dB and 2.4 / 4.9 dB at dy = 1.5 / 5 um (Fig. 6 dotted curves, +/-0.2 dB). The text's "about 1 dB better" for 500 nm agrees with 3.3 vs 2.4.

Fab empty. III-V Lab "modified" the MLL designs (p.2), which is not a fabrication statement. The SiP recess etch and the
attachment are "our process" with authors at four orgs (D80b, D154).

Not entered:
- "3.5 dB excess due to misalignment" (relative, in notes).
- Vertical accuracy "in principle" below +/-10 nm: a process tolerance of the 90 nm BOX etch, not a coupling tolerance.
- Single-laser LI roll-off above 150 mA (Fig. 7(b)).
- Simulated laser-to-SiP temperature differences of 6.2 / 11 C at 600 mW (an assembly simulation, no parameter).
- Simulated 1-dB tolerances from Fig. 6: not printed; reading them off the curvature would be an inference.
- No wavelength is stated anywhere, so the loss rows have `band: unspecified`.

## Judgment calls

1. maeda2024 D259 / D408 strict reading. The 8.3 dB SOA gain and the SMSR 35-40 dB are left out because their figures (Fig. 10, Fig. 8) carry [13] in the caption. The srinivasan2020 precedent (D455) supports this. The value sentences themselves cite nothing, and the paper is the journal extension of [13]. The alternative is to keep 8.3 dB (measured / derived, 10 mA, 1280 nm) and SMSR 35-40 dB (about 30 mA, 25-80 C) on the D408 base rule. In its place I entered the gain from the unattributed Fig. 11, which peaks at about 9.2 dB, so it does not reproduce 8.3 dB.
2. maeda2024 InP-to-TFLN coupler as `waveguide_platform.transition` (maeda2023 / niels2025a precedent for printed coupons on the same chip), not `chip_chip_coupler.evanescent` ("die-to-wafer"). The 0.5-1.0 dB value is measured (D167 / D441), not derived: the subtracted powers are not printed.
3. tsakyridis2020 class `amplifier.other`. The device is an interferometric gate with two SOAs, not a single amplifier. The alternatives are `amplifier.soa` or `switch_fabric.other` (D158 by function). The extinction rows are output-signal ERs of the converter's eye, not a static gate contrast.
4. itoh2024: one row per electrode diameter (the PC design changes per size), plus four phase-series rows. The series' +180 nm devices are not stated to be the size-series L = 200 um device, so they are kept separate. Fig. 3 kappas are `derived` (model extraction, D80a); the alternative is `measured` as a standard fit of own data.
5. moscosomartir2017: the 7 dB interface loss and the more than 3 mW on-chip power are author_estimate (GC term of unstated value, plus a different reference laser). The MLL is `laser.comb`, although mode-locking is not characterized here.
6. Figure reads (itoh2024 thresholds and slope efficiencies; maeda2024 Fig. 11 gains, Fig. 4 transmittance and Fig. 3(b) taper-length labels; moscosomartir2017 Fig. 5 threshold and Fig. 6 peaks) were taken from page renders or enlarged embedded images. The reading uncertainty is in the notes.

## Registry gaps (skipped values)

| proposal | skipped value | source |
|---|---|---|
| conversion_range_nm (input-wavelength span of an all-optical wavelength converter at a stated BER criterion; amplifier / frequency_converter) | 8.3 nm (1541-1549.3 nm, error-free 20 Gb/s) | tsakyridis2020 p.9 |
| input_dynamic_range_db / loud-soft ratio (power-equalization range of a burst-mode amplifier or gate; D250 deferred) | up to 8 dB measured, > 9 dB theory | tsakyridis2020 p.7, p.6 |
| reflectivity_pct on laser (integrated back-mirror reflectivity) | about 40 % metal p-electrode | itoh2024 p.2 |
| hole_diameter_nm on laser (D431 candidate) | 135 / 79 nm (test sample) | itoh2024 p.2 |
| tolerance at a stated dB criterion on waveguide_platform.transition (D250 deferred) | about 1.0 um within 0.5 dB, simulated | maeda2024 p.3 Fig. 4 |
| rollover_current_ma (laser L-I rollover onset) | about 150 mA, single-laser flip-chip | moscosomartir2017 p.3 Fig. 7(b) |
