# lit_108 batch report (2026-11-08)

All three cached texts match their source rows (page-1 title). None is a correction, an erratum or another paper. No
garbled text layer is flagged. salamin2018 is the ACS "Just Accepted" manuscript (pre-copyedit), the paper itself;
its Supporting Information (S1-S4) is not cached. Figure values were read from the cached `page_NN.png` renders.
Dry-run: +18 components, +74 metrics, 0 errors (the one warning, ni2025b m18 / m4, is on an existing merged row).

| paper | components | metrics |
|---|---|---|
| yang2026a | 9 (switch_fabric.other 2; phase_shifter.thermo_optic 2; mode_converter.mdm_mux 3; mode_converter.converter 1; mode_converter.other 1) | 36 |
| salamin2018 | 5 (photodetector.other 3; fiber_chip_coupler.grating 1; mode_converter.converter 1) | 19 |
| shen2016 | 4 (photodetector.iii_v_on_platform 3; waveguide_platform.other 1) | 19 |

## Not entered, and why

yang2026a
- Table 1 rise / fall time ~15-25 us for "This Work": footnote c says it is estimated from the typical response of
  standard SOI thermo-optic waveguides, not measured on this device. Noted on the switch row.
- Table 1 rows of other works (rule 3).
- Waveguide crossing inside the bi-MUX and the grating couplers: no stated value.
- Heater material / geometry and arm length: not printed (only the 42 x 230 um2 single-arm footprint, entered).

salamin2018
- NEP 1-5 pW/Hz^0.5 (p.12): no registry parameter, device not named.
- Capacitance "a few fF" (p.5): no number (S1 not cached).
- 72 Gbit/s OOK eye, BER 1.6e-2 at 1316 nm, 8.5 V (p.15, p.17): taken on a fourth device (20 um, 200 nm slot) that has
  no other value; no data-rate parameter, so no row (skill rule 9). In the notes of the 10 um row.
- Design study: maximum QE 75 %, plasmonic loss share 25-70 %, 14 % plasmonic / 50 % recombination split of the lost
  photons (p.7-8, p.11): simulation of the concept, no specific device.
- RC limit "can reach THz" (p.5): qualitative estimate.
- a-Ge resistivity about 500 ohm cm (p.10): material property.
- Fiber-to-plasmonic-detector total about 21 dB (p.12-13): the sum of the two entered terms.
- 1.6 dB grating coupler (ref. 43) and the 0.12 A/W hot-carrier detector (ref. 26): cited (rule 3).

shen2016
- 40 / 54 Gb/s open eyes at -4 V (p.11): no parameter.
- Transit-limited 123 / 85 GHz and RC-limited about 145 GHz (p.4): model estimates with assumed drift velocities
  and 100 ohm; no parameter for partial bandwidth limits.
- n-contact loss coefficients 0.93 / 2.91 dB/um and GeAg 0.56 dB/um (ref. 23), 2.5 um optimal p-contact spacing
  (ref. 21): the authors' earlier work (rule 3, D259).
- "Typical" 6 dB fiber-to-PD coupling loss used to set the LCA power (p.9): assumed, not measured; no grating
  coupler value printed, so no coupler row.
- Over 97 % of the waveguide mode coupled into the PD modes at the butt joint (simulated, p.4): the joint is part
  of the PD, not a separate component, so no transition row.
- Responsivity vs length (Fig. 3(b)) and Cj vs area (Fig. 6(d)) point clouds: plotted only.

## Missing fab / facility orgs

None. Ids used, all in the registry: org_applied_nanotools (yang2026a fab, p.5 Sec. 3), org_eth_zurich (salamin2018
fab, p.21 author contributions), org_binnig_and_rohrer_nanotechnology_center and
org_first_center_for_micro_and_nanoscience (salamin2018 facilities, p.20), org_nanolab_tu_e (shen2016 facility,
p.12).

Alias candidates (not new ids): "Binning and Rohrer Nanotechnology Center (BRNC)" (salamin2018 p.20, misspelling
of the registered name) and "Nanolab@TU/e" (shen2016 p.12, case variant of the registered alias) for
`org_aliases.csv`.

## Judgment calls

1. yang2026a switch / phase-shifter split: the 2x2 MCE switch and the reference switch are `switch_fabric.other`
   (D158) with IL, crosstalk and extinction; P_pi goes on separate `phase_shifter.thermo_optic` rows for the
   mode-cycling arm and the reference arm (D396, chang2026a precedent). The 42 x 230 um2 Table 1 footprint is the
   single phase-shift arm (footnote b), so it is on the phase-shifter row.
