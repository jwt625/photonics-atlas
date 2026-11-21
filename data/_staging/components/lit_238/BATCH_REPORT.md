# lit_238 batch report

Papers: lit:pudo2008, lit:matsuo2012, lit:zhou2023b, lit:he2024. Page-1 titles match the source rows; no garbled text
layer; none is a correction. No existing component rows for these sources. verified_on 2026-11-20. Dry run of
`merge_component_staging.py`: +8 components, +62 metrics, 0 errors (the one warning names the merged row
cmp_lit_ni2025b_pimmwc, not in this batch).

| paper | components | metric rows |
|---|---|---|
| pudo2008 | 0 | 0 |
| matsuo2012 | 1 | 7 |
| zhou2023b | 6 | 38 |
| he2024 | 1 | 17 |

## pudo2008 (scaling of passively mode-locked soliton Er waveguide lasers, OE 2008)

No rows. The paper is a scaling analysis (soliton area theorem) of three lasers that the authors' own earlier or
forthcoming papers report:
- Sec. 3, 491 MHz laser: 20.7 cm Er-doped fiber butt-coupled to an SBR, assigned to ref. [14] (authors' Opt. Lett. 2008).
  Fiber laser (out of scope, D80f) and cited (rule 3, D259 / D408).
- Sec. 4, 3.2 GHz laser: 3 cm Er-Yb fiber (NP Photonics), assigned to ref. [15]. Fiber laser and cited.
- Sec. 5, integrated laser (5 cm Er-doped alumino-silicate waveguide + 20 cm P-doped silica waveguide, loop mirror with
  10 % output coupling, butt-coupled commercial SBR BATOP SAM-1550-23-x-2ps): assigned to ref. [16], the authors'
  forthcoming LEOS 2008 paper ("440 fs pulses at 394 MHz [16]", p.8). D259 / D408 cover values assigned to a
  forthcoming paper of the authors, so Tables 11-14 (labelled "estimated parameters", incl. Pcav 12 mW, 400 fs, 394 MHz,
  25 % lumped loss, g0 1.5 dB/cm, Aeff 10 / 40 um2, beta2 +30 / -25 fs2/mm) and the Fig. 6 layout / SBR inset are not
  entered. Printed conflict for the record: text 440 fs vs Table 14 400 fs (p.8 vs p.9).
- Model outputs not entered: projected repetition-rate limits (theoretical 5 GHz, "actual highest possible" 3 GHz for
  the integrated laser, p.9-10; > 20 GHz for the Sec. 4 fiber laser, p.8). They are simulations of a hypothetical
  family of cavity lengths built on the cited lasers' estimated parameters, not a defined design (judgment 1).
- Table 15 (silica / As2S3 / Si n, n2, beta2, loss) cites refs. [20], [21]; the SBR datasheet values (14 % modulation
  depth, 2 ps, 25 uJ/cm2) belong to the cited laser and have no registry parameter.

Orgs: none (no component rows; acknowledgment names grants only).

## matsuo2012 (RT CW lateral-current-injection LEAP photonic-crystal laser, OE 2012)

Row `laser.other` `cmp_lit_matsuo2012_leap_laser_lci` (platform inp_membrane, class / platform as the merged matsuo2013
rows):
- threshold 0.39 mA (printed 390 uA, derived); effective threshold 9.4 uA (author_estimate; conclusion prints ~9.5 uA,
  conflict noted); optical-pump threshold 11.8 uW effective absorbed power (author_estimate: calculated absorption
  coefficient and confinement factor).
- waveguide-referred output 1.82 uW at 2.0 mA (author_estimate: rests on the 10 dB coupling loss of ref. [7]).
- 3-dB linewidth at threshold 0.035 nm (measured; wavelength 1559.5 nm read off Fig. 4(a), `wavelength_inferred`).
- figure reads: lasing peak about 1559.5 nm near threshold (Fig. 4(a)); voltage about 2.45 V at 2.0 mA (Fig. 3(a)).

Not entered: Q 44,600 from the linewidth and FDTD Q ~4200 / Veff ~0.15 um3 (no laser Q / mode-volume parameter, D250);
active-region temperature rise 7.1 K at 1.2 mA and < 15 K at 2.0 mA (no parameter; rests on the 0.095 nm/K of ref.
[18]); ref. [7] values (Pth 3.2 uW, 53 % differential efficiency, 8.76 fJ/bit) and ref. [19] 100 nm wavelength range
(rule 3); active-region dimensions 2.6 x 0.3 x 0.15 um and 220 nm holes kept in core_material (matsuo2013 precedent; no
hole-diameter parameter).

Orgs: fab org_ntt. First-person fabrication steps (p.4 Sec. 2: "we employ Zn diffusion and Si ion implantation", "we
deposited a SiO2 layer") with all authors at two NTT Corp. laboratories (D154 parent; NTT Corp. -> org_ntt as on the
merged matsuo2013 rows). Staff thanked "for fabricating the device" without an org (not a facility, D84b / D543). No
missing org.

## zhou2023b (on-chip calibration for a 1 x 32 Si OPA, PTL 2023)

Rows (all fab org_amf, platform soi, 220 nm Si on 3 um BOX):
- `free_space_emitter.other` OPA: horizontal steering 36.4 deg (18.3 + 18.1, derived) at 1580 nm; vertical 11.5 deg over
  1530-1610 nm; 0.144 deg/nm (derived, sign as printed though Fig. 7(b) decreases); emission angle about 12.4 / 1.0 deg
  at 1530 / 1610 nm (Fig. 7(b) reads); best SLSR 9.3 dB; FWHM 0.98 x 0.95 deg measured, 0.96 x 0.92 deg simulated
  (1550 nm); total loss about 13 dB (device_total, author_estimate); 32 channels, 2.5 um pitch, footprint 8.4 x 1.9 mm
  (derived), stack thicknesses.
- `free_space_emitter.grating_emitter` emitter: 5.5 dB grating-emission term (author_estimate, loss_breakdown); period
  630 nm, duty 0.5, 100 um long, 1 um wide, 70 nm groove depth.
- `phase_shifter.thermo_optic` folded TiN phase shifter (reference MZI, test_structure true): P_pi 5.3 mW, MZI ER
  > 24.7 dB (Fig. 4(a) label), rise / fall 21 / 23 us, heater 330 ohm (author_estimate), heater 8 x 222 um, 120 nm,
  2 um above the waveguide.
- `splitter.mmi` five-stage 1 x 32 MMI network: 1.4 dB excess loss (device_total, author_estimate); 1 input, 32
  outputs.
- `fiber_chip_coupler.grating` input GC: 4.9 dB per coupler (author_estimate, loss_breakdown).
- `photodetector.ge_waveguide` GeSi PD: 1 A/W and 3 uA dark current at -1 V (author_estimate: no PD measurement shown);
  32 per chip.

Not entered and why:
- "consumption of the OPA unit is less than 0.33 W" (p.3): power_consumption_w not allowed for free_space_emitter
  (registry gap below).
- 1.2 dB waveguide term of the loss budget: no length, no waveguide test structure; kept in the OPA loss row includes
  (judgment 3).
- ~28 uW into each interferometric structure (measured) and 20 % of the grating input (FDTD): no parameter.
- MMI region sizes 6 x 32 um and 1.8 x 2.65 um: which kind sits where is not stated, so they stay in core_material /
  notes; folded-waveguide widths 0.6 / 0.5 / 0.4 um and 8 um tapers in core_material (three widths in one path).
- Interferometric structure length 29 um: geometry only. TIA gain 220 kOhm: setup.

Orgs: fab org_amf ("The chip is fabricated by Advanced micro foundry (AMF) based on CMOS processes", p.2 Sec. II).
process_name empty (no PDK or node named; "CMOS processes" is generic, Contract v7). No facility. No missing org.

## he2024 (gain-coupled high-power low-RIN 1.55 um DFB laser, PTL 2024)

Row `laser.dfb` `cmp_lit_he2024_gc_dfb_ridge6um` (platform inp):
- output about 220 mW kink-free at 900 mA, 25 C (measured, ref_plane chip); SMSR about 60 dB above 400 mA; SMSR > 55 dB
  at 300 mA over 20-60 C; 110 pm/K (printed 0.11 nm/K, derived); FWHM divergence 10 deg x 20 deg; RIN about -150 dB/Hz
  at 300 mA and < -166 dB/Hz at 900 mA over 0-20 GHz; differential resistance < 1.58 ohm (series_resistance_ohm, D254).
- kappa_i about 10 cm-1 (author_estimate, origin not stated); kappa_g ~3.01 cm-1 (simulated).
- figure reads: threshold about 135 mA and about 2.45 V at 900 mA (Fig. 4); peaks about 1546.9 nm (300 mA) and
  1550.0 nm (900 mA) (Fig. 5(a)).
- ridge 6 um (design_target), cavity 1400 um (printed 1.4 mm, derived).

Not entered: 80 % single-mode yield of the uncoated lasers (no parameter; other devices); sibling 4 / 8 um ridges (no
values); Fig. 2-3 carrier-density-ripple simulations; refs. [9], [10] comparison values (rule 3); slope efficiency
(not printed; would be arithmetic on two figure reads).

Orgs: fab org_tsinghua_university ("We fabricated a series of ... DFB lasers", p.2; every author at BNRist and the
Department of Electronic Engineering, Tsinghua University; D154 parent). No facility.

## Judgment calls for the auditor

1. pudo2008 0 rows: all experimental lasers are assigned to the authors' refs. [14]-[16] (two fiber lasers, out of
   scope; the integrated one forthcoming, D259 / D408); the repetition-rate projections are not entered as a
   `row_kind: design` laser because the analysis defines no single design.
