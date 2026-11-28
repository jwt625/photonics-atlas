# lit_320 batch report

Distilled 2026-11-28. Papers: lit:roeloffzen2013, lit:maesenovo2013, lit:herr2014a. Result: 5 component rows, 26
metric rows; `merge_component_staging.py --dry-run`: +5 components, +26 metrics, 0 errors (the 2 warnings name merged
rows of other batches). Page-1 titles match the source rows: roeloffzen2013 and maesenovo2013 are the Optics Express
publisher copies; herr2014a is the arXiv preprint 1311.1716v1 of the listed Physical Review Letters paper (same title
and authors). No cached file is another paper or a correction / erratum. Values from the cached text and page renders
only.

## lit:roeloffzen2013 (Optics Express, 25 p, partly a review of the authors' TriPleX MWP work)

Components: 2 (`resonator.ring`, platform `sin`, fab empty, `process_name` "Si3N4/SiO2 TriPleX waveguide
technology"). Metric rows: 6.
- `cmp_lit_roeloffzen2013_obfn16_rr_delay_lines` (4): ring FSR 25 GHz (measured, Fig. 10), bend radius 125 um
  (mask layout), chip footprint 0.7 x 2.2 cm -> 1.54e8 um2 (derived), heater power 20 W total for 120 heaters
  (`tuning_power_mw` 20000, author_estimate, origin not stated).
- `cmp_lit_roeloffzen2013_pm_im_two_rr_cascade` (2): FSR 25 GHz (author_estimate: not stated whether measured or
  design), power coupling kappa1 = kappa2 = 0.52 -> 52 % (Fig. 24(c) label, author_estimate).

Own vs reproduced (D259 / D259a / D408): the abstract names the 16-channel beamforming network and the modulation
format transformer as new measurements; Figs. 9, 10 and 24 carry no "from [N]". Every other result figure is captioned
"from [N]" with N one of the authors' own earlier papers, and those values are removed:
- Sec. 4.2 waveguide loss 0.12 dB/cm (R = 50 um) and 0.095 dB/cm (R >= 70 um), ring circumference 8783 um, FSR 20 GHz,
  bend radii 50-125 um (p.12, Fig. 6 "from [10]"; also restated on p.8 with ref. [10]).
- 4 x 1 MZI-coupler combiner, 6 dB combining gain (p.12-13, Fig. 7 "from [7]"); 1 x 8 delay circuit with 14 GHz FSR
  rings (p.13, Fig. 8 "from [8]").
- Separate-carrier-tuning processor: 0 to about 400 ps delay, 0-360 deg phase, 1 GHz band (p.15-16, Figs. 11-12 "from
  [9]"); two-tap microwave photonic filter (p.16-17, Figs. 13-14 "from [9]").
- Chebyshev II MZI-RR filters, FSR 19.6 GHz (p.17-18, Fig. 15 "from [14] and [10]").
- Frequency discriminator chip: five add-drop rings, FSR 21.5 / 10.7 GHz, bend radius 150 um, footprint 9 x 7 mm,
  SFDR link, UWB pulse shaping, IFM (p.18-21, Figs. 16-19 "from [11]", "[12]", "[13]").
- Hilbert transformer and I/Q generation with a 15 GHz FSR ring (p.21-22, Figs. 20-22 "from [15]"); polarization
  network (p.22-23, Fig. 23 "from [14]").
- Sec. 3 cited values: 49-laser array to tapered TriPleX coupling 2.2 dB total loss (p.10, ref. [30]); 25 kHz
  external-cavity laser linewidth (p.10, ref. [26]); liquid-crystal cladding tuning at 5 V with 80,000x lower power
  (p.11, ref. [32]); 8 x 1 OBFN heater about 350 mW average, pi tuning, about 40 C over a 2 mm heater (p.11, ref. [7]);
  silica / SiON < 0.05 dB/cm (p.8, refs. [18, 19]).

Values not entered and why (own data):
- 16 x 1 OBFN delay: 6-RR cascade maximum delay 650 ps over a 4.5 GHz bandwidth, 2 / 3 / 4-RR cascades in Fig. 10(a)-(c)
  (p.14-15): no delay parameter in the registry (in the component notes; gap below).
- 16 x 1 OBFN design requirements 16 inputs, 4.5 GHz, 290 ps (p.14): requirements, and `n_inputs` is not allowed for
  `resonator`.
- PM-IM conversion: 7.5 GHz RF bandwidth centred at 12.25 GHz (p.24, Fig. 24(d)), PM sweep 10 MHz-20 GHz, 3 pi phase
  jump and 5.5 GHz markers (Fig. 24(c)): system-level RF quantities, no registry parameter (component notes).
- TriPleX surface roughness < 0.4 nm by AFM (p.9): general platform statement with no device, no registry parameter.
- Fig. 2 / Fig. 3 / Table 1 theory curves (p.6-8): generic transfer-function illustrations, no device.

Judgment calls:
- Ring delay-line arrays as one `resonator.ring` row each (D165; xiang2018 TTD precedent): the registry has no
  delay-line class. The OBFN row carries chip-level footprint and heater power with the scope in `condition`.
- The 20 W sentence reads "the 16x1 OBFN chip, from Fig. 8 has 120 heaters" (p.24-25), but Fig. 8 is the 1 x 8 delay
  circuit of ref. [8]: entered on the 16 x 1 OBFN (Fig. 9) the sentence names, conflict in notes; `tuning_power_mw`
  used for a chip-total heater power (definition "heater / tuning power for the stated range"). Coordinator may prefer
  notes only.
- Platform `sin`, core / cladding from the Sec. 3 process statement ("The TriPleX waveguides described in this paper
  are fabricated using ..."); the cross-section geometry of these chips is not stated.
- Fab empty: passive process description, no fabricating org named; LioniX BV and SATRAX BV are author affiliations
  only (Contract v7, D545 / D806 precedent).
- No operating wavelength is printed for either device; no metric used needs one.

Missing fab / facility orgs: none needed (no fab statement, no facility). For the org round only: "LioniX BV" (p.1
affiliation 3) has no time-correct registry org (D545 open item); not used on any row here.

## lit:maesenovo2013 (Optics Express, simulation-only design)

Components: 2 (`splitter.mmi`, `row_kind: design`, platform `soi`, TE). Metric rows: 16.
- `cmp_lit_maesenovo2013_swg_mmi_2x2_2d` (10): excess loss < 1 dB, imbalance < 0.6 dB, phase deviation < 3 deg over
  the printed 1260-1675 nm range (simulated); W_MMI 6 um, L_MMI 23.18 um (122 periods), W_a 1.2 um, W_g 450 nm
  (derived from 0.45 um), taper 10 um (53 periods), pitch 190 nm, Si 260 nm.
- `cmp_lit_maesenovo2013_swg_mmi_2x2_3d` (6): the same three bounds for the 3D FDTD re-optimized design (pitch 198 nm,
  94 / 51 periods), checked against the Fig. 4 SWG (3D) points; L_MMI 18.612 um and taper 10.098 um derived as
  periods x pitch.

Values not entered and why:
- Conventional comparison MMI (W_MMI 6 um, W_a 1.2 um, S 2 um, L_T 10 um, L_MMI 48.2 um at 1.47 um, p.7): its
  performance is only plotted (Fig. 4), and the "insertion loss minima <= 0.25 dB" (p.5, Fig. 2(c)) belong to a
  device-length sweep at several center wavelengths, not one design; no row.
- Intro "bandwidth typically limited to about 100 nm for 2 x 2 MMIs" (p.2): general literature statement, rule 3.
- Wavelength-averaged beat length 46.5 um (p.6), SWG effective index about 2.72 and pitch upper bound about 230 nm
  (p.5), modal phase error < 45 deg threshold (p.6, ref. [25]): no registry parameter / design criteria.
- Access separation S = 2 um (center to center) is stated for the conventional paired MMI (p.4, p.7), not restated for
  the SWG design: not entered.
- P_MMI / P_T period counts and the 50 % duty cycle: kept in `condition` (`n_periods` and `fill_factor` are not allowed
  for `splitter`; gap below).

Judgment calls:
- The 450 nm bandwidth endpoints are not printed; rows use the printed covered range 1260-1675 nm (p.7 Sec. 4 and
  Sec. 5) with the 450 nm wording in notes (not marked inferred: the range is printed with the claim).
- 2D and 3D designs as sibling rows (different pitch and length, rule 9). The 3D row repeats the printed bounds because
  the text states the 2D results were verified in 3D; the Fig. 4 3D readings in notes support each bound over
  1260-1675 nm. Widths are not restated for the 3D design and are left off that row.
- Platform `soi`: Si core on an SiO2 substrate with an SU-8 superstrate (p.3); the paper never says "SOI wafer".

Missing fab / facility orgs: none (design only).

## lit:herr2014a (arXiv 1311.1716v1, preprint of the Physical Review Letters paper)

Values from the preprint only; the journal version was not read.

Components: 1. Metric rows: 4.
- `cmp_lit_herr2014a_sin_spiral_microresonator` (`resonator.other`, `sin`): linewidth 350 MHz (TM11, measured,
  band unspecified), FSR about 76 GHz (measured), Si3N4 800 nm high (design_target), 2 um wide (derived).

Values not entered and why:
- Every MgF2 result (FSR 14.09 GHz, linewidths 50-500 kHz, kappa/2 pi 72 / 147 / 278 / 173 kHz, D2/2 pi 1.9 and 21
  kHz, D3/2 pi 90 Hz, single-soliton spectrum 3-dB width 13 nm (1.62 THz), 194 fs pulse, about 30 mW pump at 1552 nm,
  14.09 GHz repetition-rate beat; p.1-3, Figs. 1-3): the resonator is a crystalline MgF2 resonator (Fig. 2(a) inset, 5 mm
  scale bar), a discrete bulk polished crystalline resonator out of scope (D411; tebeneva2024 / zhang2025e precedent).
- Fig. 4 simulation parameters (kappa/2 pi 1 MHz, FSR 35 GHz, gamma 4e-4 /m/W, 100 mW pump; p.4): assumed generic
  values, no device.

Judgment calls:
- Class `resonator.other`: the text says only "Si3N4 microresonator"; the Fig. 2(b) inset micrograph shows a
  spiral-type layout, not a plain ring.
- Linewidth "resonator linewidth of 350 MHz" is unqualified: entered as `linewidth_mhz` (loaded width) with a note.
- No wavelength is stated for the Si3N4 measurement: `band: unspecified` with a note (rule 8; the device's operating
  band is not stated either).

Missing fab / facility orgs: none (fabrication of the Si3N4 device not stated).

## Registry gaps

- `group_delay_ps` (resonator, wdm, waveguide_platform): peak or flat-top group delay of a delay line, with the delay
  bandwidth in `condition`. Skipped: roeloffzen2013 16 x 1 OBFN 6-RR cascade 650 ps over 4.5 GHz (p.14, Fig. 10(d));
  same gap as xiang2018 (merged notes).
- `delay_bandwidth_ghz` (resonator, wdm): bandwidth over which the stated group delay holds. Skipped: roeloffzen2013
  4.5 GHz (p.14).
- `n_periods` and `fill_factor` allowed for `splitter` (SWG multimode sections and SWG tapers). Skipped: maesenovo2013
  P_MMI 122 / 94, P_T 53 / 51, duty cycle 50 % (p.6-7).
