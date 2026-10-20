# PIC component atlas: taxonomy, spec fields, schema, corpus yield (research, 2026-10-20)

Exploration only. Nothing in the EO atlas, packaging atlas, OFC folders or blog was modified, downloaded or committed. Scratch work (scan scripts, extracted blog text, snippets) is in the session scratchpad `components/` folder.

## 0. Sources, locator conventions, method

| corpus | path | items with text | access | locator form used here |
|---|---|---|---|---|
| EO atlas | `references/<paper_id>/text.md` | 231 | per `papers.csv` `access` / `redistribution` | `paper_id p.N` (`<!-- page N -->`) |
| Packaging atlas | `advanced-packaging-atlas/references/<id>/text.md` + `data/optical_interfaces.csv` (55 rows) | 296 | no access column; mostly IEEE ECTC/EPTC (assume not OA) | `pkg:<id> p.N` |
| OFC 2026 | `PlayGround/20260320_OFC/extracted_text/*.md` + `ofc-2026/ofc_browser/extracted_text/` | 677 distinct session codes (the 126 browser texts are a subset of the 677) | not OA (facts/locators only) | `ofc2026:<code>:p.~N` (see note) |
| Blog PDFs | `jwt625.github.io/assets/doc/...` (14 PDFs extracted with pymupdf) | 14 | mixed | `blog:<relative path> p.N` (PDF page index) |

- **OFC page caveat:** the OFC `.md` files have no page markers. Pages are inferred from the nearest preceding `_page_K_` image reference (marker index K is 0-based, so p = K+1). Treat `p.~N` as approximate (+/-1). The papers are 3 pages long.
- **Overlap:** 54 OFC 2026 papers are already in the EO atlas (venue `Optical Fiber Communication Conference (OFC) 2026, paper <code>`, access `unknown`, local-only), e.g. `porto2026` = ofc2026:Th1C.4, `hulyal2026` = ofc2026:W1A.7, `zhou2026` = ofc2026:Th1C.3. Dedupe by DOI or session code. (Corrected 2026-10-20 per audit; originally stated three.)
- **Method:**
  - Keyword plus metric regex within a +/-200-250 character window per class (script `strict3.py`). This gives candidate counts.
  - OFC titles were also classified separately by primary component.
  - Deep reads covered 30 EO papers, 25 OFC papers, 4 blog PDFs and the packaging `optical_interfaces.csv`. Every example value below was read in the cached text.
  - Spot checks found false positives: `axline2026` and `chen2022` mention GCs without numbers, and the `nelan2022` crossing hit has no crossing loss. They also found false negatives: the PD pattern needs "photodetector" near "A/W". The counts in §4 are therefore candidate yields, not verified yields.

## 1. Taxonomy (class -> subtype) and value by application

Value ratings: H = high, M = medium, L = low. CPO = co-packaged optics. AMO = atomic, molecular and optical (trapped ions, neutral atoms, clocks).

| class | subtypes | CPO / interconnect | AMO / quantum | note |
|---|---|---|---|---|
| `fiber_chip_coupler.grating` | 1D uniform, apodized, 2D (polarization-splitting), dual-layer (Si+SiN, poly-Si overlay), bottom reflector, mode-multiplexing (few-mode/MCF), focusing, photonic-crystal | H (wafer test; surface I/O) | M (cryo packaging, visible/UV emitters) | most-reported side metric in EO papers |
| `fiber_chip_coupler.edge` | inverse taper, trident/multi-tip, cantilever/suspended, SiN/SiON/polymer SSC, double-layer taper, multimode inverse-designed | H (CPO fiber attach) | M | loss scope is the main pitfall |
| `chip_chip_coupler` | evanescent (die-to-wafer, SiN tip-to-tip), adiabatic, butt (laser-to-PIC), photonic wire bond (PWB), micro-transfer printed | H (heterogeneous lasers, chiplets) | L | overlaps packaging `optical_interfaces` |
| `micro_optics` | facet-attached 3D-printed microlens (FaML), integrated SiON microlens, metalens pair, vertical tapered waveguide to PD, MLA to GC array | H (expanded-beam, detachable) | M (astro-photonics MLA to GC) | metric = loss + 1-dB tolerance |
| `fiber_interface` | FAU (pitch, angle), V-groove, MCF fan-in/fan-out, glass-waveguide fan-out/substrate | H | L | mostly OFC/packaging |
| `free_space_emitter` | focusing grating emitter (ion/atom addressing), metasurface coupler/lens, UV/visible platform emitters | L | H | **no quantitative examples in any local corpus** (gap, §5) |
| `splitter` | MMI 1x2/2x2/NxN/arbitrary ratio, directional coupler (straight, bent/S-bent, tunable), adiabatic coupler, Y-branch, 90° hybrid | M | M | usually reported only as loss-budget terms |
| `crossing` | MMI-based, SWG, multilevel | M (switch fabrics) | M (meshes) | thin coverage |
| `resonator` | single ring/racetrack (all-pass, add-drop, Euler), coupled rings, photonic-crystal/FP cavity, Bragg resonator; tracked for Q, loss extraction, FSR, tuning | M | H (high-Q, SIL lasers) | intrinsic vs loaded Q pitfall; ring used as a channel filter goes to `wdm.mrr` |
| **`wdm`** (top-level category, user feedback 2026-10-20) | `wdm.awg` (incl. overlapping/flat-top), `wdm.eg` (echelle / planar concave grating), `wdm.cascaded_mzi` (MZI lattice, CWDM/LWDM trees), `wdm.mrr` (microring mux/demux, ring filter banks, collective tuning), `wdm.bragg_cdc` (Bragg / contra-directional coupler add-drop), `wdm.interleaver`, `wdm.tff` (thin-film filter in optical sub-assemblies) | H | L | OFC-dominant; mux and demux both rows; grid per ITU-T G.694.1 (DWDM) / G.694.2 (CWDM), LAN-WDM per IEEE 802.3 |
| `polarization` | PBS, PSR/PRC, polarization compensator, 2D GC as PBS | H (ELS polarization) | M | |
| `phase_shifter` | thermo-optic (incl. undercut, folded), MEMS, phase-change (Sb2Se3, GST), ferroelectric non-volatile, EO (EO atlas) | M (ring tuning power) | H (programmable meshes) | MEMS/PCM have no local metrics |
| `switch_fabric` | MZI NxN, MEMS, WSS | M | M | composite; link to its component rows |
| `photodetector` | Ge/GeSi waveguide PD, APD, vertical-illumination PD, graphene, InGaAs on TFLN, SNSPD/SPAD | H (400G/lane) | M (SNSPD) | |
| `laser` | DFB, SOA-integrated DFB, EML (with EO atlas), DBR, ECL, self-injection-locked (SIL), PCSEL, VCSEL, ELS/ELSFP module, comb source | H (ELS power classes) | H (visible SIL, narrow linewidth) | chip vs fiber-coupled vs module level |
| `amplifier` | SOA (QW/QD), Er/rare-earth waveguide amplifier, parametric | M | L | |
| `nonreciprocal` | isolator, circulator (magneto-optic, Faraday-rotator hybrid, time-modulated) | M (ELS back-reflection) | M | no integrated metrics in EO/pkg/OFC |
| `waveguide_platform` | Si strip/rib, SiN (thin/thick), Ge-silica, Al2O3 (UV), TFLN/TFLT, BTO, suspended GaAs, glass (ion-exchange/laser-written), polymer | H | H (UV/visible loss) | propagation loss vs band is the backbone plot |
| `mode_converter` (extension) | MDM mux, mode converter, few-mode/MCF GC | M | L | 18 EO / 29 OFC mention it |

