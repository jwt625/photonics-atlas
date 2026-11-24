# lit_267 batch report

Distilled 2026-11-24. Papers: lit:sun2015a, lit:orcutt2011, lit:cardenas2009, lit:dumon2004a. All four cached texts match
their source rows (page-1 titles), none is a correction, no garbled text layer. Validation:
`merge_component_staging.py data/_staging/components/lit_267 --dry-run` -> +22 components, +97 metrics, 0 errors
(the 2 warnings name rows of other batches).

| paper | components | metric rows |
|---|---|---|
| dumon2004a | 7 | 25 |
| cardenas2009 | 3 | 17 |
| orcutt2011 | 4 | 24 |
| sun2015a | 8 | 31 |
| total | 22 | 97 |

## dumon2004a (LEOS 2003, 2 pages)

Rows: three photonic wires (400 / 450 / 500 nm x 220 nm, `waveguide_platform.straight`), three 3 um ridge to wire width
tapers (`waveguide_platform.other`), one racetrack (`resonator.ring`).

- Wire losses 33.8 / 7.4 / 2.4 dB/cm from the Fig. 1 table (Fabry-Perot cavity loss vs wire length, slope fit): `measured`,
  `cutback`, the +/- fit uncertainty in notes. No wavelength is stated for the loss measurement: `band unspecified`.
- Taper losses 0.27 / 0.22 / 0.19 dB, `le`, `author_estimate`: the paper builds this upper bound by replacing the facet
  reflection with its theoretical value (assumed input). The 200 um taper length is printed only for the 500 nm taper.
- Racetrack: Q 3086 (caption; text "over 3000") as `q_loaded`, wavelength 1500-1650 nm inferred from the Fig. 2 axis; FSR
  about 14 nm; finesse 27; width 500 nm, gap 230 nm, bend radius 3 um, straight 3 um as design labels.
- Not entered: the 76 % core confinement (no parameter); the abstract text layer prints "2.4dBkm" (page render: dB/cm).
- Fab: org_imec. "We have fabricated photonic wires using deep UV lithography"; every author lists imec (Ghent University -
  IMEC or IMEC vzw), as in the pathak2014a / bogaerts2006 rows. Borderline, see judgment call 1.

## cardenas2009 (Optics Express 2009)

Rows: etchless 1 um and 1.5 um waveguides (`waveguide_platform.straight`), 1 um bend series (`waveguide_platform.bend`).

- 0.3 +/- 0.02 dB/cm (1 um, TE) and 0.5 +/- 0.05 dB/cm (1.5 um), cut-back, `measured`. The 1 um row uses 1550 nm because the
  abstract states "0.3 dB/cm at 1.55 um", but the test source is an ASE centred at 1520 nm (p.4). The conflict is noted. The
  1.5 um row and the bend rows have no stated wavelength, so they use 1520 nm with `wavelength_inferred`.
- TE-to-TM extinction > 25 dB at the output entered as `per_db` (gt) on the 1 um row.
- Bend loss per bend: 0.007 / 0.03 / 0.15 dB at R = 50 / 20 / 10 um (Fig. 6 labels, +/- 0.005 dB) entered as
  `bend_loss_db_per_90`. The 90 deg angle is printed only in the abstract, and only for R = 50 um.
- Geometry: patterned widths 1000 / 1500 nm `derived` (printed in um, D157); core 70 / 90 nm `design_target` (the paper does
  not say whether the values come from simulation or measurement); BOX 3 um, PECVD cladding 2.5 um; 8 nm Si slab `simulated`
  (Fig. 1(c) is the simulated profile).
- Not entered: simulated mode size 1.01 x 0.52 um at the 1/e field point and confinement factor 0.38 (not facet MFD; no
  parameter); 0.3 nm rms AFM slab roughness (no parameter); the 3 dB/cm of the comparison etched strip waveguide (Fig. 4(b),
  a "typical" value given only for comparison, with no fabrication detail).
- Fab org_cornell_university ("We fabricate etchless waveguides", all authors Cornell); facility
  org_cornell_nanoscale_facility ("performed in part at the Cornell NanoScale Facility").

## orcutt2011 (Optics Express 2011)

Rows: grating coupler, 670 x 80 nm polysilicon waveguide, 20 um weakly coupled test ring, four-channel second-order ring
filter bank (`wdm.mrr`). Platform `other` (polysilicon gate layer of a bulk CMOS process, Si substrate locally removed by
XeF2).

- GC: minimum IL 4.8 dB at 1560 nm (`per_coupler`, method `unspecified`: the paper does not say how one coupler was
  isolated), 1-dB bandwidth 93 nm, simulated IL 5.5 dB; design 480 nm gaps / 590 nm bars -> period 1070 nm and fill factor
  0.551 (`derived`); "5 um mode size of the coupler" -> `mfd_chip_um` `author_estimate` (definition not stated, judgment
  call 4).
