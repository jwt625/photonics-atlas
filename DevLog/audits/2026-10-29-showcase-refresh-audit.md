# Showcase refresh audit (2026-10-29, D414)

Fresh-context audit of the 24 showcase rows selected on 2026-10-29: 19 OK, 5 FIX (applied verbatim), 0 REJECT.

# Showcase audit, rows selected_on 2026-10-29 (fresh context, read-only)

Date: 2026-10-29. Scope: 24 rows of data/components/component_showcase.csv with selected_on 2026-10-29.
Checks per row: criterion / rationale numbers vs components.csv + component_metrics.csv and paper text (references/<id>/text.md,
page renders where the table is an image; Tu2D.4 and M1D.2 from PlayGround/20260320_OFC/extracted_text; li2026aa from
eo-modulator-atlas/references); primary metric present with basis measured; required geometry present (heroes);
ranking recomputed from the CSVs; privacy. CSV integrity: 43 rows, 7 fields each, no duplicate (template, role, rank),
all component ids exist.

Result: 19 OK, 5 FIX, 0 REJECT.

| # | component_id | template / role / rank | verdict |
|---|---|---|---|
| 1 | cmp_lit_fan2025_awg2_6x6_demux | awg hero 1 | OK (note A) |
| 2 | cmp_lit_pathak2014_awg_8x400_grid1nm | awg hero 2 | OK (note A) |
| 3 | cmp_lit_bogaerts2006_awg_16x200ghz | awg typical 2 | FIX |
| 4 | cmp_larocque2024_dc_michelson | dc typical 1 | OK |
| 5 | cmp_lit_elsaeed2024_straight_dc_50 | dc typical 2 | OK (note C) |
| 6 | cmp_lit_naraine2024_ec_tip350 | edge_taper hero 1 | FIX |
| 7 | cmp_li2026aa_ssc | edge_taper hero 2 | OK |
| 8 | cmp_lit_mangal2020_downward_gc_reflector | gc_1d hero 1 | OK |
| 9 | cmp_lit_murray2015_dev5_underetched | heater_ps hero 1 | OK |
| 10 | cmp_lit_yong2021_ps3_suspended_7pass | heater_ps hero 2 | OK |
| 11 | cmp_ofc2026_tu2d4_tin_heater_ps | heater_ps typical 1 | OK |
| 12 | cmp_liu2026d_tops_or | heater_ps typical 2 | OK |
| 13 | cmp_lit_sheng2012_mmi_1x2 | mmi hero 1 | OK |
| 14 | cmp_lit_lu2016a_mmi_2x2 | mmi typical 1 | OK (note D) |
| 15 | cmp_lit_naraine2024_mmi_1x2 | mmi typical 2 | OK |
| 16 | cmp_lit_boust2020_dfb_laser | ridge_laser hero 2 | OK |
| 17 | cmp_ofc2026_m1d2_single_section_dfb_600um | ridge_laser typical 1 | OK |
| 18 | cmp_lit_isichenko2023_sin_ring_780 | ring_bus hero 2 | FIX |
| 19 | cmp_lit_luke2020_ring_r80_w2_etch400 | ring_bus typical 1 | OK |
| 20 | cmp_lit_shang2017_vertical_coupler | transition_bilayer hero 2 | OK |
| 21 | cmp_lit_neutens2025_wg_w1000 | waveguide_xsec hero 1 | OK (note B) |
| 22 | cmp_lit_song2024a_wg_2p5um | waveguide_xsec hero 2 | OK |
| 23 | cmp_lit_zhang2013a_pso_y_junction | y_branch hero 1 | FIX |
| 24 | cmp_lit_lin2019_asym_y_junction_family | y_branch typical 1 | FIX |

Out of scope: cmp_ofc2026_m1e6_sin_ring_r75um (ring_bus typical, rank 1 -> 2) keeps selected_on 2026-10-20, so it is not
among the 24 rows; its text is unchanged.

## FIX items (exact replacement text)

### 3. cmp_lit_bogaerts2006_awg_16x200ghz (awg typical 2), rationale
Issue: two pathak2014 copies sit 0.1 dB from the 2.1 dB median, not one: 16 x 200 GHz 1 nm grid (2.0 -> 3.7 dB) and
4 x 400 GHz 5 nm grid (2.2 -> 2.5 dB) (references/pathak2014 p.4 Table I; metrics rows of both ids, geo complete).
Criterion count: n = 28 reproduces only with bound-only components excluded (suzuki2021 "< 2 dB"); with it n = 29,
median unchanged 2.1 dB. Criterion may stay; optional clarity edit given.

Replacement rationale:
"imec 248 nm DUV SOI: 16-channel 200 GHz AWG with 36 arms, 500 x 200 um; 2.2 dB insertion loss in the centre output ports (central input, normalized to a photonic wire), general crosstalk -17 to -20 dB, 3 dB centre-to-edge nonuniformity. Ties at 0.1 dB from the median with two pathak2014 copies (16 x 200 GHz 1 nm grid, 2.0 dB; 4 x 400 GHz 5 nm grid, 2.2 dB; both best-channel ends of a channel range) broken by the single centre-port value"

