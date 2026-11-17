# lit_163 batch report

Distilled 2026-11-16. Papers: lit:feldmann2019, lit:zhang2019e, lit:jiang2018. Totals: 7 components, 56 metric rows.
Validation: `merge_component_staging.py data/_staging/components/lit_163 --dry-run` -> +7 components, +56 metrics,
0 errors, no warnings on this batch. Page-1 titles match the source rows (feldmann2019 and jiang2018 are arXiv
versions, zhang2019e is the arXiv preprint 1905.03163 of the ACS Photonics paper; only the cached copies were read).

## lit:feldmann2019 (All-optical spiking neurosynaptic networks with self-learning capabilities)

Components 2 / metrics 14.

| component | class | metrics |
|---|---|---|
| cmp_lit_feldmann2019_neuron_ring | resonator.ring | extinction 9 dB at 1553.4 nm (measured, p.6-7, Fig. 2(d)); R 60 um; width 1200 nm, Si3N4 344 nm, full etch 344 nm, BOX 3.3 um |
| cmp_lit_feldmann2019_mux_rings | wdm.mrr | Q ~10,000 and IL 1.5 dB (author_estimate, C band inferred); R 40-55 um; 4 channels; same stack rows |

Values not entered and why:
- Waveguide crossing under the PCM cell, 0.23 dB (p.6): cited to the authors' earlier paper (ref. 29), rule 3 / D259.
- Switching energies: threshold ~430 pJ (Supp. Sec. 9, not cached), maximum 710 pJ with 200 ns pulses, threshold at
  60 % of the maximum (p.6-7): no switching-energy parameter (registry gap, already open from D417 / D579).
- Neuronal PCM cell (10 nm GST + 10 nm ITO, 9 um2) and synapse cells (3.6 um2): only energies and geometry, no
  performance parameter -> no phase_shifter.phase_change rows (rule 9); cell data in ring notes. Synaptic weights
  (Fig. 3(d)-(e)) are normalized, no absolute transmission.
- FSR of the neuronal ring: not printed; Fig. 2(c) would read about 2.4 nm (+/- 0.1), not entered (implies a group
  index of about 2.6, which I could not reconcile with a 344 nm x 1.2 um Si3N4 guide; left out rather than guess).