- Waveguide: the text says "approximately 55 dB/cm from 1520 to 1580 nm" and cites both the cut-back (Fig. 3(b)) and the
  ring fit (Fig. 3(c)). The 55 dB/cm is the best-fit simulated ring model, so that row is `derived` with method
  `unspecified`. The Fig. 3(b) cut-back points read about 47-53 dB/cm and are entered as a separate `extracted_from_figure`
  row. The two disagree, see judgment call 3.
- Ring: Q 7960 `q_loaded` (the paper calls these intrinsic Qs of weakly coupled rings, but the coupling regime is not
  determined from the data, D403); resonance about 1551.75 nm read off the axis.
- Filter bank: drop loss < 5 dB, adjacent crosstalk > 15 dB (printed "less than 15 dB" without a sign, read as suppression;
  judgment call 5), mean channel spacing 137 GHz over 4 banks, design radius 10 um (+10 nm per channel), width 670 nm, poly
  80 nm, bus-ring coupling 7.63 % (`simulated`) and 10.2 % +/- 1 % extracted (`derived`).
- Thermal drift 7.9 GHz/C converted to 63.5 pm/K at about 1551.9 nm (Fig. 6(a)), `derived` (chauhan2022 / palmer2026
  precedent). Fig. 6(a) shows "a single ring filter", and the paper does not say it is a channel of this bank (judgment call 6).
- Not entered: ring-ring coupling 0.3 % design / 0.63 % extracted (`power_coupling_pct` is defined as bus-to-resonator);
  mean ring frequency mismatch 30.9 GHz, linewidth mismatch 810 / 680 pm, wafer-level channel variation up to 600 GHz (no
  parameter in these units); heater thermal impedance 1.8 -> 44 K/mW after undercut (Fig. 6(b), no resonator / wdm
  parameter); the projected 3 uW/GHz tuning (not demonstrated); polysilicon roughness 6-8 nm rms (no parameter).
- Fab org_texas_instruments: "an unmodified Texas Instruments 28 nm bulk-CMOS process on 300 mm wafers" with all
  in-foundry processing shared. process_name "Texas Instruments 28 nm bulk-CMOS process (unmodified, 300 mm wafers)". The
  authors did the post-foundry substrate removal ("we use post-foundry processing"), but the author list spans MIT and
  Texas Instruments, so no authors' org is added (judgment call 2).

## sun2015a (IEEE JSSC 2015)

Rows: polysilicon defect-state microring PD (`photodetector.other`), the same PD ring as `resonator.ring` in its
overcoupled and critically coupled variants (D396), two 9-channel receive macros and the 9-channel transmit bank
(`wdm.mrr`), and two vertical grating couplers (macro version and best on the platform). Platform `other` (amorphized
polysilicon over a 1.2 um deep-trench oxide in bulk Si).

- PD: responsivity 0.2 A/W (one value printed for the 1280 and 1550 nm bands -> `band unspecified`), 3-dB bandwidth
  1.5 GHz at -1 V and 7.9 GHz at -10 V, capacitance 15 fF (`author_estimate`, "estimated"), radius 7.25 um (radius
  "matching" the modulator ring). See judgment call 7.
- PD rings: overcoupled Q 4000, 60 GHz FWHM, ER_i 2.4 dB; critically coupled Q > 9000, 26 GHz FWHM, ER_i 25 dB. Linewidths
  are GHz -> MHz conversions (`derived`). The O band is inferred because Fig. 6(b) uses a relative wavelength axis. Heater
  tuning estimate 108 mW per FSR (67 uW/GHz) is `author_estimate`, on the overcoupled ring because the wavelength-locked
  receiver uses those rings.
- Receive macros: crosstalk isolation 15 dB (overcoupled) / 23 dB (critically coupled) at 1 nm spacing; channel spacing
  1 nm `author_estimate` (heater-tuned grid set point); ER_i < 3 dB on the tested macro.
- Transmit bank: > 20 dB adjacent crosstalk isolation (tuned), nominal 1 nm spacing, every ring within 0.5 nm of its nominal
  resonance (`wavelength_spread_nm` le), FSR 9 nm, 9 channels, 384 um ring pitch. See judgment call 8.
- VGCs: 5 dB per coupler in the transceiver macros and 3 dB for VGCs elsewhere on the platform. Both are link loss-budget
  terms of unstated origin -> `author_estimate`, `loss_breakdown`, O band inferred.
