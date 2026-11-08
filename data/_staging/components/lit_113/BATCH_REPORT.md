# lit_113 batch report (2026-11-08)

All five cached texts match their source rows (page-1 title). None is a correction, an erratum or another paper; no garbled text layer is flagged. chen2018 is the ACS "Just Accepted" manuscript of the source-row paper (same title, DOI 10.1021/acsphotonics.8b00788); text page 1 is the ACS cover sheet, so the article starts on text page 2. Figure values were read from the cached `page_NN.png` renders and from 300 dpi crops of `source.pdf` (scratchpad only). Dry-run: +29 components, +236 metrics, 0 errors; the one warning (ni2025b m18 / m4) is on an existing merged row, not from this batch.

| paper | components | metrics |
|---|---|---|
| sacher2017 | 10 (waveguide_platform.straight 3; waveguide_platform.transition 3; crossing.multilevel 3, of which 1 design; waveguide_platform.other 1) | 79 |
| ni2025 | 1 (crossing.swg) | 17 |
| chen2018 | 9 (crossing.mmi 8, of which 4 design; fiber_chip_coupler.grating 1) | 63 |
| radosavljevic2017 | 2 (fiber_chip_coupler.grating 2) | 26 |
| jia2014 | 7 (fiber_chip_coupler.edge 7) | 51 |

## Fab / facility orgs

- sacher2017: fab `org_astar_ime` on the 9 fabricated rows (p.4 Sec. 1: platform realized on 8 in SOI substrates fabricated at the A*STAR Institute of Microelectronics). No process name printed.
- jia2014: fab `org_astar_ime` on all 7 rows (p.5 Sec. 3.2: fabricated with the CMOS compatible process of IME Singapore); `process_name` "IME Singapore CMOS compatible process, 248 nm lithography (8-inch wafer)".
- chen2018: fab empty (p.4: fabricated with the commercial 180 nm CMOS process; no foundry named). `process_name` "commercial 180 nm CMOS process" kept as printed (precedent "standard 180-nm CMOS foundry process"); the coordinator may prefer it empty as too generic (Contract v7).
- ni2025: fab empty ("we fabricated", p.8, authors at Nanjing University of Science and Technology and Hebei University; D154).
- radosavljevic2017: fab empty (passive process description only, p.6-7; all authors at the Ghent University - imec Photonics Research Group, no sentence naming the fabricator; D80b).
- No facility acknowledged in any paper. No missing org: `org_astar_ime` is in the registry.

## Not entered, and why

sacher2017
- Misalignment excess loss about 10 mdB (Si-SiN1) and 14 mdB (SiN1-SiN2) at 1550 nm for +/- 60 nm offsets (p.9): an excess term, no parameter (in notes). The total losses with offsets (< 0.14 / < 0.21 dB) are entered.
- Underpass loss "not expected to exceed the overpass loss by more than 1 mdB" (p.11): estimate, not measured.
- Propagation-loss contributions 19-95 mdB to the three-layer transition and 0.5-2.5 mdB per crossing pitch for 1-5 dB/cm (p.6-7): assumed-input estimates.
- Simulated changes with the measured layer thicknesses (Si-SiN1 + < 3 mdB, SiN1-SiN2 - < 6 mdB, overpass - about 0.1 mdB; p.6-7): deltas, not values.
- 100-crossing array < 0.63 dB and the Table 1 values of other works (p.14): projection / cited (rule 3).
- Per-die spectra of Fig. 5(e), 5(f) and Fig. 7(b): bounds already printed in text; no further figure reads.
- Edge couplers: no value printed.

ni2025
- Simulated reflection < -12 dB for TE0-TE2 (p.6): no crossing reflection parameter (registry gap).
- Design sweeps (Figs. 2-4, Fig. 6 tolerances): design-space plots, no device value.
- SWHM duty cycles (fb1 0.7, fb2 0.24, fc 0.7, fa2max 0.72), t2max 180 nm, Lb 2.5 um, minimum feature 60 nm: `fill_factor` is not allowed on crossing (registry gap); in notes.
- On-chip TE GCs and mode MUX / DEMUX: no value printed.
- Table 2 rows of other works (rule 3).

