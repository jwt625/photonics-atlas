# Batch lit_53 report (distill subagent, 2026-10-30)

Dry-run result: `batch lit_53: +13 components, +101 metrics; errors 0`. The only warning is the pre-existing one on
cmp_lit_ni2025b_pimmwc-m18. Files are ASCII only, with no e-mail or street text. All five sources are
`restricted_local_only`, so the rows hold facts and locators only.

Source checks: for all five papers, the page-1 title and authors match the source row. None is a correction or a
different paper, and none is flagged `garbled_text_layer`. No supplement is cached (hutchison2016 Supplement 1 is
referenced but absent). Not audited, not merged.

## Per paper (components / metrics)

### acoleyen2009 (4 / 37)

**Rows**
- `opa_16ch_heater` (free_space_emitter.other), 1550 nm, TE:
  - Thermo-optic steering 2.3 deg (phi, 0-3.95 mA).
  - Wavelength steering 14.1 deg over 1500-1600 nm (theta).
  - Emission angles 9.4 / 2.0 / -4.7 deg and FWHM divergences 2.4 / 2.5 / 2.8 deg at 1500 / 1550 / 1600 nm.
  - Geometry: 16 elements, 2 um pitch, 630 nm period, duty 0.5, 50 periods, 800 nm width, 220 nm Si, 70 nm grating
    etch, 2 um BOX, about 1 um BCB.
- `opa_16ch_reference` (free_space_emitter.other, test structure; the array without the heater): measured phi FWHM
  2.7 deg and simulated 2.4 deg.
- `grating_element` (free_space_emitter.other): simulated single-coupler outcoupling efficiency 34 % at 1500 nm,
  25 % at 1600 nm and a 14 % dip near 1565 nm (Fig. 2 inset caption says simulated), plus the grating geometry.
- `ti_heater` (phase_shifter.thermo_optic):
  - P_pi 8.2 mW, author_estimate. It rests on the assumption that about half of the electrode resistance acts on the
    phase shift.
  - Resistance about 15 kOhm, derived (kOhm -> ohm).
  - Total ramp 14.28 pi, derived by the authors from 0.105 pi x (1+...+16).
  - Ti about 100 nm, BCB about 1 um.

**Not entered**
- Main-beam power fraction 42.2 % (theory 44.4 %): no parameter.
- 1/e2 decay after about 35 periods: no parameter (in notes).
- 680 nm Gaussian fit width: a fit parameter.
- Grating-lobe angle 50.8 deg: computed from the design pitch.
- n_eff 2.496 and the Si thermo-optic coefficient: cited values.

**Fab and facility**
- Fab is org_imec on the three SOI rows ("fabricated ... using standard CMOS processes in IMEC").
- The heater row has no fab org: the BCB / Ti post-processing site is not stated.
- The far-field imaging at EPFL is a measurement, not a facility.

### hutchison2016 (3 / 26)

**Rows**
- `opa_uniform` (free_space_emitter.other, the comparison device; the divergence statistics and the wavelength
  steering were measured on it):
  - Theta FWHM 0.142 deg mean, std 0.005.
  - Psi FWHM 0.14 deg mean, std 0.02, best 0.11 (n = 75, 1270 nm).
  - Steering 17 deg in theta over 1260-1360 nm.
  - Steering about 10 deg in psi (grating-lobe limited).
- `opa_nonuniform` (free_space_emitter.other):
  - Steering >= 80 deg in psi (measurement limited by the NA 0.7 objective).
  - SLSR 8.9 dB, the worst of five beams. This is the printed Fig. 5(b) label, entered as measured.
  - Simulated SLSR > 10 dB at 0 deg and > 8.8 dB at 40 deg.
- Shared geometry on both OPA rows: 128 channels, 490 nm period, duty 0.5, 16 nm grating etch (measured by
  profilometry), 400 nm rib width / Si thickness (derived), slab 200 nm (derived: 0.4 - 0.2 um).
- `input_gc` (fiber_chip_coupler.grating): FWHM about 25 nm at about 1.3 um, author_estimate. It is a parenthetical
  setup statement, as in D418.

**Not entered**
- Divergence of the non-uniform OPA: the paper says only "same typical beam width".
- Resolution counts (> 500 spots, > 60,000 points): computed.
- Star coupler and thermo-optic tuners: no metric, so no row.

**Fab and facility:** fab is org_intel ("we have designed and fabricated"; all authors at Intel Labs; 300 mm CMOS
facility).

### sysak2008 (2 / 18)

