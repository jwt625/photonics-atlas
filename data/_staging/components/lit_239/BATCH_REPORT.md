# lit_239 batch report

Papers: lit:wang2023f, lit:kourogi1993, lit:lu2008, lit:levy2012. Page-1 titles match the source rows; no
`garbled_text_layer` flags. verified_on 2026-11-20. Dry run of `merge_component_staging.py`: +15 components,
+64 metrics, 0 errors (the one warning names the merged row cmp_lit_ni2025b_pimmwc, not in this batch).
Fab orgs: only wang2023f SiN rows (org_ligentec). No facility orgs.

| paper | components | metric rows |
|---|---|---|
| wang2023f | 11 | 46 |
| kourogi1993 | 0 | 0 |
| lu2008 | 1 | 12 |
| levy2012 | 3 | 6 |

## wang2023f (hybrid SiN / polymer line-beam OPA, IEEE Photonics J. 2023)

Rows:
- `fiber_chip_coupler.edge` SiN SSC (1500 um linear taper, 200 nm tip): 0.8 dB per_coupler measured (UHNA4 fiber,
  TE, 1550 nm; method not described, D167); taper geometry.
- `chip_chip_coupler.butt` SiN SSC to polymer phase-modulator chip (UV-epoxy bonded): 2 dB per_interface
  author_estimate (loss-budget term, origin not stated); same SSC geometry (D396 cross-note).
- `splitter.mmi` 1x2 MMI: excess loss 0.2 dB per_component measured.
- `splitter.mmi` 1x64 tree (six MMI stages): 1.2 dB device_total derived (6 x 0.2 as printed, "leading to").
- `waveguide_platform.straight` SiN 500 nm x 1 um: ~0.2 dB/cm measured; core, width, 4 um BOX, 3.3 um cladding.
- `phase_shifter.thermo_optic` polymer TO modulator: P_pi 2.1 mW simulated (FEM); 1 dB array loss (breakdown,
  measured; see judgment call 2); Au heater 10 um x 3 mm, core t2 3 um, t1 9 um, t3 6 um.
- `free_space_emitter.other` tapered line-beam emitters Wtip 200 / 300 / 500 nm: measured vertical beamwidth
  13 / 20 / 32 deg; simulated 14 deg (text) and ~16 / ~33 deg (Fig. 2(b) read, +/- 1 deg); Wtip 300 row also has
  FIB-measured tip 320 nm x 500 nm, 100 um taper length, 0.5 dB emitter term (author_estimate), 3 um pitch, 64 ch.
- `free_space_emitter.other` SiN reference OPA (splitter directly to emitter, no PMs): horizontal FWHM 0.4 deg
  measured, 64 ch.
- `free_space_emitter.other` hybrid OPA: ~30 deg steering range and 20 deg vertical FOV measured (Fig. 8), ~9 dB total
  IL device_total measured; simulated ~30 deg range and ~0.4 deg horizontal FWHM; 64 ch, 3 um pitch.

Not entered:
- Measured P_pi ~2.3 mW (p.8): the sentence carries refs. [26]-[29], incl. the authors' own earlier polymer
  phase-modulator papers [26], [29]; not clearly this paper's result (D80i / D259). Judgment call 1.
- OPA transmitter with the PMMA lens module (~51 deg range, 10.3-0.6 deg vertical beamwidth vs d1 = 1-4 mm,
  ~3.2 deg/mm, ~5 deg vertical FOV, ~0.6 deg horizontal FWHM, ~3.6 dB main-lobe variation; p.4-p.8, Figs. 4, 5, 9,
  10): chip plus off-chip bulk lens (D411, zhang2021a precedent); in the hybrid OPA notes. Lens Table I (design).
- Main-lobe power variation ~3 dB measured / ~3.3 dB simulated, grating lobes at +/- 31.1 deg, simulated ~13 dB
  adjacent-taper crosstalk, simulated MFD 2.1 x 2.2 / 0.8 x 0.7 um2 (Wtip 0.2 / 1 um): no parameter for
  free_space_emitter (notes).
- ~0.5 dB propagation term and ~3 dB residual bonding loss of the breakdown (no length; unassigned interface).
- Simulated 47 deg at Wtip 1 um (Fig. 2(b) sweep endpoint; no fabricated device, no design row made).
- Array period 50 um of the polymer modulators (pitch_um not allowed on phase_shifter); polymer index contrast,
  thermal conductivity, TO coefficient (material properties).

Orgs: fab org_ligentec on the SiN rows ("The SiN chip was fabricated at Ligentec SA through a photonic damascene
process", p.6; Acknowledgment p.8); process_name "photonic damascene process" as printed (the same paragraph says the
SiN was "fully etched"; both in notes). Polymer chip and bonding: passive, no org -> fab empty on the polymer, interface
and hybrid OPA rows (D515 / D399 / D450). Polymer vendor ChemOptics (LFR) in notes only. No facility. No missing orgs.

## kourogi1993 (wide-span optical frequency comb generator, IEEE JQE 1993)

0 rows. The comb generator is a bulk AR-coated LiNbO3 crystal (1.25 x 1.0 x 20.0 mm3) in a microwave guide inside a
free-space Fabry-Perot cavity (p.2-p.3, Fig. 2): bulk crystal part, out of scope (D411; rueda2019 / yokota2022 /
zhang2025e precedents). Values not entered for that reason: comb span > 4 THz, 5.8 GHz modulation (3 FSR), finesse
~200, cavity efficiency 5 %, modulation index 0.2 pi rad at 10 W, SNR 61 dB at 0.487 THz, 19 dB/THz slope,
4 THz maximum measurable difference. The DFB lasers and balanced receiver are setup equipment (rule 13). No orgs.

