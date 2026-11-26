# lit_291 batch report

Batch lit_291 (D780, family C): heck2012, siew2021, lim2014, vlasov2012. Distilled 2026-11-26 under Contracts v4-v7.
Totals: 38 components, 119 metric rows. `merge_component_staging.py --dry-run`: 0 errors (the 2 warnings are on
merged rows of other papers). Page-1 titles match the source rows for all four papers. None is a correction or
another paper. All four are reviews, overviews or invited papers: values credited to references are not entered
(rules 1 and 3, D259 / D408).

| paper | components | metrics |
|---|---|---|
| heck2012 | 2 | 7 |
| siew2021 | 29 | 75 |
| lim2014 | 7 | 37 |
| vlasov2012 | 0 | 0 |

## heck2012 (Hybrid silicon PIC technology, JSTQE 2013 invited review, UCSB)

Rows: two passive hybrid Si / III-V tapered mode converters, Type 1 and Type 2 (`waveguide_platform.transition`,
platform `other` as in merged hybrid III-V/Si taper rows). Each row has transition_loss_db (0.5 / 0.3 dB per
transition, 1550 nm, cutback offset and slope fit of Fig. 4, `measured`), the 2 um Si width where the taper starts,
and the Fig. 2 taper-length label (80 / 100 um, `extracted_from_figure`). The Type 1 row also has the 0.5 um design
tip width.

Not entered:
- Taper back reflection below -41 dB for both types (p.3). `back_reflection_db` is not allowed for waveguide_platform
  (registry gap, below).
- Hybrid waveguide loss: the slope of the Fig. 4(a) fit is not printed.
- All of Sec. III and Sec. IV, because every result is credited to a reference, mostly the authors' own earlier work
  (D259 / D259a): DFB lasers [56], [57], [59]; MLL [60]; SOAs [61], [44]; 2R regenerator [63]; EAMs [64]-[66] (EO
  anyway); PBS / PSR [67], [68], [70]; ring isolator 9 dB [74]; ULLW 0.4 / 0.8 dB transitions and 1.2 dB/m [86]; AWG
  laser [36]; buffer [89]; DQPSK receiver PD 0.64 A/W [90]; beam steering [42]; QWI CWDM DFB array [49]; EAM array
  [93]; CMOS switch [94]. The Fig. 6, 9, 10, 14, 26, 27, 32 and 34 data belong to those cited works.

Fab / facility: both empty. The text says only that the tapers "were fabricated", with no org named (D80b). The
acknowledgment thanks people for discussions only.

Judgment call (auditor): the taper value sentence and the Fig. 4 caption carry no citation, so the D408 test allows
the values. However, the paragraph cites the authors' refs. [37] and [38] "for details about the designs". [37] is
the authors' 2013 Photon. J. paper, titled characterization of insertion loss and back reflection in passive hybrid
silicon tapers, so the data probably also appear there (forthcoming at the time). Under the D259 "even forthcoming"
clause both rows would be deleted. Recommendation: keep them, because no value or figure is attributed to [37] and
D408 applies only to an explicit attribution. Delete both components if the coordinator reads the design-details
citation as an attribution.

## siew2021 (Review of Si photonics technology and platform development, JLT 2021, all authors AMF)

The paper mixes a literature review with AMF's own platform data. Entered: AMF data printed without a reference. Fab
on every row is `org_amf` ("fabricated at AMF", Fig. 3; "MPW wafers running in AMF in 2019 and 2020", p.5).
- MPW waveguides (PCM cutback, Fig. 6): Si channel waveguide 1.48 dB/cm and Si slab (90 nm slab rib) waveguide
  1.04 dB/cm, entered as wafer means with `measured` basis and no wavelength (`band: unspecified`). Also 220 nm core,
  90 nm slab design, and 89.1 nm measured slab (891 A, `derived`).
- Table III, AMF Si PDK library: 12 rows (C and O band edge coupler, grating coupler, 1x2 MMI, 2x2 MMI, crossing, plus
  C-band PBS and PBRS / PBRC). Table VI, AMF SiN PDK library: 8 rows (C and O band grating coupler, 1x2 MMI, 2x2 MMI,
  crossing). All are `author_estimate` with `statistic: typical` and the printed bounds (D544 velha2016 precedent: no
  measurement or method shown). MMI "Loss" is entered as excess_loss_db. The Si grating couplers also have the 70 nm
  grating etch and the 220 nm core.