## 2. Shared fields and per-class tracked specs

### 2.1 Shared fields (every component row)

`platform` (enum; reuse EO `waveguide_platform` plus new values), `core_material`, `core_thickness_nm`, `etch_depth_nm`, `cladding`, `min_feature_nm` (e.g. 120 nm design constraint, ofc2026:Tu2J.5:p.~1), `wavelength_nm`, `band` (ITU-T G.Sup39 / ISO 20473, identical to EO schema convention (l)), `polarization` (TE/TM/both/PI), `mode` (TE0, LP11...), `temperature_c` plus `temperature_ref` (chip/case/ambient; for example W1B.3 states case temperature), `foundry_or_fab`, `process_name`/PDK, `wafer_size_mm`, `wafer_supplier`, `statistic` (single/mean/median/wafer_map, `n_samples`), `basis` (measured/simulated/derived/author_estimate/design_target/extracted_from_figure/calculated), `method` (cutback/reference_structure/loopback/loss_breakdown/ring_extraction/OFDR/wafer_prober), `scope` (enum, §2.3), `host_device_id` (EO atlas `device_id` when the component is side data of a modulator), `qualifiers`, `locator`, `notes`.

### 2.2 Cross-class pitfalls (bind as schema rules)

1. **Sign:** many sources quote loss as negative dB, e.g. "−0.98 dB" (ofc2026:Tu2J.2:p.~1) or "loss < −2.4 dB" (ofc2026:W4B.5:p.~1). Store loss as positive dB, quote the source sign in the note, and flip `lt`/`gt` accordingly.
2. **Linear vs dB:** "peak efficiencies around 30%" (witmer2020 p.11) and "81-85% coupling throughput" (blog AstroPIC II p.1-2) go in a `%` field. Any dB value made from them is `derived`.
3. **Bandwidth definition:** 1-dB vs 3-dB vs FWHM. witmer2020 p.11 quotes FWHM about 40 nm, which is a 3-dB width. Keep `bw_1db_nm` and `bw_3db_nm` separate and never convert between them.
4. **Scope:** per coupler, per facet, loopback/2, fiber-to-fiber, or unstated. Example: holzgrafe2020 p.4 says "≈10 dB insertion loss" for the GCs with no scope given, measured at T ≈ 1 K.
5. **Measured vs simulated in the same abstract:** ofc2026:W4B.5 gives simulated −1.83 dB with a 34 nm 1-dB BW (p.~1) and measured −1.9 dB with a 20 nm 1-dB BW (p.~2). ofc2026:Tu2J.5 gives simulated −1.5 to −2.5 dB vs measured −2.4 to −5.1 dB (p.~1).
6. **Values cited from prior work go to notes:**
   - ofc2026:Tu2J.2:p.~1 cites "0.16 dB/cm at 1311nm [3]".
   - li2026aa p.8 has a 3.64 A/W PD in a reference title.
   - steckler2025 p.8 has a comparison table that mixes cited PDs.
   - ofc2026:W1B.3:p.~1 quotes a PCE of 21.6% from its own earlier work [3].
   This is the same rule as packaging rule (a) and EO convention (bb).
7. **Loss-budget decomposition:** many EO papers give component losses only as terms of a device budget, e.g. valdez2023 p.7 and li2025b p.6. Use `basis: derived`, `method: loss_breakdown` and link `host_device_id`.
8. **Q extraction:** loaded vs intrinsic Q. Loss "extracted from the loaded quality factor" (li2025b p.6) vs from intrinsic Q on a reference resonator on the same chip (feng2022 p.9).
9. **Calculated tolerances:** ofc2026:Th2A.8:p.~2 gives a "calculated" 1-dB tolerance of ±18 µm. That is `simulated`, not measured.

### 2.3 `scope` enum for coupling and insertion loss

`per_coupler` · `per_facet` · `per_interface` (chip-chip) · `loopback_half` (loopback/2, may include connector/fiber) · `fiber_to_fiber` · `on_chip_excess` · `device_total` · `de_embedded` (coupler loss removed) · `unspecified`. Also `includes`/`excludes` free text, as in EO `il_onchip_includes`.

### 2.4 Per-class spec fields and example values

Each example states its basis. "meas" = measured, "sim" = simulated, "derived" = derived from a loss budget.

#### Grating coupler

Fields: `peak_loss_db` (+scope), `peak_ce_pct`, `center_wavelength_nm`, `bw_1db_nm`, `bw_3db_nm`, `pdl_db` (2D GC), `fiber_angle_deg`, `fiber_type`, `back_reflection_db`, `power_handling_dbm`, `period_nm`, `fill_factor`, `etch_depth_nm`, `overlay` (poly-Si, SiN), `bottom_reflector` (y/n), `apodized` (y/n), `n_modes`, `statistic` (wafer-level).