- 4-neuron layer (Fig. 5): 15 distributor rings per neuron on WDM channels 27-41 (C band), coupling efficiency
  1/(N'+1-i) as a design rule; no measured component value. Grating couplers: no values. Language-identification
  results are simulations of the network, not components.

Judgment calls:
- Mux-ring Q and IL `author_estimate` (D76: measured vs design origin not stated in the main text; details referred
  to Supp. S5, not cached). The IL scope is `unspecified` (per-ring drop path vs whole multiplexer not stated).
- "10.000" read as ten thousand (thousands separator).
- Neuron ring as `resonator.ring` holding the ring-level contrast (zheng2020 / fang2021 precedent, D396), no separate
  PCM-cell row.
- 1.2 um width applied to both rows from the Methods sentence covering all circuits (derived, D157).

Orgs: fab empty (passive Methods sentences; authors at Muenster, Oxford, Exeter). No facility named; the arXiv copy has
no acknowledgment section. Wafer supplier Rogue Valley Microdevices in notes. No missing orgs.

## lit:zhang2019e (Miniature Multilevel Optical Memristive Switch Using Phase Change Material)

Distilled from the cached arXiv preprint (1905.03163) of the ACS Photonics paper; the journal version was not read and
may differ. Components 4 / metrics 32.

| component | class | metrics |
|---|---|---|
| cmp_lit_zhang2019e_gst_mmi_d0p75 | phase_shifter.phase_change | IL 0.62 dB, contrast 2.92 dB (Table 1), D 0.75 um + 4 stack / heater rows |
| cmp_lit_zhang2019e_gst_mmi_d1 | phase_shifter.phase_change | IL 0.98 dB, contrast 10.39 dB (Table 1), D 1 um + 4 rows |
| cmp_lit_zhang2019e_gst_mmi_d1p2 | phase_shifter.phase_change | IL 4.03 dB, contrast 18.59 dB (Table 1), D 1.2 um + 4 rows |
| cmp_lit_zhang2019e_gst_mmi_switching_demo | phase_shifter.phase_change | 5 levels, > 50 cycles, contrast ~4.9-6.1 dB (Fig. 5 read), heater ~250 ohm, pulse powers 520 / 90 / 50 mW + 4 rows |

Values not entered and why:
- Switching energies 10 nJ (re-amorphization) and 8.2 nJ (crystallization) (p.12): no switching-energy parameter
  (registry gap).
- Fig. 3 erase thresholds (> 4.5 V at 100 ns; 140 / 180 ns at 3.5 V), Fig. 4 write thresholds (11-11.8 V, 16 ns,
  ablation at 12 V), "recovery time about 100 ns" and amorphization "response time around 100 ns": no threshold
  parameter; the response times are not defined as 10-90 % or as first-order time constants, and the Fig. 4 device is
  not identified (notes only).
- "Transmission contrast exceeding 20 dB" (abstract p.2, p.11, conclusion p.15): no measured device shows it (Table 1
  maximum 18.59 dB); p.11 frames it as possible with larger GST. Not entered.
- "Bandwidth of more than 100 nm (limited by measurement)" (p.10-11): no bandwidth parameter on phase_shifter.
- MMI 12 x 2 um, 4 um tapers to 1.2 um, crossed strip 1.7 um, GST / ITO 30 nm, Ti/Au 20/100 nm: `mmi_*`,
  `taper_length_um` and a PCM-thickness parameter are not allowed on phase_shifter (registry gap; values in
  core_material).
- Table 1 "+/-" spreads (meaning and sample count not printed): kept in notes, not as `std` rows.

Judgment calls:
- Class `phase_shifter.phase_change` for the amplitude-only non-volatile 1x1 switch (D155; chen2022c wg_switch_1x1
  precedent), not `switch_fabric.other`.
- Fig. 5 device diameter is not stated: its values sit on a separate `switching_demo` row (D159; delaney2021
  endurance-row precedent) instead of a Table 1 row. It may be one of the three Table 1 devices (Fig. 3(b) of the 1 um
  device saturates near Delta T / T0 = 3.9, Fig. 5 near 3.0; no match is stated).
- Printed conflict (D417), on the d1 row note: Fig. 3(b) / (d) maximum Delta T / T0 about 3.9 (about 6.9 dB as a
  contrast) vs Table 1 10.39 dB for the 1 um device; kept as printed.
- p.12 text says "Figure 5(b) shows ... five clear distinct levels" while the caption puts the multi-level trace in
  Fig. 5(c); locator cites Fig. 5(c).
- Fig. 5 contrast 4.9-6.1 dB `extracted_from_figure`: read Delta T / T0 (amorphous 285-310 %, crystalline 0-25 %),
  converted with 10 log10((1 + a) / (1 + c)); formula and reading in notes.
- Pulse peak powers 520 / 90 / 50 mW and the ~250 ohm resistance `author_estimate` (origin not stated; the powers equal
  V^2 / 250 ohm). Stored in `tuning_power_mw` as zheng2020 did for Set / Reset pulse powers.
- IL scope `unspecified` and band `unspecified`: Table 1 prints neither the reference structure nor the wavelength
  (spectra 1500-1600 nm in Supp. S3, not cached).
- GST disk diameter stored as `length_um` (extent along propagation), as earlier rows store PCM cell lengths.

Orgs: fab `org_shanghai_jiao_tong_university` (author contributions p.15: H. Zhang fabricated, J. Xu contributed to
fabrication, both SJTU; D395 / D439); facility `org_center_for_advanced_electronic_materials_and_devices` (AEMD of
SJTU thanked for support in device fabrication, p.16). No missing orgs.

## lit:jiang2018 (Miniaturized high-frequency sine wave gating InGaAs/InP single-photon detector)

Components 1 / metrics 10.

| component | class | metrics |
|---|---|---|
| cmp_lit_jiang2018_ingaas_spad | photodetector.spad | PDE 30 % (module, 243 K), DCR 2000 Hz, afterpulse 8.8 / 7.1 / 6.4 % at 243 / 253 / 263 K, breakdown 65.9 V, dark current 0.2 nA at Vbr - 1 V, capacitance ~130 fF, junction 25 um, module power 15 W |

Values not entered and why:
- Effective gating width 138 ps FWHM (Fig. 4(b), 20 % PDE) and 176 ps (p.4 normalization): gate width rejected as a
  parameter (D250). The two values are quoted at different settings as far as the text shows; no conflict claimed.
- Punch-through voltage 38.6 V: no parameter.
- Normalized afterpulse 7.5e-5 / ns and DCR 9.1e-6 / ns: per-gate-time quantities, no parameter (registry gap, as
  ren2025 per-gate dark count, D576).
- DCR at 253 / 263 K: only in Fig. 4(a) (log axis, curve ends near 28-30 % PDE); not read.
- One-week stability (PDE ~20 %, 243.0-243.6 K, Fig. 6): no parameter. Timing jitter: a design goal, not reported.
- MIRC readout circuit (LTCC; ~40 dB gain, ~80 dB rejection at 1.25 GHz) and gating electronics: electronics, not
  photonic components (rule 13 analogue).

Judgment calls:
- In scope as a discrete fiber-pigtailed detector chip measured at the module input (D155, qi2024 precedent, same
  group and architecture); `ref_plane module` on the PDE row.
- No wavelength is printed anywhere (only "near-infrared"); PDE row `band: unspecified` with note.
- Chip I-V / C-V values at "room temperature": `temperature_k` left empty (no number printed), stated in the
  condition. qi2024 entered 300 K for the same wording; the coordinator may align.
- Dark-current bias -64.9 V computed from the printed Vbr 65.9 V minus 1 V (reverse bias negative, qi2024).
- DCR "as low as 2.0 kcps" -> 2000 Hz `derived` (D256), statistic `best`; PDE 30 % is the operating point, not a
  maximum.
- Module power 15 W `author_estimate` (measured vs rated not stated), scope in the condition.

Orgs: fab empty: "We design and fabricate" with authors at USTC, China Electronics Technology Group Corporation No.44
Research Institute and QuantumCTek (D154; qi2024 precedent). Not in the registry (only relevant if the coordinator
assigns fab): "China Electronics Technology Group Corporation No.44 Research Institute" (p.1 affiliation 3). No
facility named.

## Registry gaps (with the skipped value)

- Switching / programming energy per pulse (phase_shifter, resonator with PCM): feldmann2019 430 pJ threshold and
  710 pJ maximum (p.6-7); zhang2019e 10 nJ / 8.2 nJ (p.12). Proposed `switching_energy_nj`: electrical or optical
  energy of one programming pulse, type and pulse width in condition.
- Geometry on phase_shifter: `mmi_width_um` / `mmi_length_um` / `taper_length_um` (zhang2019e 2 / 12 / 4 um, p.4) and a
  PCM layer thickness (zhang2019e 30 nm, feldmann2019 10 nm GST).
- Per-gate-time noise of gated SPADs (jiang2018 9.1e-6 / ns DCR, 7.5e-5 / ns afterpulse, p.4).
- Operating optical bandwidth of a broadband phase_shifter / attenuator (zhang2019e > 100 nm, p.10-11).
