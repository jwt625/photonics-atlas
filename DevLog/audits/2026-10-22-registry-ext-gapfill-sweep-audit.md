---
title: Fresh-context audit of the D169 registry extension, the lit gap-fill and convention sweep 2
date: 2026-10-22
mode: read-only audit (coordinator + 10 sub-auditors, one per lit gap-fill batch, three for sweep2 ops, one for sweep2 misses). No repo writes except this file; no git, no network. Proposed corrections below are not applied and were not dry-run through patch_component_staging.py (its RunLog writes into logs/); instead every op was checked by script against the current staging CSVs (ids exist, columns valid, new metric ids unused, add_metrics units = registry units, YAML round-trips)
scope: DevLog-007 D169, D250-D255 and the 22:39-23:05 Progress entry
---

# Audit: registry extension, gap-fill, sweep 2 (2026-10-22)

Inputs: `data/schema/component_parameters.yaml` vs `HEAD`, `data/schema/component_layouts.yaml`,
`data/schema/components.schema.yaml`, `data/_staging/components/lit_0{1..6}/gapfill.yaml`,
`data/_staging/components/*/sweep2.yaml` (28 batches). Pre-pass state from the session backup
`backup-2026-10-22-pre-registry-ext.zip` (staging CSVs before the pass). Every gap-fill row and every sweep2 op was
re-read at its locator in `references/<id>/text.md`, `../eo-modulator-atlas/references/<id>/text.md`, the OFC extracted
text or the packaging text; figure renders were opened where the value or a competing label sits in a figure (song2021
Fig. 1(c), guo2026 Fig. 2(a)/(b), yue2026 Fig. 6, kim2019 Table I, shikama2017 Figs. 4/6/7, tanizawa2015 Fig. 4,
wang2026 Table II, valdez2023a Fig. 2).

Note on state: `lit_0N/coord2.yaml` (org round 5, applied 23:15-23:17, after the gap-fill) already set the GWNIC
facility on the three meng2023 rows and the Technion MNFU facility on oz2023; the sub-audit's proposal for those was
dropped as moot. All proposed notes below were diffed against the post-coord2 CSVs (no fact dropped).

## Counts

| part | checked | ok | imprecise | wrong | misses found |
|---|---|---|---|---|---|
| 1 registry: new parameters | 28 | 28 | 0 | 0 | - |
| 1 registry: class allowances (22 parameters) | 25 | 23 | 2 | 0 | 1 (series_resistance_ohm for amplifier) |
| 1 registry: def changes / enums / subtype / layout | 4 + 2 + 1 + 1 | 6 | 2 | 0 | - |
| 2 gap-fill metric rows (lit_01..06) | 132 | 117 | 15 | 0 | 2 (lit_05) |
| 2 component ops (65 updates incl. 22 reclass / platform, 2 new components, 1 metric notes update) | 68 | 67 | 1 | 0 | - |
| 3 sweep2 ops (all, 28 batches) | 116 | 101 | 1 | 14 | - |
| 3 unchanged rescale-like rows (dimension candidates) | 39 | 26 | 10 | 3 | 3 |
| 3 unchanged rescale-like rows (non-dimension, outside D255 scope) | 6 verified of 32 candidates | 0 | 0 | 6 (D82d) | 6 |

Per batch, gap-fill metric rows ok / imprecise: lit_01 32/3, lit_02 15/2, lit_03 23/1, lit_04 20/4, lit_05 14/4,
lit_06 13/1. Sweep2 ops ok / imprecise / wrong: lit_02+lit_03+lit_05+lit_06 31/0/12, lit_04+bf+bt 39/0/2,
ofc+pilot+pk 31/1/0. Registry arithmetic confirmed: 161 -> 189 parameters, 22 parameters widened by 25 class
allowances, defs changed for fill_factor, fsr_nm, extinction_db, slsr_db; all 3589 merged metric rows pass the
parameter-class allowance and unit check after the reclasses.

## Part 1: registry extension (D169, D250, D251)

All 28 new parameters have a unit, `kind`, class list and a definition that names what goes into `condition`. None
re-adds a D77 / D81 / D250 rejection: `endurance_cycles` (cycle count) is not the rejected "lifetime" (time to
failure); `dgd_ps` (polarization / mode group-delay difference) is not the rejected chromatic dispersion (beta2, D250
"D81 stands"); `bw_0p5db_ghz` is a passband width, not the rejected 0.5 / 3 dB alignment tolerances. Units follow the
existing style (`%/W/cm2`, `mA/cm2`, `K/W`, `deg/nm`). `dark_current_density_ma_per_cm2` requires bias (`conditions:
[bias]`) as D169 says; DCR / afterpulsing / recovery cannot require a bias because SNSPD bias is a current and
`bias_v` is volts: the defs put it in condition, which the 8 new detector rows do.

Findings:

| id | rating | evidence | fix |
|---|---|---|---|
| R1 fsr_nm def (+laser) | imprecise | def puts two different quantities (longitudinal-mode spacing, intracavity-filter FSR) under one laser parameter; `fsr_ghz` (laser since D81) did not get the same clarification | add the same laser clause to `fsr_ghz`; consider a separate `mode_spacing_nm` if more laser rows arrive (lu2024 m23 / m24 are mode spacings) |
| R2 gap_nm def (+crossing, +switch_fabric) | imprecise | def still reads "coupling gap (vertical gap for inter-layer transitions)"; the crossing row (nan2025 3D crossing m7) is a vertical interlayer gap of a multilevel crossing, the switch row (tanizawa2015 m13) a DC gap | def: "... vertical gap for inter-layer transitions and multilevel crossings" |
| R3 series_resistance_ohm classes | imprecise (registry gap) | zhang2023 (lit_01) SOA differential resistance 10 ohm is a confirmed skipped value (D81 criterion met) but amplifier was neither added nor listed in D250 | add `amplifier` or record the deferral in D250 |
| R4 coupling_angle_deg vs layout | imprecise | new geometry parameter for bent DCs (elsaeed2024, 4 rows) but the `dc` template (`component_layouts.yaml`, optional list) does not use it, so a bent DC is drawn as a straight DC | add `coupling_angle_deg` to the `dc` template optional list (layout owner) |
| R5 primary_by_class (D251) | imprecise (naming) | key is `class.subtype` (`crossing.mmi`) under a name that says class; the 19 crossing_loss_db rows on crossing.mmi all carry scope per_component, so the override filter works; app does not read it yet (documented in D251) | rename to `primary_by_subtype` or document the key form in the file header |
| R6 power_conversion_efficiency_pct | ok (caveat) | one parameter spans amplifier pump-to-signal, SHG fundamental-to-harmonic and OPO pump-to-signal+idler efficiencies; all 4 rows state the definition in condition | none; plots must split by class |
| R7 shi2024 dual efficiency | ok (caveat) | m9 (%/W/cm2, printed) and m1 (%/W) hold the same measurement in two normalizations; notes say deliberate | none |
| R8 enum / subtype | ok | platform `gap_on_insulator`, `iii_v_on_si_epi`, subtype `nonreciprocal.other` used exactly by the D252 reclasses; app color families pending (D251, app owner) | none |