2. yang2026a P_pi 11.9 / 26.8 mW `measured` (cos^2 fit of own data, D80a), qualifier approx; the extinction 32.7 dB
   is approx (p.8 "about"; abstract "over", Table 1 ">"). Measurement wavelength not stated: `c_band` with
   `wavelength_inferred` (C-band ASE source, p.5).
3. yang2026a switch / bi-MUX / ADC / loop measured IL `scope: unspecified`, `method: unspecified`: the text never
   says how the spectra were normalized. Fig. 3(c) labels an "ADC for calibration" structure, which suggests a
   reference normalization for the bi-MUX, but the procedure is not described (noted; an auditor may upgrade to
   per_component / reference_structure). Spectral windows are read from the figure axes (`wavelength_inferred`).
4. yang2026a uni-MUX and mode exchanger have simulated values only; they exist on the chip inside the bi-MUX / loop,
   so `row_kind: fabricated` (D80e). The bi-MUX is a separate row (its own measured values). The ADCs used to excite
   TE1 are a `mode_converter.mdm_mux` test-structure row (measured IL / crosstalk). The passive mode-cycling loop is
   `mode_converter.other`, test structure.
5. salamin2018 class / platform: the a-Ge plasmonic MSM detectors are `photodetector.other`, platform `plasmonic_mim`
   (ding2019 precedent). `ge_waveguide` was not used: amorphous Ge photoconductor in a metal slot, not a crystalline
   Ge-on-Si waveguide PD. The Si-to-plasmonic coupler is `mode_converter.converter` (D76, kohli2023 precedent),
   platform `soi` (the photonic side, as in kohli2023 which used the host stack); `plasmonic_mim` is the alternative.
6. salamin2018 IQE rows `author_estimate` with `ref_plane: on_chip`: the absorbed power rests on reference
   structures plus a 3D EM simulation (p.11). The 36 % row carries `qualifier: le` ("up to") with the 10 V bias read
   from Fig. 3(b); the Fig. 3(c) IQE labels (15.7 / 10.7 / 4.4 % at 7 / 6 / 4 V) are printed figure labels. The
   Fig. 3(d) spectrum is assigned to the 3 um device from the Methods sentence on the static plots (text names only
   the 160 nm slot).
7. salamin2018 13.8 dB photonic-plasmonic loss `author_estimate` ("origin not stated"); 7.1 dB GC `measured`
   per_coupler ("tested to be"). The 90 % Si-to-plasmonic coupling is `simulated` (refers to S3, which includes the
   3D EM simulation; S3 not cached); `author_estimate` is the alternative.
8. salamin2018 fab: author contributions name two authors who fabricated the devices; all authors at ETH Zurich IEF,
   so `org_eth_zurich` (D154, flory2020 precedent; `org_eth_ief` exists as a lab id).
9. shen2016 fab empty: passive fabrication wording and authors at two institutions (TU/e and Ghent University-IMEC).
   No process / MPW name printed (IMOS is the platform name), so `process_name` empty.
10. shen2016 QE 56 % `derived` (authors' conversion from 0.7 A/W). Capacitance 14.2 fF `measured` (S22 fit, D80a);
    the 11 fF parallel-plate estimate `author_estimate`. Saturation photocurrent 3 mA approx with the linearity /
    thermal-failure definition in condition. "As low as 5 fF" for 3 x 5 um2 PDs is a separate design row
    (statistic best). "Most 3 um wide PDs" Rs < 50 ohm is a population row (D165, statistic typical).
11. shen2016 n-contact loss 1.16 dB/um measured on testing waveguides of this chip: `waveguide_platform.other` row,
    `prop_loss_db_per_cm` 11600 `derived` (unit conversion), C-band inferred. The method comes from the authors'
    earlier work but the value is this paper's measurement, so it is entered.
12. shen2016 lower cladding "SiO2 + BCB about 2.4 um" entered as `box_thickness_um` 2.4 approx (definition "buried
    oxide / lower cladding thickness").

## Registry gaps

- Data-rate / eye-diagram result for photodetectors: salamin2018 72 Gbit/s OOK (p.15, Fig. 4(b)), shen2016 54 Gb/s
  (p.11, Fig. 7). Proposed `data_rate_gbps` (unit Gbit/s, photodetector, condition: modulation format, BER or
  "open eye", bias).
- Noise-equivalent power: salamin2018 1-5 pW/Hz^0.5 (p.12). Proposed `nep_pw_per_rthz` (unit pW/Hz^0.5,
  photodetector, bias in bias_v).
- Plasmonic / MSM slot width: entered as `absorber_width_um` (the slot is filled with the a-Ge absorber); a
  `slot_width_nm` geometry parameter for photodetector would avoid the role ambiguity.