| source | platform / band | values |
|---|---|---|
| ofc2026:Tu2J.2:p.~1 (TSMC) | Si 270 nm + SiN dual-layer, O-band | Wafer-level, 29 dies: −0.98 dB (Si) / −1.16 dB (SiN/Si), 1-dB BW 24 -> 62 nm. Si loopback shows absorption at about 15 dBm; SiN is stable to 24 dBm (instrument limit). meas |
| ofc2026:Tu2D.3:p.~1 (Samsung Foundry) | 305 nm Si / 400 nm SiN, O-band | 1D Si GC 1.9 dB, 1-dB BW 27 nm. 2D Si GC 2.4 dB TE and TM, 17 nm. 1D SiN GC 2.1 dB, 57 nm. meas |
| ofc2026:W4B.4:p.~1 | 220 nm SOI + 160 nm poly-Si, 2D GC to 7-core MCF | −2.4 dB, 3-dB BW 55 nm, PDL < 0.7 dB within the 3-dB band. meas |
| kharel2021 p.4 | TFLN (no high-index substrate), 1560 nm | 6 dB/facet; GC pair total 13 dB. meas |
| kohli2025 p.4 | plasmonic BTO-on-SiN, 1550 nm | 2.8 dB per coupler by cutback. meas |
| witmer2020 p.11 | SOH, cryo-packaged with angle-polished fibers | Peak efficiency about 30%, FWHM about 40 nm. meas, approx |
| li2022b p.1, p.3 | TFLN, 532 nm | 5 dB coupling loss; design period 288 nm, fill factor 0.6 (design_target). |
| luan2026a p.4 | Si photonic-crystal apodized GC, 2 µm band | 14 µm wide, 400 µm taper, 6 dB IL. meas |
| li2025b p.6 | suspended GaAs | 7.0 dB per GC (derived from loss breakdown). |
| falcone2026 p.5 | nanoimprinted BTO sol-gel | 4 dB per grating (sim); period 1.2 µm, element width 470 nm, height 350 nm (design). |
| blog:2025/1362309-AstroPIC II... p.1-2 | astro-photonics, NIR | 81-85% coupling throughput for a 20 nm narrowband (linear). |
| pkg:ectc51909.2023.00009 p.6 Table I | SPGC, 1308 nm | 3.27 dB per SPGC, mean over several wafers (+/-0.2 dB), from packaging `optical_interfaces.csv`. |

#### Edge coupler / SSC

Fields: `loss_db` (+scope), `wavelength_nm` (spectral list), `mfd_chip_um` (with 1/e² definition stated), `mfd_fiber_um`, `fiber_type` (SMF-28, UHNA7, lensed, PMF, MMF), `tip_width_nm`, `taper_length_um`, `pdl_db`, `tol_1db_x_um`/`tol_1db_y_um`/`tol_1db_z_um`, `alignment` (active/passive/self_aligned), `facet_ar` (y/n), `n_modes`.

| source | platform / band | values |
|---|---|---|
| li2026aa p.4 | TFLN SSC, 1260-2060 nm | TE per-facet loss: 0.78 dB @1310 nm, 1.18 @1450, 1.73 @1485, 0.69 @1550, 0.56 @1590, 0.69 @1653, 0.82 @1970, 2.21 @2000 nm. meas. Gives 8 metric rows. |
| liu2026d p.4 | TFLN, visible and NIR | 3.0 dB/facet at 940 nm (estimated from test structures); 19 dB/facet at 488 nm; 16 dB/facet for orange/red. Tip width 5 µm (visible) / 200 nm (NIR). |
| valdez2023 p.7 | SOI inverse taper to lensed fiber, O and C | Tip 180 nm, tapering to 650 nm over 300 µm (design). |
| hu2026a p.5-6, p.11 | SiON SSC (3x3 µm) to UHNA7; DFB butt-coupled to TFLN | DFB-to-chip adds about 5 dB extra coupling loss. meas, approx |
| hulyal2026 p.3 | LTOI double-layer edge tapers | "additional 4 dB coupling loss". Scope unstated (likely both facets); needs `scope: unspecified`. |
| ofc2026:Th2A.1:p.~1 | PLC/SiN SSC to InP SOA, 1310 nm | About 1.5 dB per facet. SOA MFD 2.74x0.68 µm (TE) and 2.43x0.77 µm (TM), 1/e², simulated. |
| ofc2026:Tu2J.5:p.~1 | 400 nm SiN, multimode inverse-designed | 5-mode coupler: meas −2.4 to −5.1 dB vs sim −1.5 to −2.5 dB. Footprint 36x40 µm. |
| pkg:ectc51687.2025.00012 p.2-3 | EC to FAU, CPO | 2.46 dB (active) / 2.62 dB (passive, mean of 10 chiplets), loopback/2 including MTP-MT connector. |
| ofc2026:Th1D.3:p.~1 | glass waveguide fan-out to SMF-28 Ultra, 1310 nm | < 0.3 dB per fiber facet; fiber-to-fiber 0.62 ± 0.01 dB. |

#### Micro-optics / PWB / chip-chip coupling

Fields: `loss_db` (+scope), `tol_1db_lateral_um`, `tol_1db_longitudinal_um`, `beam_diameter_um`/MFD at the interface, `lens_material`, `lens_index`, `lens_height_um`, `ar_coating`, `writer`/process (two-photon lithography, wafer-scale SiON), `pwb_length_um`, `polymer`, `reflow_compatible` (y/n), `pdl_db`, `wdl_db`.

| source | values |
|---|---|
| ofc2026:W4B.1:p.~1 | FaML: fiber-to-chip IL < 1 dB; 1-dB excess loss at 5 µm misalignment; 25 µm MFD. Adaptive design corrects up to 30 µm placement error. PICs from Tower and Applied Nanotools. meas |
| ofc2026:W4B.2:p.~1-2 | SiON integrated microlens (h 18.1 µm, r 20.4 µm, n 1.57). Loss 1.0 dB (O) / 1.4 dB (C); < 1.3 dB per coupler across the O-band; PDL 0.3 / 0.1 dB; WDL < 0.1 dB. 1-dB tolerance ±2 µm lateral, 27 µm longitudinal. With AR coating, 0.34 dB TE / 0.32 dB TM (sim). |
| ofc2026:Th2A.8:p.~1-2 | Metalens pair, PIC to detachable FAU: 1-dB tolerance ±18 µm (calculated); 70 µm collimated beam; 36-channel 2D FAU at 500/250 µm pitch. |
| ofc2026:Th3C.3:p.~1 | Vertical tapered waveguide, 50 µm-core MMF to PD apertures down to 10 µm: CE > 95%, tolerance > ±25 µm. |
| singer2025 p.6 | PWB-packaged SOH MZM array: fiber-to-fiber 10.8 dB, on-chip excess 4.2 dB. The PWB share is only in Appendix B (not extracted). |
| pkg:ectc51846.2026.00016 p.6 | Fiber+lens to fiber+lens 0.6 dB (< 0.3 dB per lens). |
| pkg:ectc51529.2024.00227 p.5 | Evanescent die-to-wafer coupler 0.32-0.37 dB per coupler, passive, 1310 nm. |

