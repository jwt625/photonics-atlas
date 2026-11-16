# lit_143 batch report

Distilled 2026-11-15 under the pic-component-distill skill (Contracts v4-v7). Validation:
`merge_component_staging.py data/_staging/components/lit_143 --dry-run` -> +29 components, +141 metrics, 0 errors.
All four cached texts match their source rows (page-1 titles checked). No correction / erratum, no garbled-text flag.

| paper | components | metric rows |
|---|---|---|
| lit:chatterjee2019 | 5 | 25 |
| lit:zhong2021 | 4 | 22 |
| lit:martinez2016 | 9 | 21 |
| lit:lin2022a | 11 | 73 |
| total | 29 | 141 |

## lit:chatterjee2019 (Si PIN PD on SiN-SOI, 850 nm; arXiv v1 text)

Components: SiN grating coupler (`fiber_chip_coupler.grating`, sin), SiN-Si inverse-taper vertical coupler
(`waveguide_platform.transition`, si_sin_multilayer), Si PIN PD device D3 at 115 um and at 105 um
(`photodetector.other`), 200 nm-intrinsic PIN design (row_kind design, simulated 25 GHz).

Not entered and why:
- Figure values of Figs. 3(b), 6, 7, 9-12: the render's figure fonts are garbled (axis labels unreadable); no reads.
- Fig. 2(a) "10 um" label: meaning (grating width vs length) not unambiguous (D156).
- Calculated pin capacitance about 0.76 fF and series + pad resistance about 416 ohm: stated once for the pin of all
  devices, no device named (D254); in PD notes.
- Table 1 "This work, Integrated: No" responsivity 0.2 A/W: device length and illumination path not stated (D159).
- Photocurrents 5.09 uA (10 V) and 7.5 uA (25 V): operating points, no parameter; in notes.
- Table 1 values of other works (refs. 7, 11, 12, 14): rule 3.

