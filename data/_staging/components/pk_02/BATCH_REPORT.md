# Batch report pk_02 (packaging-atlas on-chip components, 2026-10-20)

Transcribed (condensed) by the coordinator from the batch agent's report. Dry run 0 errors: 25 components, 59 metrics.
Source pk:<paper_id>; host empty; PK text.md page locators plus section / figure / table; each component note lists the
PK metrics ids it covers. No duplicate of a pk_oi physical design.

## Per paper (components / metrics)

- ectc51687.2025.00014 Sumitomo (1/1): MZI switch PIC (switch_fabric.mzi_mesh) crosstalk ~40 dB across the full
  module (p.4 Sec. IV.D; p.5 Fig. 9), band unspecified; fab empty ("commercial MPW", foundry not named).
- ectc51846.2026.00176 Lightmatter (1/6): external CW DWDM O-band laser (laser.els_module): 8 wavelengths per fiber at
  200 GHz, 25 mW per wavelength, linewidth < 5e5 Hz (derived from < 0.5 MHz), RIN <= -150 dB/Hz, SMSR >= 40 dB;
  author_estimate (origin not stated; vendor not named, possibly a supplier specification).
- ectc51909.2023.00108 TSMC iOIS (3/3, author_estimate "can reach", band unspecified, platform other): CI straight
  waveguide 0.21 dB/cm, 90-degree bend 0.009 dB, transition between adjacent CI layers 0.015 dB per_component.
- ectc51909.2023.00009 CEA-Leti (4/19, fab org_cea_leti): rib 0.32 dB/cm and deep-rib 0.81 dB/cm mean (cutback on
  spirals, 1310 nm inferred, Table I p.6); butt-coupled Ge PD > 0.8 A/W at -1 V, Fig. 21 0.68 A/W at 0 V and 0.98 A/W
  at -5 V, dark ~40 nA at -1 V and ~16 uA at -4 V (Fig. 20), Ge 1 x 15 um; PIN microring filter extinction 18 dB at
  1 V forward (drop loss ~3 dB), up to 27 dB at 2 V, ~20 dB at 1.5 V (conclusion).
- ectc51909.2023.00230 IZM on CEA-Leti PDK (4/7, fab org_cea_leti, wafer-prober medians): strip 0.7 dB/cm (C), rib
  0.1 (C) / 0.2 (O) dB/cm, deep-rib 0.5 dB/cm (O); Ge PD 0.9 A/W at -1 V (O band inferred from the sentence).
- ectc51909.2023.00048 AIM (4/12, fab org_aim_photonics, named AIM MPW process): SiN low-loss < 0.3 dB/cm (C+L) and
  < 0.5 dB/cm (O); Si low-loss < 2 dB/cm (O); Si standard > 4 dB/cm (O); O-band PD > 30 GHz (bias not stated), Fig. 6(d)
  ~3 GHz at 0 V and ~13 GHz at -1 V, responsivity at -1 V 0.85 / 0.81 / 0.69 A/W at 1260 / 1310 / 1360 nm. The
  text.md is in a shifted font: values decoded and checked against the page renders.
- ectc51529.2024.00023 Corning (1/1): IOX waveguide 0.034 dB/cm at 1310 nm, cutback over 4 lengths.
- ectc51846.2026.00106 Corning (3/5): straight IOX 0.041 dB/cm mean (n = 14), 0.0397 best, cutback 1310 nm;
  enhanced-delta-n bend 0.01 dB/cm at R = 10 mm (abstract) / ~0.01 at R > 6 mm (conclusion), author_estimate;
  uniform-delta-n bend 4 dB/cm at R = 10 mm, author_estimate.
- ectc51909.2023.00324 AIST (1/3): polymer waveguide 0.4 dB/cm cutback (Fig. 5, O band inferred); core 8.6 x 8.2 um
  measured from the micrograph.
- ectc51846.2026.00110 DNP (3/6, fab org_dai_nippon_printing: "we successfully fabricated", all authors DNP), 1310 nm:
  polymer arrays (fiber_interface.fan_out) delta 2.3 % at 10 um pitch crosstalk 32.3 dB (printed -32.3); delta 1.3 %
  at 20 um and 0.4 % at 30 um > 30 dB.

## Not entered

EO values (00009 PN ring modulator, 00048 / 00230 MZMs, 00019 EML); 00048 DFB LIV (figure only, laser cited [13]);
00106 Fig. 6 bend readings (fiber-to-fiber totals, mapping not stated); 00110 BPM simulations and index values;
00023 bulk absorption (material) and cited 0.043 / 0.048 dB/cm; 00134 "< 0.1 dB/cm" (general claim next to a citation),
Fig. 10(b) arbitrary units; 00144 PD bandwidth (simulation on cited parameters); 00052 PWG crosstalk (simulated,
reduced pitch); 00284 "< 0.1 dB" cited [5]. Values for existing pk_oi rows (coordinator): 00048 dfb_trench_edge
"< 1.6 dB" (p.6 Sec. IV); 00014 vcbel_pair excess < 0.1 dB at +/-3 um (p.4 Sec. IV.C), Fresnel 2 x 0.2 dB (p.5
Sec. V.A), simulated 14 dB in air vs 0.3 dB with resin at 2 um roughness (p.4 Sec. IV.B).

## Judgment calls

Lightmatter laser author_estimate (not specification: vendor and purchase not stated); AIM SiN text values attributed
to the first nitride layer (Fig. 6(a), noted); 00230 PD band from sentence position; DNP arrays as
fiber_interface.fan_out (fan-in from fiber pitch; crosstalk_db not allowed for waveguide_platform); fab empty for
00106 / 00023 / 00324 under D80b (passive "fabricated"; note: pk_oi 00106 rows carry org_corning, to reconcile);
TSMC CI values author_estimate, band unspecified.

## Registry gaps

crosstalk_db for waveguide_platform (dense waveguide arrays); il_nonuniformity_db for waveguide_platform; excess loss at
a stated misalignment. No missing orgs.
