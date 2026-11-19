# lit_210 batch report

Distilled 2026-11-18. Papers: lit:guan2014b, lit:jeong2020, lit:lu1994, lit:koyama2013. All four texts match their
source rows (page-1 title). Validation: `merge_component_staging.py data/_staging/components/lit_210 --dry-run` ->
+9 components, +78 metrics, 0 errors.

| paper | components | metric rows |
|---|---|---|
| guan2014b | 5 | 33 |
| jeong2020 | 2 | 35 |
| lu1994 | 0 | 0 |
| koyama2013 | 2 | 10 |

## guan2014b (JSTQE 2014, invited overview, Si reconfigurable lattice filters)

Components: unit-cell lattice filter (`wdm.cascaded_mzi`), four-cell lattice filter (`wdm.cascaded_mzi`), 0.5 um Si rib
waveguide (`waveguide_platform.straight`), p-i-n carrier-injection phase shifter (`phase_shifter.other`), polished
AR-coated facet with lensed fiber (`fiber_chip_coupler.edge`). Platform `soi_rib` (rib waveguides on SOI stated, p.4).

Entered: 10 GHz FSR (design, `author_estimate`); unit-cell 400 MHz 3-dB bandwidth (Fig. 8 caption, MHz -> GHz,
`derived`); 22 dB fiber-to-fiber device insertion loss (p.7); 5-7 dB per facet (`author_estimate`, "We estimate", no
method); 0.3 dB/cm for the 0.5 um rib (OVNA, C band inferred); 4 dB induced loss per 2 pi of the p-i-n phase shifter
(C band inferred); four-cell Fig. 11(b) -1 dB 1.8 GHz and -3 dB 2.5 GHz; stack geometry (500 nm core, 250 nm slab,
250 nm rib height as etch depth, 3 um BOX, 0.5 / 3.0 um widths, 300 um bend radius, 200 um taper).

Not entered:
- Q 2.7e5 (p.5, cites ref. [10]) and 13 mA per 2 pi (p.5, cites ref. [13]): cited values (rule 3).
- Fig. 10 pole magnitudes 0.11 / 0.87: caption cites the authors' ref. [13] (D259a).
- Fig. 11(a) state (-1 dB 600 MHz, -3 dB 1 GHz, -20 dB 2.8 GHz, > 30 dB extinction): the p.6 sentence attributes Fig.
  11(a) to ref. [13] (D259 / D408). Fig. 11(b) has no attribution and is kept.
- Reconfiguration < 16.67 ns, 30-50 ns settling, 15-30 mW heat load (Fig. 14, caption and sentences cite the authors'
  ref. [21], D259a).
- Directional coupler < 3 % splitting error (cites ref. [10]).
- Worst-case unit-cell round-trip loss 0.6 dB (assumption-based, no parameter).
- Two-tone SFDR 61.6 dB (p.7; conclusion prints 61.5 dB): link-level metric, no parameter (not proposed).
- p-i-n threshold voltage 0.85 V (p.6): `forward_voltage_v` is not allowed for `phase_shifter` (registry gap below).
- Fig. 11(b) -20 dB width 7.6 GHz: no `bw_20db` parameter (not proposed; single value).
- Fig. 5(c) photograph labels 13 mm / 6 mm: not tied to one device.

Orgs: fab sentence p.4 Sec. IV "fabricated in BAE Systems CMOS foundry and Microlab/Marvell Nanolab facilities,
University of California, Berkeley", followed by first-person process steps. Entered fab `org_university_of_california_davis`
(all authors at UC Davis at the time), facility `org_marvell_nanofabrication_laboratory`. Missing: **BAE Systems**
(fab, foundry; p.4 Sec. IV), not in `organizations.csv` / `org_aliases.csv` (same gap as lit:shi2013). process_name =
printed wording "BAE Systems CMOS foundry, 6-in SOI, DUV stepper lithography with photoresist reflow".

## jeong2020 (JLT 2020, polarization-diversified 16-lambda DeMUX)

