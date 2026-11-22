# lit_247 batch report

Papers: lit:hadijelhouati2019, lit:virot2017, lit:chen2016d, lit:zhang2014b, lit:rosa2016, lit:ahn2007. Page-1 titles
match the source rows; no garbled text layer; none is a correction. verified_on 2026-11-22. Dry run of
`merge_component_staging.py`: +42 components, +347 metrics, 0 errors; the one warning names the merged row
cmp_lit_ni2025b_pimmwc, not in this batch. Generator script: scratchpad `lit_247/gen.py`.

| paper | components | metric rows |
|---|---|---|
| hadijelhouati2019 | 2 | 11 |
| virot2017 | 19 | 183 |
| chen2016d | 3 | 39 |
| zhang2014b | 1 | 20 |
| rosa2016 | 5 | 56 |
| ahn2007 | 12 | 38 |

Only values the papers report as their own are entered; comparison-table rows of other works (chen2016d Table 2,
baseline values cited from the authors' earlier papers) are out (rules 1, 3).

## hadijelhouati2019 (sidewall-grating distributed Bragg deflector, OE 2019)

Rows:
- `mode_converter.converter` SGD Gaussian beam expander (row_kind design, `soi`): simulated insertion loss 2.15 dB
  per_component (loss breakdown in includes), back-to-back pair 4.5 dB `device_total` and 1-dB bandwidth 150 nm
  (Fig. 9(c)); grating length 60 um, input taper 13.75 um, 260 nm Si, footprint ~560 um2 (7 x 80 um, Fig. 1).
- `splitter.other` uniform SGD partial deflector (fabricated test structure, `soi`): measured cross-port fraction ~10 %
  at 1565 nm (reference straight wire, Fig. 11(b)); design 13 % cross / 72 % through (simulated); 15 um grating.

Not entered: measured bandwidth ~40 nm (level not defined); in-plane radiation angle -8.4 deg and the 0.38 -> 30 um
MFD (no allowed parameter on mode_converter); per-element efficiencies 60-80 % (Fig. 7 design curve); 96 % overlap;
the illustrative ~551 nm pitch; the intro's "more than 80 %" kept in the wire (conflicts with the 72 % design; through
port terminated, not measured); W_SWG 2 um / W_adapt 1.5 um / 21 um capture-waveguide width (no role-specific
parameter; in core_material).

Fab / facility: fabricated by 100 keV EBL and RIE on a standard SOI wafer (p.12), no site or org named: fab empty.

## virot2017 (lateral Si/Ge/Si waveguide PIN photodiodes, OE 2017)

Rows: 15 device rows `photodetector.ge_waveguide` (W_Ge 0.3 / 0.5 / 0.8 / 1 um x L_Ge 5 / 10 / 20 / 40 um; the
W 0.3 x L 40 cell has no data in either table, no row) + 4 width-family rows. Per device: dark current at -1 V
(Table 1(a)), -3 dB bandwidth at 0 to -4 V (Table 2, "> 50" as 50 `gt`, set-up limit noted), geometry (Ge width,
length, ~260 nm thickness, 220 nm Si, 2 um BOX). Responsivity at -1 V / 1550 nm: 1.16 A/W (L 40, best), ~0.5 A/W
(L 10), figure reads ~0.19 (L 5) and ~0.74 (L 20) from Fig. 4(b); simulated 0.63 (W 1, L 10) and 0.35 / 0.57 / 0.66 A/W
(W 0.3 / 0.5 / 0.8, L 10). Family rows: Table 1(b) mean and standard deviation of the dark-current density (A/cm2 ->
mA/cm2, derived).

Not entered: optical power fractions in Ge vs doped Si (54.5 % / 86 %, simulated; no parameter); built-in field values
(TCAD); 300 nm x 5 um minimum cavity (process capability).

Fab / facility: "fabricated in LETI's cleanroom facilities" (p.4) -> fab `org_cea_leti` (passive sentence naming the
org, Contract v7); the institute's own cleanroom is not a shared facility (D404).

## chen2016d (lumped dual-region high-power Ge PD, OE 2016)

Rows: three `photodetector.ge_waveguide` rows, type A (one-side, 1D GC), type B (double-side, splitter + 2D GC),
type C (two parallel Ge regions, four-port 2D GC). Per row: dark current at -3 V (printed, uA -> nA) and at -1 V (Fig.
5(a) read), responsivity at -3 V (on_chip, grating loss taken out), maximum photocurrent at 18 dBm waveguide power,
bandwidth at 0.42 mA and at 13 mA (-3 V), Ge 5 x 10 x 0.5 um, 220 nm Si, 2 um BOX. Types A and C: junction resistance
(author_estimate), total capacitance (derived from Eq. (1) / (2)), junction capacitance (author_estimate).

