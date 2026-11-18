# lit_201 batch report

Distilled 2026-11-18. Papers: lit:cheng2023a, lit:ji2022, lit:klaus2012, lit:lee2014. All four cached texts match
their source rows (page-1 titles checked; ji2022 title differs only by the "ffi" ligature). Institutional download
stamps ignored. Totals: 14 components, 91 metric rows. `merge_component_staging.py --dry-run`: +14 components,
+91 metrics, 0 errors (one pre-existing warning on another batch, lit ni2025b).

## lit:cheng2023a (8 components / 54 metric rows)

Silicon PBS from a multimode anti-symmetric apodized Bragg grating (MASABG) with a dual-core adiabatic TE0/TE1 mode
(de)multiplexer, 220 nm SOI, EBL, single full etch.

- `cmp_lit_cheng2023a_masabg_pbs` (polarization.pbs, 12 rows): measured average IL 1.0 dB (TE, Drop) and 0.4 dB (TM,
  Thru) over 1415-1675 nm, normalized to straight waveguides (per_component, reference_structure); measured
  PER > 20 dB over 1432-1673 nm and > 30 dB over 1485-1670 nm (band edges read off Fig. 8(c)-(d), +/- 5 nm; printed
  bandwidths ~240 / ~190 nm in notes); simulated PER 60 / 46 dB and IL 0.2 / 0.1 dB at 1550 nm; length 85 um
  (Table I), W 800 nm, Si 220 nm, 1 um SiO2 cladding.
- `cmp_lit_cheng2023a_te0_te1_mode_demux` (mode_converter.mdm_mux, separate test device, 12 rows): measured average
  IL 0.4 dB (TE0 to TE0) and ~1.6 dB (TE1 to TE1) over 1400-1700 nm (scope unspecified: normalization not stated for
  this device); simulated IL < 0.13 dB and mode ER > 17 dB over 1400-1700 nm; taper lengths 15 / 35 / 5 um, widths
  500 / 800 / 300 / 200 nm, Si 220 nm.
- Six test grating couplers `cmp_lit_cheng2023a_te_gc1..3`, `tm_gc1..3` (fiber_chip_coupler.grating, 30 rows):
  minimum IL at each of the two fiber angles read off Fig. 12(c)-(h) (+/- 0.5 dB / +/- 5 nm), scope unspecified (GC
  pair joined by a waveguide; the paper does not say whether the plotted IL is per pair or per coupler); Table II
  pitch, duty cycle 0.55 (undefined, kept as printed, D253), subwavelength period 400 nm (TE), full 220 nm etch.

Not entered: PBS design values S 400 nm, hole widths 160 / 50 nm, Bragg periods 400 / 200 nm, N = 30, Nt = 21
(period_nm / n_periods not allowed for polarization; in notes); simulated ER bandwidths ~280 / ~240 nm (edges not
printed); +/- 10 nm fabrication tolerance (no parameter); mode demux gaps 1.2 / 0.16 / 1.2 um (gap_nm not allowed for
mode_converter); mode demux measured leakage (only "low crosstalk" printed); Table I values of other works (rule 3);
TM GC etch width 160 nm (no parameter, in note); GC design centre wavelengths (in labels only).

Orgs: fab empty (passive fabrication sentence, no org named); facility
`org_center_of_optoelectronic_micro_and_nano_fabrication_and_characterizing_facility` on all 8 rows (acknowledgment
"for the support in device fabrication", p.7). No missing orgs.

## lit:ji2022 (2 components / 19 metric rows)

Scope decision: in scope. The paper builds an all-fiber fused-taper fan-in / fan-out (reverse-tapered MCF spliced to
a down-tapered SMF-28 bundle): a fiber-only passive part, which D80f / D411 keep in scope, and the registry subtype
`fiber_interface.fan_out` is defined as "MCF fan-in/fan-out" (precedents shikama2017, zhong2026, thomson2007).
Platform left empty (fiber stack; D422 / shikama2017 precedent).

- `cmp_lit_ji2022_fifo_mcf1` (Fibercore SM-7C1500, 35 um spacing, ratio 2 + TEC; 10 rows) and
  `cmp_lit_ji2022_fifo_mcf2` (Hengtong trench-assisted, 37.6 um, ratio 1.86; 9 rows): measured mean IL 0.64 / 0.74 dB
  at 1550 nm (device_total, single FI/FO, +/- in notes); per-core IL ranges 0.42-0.78 / 0.40-1.20 dB (Fig. 8(a)-(b));
  mean return loss > 61 / > 65 dB; mean FI + 4 m MCF + FO crosstalk 66 / 67.5 dB and worst plotted pair ~52 / ~60 dB
  (Fig. 8(c)-(d)); 7 channels; MCF pitch (specification), 70 um interface pitch (design), MCF MFD 6.4 / 10.4 um
  (specification); MCF1 calculated interface coupling loss 0.59 dB at 70 um (simulated, per_interface).

