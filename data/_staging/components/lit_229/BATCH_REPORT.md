# lit_229 batch report

Papers: lit:xu2019c, lit:hoessbacher2014, lit:gao2011. Page-1 titles match the source rows. verified_on 2026-11-20.
Dry run of `merge_component_staging.py`: +10 components, +71 metrics, 0 errors; the one warning names the merged row
cmp_lit_ni2025b_pimmwc, not in this batch.

| paper | components | metric rows |
|---|---|---|
| xu2019c | 3 | 15 |
| hoessbacher2014 | 5 | 27 |
| gao2011 | 2 | 29 |

## xu2019c (GeSn/Ge MQW p-i-n photodiode on 300 mm Si, 2 um band, Optics Express 2019)

Rows (all `photodetector.vertical`, platform `other` as the merged Ge-on-Si vertical PDs kang2008 / duan2012):
- `gesn_mqw_pd_d20` (dark-current and RF device): dark current 170 nA at -1 V (printed 0.17 uA, derived); J_dark about
  54 mA/cm2 (Fig. 9(a) read); 3-dB bandwidth > 10 GHz at -7 V and 2000 nm (modulator-limited lower bound), about
  0.8 GHz at 0 V and 1.9 GHz at -3 V (Fig. 14 reads); diameter 20 um, GeSn absorber 150 nm (6 x 25 nm wells).
- `gesn_mqw_pd_d40` (photoresponse device): responsivity 0.214 / 0.047 / 0.029 / 0.015 A/W at 1550 / 1742 / 1877 /
  2000 nm, -1 V, fiber-referred surface illumination; diameter 40 um, absorber 150 nm.
- `gesn_mqw_pd_series` (D165 array row, D = 20-100 um): headline leakage density 44 mA/cm2 at -1 V (diameter not
  named) and J_bulk 42 mA/cm2 from the J_dark vs 1/D fit (n = 6).

Not entered:
- J_surf 5.7 uA/cm (p.9; no per-perimeter leakage parameter).
- Fig. 14 -5 V trace: approaches -3 dB near 7-10 GHz without a clear crossing (caption: > 10 GHz only for reverse
  bias larger than 5 V).
- Rectifying on/off ratio 1e4-1e5 (p.9), AFM roughness 0.636 nm (p.7), threading dislocation density ~1e7 cm-2 (p.3),
  predicted cut-off about 2.05 um (p.2, calculation): no parameter. Fig. 10 benchmark values are other works.
- Critical-thickness and band-structure calculations (Figs. 2-3): material modelling, no component value.

Fab / facility: fab empty (growth and processing passive, authors at NUS, Applied Materials, NTU; D80b). The
acknowledgment thanks one staff member at Si-COE, NTU, for RF-measurement help: staff thanks, no facility (D72).

Judgment calls:
1. Fig. 12 responsivities on the 40 um row: Fig. 12 and its sentence do not restate the diameter; they follow the
   Fig. 11 measurement (D = 40 um) in the same section with the same four laser wavelengths (sun2018 precedent, note on
   the row). Alternative: D159, values to notes.
2. 44 mA/cm2 on the series row (no diameter named; Fig. 9(a) minimum about 44.6 mA/cm2 at D = 100 um) rather than on
   a 100 um row (no such row: no other value is tied to D = 100 um).

## hoessbacher2014 (plasmonic memristor latching optical switch, Optica 2014)

Rows (memristor rows `phase_shifter.other`, platform `other`):
- `memristor_l5`: ON/OFF extinction 6 dB and latching extinction 3.5 dB (quasi-static, 1550 nm, TM); latching 3 dB
  after a 5 min, 2 V step (Fig. 5); 50 cycles (`endurance_cycles`); 3-dB modulation bandwidth 30 MHz as `bw3db_khz`
  30000 (derived); peak operating power < 200 nW as `tuning_power_mw` < 0.0002 (author_estimate: bound from the
  2 V operation and the 100 nA compliance, no current measured); length 5 um, Si strip 800 x 340 nm, BOX 2 um.
- `memristor_l10`: extinction 12 dB at 1550 nm; geometry.
- `memristor_l20`: latching extinction about 0.6 dB after a 5 ms, 2 V impulse; geometry.
- `hybrid_wg` (`waveguide_platform.straight`, D396 cross-row): propagation loss 1 dB/um by cutback -> 10000 dB/cm
  (derived), simulated 0.2 dB/um -> 2000 dB/cm (simulated, D83f); Si strip geometry.
- `si_hybrid_interface` (`mode_converter.converter`, platform `soi`, D76 / salamin2018 precedent): 6.5 dB per
  interface by cutback (measured, per_component), 1.2 dB simulated.

Not entered:
- Set threshold about 2.9 V (Fig. 3), switching energy 60 uJ / 1 nJ (p.4), operating voltage about 2 V: no
  parameter (registry gaps below).
- Simulated 39 % field fraction in the SiO2 layer (p.2), ITO carrier density 1e19 cm-3 (nominal, in core_material).
- PECVD-SiO2 comparison sample: "much lower extinction", no number (p.3).
- Theoretical ITO-index extinction ~1 dB (cited to ref. [9], rule 3); VO2 and a-Si switches in the introduction
  (other works).
