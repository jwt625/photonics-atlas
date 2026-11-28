# Batch lit_313 report

Papers: lit:kim2015, lit:xiong2012, lit:lu2021. Distilled 2026-11-28. Validation: `merge_component_staging.py
data/_staging/components/lit_313 --dry-run` -> +9 components, +52 metrics, 0 errors (the 2 warnings are in other
batches: guo2024a, ni2025b).

All three cached copies are arXiv preprints of the listed journal papers; values are taken from the preprint only
(journal versions not read), and every component note says so:

- kim2015: arXiv 1408.1739v2 (2014-08-11) of Nature Physics (10.1038/nphys3236), 26 pages incl. supplement.
- xiong2012: arXiv 1401.4768 of Nano Letters (10.1021/nl3011885), 19 pages (author manuscript layout).
- lu2021: arXiv 2101.04735v1 (2021-01-12) of Optica (10.1364/optica.418984), 7 pages.

Page-1 title check: all three match their source rows (kim2015 capitalization only). None is a correction / erratum.
`garbled_text_layer` false for all three; figure labels read from the page renders (lu2021 Fig. 1(b) also from a zoomed
render of the PDF page, helper in the batch scratch folder).

## lit:kim2015 (1 component / 5 metric rows)

| component | class | platform | metrics |
|---|---|---|---|
| cmp_lit_kim2015_silica_microsphere_d150 | resonator.disk | silica | linewidth 4.4 MHz + Q 4.4e7 (anti-Stokes mode, 349.3 MHz triplet, p.6 / Fig. 2(d)); linewidth 0.4 MHz + Q 4.9e8 (Stokes mode, 199.8 MHz triplet, p.7 / Fig. 3(d)); radius ~75 um derived from the ~150 um diameter |

- Scope: silica microsphere coupled by a tapered fiber, kept in scope under D411 / D633 (fiber-coupled amorphous silica
  resonator; ilchenko1999 and bino2018 precedents, class `resonator.disk`, platform `silica`).
- Q values are unqualified in the text -> `q_loaded` (probe transmission through the coupling taper), `measured`.
- Wavelength: the modes' wavelengths are not printed; the control laser is a 1550 nm tunable diode laser (p.6, Supp.
  p.22) -> 1550 nm with `wavelength_inferred`.
- Not entered: acoustic mode frequencies 349.3 / 199.8 / 143.7 MHz, phonon lifetimes 59.2 / 56.2 us, acoustic
  linewidths Gamma_B 16.9 kHz (Fig. 2, Supp. p.26) and opacity linewidth 17.8 kHz (p.7), slow-light delay 110 us at
  1 mW control (p.6, Fig. 2(f)), fast-light advancement 35 us at 380 uW (p.7, Fig. 3(f)), delay-bandwidth products
  1.87 / 0.63 MHz-us and the normalized 3.98e6 W^-1 m^-1 (p.10, Supp. Table 1 p.25): no registry parameter (gaps
  below). Strong-coupling at 40 uW dropped power (Supp. p.26) is a calculation, not a device metric. Non-reciprocity is
  qualitative (Fig. 4, transparency absent for a backward probe, no isolation number): no nonreciprocal row
  (kittlaus2020a / sohn2018 ruling, D419). Supp. Table 1 rows of other works are cited values (rule 3). The tapered
  fiber has no performance metric of its own (not a row).
- Fab / facility: no fabrication statement for the sphere; acknowledgments list funding and discussions only. Fab and
  facility empty. No missing orgs.

## lit:xiong2012 (6 components / 29 metric rows)