Components: C-band polarization-diversified DeMUX and O-band TE DeMUX, both `wdm.other` (interleaver + AWG combination),
platform `soi` (Si wire, PBS/PR on a partial rib).

Entered (C band): excess loss 5-6 dB (die A, TE and TM, reference-waveguide normalized) and 5-6 dB over dies A-C
(TE, n = 3); PDL < 0.5 dB; channel spacing about 100 GHz; interleaver suppression of the AWG periodic response > 25 dB
(`extinction_db`); lambda1-lambda8 group center 1555 nm; TE / TM grid difference < 0.1 nm (`wavelength_spread_nm`);
3-dB width > 0.42 nm; Table II crosstalk at Ch01 (adjacent 22.1 dB, non-adjacent 19.5-34.6 dB, subtotals 13.25 / 22.04
dB and total 12.71 dB cumulative); Fig. 8 total crosstalk 12.2-16.8 dB over all outputs; 16 channels; footprint 4.76
mm2; Table I design values (FSR 25.6 / 12.8 nm, spacing 12.8 / 0.8 nm, 32 arms, ng 2.7515, widths 2 um / 480 nm); 200
nm core, 2 um BOX. O band: design FSR 14.6 / 7.3 nm, spacings 7.3 / 0.8 nm (~140 GHz), 16 channels, length 2.0 mm from
the Fig. 13 label, stack.

Not entered:
- Loss split 0.5 / 0.5 / 4.5 dB and AWG 1.2 dB (attributed to refs. [9], [13], [14]); crossing < 0.1 dB / < -30 dB (ref.
  [10]); waveguide loss < 0.5 dB/cm (ref. [22]); sigma 120 GHz (ref. [22]).
- Channel grid +/-< 5 GHz and die-to-die center deviation +/-< 20 GHz (p.6): spreads printed in GHz;
  `wavelength_spread_nm` would need a GHz -> nm conversion at an assumed wavelength (registry gap below).
- Table I effective index 2.3343 and kappa_DC 0.5 / 0.2 / 0.2 / 0.04 (no wdm parameter for neff or DC coupling).
- O-band crosstalk / excess loss: only "worse than" C band (no number); O-band chip width: text prints "0.9-um-wide and
  2.0-um-long" (unit misprint), Fig. 13 labels only the 2.0 mm length.
- 32 Gbps NRZ eye diagrams (system test); Fig. 8 Ch01 -13.7 dB (method cross-check of the Table II total).
- Table III comparison columns of refs. [16]-[19] (other works).
- PBS/PR, crossing, interleaver and AWG as separate rows: no value isolated to any of them in this paper.

Orgs: fabrication sentence p.3 Sec. III is passive with no org ("fabricated by ArF-immersion lithography technology on
a 300-mm SOI wafer [22]"): fab empty, process_name = printed wording. No facility statement (NEDO acknowledgment is a
program). No missing orgs.

## lu1994 (JLT 1994, double-layer network architecture)

0 components. Architecture / theory paper: path loss, SNR, crossover, element and driver counts are formulas in the
per-switch loss L and per-switch crosstalk |X|; no fabricated or designed physical device. The "0.2 dB loss in each
switch on average" (p.1) and "|X| usually 20 dB" (p.2) are generic technology figures, not the paper's own device;
Fig. 15 uses |X| = 20 dB, m = 0.01 as assumed inputs. Scan read from the text layer and page renders (tables / figures
are formulas and curves of those formulas only).

## koyama2013 (IPRM 2013, non-blocking 4x4 InAlGaAs/InAlAs MZ switch fabric)

Components: 4x4 fabric (`switch_fabric.mzi_mesh`, six 2x2 elements in four stages) and the 2x2 element measured on the
same wafer (`switch_fabric.other`, D158). Platform `inp`.