Not entered: Table 1 fit parameters (rounded model inputs), the 1.152 mA/um3 maximum current density (no parameter),
RF output power at 18 mA, eye / BER thresholds, the 22 GHz nine-region estimate. No wavelength anywhere in the paper:
`band: unspecified` on the responsivity and bandwidth rows.

Fab / facility: "fabricated ... at the Institute of Microelectronics (IME) in Singapore" (p.5) -> `org_astar_ime`.
Huawei appears only in the funding list.

## zhang2014b (floating Ge photodetector, OE 2014)

Row: one `photodetector.ge_waveguide`. Responsivity 1.14 / 1.20 / 1.44 / 1.74 A/W at -4 / -8 / -12 / -16 V (1550 nm,
on_chip; -8 and -16 V from the Fig. 5(b) legend), dark current 120 / 290 / 900 / 26000 nA, bandwidth ~20 GHz (-4 V),
> 40 GHz (-8, -12 V), ~30 GHz (-16 V), capacitance 8 fF (S-parameter phase), series resistance ~490 ohm
(author_estimate from sheet resistances), Ge base 1.5 um, height 350 nm (derived), 25 deg sidewall (measured), 220 nm
Si, 2 um BOX, 90 nm slabs.

Not entered: absorber length (the electrically characterized Set B device's length is not stated; the Set A devices are
11 / 16 um incl. 6 um tapers); 26 dB attenuation of the 16 um Ge strip at 1550 nm (no parameter); transit (33.6 GHz)
and RC (36.8 GHz) model bandwidths; 88 % simulated confinement; sensitivity gains vs the cited 0.75 A/W baseline.

Fab / facility: OpSIS MPW run, "Fabrication occurred at Institute of Microelectronics in Singapore" (p.5) -> fab
`org_astar_ime`, `process_name` "OpSIS foundry multi-project wafer (MPW) run". Missing org: OpSIS (MPW access
provider, fab role per D398 / D458), "OpSIS foundry", p.5 Sec. 3.

## rosa2016 (thermo-optic 2x2 MMI switch, OE 2016)

Rows: five `switch_fabric.other` (D158) rows by MMI / heater / pad design: no-trench flat Ti pads (254.2 mW),
trench flat Ti pads (122.7 mW), trench flat Cu pads (36.5 mW), trench meander Cu pads (24.9 mW, best), no-trench
meander (54.4 mW, pad metal not stated). Simulated switching powers from Table 1 on the matching rows; Table 2
heating / cooling times as `fall_time_us` / `rise_time_us` (cross port) where the device is unambiguous; cross-port
extinction read off Fig. 7 (~34 / ~22 / ~35 dB, sampling-limited); geometry (MMI 594.5 or 616 um x 9 um, heater
80 x 3.7 um on flat rows, Ti 100 nm, 700 nm cladding, 220 nm Si, 2 um BOX, footprint ~5000 um2 on no-trench rows).

Not entered: Table 2 trench flat-heater times 0.45 / 4.3 us (D159: Ti and Cu flat-heater trench devices both exist);
measured insertion loss / crosstalk (only "very small impact"; Fig. 7 absolute dBm without input reference);
simulated trench IL 0.5 dB and > 20 dB crosstalk (design values shared by several rows; in notes); Fig. 7(a)
no-trench extinction (dip hidden by the legend). No wavelength anywhere: `band: unspecified`.

Fab / facility: fabrication passive (p.6), all authors NTC / UPV: fab empty. SEM imaging thanked to the UPV Electronic
Microscopy Department (service thanks, p.8): not a facility. SOI from SOITEC (note).

## ahn2007 (waveguide-integrated Ge photodetectors, OE 2007)

