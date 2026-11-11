# Batch cpo_01 report (distill subagent, 2026-11-01)

Three co-packaged-optics papers. Dry run on a scratchpad copy of the repo with the three rows of `sources_proposed.csv`
appended to its registry: `batch cpo_01: +4 components, +14 metrics; errors 0` (one WARN about another batch's row,
cmp_lit_ni2025b_pimmwc-m18). Without those registry rows the source_id foreign keys cannot resolve, so the sources must be
registered before the merge. All three are restricted: facts and locators only. Page-1 titles match; none is a correction
or erratum; text layers clean. Page renders checked: COUPE p.3, Intel pp.2-3, NVIDIA p.3 (Figs. 23.1.5-23.1.7).

## Registry proposals (`sources_proposed.csv`, nothing edited by hand)

- `pk:ectc51687.2025.00015`, `eo:levy2026`, `eo:song2026`. They should come from `build_sources.py` once the sibling paper
  rows exist; at distill time both sibling caches hold the papers but neither `papers.csv` lists them.
- `access`: `paywalled` on the EO and pk rows of levy2026 and song2026 (as in EO papers.csv); `unknown` on pk:ectc51687.2025.00015 (PK source.json rule). `same_as`: pk:vlsitechnologyandcir65830.2026.11577543 -> eo:levy2026, pk:isscc49663.2026.11409081 -> eo:song2026.
- Intel and NVIDIA are entering two corpora. Rows use the EO ids (EO is canonical in the `same_as` precedent for OFC papers
  and is what `host_device_ids` links to). If the pk ids are preferred: `pk:vlsitechnologyandcir65830.2026.11577543`,
  `pk:isscc49663.2026.11409081`, with component ids renamed to match.

## Per paper (components / metrics)

- ectc51687.2025.00015 TSMC COUPE (2 / 8): 1D GC in the COUPE-GC stack (fiber_chip_coupler.grating): IL < 1.2 dB half-loopback,
  1-dB width about 25 nm (about 20 nm at PIC wafer level, derived), peak-wavelength spread < +/-1.7 nm across the wafer, 127 um
  fiber spacing. Added optical path (micro_optics.integrated_lens): net IL mean 0 dB, std 0.04 dB (derived per D80a), 800 um
  support Si.
- levy2026 Intel (1 / 3): integrated DFB array (laser.dfb): 16 lasers, 200 +/- 40 GHz, printed carrier wavelengths
  1302.22-1319.54 nm. Fab org_intel from the acknowledgement.
- song2026 NVIDIA (1 / 3): RX ring filter bank (wdm.mrr, soi): Q 4K, 200 GHz, 9 channels. About 5 um radius removed (rule 2, in EO song2026-a epitaxy_or_stack).

## Not entered, and why

COUPE:
- FAU coupling loss: not reported; the matching FAU is in development (p.5). The IL is wafer-level, no FAU in the number.
- PIC-wafer IL: only described as matching (p.1), no number.
- Peak wavelength: Fig. 6 axis has no tick labels.
- Edge-coupler variant: mentioned only (p.2), no data.
- Out of scope: SoIC / TDV daisy-chain resistance, 3 dB bandwidth > 100 GHz (simulated, RF path), TDECQ 1.61 to 1.68 dB (loopback).

Intel (p.1 unless noted), no quantitative result for any of these, so no rows:
- Vertical coupler, RAMZI and CMZI interleavers, ring add-drop filters, SOAs, polarization splitter, dynamic polarization control.
- Ge PD: only -10.9 dBm worst-case received power (link condition). 24 GHz, about 65 dBOhm and 3 uArms are the EIC receiver.
- 1.69 pJ/b PIC efficiency: link budget, no parameter, laser amortization assumed.
- MRM extinction ratio, bias and data rate: EO atlas scope.

NVIDIA:
- TX ring Q about 4.5K: modulator, EO atlas scope (rule 2).
- Grating couplers: no loss stated. Fig. 23.1.5 top left shows a TX bus transmission envelope peaking near -4 dB, but neither
  the optical path nor the normalization is stated, so assigning it to the couplers would be a guess. For the audit to rule.
- Ge PD: no responsivity, capacitance or bandwidth. RX sensitivity -16.0 dBm OMA is link-level with the TIA.
- FAU, lens carrier chip, 2 GC rows (Fig. 23.1.7): labels only, no performance.
- Heater code versus wavelength (Fig. 23.1.5): DAC code only, TX rings. 0.76 / 0.49 pJ/b ring heaters: link energy, no parameter.
- 10 % laser wall-plug efficiency: assumption, cited. Multi-wavelength laser: bench equipment (rule 13).

## Judgment calls for the audit

1. COUPE values next to citation [3], the authors' own org platform paper (D259 / D408): kept, because the abstract and
   conclusion present them as this paper's first COUPE wafer results. If the audit reads Fig. 6 as reproduced, the GC IL and
   bandwidth rows go.
2. COUPE net IL on a separate micro_optics row rather than the GC row: the paper attributes it to the added path.
3. COUPE fab_org_ids empty: no fabrication sentence naming an org (D80b), though the paper calls it TSMC's COUPE wafer.
4. Platform empty for COUPE and Intel (D422): neither paper states the guiding stack. NVIDIA `soi` from Fig. 23.1.6.
5. `length_um` for the 800 um support Si is the closest parameter; the condition says what it is.
6. NVIDIA Q basis `author_estimate` (D82a): a selected design value; test-chip validation is mentioned without data.
7. host_device_ids set after the EO merge: levy2026-a, song2026-a.

## Missing orgs

None. org_intel and org_tsmc exist; no facility is named in any paper.

## Registry gaps (values kept in component notes)

- `il_improvement_db` (reflector or stack gain over a reference, positive dB; fiber_chip_coupler, micro_optics): COUPE Cu
  reflector 0.5 dB, p.3 Sec. IV.A, Fig. 5(b).
- `delta_il_after_stress_db` (IL change after a named reliability test, stress in condition; fiber_chip_coupler, micro_optics,
  fiber_interface): COUPE < 0.25 dB, p.4 Fig. 11.
- `beam_angle_variation_deg` (sample-to-sample beam-angle spread, +/- value; fiber_chip_coupler, micro_optics, fiber_interface):
  COUPE < +/-0.1 deg, p.3 Fig. 8.
