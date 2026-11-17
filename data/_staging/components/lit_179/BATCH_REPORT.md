# lit_179 batch report

Papers: lit:wang2014a, lit:nielson2005. verified_on 2026-11-16. Both cached texts match their source rows (page-1
titles checked); neither is a correction. Dry-run: +6 components, +103 metrics, 0 errors.

## lit:wang2014a (Optics Express 2014, 8x8 Si nanowire AWG routers)

Components 4 / metric rows 88:

| component | metrics | content |
|---|---|---|
| cmp_lit_wang2014a_awg1 | 16 | 3.2 nm, no optimization: IL 8.6-10.1 dB and crosstalk 6.0-7.5 dB read off Fig. 2(d) / (e); Table 1 design |
| cmp_lit_wang2014a_awg2 | 20 | 3.2 nm, 1 um arrayed waveguides: Fig. 2 ranges (IL 3.1-4.8, crosstalk 19.3-21.1 dB); text "< 3 dB" / "< -17 dB"; design |
| cmp_lit_wang2014a_awg3 | 27 | 3.2 nm, wide arrays + bi-level tapers: IL 2.32 dB best, Fig. 2(d) range 2.32-4.7, crosstalk 20.5-24.5 dB, 3 dB BW ~1.1 nm, all-input non-uniformity 4.13 dB, all-input crosstalk > 20 dB; design incl. taper 20 um / 70 nm etch / 2.5 um |
| cmp_lit_wang2014a_awg4 | 25 | 0.8 nm (DWDM): IL 2.92 dB best, Fig. 3(c) range 2.92-5.55, crosstalk 16.9-17.8 dB, 3 dB BW ~0.3 nm, non-uniformity 3.66 dB, all-input crosstalk > 15.5 dB; Fig. 3 caption design |

IL rows: scope `de_embedded`, method `reference_structure`, excludes grating couplers (spectra normalized to a
reference waveguide, p.4; fan2025 precedent), TE, C band inferred from the plot spans (no wavelength stated with the
values). Crosstalk type (adjacent / non-adjacent) is not stated: `crosstalk_db` with the wording in condition.

