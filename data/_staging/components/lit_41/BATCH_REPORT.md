# Batch lit_41 report (distill subagent, 2026-10-29)

Dry-run `batch lit_41: +28 components, +128 metrics; errors 0` (the one WARN printed concerns ni2025b, another batch).
ASCII, no e-mail, no quotes (all six sources `restricted_local_only`). Page-1 title / authors match the source row for
all six papers; no garbled text layer (keyvaninia2019 p.6 and p.8 text is column-interleaved: read from the page
renders).

## Per paper (components / metrics)

- benedikovic2015 (4 / 27): apodized SWG GC with backside Al mirror (fabricated): 0.69 dB peak at 1535 nm and 0.85 dB
  ripple-averaged (loopback_half, derived: back-to-back minus waveguide), 3-dB BW ~60 nm, peak wavelength, simulated
  0.67 dB and back-reflection ~6 % -> 12.2 dB (simulated), geometry (chirped period 751-847 nm, SWG pitch 450 nm,
  25 periods, 27 deg, 220 nm / 3 um BOX, full etch), fiber MFD 10.4 um (specification). Three design-step rows
  (simulated only): apodized without mirror 1.92 dB, uniform 27 deg 2.6 dB, uniform 10 deg 5.3 dB (+ period, DCz 55 %
  as fill_factor 0.55 derived, definition not given). Not entered: SWG hole sizes 104-194 nm (no parameter), Fresnel
  0.15 dB / ripple 0.3 dB (notes). Fab empty (passive; authors at three orgs).
- ong2018 (15 / 41): HPF SWG GC rectangular (Ly 600 nm): 7.49 dB peak (Device 4 scan, de-embedded via waveguide and
  POR-to-MMF loss, derived), 6-device range 7.9-8.6 dB read off Fig. 7 (extracted_from_figure), 1-dB / 3-dB BW ~14 /
  29.5 nm, 1-dB tolerance 21.4 x 10.1 um entered halved as 10.7 / 5.05 um (derived, region not centred on the peak),
  5-die mean 9.1 dB at 1603 nm (loopback_half, Table 3), geometry (Table 2 period / duty-cycle ranges, 600 nm SWG pitch,
  15 um width, 500 um taper, 14.5 deg, 5.14 um cladding). POR half-etched GC 4.28 dB (Fig. 8(a)). Curved-layout
  orientation variants: 6 rows Ly 600 (Table 3 means at 1603 nm; Fig. 8(c)/(d) peaks 12.19 / 12.40 dB at 1550 nm) and
  7 rows with periods 29-36 at Ly 300 nm (Table 4). -1 dB / -3 dB areas (um2) in notes. Not entered: number of periods
  (40 in text vs Table 2 rows to 42), Fig. 11 single-die values, simulated tilt tolerance (Fig. 12), % change columns.
  Fab empty: unnamed 300 mm CMOS foundry; AIM Photonics acknowledgment = program (D80c).
- snyder2018 (1 / 19): SiON ridge + etched slab-lens edge coupler on Si inverse taper (SMF-28 design), platform sion
  (D82f), fab org_imec ("fabricated in imec's 200 mm pilot line"): O-band 4-6 dB per facet, <4.8 dB 1475-1625 nm
  both polarizations, PDL <1 dB, 1-dB BW >150 nm, 1-dB tolerance ranges >4 um / ~3.5 um halved (derived), simulated
  MFD 9.8 um, vertical mode ~3 um (author_estimate), target MFDs 10.4 / 9.2 um (specification), geometry (130 nm tip,
  300 um final taper, SiON 3 um / ridge 2.5 um / slab 1.5 um from Fig. 2 labels, 0.4 um SiO2, 380 nm input width).
  Per-facet values stated without the extraction method: measured, method unspecified (D167). Not entered: lens radius
  9.67 um / apex distance 22.66 um (gap below), 2.5 dB vertical-expansion loss term (simulated budget), expanded-beam
  design (fabricated but never coupling-measured; only design values).
- xie2016 (1 / 4): SMF nanospike self-aligned launch into HC-PCF at 1064 nm (fiber_interface.other, D80f, platform
  silica): 0.57 dB / 87.8 % launch efficiency (author_estimate: taper 0.31 dB and HC-PCF 0.13 dB/m subtracted, origin
  not stated), 81 % total transmission (device_total, measured), 88.3 % theory (simulated), back-reflection ~0.05 % ->
  33 dB (derived). Not entered: tip 150 nm / insertion 50 um (no fiber_interface taper parameter), 450 mW handling
  (power_handling_dbm not allowed), ~10 % orthogonal-polarization drop (attributed to taper / fiber), optomechanics.
  Fab empty (passive; HF-etching help from a named person, org not stated).