chen2018
- 2D-FDTD "average transmission efficiency above 99.4 % from 1500 to 1600 nm" (p.3): stated in the 3 x 3 design paragraph, superseded by the per-device 3D-FDTD bounds; not entered (it could belong to the 3 x 3 only or to all).
- Fabrication tolerance (Fig. 7: < 0.08 dB change for +/- 50 nm width deviation) and the 18 deg minimum angle: no parameter (notes).
- Fig. 8 curve values other than the printed 10-channel point: design sweep.
- Table I w2-w6 and L2 per crossing: no parameter for stepped taper widths; in notes. L2 is not entered as `mmi_length_um` (the printed total length is: total = 2 x 24 um + L2 for all four devices).

radosavljevic2017
- Fig. 5 / Fig. 7 tolerance maps and their "< 5 %" / "up to 10 %" statements: simulated sensitivities, no parameter.
- Simulated -4 dB / -1.5 dB (abstract): duplicates of the 40 % / 70 % rows; the measured -5 dB / -4 dB abstract values are entered beside the % rows because the -5 dB (32 %) conflicts with the body's 30 %.
- Ge-on-SOI apodization (we,start 1.4 um, we,end 0.5 um) and the 3.2 um Si layer: no parameter (notes).
- Fiber loss 1-2.5 dB/m and the TM fraction: setup corrections (condition).

jia2014
- Mode-mismatch calculations (0.5 dB TE / 0.6 dB TM, PDL 0.1 dB; p.4) and Fig. 2, 3, 5, 9 sweeps: rough design estimates superseded by the BeamProp values (entered).
- 3-dB alignment tolerances (s6: > +/- 3.5 um X and Y; s5: +/- 1.3 / +/- 1.1 um; Si: about 3.5 / 3 um): no 3-dB tolerance parameter (registry gap); in notes. Fig. 8 1-dB widths were not read (the curves are normalized and the 1-dB crossing is not labelled).
- "Smaller than 1 dB/facet if the tip is below 100 nm" and "within 2 dB/facet" with a second intermediate material (p.9): projections.
- SiON tip width 700 nm (Wtip1), cantilever Wc 9 um / Hc 8 um (Si: 7 um), offset = Ltip1: no parameter (notes).

## Judgment calls