Not entered:
- "For each input channel, the insertion loss ranges from 2 dB to 4 dB" (p.6 Sec. 4): does not say which inputs and
  conflicts with Fig. 2(d) (AWG #3 up to ~4.7 dB), Fig. 3(c) (AWG #4 up to ~5.55 dB) and the Fig. 4 colour scale
  (points up to 6-7 dB). Treated as D159-like (sample set unclear); in component notes of #3 / #4.
- Central-wavelength fluctuation "several nanometers" and ~5 % channel-spacing deviation (p.7): no value in nm (the
  5 % is in the channel_spacing notes).
- System test (p.8-9): < 1.2 dB power penalty at 10 Gb/s with 15 km SSMF (AWG #4): link-level, no parameter.
- AWG #4 size "about 4 times larger" (p.5): no dimension.
- Table 2 values of other works (refs [6]-[11]): rule 3.

Judgment calls:
- Text "< 3 dB" IL for AWGs #2 and #3 (p.5) kept as printed on both rows with conflict notes (D417): Fig. 2(d) shows
  every AWG #2 channel at ~3.1-4.8 dB and AWG #3 channels 1-3 at ~3.7-4.7 dB. The audit may prefer to drop these
  two rows as superseded by the figure ranges.
- Table 1 prints the FSR unit as "(um)"; entered 25.6 nm (8 x 3.2 nm), note on each row.
- Design channel spacing and FSR `author_estimate` (D82a). Focal length L entered as `fpr_length_um` (palmer2026,
  vellekoop1991 precedent). d and da as two `pitch_um` rows with condition.
- AWG #4 takes the Sec. 2 optimization geometry (1 um arrays, 450 nm bends at 5 um radius, 20 um / 70 nm / 2.5 um
  bi-level taper) because the paper builds it on the "comprehensive optimal design" (p.5, Fig. 3 caption); noted on
  each row. AWG #1 gets only the 450 nm strip width (no bend radius or taper stated for it).
- Platform `soi_strip` for all four (p.3 "SOI strip nanowire waveguide"); the shallow bi-level taper is in
  core_material.
- Fab empty: "fabricated with a 130 nm CMOS process on the 200-mm SOI wafer" (p.3) is passive and names no org;
  authors at SIMIT, Grace Semiconductor Manufacturing Corporation (registry org_grace_semiconductor_manufacturing) and
  Purdue (D80b; same handling as lit:sheng2012). process_name "130 nm CMOS process (200-mm SOI, 248-nm DUV)".

Missing orgs: none (no fab / facility statement).
Registry gaps: system power penalty (dB at a stated BER / data rate / fiber length) on wdm: proposed
`power_penalty_db` (wdm, switch_fabric; "receiver power penalty caused by the component in a link, conditions in
condition"), skipped value 1.2 dB lt (p.9 Sec. 5). Low priority (link-level).

## lit:nielson2005 (IEEE PTL 2005, MEMS ring-resonator wavelength-selective switch)

Components 2 / metric rows 15:

| component | metrics | content |
|---|---|---|
| cmp_lit_nielson2005_mems_ring_switch (`switch_fabric.mems`) | 7 | drop-port IL 11 dB (0 V), through-port extinction 1.6 dB (0 V), drop-port reduction 15 dB at 30 V, switching 60 us (down, voltage ON) / 16 us (up, voltage OFF), ~1 uW at 100 kHz (author_estimate), bridge length 160 um |
| cmp_lit_nielson2005_ring_filter (`wdm.mrr`) | 8 | FSR 12.5 nm around 1550 nm (author_estimate), inner / outer radius 13.47 / 14.48 um, ring width 1010 nm, bus width 1050 nm, 330 nm core, gap 185 nm, 3 um BOX |

Not entered (registry gaps, all in the switch row notes):
- Pull-in voltage 24 V measured (profilometer and optical tests), 15 V design (p.3 Sec. IV): proposed
  `pull_in_voltage_v` (switch_fabric, phase_shifter; "voltage at which an electrostatic parallel-plate actuator
  snaps down, method in notes"); already a candidate in D440 / D594.
- Actuation voltage 30 V (p.3): proposed `actuation_voltage_v` (switch_fabric; D594 candidate).
- Switching rate up to 8 kHz (p.3): no parameter (bw3db_khz is a small-signal bandwidth).
- More than 5,000,000 cycles without failure (p.3): `endurance_cycles` exists only for phase_shifter; widen to
  switch_fabric (D594 candidate).
- About 10 us expected with faster test equipment (p.3): projection, not a result.
- Bridge-gap deformation 1.0 -> 0.34 um and effective initial gap 2.2 um (p.2-3): no fitting parameter (gap_nm on
  switch_fabric is the directional-coupler gap); in notes.

Judgment calls:
- Two rows by class (D396): the MEMS switch (switching metrics) and the ring filter (FSR, geometry), cross-noted.
  Drop-port IL / extinction stay on the switch row because they depend on the bridge state. Alternative: a single
  `switch_fabric.mems` row with the ring FSR / geometry in notes (testa2018 / D407 style); `switch_fabric.wss` was
  considered (the paper calls it a wavelength-selective switch) but `mems` follows han2015 / seok2016 / D594.
- Switching times: 60 us (bridge down, voltage ON, through-port power rises in Fig. 6) -> `rise_time_us`, 16 us
  (bridge up) -> `fall_time_us`, as the seok2016 ON / OFF mapping; definition not stated and limited by the test
  equipment (notes). No `le` qualifier added (printed as observed values).
- 11 dB drop-port IL: scope `unspecified` (Fig. 5 is relative transmissivity; drop peaks about -25 dB against a
  through-port level about -14.5 dB, reference not stated).
- FSR 12.5 nm `author_estimate`: stated in the design section with no method; Fig. 5 drop peaks (~1552.5 / 1565 /
  1577.5 nm) are consistent.
- Fab org_mit on both rows as borderline (D84b): the acknowledgment thanks MIT Microsystems Technology Laboratories
  technical staff for support in fabrication (p.3); staff thanks set no facility (facility empty). The ring process
  is cited to the authors' ref. [6]. Process name empty ("CMOS compatible microfabrication" names no node or flow).
- Platform `sin` for silicon-rich SiN (n 2.2), as for other SRN rows; air top cladding.

Missing orgs: none (org_mit and org_mit_microsystems_technology_laboratory exist).