Rows (12): SiN- and SiON-coupled Ge PD family rows (levelled-off 1.08 / 0.96 A/W, derived, D394), six length rows
(10 / 20 / 40 um per waveguide, Fig. 3 reads; the 10 um SiN row adds the Fig. 4 spectrum 0.95-1.15 A/W over
~1475-1567 nm), the 7 x 10 um Fig. 2 device (leakage density 0.41 A/cm2 at -0.5 V, -1 V dark read ~0.9 uA,
footprint 70 um2), an unnamed impulse-response device (6.6 / 7.2 / 7.5 GHz at 0 / -1 / -3 V, ~400 fF author_estimate,
60 nA at -0.1 V from the summary sentence), SiN and SiON waveguide rows (2.2 / 6.9 dB/cm cutback at 1550 nm, 0.9 x 0.4
and 0.9 x 0.9 um, 2 um cladding).

Not entered: ~90 % efficiency (restatement of the responsivity); 0.45 A/W normal-incidence and 0.76 A/W at 1650 nm
estimates (hypothetical devices); "< 1 dB/cm" and "<= 1 dB" projections; photocurrent / dark ratio > 100.

Fab / facility: all authors MIT, no fabrication sentence naming an org (fab empty). Missing org (borderline fab,
D84b): "BAE Systems" (acknowledgment, p.6: two staff thanked "for support of the CMP process"); not set because no
registry id exists.

## Judgment calls

(a) hadijelhouati2019: the Gaussian expander is `mode_converter.converter` (wire mode to a 30 um slab beam) and carries
the simulated back-to-back pair values (device_total, D163 analogue); the fabricated uniform tap is `splitter.other`
with `split_ratio_pct` for the cross-port fraction (alternative: free_space_emitter.other, rejected because the beam
stays in the chip plane).
(b) virot2017 Table 2 prints the fourth block as "W_Ge = 0.8 um" twice; assigned to W_Ge = 1 um from the p.8 / p.9 text.
(c) virot2017 family rows: the text says the density is normalized by width x height, but the printed means and sample
standard deviations are reproduced exactly by I_d / (L_Ge x 260 nm) over the Table 1(a) cells; n_samples is that cell
count. Entered as derived (A/cm2 -> mA/cm2).
(d) Bandwidth rows without a stated RF wavelength (virot2017, zhang2014b) carry 1550 nm `wavelength_inferred`;
chen2016d and rosa2016 state no wavelength at all and get `band: unspecified`. virot2017 responsivity ref_plane
`unspecified` ("input received optical power"; GC loss not discussed).
(e) chen2016d: junction resistance (total minus nominal 50 ohm cable) and junction capacitance (minus simulated pad)
author_estimate; total capacitance derived (Eq. (1) / (2) on own measurements); type C 28.8 mA entered `ge` because
the paper states it had not saturated.
(f) zhang2014b: Fig. 5(b) legend responsivities (1.20 A/W at -8 V, 1.74 A/W at -16 V) entered as measured (printed
labels); no absorber length (device length unstated).
(g) rosa2016: rows split by trench / heater / pad metal. Table 2 pad metal is not stated; times entered only where one
described device matches (no-trench flat -> the Ti-pad row; meander -> the single meander devices); trench flat times
withheld (D159). Switching power stored as `p_pi_mw`. p.7 prints both 254.2 and 245.2 mW for the first device; 254.2
kept (D417 note). Simulated Table 1 powers placed on the matching rows (the Ti row note says pads are not simulated).
(h) ahn2007: unnamed speed device kept as its own row (matsuo2013 precedent); PD platforms `sin` / `sion` by the feed
waveguide (bernard2021 precedent), empty for the two rows whose waveguide is not stated; responsivities derived
(input power from the reference waveguide and the cutback loss).

## Registry gaps

- Absorber attenuation of a waveguide PD section (zhang2014b 26 dB for the 16 um Ge strip at 1550 nm, p.5 Fig. 4):
  proposed `absorption_db` (photodetector; transmitted-power drop of the absorber section, length in condition).
- In-plane emission angle and output-beam MFD for an in-plane beam converter (hadijelhouati2019 -8.4 deg, p.8;
  30 um MFD, p.2-3): proposed allowing `emission_angle_deg` and `mfd_chip_um` on mode_converter, or a
  slab-beam subtype.
- `n_periods` on splitter (hadijelhouati2019 uniform SGD 25 periods, p.11).
- Photocurrent density per absorber volume (chen2016d 1.152 mA/um3, p.1 / p.3): proposed
  `photocurrent_density_ma_per_um3` (photodetector; volume definition in condition).

## Missing orgs

- "OpSIS foundry" (zhang2014b p.5 Sec. 3), fab role (MPW access provider, D398 / D458).
- "BAE Systems" (ahn2007 p.6 Acknowledgments), borderline fab (staff support of the CMP process, D84b).
