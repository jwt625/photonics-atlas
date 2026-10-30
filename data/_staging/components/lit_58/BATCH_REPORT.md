# Batch lit_58 report (distill subagent, 2026-10-30)

Classes: crossing, fiber_chip_coupler, polarization. Papers: jones2013, streshinsky2013, fukuda2006, huang2013,
vermeulen2010, zhang2013. All six are `restricted_local_only`: facts and locators only, quotes of a few words at most.
Page-1 title and authors match the source rows for all six; none is a correction / erratum; no `garbled_text_layer`.
Rows built by a scratchpad script (one spec for all papers). Dry-run: `batch lit_58: +20 components, +118 metrics;
errors 0` (only the pre-existing WARN on cmp_lit_ni2025b_pimmwc-m18).

## Per paper (components / metric rows)

- jones2013 (7 / 31). Nitride-over-silicon vertical crossing (crossing.multilevel, si_sin_multilayer):
  - gap410 row: measured crosstalk 49.4 TE / 44.3 TM at 1550 nm (port 1, ge); simulated crosstalk 65 / 60 dB; simulated
    per-crossing loss < 0.001 / < 0.05 dB (Si input) and about 1 dB (Si3N4 input, 400 nm); gap 410 nm; Si 400 x 230 nm;
    footprint 0.3 um2.
  - gap305 row: Si3N4-input crossing loss from the 0 / 2 / 4-crossing cutback, read off Fig. 8(b): 2.4 dB TE, 0.8 dB TM
    (extracted_from_figure, +/- 0.1 dB reading; stated measurement error 0.5 dB).
  - gap > 1 um design row: simulated Si-input loss < 0.003 / < 0.03 dB, Si3N4-input < 0.1 dB, crosstalk > 100 dB.
  - Building blocks: 100 um Si-Si3N4 adiabatic transition (simulated < 0.1 dB); loss-budget rows (author_estimate,
    origin not stated): Si strip 1.4 TE / 4.0 TM dB/cm, 5 um bend < 0.1 TE / ~1.5 TM dB per turn, lensed-fiber facet
    ~12 dB.
- streshinsky2013 (1 / 11). Bi-wavelength 2D PSGC (fiber_chip_coupler.grating, soi):
  - IL 7.1 dB at 1576 nm and 8.2 dB at 1296 nm (loopback_half);
  - PDL 1.06 dB at 1550 nm and 5.6 dB at 1310 nm;
  - polarization isolation as crosstalk_db ge 24 / 8.4 dB (derived from PDL, Eq. 3);
  - fiber angle 23 deg; stack 220 nm / 60 nm etch / 2 um BOX / 2.1 um top oxide.
- fukuda2006 (4 / 28):
  - Single-stage DC polarization splitter (polarization.pbs): ER 10 dB cross / 13 dB bar over the C band; 25 dB bar /
    13 dB cross at 1552.52 nm (waveplate method); excess loss < 0.5 dB per port; footprint 112 um2 (7 x 16, derived);
    Si 400 x 200 nm, BOX 3 um.
  - Two-stage splitter: ER 15 dB cross (C band), 23 dB both ports; loss < 0.5 dB.
  - SSC (fiber_chip_coupler.edge): 0.5 dB/facet; 80 nm tip; 3 x 3 um Si-rich oxide core; 7 um overcladding.
  - Si wire: 2.2 TE / 1.7 TM dB/cm cutback; group index 4.2 / 2.8 and DGD ~50 ps/cm (author_estimate).
- huang2013 (3 / 16). HNSW TE-pass polarizers (polarization.other, platform other):
  - S2 (Wp 144 nm, Lp 1 um): IL 2.2 dB mean over 1525-1605 nm and 2.2 dB at 1550 nm; PER > 16 dB.
  - S1 (Wp 71 nm): IL 2.4 dB mean; PER > 16 dB.
  - HNSW active-region waveguide (waveguide_platform.straight): ~0.4 dB/um -> 4000 dB/cm (derived); simulated 6800 dB/cm.
- vermeulen2010 (3 / 18):
  - a-Si overlay GC (fiber_chip_coupler.grating): -1.6 dB at 1530 nm (best, loopback_half); 1 dB / 3 dB bandwidth
    44 / 80 nm; period 690 nm; fill factor 0.35 (tooth fraction, derived from 35 %); fiber angle 13 deg; 220 nm Si +
    160 nm a-Si; etch 230 nm (derived 160 + 70); BOX 2 um; 15 um grating width.
  - Design row for the uniform overlay grating without waveguide etch (h 150 / o 220 nm, ~80 % simulated).
  - 450 x 220 nm strip waveguide 1.8 dB/cm.