- cheng2023 (6 / 26): fab org_applied_nanotools ("fabricated ... in Applied Nanotools"). CAMN TM-pass polarizer
  (polarization.other): IL <0.5 dB mean (de_embedded via GC calibration circuit, derived), PER >30 dB 1507-1575 nm,
  geometry; width-deviated polarizers W 0.74 / 0.86 um (PER >20 dB each); CAMN PBS (polarization.pbs): IL <0.5 dB TM
  through and TE drop, PER >20 dB both; design rows (simulated): polarizer 0.73 dB mean over 1294-1603 nm, PBS 0.7 dB
  TE (1292-1606 nm) / 1.3 dB TM (above 1377 nm, upper end not stated). Not entered: reflection suppression ~26.4 dB
  measured (gap), 20 dB-ER bandwidths 309 / 312 / 314 / >373 nm (gap), CAMN period / N (period_nm, n_periods not
  allowed for polarization), bare-CAMN and chirp-study simulations (3-dB reflection BW 421 vs 255 nm), width-deviated
  PBSs (ER >20 dB only over "the major part" of the range), mode-coupler geometry (notes).
- keyvaninia2019 (1 / 11): InGaAsP/InP mode-evolution PRS (polarization.psr, platform inp): PER >19 dB 1520-1620 nm,
  peak 24 dB (best), >17 dB over C+L for variants -200..+100 nm of the actual design, simulated >18 dB for +/-200 nm,
  max IL 1 (TE) / 1.8 (TM) dB (+/-0.5 dB, scope unspecified, wavelength inferred from the measured range), length
  2000 um, layer geometry (440 nm derived from 120 + 320 nm, etch 120 nm, W1 1.7 um). Fab empty (passive; HHI).

## Judgment calls

1. ong2018 / snyder2018 1-dB tolerances printed as full ranges / extents were halved (derived) per the merged
   precedent (halved full-range rows); ong2018's -1 dB region is asymmetric about the peak (noted).
2. ong2018 orientation variants entered as separate rows (sibling designs, rule 9), mostly one IL metric each.
3. keyvaninia2019 kept as one component row although mask-width variants were measured: the headline PER values do
   not name the variant consistently (19 dB claim vs Fig. 8 curves); per-variant figure readings not entered (D159 /
   D165). Text vs Fig. 3 conflict on the Y-branch width (1.5 vs 1.6 um) and gap (200 vs 120 nm): not entered.
4. cheng2023 ER entered as per_db (polarization precedent, 7 / 12 merged rows per_db); ratio of two measured spectra of
   the same device kept measured; IL normalized to a calibration circuit derived (D80a).
5. benedikovic2015 coupler loss: back-to-back minus waveguide loss, halving implied -> loopback_half derived.
6. snyder2018 source row venue says "2022 IEEE 72nd ECTC"; the PDF prints 2018 IEEE 68th ECTC (DOI ectc.2018.00130):
   registry metadata fix for the coordinator.

## Orgs missing

None needed (org_imec, org_applied_nanotools exist; no other fab / facility statements).

## Registry gaps

- `back_reflection_db` for `polarization` (cheng2023 polarizer mean reflection suppression ~26.4 dB, p.10-12 Fig. 9(b);
  def: TE back-reflection suppression relative to the transmitted mode, positive dB).
- `er_bandwidth_nm` (polarization / mode_converter): full width over which the extinction ratio exceeds a stated level
  (cheng2023 20 dB-ER bandwidths 309 / 314 / >373 nm simulated, p.8-9).
- `period_nm`, `n_periods` for `polarization` (cheng2023 CAMN 0.354-0.433 um, N 12, p.9; nanobeam / grating polarizers).
- `tol_1db_area_um2` for `fiber_chip_coupler` (ong2018 -1 dB alignment area 47.0 um2 etc., Tables 3-4) - or a
  full-extent tolerance parameter, to avoid halving asymmetric extents.
- `lens_radius_um` for `fiber_chip_coupler` (snyder2018 integrated slab-lens radius 9.67 um, p.3 Table I).
- `tip_width_nm` for `fiber_interface` (xie2016 nanospike end diameter ~150 nm, p.1-3).