## Part 2: gap-fill (lit_01..lit_06)

Every add_metrics row in the packet equals the merged row (no replay drift). No value is cited from other work, no
duplicate of an existing row, no D250-rejected parameter slipped in, every row satisfies the registry `conditions`
(wavelength for gain_db_per_cm / q_external / pdl_db / conversion_efficiency_pct_per_w_cm2, bias for
dark_current_density_ma_per_cm2). D254 rulings applied as written (virot2014 F with the printed gain, brisson2023
200 MHz as the paper's maximum count rate, I-V-slope resistances, hosseini2015 typical ER kept as a note).

Reclasses and new components (all ok):
- mckenna2022 SHG racetrack -> frequency_converter.shg, OPO -> frequency_converter.other: all existing parameters (Q,
  FSR, pump threshold, poling period, geometry) allowed for the new class.
- song2025a four-port and 5x5 routers -> nonreciprocal.other (multi-port splitting routers, p.9-10); three-port stays
  circulator.
- kuznetsov2025 (4) and wilson2019 (5) -> gap_on_insulator (GaP bonded via Al2O3 onto SiO2 on Si; kuznetsov p.8
  Methods, wilson p.1-2); song2021 si_px / hs (9) -> iii_v_on_si_epi (InP-on-Si template on V-grooved Si, p.1-3);
  inp_px rows on native InP correctly left as inp.
- meng2023 double_heater (endurance ~500,000 cycles tied to the two-sided heaters, p.5, p.10) and single_pair (6 levels,
  Fig. 4, p.7-9): text ties each value to that design, the 4-bit element uses single-sided heaters (p.4 Fig. 1(d));
  fab_org_ids GWU;MIT supported by the p.14 contributions (D80b).

Non-ok rows:

| id | rating | evidence | fix |
|---|---|---|---|
| cmp_lit_ronn2019_er_al2o3_si3n4_slot_amp_250um-m3 | imprecise | p.7 Table 1, p.8 Eq. (1): value / basis right; notes say "as the gain_db row m3" but this component has no gain_db row (that row is on the 1200 um component) | notes |
| cmp_lit_ronn2019_er_al2o3_si3n4_slot_amp_700um-m3 | imprecise | same cross-reference error | notes |
| cmp_lit_song2025a_mo_si_four_port_router-m9 | imprecise | p.9 text cites Fig. 4(e); the p.8 caption labels (d) the four-port spectra | locator p.9 Fig. 4(d)-(e) as sibling m3, note |
| cmp_lit_suda2025_polymer_sm_wg_fr4-m11, -m12 | imprecise | p.3-4: PDL is the TE-TM difference of the fiber-to-fiber IL; scope empty | scope fiber_to_fiber, includes |
| cmp_lit_qi2024_ingaas_spad-m11 | imprecise | p.5 Fig. 5(c): 119 ps FWHM ok; notes attribute the gate-width rejection to "D169" instead of D250 | notes |
| cmp_lit_kim2019_opa_32el-m6, -m7; cmp_lit_kim2019_opa_125el-m6 | imprecise | p.9 Sec. V / p.10 Table I give no wavelength; sibling rows m1 / m2 of the same calibrated beam carry c_band inferred (rule 8) | band c_band, wavelength_inferred true, note |
| cmp_lit_shikama2017_fifo_6mode_19core-m8 | imprecise | p.5 Sec. IV.A defines the MDL as excess loss on insertion of the FI device and FM-MCF (notes said setup subtraction not stated); no scope; c_band set without wavelength_inferred (sibling m2 inferred) | scope device_total, includes / excludes, wavelength_inferred, notes |
| cmp_lit_huang2019a_mode_filter_lpg-m11, -m12 | imprecise | p.4 Sec. IV does not say the ~190 / ~140 nm estimates use the RW2 E11 spectrum | notes |
| cmp_lit_huang2019a_mode_filter_lpg-m13 | imprecise | p.4 Sec. IV, Fig. 6(a): one 197 nm value stated for TE and TM; polarization blank | polarization both |
| cmp_lit_qi2025_fp_slr_cavity-m11 | imprecise | p.5 Sec. III B: "before undercut" is an inference from the 120 mW operating point, not stated | condition marks the inference |
| cmp_lit_tanizawa2015_mz_element_tm-m11 | imprecise | p.4 envelope definition belongs to the cross state; p.5 Fig. 4 draws the envelope fit only in panel (b); the bar 4.3 nm is marked on the measured trace in (a) | condition, notes |
| cmp_lit_tanizawa2015_mz_element_tm (component notes) | imprecise | notes still say the 1.5 mW trimming power is "not entered" although power_consumption_w m10 holds it | notes |

Misses that D169 now allows (lit_05; all other batches none):
- huang2019a: calculated -10 dB width 142 nm (1500-1642 nm, transfer-matrix, TE; p.2 Sec. II, Fig. 2(a)) ->
  add bw_10db_nm m17, simulated.
- bock2010 FDTD crossing: simulated loss variation < 0.1 dB over 1520-1580 nm, TE and TM (p.5 Sec. 3, Fig. 2) -> add
  wdl_db m3, simulated.

Observations (no fix proposed): zhang2023 (lit_01) Fig. 10 is reproduced from the authors' own OFC 2022 paper and the
WTL1 values (incl. new m7 / m8) are restated in this paper's Sec. 5 text: accepted by the lit_01 audit, rule 3 could
be read against it (question Q5). meng2023 4bit m4: 15 x 0.75 dB = 11.25 dB vs printed 12 dB (entered as printed).
starnault2026 C+L isolation bandwidth printed only as 14 THz: not converting it is right.

## Part 3: convention sweep 2

All 116 ops were checked (not only a sample). Every op changed only basis / notes (mehta2016 also value, value_max;
song2021a also qualifier), every conversion is an exact power of ten or percent-to-fraction, old notes are kept
verbatim with the printed value and the original basis appended, no simulated row was touched (D83f).
fill_factor: mehta2016 (p.5 Methods 1 defines the duty cycle as the SiO2-gap fraction, 0.1-0.4 -> 0.6-0.9 derived),
jahed2022 (69 % -> 0.69, undefined, dual-etch staircase), song2021a (near 50 % -> 0.5 approx), qiao2017 (60 %, note),
li2022b (rho 0.6, undefined; Fig. 2(a) does not label rho) are correct.

Wrong / imprecise ops:

| id | rating | evidence | fix |
|---|---|---|---|
| lit_03 song2021 absorber_thickness_nm 1000 nm: si_px40-m5, si_px30-m3, si_px20-m3, inp_px40-m3, inp_px30-m3, inp_px20-m3, hs_d10-m4, hs_d15-m3, hs_d20-m3, hs_d25-m3, hs_d30-m3, hs_d40-m3 (12) | wrong | p.2 Fig. 1(c) epitaxial-stack label prints the InGaAs layer as 1000 nm (stored unit); text prints 1 um (p.3 Sec. II.C, p.5 Sec. IV.D). D255 excludes rows whose figure label prints the stored unit (guo2026 precedent); the text-only scan could not see the image label | basis back to design_target, locator adds p.2 Fig. 1(c), notes give both forms |
| bf_02 cmp_guo2026_wg_ridge_0p4um-m2 | wrong | p.5 Fig. 2(a) ridge cross-section inset labels 400 nm; the sibling cmp_guo2026_gc_532-m11 was excluded on that label, so the two 400 nm rows now carry different bases | revert to design_target, add Fig. 2(a) to locator |
| bf_02 cmp_guo2026_gc_532-m5 fill_factor 0.7 | wrong | p.5 Fig. 2(b) GC sketch draws the rho bracket over the etched groove opening between two teeth (checked on the render): rho is the gap fraction, so the sweep note "not defined in the paper" is contradicted and 0.7 stored as a tooth fraction is wrong under D253. Supporting inference only: 100 nm etch with ~60 deg sidewalls (p.13) at 285 nm period fits a 0.7 gap better than a 0.7 tooth | value 0.3, derived, printed value and Fig. 2(b) definition in notes; m3 notes aligned. Minimum alternative if the sketch is judged too weak: keep 0.7, correct the note (question Q2); D253's "do not define" list then loses guo2026 |
| ofc_03 cmp_ofc2026_th2a1_plc_sin_ssc_to_soa-m3 | imprecise | range 1600..3000 nm; p.~1 / p.~2 Sec. 2 print 1.6 to 3.0 um in 0.2 um steps; note gives only 1.6 um | notes |

Unchanged rows that look like rescales (misses). Candidates found by a scan of all merged rows not touched by sweep2
(dimension parameters, non-derived basis, the same quantity present in another length unit somewhere in the text,
hyphenated forms included): 38, plus one found by the sweep sub-auditor with a range-aware scan. All 39 read at the
locator.

| id | rating | evidence | fix |
|---|---|---|---|
| bf_01 cmp_boynton2020_vertical_coupler-m3 tip_width_nm 200 | wrong (miss) | p.4 prints the minimum width as 0.2 um; the only "200 nm" in the text is the LN film thickness. This is the row D157 names as the example to fix | derived, D157 note |
| pilot_1 cmp_li2026aa_adiabatic_splitter-m7 width_nm 800 | wrong (miss) | p.3 prints W = 0.8 um; "800 nm" in the text is only the operating bandwidth | derived, D157 note |
| ofc_02 cmp_ofc2026_th1d4_fs_glass_wg-m2 width_nm 18000..20000 | wrong (miss) | pNA Sec. 2 prints about 18-20 um (measured); the scan missed the range form | derived, D157 note |
| lit_05 cmp_lit_elsaeed2024_bent_dc_40/60/70-m3, -m4, straight_dc_50-m4 (7) | imprecise | cited Fig. 8 / 11 / 12 captions print 0.1 / 0.38 um; p.2 Fig. 1 caption gives 100 nm / 380 nm for all DCs (stored unit) | locator p.2 Fig. 1 caption first, notes with both forms; basis stays |
| lit_05 cmp_lit_nevlacsil2020_mmi_te_tm-m4, smwg_crossing-m4 | imprecise | cite only p.5 Table 2 (0.7 um); p.4 Sec. 2 prints 700 nm | locator as the sibling rows |
| bf_09 cmp_valdez2023a_sin_feeder_waveguide-m3 | imprecise | p.1 (Sec. I, not Sec. II) prints 0.18 um; p.3 Fig. 2 label prints 180 nm | locator, notes |
| 26 others (cai2025 taper, ectc51909.2023.00009 x4, guo2026 x4, li2026aa ssc, elsaeed2024 bent_dc_50 x2 / straight m6, kim2019 x2, maeda2023 taper, nevlacsil2020 x2, qiao2017 rib, vazquezcordova2014 x3, wang2026 visible m9, liu2025b rib m2, wang2024b spiral x2) | ok | stored unit printed at the locator (e.g. liu2025b p.4 "180 nm x 1000 nm"; guo2026 Fig. 2(a) 0.8 um / 400 nm labels) | none |

Correction to the D255 log: wang2026 Table II was not excluded for an "unknown printed unit": the table footnote
(page_05 render) gives um, so 1.6 um is printed in the stored unit and the row is ok as stored.

Outside the D255 scope (non-dimension prefix conversions, D82d): a scan of all merged rows for values absent in the
stored unit but present in another unit of the same family (Hz / kHz / MHz / GHz / THz, uW / mW / W, dB/m, time,
capacitance, current) gives 32 candidates with measured / author_estimate basis. Verified at the locator (6, all
measured, all stored rescaled from the printed unit and not derived): lit_02 lu2024 m12 (45 kHz -> 45000 Hz),
lit_02 billah2018 m3 (2.7-5.8 MHz -> Hz; value stored as "2700000.0"), lit_06 deng2026 topic_ring m1 (3.20 / 3.12 THz
-> GHz), bf_05 aihara2026 m5 (93 mW -> 0.093 W), pilot_2 didier2026 m1 (1.42 W -> 1420 mW), lit_01 mckenna2022 OPO
m1 (73 uW -> 0.073 mW; the gap-fill's own SHG m15 690 uW -> 0.69 mW is derived, so the batch is internally
inconsistent). The other 26 (mostly OFC linewidth_hz in kHz, dB/m author_estimate losses, mohl2025 Table V rates) are
unverified candidates for a follow-up sweep; the author_estimate dB/m rows (cai2025, powell2024a, OFC Th1D.6 / Th1D.7)
already state the conversion in notes and need a ruling (Q1).

## Method notes on the sweep

- The D255 test "value absent in the stored unit anywhere in the source text" has three blind spots seen here: stored-
  unit labels inside figure images (song2021, guo2026 ridge), coincidental matches of an unrelated quantity in the
  stored unit (boynton2020, li2026aa), and range / double-space forms ("18-20 um", "1000  nm"). A follow-up should
  decide per row at the locator, not on a whole-text string match.
- Proposed consistent rule (Q3): when the source prints the stored-unit form for the same quantity anywhere (text,
  table or figure label), keep the basis and cite that locator; derived only when the quantity is printed solely in
  another unit.

## Questions for the coordinator

1. Q1: Does D82d apply to non-dimension prefix conversions (kHz -> Hz, W <-> mW, THz -> GHz)? If yes, a sweep 3 over
   the 32 candidates; for author_estimate rows whose value is unit-converted, keep author_estimate (the uncertainty
   is the assumed input, analogous to D83f) with the conversion in notes.
2. Q2: guo2026 rho: accept the gap-fraction reading of the Fig. 2(b) sketch (store 0.3) or keep 0.7 with a corrected
   note.
3. Q3: adopt the "stored unit printed anywhere for the same quantity -> keep basis" rule above (it decides song2021,
   guo2026 ridge and the 10 imprecise locator rows consistently).
4. Q4: series_resistance_ohm for amplifier (zhang2023 SOA 10 ohm), or record the deferral in D250.
5. Q5: zhang2023 WTL1 values restated from the authors' own conference paper (rule 3).

## Proposed correction files

One file per affected batch, `data/_staging/components/<batch>/extaudit.yaml`, replay order patch, sweep, gapfill,
addendum, geometry, geoaudit, coord, sweep2, coord2 (lit batches), extaudit. 55 ops in 14 batches. The D82d ops
(lit_01 mckenna2022 OPO m1, lit_02 lu2024 m12 / billah2018 m3, lit_06 deng2026 topic_ring m1, bf_05, pilot_2) depend on
Q1; the guo2026 m5 / m3 ops depend on Q2.

### lit_01 (4 ops)

```yaml
# lit_01: proposed data/_staging/components/lit_01/extaudit.yaml (2026-10-22 ext audit; replay after sweep2.yaml and coord2.yaml)
metrics:
  cmp_lit_ronn2019_er_al2o3_si3n4_slot_amp_250um-m3:
    notes: 'Printed 20.1 +/- 7.31 dB/cm (Table 1). Authors'' arithmetic on measured signal enhancement and the measured
      unpumped loss (Eq. 1; same basis as gain_db m3 of the 1200 um component): derived. p.6 text: ''up to'' this value
      with 4.5 mW injected pump. Net material gain per length (lower bound, alpha0 ~ 0 assumed) not entered.'
    why: Notes referred to 'the gain_db row m3', which does not exist on this component (m3 is this row; gain_db m3 is on
      the 1200 um component)
  cmp_lit_ronn2019_er_al2o3_si3n4_slot_amp_700um-m3:
    notes: 'Printed 16.9 +/- 4.70 dB/cm (Table 1). Authors'' arithmetic on measured signal enhancement and the measured
      unpumped loss (Eq. 1; same basis as gain_db m3 of the 1200 um component): derived. Net material gain per length (lower
      bound, alpha0 ~ 0 assumed) not entered.'
    why: Notes referred to 'the gain_db row m3', which does not exist on this component (m3 is this row; gain_db m3 is on
      the 1200 um component)
  cmp_lit_song2025a_mo_si_four_port_router-m9:
    locator: p.9 Fig. 4(d)-(e)
    notes: Printed theoretical crosstalk of -21 dB (positive magnitude entered). The p.9 text cites Fig. 4(e) for the theoretical
      spectra; the Fig. 4 caption (p.8) labels (d) the four-port spectra and (e) the phase gradients.
    why: Text and caption label the four-port spectra panel differently; match the sibling isolation row m3 locator
  cmp_lit_mckenna2022_ppln_racetrack_opo-m1:
    basis: derived
    notes: 'Printed about 73 uW; uW -> mW (D82d): derived. Extracted by fitting the output-vs-input curve with eq. (4) (standard
      fit of own data). The 25.65 C printed on p.4 is the near-degenerate (mu ~ 0) operating point, not the threshold measurement.'
    why: 'D82d: a prefix conversion makes the value derived (sibling SHG row m15, 690 uW -> 0.69 mW, already derived)'
```

### lit_02 (4 ops)

```yaml
# lit_02: proposed data/_staging/components/lit_02/extaudit.yaml (2026-10-22 ext audit; replay after sweep2.yaml and coord2.yaml)
metrics:
  cmp_lit_suda2025_polymer_sm_wg_fr4-m11:
    scope: fiber_to_fiber
    includes: two fiber-waveguide facets and 11 mm propagation
    why: 'G_lit_02 audit: PDL is the TE-TM difference of fiber-to-fiber insertion loss (p.3-4); scope as on the IL rows
      m1 / m2 and the lit_05 gap-fill pdl rows'
  cmp_lit_suda2025_polymer_sm_wg_fr4-m12:
    scope: fiber_to_fiber
    includes: two fiber-waveguide facets and 11 mm propagation
    why: 'G_lit_02 audit: PDL is the TE-TM difference of fiber-to-fiber insertion loss (p.3-4); scope as on the IL rows
      m1 / m2 and the lit_05 gap-fill pdl rows'
  cmp_lit_lu2024_pcw_dfb-m12:
    basis: derived
    notes: '''reaches 45 kHz''; Lorentzian per the conclusion (p.9). Printed 45 kHz (measured value), stored in Hz: prefix
      conversion, basis derived (D82d).'
    why: 'ext audit (D82d, outside the D255 dimension scope): p.8 prints 45 kHz, stored 45000 Hz; a prefix conversion is
      derived (pending ruling Q1)'
  cmp_lit_billah2018_hcsel_dfb-m3:
    value: '2700000'
    value_max: '5800000'
    basis: derived
    notes: 'Values 2.7 / 2.9 / 5.8 / 4.2 MHz. Printed in MHz (measured values), stored in Hz: prefix conversion, basis derived
      (D82d).'
    why: 'ext audit (D82d, outside the D255 dimension scope): p.8 Sec. 4C prints 2.7 MHz etc., stored in Hz; prefix conversion
      is derived (pending ruling Q1); value strings without the float suffix'
```

### lit_03 (13 ops)

```yaml
# lit_03: proposed data/_staging/components/lit_03/extaudit.yaml (2026-10-22 ext audit; replay after sweep2.yaml and coord2.yaml)
metrics:
  cmp_lit_qi2024_ingaas_spad-m11:
    notes: FWHM timing jitter of the SPD module (SPAD + gating / readout electronics); the 117 ps effective gate width is
      not entered (gate width rejected as a registry parameter, D250)
    why: notes cited the gate width as "D169 not added"; the rejection is D250
  cmp_lit_song2021_si_px40-m5:
    basis: design_target
    locator: p.2 Fig. 1(c); p.3 Sec. II.C; p.5 Sec. IV.D
    notes: 'InGaAs absorption layer thickness. Fig. 1(c) (p.2, epitaxial stack of the PD on Si) prints 1000 nm, the stored
      unit; the text prints 1 um (p.3 Sec. II.C, 1-um-thick, p.5 Sec. IV.D). Not a unit rescale (D255 figure-label exclusion):
      basis design_target.'
    why: 'S1 audit: D255 excludes rows whose figure label prints the stored unit; song2021 Fig. 1(c) prints UID InGaAs 1000
      nm, so the sweep2 D157 rescale (design_target -> derived) is reverted'
  cmp_lit_song2021_si_px30-m3:
    basis: design_target
    locator: p.2 Fig. 1(c); p.3 Sec. II.C; p.5 Sec. IV.D
    notes: 'InGaAs absorption layer thickness. Fig. 1(c) (p.2, epitaxial stack of the PD on Si) prints 1000 nm, the stored
      unit; the text prints 1 um (p.3 Sec. II.C, 1-um-thick, p.5 Sec. IV.D). Not a unit rescale (D255 figure-label exclusion):
      basis design_target.'
    why: 'S1 audit: D255 excludes rows whose figure label prints the stored unit; song2021 Fig. 1(c) prints UID InGaAs 1000
      nm, so the sweep2 D157 rescale (design_target -> derived) is reverted'
  cmp_lit_song2021_si_px20-m3:
    basis: design_target
    locator: p.2 Fig. 1(c); p.3 Sec. II.C; p.5 Sec. IV.D
    notes: 'InGaAs absorption layer thickness. Fig. 1(c) (p.2, epitaxial stack of the PD on Si) prints 1000 nm, the stored
      unit; the text prints 1 um (p.3 Sec. II.C, 1-um-thick, p.5 Sec. IV.D). Not a unit rescale (D255 figure-label exclusion):
      basis design_target.'
    why: 'S1 audit: D255 excludes rows whose figure label prints the stored unit; song2021 Fig. 1(c) prints UID InGaAs 1000
      nm, so the sweep2 D157 rescale (design_target -> derived) is reverted'
  cmp_lit_song2021_inp_px40-m3:
    basis: design_target
    locator: p.2 Fig. 1(c); p.3 Sec. II.C; p.5 Sec. IV.D
    notes: 'InGaAs absorption layer thickness. Fig. 1(c) (p.2, epitaxial stack of the PD on Si) prints 1000 nm, the stored
      unit, and p.3 Sec. II.C states identical InGaAs PIN epitaxy on the native InP substrate; the text prints 1 um (p.3
      Sec. II.C, 1-um-thick, p.5 Sec. IV.D). Not a unit rescale (D255 figure-label exclusion): basis design_target.'
    why: 'S1 audit: D255 excludes rows whose figure label prints the stored unit; song2021 Fig. 1(c) prints UID InGaAs 1000
      nm, so the sweep2 D157 rescale (design_target -> derived) is reverted'
  cmp_lit_song2021_inp_px30-m3:
    basis: design_target
    locator: p.2 Fig. 1(c); p.3 Sec. II.C; p.5 Sec. IV.D
    notes: 'InGaAs absorption layer thickness. Fig. 1(c) (p.2, epitaxial stack of the PD on Si) prints 1000 nm, the stored
      unit, and p.3 Sec. II.C states identical InGaAs PIN epitaxy on the native InP substrate; the text prints 1 um (p.3
      Sec. II.C, 1-um-thick, p.5 Sec. IV.D). Not a unit rescale (D255 figure-label exclusion): basis design_target.'
    why: 'S1 audit: D255 excludes rows whose figure label prints the stored unit; song2021 Fig. 1(c) prints UID InGaAs 1000
      nm, so the sweep2 D157 rescale (design_target -> derived) is reverted'
  cmp_lit_song2021_inp_px20-m3:
    basis: design_target
    locator: p.2 Fig. 1(c); p.3 Sec. II.C; p.5 Sec. IV.D
    notes: 'InGaAs absorption layer thickness. Fig. 1(c) (p.2, epitaxial stack of the PD on Si) prints 1000 nm, the stored
      unit, and p.3 Sec. II.C states identical InGaAs PIN epitaxy on the native InP substrate; the text prints 1 um (p.3
      Sec. II.C, 1-um-thick, p.5 Sec. IV.D). Not a unit rescale (D255 figure-label exclusion): basis design_target.'
    why: 'S1 audit: D255 excludes rows whose figure label prints the stored unit; song2021 Fig. 1(c) prints UID InGaAs 1000
      nm, so the sweep2 D157 rescale (design_target -> derived) is reverted'
  cmp_lit_song2021_hs_d10-m4:
    basis: design_target
    locator: p.2 Fig. 1(c); p.5 Sec. IV.D
    notes: 'InGaAs absorption layer thickness. Fig. 1(c) (p.2, epitaxial stack of the PD on Si) prints 1000 nm, the stored
      unit; the text prints 1 um (p.3 Sec. II.C, 1-um-thick, p.5 Sec. IV.D). Not a unit rescale (D255 figure-label exclusion):
      basis design_target.'
    why: 'S1 audit: D255 excludes rows whose figure label prints the stored unit; song2021 Fig. 1(c) prints UID InGaAs 1000
      nm, so the sweep2 D157 rescale (design_target -> derived) is reverted'
  cmp_lit_song2021_hs_d15-m3:
    basis: design_target
    locator: p.2 Fig. 1(c); p.5 Sec. IV.D
    notes: 'InGaAs absorption layer thickness. Fig. 1(c) (p.2, epitaxial stack of the PD on Si) prints 1000 nm, the stored
      unit; the text prints 1 um (p.3 Sec. II.C, 1-um-thick, p.5 Sec. IV.D). Not a unit rescale (D255 figure-label exclusion):
      basis design_target.'
    why: 'S1 audit: D255 excludes rows whose figure label prints the stored unit; song2021 Fig. 1(c) prints UID InGaAs 1000
      nm, so the sweep2 D157 rescale (design_target -> derived) is reverted'
  cmp_lit_song2021_hs_d20-m3:
    basis: design_target
    locator: p.2 Fig. 1(c); p.5 Sec. IV.D
    notes: 'InGaAs absorption layer thickness. Fig. 1(c) (p.2, epitaxial stack of the PD on Si) prints 1000 nm, the stored
      unit; the text prints 1 um (p.3 Sec. II.C, 1-um-thick, p.5 Sec. IV.D). Not a unit rescale (D255 figure-label exclusion):
      basis design_target.'
    why: 'S1 audit: D255 excludes rows whose figure label prints the stored unit; song2021 Fig. 1(c) prints UID InGaAs 1000
      nm, so the sweep2 D157 rescale (design_target -> derived) is reverted'
  cmp_lit_song2021_hs_d25-m3:
    basis: design_target
    locator: p.2 Fig. 1(c); p.5 Sec. IV.D
    notes: 'InGaAs absorption layer thickness. Fig. 1(c) (p.2, epitaxial stack of the PD on Si) prints 1000 nm, the stored
      unit; the text prints 1 um (p.3 Sec. II.C, 1-um-thick, p.5 Sec. IV.D). Not a unit rescale (D255 figure-label exclusion):
      basis design_target.'
    why: 'S1 audit: D255 excludes rows whose figure label prints the stored unit; song2021 Fig. 1(c) prints UID InGaAs 1000
      nm, so the sweep2 D157 rescale (design_target -> derived) is reverted'
  cmp_lit_song2021_hs_d30-m3:
    basis: design_target
    locator: p.2 Fig. 1(c); p.5 Sec. IV.D
    notes: 'InGaAs absorption layer thickness. Fig. 1(c) (p.2, epitaxial stack of the PD on Si) prints 1000 nm, the stored
      unit; the text prints 1 um (p.3 Sec. II.C, 1-um-thick, p.5 Sec. IV.D). Not a unit rescale (D255 figure-label exclusion):
      basis design_target.'
    why: 'S1 audit: D255 excludes rows whose figure label prints the stored unit; song2021 Fig. 1(c) prints UID InGaAs 1000
      nm, so the sweep2 D157 rescale (design_target -> derived) is reverted'
  cmp_lit_song2021_hs_d40-m3:
    basis: design_target
    locator: p.2 Fig. 1(c); p.5 Sec. IV.D
    notes: 'InGaAs absorption layer thickness. Fig. 1(c) (p.2, epitaxial stack of the PD on Si) prints 1000 nm, the stored
      unit; the text prints 1 um (p.3 Sec. II.C, 1-um-thick, p.5 Sec. IV.D). Not a unit rescale (D255 figure-label exclusion):
      basis design_target.'
    why: 'S1 audit: D255 excludes rows whose figure label prints the stored unit; song2021 Fig. 1(c) prints UID InGaAs 1000
      nm, so the sweep2 D157 rescale (design_target -> derived) is reverted'
```

### lit_04 (4 ops)

```yaml
# lit_04: proposed data/_staging/components/lit_04/extaudit.yaml (2026-10-22 ext audit; replay after sweep2.yaml and coord2.yaml)
metrics:
  cmp_lit_kim2019_opa_32el-m6:
    band: c_band
    wavelength_inferred: 'true'
    notes: '''achieving SLSR of 8.5 dB''; Table I small variant 8.5 dB. Wavelength not stated for this measurement; C band
      inferred as for the beam-divergence rows m1 / m2 of the same calibrated beam (Fig. 12).'
    why: rule 8 / consistency with m1 / m2 (same calibrated Fig. 12 beam, c_band inferred); kim2019 p.9 Sec. V gives no
      wavelength for the SLSR
  cmp_lit_kim2019_opa_32el-m7:
    band: c_band
    wavelength_inferred: 'true'
    notes: '''over 16 deg in theta via phase shifter control'' read as the demonstrated span (Table I steering range phi/theta
      18.5/16 deg, no bound), so no qualifier. Wavelength not stated for the phase-steering run; C band inferred as for
      m1 / m2.'
    why: rule 8 / consistency with m1 / m2; phase steering at an unstated wavelength (p.9 Sec. V)
  cmp_lit_kim2019_opa_125el-m6:
    band: c_band
    wavelength_inferred: 'true'
    notes: 'Table I ''Sidelobe Suppression'', This Work, large variant (125 elements): 7.4 dB; not in the running text.
      Wavelength not stated; C band inferred as for the beam-divergence rows m1 / m2.'
    why: rule 8 / consistency with m1 / m2 of the same component (c_band inferred); Table I p.10 gives no wavelength
  cmp_lit_shikama2017_fifo_6mode_19core-m8:
    scope: device_total
    includes: FI device and its PC connection to the FM-MCF
    excludes: setup (measured as the excess loss on insertion of the FI device and the FM-MCF)
    wavelength_inferred: 'true'
    notes: '''the mode dependent loss of the total output power was less than 1.7 dB for all the cores''; measured as the
      excess loss of the total output power on insertion of the FI device and the FM-MCF (p.5 Sec. IV.A), indicates cladding-mode
      leakage at butt coupling. Wavelength not stated for this value; C band inferred as for m2 (same Fig. 9 measurement).'
    why: shikama2017 p.5 Sec. IV.A defines the measurement as excess loss on insertion of FI device and FM-MCF (setup referenced
      out, old note said not stated); scope / includes / excludes as on sibling m7; C band not stated for this value, so
      wavelength_inferred true as on sibling m2
```

### lit_05 (17 ops)

```yaml
# lit_05: proposed data/_staging/components/lit_05/extaudit.yaml (2026-10-22 ext audit; replay after sweep2.yaml and coord2.yaml)
components:
  cmp_lit_huang2019a_mode_filter_lpg:
    notes: Fabricated with the authors' in-house microfabrication facilities (p.2 Sec. III); three of four authors at City
      University of Hong Kong, one at UESTC (borderline fab_org_ids, D84b-like). Rejection ratios (18.4 dB vs E21, 16.9
      dB vs E12 at 1550 nm), 10-dB rejection bandwidths (~190 nm, ~140 nm; author estimate assuming wavelength-flat higher-mode
      losses), RW2 -10 dB bandwidths (197 nm; 182 nm at 66 C), grating period / count and the calculated -10 dB bandwidth
      (142 nm) entered in the D169 gap-fill (m9-m17); RW2 -15 dB bandwidths (97 / 90 nm) and calculated -15 / -20 dB widths
      not entered (no -15 / -20 dB width parameter).
    why: 'G_lit_05 audit: mention the simulated -10 dB width row m17 added below'
  cmp_lit_bock2010_swg_crossing_fdtd:
    notes: Simulation-only layout (3 um, 12-segment tapers; pitch 200 -> 300 nm; segment length 150 nm), not the fabricated
      50 um-taper design (p.3-5). Simulated loss variation < 0.1 dB (TE and TM, 1520-1580 nm) entered as wdl_db m3 (D169).
    why: 'G_lit_05 audit: mention the simulated wdl_db row m3 added below'
metrics:
  cmp_lit_huang2019a_mode_filter_lpg-m11:
    notes: Printed ~190 nm (1440-1630 nm); estimated assuming wavelength-insensitive higher-mode insertion losses (BPM-confirmed);
      higher-mode loss spectra not measured. Which E11 spectrum the estimate uses is not stated.
    why: 'G_lit_05 audit: the text does not say the estimate uses the RW2 spectrum (p.4 Sec. IV)'
  cmp_lit_huang2019a_mode_filter_lpg-m12:
    notes: Printed ~140 nm (1450-1590 nm); estimated assuming wavelength-insensitive higher-mode insertion losses (BPM-confirmed);
      higher-mode loss spectra not measured. Which E11 spectrum the estimate uses is not stated.
    why: 'G_lit_05 audit: the text does not say the estimate uses the RW2 spectrum (p.4 Sec. IV)'
  cmp_lit_huang2019a_mode_filter_lpg-m13:
    polarization: both
    why: 'G_lit_05 audit: one value stated for the TE and TM spectra (p.4 Sec. IV, Fig. 6(a))'
  cmp_lit_qi2025_fp_slr_cavity-m11:
    condition: highly reflective operating point (120 mW heater power; undercut state not stated, presumably before undercut
      given the 120 mW tuning power); symmetric double-sided model (kappa_i + 2 kappa_e), external coupling per SLR
    why: 'G_lit_05 audit: the text does not state that the Fig. 4 measurement precedes the undercut (p.5 Sec. III B; Sec.
      IV)'
  cmp_lit_elsaeed2024_bent_dc_40-m3:
    locator: p.2 Fig. 1 caption; p.7 Fig. 12 caption
    notes: Fig. 1 caption gives the nominal gap of all DCs as 100 nm; Fig. 12 caption prints 0.1 um.
    why: 'D157 audit: stored 100 nm is printed in nm at p.2 Fig. 1 caption (all DCs); cite it, basis stays design_target'
  cmp_lit_elsaeed2024_bent_dc_40-m4:
    locator: p.2 Fig. 1 caption; p.7 Fig. 11 caption
    notes: Fig. 1 caption (and p.4) give the waveguide width of all DCs as 380 nm; Fig. 11 caption prints 0.38 um.
    why: 'D157 audit: stored 380 nm is printed in nm at p.2 Fig. 1 caption (all DCs); cite it, basis stays design_target'
  cmp_lit_elsaeed2024_bent_dc_60-m3:
    locator: p.2 Fig. 1 caption; p.7 Fig. 12 caption
    notes: Fig. 1 caption gives the nominal gap of all DCs as 100 nm; Fig. 12 caption prints 0.1 um.
    why: 'D157 audit: stored 100 nm is printed in nm at p.2 Fig. 1 caption (all DCs); cite it, basis stays design_target'
  cmp_lit_elsaeed2024_bent_dc_60-m4:
    locator: p.2 Fig. 1 caption; p.7 Fig. 11 caption
    notes: Fig. 1 caption (and p.4) give the waveguide width of all DCs as 380 nm; Fig. 11 caption prints 0.38 um.
    why: 'D157 audit: stored 380 nm is printed in nm at p.2 Fig. 1 caption (all DCs); cite it, basis stays design_target'
  cmp_lit_elsaeed2024_bent_dc_70-m3:
    locator: p.2 Fig. 1 caption; p.7 Fig. 12 caption
    notes: Fig. 1 caption gives the nominal gap of all DCs as 100 nm; Fig. 12 caption prints 0.1 um.
    why: 'D157 audit: stored 100 nm is printed in nm at p.2 Fig. 1 caption (all DCs); cite it, basis stays design_target'
  cmp_lit_elsaeed2024_bent_dc_70-m4:
    locator: p.2 Fig. 1 caption; p.7 Fig. 11 caption
    notes: Fig. 1 caption (and p.4) give the waveguide width of all DCs as 380 nm; Fig. 11 caption prints 0.38 um.
    why: 'D157 audit: stored 380 nm is printed in nm at p.2 Fig. 1 caption (all DCs); cite it, basis stays design_target'
  cmp_lit_elsaeed2024_straight_dc_50-m4:
    locator: p.2 Fig. 1 caption; p.5 Fig. 8 caption
    notes: Fig. 1 caption gives the nominal gap of all DCs as 100 nm; Fig. 8 caption prints 0.1 um.
    why: 'D157 audit: stored 100 nm is printed in nm at p.2 Fig. 1 caption (all DCs); cite it, basis stays design_target'
  cmp_lit_nevlacsil2020_mmi_te_tm-m4:
    locator: p.4 Sec. 2; p.5 Table 2
    why: 'D157 audit: stored 700 nm is printed in nm at p.4 Sec. 2 (crossing single-mode width); Table 2 prints 0.7 um;
      match sibling rows, basis stays design_target'
  cmp_lit_nevlacsil2020_smwg_crossing-m4:
    locator: p.4 Sec. 2; p.5 Table 2
    why: 'D157 audit: stored 700 nm is printed in nm at p.4 Sec. 2 (crossing single-mode width); Table 2 prints 0.7 um;
      match sibling rows, basis stays design_target'
add_metrics:
- metric_id: cmp_lit_huang2019a_mode_filter_lpg-m17
  component_id: cmp_lit_huang2019a_mode_filter_lpg
  parameter: bw_10db_nm
  value: '142'
  unit: nm
  wavelength_nm: '1500'
  wavelength_max_nm: '1642'
  polarization: te
  condition: -10 dB (90% conversion) width of the calculated E11 transmission of the three-section pi-phase-shifted LPG
    (L1 = 6, L2 = 14, L3 = 22 periods, kappa 372 /m), transfer-matrix method
  basis: simulated
  locator: p.2 Sec. II; p.2 Fig. 2(a)
  notes: 'Printed 142 nm (1500-1642 nm) for the chosen length distribution; TM results stated almost the same. Measured
    RW2 width: m13.'
  why: 'G_lit_05 audit: D169 bw_10db_nm for mode_converter; design-stage simulated width missed by the gap-fill'
- metric_id: cmp_lit_bock2010_swg_crossing_fdtd-m3
  component_id: cmp_lit_bock2010_swg_crossing_fdtd
  parameter: wdl_db
  value: '0.1'
  unit: dB
  qualifier: lt
  wavelength_nm: '1520'
  wavelength_max_nm: '1580'
  polarization: both
  scope: per_component
  condition: simulated loss variation of the wf = 350 nm SWG crossing over 1520-1580 nm, TE and TM (3D FDTD)
  basis: simulated
  locator: p.5 Sec. 3; p.5 Fig. 2
  notes: Printed loss variation < 0.1 dB for TE and TM polarizations.
  why: 'G_lit_05 audit: D169 wdl_db for crossing; simulated value of the FDTD design row missed by the gap-fill'
```

### lit_06 (3 ops)

```yaml
# lit_06: proposed data/_staging/components/lit_06/extaudit.yaml (2026-10-22 ext audit; replay after sweep2.yaml and coord2.yaml)
components:
  cmp_lit_tanizawa2015_mz_element_tm:
    notes: 'Test element on the same die. DC waveguides 430 nm wide with a 430 nm gap (Fig. 8(a); gap entered as m13). 3-dB
      DCs designed for TM (larger dimensional tolerance); designed cross state without heating. Crosstalk-below-35-dB bandwidth
      4.3 nm (bar) and 2.3 nm (cross, envelope fit, Fig. 4(b)) (entered as xt_bandwidth_nm m11 / m12). Cross-state trimming
      power 1.5 mW typical (entered as power_consumption_w m10). ''We fabricated the 32 x 32 switch'' (300 mm SOI, ArF immersion
      lithography) (p.3 Sec. 2); 13 of 15 authors at AIST, 2 at Furukawa Electric: fab org set to AIST (borderline D80b,
      facility not named).'
    why: 'G_lit_06: stale ''not entered'' for the 1.5 mW trimming power (m10 holds it); the envelope fit is drawn only for
      the cross state (p.5 Fig. 4 render)'
metrics:
  cmp_lit_tanizawa2015_mz_element_tm-m11:
    condition: crosstalk (leakage / intended output) below -35 dB, bar state; width read on the measured leakage trace
    notes: minimum crosstalk below -40 dB at about 1545 nm (m1); the envelope fit is drawn only in the cross-state panel
      Fig. 4(b), the bar-state 4.3 nm is marked on the measured trace in Fig. 4(a) (p.5)
    why: 'G_lit_06: p.4 envelope definition follows the cross-state TE-floor discussion and Fig. 4 shows the envelope fit
      only in panel (b); bar condition / notes misattributed it'
  cmp_lit_deng2026_topic_ring-m1:
    basis: derived
    notes: '''FSRs spanning from 3.20 THz to 3.12 THz''; dFSR/dL = -0.31 +/- 0.01 THz/um and d(lambda)/dL = 67.5 +/- 0.6
      nm/um from linear regression (Fig. 6, no registry parameter). Printed in THz (measured values), stored in GHz: prefix
      conversion, basis derived (D82d).'
    why: 'ext audit (D82d, outside the D255 dimension scope): p.10 Sec. 2 prints 3.20 / 3.12 THz, stored 3200 / 3120 GHz
      (pending ruling Q1)'
```

### bf_01 (1 ops)

```yaml
# bf_01: proposed data/_staging/components/bf_01/extaudit.yaml (2026-10-22 ext audit; replay after sweep2.yaml)
metrics:
  cmp_boynton2020_vertical_coupler-m3:
    basis: derived
    notes: 'tapers 0.2 to 1.2 um wide; the top layer then widens from 1.2 to 1.6 um over 100 um. D157: printed as 0.2 um
      (design_target value), stored in nm: unit rescale, basis derived.'
    why: 'D157 sweep (audit miss): printed 0.2 um, stored 200 nm (pure unit rescale of a printed dimension is derived; the
      only 200 nm in the text is the LN film; verified at p.4)'
```

### bf_02 (3 ops)

```yaml
# bf_02: proposed data/_staging/components/bf_02/extaudit.yaml (2026-10-22 ext audit; replay after sweep2.yaml)
metrics:
  cmp_guo2026_gc_532-m5:
    value: '0.3'
    basis: derived
    locator: p.6 Passive component characterization; p.5 Fig. 2(b)
    notes: Printed optimized duty cycle rho = 0.7 (p.6; design_target value). Fig. 2(b) GC sketch places the rho bracket
      over the etched groove opening (gap fraction); stored as the tooth fraction 1 - 0.7 = 0.3 (D253).
    why: 'S2 audit: Fig. 2(b) defines rho as the etched-gap width per period, so D253 gap-fraction conversion applies (not
      the undefined case)'
  cmp_guo2026_gc_532-m3:
    notes: Maximal simulated efficiency at p = 285 nm, duty cycle rho 0.7 (gap fraction per Fig. 2(b); tooth fraction 0.3);
      stated as 3.5 dB per coupler.
    why: 'S2 audit: align duty-cycle wording with the converted fill_factor row m5'
  cmp_guo2026_wg_ridge_0p4um-m2:
    basis: design_target
    locator: p.6; p.7 Fig. 4(b); p.5 Fig. 2(a)
    notes: Printed 0.4 um in the text (p.4, p.6) and on the Fig. 4(b) axis; the Fig. 2(a) ridge cross-section inset labels
      the width 400 nm (stored unit), so not a pure unit rescale (D255 figure-label exclusion, as cmp_guo2026_gc_532-m11).
    why: 'S2 audit: source prints the stored-unit value 400 nm in Fig. 2(a) for the same ridge; D255 excludes such rows'
```

### bf_05 (1 ops)

```yaml
# bf_05: proposed data/_staging/components/bf_05/extaudit.yaml (2026-10-22 ext audit; replay after sweep2.yaml)
metrics:
  cmp_aihara2026_dfb_membrane_300um-m5:
    basis: derived
    notes: '93 mW as stated (measured value), stored in W: prefix conversion, basis derived (D82d); temperature from the
      general statement that all measurements except the E-O response were at 55 C'
    why: 'ext audit (D82d, outside the D255 dimension scope): p.2 Sec. 3 prints 93 mW, stored 0.093 W (pending ruling Q1)'
```

### bf_09 (1 ops)

```yaml
# bf_09: proposed data/_staging/components/bf_09/extaudit.yaml (2026-10-22 ext audit; replay after sweep2.yaml)
metrics:
  cmp_valdez2023a_sin_feeder_waveguide-m3:
    locator: p.1 Sec. I; p.3 Fig. 2
    notes: 'SiN height as stated: 0.18 um in Sec. I (p.1), 180 nm in the Fig. 2 process-flow label (p.3).'
    why: 'D157 audit: stored 180 nm is printed in nm at p.3 Fig. 2 label; cite it (and fix Sec. II -> Sec. I), basis stays
      design_target'
```

### pilot_1 (1 ops)

```yaml
# pilot_1: proposed data/_staging/components/pilot_1/extaudit.yaml (2026-10-22 ext audit; replay after sweep2.yaml)
metrics:
  cmp_li2026aa_adiabatic_splitter-m7:
    basis: derived
    notes: 'single-mode width set to 0.8 um in the SSC, splitter and bend regions. D157: printed as 0.8 um (design_target
      value), stored in nm: unit rescale, basis derived.'
    why: 'D157 sweep (audit miss): printed 0.8 um, stored 800 nm (pure unit rescale of a printed dimension is derived; 800
      nm in the text is only the operating bandwidth; verified at p.3)'
```

### pilot_2 (1 ops)

```yaml
# pilot_2: proposed data/_staging/components/pilot_2/extaudit.yaml (2026-10-22 ext audit; replay after sweep2.yaml)
metrics:
  cmp_didier2026_tops-m1:
    basis: derived
    notes: 'Text and plot label 1.42 W; caption 1.43 W. Printed in W (measured value), stored in mW: prefix conversion,
      basis derived (D82d).'
    why: 'ext audit (D82d, outside the D255 dimension scope): p.3 prints 1.42 W, stored 1420 mW (pending ruling Q1)'
```

### ofc_02 (1 ops)

```yaml
# ofc_02: proposed data/_staging/components/ofc_02/extaudit.yaml (2026-10-22 ext audit; replay after sweep2.yaml)
metrics:
  cmp_ofc2026_th1d4_fs_glass_wg-m2:
    basis: derived
    notes: '''approximately 18-20 um'' for the fabricated waveguides; how measured not stated (micrographs Fig. 2). D157:
      printed as 18-20 um (measured value), stored in nm: unit rescale, basis derived.'
    why: 'S3 audit, D157 miss: pNA Sec. 2 prints the cross-section diameter as approx. 18-20 um; stored 18000..20000 nm
      is a pure unit rescale (derived); missed by the sweep2 scan (range form)'
```

### ofc_03 (1 ops)

```yaml
# ofc_03: proposed data/_staging/components/ofc_03/extaudit.yaml (2026-10-22 ext audit; replay after sweep2.yaml)
metrics:
  cmp_ofc2026_th2a1_plc_sin_ssc_to_soa-m3:
    notes: 'D157: printed as 1.6 to 3.0 um in 0.2 um steps (design_target value), stored in nm: unit rescale, basis derived.'
    why: 'S3 audit: row is a range 1600..3000 nm; printed value_max 3.0 um (p.~1 / p.~2 Sec. 2) was missing from the D157
      note'
```
