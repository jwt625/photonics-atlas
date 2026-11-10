# lit_120 batch report (2026-11-09)

All seven cached texts match their source rows on page 1 (nie2019 has a different title wording, see below); none is
a correction, an erratum or another paper. song2024 is flagged `garbled_text_layer`, but only p.10 (references) is
garbled. Every value used comes from the clean body pages (p.1-9), and the figures were checked on the page renders.
Figure values were read from the cached `page_NN.png` / `img_*.png` renders. Dry-run: +25 components, +272 metrics,
0 errors. The one warning (ni2025b m18 / m4) is on an existing merged row, not from this batch.

| paper | components | metrics |
|---|---|---|
| cui2023a | 1 (resonator.ring) | 18 |
| karunakaran2024 | 3 (resonator.ring; laser.comb; fiber_chip_coupler.edge) | 16 |
| lin2023 | 6 (splitter.mmi, one per design split ratio 50:50 ... 5:95) | 96 |
| song2024 | 1 (splitter.y_branch) | 17 |
| nie2019 | 3 (wdm.bragg_cdc 2: 16-stage cascade, single-stage length series; waveguide_platform.other 1: mode-transition taper) | 18 |
| hu2020 | 7 (wdm.bragg_cdc 6: periods 370 / 374 / 378 / 382 nm, 376 nm filter twin, apodized design; switch_fabric.other 1) | 66 |
| xu2023b | 4 (switch_fabric.other; splitter.mmi; resonator.ring; fiber_chip_coupler.grating) | 41 |

No paper has 0 rows.

## Fab / facility orgs

- cui2023a: fab `org_ligentec` (p.3 Sec. 2: fabricated by the MPW foundry LIGENTEC, Switzerland, with the standard
  LIGENTEC-AN800 technology; p.5). `process_name` "LIGENTEC-AN800 (MPW)".
- karunakaran2024: fab `org_ligentec` on all 3 rows (p.2 Sec. 2.1: commercial-grade multi-project wafer run at
  LIGENTEC SA using the AN800 process). `process_name` "AN800 (MPW run)". One co-author is at LIGENTEC; that
  affiliation is not used for fab.
- song2024: fab `org_ligentec` (p.6 Sec. 3: fabricated on the 800 nm silicon nitride platform "Ligentec AN800 MPW").
  `process_name` "Ligentec AN800 MPW".
- xu2023b: fab `org_institute_of_microelectronics_chinese_academy_of_sciences` on all 4 rows (p.2 Sec. 2: fabricated
  with the 180 nm pilot-line at IMECAS). `process_name` "IMECAS 180 nm pilot-line (8-inch)".
- hu2020: fab empty (passive "was fabricated", D80b). Facility
  `org_center_for_advanced_electronic_materials_and_devices` on the 6 fabricated rows (p.9 Acknowledgments: AEMD of
  SJTU thanked for support in device fabrication; D80c). It is not set on the design-only apodized row.
- lin2023: fab empty. p.3 Sec. 3 says the devices were made on a commercial X-cut LNOI wafer (vendor not named) with EBL
  and ICP, and names no org.
- nie2019: fab empty. p.1 states only e-beam lithography prototyping and names no org.
- Missing orgs: none.

## Judgment calls

1. nie2019: the cached text is the accepted manuscript. Its title reads "High rejection ratio on-chip pump rejection
   filter ...", while the source row reads "High extinction ratio on-chip pump-rejection filter ...". The authors and
   content are the same, so I did not stop on it (D430 / D433 precedent). The coordinator may confirm.
2. hu2020: one physical device (period 376 nm) gets two rows under D396: `switch_fabric.other` for the switch
   (D158 / D407) and `wdm.bragg_cdc` for the filter response in both GST states. The four period-series devices were
   measured only with amorphous GST and are filed as `wdm.bragg_cdc`.
   - Three values are stated once for all four devices: about 2.5 dB average through-port loss, 0.5-1.5 dB drop loss
     and about 5 nm 3-dB width. I entered them on each row and noted that (govdeli2025 precedent). D254 would argue for
     notes only.
   - The simulated values (FDTD, L = 200 um, period 374 nm) are on the 374 nm row.
   - Platform `soi_strip`: light is guided in the 220 nm Si strips, and GST is a 50 nm surface grating.
3. karunakaran2024 `q_intrinsic` 2.7e6 (1.97 um) and 1.5e6 (1.55 um) are `measured`. The paper does not describe
   the extraction, but it sets the coupling regime from data: the visibility-vs-gap trend in Fig. 1(b) shows the rings
   over-coupled at 1.97 um and under-coupled at 1.55 um (D403 clause "regime determined from the data"). If the
   auditor reads D403 strictly, these become `author_estimate`. The 0.11 dB/cm loss is `author_estimate`, because the
   group index is not stated (D76).
4. cui2023a `q_intrinsic` and the 0.051 dB/cm loss are `author_estimate`. The paper uses the under-coupled formula
   without showing the regime (D403).
   - `radius_um` 130 approx is the effective Euler-bend radius from Table 1 ("~0.13 mm", `derived`). The racetrack
     has no single radius, and Rmin 63 um is in `min_bend_radius_um`.
   - Two `width_nm` rows, 1.5 um (bends) and 7 um (straights), each with its role in the condition.