## lu2008 (312-fs passive single-section InAs/InP QD mode-locked laser, Opt. Express 2008)

Row: one `laser.comb` (pulses characterized, D83b / D695) 456 um x 2.5 um ridge InAs/InP QD FP laser, 18 C CW:
threshold 17.2 mA; slope efficiency 0.31 W/A (derived, printed mW/mA); average output 13.26 mW at 60 mA and 8.6 mW at
45 mA (ref_plane unspecified); centre wavelength 1541 nm and 3-dB spectral width 11.62 nm (45 mA); mode spacing
0.73 nm; repetition rate 92 GHz (10.87 ps train, 60 mA); pulse width 312 fs derived (442 fs x 0.707 Gaussian, 45 mA,
D84c); length, ridge width, 355 nm InGaAsP core.

Not entered: external differential QE up to 38 %, OSNR 62 dB, RF mode-beating linewidth < 20 kHz (resolution-limited),
TBP 0.457, threshold current density per QD layer < 300 A/cm2, temporal pulse extinction ~15 dB, peak power 0.3 W
(no parameters); 312-800 fs pulse-width spread (conditions not given); 442 fs autocorrelation width (raw, the
deconvolved value is entered). Conflict: intro 13.2 mW vs Sec. 2 13.26 mW at 60 mA (Sec. 2 entered, both in notes).

Orgs: fab empty (growth / processing passive; all authors at NRC Institute for Microstructural Sciences, D80b). No
facility. Missing alias candidate (not needed for a row): "Institute for Microstructural Sciences, National Research
Council" -> org_national_research_council_canada (p.1 affiliation).

## levy2012 (Si3N4 multiple-wavelength source, IEEE PTL 2012)

Rows:
- `laser.comb` Kerr comb (116 um ring, 1541 nm pump): 200 GHz line spacing (channel_spacing_ghz, D83b), > 100 lines
  across 200 nm (n_channels gt), up to 1 mW per line in the bus (output_power_mw, statistic best, on_chip,
  author_estimate: on-chip derivation not stated).
- `resonator.ring` the comb cavity (D396): intrinsic Q ~1e6 (approx, author_estimate, D403; C band inferred from the
  1541 nm pump), radius 116 um.
- `fiber_chip_coupler.edge` lensed fiber into the Si3N4 bus: 7 dB "coupling losses", scope unspecified, measured
  (D167), 1541 nm inferred.

Not entered: threshold ~50 mW (credited to ref. [11], the authors' 2010 paper; rule 3); RF noise drop > 25 dB,
cavity enhancement 200, BER / < 0.5 dB power penalty (no parameters / system level); 230 um / 100 GHz design remark
and +/- 50 nm fabrication error with 0.2 % index deviation (generic); cross-section 725 by 1550 nm kept in
core_material only (which dimension is the thickness is not printed).

Orgs: no fabrication statement -> fab empty. Facility empty: the Cornell NanoScale Facility, the Center for Nanoscale
Systems and NNIN appear only in the funding sentence "This work was supported in part by ..." (p.1 footnote; D80c /
D83e). Judgment call 3.

## Judgment calls for the auditor

1. wang2023f measured P_pi ~2.3 mW (p.8) left out because the sentence cites [26]-[29] (own earlier work among them);
   alternative: enter as author_estimate with a D80i note.
2. wang2023f loss-breakdown bases: polymer modulator array 1 dB `measured` (p.6 says the polymer chip loss "was
   characterized in a similar manner"), SiN-polymer 2 dB and emitter 0.5 dB `author_estimate` (origin not stated).
   Alternative: all three author_estimate.
3. levy2012 facility: CNF named in "supported in part by" funding list -> empty (D83e reading); alternative:
   org_cornell_nanoscale_facility as borderline facility (D80c "facility thanked for supporting this work").
4. wang2023f SiN reference OPA kept as its own row (tip width not restated, D159) rather than merged into the Wtip
   300 nm emitter row; the 200 / 300 / 500 nm rows are labelled as emitters though measured as SiN OPAs.
5. wang2023f SiN-polymer interface as `chip_chip_coupler.butt` with platform `sin` (taper side) and the hybrid OPA
   platform `other` (D71 Si-polymer hybrid precedent).
6. wang2023f 1x64 tree row with 1.2 dB derived (pure 6 x 0.2 arithmetic) kept as a distinct design.

## Registry gaps (skipped value + locator + proposed definition)

- free_space_emitter crosstalk between adjacent emitters (wang2023f ~13 dB simulated, p.3): allow `crosstalk_db`.
- free_space_emitter main-lobe power variation over the steering range (wang2023f ~3 dB measured p.7, ~3.3 dB
  simulated p.3): `steering_power_variation_db`, max minus min main-lobe power over the stated range.
- free_space_emitter grating-lobe angle (wang2023f +/- 31.1 deg, p.3 / p.6): `grating_lobe_angle_deg`.
- free_space_emitter emitter-facet MFD and tip / taper geometry (wang2023f 2.1 x 2.2 um2, p.3; Wtip / Ltaper): allow
  `mfd_chip_um`, `tip_width_nm`, `taper_length_um`.
- phase_shifter `pitch_um` (wang2023f 50 um array period, p.8).
- laser: external differential QE (lu2008 38 %, p.3), OSNR (62 dB, p.3), RF mode-beating linewidth (< 20 kHz, p.6),
  time-bandwidth product (0.457, p.4), threshold current density per QD layer (< 300 A/cm2, p.3) - recurring
  (D678 / D696).
- laser.comb comb span (levy2012 ~200 nm, p.2; D418 candidate).