#### Splitters: MMI / DC / Y-branch / crossing

Fields: `excess_loss_db`, `imbalance_db` or `split_ratio` (power), `split_ratio_variation` over a stated span, `bw_nm` (for a stated criterion), `phase_error_deg` (90° hybrid), `footprint_um2`, `gap_nm` (DC), `tuning_power_mw` (tunable DC); crossing: `crossing_loss_db`, `crosstalk_db`.

| source | values |
|---|---|
| valdez2023 p.3, p.7 | Si-LN MZM: 2x2 MMI 0.2 dB per coupler (derived, loss breakdown); MMI width 6 µm. |
| nelan2022 p.6 | TFLN MMI: peak splitting difference 1.4% at 1530 nm, which supports > 45 dB ER (p.3). |
| li2022b p.3 | TFLN, 532 nm: MMI 4 µm x 36.1 µm (design_target). |
| ofc2026:M1E.2:p.~1 | CWDM demux built from MMIs with power coupling coefficients 0.5 / 0.81 / 0.96. |
| ofc2026:W2A.9:p.~1 (imec) | S-bent DC: coupling variation 0.065 over 80 nm, vs 0.298 for a straight DC, at 200 nm gap. meas |
| ofc2026:M2D.2:p.~1 | Curved tunable DC: 40:60 to 60:40 with < 20 mW heating. 4x4 fabric crosstalk < −50 dB, on-chip IL < 1.5 dB. |
| li2025b p.6, p.10 | Suspended GaAs: 1.0 dB per Y-splitter (derived from stand-alone test structures). |
| ofc2026:W2A.3:p.~2 | Compact crossing 1.35 dB measured vs foundry library 1.3 ± 0.05 dB. |

#### Resonators (single-device Q / loss; channel filters go to WDM)

Fields: `q_intrinsic`, `q_loaded`, `extraction` (fit model, reference resonator), `fsr_ghz`/`fsr_nm`, `radius_um`, `coupling_gap_nm`, `drop_il_db`, `bw_1db_ghz`, `er_db`, `tuning_eff_mw_per_pi` (or nm/mW), `prop_loss_derived_db_per_cm`.

| source | values |
|---|---|
| berman2026 p.1-2 | BTO racetrack: Q_L 605k, Q_i > 1 M; propagation loss about 0.5 dB/cm. |
| feng2022 p.9 | TFLN racetrack: Q_i 1.1x10^6, from a reference racetrack on the same chip. |
| ofc2026:Tu2D.3:p.~1 | Ring drop filter (DRF): drop-port IL < 1.0 dB, 1-dB BW 105 GHz. |
| ofc2026:Tu3C.4:p.~1 | Si ring WDM filter: 3.80 mW/π per channel with collective tuning. |
| ofc2026:Th1D.7:p.~1 | Ge-silica: 3 mm diameter, FSR 21.2 GHz, air-clad rings used for loss extraction. |

#### WDM (top-level category; subcategories AWG, EG, cascaded MZI, MRR, Bragg/CDC, interleaver, TFF)

Shared WDM fields: `subtype`, `function` (mux/demux/add-drop/interleave), `grid` (DWDM G.694.1 / CWDM G.694.2 / LAN-WDM / custom), `n_channels`, `channel_spacing_nm`/`_ghz`, `center_wavelengths_nm`, `il_db` with `il_point` (channel center / worst-case over passband / worst channel), `il_nonuniformity_db`, `crosstalk_adjacent_db`, `crosstalk_nonadjacent_db`, `crosstalk_cumulative_db`, `bw_1db`, `bw_3db`, `passband_shape` (Gaussian/flat-top), `pdl_db`, `pd_wavelength_shift_nm`, `footprint_um2`, `thermal_drift_pm_per_k`, `tuning_power_mw_per_channel` (and `tuning_scheme`: per-channel/collective/athermal/none), `polarization`.
Subtype fields: AWG/EG `n_arms`, `diffraction_order`, `fsr_nm`; cascaded MZI `n_stages`, `delay_lengths_um`; MRR `n_rings_per_channel` (order), `fsr_nm`, `ring_radius_um`, `drop_il_db`, `through_il_db`; Bragg/CDC `grating_period_nm`, `kappa`; TFF `aoi_deg`, `vendor` (links to supply-chain atlas).
Pitfalls: crosstalk definition (adjacent vs non-adjacent vs cumulative; at center vs over passband); IL at channel center vs worst case over the passband; ring filter values quoted at one detuning; mux vs demux measured direction.

| source | values |
|---|---|
| ofc2026:Th2A.9:p.~1 | Si overlapping AWG, 16 ch at 1.6 nm: IL < 1 dB, adjacent crosstalk < −22 dB, 540 x 590 µm². |
| ofc2026:M1E.2:p.~1 | MZI CWDM at 20 nm spacing: crosstalk < −20 dB, 1-dB BW 16 nm. |
| hulyal2026 p.2-3 | LTOI AWG: 106 GHz spacing, 3-dB BW 85 GHz, 5 dB IL; two cascaded AWGs give crosstalk < −20 dB. |

#### Polarization

Fields: `il_db`, `per_db` (polarization extinction ratio), `pdl_db` (mean/max), `bw_nm`, `sop_tracking_rate`, `control_power_mw`.

| source | values |
|---|---|
| ofc2026:Th3C.5:p.~1 | SiP polarization compensator for ELS: IL 1.9 dB (EC de-embedded), mean PDL 0.77 dB, PER 19 dB. Without compensation the mean PDL is 5.01 dB under 1 kHz SOP scrambling. |
| wang2022a p.1 | TFLN DP-IQ modulator with SSC + PRC: 12 dB IL with PMF. Module level only; the PRC is not separated. |