5. lin2023:
   - Split ratios are read off Fig. 3(a), measured curve, +/- 1 percentage point: 50 / 43 / 29.5 / 20.5 / 10 / 6.5 %
     at Output1.
   - The "< 0.3 dB IL" stated for all fabricated devices is entered as `excess_loss_db` lt 0.3 on each row (the
     paper's IL is total output power vs input). So are the "< 0.25 dB" simulated value and the "< 3 % PSR
     variation" (`coupling_variation` lt 0.03, derived %->fraction).
6. song2024: Y-branch excess losses are `derived`: the MZI excess loss was halved for two Y-branches (D80a).
   - Imbalances are `derived`: computed from the MZI extinction with Eq. (15). The text prints the TE imbalance as an
     average of "about 0.40 dB", while Table 2 and the conclusion print it as an upper bound; the TM 1.47 dB has the
     same ambiguity (D417 notes).
7. nie2019: the single-stage filters (L = 150-3000 um) are one series row (D165). The paper gives the stop-band
   positions and the about 40 dB saturation for the series. Per-length values exist only in Fig. 3(b), whose curves
   are shifted for visualization, so I did not read them.
   - The simulated -0.15 dB per mode-transition taper became its own `waveguide_platform.other` row (band inferred
     from the 785 nm design).
8. xu2023b:
   - Platform `other` (poly-Si on oxide, not an SOI wafer).
   - Grating-coupler 15.96 dB entered `per_coupler`, method unspecified (the paper says the coupler "has" this
     efficiency, without the arithmetic).
   - MMI 4.19 dB per port is `measured` (cascade fit); the 1.19 dB excess is `derived`.
   - Ring Q_int 9108 and 65.63 dB/cm are `author_estimate` (assumed critical coupling).
   - Power consumption mW -> W is `derived`.
   - Conflicts noted: 8.32 mW / -3.4 V (intro) vs 7.98 mW / -3.35 V (abstract, Sec. 2); IL 5.9 dB vs Table 1 6.3 dB.

## Not entered, and why

cui2023a
- n-w model scattering losses 0.18 / 0.03 / 0.015 dB/cm (1 / 3 / 7 um; assumed roughness): model estimate, scattering
  only (in notes).
- Simulated Euler-bend mode-excitation ratios below -30 dB: no resonator parameter.
- LAT length 150 um (`taper_length_um` not allowed for resonator), MSW length 1000 um, ring length 3720 um: in notes.
- AN800 0.2 dB/cm and the Table 1 values of other works: cited (rule 3).

karunakaran2024
- The three other rings of the gap series (400-600 nm): only the Fig. 1(b) visibilities exist.
- Comb span 422 nm at -20 dB, soliton-step durations 2 us / 1.7 ms, primary-comb spacing 26 FSR: no parameter (comb
  span rejected in D81).
- Calculated GVD window, gamma 0.672 /W/m: no parameter.

lin2023
- Per-device IL spectra (Fig. 4(b), 3D perspective plot): not read reliably.
- Simulated fabrication-tolerance derivatives (0.265 % per 5 nm etch, < 0.15 % per 50 nm Lr, about 0.35 % per
  50 nm Wr): no parameter.
- Wr, Lr (removed-corner size) and Wgap (0.3-0.6 um, per device not stated): in notes.
- The back-to-back grating couplers have no reported values.

song2024
- Minimum output gap 300 nm (a foundry rule, not a coupling gap), leg offset 0.85 um, Lleg / Lext: in notes.
- Simulated thickness / index tolerances: in notes.
- Table 2 values of other works (rule 3).

nie2019
- Stop-band "bandwidth less than 3 nm" (16-stage): no level is stated, so it cannot go into `bw_3db_nm`; no
  stop-band parameter exists for `wdm` (registry gap below).
- The 4 / 8 / 10-stage cascades and the equal-length single stage: Fig. 4(b) only, shifted curves.
- Grating width Wg 320 nm, duty cycle around 50 %, 80 nm grating offset: no `wdm` parameter (`grating_width_um` /
  `fill_factor` are not allowed for wdm); in notes.
- 4.8 dB for 32 tapers: the authors' multiplication of a simulated value.

hu2020
- Corrugation depth 50 nm, GST strip 390 x 100 x 50 nm, 540 GST cells: no wdm parameter, in notes.
- Optical-pulse switching energies 9.5 / 3.2 nJ: calculated from cited pulse energies.
- Ellipsometric GST indices: cited (ref. 15).
- GST grating period on the switch row: `period_nm` is not allowed for switch_fabric (gap below); the value is on the
  filter twin.

xu2023b
- Loss budget (MMIs 2.38 dB + arm 1.12 dB = 3.50 dB): the authors' arithmetic.
- The pi/2 phase shifter (11.7 x 0.8 um) is geometry only and is not a row.
- Arm length 170 um, S_dope 0.8 um, bend radius 50 um: no switch_fabric parameter, in notes.
- The second 0.8 um label in the MMI drawing of Fig. 1(a) cannot be tied to a dimension (D156).

## Registry gaps (proposed)

- `stopband_width_nm` for `wdm` (nie2019 p.4: 16-stage GACDC stop band "less than 3 nm", level not stated; definition
  as for reflector: full stop-band width at the stated contrast level, level in condition). Also usable for CDC
  pump-rejection filters in general.
- `period_nm` for `switch_fabric` (hu2020 p.7: switch grating period 376 nm; definition: grating period of a
  grating-based switch element).
- `fill_factor` / `grating_width_um` for `wdm` (nie2019 p.2: Wg 320 nm, duty around 50 %; Bragg / CDC filter
  geometry).
