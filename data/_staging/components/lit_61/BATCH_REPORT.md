# Batch lit_61 report (distill subagent, 2026-10-30)

Dry-run `batch lit_61: +16 components, +141 metrics; errors 0` (one WARN about another batch's row,
cmp_lit_ni2025b_pimmwc-m18). All six sources are `restricted_local_only`: facts and locators only, no quotes beyond a few
words. ASCII only; no e-mail, street or postal text. Page-1 title check: all 6 texts match their source rows; none is a
correction / erratum; no `garbled_text_layer`. Rows built by a scratchpad script (one spec file for all papers). Figure
renders checked: goh2001 pp.2, 7, 8 (Tables I-II, Fig. 12), pathak2012 p.4 (Fig. 3 labels), yang2010 p.4 (Fig. 2(c)),
mizukami2011 p.4 (Fig. 8-9 inset labels), popovic2006 Fig. 3 (labels 2 / 18 / 29 / 31 / 51 dB, FSR 20.8 nm).

## Per paper (components / metrics)

- goh2001 (5 / 28): 16x16 silica PLC double-MZI matrix switch (switch_fabric.mzi_mesh, ge_silica): 256-path statistics at
  1.55 um (fiber-to-fiber IL mean 6.6 / range 6.0-8.0 dB, PDL mean 0.08 / < 0.33 dB, worst-polarization ER mean 53 / range
  40-63 dB), example path ER 67 dB, worst path over 1530-1560 nm (ER > 42, IL < 8.2 dB), estimated multiple crosstalk mean 40 /
  range 33-50 dB (author_estimate, worst-case model), power 16.6 W (derived 16 x 1.04 W; Table II 17 W) and 61 W before phase
  trimming (author_estimate, origin not stated), chip 100 x 107 mm, circuit length 66 cm. Double-MZI switching unit
  (switch_fabric.other, D158): about 500 mW ON power per MZI (p_pi_mw), 1.04 W average unit ON power, about 0.2 dB/stage
  intersection + bend excess (author_estimate, loss budget with assumed 0.4 dB/point coupling). 3-dB DC: coupling ratio 42 %
  average (author_estimate, origin not stated). Intersection (crossing.other): about -66.7 dB crosstalk on test waveguides.
  0.75 %-delta waveguide: 66-cm test waveguide 3.0 dB fiber-to-fiber, 3.3 dB/m -> 0.033 dB/cm (author_estimate, assumed coupling
  loss), bend radius > 5 mm, 7 x 7 um core. Not entered: Table I (cited [18], [19]); Table II previous-work column and 8x8
  values (authors' earlier work); 135 mW per MZI (cited [27]); heater length 4 mm (Fig. 6 trimming data not tied to the matrix
  chip); trimming powers 4-7 W / 25 s / 1 s, bias < 3 mW after trimming, 3.6 % heater-resistance change, 0.2 dB coupling-ratio
  penalty, uniform-supply 0.1 dB loss increment / ER degradation (no parameters).
- pathak2012 (2 / 23): polarization-diversity 16 x 200 GHz AWG demux (wdm.awg; two identical AWGs, one row): estimated
  fiber-to-fiber loss < 15 dB (author_estimate), per-channel PDL 0.06-2.32 dB, 16 channels / 72 arms / 200 GHz / 1.6 nm,
  footprints (circuit 1400 x 850, single AWG 365 x 650 um2), 800 / 450 nm widths, 2 um apertures, 70 / 220 nm etches, 150 nm
  slab (derived, Fig. 3(c) label). 2D focusing GC (fiber_chip_coupler.grating): PDL 1.1 dB and peak-efficiency wavelength 1520
  nm from the two-GC reference circuit, estimated 12 dB for two GCs -> 6 dB loopback_half (author_estimate), 610 nm pitch, 10 deg,
  70 nm holes in 220 nm Si, 500 nm output wire. Not entered: AWG IL -2.6 dB and crosstalk 21.5 dB (attributed to [18], see Q1);
  polarization-dependent wavelength shift 0.028-0.12 nm (registry gap); hole diameter 390 nm, 30 um focusing distance, 2 dB loss
  at 4 um offset, < 1 um / < 0.5 um position offsets (no parameters).
