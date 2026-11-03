# Batch lit_73 report (distill subagent, 2026-11-02)

Classes fiber_chip_coupler, fiber_interface (plus waveguide_platform.straight / bend / transition and
chip_chip_coupler.evanescent rows the papers hold). Papers: su2026, du2022, cheben2015, lindenmann2014, sutherland2019,
brusberg2025, he2021. Page-1 titles match the source rows; no wrong paper, no correction. Totals: 26 components, 233 metric
rows. Dry run: 0 errors.

## Per paper

| paper | components | metrics | contents |
|---|---|---|---|
| su2026 | 8 | 78 | cantilever edge couplers A, B, C; simulated optimized B, C; SiN1-Si transition (design); Si and SiN waveguides |
| du2022 | 2 | 21 | expanded-beam connector PIC-to-fiber and LD-to-fiber |
| cheben2015 | 7 | 61 | SWG edge couplers N1-N3; reference inverse tapers I1-I3; SOI spirals |
| lindenmann2014 | 2 | 21 | MCF-to-SOI photonic wire bonds; reference SOI GC |
| sutherland2019 | 1 | 8 | glass-tube MT-style ferrule |
| brusberg2025 | 4 | 36 | straight IOX waveguides; IOX fan-out; its S-bends; IOX-SiN evanescent coupler |
| he2021 | 2 | 8 | U-Groove fiber array assembly; SiN edge coupler (pair values only) |

## Values not entered, and why

- su2026: die-to-die fluctuation 0.17 / 0.18 dB (p.12; no parameter, in a metric note); simulated facet overlap 90.8 / 90.6 %,
  overlap PDL < 0.01 dB and 1-dB tolerances +/-2.0 / +/-1.7 um (p.4-5; stated once for the facet of all three designs, D254, in
  notes); SiN1-Si sweep points at W3 350 / 500 nm (p.7, notes); SiN2-SiN1 transition (figure only, Fig. 6(a)); EME taper sweeps;
  Table 1 other works and the cited 1.3 dB / 0.4 dB of refs. [29,30]; projected gains; tape-out L3-SiN1 printed "250 nm" (unit
  looks wrong, no row); Tables S1 / S2 are in Supplement 1, not in the cached text.
- du2022: calculated Gaussian tolerance curves (Fig. 3-4; model of a general mode size, not a device); intro 6.3 dB and about
  0.5 dB (other works); SSC 3 um mode, GC, MMI (no isolated value, no rows); lens focal lengths and offsets in notes (no
  parameter); 5 % remating variation (p.10, no parameter, note); LD 26 deg divergence (cited, ref. [16]).
- cheben2015: refs. [4,6] values (0.9 / 1.2 dB, 0.23 / 0.47 dB, 0.3 dB; D259); less than 0.2 dB over 1480-1580 nm (p.10; coupler
  and polarization not named, N3 TM inset looks wider: D159, in notes); design-step values on a homogeneous-index model
  (250 nm tip, nSWG 2.6, PDL 0.1 dB); substrate-leakage FDTD on equivalent strips (TE 0.04 / TM 0.15 dB, TM 0.72 dB at 2 um BOX);
  Bragg wavelengths; 240 % / 270 % comparison; Fig. 3 segment lengths L = 198 / 194 nm.
- lindenmann2014: ref. [2] 9.8 dB and the authors' earlier 1.6 dB (D259); bake and rinse result without numbers (note); writing
  times; 0.1 dB diameter window 10.9-13.0 um (note); Fig. 3-4 curves beyond the printed 60 um point.
- sutherland2019: max-IL change 0.2-0.5 dB over repeated mating (p.4; no parameter, note); 0.21 um diameter mismatch (note);
  receptacle ferrule and housing (no optical value, no rows). Fiber-to-PIC loss is not measured: all values are ferrule to
  ferrule or ferrule to V-groove array.
- brusberg2025: detachable connector 0.8 dB (p.3): its sentence carries ref. [7], the authors' earlier paper, and the summary
  repeats it (D259 / D408): no value and no connector row; C-band coupling (ref. [6]); Fig. 2(C) curves and standard fan-out
  simulation (no printed values); 550 um guide pins (no parameter).
- he2021: refs. [2,3] sub-1 dB penalties; 1.4 um pedestal control and below-1-um stage targets (notes); pedestal and groove
  dimensions in core_material (no parameter).

## Missing orgs