Judgment calls:
- 46 nA "as low as" at 10 V assigned to D3 (115 um): the sentence ends "for device D3"; statistic best, note kept.
- Bandwidths 14 / 15.5 GHz `derived` (authors' f3dB = 0.45 / FWHM on their own pulse FWHM; wang2026g precedent).
- GC 12.6 dB "dB/coupler": scope per_coupler, method unspecified (single vs pair test not stated).
- Responsivity wavelength not stated: band nir_below_o, `wavelength_inferred` (850 nm band device).
- One transition row for the D1-D3 taper variants (only the simulated 72 % of the optimized 15 um taper is stated).
- PD platform `si_sin_multilayer` (govdeli2025 precedent: Si junction fed by a SiN waveguide).
- Fab empty: passive "were fabricated", all authors at IISc, no facility acknowledged (D80b).

Missing orgs: none (no fab / facility statement).

## lit:zhong2021 (doped-Si heater TO modulators at 2 um)

Components: doped-Si heater in an unbalanced MZI (`phase_shifter.thermo_optic`), doped-Si heater in the R = 40 um ring
(`phase_shifter.thermo_optic`), the ring itself (`resonator.ring`, D396 cross-noted), doped rib waveguide loss
(`waveguide_platform.straight`). Platform `soi_rib` (220 nm SOI, 150 nm ridge height).

Fab / facility: fab `org_institute_of_microelectronics_chinese_academy_of_sciences` ("MPW runs involved at" IMECAS,
p.3); facility `org_zju_micro_nano_fabrication_center`, `org_westlake_center_for_micro_nano_fabrication`
(fabrication support acknowledged, p.8). process_name "IMECAS multi-project-wafer (MPW) runs, 220 nm SOI, DUV
lithography" (built from the printed wording; the coordinator may shorten it).

Not entered and why:
- MZI FSR about 8.5 nm: fsr_nm not allowed on phase_shifter (in notes; it is the MZI's FSR, not a component one).
- FOM values (mW-1 us-1): no parameter. Simulated 57.53 K per pi (p.3): no parameter.
- Table 1 rows of other works: rule 3.

Judgment calls:
- Ring "P_pi" 3.33 mW (P = FWHM x pi / eta) entered as `tuning_power_mw` derived (chang2026a precedent); printed
  inputs give 3.46 mW (conflict noted, D417).
- MZI on-off ratio 17 dB entered with the printed 2005 nm, which lies outside the plotted 2018-2033 nm span (noted).
- MZI insertion loss 1.13 dB on the phase-shifter row, scope de_embedded, includes the two MMIs (no separate MZI row).
- 19.5 dB/cm doped-waveguide loss `author_estimate` (ring extraction, inputs not stated; D76).
- Ring Q 1.8e4 unqualified -> `q_loaded`; ring notch depth about 9 dB read off Fig. 5(b).

Missing orgs: none (all three in the registry).

## lit:martinez2016 (Ge-on-Si waveguide-coupled SACM APDs, Sandia)

Components: 8 APD designs (`photodetector.apd`, soi): no-overlap t = 0 with Wmulti 1.0 / 0.5 / 0.4 / 0.3 um, overlap
t = 100 nm with Wmulti 0.9 / 0.4 / 0.3 / 0.2 um (breakdown voltage per caption on each); reference Ge p-i-n
(`photodetector.ge_waveguide`). Gain, bandwidth, GBP, responsivity and dark current only for the 1.0 um and 0.5 um
no-overlap devices (as printed); excess noise factor at M = 10 / 20 / 40 on the 1.0 um row (second identical device,
noted).

Fab: `org_sandia_national_laboratories` (D84a: "within our Si photonics process", "our selective epitaxial Ge on Si
growth process", "at our CMOS facility", device "manufacture"; all authors at Sandia). No named process -> process_name
empty.

Not entered and why:
- "12.6 to 6.2 GHz for 0.3 to 1.0 micron" (p.9): the 0.3 um device (overlap or not) is not identified (D159).
- "saturate around 12 GHz for all variations" (p.9): no device; note-level.
- Figure reads of Figs. 2(b)-(c), 3(b)-(c), 5(b)-(c) (per-device responsivity / gain curves): not needed for the stated
  values; not read.
- BER sensitivities (BER < 1e-12 from -18.3 dBm (1.0 um) and -17.2 dBm (0.5 um), 10 Gbps, 1550 nm) and NEP
  0.21 / 0.38 / 0.72 pW/sqrt(Hz): no parameter (NEP kept in the excess-noise condition).

Judgment calls:
- Gain values `derived` (Eq. (2) ratio of own measurements, unity gain from the measured p-i-n; anthony2019 precedent);
  GBP `derived`; 54.5 A/W `derived` (authors' arithmetic); dark current 2.7e-5 A -> 27000 nA `derived`.
- Breakdown voltages entered positive as printed (criterion 0.2 mA compliance in condition).
- Reference p-i-n row (0.8 A/W, QE 0.66): value sentences carry no citation and call the values measured (D80i), but
  the p-i-n design is the authors' earlier ref. 6; flagged for the audit. Wavelength 1510 nm inferred (APD tests at
  1510 nm; 0.8 A/W with QE 0.66 corresponds to about 1.5 um).

Missing orgs: none.

## lit:lin2022a (SiN-on-Si waveguide PDs, visible, AMF; arXiv v2 with Supplementary Information)

Components: PIN PDs l = 50 / 100 / 200 / 500 um (`photodetector.other`), PN PDs l = 50 / 100 / 200 / 500 um
(`photodetector.apd`, govdeli2025 precedent), SiN tapered edge coupler (`fiber_chip_coupler.edge`), SiN routing
waveguide (`waveguide_platform.straight`), thermally tuned SiN racetrack ring with PD tap (`resonator.ring`). PD platform
`si_sin_multilayer`; passive SiN parts `sin`.

Fab: `org_amf` ("fabricated on 200-mm Si substrates at Advanced Micro Foundry", p.5). process_name from the printed
wording "foundry visible spectrum PIC platform on 200-mm Si wafers (Advanced Micro Foundry)". No facility.

Not entered and why:
- Main-text routing-waveguide losses (1.1-5.9, 1.8-7.1 dB/cm) and edge-coupler losses (7.5-11.3, 5.9-8.6 dB/facet):
  cited from the authors' refs. 2 / 35 (rule 3); this paper's own Fig. S2 values are entered instead.
- Parasitic capacitance Cp 70 +/- 21 fF (PIN) / 55 +/- 17 fF (PN): pad term extrapolated to zero length, not the device
  capacitance; per-length junction capacitance only as Fig. S14 curves (fF/mm, no parameter).
- V_M=1 = -4.5 +/- 0.9 V: no parameter. Low-gain bandwidth 7.6 +/- 0.3 GHz: bias not printed and stated for both
  lengths at once. Example V_br -13.1 V (Fig. S18): one example device.
- Calculated RC-limited bandwidth ~30 GHz, simulated EQE / mode-mismatch curves, simulated substrate-leakage and via
  losses: simulations / partial terms, notes only.
- Ring: no Q, FSR or tuning efficiency printed; dip positions vs heater power (about 65 / 203 / 336 mW) left in notes
  (per-FSR power would be an interpretation).
- Gap_nm (Wgap 150 nm design, 190 +/- 10 nm TEM) and SiN thickness at the PD (120 +/- 10 nm TEM): `gap_nm` not allowed
  on photodetector; values in component notes.
- Table II values of other works: rule 3.

Judgment calls:
- Dark currents printed in pA stored in nA as `derived` (D256).
- EQE: text bounds (> 60 % TE 400-535 nm, TM 400-640 nm), Table II span 60-88 %, and 12 Fig. 2(d) point reads
  (`extracted_from_figure`, +/- 3 points, mean of 3 devices). The Table II span is not the full min-max of Fig. 2(d)
  (TE 594 nm reads about 31 %); kept as printed with polarization unstated.
- APD M, GBP and V_br `derived` (ratio of own measurements; Miller-form fit as model-parameter extraction, D80a);
  V_br sign as printed (-13.3 / -13.8 V).
- Edge-coupler losses: 12 figure reads (TE / TM x 6 wavelengths), per_facet, method unspecified (isolation method not
  stated). Facet-end width 5.2 um entered as `tip_width_nm` 5200 (wide end; noted).
- Routing-waveguide losses: 6 figure-label values (`measured`, cutback fits) mapped by colour / marker; caption width
  520 nm vs 500 nm in the main text (noted).
- PIN 200 um row carries the cross-note to the ring PIC; PIN / PN 100-500 um rows hold only series resistance plus
  length (sibling designs, rule 9).

Missing orgs: none.

## Registry gaps (proposals, with the skipped value)

1. `receiver_sensitivity_dbm` (photodetector): received optical power for a stated BER and data rate (BER and rate in
   condition). martinez2016 -18.3 dBm (1.0 um APD) and -17.2 dBm (0.5 um APD) for BER < 1e-12 at 10 Gbps, 1550 nm,
   50 ohm amplifier (p.8 Sec. 1.2, Fig. 6). Possibly system-level (amplifier-limited per the authors).
2. `nep_pw_per_rthz` (photodetector): noise-equivalent power at a stated gain. martinez2016 0.21 / 0.38 / 0.72
   pW/sqrt(Hz) at M = 10 / 20 / 40 (p.7).
3. `fsr_nm` on phase_shifter (or a test-interferometer FSR in condition): zhong2021 MZI FSR about 8.5 nm, input to its
   P_pi (p.4).
4. `gap_nm` on photodetector (waveguide-to-absorber vertical spacing): lin2022a Wgap 150 nm design, 190 +/- 10 nm TEM
   (p.2-3).
5. `unity_gain_voltage_v` (photodetector, APD): lin2022a V_M=1 = -4.5 +/- 0.9 V (p.4).