1. sacher2017 mdB values: every value printed only in mdB is stored in dB as `derived` (D256); values printed in dB (abstract < 0.15 dB, offset bounds < 0.14 / < 0.21 dB, figure fit labels 0.042 and 0.00024 dB) keep `measured`. Simulated mdB values stay `simulated`.
2. sacher2017 transitions: three rows (Si-SiN1, SiN1-SiN2, and the cascaded Si-SiN1-SiN2 measured as its own trace and stated in the abstract), with cross-notes. Platform `si_sin_multilayer` for the two Si-SiN rows, `sin` for SiN1-SiN2 (huang2026 / fahrenkopf2019 precedent). +/- 60 nm offset bounds are entered as conditions on the same rows (lithographic offsets of the same design, not new designs).
3. sacher2017 crossing: one row per SiN2 width (1.5 um headline, 0.9 um from Fig. 7(c)/(d) only); overpass loss and both crosstalk directions on the same physical-crossing row with the path in `condition`. Per-die upper bounds (90 % confidence) are four rows; die 4 0.28 mdB carries `statistic: best` ("as low as"); the Fig. 7(f) fit slope 0.24 mdB is a separate `measured` row. `gap_nm` 850 nm is derived from the design spacers + SiN1 thickness (not printed as a crossing gap). The no-slab design (Fig. 3(b)) is a `design` row; the Si slab taper (simulated < 54 mdB only) a fabricated `waveguide_platform.other` row (D80e).
4. sacher2017 crosstalk: suppression stored with `ge` (printed "maximum crosstalk -56 dB"); method `reference_structure` (edge-coupler response from a single Si rib waveguide, Eq. (1)).
5. ni2025 conflicts (D417): measured rows follow the p.8 results section (0.14 / 0.08 / 0.20 dB at 2 um, < 1.1 dB and CT < -20 dB over 1950-2050 nm); the abstract "below -25 dB at 2 um" is entered as its own row; p.2 (IL < 0.37 dB, CT < -32 dB "experimental") and Table 2 (Exp IL < 0.2 dB, 2000-2100 nm) are in notes only. Per-crossing values from a 5-crossing cascade kept `measured` (printed average, no arithmetic shown; D167 analogue). Platform `soi` (etch depth of the holes not stated).
6. chen2018: polarization not stated anywhere, left empty. C-band bounds entered with `band: c_band` and no wavelength numbers. `mmi_width_um` = w7 (6 um, the maximum arm width) and `mmi_length_um` = printed total length of the tapered multimode crossing; `taper_length_um` 24 um derived (6 x 4 um). The 10 x 10 point (2D-FDTD, wavelength-averaged) is a design row with `statistic: mean`. Fig. 9 w7 = 2 / 4 um reads are simulated (D454), +/- 0.03 dB.
7. chen2018 GC: about -4.5 dB/facet entered as `per_coupler`, `measured` (D167), C-band inferred.
8. radosavljevic2017 bandwidths: both measured 3-dB widths are `author_estimate` (D435). Ge-on-SOI is printed as "estimated by interpolation" and its data start above half maximum; for Ge-on-Si the data also start above half maximum (about 20 % at 5.18 um vs a 30-32 % peak) and the right half point (about 5.30 um) already gives > 120 nm from the data start, so the printed "about 100 nm" cannot be reproduced from Fig. 4(d). Coordinator may prefer `measured` + approx for Ge-on-Si.
9. radosavljevic2017 measured efficiencies: `loopback_half` (Eq. (2) adds 3 dB for two couplers), method `loopback`, basis `measured` (printed result). Platform `other` (Ge-on-Si, Ge-on-SOI). The Ge-on-Si 30 % (body, conclusion) vs 32 % / -5 dB (abstract) conflict is kept on both rows with notes. Simulated CE `per_coupler`.
10. jia2014: one row per Table 2 structure (6 SiN rows: five comparison structures and the proposed converter) plus the Si converter. Per-facet values `loopback_half` + method `loopback` (propagation loss removed by cutback, facet split not described), basis `measured`. `tip_width_nm` = Si3N4 tip (the HIC tip the paper features); SiON overlay width / thickness in `overlay_width_um` / `overlay_thickness_um`. `mfd_fiber_um` 9.2 um `specification` on the two cleaved-SMF converters (design target fiber). PDL and the Si converter losses have no stated wavelength: `cl_band` inferred from the figure captions; BeamProp values `c_band` inferred.

## Registry gaps (proposed)

- `tol_3db_lateral_um` (fiber_chip_coupler, chip_chip_coupler, micro_optics, fiber_interface): lateral misalignment for 3 dB excess loss (half-width, +/- value). Skipped: jia2014 s6 > +/- 3.5 um X and Y (p.7, Fig. 8), s5 +/- 1.3 / +/- 1.1 um with lensed fiber (p.7), Si converter about 3.5 / 3 um (p.8).
- `back_reflection_db` extended to `crossing`: ni2025 simulated reflection < -12 dB (p.6).
- `fill_factor` extended to `crossing` (SWG / SWHM duty cycles): ni2025 Table 1 f 0.7 / 0.24 / 0.7 / 0.72 (p.6).
- `overlay_tip_width_nm` (fiber_chip_coupler): tip width of the overlay (e.g. SiON) taper at the facet, distinct from the core tip `tip_width_nm`. Skipped: jia2014 Wtip1 700 nm (p.5 Table 1).
- `misalignment_excess_loss_db` (waveguide_platform, chip_chip_coupler): excess loss for a stated lateral offset (offset in condition). Skipped: sacher2017 about 10 / 14 mdB at 1550 nm for +/- 60 nm (p.9). Low priority; the total loss with offset is entered.
