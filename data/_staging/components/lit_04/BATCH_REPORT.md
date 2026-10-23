# Batch lit_04 report (distill subagent, 2026-10-22, transcribed by the coordinator)

Dry-run `batch lit_04: +42 components, +199 metrics; errors 0`. host_device_ids empty everywhere. djogo2026 and
yue2026 open_license_ok (no quotes used beyond a few words).

## Per paper

- sulway2023 (3 / 13): NTFC fiber_chip_coupler.other (soi, fab AMF): per-coupler 0.48 dB best at 2003 nm, 0.63 dB
  mean 2000-2080 nm (cutback intercept minus splices / 2, derived); fitted 1-dB 295 nm, 3-dB 511 nm; simulated with
  struts 1.69 dB; geometry w_t 200 nm, w_s 700 nm, L_c 30 um, Si 220 nm, BOX 3 um. No-strut design < 0.07 dB
  (simulated). Nanofiber taper + splice fiber_interface.other 0.07 / 0.09 dB measured (wavelength inferred). Not
  entered: "flat within +/-0.968 um" (not a 1-dB tolerance), 3 deg pitch from chip plane, Table II SiN/LN designs.
  Authors' own post-processing org ambiguous (Bristol / Waseda / NTT): only AMF entered.
- zhang2021 (9 / 51): buried 3D poly-Si SSC as waveguide_platform.transition (on-chip only, no fiber coupling
  shown): six length siblings 50-300 um, 0.56/0.64/0.77/0.89/1.01/1.19 dB per SSC (cutback, measured, +/- in
  condition), geometry each. Lossless-fill concept design row > 99 % TE/TM simulated. Poly-Si thick WG 37.7 dB/cm,
  thin Si rib 4.4 dB/cm (from dB/mm, derived). Not entered: ~0.2 dB fabrication-only loss (rests on simulated poly
  loss), 3.34 dB/mm material loss (assumed), C-band variation < +/-0.1 dB. Fab Southampton borderline (D84a in-house
  CMP / own flow).
- jia2017 (2 / 20): suspended oxide SSC fiber_chip_coupler.edge (fab A*STAR IME "our MPW platform"): Table I 1550 nm
  TE 0.95 dB best, 0.95-1.3 dB over 5 chips, TM 1.3-1.4 dB; MO4 oil < 1.5 dB over band; n = 1.424 oil < 1.5 dB;
  abstract < 1.3 dB; PDL < 0.5 dB (abstract), < 0.2 dB on 4/5 chips; 1-dB tolerance > 2 um lateral, > 40 um
  longitudinal; simulated < 1 dB; tip ~105 nm measured / 90 nm target; cladding 3.7 um measured; overlay width 10 um
  (model); sidewall 72 deg. Si WG 1.8 dB/cm TE, 0.9 TM (best). Not entered: 0.4 dB cross-wafer uniformity, 0.5 dB
  packaging variation, modelled scattering < 0.1 dB/facet.
- djogo2026 (10 / 36): packaged C-1 interposer fiber_interface.fan_out (glass): 2.75 dB mean at 1550 nm (MCF probe
  subtracted, derived); single pass at 1505 nm 4.98 packaged / 4.65 pre-curing / 3.2 best (author_estimate: rest on
  ~3 dB polarization and ~2 dB probe terms); 40 channels, 38.5 um pitch. Prototypes A-3 / B-2 / C-1 measured fan-out
  and full-circuit means plus simulated Table II. Laser-written WG four depths 0.20-0.71 dB/cm author_estimate
  (calculated 0.3 dB/end coupling). S-bends 0.5 / 0.4 dB. 80 deg crossing <= 0.01 dB, crosstalk > 40 dB (noise
  floor). SiP GC loop 4.9 dB fiber-to-fiber, 2.45 dB loopback half (derived), 48 nm loop 3-dB width near 1504 nm.
  Chiral MCF fanout 1.0 dB (origin not stated). Cited, not entered: TIR mirror 0.4-0.8 dB [24], socket < 0.2 dB
  [25], MCF misalignment < 0.2 dB [25]. Not entered: 6 unfabricated Table II mappings, channel spectra 2.9-4.0 dB,
  two-pass 3.0 / 3.2 dB. fab empty (passive wording; D80b).
- shikama2017 (1 / 6): FI/FO 6-mode 19-core fiber_interface.fan_out, fab org_ntt ("we fabricated"): LP01 < 0.6 dB
  all cores, core-to-core nonuniformity < 0.5 dB, crosstalk > 60 dB, return loss > 45 dB, 19 channels, 43.4 um pitch
  (fiber spec). Not entered: MDL < 2 dB / < 1.7 dB (gap), modal crosstalk Tables II/III (include MPLC).