#### Phase shifters (non-EO)

Fields: `p_pi_mw`, `v_2pi_v`, `il_db`, `length_um`/`footprint_um2`, `rise_us`/`fall_us`, `undercut` (y/n), `holding_power` (non-volatile), `endurance_cycles` (PCM/MEMS).

| source | values |
|---|---|
| ofc2026:M2D.1:p.~1 | Folded TOPS: 2.52 mW/π, 0.4 dB IL, < 1 V for 2π, 245 x 15 µm. |
| liu2026d p.1 | TFLN TO: Pπ 40.4 mW at 488 nm and 150.3 mW at 940 nm. |

#### Photodetectors

Fields: `responsivity_a_per_w` (internal vs fiber-referred), `bias_v`, `wavelength_nm`, `dark_current_na` at bias, `bw3db_ghz`, `capacitance_ff`, `saturation_mw`, `ge_width_nm`, `length_um`, `bw_efficiency_product`, `apd_gain`.

| source | values |
|---|---|
| ofc2026:Th3F.1:p.~1 (IME/NSTIC, 200 mm) | > 100 GHz, > 1.1 A/W, < 25 nA at −2 V; 121.5 GHz·A/W. |
| ofc2026:Th3F.3:p.~1 (imec) | > 110 GHz, 0.9 A/W, ≤ 6 fF at −0.5 V; Ge width 200-600 nm. |
| wu2025 p.8 | Ge PD after BEOL TFLN bonding: 55 nA at −1 V, > 0.8 A/W across the C-band, 47 / 56 GHz at −1 / −2 V. |

#### Lasers / ELS

Fields: `p_out_dbm` with level (chip / fiber-coupled / module at TPL2), `pce_pct`/`wpe_pct`, `threshold_ma`, `smsr_db`, `linewidth_hz` (intrinsic/Lorentzian vs integrated), `rin_db_per_hz`, `per_db`, `n_channels`, `grid`, `temperature_c` + ref, `integration` (heterogeneous / butt / PWB / micro-transfer printed).

| source | values |
|---|---|
| ofc2026:W1B.3:p.~1 | 8-channel SOA-integrated DFB TOSA: 25 dBm fiber-coupled per channel at 25 °C case. Uses a lens-integrated isolator. |
| ofc2026:W3E.1:p.~1 | Cooled TOSA > +25 dBm per channel; quotes the OIF class definitions. |
| ofc2026:W4E.2:p.~1 | O-band PCSEL: > 500 mW, 20% WPE, 82 kHz linewidth; 2x2 array at 2.0 ± 0.09 nm spacing. |
| blog:2025/OIF-ELSFP-02.0-1.pdf p.38 Table 6 | Power per λ per core at TPL2, ±1.5 dB: LP 11, MP 14, HP 17, VHP 20, UHP 23, SHP 26 dBm. p.35: RIN, back-reflection tolerance and SMSR are set per application. p.36: PER defined at the MT ferrule. |

#### Amplifiers (SOA / Er)

Fields: `gain_db` at stated input and current, `psat_in_dbm`/`psat_out_dbm` (1-dB), `nf_db`, `bw_nm`, `pdg_db`, `current_ma`, `temperature_c`, link penalty.

| source | values |
|---|---|
| ofc2026:M1B.1:p.~1-2 | QD-SOA: 1-dB Psat 6 dBm (input) / 19.5 dBm (output); NF 5.5 dB (estimated); link penalty 2.0 dB at 8λ x 400 GHz. |
| porto2026 p.2 | InP Tx: SOA gain vs input power with 1-/3-dB compression, at 60 °C (figure only). |

#### Isolators / circulators

Fields: `isolation_db`, `il_db`, `fom` (= isolation/IL), `bw_nm`, `magnet` (y/n), `mechanism`, `power_handling`.

| source | values |
|---|---|
| blog:2025/conradi_hauke - Nonreciprocity... p.4 | Polymer PIC with integrated Faraday rotator: isolator loss < 1 dB, isolation > 40 dB; circulators 4-8 dB loss, 9-18 dB isolation. |
| same source, p.29 | FOM definition: isolation/IL. Its reference [56] gives a free-space isolator at 0.22 dB / 43 dB, FOM 195. |

#### Waveguide platform

Fields: `prop_loss_db_per_cm` (or dB/m), `wavelength_nm`, `polarization`, `width_nm`, `mode` (SM/MM), `method` (cutback / ring intrinsic Q / OFDR), `bend_loss_db_per_90` or `_per_cm`, `min_bend_radius_um`, `transition_loss_db` (Si-SiN, etc.).

| source | values |
|---|---|
| ofc2026:Tu2D.3:p.~1 | Si strip 1.2, SiN 0.4, Si rib 0.7 dB/cm (O-band); Si-SiN transition < 0.1 dB. |
| ofc2026:W2A.4:p.~1 | 800 nm Si3N4, TE and TM, ring-extracted: < 2 dB/m (MM), < 15 dB/m (SM). |
| ofc2026:Th1D.7:p.~1 | Ge-silica: 0.08 dB/m at 1064 nm, sub-dB/m from violet to telecom. |
| ofc2026:Th1D.3:p.~1 | Glass: 0.04 dB/cm propagation, 0.01 dB/cm bend (estimated). |
| blog:2025/UV integrated photonics in sputter deposited aluminum oxide p.1 | Polycrystalline Al2O3: 1.3 dB/cm at 369 nm, TM. |
| li2022b p.1 | TFLN: 2.2 dB/mm at 532 nm. |
| didier2026 p.4 | TFLN on sapphire: 1 dB/cm at 3.7 µm to 5.3 dB/cm at 4.5 µm (cutback with mid-IR GCs). |
| berman2026 p.1 | BTO: about 0.5 dB/cm. |
| li2025b p.6 | Suspended GaAs: 5.5 dB/cm, from loaded Q. |

#### Free-space emitter (AMO)

Proposed fields, none observed in the corpus: `beam_waist_um`, `focus_height_um`, `emission_angle_deg`, `efficiency_to_target_pct`, `crosstalk_to_neighbor_db`, `polarization_purity_db`, `wavelength_nm` (UV/visible), `platform`.

- The only nearby local data are metasurface **modulators**: fukui2025 p.2 (Q 102, IL 0.56 dB) and sun2026a p.2. They belong in the EO atlas, not here.