None for fab / facility. Author or supplier orgs without a fab role, for the org round only: TeraXion (cheben2015 p.1, not in the
registry), Fibercore (lindenmann2014 p.2, MCF supplier, note), Nanoscribe (lindenmann2014 p.4, tool vendor).

## Judgment calls for the auditor

1. Pair measurements with propagation and link loss removed (su2026, cheben2015): `loopback_half`, `loopback`, `derived`, although
   su2026 axes print dB/facet and cheben2015 never writes the halving. Precedent: gradkowski2023 and 9 merged edge rows. These rows
   do not rank under the `edge_taper` primary (per_facet); D167 (measured, per_facet) is the alternative for su2026.
2. PDL: su2026 `derived` (caption says calculated by subtraction); cheben2015 `measured` (text says measured directly).
3. su2026 platform `silica` (D82f: pure SiO2 facet, tip retracted 20 um; nauriyal2019 precedent), stack in core_material. Fab
   org_zhangjiang_laboratory from the conclusion's first-person statement, with all authors listing that org (three also Fudan).
4. su2026 figure-read die spreads (Fig. 10): six rows at +/-0.03 dB. Design A reads agree with the printed 0.17 / 0.18 dB.
5. du2022 printed values disagree with the paper's own data, entered as printed and flagged: 1-dB tolerance about +/-35 um
   against Fig. 10 about +/-75-90 um; better than 85 % against Table 1 values to 0.95 dB and Fig. 10 peak about 83-85 %; beam 160 um
   diameter (abstract) against 80 um diameter (p.8) and 80 um waist (p.9-10); less than 1 dB (abstract) against 1.11 dB (Table 2).
   Beam size entered as `author_estimate`. Scope `per_coupler` with method `unspecified`: input calibration not stated. Fab empty
   on both connector rows (authors at two orgs); AMF named only for the PIC, in notes.
6. du2022 `il_nonuniformity_db` used for swap-test spread across connectors, not across channels only: basis `derived`.
7. cheben2015 I3 simulated rows tied to the fabricated 170 nm tip by the matching tip width (paper does not name I3 there). N3 TM,
   I2, I3 are figure reads. N3 92 % stored as `derived`, `loopback_half` (abstract form of 0.32 dB).
8. lindenmann2014 wavelength 1550 nm inferred for measured rows (not stated; design wavelength). GC reference kept as its own row
   (on-chip part with a measured value; rule 13 does not exclude it). Fab KIT from first-person fabrication text with all authors at
   KIT (D80b); borderline wording; SOI chip origin not stated.
9. sutherland2019: band unspecified on all loss rows; fab empty despite all authors at Corning units (passive sentences only).
   Fig. 7 channel 8 reads about 1.55 dB against the printed < 1.5 dB. < 1.1 dB `author_estimate` (Fresnel 0.4 dB of unstated origin).
10. brusberg2025: IOX-SiN coupler in chip_chip_coupler.evanescent even though the values include fan-out bends and propagation
    (scope `per_interface`, includes spelled out). Polarization `tm` on the 0.38 dB minimum from the Fig. 3(C) legend; the text gives
    none. Text and caption swap the Device colors. Straight IOX row holds fiber-to-fiber and budget values in
    waveguide_platform (no pitch / channel parameter there). 0.3 dB, 0.126 dB, 0.14 dB `author_estimate`, `loss_breakdown`; bend
    coefficient `simulated` though the paper says estimated (Fig. 2(C) is the simulated curve).
11. he2021: excess < 1 dB is `insertion_loss_db` per_facet with active-alignment loss excluded, on the v_groove row; 2 um tolerance on
    the edge coupler is a design statement, `author_estimate`. EC row has only figure-read pair values, kept because the
    paper's EC has no other row. Fab org_imec only on the U-Groove row (D399 logic); platform empty on the assembly row.

## Registry gaps (value skipped + locator + proposed definition)

- `il_nonuniformity_db` on fiber_chip_coupler: su2026 0.17 / 0.18 dB (p.12). Max minus min coupler loss across dies or channels.
- `mating_repeatability_db` on fiber_interface: sutherland2019 0.2-0.5 dB (p.4); du2022 5 % is a linear form (p.10). Change of
  insertion loss over repeated mate / demate cycles, cycle count in condition.
- `pitch_um` on chip_chip_coupler: brusberg2025 SiN U-loops 100 um (p.2). Channel pitch of the coupled array.