Not entered: reverse-tapering loss < 0.1 dB per channel ("ratio around 2", MCF not identified, D159, in notes);
interface MFDs 11.0 / 12 / 13.9 um and bundle 12 um (no fiber_interface MFD-at-interface parameter, registry gap);
MCF-MCF splice losses of the crosstalk test assembly (test splices, not the device); calculated < 0.6 dB over
70-100 um and MFD-only < 0.1 dB estimate (notes); process settings (flame, splicer, cleaver).

Orgs: fab empty ("we fabricated" with authors at Fudan University, Shanghai University / Jiangsu Hengtong Fiber
Science and Technology, City University of Hong Kong; sentence names no single org, D154 / D395). No facility.

## lit:klaus2012 (2 components / 14 metric rows)

Scope decision: bulk free-space MCF MUX/DEMUX with fiber in and fiber out (SMFs and MCF) kept as a fiber-coupled
passive part (D80f / D411; jung2018 C-lens isolator precedent), platform `other`. Differs from fontaine2019 (D642,
fiber at input only).

- `cmp_lit_klaus2012_mux_19ch` (10 rows): MUX - 2 m MCF - DEMUX total IL mean 1.3 dB (19 channels, 1.55 um ASE,
  fiber_to_fiber), per-channel 1.1-1.55 dB (Fig. 6(a)), centre channel 1.22 dB; maximum aggregate crosstalk ~50 dB;
  nearest-neighbour average crosstalk 56.5-64 dB (Fig. 6(b)); simulated minimum field-mismatch coupling loss 0.01 dB
  (per_coupler, wavelength inferred); 19 channels; design MCF MFD 7.8 um; measured SMF MFD 10.8 um; centre beam
  ~0.5 mm (author_estimate, converted).
- `cmp_lit_klaus2012_mux_7ch` (4 rows): IL < 1.5 dB and crosstalk ~50 dB from the conclusion sentence covering both
  devices (author_estimate, scope unspecified, see judgment call (d)); 7 channels; accommodated core pitch 30-100 um.

Not entered: loss-budget terms (connector < 0.3 dB spec sheet, uncoated MCF facets ~0.3 dB, AR surfaces ~0.25 dB);
lens focal lengths 2 / 3 mm and 127 mm separation (no focal_length parameter; registry candidate from D432);
volumes 20 x 35 cm and 30 x 43 cm (notes); cone angles; "few tenths of a dB" mismatch penalty; lossless < 0.005 dB
condition (theoretical).

Orgs: fab empty ("We designed and fabricated" with authors at NICT and Optoquest Co. Ltd.; no single org named).
Optoquest Co. Ltd. is not in the registry (only relevant if the coordinator assigns fab; p.1 affiliation).

## lit:lee2014 (2 components / 4 metric rows)

- `cmp_lit_lee2014_fifo_7core` (fiber_interface.fan_out, platform other): measured IL < 0.5 dB (device_total, band
  unspecified); 7 channels.
- `cmp_lit_lee2014_mcf_sc_connector` (fiber_interface.connector): measured IL < 0.5 dB (per_interface, band
  unspecified); 7 channels.

Not entered: protection optical-switch unit recovery time < 5 ms (system-level unit with FPGA / switch / PDs, switch
type not stated; out of scope); module size 25 mm x 88 mm (in core_material, no clear footprint orientation).

Orgs: fab empty (passive fabrication sentences; all authors Hitachi Central Research Laboratory, D80b). No facility.

## Judgment calls

(a) ji2022 in scope as `fiber_interface.fan_out` (all-fiber passive FIFO, D80f / D411), platform empty.
(b) klaus2012 and lee2014 free-space bulk FI/FO devices kept in scope (fiber in and out), platform `other`.
(c) cheng2023a fab empty with the HUST WNLO facility as facility only ("support in device fabrication"); a D448 reading
    would add `org_huazhong_university_of_science_and_technology` as fab (li2026aa precedent kept fab empty).
(d) klaus2012 7-channel IL < 1.5 dB / crosstalk ~50 dB entered as author_estimate from the joint conclusion sentence
    (a bound stated for each device, not a "typical" family value; D254 boundary); without them the row would have no
    performance metric.
(e) cheng2023a PER band edges and GC minima read off figures (`extracted_from_figure`); GC scope unspecified (pair vs
    per-coupler not stated).
(f) ji2022 / klaus2012 fab empty: first-person "we fabricated" across authors at several orgs (D154 / D395).
(g) klaus2012 19-channel simulated 0.01 dB entered as `per_coupler` (one MUX or DEMUX, field-mismatch term only).

## Registry gaps

- `period_nm` / `n_periods` for polarization (cheng2023a Bragg period 400 nm, apodized 200 nm, N 30 / Nt 21, p.4).
- `gap_nm` for mode_converter (cheng2023a 1.2 / 0.16 / 1.2 um, p.4; already listed in D533).
- Mode-field diameter at the device interface for fiber_interface (`mfd_chip_um` widened or a new
  `mfd_interface_um`): ji2022 11.0 / 12 / 13.9 um and bundle 12 um (p.4); thomson2007 precedent.
- `focal_length_um` (micro_optics / fiber_interface): klaus2012 2 mm / 3 mm (p.3), candidate from D432.
- Optical-switch recovery / protection-switching time (lee2014 < 5 ms, p.2): not proposed (system level).
