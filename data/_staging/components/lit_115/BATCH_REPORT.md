# lit_115 distill report (2026-11-08)

Batch: 8 papers (polarization family), 20 components, 139 metric rows. Validator: `merge_component_staging.py
data/_staging/components/lit_115 --dry-run` -> +20 components, +139 metrics, 0 errors (the one warning printed belongs to
another batch's merged row, ni2025b). Page-1 title check: all 8 cached texts match their source rows; none is a
correction / erratum. xu2019 `garbled_text_layer` flags p.7 only (reference list); all values come from clean p.1-p.6
text and the p.6 figure. All 8 sources are `restricted_local_only`: facts and locators only.

## Per paper

| paper | components | metrics | rows |
|---|---|---|---|
| guan2014 | 3 | 27 | double-etched DC PSR (polarization.psr); TE and TM single-polarization GCs (calibration) |
| chung2019 | 3 | 13 | InGaAs-InP 12 um waveguide (loss, 6.15 um); as-cleaved facet; mid-IR PRS |
| zhang2016 | 3 | 21 | bent-DC PSR; TE and TM GCs |
| xu2019 | 1 | 15 | SWG hetero-anisotropic metamaterial PBS |
| shen2015 | 2 | 25 | 2.4 x 2.4 um2 DBS PBS; mode-converting DBS PBS |
| su2014 | 1 | 12 | four-port mode-evolution PBS |
| velha2016 | 6 | 14 | polarization controller / compensator; 2D GC; TE GC; 50:50 MMI; Ge PD; thermo-optic PS |
| ding2013a | 1 | 12 | taper + Y-splitter + 2x2 MMI PSR |

## Values not entered and why

- guan2014: SPGC loop peak levels (Fig. 7, about -12.3 to -13.3 dB): the TE / TM curve groups cannot be tied to the labels
  unambiguously (D156); simulated SPGC PER > 25 dB (p.6; `per_db` not allowed for fiber_chip_coupler); gap 0.2 um, bend
  radius 5 um, taper L3 3 um, ridge L5 21 um (no polarization parameters; in notes); Fig. 5 simulated tolerances. CDSEM
  values (p.5) were entered as wafer-level `measured` thickness rows with a condition saying they are not from the tested
  device; the 192 +/- 4 nm line width is in notes only (a 200 nm test line, not W2).
- chung2019: measured average TM00-to-TE00 conversion efficiency 31.2 % (4 devices, p.6) and simulated 47 % / near 100 %
  (p.4): no registry parameter. MMI 435 x 22.7 um, pre- / post-converter widths and lengths in notes (mmi_* not allowed
  for polarization). Simulated bend mode-mismatch loss (Fig. 2(c)) plotted only.
- zhang2016: peak conversion efficiency 96.9 % (its dB form 0.135 dB is entered); gap 140 nm, radii R1 20 / R2 19.409 /
  R0 3 / R3 14 um, arc angle 26 deg (not allowed for polarization); simulated responses and tolerances (Fig. 4 dashed,
  Fig. 5).
- xu2019: printed BW for 1-dB IL and BW for 20-dB PER (both > 200 nm, p.6): the first is an absolute IL criterion, not the
  registry's 1-dB-from-peak width, and BW20dB has no parameter; the IL / PER rows carry the 1460-1675 nm span. SWG pitch
  250 nm, duty cycles 0.74 / 0.70, period counts 10 / 29 / 5 (subwavelength_period_nm / fill_factor / n_periods not
  allowed for polarization).
- shen2015: abstract average transmission > 70 % (averaging basis not stated) and peak about 80 %; simulated Si-thickness
  tolerances (+/-20 nm, +/-17 nm); on-chip polarizer and tapers (no numbers in the main text; Supp. Sections 4 / 6 not
  cached).
- su2014: nothing printed beyond the entered rows; microring and inverse-taper couplers have no values.
- velha2016: GC "-1 dB spectral bandwidth of 20 nm" stated once after both GC losses (D159, in notes on both GC rows);
  4-channel WDM 1 dB spectral uniformity (power_uniformity_db not allowed for polarization; in notes); PPM 70 nA threshold
  (operating condition, in notes).
- ding2013a: simulated tolerances (63 / 40 / 100 nm) and > 95 % TM0-TE1 conversion; Fig. 4(c) size-deviation devices
  (no number printed); MMI 2 x 13.7 um and arm length difference 173 nm (no polarization parameters).

## Fab / facility orgs

- velha2016: fab `org_imec` on all 6 rows ("manufactured by IMEC in a multi-project wafer run", p.2), process_name
  "IMEC multi-project wafer run (photonic design kit)".
- zhang2016: facility `org_center_for_advanced_electronic_materials_and_devices` (AEMD of SJTU acknowledged for support
  in device fabrication, p.7); fab empty (cai2021 precedent).
- Fab empty (passive fabrication statements, D80b): guan2014 (OpSIS named only as a grant, p.8), chung2019, xu2019,
  shen2015, su2014 (CNSE co-authors; poulton2017 precedent), ding2013a.

Missing from the registry (facility role):

| name as printed | paper | locator | role |
|---|---|---|---|
| Texas Nanofabrication Facilities (supported by the NSF NNCI) | chung2019 | p.7 acknowledgments | facility |
| University of Utah shared facilities of the Micron Technology Foundation Inc. Microscopy Suite | shen2015 | p.5 acknowledgments | facility |
| University of Utah USTAR shared facilities | shen2015 | p.5 acknowledgments | facility |

(University of Utah itself has no registry row; Utah Nanofabrication Facility appears only as an author affiliation in
shen2015, not as a fabrication statement.)

## Judgment calls

1. GC-normalized (straight-waveguide-normalized) IL and crosstalk levels are `derived` + `de_embedded` +
   `reference_structure` (guan2014a precedent); port-ratio PER (xu2019 Eq. 8-9, shen2015 ER) is `measured` + `direct`.
2. Polarization crosstalk / extinction stored as `per_db` (crosstalk_db is not allowed for polarization; merged PSR
   precedent).
3. Efficiencies in % (shen2015 71 / 80 / 58 / 71 % measured, 81 / 89 / 80 / 83 % simulated) entered as
   `insertion_loss_db` = -10 log10(eta), `derived` (simulated stays `simulated`, D83f), printed % in notes.
4. xu2019 IL < 1 dB from two sets of ten cascaded PBSs: `derived` + `cutback` + `per_component` (cascade / N, rule 4),
   though the arithmetic is in the uncached supplement.
5. chung2019 4.67 dB PRS IL `author_estimate` + `loss_breakdown`: the paper says "estimate", attributes MMI / Y-junction
   terms from near-IR literature, and the printed powers do not reproduce the number without unshown steps. The facet
   loss 2.7 / 2.78 dB is scope `unspecified` ("averaged coupling loss of two as-cleaved facets": per-facet average or
   two-facet total not stated).
6. velha2016 building-block values (GC 9.7 / 2.7 dB, MMI 0.5 dB, PD 10 nA / 0.9 A/W) entered as `measured` with the
   paper's word "were determined"; they may be design-kit values (the paper does not say). MMI 0.5 dB "insertion loss"
   of a 50:50 coupler entered as `excess_loss_db` (rule 6). Platform left empty on all velha2016 rows: the paper never
   states SOI / BOX (D422 / D423). Ge PD subtype `ge_waveguide` from the waveguide termination (geometry not described).
   Thermal time constant about 4 us and < 100 kHz `author_estimate` (no measurement shown). Residual post-compensation
   power spread entered as `pdl_db` (1 dB range, 0.22 dB std; ofc2026 Th3C.5 precedent).
7. shen2015 mode-converting PBS: peak efficiencies and ERs have no printed wavelength; span from the Fig. 5 axes with
   `wavelength_inferred`. The abstract "> 10 dB within 32 nm" row uses 1550 nm inferred (band edges not printed). One
   `polarization.pbs` row for the mode-converting device (no separate mode-conversion metric printed, so no
   mode_converter row under D396).
8. su2014 T-shaped ridge dimensions (110 nm thickness, 120 / 550 nm widths) are SEM values (`measured`); "110 nm ridge
   thickness" stored as `slab_thickness_nm` (lower layer of the T).
9. guan2014 printed 0.19 / 0.2 um widths and 0.63 / 0.93 um periods are `derived` (D157); duty cycles 65 / 76 % and
   zhang2016 filling factor 48 % stored as fractions, `derived`, definitions not stated (D253).
10. zhang2016 is the journal extension of the authors' ECOC 2016 paper: values kept (D408).

## Registry gaps (proposed)

- `polarization_conversion_efficiency_pct` (unit %, classes polarization, performance, conditions wavelength):
  "converted-polarization power as a fraction of the total output (or of the input, definition in condition), linear,
  as reported". Skipped values: chung2019 31.2 % measured mean of 4 devices at 6150 nm (p.6), 47 % simulated (p.4);
  zhang2016 96.9 % peak at 1564 nm (p.6). (aamer2012 reported the same gap.)
- Allow `gap_nm`, `coupling_length_um`, `radius_um`, `min_bend_radius_um`, `mmi_width_um` / `mmi_length_um` and
  `subwavelength_period_nm` / `fill_factor` on `polarization` (DC / MMI / SWG-based PSRs and PBSs): skipped guan2014 gap
  200 nm (p.3), zhang2016 gap 140 nm and R1 20 um (p.3-p.4), chung2019 MMI 435 x 22.7 um (p.4), ding2013a MMI 2 x 13.7 um
  (p.2), xu2019 SWG pitch 250 nm and duty cycles 0.74 / 0.70 (p.5).
- `bw_at_criterion_nm` (or `bw_per_db_nm`) for polarization: "wavelength span over which the stated criterion holds
  (criterion, e.g. PER > 20 dB or IL < 1 dB, in condition)". Skipped: xu2019 BW20dB > 200 nm and BW1dB(IL) > 200 nm
  (p.6).
- `per_db` on `fiber_chip_coupler` (polarization-selective GCs): skipped guan2014 simulated SPGC PER > 25 dB (p.6).