- Not entered:
  - Modulator values (Q 8000 / 28.8 GHz FWHM, ER_i 15 dB, 2.7 GHz/V or 15 pm/V, 20 fF, 500 Ohm, 15.9 GHz RC bandwidth, eye
    ER / IL 6.8 / 2.2 and 7.6 / 1.8 dB), rule 2. The modulator is an EO-atlas candidate.
  - Values cited from the authors' earlier papers (rule 3 / D259): waveguide loss 40 -> 18 -> 10.5 dB/cm (refs. [18],
    [29]), dark current < 50 pA at -10 V ([33]), lock range 0.5 nm / 90 GHz ([36]), 3 um ring with 3.7 THz FSR and
    10 uW/GHz ([31]).
  - Generic 10 GHz/K (55 pm/K) thermal shift (Sec. II, not tied to a device).
  - Heater resistance 1 kOhm and 6 mW maximum heater power: `heater_resistance_ohm` is allowed only for phase_shifter;
    the values are in the ring's notes.
  - Fig. 20(d) estimated link budget (modulator 1.6 dB / ER 7.7 dB, ring ER_i penalty 3.7 dB, 90/10 split 1 dB, amplifier
    8 dB): modulator or setup values.
  - Fig. 4 schematic labels (100 nm, 230 nm): it is unclear which dimension each one marks.
  - Circuit metrics (energy per bit, sensitivity).
- Fab empty, process_name "0.18 um bulk CMOS memory periphery process": the paper never names the org that fabricated the
  chips. The authors are at MIT, UC Berkeley, CU Boulder and Micron, the process changes cite Micron's ref. [29], and
  "we build ... as part of a technology development reticle" names no org (D80b).

## Judgment calls for the auditor

1. dumon2004a fab org_imec, from a first-person fabrication sentence with authors at Ghent University-imec and IMEC vzw
   (pathak2014a precedent). The alternative is to leave fab empty.
2. orcutt2011: fab is org_texas_instruments only. The post-foundry XeF2 substrate removal was first-person ("we") by an
   author list spanning MIT and TI, so MIT is not added (D154 / D440). The rows may need an `exclude_values` review for
   the benchmark, since the chips were post-processed.
3. orcutt2011 waveguide 55 dB/cm is entered as `derived` (ring-model fit), with a separate figure-read cut-back range of
   47-53 dB/cm. The printed text value disagrees with its own Fig. 3(b).
4. orcutt2011 "5 um mode size of the coupler" is entered as `mfd_chip_um` `author_estimate`. The definition is unknown;
   the row could be dropped.
5. orcutt2011 crosstalk "less than 15 dB" is read as > 15 dB suppression, supported by Fig. 5(a).
6. orcutt2011 7.9 GHz/C: Fig. 6(a) shows "a single ring filter", and the text calls it "the filters' effective
   thermo-optic coefficient". The value is on the filter-bank row; D159 would drop it if the ring is not a bank channel.
7. sun2015a PD responsivity and bandwidths are stated without a reference in the value sentence. The preceding sentence
   cites the authors' ref. [33] (Mehta et al., OL 2014) for the detector concept, and the dark current sentence cites [33]
   explicitly. Entered as `measured` (D408), but the values may come from [33]. The values are given for "this
   photodetector" before the two coupling variants are distinguished, so they sit on one photodetector row (D159 /
   D254 risk).
8. sun2015a transmit bank: a bank of ring modulators is entered as `wdm.mrr` with spectral metrics only (crosstalk,
   spacing, FSR, spread, pitch). The modulator metrics stay out (rule 2). The alternative is no row.
9. sun2015a VGC 5 / 3 dB as `author_estimate` link-budget terms with the O band inferred.
10. cardenas2009 0.3 dB/cm at 1550 nm (abstract) against the 1520 nm ASE source; the 1.5 um and bend rows use 1520 nm
    inferred.

## Missing fab / facility orgs

None. All needed ids exist: org_imec, org_cornell_university, org_cornell_nanoscale_facility, org_texas_instruments.

## Registry gaps (skipped value + locator + proposed definition)

- `ring_ring_coupling_pct` (wdm, resonator): orcutt2011 0.3 % design / 0.63 +/- 0.08 % extracted (p.9 Fig. 4 caption;
  p.10 Fig. 5 caption). Proposed definition: "power coupling between adjacent rings of a coupled-ring / higher-order
  filter".
- `heater_resistance_ohm` for resonator / wdm: sun2015a 1 kOhm integrated microring heater (p.11).
- `thermal_impedance_k_per_mw` for resonator / wdm / phase_shifter: orcutt2011 heater temperature rise per power, 1.8 ->
  44 C/mW after substrate removal (p.11 Fig. 6(b)). Proposed definition: "heater temperature rise per mW of heater power
  (linear fit)".
- `resonance_mismatch_ghz` (wdm): orcutt2011 mean frequency mismatch 30.9 GHz between the two rings of second-order
  filters (p.10 Fig. 5(d)).