## 3. Schema recommendation

**Recommended: one generic `components.csv` plus a long-format `component_metrics.csv`, with a per-class parameter registry (YAML) and generated per-class wide views.**

| option | pro | con |
|---|---|---|
| per-class wide tables (like EO `devices.csv`) | Column-level validation; easy human audit; the EO atlas proves it works for one class | About 18 classes means about 18 tables with drifting shared columns. Spectral lists like li2026aa (8 wavelengths) need 8 rows that repeat geometry. New classes need a schema change. |
| **generic + long metrics (recommended)** | One schema across classes. Conditions (λ, polarization, mode, T, bias) live per metric, so spectra and wafer statistics fit naturally. Already proven at scale by the packaging atlas `metrics.csv` (7,511 rows; category `optical` has 199). Cross-class views are trivial (all loss items in a link budget). | Validation moves to a registry; human audit needs a pivot view. |

Registry (`data/schema/component_parameters.yaml`), one entry per parameter per class: `parameter`, `unit`, `class`, `required_conditions` (e.g. `wavelength_nm` for loss), `allowed_scope` (enum §2.3), `allowed_basis`, `sign` (stored positive), `definition` (e.g. "bw_1db_nm: full width where transmission ≥ peak −1 dB"). The validator enforces unit, conditions and scope. `scripts/build_views.py` pivots to wide tables per class for the app.

Tables and links:

```
papers (shared paper_id scheme with EO + packaging atlases; access, license, redistribution)
  |-- paper_authors -> people            (reuse EO build_people.py)
  |-- author_affiliations -> organizations (ROR-keyed; org_type adds wafer_supplier, foundry, facility)
  |                         -> org_sites
components (component_id, paper_id, class, subtype, label, physical_component_id,
            platform_id, process_id, host_device_id -> EO devices.device_id,
            pkg_oi_id -> packaging optical_interfaces.oi_id, test_structure, tags, notes)
  |-- component_metrics (metric_id, component_id, parameter, value, value_text, unit,
  |                      wavelength_nm, band, polarization, mode, temperature_c, temperature_ref,
  |                      bias_v, condition, scope, includes, excludes, statistic, n_samples,
  |                      method, basis, source, locator, qualifiers, notes)
  |-- component_geometry (long: parameter/value/unit/basis/locator; e.g. tip_width_nm, period_nm)
platforms (platform_id, core_material, core_thickness_nm, cladding, substrate, wafer_supplier -> organizations)
processes (process_id, foundry -> organizations, process_name/PDK, node, wafer_size_mm, layer stack, public PDK y/n)
fibers (fiber_id, type e.g. SMF-28 Ultra / UHNA7 / PMF / 7-core MCF / 50 µm MMF, mfd_um at λ, source)
evidence/<paper_id>.yaml (same as EO: field, value, locator, basis, note)
```

- Examples of `process_id` values: TSMC SiPh (ofc2026:Tu2J.2), Samsung Foundry 300 mm (ofc2026:Tu2D.3), AMF (singer2025 p.5), IME/NSTIC 200 mm (ofc2026:Th3F.1), imec (ofc2026:Th3F.3, W2A.9), Tower and Applied Nanotools (ofc2026:W4B.1).
- Carry over the EO conventions unchanged: (b) qualifiers, (e) organization names, (i) locators, (l) bands, (n)/(gg) identity and licence, (y) source defects, (z) statistic.
- Add a row-granularity rule: one component row per physical design; operating points are metric conditions, not new rows.

## 4. Corpus yield (candidate counts, regex-based, not verified)

- **EO OA** = `access` in {open_access, arxiv}.
- **lic-ok** = `redistribution: open_license_ok`.
- **OFC title n** = titles whose primary topic matches the class, a separate signal from the regex.
- OFC is entirely non-OA. The packaging atlas has no access column; it is mostly IEEE (treat as not OA).