- Table V SiN platforms (rows without references): LPCVD 400 nm (< 0.42 dB/cm at 1550 nm, < 0.22 at 1580 nm), PECVD
  400 nm (< 3.01 and < 1.25 dB/cm) and PECVD 600 nm (2.5 dB/cm at 2000 nm), all `author_estimate`. The Fig. 7 wafer
  means (0.37 / 3.00 dB/cm at 1550 nm) are `measured`, on the 400 nm rows.
- Fig. 8 SiN-to-Si vertical transitions (`si_sin_multilayer`): LPCVD and PECVD rows, each with < 0.2 dB over 1500-1560
  nm (TE), a wafer-map mean of 0.170 / 0.146 dB, and an inter-layer oxide gap of 150 / 250 nm.
- Fig. 15 AMF PDK Ge PDs: vertical row has 1.12 A/W at -1 V and 25 / 28 GHz at -1 / -3 V. Lateral row has ~0.83 A/W at
  -1 V, 31 GHz at -1 V, > 40 GHz at -5 V, and 7 nA at -3 V.

Not entered:
- Table I (foundry platform comparison) and Table II (PDK performance of AMF, AIM, CEA-Leti, GF, IHP, imec, VTT). Every
  row carries a reference; the AMF row cites [48], the AMF PDK3.1 user manual.
- Table IV (other foundries' SiN processes, referenced) and the Table V rows 430-648 nm [83] and 1310 nm [84] (the
  authors' group's earlier papers).
- Tables VII and VIII (literature modulators and PDs). The Table VIII AMF rows also cite [48].
- Fig. 11 modulator chart (refs. [93]-[102]) and the "1 dB or less" packaging loss [129].
- AMF PDK MZM data (p.10, Fig. 12-13): 4.0 mm device Vpi 5.9 V and 29 GHz at 0 V, > 40 GHz at -3 V; 2.4 mm device
  0.8 Vpi at 7 V, 38-40 GHz at 0 V, ER 3.947 dB at 56 Gb/s, 3.9-4.3 dB ER at 3 Vpp; doping sheet resistances 4100 /
  1640 ohm/sq; S11 < -13 dB. These stay out under rule 2 and are an EO-atlas candidate.
- Fig. 5 CD statistics (499 +/- 6.4 nm for a 500 nm waveguide): the waveguide type is not stated (D159), so the value
  is in component notes only.
- Fig. 4 grating-etch remaining Si (1503 A): process monitor, notes only.
- Vertical PD dark current: shown only on the Fig. 15(a) log plot, not printed.
- Thermo-optic coefficients (material constants).

Facility: none. The acknowledgment thanks AMF staff (D72).

Judgment calls (auditor):
1. Table III / VI / V values are entered as AMF platform figures (`author_estimate`, typical). The source is clear (the
   authors are AMF and say "we develop ... Table III lists the typical performance"), but no measurement is shown.
2. The Fig. 7 wafer means are placed on the 400 nm rows. Fig. 7 does not state a thickness; the text introduces it as
   an example of the Table V platforms at 1550 nm, where Table V gives 400 nm. The Fig. 7 caption swaps
   (a) PECVD / (b) LPCVD. The panel titles and the text agree with each other (LPCVD 0.37, PECVD 3.00), and those are
   followed (D417 note).
3. "x +/- y" wafer statistics are entered as `statistic: mean` with the +/- in notes (velha2016 precedent). The paper
   names the average only for Figs. 4-5.
4. Table VI C-band 2x2 MMI "Loss <0.7" has no printed unit; dB is assumed from every other entry in the table (noted).
5. PD subtype is `photodetector.other`: the text never states waveguide coupling for the AMF PDs (D80h). Wavelength
   1550 nm is inferred from the Table VIII caption.
6. Si PDK edge couplers have an empty platform: the facet layer is not stated (D82f / D422).

## lim2014 (Review of Si photonics foundry efforts, JSTQE 2014 invited, all authors IME A*STAR)