Optional criterion:
"foundry AWG with measured insertion loss closest to the median of measured AWG insertion loss (2.1 dB, n = 28 wdm.awg components, bound-only values excluded), reporting n_arms and n_channels"

### 6. cmp_lit_naraine2024_ec_tip350 (edge_taper hero 1), rationale
Issue: Table III (p.8) is titled "Best measured polarization-independent SiN edge couplers"; 350 nm is the best
polarization-independent tip at 1550 nm LF, not strictly the best tip of the sweep (Fig. 5(b) TE / TM at 300 nm are
about equal). Numbers all verified (0.52 TE / 0.60 TM, 2.5 um spot, 100 um taper, 0.75 um access, 400 nm LPCVD SiN,
4.5 um thermal SiO2, 3 um PECVD SiO2).

Replacement rationale:
"0.52 dB per coupler TE (0.60 dB TM) at 1550 nm with a tapered lensed fiber (2.5 um spot), best polarization-independent tip of a measured tip-width sweep (Table III); 350 nm tip, 100 um linear inverse taper, 0.75 um access waveguide, 400 nm LPCVD SiN on 4.5 um thermal SiO2, 3 um PECVD SiO2 cladding; Applied Nanotools SiN rapid-prototyping process"

### 18. cmp_lit_isichenko2023_sin_ring_780 (ring_bus hero 2), rationale
Issue: "Higher Q_i values in the atlas are ge_silica only" is false atlas-wide: cmp_lit_heim2025_coil_resonator
(sin, resonator.other, q_intrinsic 200 M, measured) is higher. True only within the ring_bus classes. All other
numbers verified (references/isichenko2023 p.3 lines 142-147: 145 M / 65 M, 30 dB, 5.84 mm, 0.36 dB/m, 40 nm x 4 um,
15 / 6 um claddings, TM; acknowledgement p.7).

Replacement rationale:
"Q_i 145 M (loaded Q 65 M, 30 dB extinction) at 780 nm, TM mode, from an unbalanced-MZI-calibrated resonance scan; radius 5.84 mm as printed for the two resonators of the 0.36 dB/m loss fit; Si3N4 core 40 nm x 4 um on 15 um lower SiO2, 6 um upper SiO2; bus-waveguide coupled; fabrication credited to Honeywell (acknowledgement). Second platform (sin). Gap and bus width not reported (drawn schematically). Replaces M1D.4 (sin, Q_i over 30 M). Higher measured Q_i among ring_bus components is ge_silica only (Th1D.6, Th1D.7, chen2026a)"

### 23. cmp_lit_zhang2013a_pso_y_junction (y_branch hero 1), rationale
Issue: the paper says "Y-junctions in 26 dies were tested" (references/zhang2013a p.5, text line 332; reticle size
2.5 x 3.2 cm stated separately), not 26 reticles. Other numbers verified (0.28 +/- 0.02 dB, die 0.27 +/- 0.01 dB,
2 um spline taper 0.5 -> 1.2 um, 220 nm Si, 2 um BOX, 2.3 um oxide, 248 nm, 8-inch).

Replacement rationale:
"0.28 +/- 0.02 dB cross-wafer mean excess loss (26 dies, 8-inch wafer; one die 0.27 +/- 0.01 dB) from the slope of cascaded Y-junction MZ loops; 2 um spline taper from 0.5 to 1.2 um, 500 nm waveguides, 220 nm Si, 2 um BOX, 2.3 um oxide cladding, 248 nm lithography (fab not named). Only y_branch component with a stated length and a measured excess loss; SOI"

### 24. cmp_lit_lin2019_asym_y_junction_family (y_branch typical 1), rationale
Issue: "the per-design rows carry neither the length nor the fab" is false for the fab: all 11 cmp_lit_lin2019_y_r1_*
rows have fab_org_ids org_applied_nanotools; they carry only imbalance_db (14 metric rows) and no length_um.

Replacement rationale:
"Applied Nanotools EBL, 220 nm SOI on 2 um BOX: family of 11 asymmetric Y-junctions sharing splitting length 2.32 um and 500 nm waveguides; measured split ratio 0 to -18 dB across the C-band, excess loss below 0.5 dB from cascaded structures (derived). Array-level row: the per-design rows carry only the split ratio, no length; branch radii r1 0.12-1.70 um are not template dimensions"

## Notes (no change proposed; for coordinator)

- A (awg heroes): both heroes rank on the best-channel end of a per-channel range (fan2025 1.14 of 1.14-2.75; pathak2014
  1.3 of 1.3-2.7). This is the usual AWG best-channel convention and both rationales print the full range. If the
  "bounds of a range are not hero values" ruling is meant to cover per-channel ranges too, rank 1 becomes fan2025 AWG1
  8 x 8 (1.26 dB, single central-channel value, geo complete) and the soi rank 2 would fall to bogaerts2006 (2.2 dB,
  already typical 2). Same pattern, ranking unaffected: yong2021 0.63 is the low end of 0.63-0.67 (text single 0.65,
  still rank 2); mmi rationale "qiao2017 0.12 dB" is the low end of 0.12-0.56 dB over 1500-1570 nm (only cited as next).