| class | EO n (of 231) | EO OA | EO lic-ok | EO top 5 (access) | pkg n | OFC regex n (of 677) | OFC title n | OFC top 5 |
|---|---|---|---|---|---|---|---|---|
| grating_coupler | 34 | 25 | 10 | falcone2026 (arxiv, lic-ok); didier2026 (OA, lic-ok); hu2026 (arxiv, lic-ok); luan2026a (arxiv); he2019 (arxiv) | 2 | 17 | 3 | W1A.1; W1A.3; M1E.1; M1G.2; M2B.2 (dedicated: Tu2J.2, W4B.5, W4B.6) |
| edge_coupler | 25 | 22 | 11 | huang2026a (arxiv); pan2021 (OA); rahman2025 (arxiv); li2024 (paywalled); li2026 (arxiv, lic-ok) | 1 | 3 | 4 | Th2A.1; Th1H.2; Th3C.3 (dedicated: Tu2J.5) |
| pwb_microoptics | 8 | 6 | 2 | singer2025 (OA); taghavi2026 (arxiv, lic-ok); ummethala2021 (arxiv); kholeif2026 (unknown); wolf2018a (arxiv) | 4 | 8 | 7 | Th2A.10; W4B.2; W2A.23; W4B.1; W1B.4 |
| fiber_array / fan-out | 3 | 3 | 3 | geravand2025; axline2026; wu2022 (all arxiv, lic-ok) | 5 | 11 | 20 | Th2A.8; M2D.6; M4B.2; W4B.2; M2D.2 |
| free_space_amo | 9 | 8 | 5 | sun2026a (arxiv); fukui2025 (arxiv, lic-ok); prountzou2026 (arxiv, lic-ok); karakida2026 (unknown); soma2025 (arxiv) | 0 | 4 | 0 | M1G.5; Th2A.8; W2A.23; W1B.5 |
| mmi | 16 | 15 | 6 | schwarzenberger2026 (OA); li2022b (OA); lin2026a (arxiv, lic-ok); schwarzenberger2026a (unknown); ummethala2021 (arxiv) | 0 | 4 | 13 (splitters total) | W2A.8; M2D.1; Th2A.4; Th1H.4 |
| directional_coupler | 13 | 13 | 5 | nelan2022 (arxiv); larocque2024 (arxiv, lic-ok); thiele2022 (arxiv); weigel2018 (OA); bankwitz2026 (arxiv, lic-ok) | 0 | 4 | (above) | W2A.9; M1D.3; M2D.2; W2A.4 |
| y_branch | 10 | 10 | 6 | li2025b; cai2025 (arxiv, lic-ok); lee2026; anjali2025 (arxiv); larocque2024 (arxiv, lic-ok) | 0 | 1 | 0 | W3E.2 |
| crossing | 2 | 2 | 1 | nelan2022 (false positive); larocque2024 (arxiv, lic-ok) | 0 | 4 | 0 | W2A.3; W4K.3; M2D.2; M4F.1 |
| ring_filter | 28 | 24 | 9 | berman2026 (arxiv, lic-ok); feng2022 (arxiv, lic-ok); churaev2023 (OA, lic-ok); kim2025 (arxiv); montifiore2026 (arxiv, lic-ok) | 0 | 6 | 7 | M2A.1; W1A.3; M4F.5; Th1D.7; Th2A.14 |
| wdm (all subtypes; MRR-filter papers in ring_filter row still to be split into wdm.mrr) | 4 | 1 | 0 | zhou2026, hulyal2026, kholeif2026 (unknown); holzgrafe2020 (arxiv) | 0 | 16 | 13 | Th2A.9; M3F.2; Th1C.3; M3F.3; M1E.2 |
| pbs_psr | 6 | 4 | 2 | wang2022a, geravand2025 (arxiv, lic-ok); gupta2023 (paywalled); park2026 (arxiv); starnault2026 (unknown) | 2 | 9 | 3 | W3E.1; M1K.3; Th1K.2; Tu2K.6; M2D.6 (dedicated: Th3C.5) |
| phase_shifter (TO/MEMS/PCM) | 14 | 10 | 5 | huang2026a (arxiv); liu2026d (OA, lic-ok); didier2026 (OA, lic-ok); geravand2025, hu2026 (arxiv, lic-ok) | 0 | 7 | 27 (incl. switches) | M2D.1; M2A.3; M1E.3; M4D.2; M2B.5 |
| photodetector | 10 | 8 | 3 | steckler2025 (OA); wu2025 (arxiv); boynton2020 (OA); li2026aa (OA); schwarzenberger2026a (unknown) | 2 | 15 | 15 | Th3F.3; W3E.7; Th2A.15; Th3F.1; Th3F.2 |
| laser | 15 | 7 | 4 | li2024 (paywalled); porto2026 (unknown); shen2026 (unknown); singer2025 (OA); schwarzenberger2026a (unknown) | 0 | 46 | 45 | Th1H.1; Th1K.2; W2A.11; W4D.6; M1E.6 (dedicated CPO ELS: W1B.3, W3E.1, W4E.2) |
| soa | 3 | 0 | 0 | porto2026; aihara2026; tiberi2026 (all unknown) | 0 | 19 | 30 (incl. fiber amplifiers) | M1B.1; Th1C.4; Th3E.1; Tu2E.4; Th2A.37 |
| isolator | 0 | 0 | 0 | none | 0 | 0 | 1 (Th2A.20, fiber EDFA) | none |
| waveguide_platform | 65 | 56 | 23 | lin2026b (arxiv); shen2024 (arxiv, lic-ok); zhang2026b (unknown); schwarzenberger2026a (unknown); ulrich2025 (arxiv) | 5 | 21 | 31 | W1A.3; Th1D.1; M1E.1; M2D.1; M4D.5 |

Takeaways:
- Coupler and platform-loss rows can be seeded from the EO cache now. Most of them are side data from loss budgets and are OA, about half lic-ok.
- Dedicated component papers (AWG, ELS, PD, microlens, GC) are mostly OFC, which is non-OA.
- Packaging `optical_interfaces.csv` (55 rows: edge 22, evanescent 7, grating 6, adiabatic 5, mirror 5, lens 3, other 5, unspecified 2) can be imported via the `pkg_oi_id` crosswalk. Its `scope` is free text in 51 of 55 rows, which is the reason to enum it here.
- Blog PDFs add: the ELSFP IA (laser module classes), UV Al2O3 (UV platform), AstroPIC (GC + MLA, astro), and the Conradi thesis (isolators).

## 5. Gaps and seed references

Poorly covered (fewer than 3 quantitative sources across all local corpora, or only non-OA OFC):
- **isolators/circulators**: 0 integrated sources; only the blog thesis.
- **free-space AMO emitters**: 0.
- **MEMS and PCM phase shifters**: 0 with numbers.
- **crossings**: 1, ofc2026:W2A.3.
- **PSR/PBS**: 1 dedicated (Th3C.5).
- **Y-branch**: 1, li2025b.
- **2D/bottom-reflector GC**: OFC only.
- **SOA, AWG/echelle, lasers**: OFC only, non-OA.
- **Er waveguide amplifiers**: reference mentions only.
- **SNSPD/SPAD**: mentions only.
- **PWB loss**: never isolated; singer2025 puts it in an appendix.

The seeds below were found in local reference lists, with the locator where seen. "Journal OA" is general knowledge about the venue and must be checked per article.