Entered: fabric extinction about 20 dB (TE and TM, Fig. 7, wavelength not stated: `band unspecified`); 4x4 ports;
6 mm length and 6 mm x 1 mm footprint (derived); element extinction per port read off Fig. 5(c) at 1520 nm (port 1'
about 18 dB, port 2' about 19 dB, +/- 1 dB, `extracted_from_figure`); 2x2 ports; element length about 4 mm (Fig. 5(b)
label).

Not entered:
- MMI 3-dB coupler 215 um and phase shifter 200 um (Fig. 2 labels): the schematic sentence attributes the element design
  to the authors' ref. [3] (D259; geometry kept out, judgment call (e)).
- About 5 mA and about 3 ns (earlier 4x4 fabric, ref. [4]).
- Offset bias 6.5 mA and switching currents (~6.5 / ~24.5 mA, Fig. 5(c)): no switching-current parameter (notes only).
- Fabric crosstalk ("almost the same", no number); Fig. 7 relative powers are not absolute insertion losses.

Orgs: fabrication sentence p.1 Sec. II is passive, no org named (authors at Waseda University and Hitachi): fab empty;
process_name = printed "i-line stepper photolithography and ICP-RIE (improved process)". NEDO / SORTE acknowledgment is
funding. No missing orgs.

## Judgment calls

- (a) guan2014b fab = UC Davis from the first-person process steps on p.4-5 ("We use a second lithography process",
  "we use dry thermal oxidation", "we densify the cladding", "we add an anti-reflection coating") with all authors at UC
  Davis at the time (rule 12, D419 / D440 post-processing precedent); BAE Systems would join as foundry fab once it is in
  the registry. Marvell Nanolab printed as "Microlab/Marvell Nanolab" mapped to `org_marvell_nanofabrication_laboratory`.
- (b) guan2014b geometry from sentences that cite the authors' ref. [10] for the process / taper (3 um BOX, 200 um
  taper) entered as `design_target` because the sentences describe this paper's devices in the first person; the Q and
  13 mA values in citing sentences stay out (rule 3).
- (c) guan2014b Fig. 11 split: (a) removed (sentence cites ref. [13]), (b) kept (no attribution). Fig. 11(b) port label
  conflict (caption "Notch filter H21" vs text / caption "H11 ... -1-dB bandwidth of 1.8 GHz") noted, values as printed.
- (d) jeong2020 one composite `wdm.other` row per band rather than separate AWG / interleaver / PBS/PR rows: only the
  composite was measured; sub-filter design values carry the sub-filter in `condition`. Two `width_nm` rows (W_DL 2 um,
  W_WG 480 nm) distinguished by condition. Table I values entered as `author_estimate` (design inputs of the
  calculation), ng with 1550 nm from the Table I header.
- (e) koyama2013 Fig. 2 dimensions kept out (element design attributed to ref. [3]); fabric extinction entered once as
  "about 20 dB" (abstract / p.2), the conclusion's "up to about 20 dB" in notes.
- (f) koyama2013 element extinction read per output port off Fig. 5(c) (max over min of the same port); the paper prints
  no element ER number.
- (g) lu1994: no rows (theory paper; generic per-switch numbers are not a component of this source).

## Registry gaps

- `forward_voltage_v` for `phase_shifter`: guan2014b p-i-n threshold (turn-on) voltage 0.85 V (p.6 Sec. V). Proposed:
  widen `forward_voltage_v` to phase_shifter ("forward / turn-on voltage of a carrier-injection phase shifter, criterion
  in condition").
- Frequency-domain spread for wdm: jeong2020 channel grid deviation +/-< 5 GHz and die-to-die center deviation
  +/-< 20 GHz (p.6 Sec. IV-A). Proposed: `wavelength_spread_ghz` (wdm, laser, resonator), "spread of channel / resonance
  frequency across channels or dies, +/- as stated, kind in condition".
- No proposal (single values or system-level): SFDR 61.6 dB (guan2014b p.7), -20 dB passband width (guan2014b Fig. 11),
  switching current of a carrier-injection switch element (koyama2013 Fig. 5(c)).