- B (waveguide_xsec): the derived exclusion also removes values that are measured numbers rescaled per D82d / D157:
  riemensberger2022 "as low as 2.5 dB/m" (0.025 dB/cm, sin, 2.45 x 0.91 um, derived) would beat neutens2025 0.03 if
  unit-rescaled values counted; wang2024b (old hero, about 8-10 dB/m) dropped for the same reason. Consistent with the
  literal ruling; flagging only because the basis there marks a unit conversion, not a computation.
- C (dc typical 2): an alternative foundry candidate with both dimensions exists: cmp_lit_gao2025a_adc_3db (AMF,
  splitter.adiabatic, measured insertion_loss_db 0.21 / 0.24 dB TE at 1550 nm, scope unspecified). elsaeed2024 is a
  defensible pick (same class as rank 1, measured coupling ratios); neither has a measured excess_loss_db.
- D (mmi typical 1): "n = 23" reproduces as measured + derived per_component with bound-only values dropped (also as
  measured any scope); measured + derived per_component with bounds gives n = 26, median 0.226 dB. lu2016a (0.22 dB)
  is closest to either median among foundry MMIs with both body dimensions.
- Recomputed rankings that hold: edge_taper (naraine2024 0.52 < naraine tip230 0.53 < li2026aa 0.56; lin2025 0.18
  derived), gc_1d (mangal2020 3.5 after sia2022 0.13 std, W4B.5 2D GC, mangal2018 3.3 extracted_from_figure),
  heater_ps (murray dev5 0.095, dev3 0.16, dev4 0.20, then yong2021 PS3 0.63-0.67 sin), heater median (Tu2D.4 15.5 mW,
  24th of 47), mmi hero (sheng2012 0.06; neutens2025 0.014 and xu2023a 0.07 lack body dimensions), laser.dfb median
  (40 mW, 4th of 7), ring_bus (isichenko 145 M top non-ge_silica with radius), transition (shang2017 0.185 next
  measured non-bound with taper length and both layers after wu2025; TSMC ECTC 0.009 / 0.013 lack geometry;
  singaravelu2019 0.058 band-edge minimum per ruling), waveguide_xsec (neutens 0.03; dangel2013 0.031 multimode
  excluded per ruling; song2024a < 0.05 is an upper bound, conservative for a lower-is-better metric), y_branch
  (zhang2013a only measured with length).
- Privacy: no addresses, emails, building names or personal names in the 24 rows (isichenko acknowledgement names a
  person in the paper; the rationale says "Honeywell" only). Only decision id in the new text is D111 (existing style).

# Coordinator rulings (2026-10-29)
## actives
- ge_pd: no change (accepted).
- heater_ps: heroes murray2015 dev5 (0.095 mW, IME SOI) and yong2021 PS3 (AMF SiN) accepted; closes D112 heater hero gap.
  typical 1 = exact median ofc2026 Tu2D.4 (15.5 mW, ST PIC100G, also a foundry component): kept literal median even
  though the card is schematic (no geometry rows); not swapped to yong2021 PS2 (would put one paper in two roles).
  typical 2 liu2026d_tops_or: drop the stale clause about foundry SOI heaters reporting no geometry; selected_on 2026-10-29.
- ridge_laser: hero 2 boust2020 (>200 mW) accepted. typical: laser.dfb now has >= 5 rows, so the literal D105 subtype
  median applies -> ofc2026 M1D.2 (40 mW) instead of huang2019 (its only length row is the 15 mm grating, drawn as the
  cavity would mislead). typical 2 stays empty (liu2025 basis question = data follow-up, not changed here).
## passives
- ring_bus: isichenko2023 hero 2 and luke2020 (HyperLight) typical accepted; typical 2 keeps M1E.6 (PDK / MPW ring)
  instead of keyvaninia2013 (ring inside a laser cavity, Q read through the laser: not a like-for-like ring card).
- mmi, dc, y_branch, awg: accepted as proposed (dc hero stays a gap: liu2026 0.2 dB is a band-edge minimum and a
  3-waveguide 1x2; y_branch 0.02 dB was the standard deviation).
## couplers
- Hero basis is `measured` only (derived excluded, literal D105): guo2026 gc and churaev2023 transition heroes dropped;
  no unverified derived candidate promoted. singaravelu2019 0.058 dB rejected (band-edge minimum, as dc liu2026).
  dangel2013 rejected (multimode 50 x 50 um, mode-scrambled MMF launch). Typicals kept. sin / sion count as two
  platforms. gc_1d SOI hero gap closed by mangal2020; the template `gaps` entry stays (gallery hides it automatically).
## audit
- 5 FIX applied verbatim (bogaerts2006 + criterion, naraine2024, isichenko2023, zhang2013a, lin2019).
- AWG heroes kept: a per-channel IL range across AWG outputs is the AWG reporting convention, not a band-edge minimum.
- Literal measured-only rule kept for conversion-derived values (riemensberger2022, wang2024b); dc typical elsaeed2024 kept.