- yue2026 (1 / 4): cladding-free LT OPA free_space_emitter.other (ltoi_rib, fab SIMIT via contributions): emission
  angle 15 deg at 1520 nm, 6 deg at 1620 nm; LT 600 nm, BOX 4.7 um. Not entered: far field 2.6 x 1.6 deg (unclear
  which OPA), SLSR > 8 dB over 4 h, 40 deg steering, -0.09 deg/nm, 16 channels, V_pi 4.4 V (EO). Cladded LT OPA and
  LN control OPA not rows (no fitting metric).
- mehta2016 (3 / 21): focusing grating emitter 674 nm (sin): waist 1.8 um at 42 um, 2.0 um at 50 um, 2.0 um from Rabi
  scan; efficiency 32 % simulated; as-fabricated loss 8-9 dB author_estimate; angle ~-38 deg simulated; period
  290-310 nm; fill 0.1-0.4 (paper's duty = gap fraction, noted); 18 x 18 um. Input GC 10 dB simulated, 30 um beam,
  -37 deg. PECVD SiN WG 6 dB/cm measured. Not entered: crosstalk errors, polarization purity, bends 3 dB total,
  16-17 dB residual. fab/facility empty (MIT MTL / NSL staff thanks only).
- prost2022 (2 / 6): 32-ch Si/SiN OPA free_space_emitter.other (si_sin_multilayer): FWHM 0.97 x 0.58 deg measured,
  0.98 x 0.29 theoretical, aperture 480 um. TO PS P_pi 30 mW measured. Not entered: SLSR 11 dB, +/-19.2 deg,
  channels / pitch (not allowed), PATD PD (cited [14]). fab empty (imec authors, no statement; D80b).
- kim2019 (6 / 25): OPAs 32 el ~0.15 x 0.6 deg, 125 el 0.15 x 0.25 deg. L-shaped TO PS P_pi 20 mW simulated, ~270
  ohm measured, tau 4.94 us, 32.3 kHz derived (single pole), simulated loss 0.016 dB, 32 um, 0.35 um gap, 110 nm
  slab. DC 0.015-0.02 dB simulated. Edge coupler ~3 dB, Si WG 3 dB/cm (origin not stated). Not entered: SLSR 8.5 dB,
  steering 16 x 18.5 deg, 2.25 dB uniformity, 20 mW/element, -9 dB theoretical emission, Fig. 14 splitter tree.
  fab empty.
- wilson2019 (5 / 17): GaP strip WG (platform other) ~1.2 dB/cm best from Q (ring_extraction, derived), n_g 3.8
  (derived, Supp.), 300 x 500 nm on 2 um oxide. Uncladded R = 50 um ring Q_loaded 2.5e5 best, 0.7-2.5e5 range, FSR
  250 GHz. Kerr comb laser.comb P_th ~3 mW at 1560 nm. Cladded racetrack 670 MHz, Q 3e5, FSR 100 GHz. Raman
  laser.other P_th 100 mW (from 20 dBm, derived). fab IBM Research Zurich, facility BRNC. Not entered: n2, gamma,
  Raman 10 % (undefined), 1.4 THz comb envelope, GCs (no numbers).

## Orgs missing from the registry

- Chiral Photonics (djogo2026 p.2 Sec. II, p.5 Sec. III; vendor of MCF and fanout).
- SIMIT material-device and characterization platform; ShanghaiTech Material and Device Lab (SMDL) (yue2026 p.16
  ack; facilities for sample fabrication; facility_org_ids empty for now).
- Colleges of Nanoscale Science and Engineering, Albany (kim2019 p.1; possibly alias of org_suny_polytechnic_institute);
  Berkeley Wireless Research Center (kim2019 p.12; not a fab facility).

## Judgment calls

org_ntt for 2017 "NTT Corporation" (registry also has renamed org_nippon_telegraph_and_telephone); fiber-only parts
platform empty; zhang2021 SSC as waveguide_platform.transition; jia2017 platform silica (D82f); mehta2016 input
coupler and OPAs as free_space_emitter.other; wilson2019 comb / Raman as laser.* rows; djogo2026 single-pass
author_estimate; sulway2023 per-coupler derived; djogo2026 fan-out section per_component, full circuit device_total.

## Registry gaps (proposed)

mdl_db (fiber_interface, mode_converter); free_space_emitter: slsr_db, n_channels, pitch_um, steering_range_deg,
steering_efficiency_deg_per_nm; platform enum gap_on_insulator (or iii_v_on_insulator); raman conversion efficiency
(low priority); taper-interface tolerance at non-1-dB levels (deferred per D81).