**Rows**
- `sgdbr` (laser.tunable, platform other; stand-alone, 1.0 um Si waveguide):
  - Threshold 48 mA.
  - Output power <= 1.0 mW, measured with an integrating sphere.
  - Gain-section resistance 14 ohm.
  - SMSR > 30 dB at 1501-1514 nm.
  - Tuning range 13 nm.
  - Geometry: 20 um mesa, 1000 nm Si width, 400 nm Si, 300 nm rib etch, 1 um BOX.
- `sgdbr_eam_laser` (laser.tunable; the laser part of the integrated device, 2.5 um Si waveguide):
  - Output power <= 0.5 mW at 10 C and 170 mA.
  - SMSR > 35 dB over four supermodes at 1512-1554 nm.
  - Threshold < 50 mA, a statement covering both designs (p.2).
  - Same geometry, with a 2500 nm Si width.

**Not entered**
- III-V grating loss / kappa (p.6): the text prints "165 cm-1 and 3dB/100 um, respectively" for loss and kappa, so
  the units contradict the quantities and the assignment is ambiguous (D156 / D159 spirit).
- Maximum CW temperatures 30 / 45 C: no parameter.
- Section lengths and grating-burst geometry: in notes; no reflector metrics.
- Isolation > 10 kOhm between sections.
- QWI photoluminescence (PL) shifts: process data.

**Fab and facility:** fab is empty. The paper says "we have fabricated", but the authors are at Intel and UCSB, two
unrelated orgs.

**EO-atlas candidates (electroabsorption modulator integrated with the SGDBR, skill rule 2; not entered):**
- DC extinction > 5 dB at -6 V, wavelength dependent (p.8, Fig. 12).
- Small-signal 3-dB EO bandwidth > 2 GHz at 6 V reverse bias (p.8, Fig. 13). The conclusion (p.9) says "up to 2 GHz".
- Series resistance 40 ohm (p.8).
- Geometry: 200 um long, 4 um III-V mesa over a 2.5 um Si waveguide.
- Bandgap PL 1470 nm (p.6 Fig. 5).

### matsuo2013 (3 / 11)

**Rows** (all three are LEAP PhC nanocavity lasers, laser.other on platform inp_membrane, with fab org_ntt)
- `leap_laser_a430` (a = 430 nm, the device stated for Fig. 5; Figs. 6-8 attributed to it as part of the same
  section):
  - Threshold 0.0078 mA (printed 7.8 uA, derived).
  - Waveguide-referred output 0.0093 mW at 300 uA and peak wall-plug efficiency (WPE) 5.5 %. Both are
    author_estimate because they rest on a stated 10 dB fiber coupling loss of unstated origin.
  - Emission 3-dB linewidth 0.048 nm at threshold.
  - Pulsed lasing wavelength 1557.85 nm.
  - Membrane about 250 nm.
- `leap_laser_a440` (the high-temperature device): thermal drift 97 pm/K (printed 0.097 nm/K, derived), measured
  over 25-95 C.
- `leap_laser_dynamic`: small-signal bandwidth 16.2 GHz at 200 uA, and forward voltage 1.6 V at 109 uA (the
  12.5 Gb/s bias point).

**Not entered**
- Values with no parameter:
  - Q values (laser Q rejected, D250).
  - Beta / eta_i fits.
  - 16.6 K active-region temperature rise.
  - D-factor 42.4 and MCEF 53.8 GHz/mA^0.5.
  - K-factor 0.20 ns and the derived 44 GHz intrinsic bandwidth. This is a model maximum, kept out to avoid reading
    it as a measured bandwidth.
  - 14.0 fJ/b energy at 12.5 Gb/s NRZ.
  - 95 C maximum temperature.
  - PhC lattice constant and hole diameter.
- Earlier-device values (0.39 mA, 180 fJ/b): the authors' refs. [19] / [20], not entered (rule 3).

**Fab and facility:** fab is org_ntt. The paper says "the device we fabricated", and all authors are in NTT
laboratories of NTT Corporation (D154 parent). org_ntt is the current "NTT, Inc." row; the renamed-entity row
org_nippon_telegraph_and_telephone also exists, and I followed the 21 merged org_ntt uses.

### chen2000 (1 / 9)

**Row:** `vertical_taper_mst` (fiber_chip_coupler.edge, polymer).
- Lowest insertion loss 4.4 dB, device_total. It is a 1 cm waveguide with the taper at the fiber end, a 0.8 NA
  objective at the output, no index matching, measured at 1.3 um.
- Simulated per-coupler losses: 1.6 dB mode mismatch for the test samples, and 1.5 dB BPM minimum for the typical
  design.
- Design fiber MFD 10 um (specification).
- Geometry:
  - Taper lengths 0.5-2 mm.
  - Core 1.8-2.5 um and widths 4-9 um (Fig. 15 labels, converted to nm, derived).
  - SiO2 lower cladding 4 um (Fig. 15 label).
  - New cladding 0.2 mm (derived).