| component | class | platform | metrics |
|---|---|---|---|
| cmp_lit_xiong2012_aln_ring_d80_gap300 | resonator.ring | other | Q_L ~1e5 + ER 15 dB + FSR ~4.3 nm (TE, 1550 nm band, p.6 / Fig. 1(d)); n_g 2.01 derived (conflict note); radius 40, gap 300, width 1000, AlN 650 nm, BOX 2 um |
| cmp_lit_xiong2012_aln_ring_d80_gap800 | resonator.ring | other | Q_L 6e5 + linewidth 2.6 pm at 1555.01 nm (Fig. 1(e)); prop loss 0.6 dB/cm author_estimate (best); radius, gap 800, width, AlN 650 nm |
| cmp_lit_xiong2012_aln_ring_d80_vis_near_critical | resonator.ring | other | Q_L 12,000 (766-780 nm rings, band nir_below_o inferred, p.12); radius 40, width 400, AlN 330 nm |
| cmp_lit_xiong2012_aln_ring_d80_vis_weak | resonator.ring | other | Q_L 20,000; prop loss 20 dB/cm author_estimate (p.12); radius, width, AlN 330 nm |
| cmp_lit_xiong2012_gc_1550 | fiber_chip_coupler.grating | other | CE 30 % per coupler typical, 1550 nm (p.6); BOX 2 um, AlN 650 nm |
| cmp_lit_xiong2012_gc_770 | fiber_chip_coupler.grating | other | CE 10 % per coupler typical, 770 nm (p.11) |

- Platform `other` (AlN on thermal SiO2 is not in the enum; pernice2012a / lit AlN precedent), stack in core_material.
- Fab `org_yale_university`: first-person "we fabricate" (abstract p.1, p.5) with all three authors at Yale (Pernice's
  current address KIT not used; same construction as merged pernice2012a). Staff thanked for assistance in device
  fabrication (p.14) name no org: no facility. No missing orgs.
- 0.6 dB/cm: computed by the authors from the undercoupled loaded Q (600,000) taken as Q_int with n_g 2.01 ->
  `author_estimate` (D403), `statistic: best` ("as low as", p.3). The expression reproduces about 0.59 dB/cm.
  20 dB/cm (visible) rests on an unstated group index and the loaded Q -> `author_estimate` (D76).
- Printed conflicts kept with notes (D417): n_g 2.01 vs the 4.3 nm FSR with D = 80 um (gives about 2.2 at 1550 nm);
  gap range 200-600 nm (p.5) vs the 800 nm undercoupled device (p.6).
- Judgment calls: telecom rings split by gap (300 / 800 nm, rule 9 sibling designs); visible rings split by coupling
  state with no gap rows (gaps not printed); visible Q rows get `band: nir_below_o` + inferred (the paper calls
  766-780 nm "visible"; no resonance wavelength printed); waveguide width "typical 1 um" entered as 1000 nm derived
  with "typical" in notes; the 770 nm grating coupler's film (330 nm) is in core_material only, since the paper ties
  the 330 nm film to the visible rings, not explicitly to the couplers.
- Not entered, EO-atlas candidates (rule 2; xiong2012 is not in `eo-modulator-atlas/data/devices.csv`): telecom AlN
  microring modulator (resonance 1542.10 nm, ER 10 dB, Q 80,000, 8 pm shift for -7.5 to +7.5 V, p.9 / Fig. 2(f);
  3-dB EO bandwidth 2.3 GHz, p.11 / Fig. 4(a); electrode capacitance ~10 fF, p.11; 10 fJ/bit estimate, p.13; NRZ up to
  4.5 Gb/s, eye ER 3 dB at 4 Vpp, p.11 / Fig. 3); r51 test ring (~1 pm for +/-7.5 V at 1556.5 nm, p.10); visible
  modulator ring (Q 10,000 near 770.5 nm, response limited by the 12.5 GHz detector, p.12 / Fig. 4(b)). Electrode
  absorption < 1 dB/cm at 0.8 um oxide / 2 um gap is a simulated design value of the EO device (p.9, Fig. 2(c)).
  Material properties (XRD FWHM 1.62 deg, 1.5 nm rms roughness, +/-75 MPa stress, n_o 2.12) are not component metrics.

## lit:lu2021 (2 components / 18 metric rows)