- TM grating couplers: no values.

Fab / facility: fab empty (passive fabrication sentences, authors at ETH Zurich and KIT; D80b). Facility
org_binnig_and_rohrer_nanotechnology_center + org_first_center_for_micro_and_nanoscience ("partly carried out in",
p.5 acknowledgments; flory2020 / salamin2018 precedent) on all 5 rows.

Judgment calls:
3. Class `phase_shifter.other` for an amplitude-only latching switch (memristor / VOA precedents tossoun2024,
   feng2011, morichetti2021; D155). Alternative `switch_fabric.other` (D158 / D407 name 1x2 / 2x2 elements and ring
   switch elements; this one has one input and one output).
4. Peak power "below 200 nW" entered as `tuning_power_mw` lt 0.0002 author_estimate (the liu2020a leakage-power item on
   the owner list is the same question).
5. Platform `other` for the hybrid Si / ITO / SiO2 / Au section (huang2013 hybrid plasmonic precedent); not
   `plasmonic_mim` because the light runs in a Si strip with a conductor-insulator-metal cap.
6. Wavelength 1550 nm inferred (`wavelength_inferred`) for the dynamic tests and the cutback values: the setup laser
   (p.2) is the only stated wavelength.

## gao2011 (top-illuminated p-i-n InGaAs PDs grown on Si by MOCVD, IEEE PTL 2012)

Rows (`photodetector.vertical`, platform `iii_v_on_si_epi`):
- `ingaas_pin_d20`: dark current 200 nA at -1 V (derived from 0.2 uA), 64 mA/cm2 (authors' arithmetic, derived),
  about 9 uA at -5 V (Fig. 4 read); responsivity about 0.5 A/W at 0 V, about 0.57 A/W at -5 V, 0.5 A/W at -1 V
  (abstract), fiber-referred, 1550 nm; external QE 40 % (derived); bandwidth 10 GHz optical and 6.3 GHz electrical at
  -5 V, about 5 GHz at -1 V, Fig. 5 inset reads about 8 / 10 GHz at -2 / -3 V; calculated electrical 8.6 GHz
  (simulated); junction capacitance 40 fF (author_estimate); diameter 20 um, absorber 850 nm.
- `ingaas_pin_d60`: dark current about 12 uA at -1 V and 140 uA at -5 V (Fig. 4 reads); responsivity 0.5 / 0.57 A/W
  and QE 40 % (stated for both devices); bandwidth 5 GHz optical / 3.2 GHz electrical at -5 V, > 2 GHz at -1 V, inset
  reads about 3.8 / 4.7 GHz at -2 / -3 V; calculated electrical 4.1 GHz (simulated); diameter 60 um, absorber 850 nm.

Not entered:
- First process batch (thinner PBO, larger pads): about 2 GHz for all sizes, estimated 1.8 pF parasitic: a different
  design stated as a family value (D254), in notes.
- Second-batch parasitic capacitance 0.2 pF (estimate) and 0.21 pF (S22 fit): device of the fit not named (D159),
  in notes.
- Internal QE 57 %: computed from an absorption coefficient cited to ref. [9] (rule 3; duan2012 precedent).
- Responsivity flat over 1510-1580 nm (no value or device), 10 Gb/s eye diagrams, RMS roughness 3.5 nm, dark-current
  ratio about 20 at -5 V: no parameter or no new value. 0 V inset point of the 20 um device (near the axis, not read).
- 30 and 40 um siblings: fabricated, no values.

Fab / facility: fab org_the_hong_kong_university_of_science_and_technology ("We have fabricated two batches of
devices", growth in "our system"; all authors HKUST ECE; D72 / D399). No facility named.

Judgment calls:
7. Subtype `vertical` rather than `iii_v_on_platform` (top-illuminated on a bare Si substrate, not coupled to a PIC;
   chen2018a precedent), platform `iii_v_on_si_epi` (epitaxial III-V on Si; iadanza2024 uses it).
8. Optical and electrical 3-dB bandwidths both entered as `bw3db_ghz` with the type in condition (yin2007 precedent).
9. Calculated electrical bandwidths (8.6 / 4.1 GHz) `simulated` (model with an estimated Cp; yin2007 m17 precedent).

## Missing orgs

None for fab / facility. (Si-COE, NTU appears only in a staff-thanks sentence, not entered.)

## Registry gaps

- `switching_energy_nj` (phase_shifter, switch_fabric): energy per state transition as stated (hoessbacher2014 p.4:
  60 uJ for 5 min, 1 nJ for 5 ms; also listed in D417).
- `set_voltage_v` (phase_shifter): resistive-switching set / threshold voltage (hoessbacher2014 Fig. 3, about 2.9 V).
- `surface_leakage_density_ua_per_cm` (photodetector): perimeter leakage density from a J_dark vs 1/D fit (xu2019c
  p.9, 5.7 uA/cm).
- `rms_roughness_nm` (already a registry candidate, D432): xu2019c 0.636 nm, gao2011 3.5 nm (epi surface).