2. matsuo2012 effective threshold 9.4 uA and 11.8 uW pump threshold entered as `author_estimate` rows on the same laser
   row (calculated absorption inputs); the 0.035 nm linewidth row carries the figure-read wavelength with
   `wavelength_inferred` true.
3. zhou2023b loss budget: total and terms `author_estimate` (the 13 dB total equals the printed sum; no measurement
   described); terms on their own rows as zhang2021a, the 1.2 dB waveguide term only in `includes`. Band `cl_band`
   inferred from the 1530-1610 nm operating range on rows without a stated wavelength.
4. zhou2023b phase-shifter MZI ER > 24.7 dB taken from the figure label as `measured`.
5. he2024 output-power `ref_plane` chip: a bare chip on an AlN submount, collection optics not described.

## Registry gaps

- power_consumption_w on free_space_emitter: zhou2023b "less than 0.33 W" OPA unit consumption (p.3 Sec. III; also
  D432 candidate). Proposed: allow power_consumption_w for free_space_emitter, scope in condition.
- Laser Q / mode volume (matsuo2012 Q 44,600 from linewidth, FDTD Q ~4200, Veff ~0.15 um3; p.5-6): D250 stands.
- Single-mode yield (he2024 80 %, p.3): proposed `yield_pct` (fraction of devices meeting a stated criterion,
  criterion in condition).
- Registry org link: org_beijing_national_research_center_for_information_science_and_technology has no parent_org_id;
  its website is a Tsinghua domain (he2024 affiliation p.1). Proposed parent org_tsinghua_university for the org round.