| component | class | platform | metrics |
|---|---|---|---|
| cmp_lit_lu2021_ppln_microring_opo | frequency_converter.other | lnoi_rib | Pth ~0.030 mW (on-chip, 774.1 nm, 125 C, derived); efficiency 11 % at 93.0 uW (derived); Q_L / Q_int for signal 2.9e5 / 3.6e5, idler 2.2e5 / 3.9e5, pump 3.7e5 / 5.9e5 (Fig. 1(d)); poling period 3 um design; width 1800, LN 610 nm, slab 180 nm, sidewall 60 deg, BOX 1.8 um |
| cmp_lit_lu2021_facet_taper | fiber_chip_coupler.edge | lnoi_rib | IL 8.4 dB/facet (IR) and 11.1 dB/facet (near-visible), wavelengths inferred 1550 / 775 nm (p.5); facet width 4000 nm, LN 610 nm |

- Class `frequency_converter.other` for the OPO (mckenna2022 / stokowski2024 precedent; Qs on the converter row).
- Basis: threshold and efficiency are on-chip powers de-embedded with the authors' calibrated facet losses -> `derived`
  (D394; threshold also uW -> mW, D256). Q_int `derived`: the under-coupled regime is confirmed by a gap series of
  fabricated devices (p.2), so D403 allows derived (mckenna2022 precedent).
- Printed conflict kept (D417): BOX 1.8 um (Methods p.5) vs 1.9 um (Fig. 1(b)); the Methods value entered.
- Not entered: coupling Qs Q_s,1 1.5e6, Q_i,1 5.1e5, Q_p,1 1.0e6 (Fig. 1(d); registry gap); OPO tuning 1450-1650 nm at
  125 C for a 5 nm pump change (p.3), "tuning bandwidth of 180 nm (23 THz)" (p.1; inconsistent with the 200 nm span
  of p.3), signal / idler 1529.7 / 1568.4 nm at 120 uW pump (p.2), degenerate operation at 140 C (p.3): no
  frequency_converter parameter (gaps); g/2pi 1.2 MHz (p.2) and ~5.4e4 intracavity photons (p.2): no parameter; eta_max
  0.25 for critical coupling (p.3): theory. Ring radius not printed (only Lambda = 2 pi R / M = 3 um with M = 146,
  implying about 70 um; not entered). Table I (p.5) "this work" row (Q 0.6e6, 0.030 mW) repeats the entered values;
  the other rows are cited work.
- Fab / facility: "The devices are fabricated on a commercial LNOI wafer" (passive, no org; D80b) and authors at Yale
  and USTC -> fab empty; staff thanks for fabrication assistance (p.7) name no org -> no facility. NANOLN (wafer
  supplier, p.5) in notes only (D428). No missing orgs.

## Registry gaps (skipped value + locator, proposed definition)

1. `q_external` for `frequency_converter` (lu2021 Q_s,1 1.5e6 / Q_i,1 5.1e5 / Q_p,1 1.0e6, p.2 Fig. 1(d)): external
   (coupling) quality factor of a converter cavity mode, mode in condition.
2. `tuning_range_nm` and `center_wavelength_nm` for `frequency_converter` (lu2021 OPO 1450-1650 nm at 125 C, p.3; 180 nm
   printed p.1; signal / idler 1529.7 / 1568.4 nm, p.2): OPO output tuning span (control knob in condition) and output
   line wavelength. Same family as the D419 / D575 "OPO span" candidates.
3. Resonator acoustic-mode parameters (kim2015 349.3 / 199.8 / 143.7 MHz, p.6, p.7, p.11 Fig. 5; phonon lifetime 59.2 /
   56.2 us; Gamma_B 16.9 kHz, Supp. p.26; 17.8 kHz, p.7): `acoustic_frequency_mhz` and `acoustic_linewidth_khz` for
   resonator (Brillouin / optomechanical mode frequency and linewidth, mode number in condition). `mech_resonance_khz`
   is restricted to phase_shifter / switch_fabric.
4. `group_delay_us` for resonator / waveguide_platform.slow_light (kim2015 110 us slow light at 1 mW control, p.6 /
   Fig. 2(f); -35 us fast light at 380 uW, p.7 / Fig. 3(f)): optical group delay (sign as printed, control power and
   bandwidth in condition).