- zhang2013 (2 / 14):
  - Index-engineered cascaded-MMI crossing (crossing.mmi): 0.019 dB per crossing at 1550 nm (101 x 101 grid);
    crosstalk > 40 dB over 1530-1600 nm; simulated 0.008 dB; pitch 3.08 um; W_MMI 1.2 um; W 0.6 um; SWN period 200 nm;
    250 nm Si / 3 um BOX.
  - Conventional MMI crossing: 0.14 dB measured, 0.11 dB simulated.

## Values deliberately not entered

- jones2013:
  - simulated Si3N4-input maxima 15 / 3.4 dB at small gaps (p.10; gap not stated);
  - 40 dB crosstalk at 125 nm gap (p.10; design-space statement);
  - Fig. 9 crosstalk points at other gaps and Fig. 10 transition curves (plotted only);
  - conclusion "< 90 dB crosstalk suppression for a 1 um vertical gap" (p.12; contradicts "> 100 dB" for > 1 um);
  - cited values: 2.9 dB/m [29], 0.5 dB SiN taper [30], Bogaerts 0.16 dB / 40 dB [17], Bock < 0.1 dB [7];
  - Si3N4 250 nm x 1.2 um layer dimensions (no second-layer parameter for crossing; kept in core_material).
- streshinsky2013:
  - 1.5-dB windows 35 / 18 nm (no parameter);
  - s/p difference < 1 dB within the windows;
  - simulated 59 % substrate loss;
  - 1D optimum pitch 636 nm / angle 22.5 deg and the theoretical 33 deg. The fabricated lattice pitch is not printed,
    so no period_nm row.
- fukuda2006:
  - DC gap 480 nm, coupling length 10 um, bend radius 3 um (polarization has no gap / coupling-length / bend-radius
    parameters);
  - abstract "about 15 dB for a single coupler" (disagrees with the text);
  - abstract "over 20 dB" for the double coupler (superseded by 23 dB);
  - EME tolerances;
  - 10 Gb/s eye diagrams;
  - intro DGD 6.6 ps for 5 cm of 300 +/- 5 nm cores (a different waveguide, calculation).
- huang2013:
  - coupler taper Lc 1 um (taper_length_um not allowed for polarization);
  - 500 nm access width and the ~10 nm slot (no role parameter);
  - "PER > 16 dB with 1-3 um active length" (spans three devices, D159);
  - Fig. 5(d) points for Lp 2-10 um;
  - simulated PER > 17 dB at 50 nm width and TM cut-off below 210 nm (design-space).