- yang2010 (3 / 26): 4x4 non-blocking Si EO switch (switch_fabric.mzi_mesh, soi_rib): worst-case crosstalk 9 dB (state #4 Ei),
  > 10 dB for state #9 over 1524-1534 nm, crosstalk bandwidths 10 nm (state #9 all paths), > 24 nm (per input), 7 nm common to
  all states, 7 to > 120 nm per state, IL 0.6-5.8 dB (scope unspecified), steady-state power 11.3 mW (state #9) and 7.4-20.4 mW
  (derived, mW -> W), 300 x 1600 um2, 500 x 220 nm / 50 nm slab / 2 um BOX. 2x2 p-i-n MZI element (switch_fabric.other):
  15 dB off-state crosstalk with 50 nm bandwidth, on-state crosstalk > 15 dB over 1470-1590 nm at 1.06 V, 1.0 dB on-state FCA
  loss, 1.06 V cross-to-bar. MMI crossing (crossing.mmi): 0.3-0.5 dB/crossing over 1520-1540 nm, 3.5 x 1 um MMI, 500 nm access.
  Not entered: Table 2 per-element powers (phase-error correction), "many states" ER > 25 dB, Fig. 5 per-state labels,
  nanosecond switching (cited [9]), 200 um p-i-n length (no role parameter; in notes), 40 Gb/s eyes.
- mizukami2011 (1 / 10): 128 x 128 3D MEMS switch module (switch_fabric.mems, platform other): IL mean 2.3 / max 4.6 / std 0.6
  dB fiber-to-fiber incl. two internal 8MPO connections (no wavelength stated anywhere: band unspecified), switching time mean
  8 / max 38 / std 1.57 ms as rise_time_us (derived, ryf2002 precedent), static / dynamic crosstalk > 50 / > 41 dB, 128 in /
  128 out. Not entered: 0.1 dB power stabilization, < 0.5 dB repeatability and interference, -5 to 50 C operation, GR-63 /
  CISPR 22, module size 436 x 350 x 355 mm (no parameters).
- piggott2015 (1 / 11): inverse-designed 1300 / 1550 nm splitter (wdm.other): peak IL 1.8 dB (O band) / 2.4 dB (C band)
  de-embedded against a parallel straight waveguide, 3-dB bandwidths 100 / 170 nm, crosstalk > 11 dB in both bands (one row,
  band unspecified), 3 devices, 2.8 x 2.8 um2, 500 nm waveguides, 220 nm Si, 3.0 um BOX. Not entered: design specification
  (> 90 % / < 1 %) and simulated Fig. 4(a) curves (plotted only); PM lensed-fiber PER 19.0 / 20.7 dB (setup).
- popovic2006 (4 / 43): one-, two- and three-stage third-order SiN microring add-drop filters (wdm.mrr, sin). One stage: 40 GHz
  1-dB passband, 2 dB drop loss, 30 dB adjacent rejection (Fig. 3(b) label 29 dB, noted), 18 dB through extinction, 1538.36 nm
  fitted centre, 0.3 dB adjacent-channel through-port loss (scope unspecified); design rows (simulated): 0.35 dB design loss,
  stage extinction 22 / 15 dB, 30 dB rejection at 80 GHz, couplings 10.3 / 0.22 %. Two stages: > 30 dB extinction (label 31),
  FSR 20.8 nm (inset label). Three stages: > 51 dB extinction over 32 GHz; design 66 / 45 dB (simulated, 3 x stage). Shared
  geometry on each filter row (8 um radius, 900 nm ring, 702 nm bus, gaps 120 / 372 nm, 396 nm measured core, 590 nm etch).
  Ring waveguide (waveguide_platform.bend): 12 dB/cm excess ring propagation loss (independent measurement), 8 um radius as
  min_bend_radius_um. Not entered: dispersion slope about 0.3 ns/nm2, 2.3 GHz fitted mismatch, 2 GHz / 5 GHz ring / stage
  alignment, 70 pm width matching, radiation Q 250,000 and spurious-mode Q (design), 0.05 dB ripple, dose offsets (no
  parameters); Fig. 2 theory (generic fourth-order example, not a device).

## mizukami2011 scope (D411)

Kept in scope as fiber-coupled: the switch fabric couples fiber collimator arrays through two lithographic two-axis MEMS
tilt-mirror array chips (the same device family as the merged lit:ryf2002 3D MEMS crossconnect, switch_fabric.mems,
platform other). It is not a bulk crystalline part (D411's exclusion), but it is also not chip-scale: the measured unit is a
rack-mounted module (436 x 350 x 355 mm) with active mirror control. If the coordinator reads D411 as "chip-scale or passive
fiber-coupled only", delete cmp_lit_mizukami2011_mems_oxc_128x128 (10 rows) and ryf2002 for consistency.

## Judgment calls / questions for the coordinator

1. pathak2012 AWG IL -2.6 dB and crosstalk 21.5 dB not entered: the body sentence cites the authors' ECOC 2012 paper [18],
   which has the same title (conference version of this journal paper). D408 keeps journal-extension values but D259 applies
   where the value sentence attributes the value to the earlier paper; the abstract states both without a citation.
   Alternative: enter both (measured, p.1 Abstract / p.7) if the coordinator reads [18] as the same measurement.
2. pathak2012 estimated fiber-to-fiber < 15 dB entered as author_estimate although its inputs may include the [18] value
   (2.6 dB + 12 dB, not stated); delete if rule 3 is read strictly.
3. goh2001 DC coupling ratio 42 % average: author_estimate (origin not stated, loss-budget input) rather than measured.
4. goh2001 ON-state power per MZI (about 500 mW) entered as p_pi_mw on the unit row (half-wavelength asymmetric MZI, bar ->
   cross = pi); the 1.04 W unit average as power_consumption_w.
5. goh2001 66-cm test-waveguide IL (3.0 dB) and the 3.3 dB/m estimate carry 1550 nm with wavelength_inferred (loss-budget
   paragraph in the 1.55 um measurement section, no wavelength in the sentence).
6. yang2010 IL 0.6-5.8 dB scope unspecified (spectra normalized to the sum of output ports; the IL reference is not stated).
7. mizukami2011 switching time as rise_time_us (closed-loop peak search included; ryf2002 precedent); tracking_time_us is the
   alternative.
8. popovic2006: design values entered as simulated on the filter rows (stage extinction, design loss, couplings); the 12 dB/cm
   ring loss on a separate waveguide_platform.bend row (prop_loss not allowed for wdm).
9. fab orgs: goh2001 org_ntt ("we fabricated", all NTT); piggott2015 org_stanford_university (author contributions name the
   fabricating author, D395). pathak2012, yang2010, mizukami2011, popovic2006: no fabrication statement naming authors or an
   org (passive "fabricated"; all authors at one org each: Ghent University - imec, IBM T. J. Watson, NTT, MIT RLE): fab empty
   (D80b). No facility acknowledged in any of the six papers.

## Missing orgs

None needed: org_ntt, org_stanford_university in the registry; no facility named in any paper.

## Registry gaps

- wdm: `pdw_nm` (polarization-dependent wavelength shift of a polarization-diversity / polarization-insensitive filter, max
  channel-centre shift between input polarization states; pathak2012 0.12 nm worst / 0.028 nm best channel, p.8 Fig. 8).
- switch_fabric: `connection_repeatability_db` / `power_stability_db` (mizukami2011 < 0.5 dB repeatability, 0.1 dB
  stabilization, p.4-5 Table 1) - single paper, probably defer.
- crossing: `crossing_angle_deg` (goh2001 about 30 deg intersection angle, p.3) - geometry only.
- wdm: `group_delay_dispersion_ps_per_nm2` or dispersion slope (popovic2006 about 0.3 ns/nm2, p.3) - single value, defer.