Entered: the interim results of the IME / GF / Alcatel-Lucent technology transfer on GF's 200 mm 0.18 um line
(Sec. IV-B). Fab on every row is `org_globalfoundries` ("fab out from GF's line", "fabricated in GF",
"fabricated and verified in GF line"). IME ran the technology transfer; that role is in the notes, not fab.
- Si channel and rib waveguides (500 nm wide, 90 nm slab, 220 nm Si / 3 um BOX): mean loss ~2 and ~0.8 dB/cm with
  std ~0.2 dB/cm each, 52 dies, cutback. Wavelength: C band inferred ("at central wavelength" of the GCs, mean 1538
  nm).
- 5 um radius bend: 0.016 dB per 90 deg.
- Wafer-test grating coupler: ~6 dB coupling loss, mean central wavelength 1538 nm, std 2.8 nm across dies
  (`wavelength_spread_nm`, std).
- Waveguided vertical pin Ge PD, 8 x 25 um: ~11 nA mean dark current at -1 V (52 dies), 5-6 mA/cm2, 28 fF mean at
  -1 V, 1.06 A/W internal at -1 V and 1550 nm, TE, 16 dies (own de-embedding, `measured`), > 20 GHz at -1 V.
  Dimensions 8 x 25 um (width x length from the Fig. 9 axis title) and Ge > 500 nm.
- Sibling PD rows 8 x 40 and 7 x 25 um: Fig. 9 mean markers ~18.0 / ~8.6 nA (`extracted_from_figure`, +/- 0.5 nA),
  plus the shared 5-6 mA/cm2 density statement and the shared Ge thickness.

Not entered:
- p.4 platform statements. The ~180 nm Si nanotaper with "~2 to 3 dB ... achievable" (lensed fiber) is a generic
  platform-capability statement with no device, data or fabricating org, not presented as a result. The suspended
  oxide mode converter (~1-2 dB/facet, > 2 um tolerance, > 100 nm operation range) is introduced with ref. [21]
  (rule 3 / D80i).
- Table I (MPW platform comparison, "extracted from Ref. [22] and [23]"; pricing).
- Fig. 5 revenue forecast [5], the 50 % GC improvement [32], and the dark-current comparison [36]-[38].
- Forward current > 10 mA at 1 V and the 1e6 on/off ratio: no registry parameter; single values, not proposed.
- Fig. 10(b) capacitance points (~23.5 / 28.3 / 39.3 / 47 fF at ~175 / 200 / 280 / 320 um2): the points carry no
  dimension labels and the 280 um2 point matches no Fig. 9 design (D156).
- Fig. 2 deep-trench depth of 120 um: geometry of the dicing trench, not a component metric.

Facility: none.

Judgment calls (auditor):
1. Fab is `org_globalfoundries` only, with IME's technology-transfer role in the notes. The process_name is my
   wording of the printed line: "GF 200 mm 0.18 um CMOS manufacturing foundry line (IME / GF / Alcatel-Lucent
   technology transfer)".
2. The 5-6 mA/cm2 density is stated "for all the PDs". It is entered on all three PD rows; the other 5 of the 8
   designs have no rows. Bias -1 V is taken from context.
3. The GC ~6 dB is scoped `per_coupler` with method unspecified. Its wavelength is 1538 nm, inferred from the mean
   central wavelength.

## vlasov2012 (Si CMOS-integrated nanophotonics beyond 100G, IEEE Commun. Mag. 2012, IBM)

0 rows. This is a market / standards perspective with no own device results. The device statements are cited:
density 0.5 mm2/channel and 40 x 25 Gb/s on a 5 x 5 mm2 die [17]-[20], the 1490 nm laser choice [12], and the DFB
array [24]. Fig. 2 is a scaling estimate (LAN-WDM footprint and line rate vs CMOS node), not a component
measurement. The link-budget and BGA / LGA areal-density numbers are system estimates.

## Missing orgs

None. `org_amf` and `org_globalfoundries` exist in the registry. The IME role in lim2014 is a note only
(`org_astar_ime` exists).

## Registry gaps

- `back_reflection_db` on `waveguide_platform` (transition). Skipped value: heck2012 Type 1 and Type 2 hybrid
  tapers, back reflection below -41 dB (p.3 Sec. II-A). Proposed definition: as for couplers, back-reflection
  magnitude of an on-chip transition, positive dB below the input.