- vermeulen2010:
  - Fig. 4 sweep points;
  - generic 2 um 1-dB alignment sensitivity (p.2, grating couplers in general);
  - cited -1.2 dB [11], 64 % [12], -2.6 dB [10] and ~80 % for case (d) [9] (authors' own earlier work, D259).
- zhang2013:
  - measured transmission 1520-1610 nm / "> 90 nm bandwidth" (no crossing bandwidth parameter, no level stated);
  - Lin / Ls lengths, SWN width 200 nm and trench 50 nm (no role parameter);
  - 1x1 MMI simulations and Table 1 coefficients.

## Fab / facility orgs

- jones2013: fab `org_sandia_national_laboratories`. The text says all fabrication used the CMOS foundry at Sandia's
  MESA facility (p.4 Sec. 2). Sandia's MESA facility is not in the registry. It is the authors' own lab's facility,
  so it is a facility candidate only if such facilities get rows; facility is left empty.
- streshinsky2013: fab `org_astar_ime`. The text says fabrication was performed at IME, A*STAR, in an MPW run through
  the OpSIS foundry service (p.6 Sec. 3). The OpSIS foundry service is missing from the registry. It is the MPW
  access provider, a fab role per D398; already reported in D418.
- fukuda2006: fab `org_ntt`. The text says "we also fabricated" (p.6) and all authors are at NTT Microsystem
  Integration Laboratories (p.1). Pre-2025 NTT papers map to org_ntt (precedent nozaki2016, ono2016).
- huang2013: fab `org_astar_ime`. The text says "we fabricated" (p.5) and all authors are at IME (p.1).
- vermeulen2010: fab `org_imec`, from "complete fabrication process is done in the 200mm imec CMOS pilot line"
  (p.5 Sec. 3).
- zhang2013: fab empty. The fabrication sentence is passive (p.3) and the authors are at UT Austin and Omega Optics.
  No facility is acknowledged.

## Judgment calls

1. jones2013 gap of the crosstalk device: the text prints 410 nm on p.1 / p.12 and 400 nm on p.11 for the same device.
   410 nm is entered as `measured` (ellipsometry, +/- 50 nm), with the inconsistency in the notes (tossoun2024
   precedent). This is not D159: the device identity is clear.
2. jones2013 crosstalk 49.4 / 44.3 dB with qualifier `ge`. The abstract says "exceeding", and p.11 says
   near-noise-floor values may understate the crosstalk. The printed 49.4 dB exceeds the stated 46 dB TE noise floor;
   this source inconsistency is flagged in the notes.
3. jones2013 305 nm-gap wafer as its own row (different gap = sibling design). Its only performance values are the
   Fig. 8(b) data points, so they are `extracted_from_figure`, `cutback`.
4. jones2013 loss-budget terms (p.11) as `author_estimate` rows:
   - the waveguide is not named, but Si is the routing layer (noted);
   - bend loss "per turn" goes in `insertion_loss_db` `per_component`, angle not stated (korcek2023 precedent);
   - the facet row has an empty platform because the facet structure is not described.
5. streshinsky2013 IL as `loopback_half` `measured`: the per-device value is stated, the test cell has two PSGCs and
   the halving is not shown (D167, atsumi2018 precedent). Polarization isolation is a `crosstalk_db` lower bound
   (`ge`, `derived` via Eq. 3) on the GC row. There is no separate polarization.pbs row (precedent wang2022b PSGC =
   single grating row); flag if D396 should apply.
6. fukuda2006 and huang2013 losses normalized to a plain reference waveguide of the same length are
   `insertion_loss_db` `per_component` / `reference_structure` (skill rule 6). lu2015 used `de_embedded` for
   GC-calibrated PBS loss.
7. fukuda2006 waveplate extinction ratios are `statistic: best` (maximum over the waveplate rotation). The two-stage
   23 dB row takes 1552.52 nm from "in the same manner as above".
8. Platform `other` for:
   - fukuda2006 SSC: the facet mode is in a silicon-rich oxide core; no platform value fits; dheer2018 SiON overlay
     used `sion`;
   - huang2013 HNSW devices: Cu / SiO2 / Si hybrid plasmonic, not MIM.
9. huang2013 polarizer class `polarization.other` (bauters2013 TE-pass precedent). The ~0.4 dB/um HNSW loss is
   entered as 4000 dB/cm `derived` (unit conversion, D256) on a separate waveguide row.
10. vermeulen2010:
    - etch depth 230 nm `derived` (160 nm a-Si + 70 nm, printed separately; merged zhou2023 stores the same sum as
      design_target);
    - fiber angle 13 deg `design_target`: it is the measurement angle; no separate design angle is printed;
    - mfd_fiber_um not entered (no MFD printed).
11. zhang2013:
    - 0.019 / 0.14 dB per crossing `measured`: the per-crossing value is stated and the division by 101 is not shown
      (D167 analogue);
    - W_MMI 1.2 um / W 0.6 um are stated for the design analysis (p.2) and applied to both fabricated grids;
    - the 3.08 um pitch = Ls 1.88 + W_MMI 1.2 of the nc = 2.5 design confirms this for the SWN grid.

## Registry gaps (skipped value + locator, proposed definition)

- `bw_1p5db_nm` (fiber_chip_coupler), "full width within 1.5 dB of peak transmission": streshinsky2013 35 nm (1550
  band) and 18 nm (1310 band) (p.1 Abstract; p.7 Sec. 4).
- `gap_nm`, `coupling_length_um`, `min_bend_radius_um` for polarization, as the role geometry of DC-based PBS (already
  confirmed in the lit_27 audit): fukuda2006 gap 480 nm, coupling length 10 um, bend radius 3 um (p.3-4 Sec. 3.1).
- `taper_length_um` for polarization: huang2013 input / output coupler Lc 1 um (p.2-3).
- `layer2_thickness_nm` / second-layer width for crossing.multilevel, "thickness (width) of the upper crossing layer
  (material in condition)": jones2013 Si3N4 250 nm x 1.2 um (p.4 Sec. 2).
- Not proposed:
  - crossing bandwidth (zhang2013 "1520-1610 nm" without a level);
  - substrate-loss fraction (streshinsky2013 59 %, simulated only).

## Open questions

1. streshinsky2013: should a PSGC also get a polarization.pbs row (D396) to hold the isolation as per_db, or stay a
   single GC row with crosstalk_db (current)?
2. jones2013: is a Sandia MESA facility row wanted (authors' own lab facility, D82c), or does fab Sandia suffice?
3. jones2013 410 vs 400 nm gap: keep 410 measured with the note, or enter the gap as approx / ambiguous?