**Not entered**
- Headline result: coupling-loss reduction per tapered end (Table 1, 1.4-2.2 dB by width and polarization; Fig. 19
  1.8 dB). There is no parameter for an improvement relative to an untapered facet; the theurer2020 precedent applies.
- 1.4 dB/cm propagation: from "previous cutback measurement".
- 0.5 dB reflection term.
- Fig. 11 scattering losses 0.93 / 0.05 dB/cm: structure and method not stated.
- Tolerances 0.008 / 0.4 um and fiber offset 2.3 um: simulated design sensitivities with no parameter.
- Final core thickness 1.2 +/- 0.2 um at the taper end: no role-specific parameter; in core_material.
- Inverted-ridge height 0.1-0.5 um: role ambiguous (trench in the lower cladding vs core etch).

**Fab and facility:** fab is empty. There is no explicit fabrication statement; all authors are at USC.

## Judgment calls

1. **matsuo2013 dynamic row.** Sec. IV-B does not say whether the a = 430 or a = 440 nm device was measured. I made
   a third row for the dynamic values instead of attaching them to either device (D159 analogue). The alternative is
   D159 strict: no row, with the values in notes.
2. **chen2000 class.** I used fiber_chip_coupler.edge; the registry lists "polymer SSC" under edge. I did not use
   micro_optics.vertical_taper, because the merged rows of that subtype are out-of-plane mirrors and tapers to PDs.
   The batch class list suggests vertical_taper was the expected class.
3. **acoleyen2009 Fig. 2 wavelength steering.** The text does not say which array was measured. The values are on
   the heated OPA row because the abstract reports the 14.1 deg for the OPA. The theta behaviour is a property of the
   identical gratings of both arrays.
4. **acoleyen2009 single-element efficiency.** It is a separate fabricated row with only simulated values,
   following the zhang2025b arrowhead precedent and D80e.
5. **hutchison2016 platform `soi`.** The text says Si rib waveguides 0.4 um thick in a 300 mm CMOS facility, but
   does not name SOI or a BOX. The alternative is an empty platform.
6. **hutchison2016 80 deg as `ge`.** The paper says the range is measurement limited.
7. **hutchison2016 8.9 dB SLSR as `measured`.** It is a printed label value, not a curve reading.
8. **sysak2008 threshold < 50 mA.** It is entered on the integrated-laser row only. The stand-alone row has its own
   48 mA.
9. **Temperatures.** Temperatures printed in C are stored as temperature_k (C + 273.15).

## Missing organizations

None needed for fab_org_ids or facility_org_ids. org_imec, org_intel and org_ntt are in the registry. Author orgs
with no component role (Ghent University, EPFL, UCSB, USC) were not checked further.

## Registry gaps (proposed; values skipped)

| proposed parameter | class | skipped values (locator) | definition |
|---|---|---|---|
| max_operating_temp_c (or _k) | laser | sysak2008 30 C (p.7), 45 C (p.8); matsuo2013 95 C heat sink (p.6) | highest heat-sink / stage temperature with CW lasing as stated |
| energy_per_bit_fj | laser | matsuo2013 14.0 fJ/b at 12.5 Gb/s NRZ, 1.6 V / 109 uA (p.8-9) | electrical energy per bit of a directly modulated laser (V x I / bit rate) |
| mcef_ghz_per_sqrt_ma, d_factor_ghz_per_sqrt_ma | laser | matsuo2013 53.8 and 42.4 GHz/mA^0.5 (p.8) | modulation current efficiency factor / D-factor from f3dB and fr vs sqrt(I - Ith) |
| coupling_loss_reduction_db | fiber_chip_coupler | chen2000 Table 1 (p.9), 8 values with std, n 8-9 | coupling-loss improvement vs an untapered reference facet, positive dB |
| main_lobe_power_fraction_pct | free_space_emitter | acoleyen2009 42.2 % measured, 44.4 % theory (p.3) | fraction of radiated power in the main beam |
| phc_lattice_constant_nm, hole_diameter_nm | laser (PhC) | matsuo2013 a = 430 / 440 nm (p.4, p.6), holes 220 nm (p.4) | repeats the lit_47 PhC lattice gap |

## Top open questions

1. matsuo2013: keep the third (dynamic) row, or apply D159 strictly and move 16.2 GHz / 1.6 V to notes?
2. chen2000: is the class fiber_chip_coupler.edge (as entered) or micro_optics.vertical_taper?
3. hutchison2016: keep platform `soi` with the note, or leave it empty because SOI is not named?
