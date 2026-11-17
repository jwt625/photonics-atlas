# lit_162 batch report

Distilled 2026-11-16 under the pic-component-distill skill (Contracts v4-v7). Papers: lit:zhou2020a, lit:peng2024,
lit:chatterjee2020. Totals: 18 components, 126 metric rows. `merge_component_staging.py --dry-run`: +18 components,
+126 metrics, 0 errors (the one warning printed belongs to merged row cmp_lit_ni2025b_pimmwc, not this batch).

## lit:zhou2020a - 0 components, 0 metric rows

- Cached text (page 1) is "Diffraction tomography with a deep image prior" (Zhou, Horstmeyer; Duke University), arXiv
  1912.05330, matching its source row (DOI 10.1364/oe.379200, Optics Express 2020). It is the source row's paper, so no
  D397 stop on the cache.
- Content: computational 3D refractive-index tomography (deep image prior, CNN) of biological samples. No integrated
  or fiber-coupled photonic component is characterized: 0 rows (D411 scope).
- Coordinator flag: `cache_list.csv` lists zhou2020a as `benchmark_cite`, "cited in 1 benchmark tables / plots (2 um
  GeSn photodetectors)", class photodetector.vertical. This paper has nothing to do with GeSn photodetectors, so the
  benchmark-citation resolver very likely matched the wrong "Zhou 2020" Optics Express DOI. The intended GeSn
  photodetector paper is not in the cache (not checked further: no network).

## lit:peng2024 - 2 components, 31 metric rows

Cached text is the Research Square preprint rs-3435947 v1 (posted 2023-11-06, title "1.28 Terabit-per-second
all-silicon avalanche receiver") of the Nature Photonics paper of the source row ("An 8 x 160 Gb s-1 all-silicon
avalanche photodiode chip", 2024-08-09). All values are from the preprint; the journal version was not read. The
Supplementary file is not in the cache (p.14 lists it only).

| component | class | metrics |
|---|---|---|
| cmp_lit_peng2024_double_mrr_apd | photodetector.apd | 21 (responsivity 0.4 / 0.75 / >2 A/W at -8 / -8.1 / -8.2 V and 0.3 / 0.175 A/W at -6.5 / 3.5 dBm; dark ~1 / ~2 nA; 3-dB bandwidth ~40 / ~35 GHz, >50 GHz at low bias, ~40 GHz simulated; gain 5.9 / 8.9; GBP 236 / 311 GHz; F(M) 2.95 / 4.1 from Fig. 4(e); radius, Fig. 1(b) width / slab / etch) |
| cmp_lit_peng2024_rx_8ch | wdm.mrr | 10 (8 channels, FSR 9.02 nm / 1570 GHz, spacing 1.07 nm / 187 GHz, adjacent electrical crosstalk >50 dB measured, 41-66 dB simulated, radius, bus 500 x 220 nm) |

Values not entered and why:
- k ~0.28 (ionization-coefficient ratio from a McIntyre fit, p.8): no parameter (registry gap below).
- Data rates 92 Gb/s NRZ / 160 Gb/s PAM4 per channel, 1.28 Tb/s aggregate; sensitivity ~-2 dBm at 92 Gb/s NRZ (BER
  computed from Q, FEC 3.8e-3); SECQ 2.5-5.2 dB (p.8-9): link metrics, no parameter.
- PAT ~1.2 % conversion per round trip and ~7.1x cavity enhancement (p.7-8): absorption-model outputs, model in the
  uncached Supplement; no parameter.
- Simulated single-MRR comparison (~29 GHz, ~40 % responsivity-bandwidth product gain, -26 to -37 dB crosstalk;
  p.6, Fig. 2): a design that is not fabricated here.
- 0.77 nm spacing for < -40 dB crosstalk (from the measurement) and 18-channel / 3.6 Tb/s projections (p.7, p.10):
  hypothetical configurations; in notes.
- Simulated spacing for -40 dB: 96 GHz (0.552 nm) vs 245 GHz (1.4 nm) (p.6): comparison with a non-fabricated design.
- Doping levels (Fig. 1(b) labels) and the 245 / 205 nm contact offsets: no parameter; doping in core_material.
- Grating coupler and heaters: mentioned (Methods, p.6), no values.
- Table 1 rows of other works (rule 3); Table 1 "this work" duplicates the entered values.
- No capacitance, series resistance or breakdown voltage printed.

Judgment calls:
- D396: one physical set of rings entered twice, as the APD (photodetector.apd) and as the DWDM filter bank
  (wdm.mrr, the rings drop each channel to its APD in a WDM path, D400); cross-notes on both rows.
- One APD row for the 8 identical channels: the paper prints one value per quantity for "all channels"; `statistic
  typical`, `n_samples 8` where the text says all 8 channels.
- `ref_plane on_chip`: the paper states -16.5 dBm "optical power in waveguide" (p.7). Wavelength: "centre resonance
  wavelength" not printed; `band o_band`, `wavelength_inferred true` (1310 nm laser in Methods, Fig. 3(a) axis
  1302.5-1312.5 nm).