| class | title | venue, year | DOI / arXiv (verified in local text) | seen in |
|---|---|---|---|---|
| couplers (review) | Coupling strategies for silicon photonics integrated chips [Invited] | Photonics Research 7(2) 201-239, 2019 | 10.1364/PRJ.7.000201 | pkg:ectc51687.2025.00014 refs; blog Heterogeneous_Integration_in_CPO refs |
| edge coupler (review) | Edge couplers in silicon photonic integrated circuits: a review | Applied Sciences 10(4) 1538, 2020 | 10.3390/app10041538 | ofc2026:Tu2D.4 ref [5]; valdez2023 ref 40 |
| couplers (review) | High-efficiency broadband light coupling between optical fibers and photonic integrated circuits | Nanophotonics 7(12) 1845-1864, 2018 | 10.1515/nanoph-2018-0075 | pkg:ectc51846.2026.00302 ref [1] |
| GC benchmark | C- and O-band dual-polarization fiber-to-chip grating couplers for silicon nitride photonics | ACS Photonics 10, 3366-3373, 2023 | to verify | kohli2025 ref 56 |
| GC benchmark | High efficiency apodized grating coupler for SOI waveguides | Opt. Express 18, 18996-19003, 2010 | to verify | ofc2026:Tu2D.5 ref [5] |
| GC benchmark | Ultra-efficient CMOS fiber-to-chip grating couplers | OFC 2016, Th4A.3 | n/a | ofc2026:Tu2D.5 ref [6] |
| PWB | Photonic wire bonding: a novel concept for chip-scale interconnects | Opt. Express 20(16) 17667, 2012 | 10.1364/OE.20.017667 | yeh2026 ref (20) |
| PWB | Hybrid integration of silicon photonics circuits and InP lasers by photonic wire bonding | Optica 5(7) 876-883, 2018 | to verify | singer2025 ref 73 |
| AMO emitter | Integrated optical addressing of an ion qubit | Nat. Nanotechnol. 11, 1066-1070, 2016 | to verify | celik2022 ref 16; eltes2020 ref 10 |
| AMO emitter | Integrated optical multi-ion quantum logic | Nature 586, 533-537, 2020 | 10.1038/s41586-020-2823-6 | lin2026a ref [2]; UV Al2O3 blog ref 5 |
| AMO emitter | Integrated multi-wavelength control of an ion qubit | Nature 586, 538-542, 2020 | to verify | mao2024 ref 50 |
| AMO emitter | Multi-site integrated optical addressing of trapped ions | Nat. Commun. 15, 3709, 2024 | 10.1038/s41467-024-47882-5 | lin2026a ref [3] |
| visible/UV platform | Visible-light silicon nitride waveguide devices and implantable neurophotonic probes on thinned 200 mm silicon wafers | Opt. Express 27, 37400, 2019 | 10.1364/OE.27.037400 | ofc2026:Th1D.2 ref [2] |
| visible/UV platform | CMOS-foundry-based blue and violet photonics | Optica 8, 755-756, 2021 | to verify | powell2024 ref 27; UV Al2O3 blog ref 8 |
| visible platform + lasers | Extending the spectrum of fully integrated photonics to submicrometre wavelengths | Nature 610, 54-60, 2022 | 10.1038/s41586-022-05119-9 | lotkov2024 ref 1 |
| quantum (roadmap) | 2022 Roadmap on integrated quantum photonics | J. Phys. Photonics 4, 012501, 2022 | 10.1088/2515-7647/ac1ef4; arXiv:2102.03323 | ofc2026:Th1D.2 ref [1]; renaud2023 ref 7 |
| isolator | On-chip optical isolation in monolithically integrated non-reciprocal optical resonators | Nat. Photonics 5(12) 758-762, 2011 | 10.1038/nphoton.2011.270 | blog conradi thesis ref [60] |
| isolator | Electrically driven and thermally tunable integrated optical isolators for silicon photonics | IEEE JSTQE 22(6) 271-278, 2016 | 10.1109/JSTQE.2016.2588778 | ofc2026:Th2A.10 ref 4 |
| TO phase shifter | Efficient, compact and low loss thermo-optic phase shifter in silicon | Opt. Express 22, 2014 | to verify (pages conflict: 10487-10493 in datta2020 ref 32 vs 83-85 in eltes2020 ref 16) | datta2020; eltes2020 |
| MEMS | Silicon photonic MEMS switches based on split waveguide crossings | Nat. Commun. 16, 331, 2025 | to verify | akazawa2026 ref [15] |
| PCM | A new family of ultralow loss reversible phase-change materials for photonic integrated circuits: Sb2S3 and Sb2Se3 | Adv. Funct. Mater. 30, 2020 | to verify | taki2024 ref 24 |
| crossing | Design and resonator-assisted characterization of high-performance lithium niobate waveguide crossings | Opt. Lett. 48(9) 2218, 2023 | to verify | chen2024 ref 44; xie2024 ref 54 |
| SWG devices (review) | Subwavelength integrated photonics | Nature 560, 565-572, 2018 | to verify | zhang2023 ref 38; ofc2026:M2D.5 ref [7] |
| ring (review) | Silicon microring resonators | Laser Photonics Rev. 6, 47-73, 2012 | to verify | hsu2024 ref 2; lee2020 ref 22 |
| high-Q SiN | 422 million intrinsic quality factor planar integrated all-waveguide resonator with sub-MHz linewidth | Nat. Commun. 12, 934, 2021 | to verify | kohli2025 ref 24; montifiore2026 ref 23 |
| SiN platform (review) | Silicon nitride in silicon photonics | Proc. IEEE 106(12) 2209-2231, 2018 | to verify | boynton2020 ref 20; niels2025a ref 3 |
| TFLN platform (review) | Integrated photonics on thin-film lithium niobate | Adv. Opt. Photon. 13(2) 242-352, 2021 | 10.1364/AOP.411024 | khalil2026 ref 51 |
| Si platform (review) | Review of silicon photonics technology and platform development | J. Lightwave Technol. 39(13) 4374-4389, 2021 | 10.1109/JLT.2021.3066203 | schwarzenberger2026 refs |
| Si roadmap | Roadmapping the next generation of silicon photonics | Nat. Commun. 15, 751, 2024 | 10.1038/s41467-024-44750-0 | chiang2025 ref [1] |
| lasers (review) | Recent progress in lasers on silicon | Nat. Photonics 4, 511-517, 2010 | to verify | blog Thomson2016 ref [15]; wolf2018a ref 64 |
| lasers (review) | Heterogeneous silicon photonic integrated circuits | J. Lightwave Technol., 2015/2016 | to verify (cited as early access) | blog Heidel2016 ref [25] |
| Er amplifier | A photonic integrated circuit-based erbium-doped amplifier | Science 376, 1309-1313, 2022 | 10.1126/science.abo2631 | ofc2026:Th2A.21 ref [13] |

Not found in any local reference list, all to verify: an MMI self-imaging theory paper, a compact Si Y-junction benchmark, a silicon polarization-management review, a Ge-on-Si PD review, an AWG/echelle review, and SOI crossing benchmarks.

## 6. Open decisions for the build

1. Confirm the long-format metrics + registry design (§3) or prefer per-class wide tables.
2. Should OFC 2026 rows be admitted as facts-only rows (locator `ofc2026:<code>:p.~N`, no redistributed text/figures)? If yes, the approximate page locator needs a rule, e.g. verify against the NAS PDF later.
3. Should EO-atlas side data (coupler, MMI and platform loss from modulator papers) be back-filled via `host_device_id` in the first tranche? It is the largest OA yield (§4).