- Avalanche gain 5.9 / 8.9 `derived` (extracted with the authors' absorption model, D80a); GBP `derived` (5.9 x 40,
  8.9 x 35).
- ">50 GHz" at low bias entered as `gt`, bias empty (value in the uncached Supplementary Fig. 6; VNA limit 50 GHz).
- Fig. 1(b) dimensions (500 nm rib, 90 nm slab, 130 nm rib height) `extracted_from_figure` (figure labels, schematic).
- Excess-noise factor: two figure reads (gain about 6.0 -> F about 2.95; gain about 9.8 -> F about 4.1, +/-0.1);
  bias of the noise measurement not printed.
- Platform: APD `soi_rib` (Fig. 1(b) rib); filter bank `soi` (bus 220 x 500 nm, strip vs rib not stated).
- Fab `org_amf`: "fabricated using a standard Si photonics process at the Advanced Micro Foundry" (p.6) plus
  acknowledgment "We thank Advanced Micro Foundry for fabrication" (p.13). `process_name` empty: "standard Si
  photonics process" / "standard MPW run" names no PDK or node (Contract v7).

Missing fab / facility orgs: none (org_amf exists).

## lit:chatterjee2020 - 16 components, 95 metric rows

Cached text is the arXiv preprint 2007.05024 v1 (2020-07-05; title "Compact ring resonator enhanced silicon-MSM
photodetector in SiN-on-SOI platform") of the Optics Express paper of the source row. All values are from the preprint;
the journal version was not read.

| component | class | metrics |
|---|---|---|
| cmp_lit_chatterjee2020_gc | fiber_chip_coupler.grating | 5 (14 dB per coupler at 860 nm, 1-dB bandwidth 12 nm, period 650 nm, etch 220 nm, SiN 220 nm) |
| cmp_lit_chatterjee2020_sin_wg | waveguide_platform.straight | 4 (2.5 dB/mm -> 25 dB/cm cutback, 600 x 220 nm, BOX 2 um) |
| cmp_lit_chatterjee2020_ring_no_msm | resonator.ring | 7 (Fig. 7(a): Q 3816, FWHM 230 pm, ER 14 dB, IL 5 dB; FSR ~0.56 nm from Fig. 6; R 100 um, width 600 nm) |
| cmp_lit_chatterjee2020_ring_msm_fig7 | resonator.ring | 6 (Fig. 7(b): Q 4400, FWHM 200 pm, ER 6 dB, IL 9.5 dB; FSR ~0.56 nm; R 100 um) |
| cmp_lit_chatterjee2020_ring_{lw5_gw150, lw6_gw150, lw5_gw200, lw6_gw200} | resonator.ring | 5 each (Fig. 9 legend Q 3900 / 4400 / 1500 / 3200; Gw, Lw, R, width) |
| cmp_lit_chatterjee2020_rcpd_{same four keys} | photodetector.other | 11 / 9 / 8 / 8 (Table 1 dark current and responsivity at 1 / 3 / 5 V; 10 V bandwidth from Fig. 10; lw5_gw150 also 1 / 3 / 5 V bandwidths from Fig. 11; lw6_gw150 also ~0.8 nA at -5 V; Lp) |
| cmp_lit_chatterjee2020_wgpd_l{3, 5, 6, 15} | photodetector.other | 3 / 3 / 8 / 3 (Lp 6: Table 1 dark / responsivity, 10 nA at -5 V; Lp 3 / 5 / 15: bandwidths at 5 / 10 V from Fig. 12; Lp) |

Values not entered and why:
- Table 2 "This work" rows (45 / 292 pA/um2, 790 / 810 mA/W, 5 / 7.5 GHz, eta 3950 / 6075 mA/W*GHz, 4 um electrode
  separation, 100X): the row mixes devices (the 7.5 GHz is the Gw 200 nm / Lc 5 um device of Fig. 10(b), whose Table 1
  responsivity is 0.2 A/W), and the 5 GHz at 5 V matches no printed pulse width (Fig. 11: 105 ps -> 4.29 GHz): D159.
  The 7.5 GHz is entered on the device Fig. 10(b) identifies.
- 0.81 A/W at 10 V "for a 5 um long device" (abstract, conclusion): two 5 um designs exist (Gw 150 and 200 nm) and
  the device is not named; no 10 V responsivity appears in Table 1 or the figures: D159, in component notes.
- ~100X responsivity enhancement over the single-pass detector: no parameter.
- Photocurrents (Table 1; 1 uA vs 30 nA at -5 V, p.5-6): no parameter, input power not printed.
- "~4 dB more insertion and ~8 dB more extinction" with the detector (p.4): differences of the two Fig. 7 panels (both
  entered), not entered separately.
- Simulated directional-coupler coupling efficiency (Fig. 3) and the detector gap Gp 100 nm: no numeric coupling value
  printed; Gp has no photodetector parameter (in core_material).
- Electrode separation 4 um (Table 2 only): no parameter; device ambiguous as above.
- Fig. 5 SEM dimension labels are illegible in the render; nothing measured off scale bars.

Judgment calls (coordinator may overrule):
1. Row split: each of the four Table 1 RCPD designs is a photodetector row plus a resonator row for its cavity (D396:
   the resonator class carries Q, gap and coupling length, which photodetector does not allow). The detector-length
   series of WGPDs (3, 5, 6, 15 um) are four sibling rows.
2. Fig. 6 / 7(b) "SiN ring with PD": the paper does not name its design. Its Q 4400 equals the Fig. 9 legend Q of
   Lw 6 um / Gw 150 nm / Lp 6 um, but identity is only implied, so its values sit on a separate row
   (`ring_msm_fig7`) with a cross-note instead of on `ring_lw6_gw150`. If the coordinator accepts the Q match, merge
   the two rows (delete `ring_msm_fig7`'s q_loaded duplicate, move FWHM / ER / IL / FSR).
3. Bandwidths from pulse response: the paper converts pulse FWHM with its Eq. 1 (f3dB = 0.45 / FWHM, p.7). Printed
   values (3.46 +/- 0.4 GHz for the 5 um WGPD at 5 V; 7.5 GHz) and the same conversion of every other printed FWHM in
   the legends of Figs. 10-12 are `derived` with the FWHM and formula in notes (xue2022 / pospischil2013 precedent).
   Fig. 10 "Coupling length Lc" read as Lw (Table 1 pairs Lw = Lp; Fig. 11 caption and the 73 ps point agree).
4. Responsivities `author_estimate`: computed from power "in the ring waveguide" using the simulated coupler (Fig. 3)
   and a cavity-enhancement term (p.6), broadband LED 860-900 nm (`wavelength_nm` 860, `wavelength_max_nm` 900,
   `ref_plane on_chip`). WGPD responsivities also `author_estimate` (procedure "calculated from the power coupling").
5. Printed conflicts kept with notes (D417): Table 1 dark currents of RCPD Lw 6 / Gw 150 / Lp 6 are identical to the
   WGPD column (3.76 / 6.39 / 7.45 nA) and unlike the Fig. 8(a) RCPD dark trace of that design (about 10-17 nA at
   positive bias); text "0.79 A/W at 5 V" vs Table 1 0.80 A/W.
6. Bias signs as printed: Table 1 and Figs. 10-12 positive; the text's -5 V values (0.8 nA RCPD, 10 nA WGPD) entered
   at -5 V (asymmetric IV, p.5).
7. Grating coupler 14 dB/coupler: `loopback_half`, `measured` (per-coupler value from the reference waveguide, no pair
   total printed; beeck2020 / D452).
8. Ring Q / FWHM wavelengths read off the Fig. 7 axes (`wavelength_inferred`); Fig. 9 Q values have no wavelength
   (`nir_below_o`, inferred from the Fig. 6 resonances 876-880 nm). Polarization left empty everywhere (only the
   design is stated single-mode TE).
9. Platform: GC, waveguide, reference ring `sin`; rings with the Si detector and all detectors `si_sin_multilayer`
   (SiN guide evanescently coupled to the Si MSM island).

Missing fab / facility orgs: none entered. Fabrication is passive throughout ("The device is fabricated on a SOI
wafer", p.3-4) with all authors at the Indian Institute of Science (Center for Nano Science and Engineering, p.1), so
fab is empty (D80b). The acknowledgment (p.9) names only funding programmes (MHRD NIEIN, MeitY, DST NNetRA), not a
facility (D80c). The registry has no Indian Institute of Science org (relevant only if the coordinator rules
otherwise).

## Registry gaps

| gap | skipped value + locator | proposed definition |
|---|---|---|
| `ionization_ratio_k` (photodetector, unit 1) | peng2024 k ~0.28, p.8 Sec. Noise, Fig. 4(e) | APD effective ionization-coefficient ratio k from a McIntyre fit of measured F(M) (fit range in condition) |
| `data_rate_gbps` (photodetector; already raised D534) | peng2024 92 Gb/s NRZ / 160 Gb/s PAM4 per channel, p.8-9 Fig. 5(b) | highest demonstrated line rate with modulation format, equalization and BER criterion in condition |
| `sensitivity_dbm` (photodetector) | peng2024 ~-2 dBm at 92 Gb/s NRZ (FEC 3.8e-3), p.8 | input optical power at the stated BER / FEC threshold and data rate |
| `cavity_enhancement` (photodetector, unit 1) | chatterjee2020 ~100X (p.1, Table 2); peng2024 ~7.1x (model, p.8) | responsivity or intracavity power enhancement of a resonant detector over a single pass, as stated |
| `pulse_response_fwhm_ps` (photodetector) | chatterjee2020 Figs. 10-12 (60-443 ps) | FWHM of the impulse response to a short optical pulse; would hold the measured quantity instead of the 0.45 / FWHM conversion |
