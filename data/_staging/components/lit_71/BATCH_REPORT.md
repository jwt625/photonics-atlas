# Batch lit_71 report (distill subagent, 2026-11-02)

Classes mode_converter, splitter (plus waveguide_platform.other, fiber_chip_coupler.grating / edge, wdm.mrr rows the papers
hold). Papers: moralesalvarado2026, sun2025, izumisawa2026, anelli2024, luo2014. Page-1 titles match the source rows; no wrong
paper, no correction. Totals: 16 components, 135 metric rows. Dry run: 0 errors.

## Per paper

| paper | components | metrics | contents |
|---|---|---|---|
| moralesalvarado2026 | 3 | 20 | DLP-printed Y-branch; 5 % and 10 % blend slabs |
| sun2025 | 4 | 37 | 3-mode digital-metamaterial MUX; 80 nm pixel design; two GCs |
| izumisawa2026 | 3 | 36 | SPL0 slotted MMI; ADC mode (de)MUX; unslotted MIPS design |
| anelli2024 | 1 | 6 | InF3 mode-group photonic lantern |
| luo2014 | 5 | 36 | microring MDM link; ring; edge coupling; two designs |

## Values not entered, and why

- moralesalvarado2026: n / k (Fig. 2, partly from authors' ref. [21] / [24]; no parameter); Rq roughness 1.02, 0.44, 6.38, 9.20 um
  (p.13) and 9.4 deg junction angle (p.5) in notes (no parameter); simulated transmission 95 % (no splitter parameter);
  Table 2 comparison values (other works; ref. [33] is the authors' earlier PFeBSe device).
- sun2025: IL variation 0.94 dB and tolerance fluctuation 1 dB (p.5, p.10; no mode_converter parameter); link rates (system
  level); Table 1 other works; 140 / 100 nm pixel variants (unlabelled Fig. 10 curves); no value is attributed to the authors'
  ACP 2024 paper [43] (D259 not triggered).
- izumisawa2026: Fig. 8(b) (de)MUX transmission (no labelled value, TE0 above 0 dB by reference choice); Fig. 10 a_slot - 10 nm and
  Fig. 11 SPL0 curves (no labelled value); Table II other works; Table II bandwidths 100 / 35 nm (no level stated; they match
  the spans of the rows); supplement S3 (SEM parameters) is not in the cached text; a_core, a_slot, ws, W1/4 in notes.
- anelli2024: mode selectivity only as far-field images; EL 0.35 dB (authors' ref. [31]); taper angles and Dout in notes.
- luo2014: power penalties (no parameter); FSR (no printed value; design "87 channels / 50 GHz" is an extrapolation); on-chip IL
  by subtracting 10 dB was not computed: the 10 dB term has no stated origin; 4.35 Tb/s projection.

## Orgs

- Missing, needed: `ShanghaiTech Quantum Device Lab` (sun2025 p.5, device "fabricated at"; proposed facility, parent
  `org_shanghaitech_university`; no author there, so fab_org_ids left empty). `UTFPR-CT Multiuser Photonics Laboratory
  (Multi-Foton)` (moralesalvarado2026 p.15, infrastructure thanked; proposed facility; parent Universidade Tecnologica Federal
  do Parana, Curitiba, Brazil, also missing).
- Missing, note only: Le Verre Fluore (Bruz, France; anelli2024 p.3, p.6; made the fibers and capillary; supplier note).
- Entered: org_applied_nanotools (izumisawa2026 p.5 "fabricated by"); org_cornell_university (luo2014 p.7 Author contributions,
  L.-W. Luo, D395); org_cornell_nanoscale_facility (luo2014 p.7).

## Judgment calls for the auditor

1. sun2025 measured IL rows: scope `de_embedded` (a2013 precedent), not `per_component`. The paper calls it IL of the MUX, but the
   spectra come from the MUX + bus + DEMUX circuit (Fig. 4(a)) with only GC losses subtracted and no halving stated. Measured
   TE0 < 0.4 dB is below the simulated single-MUX minimum 0.49 dB: consistent with GC-subtraction uncertainty, not explained in
   the paper.
2. sun2025 GC losses `author_estimate`, origin not stated.
3. moralesalvarado2026 slabs as `waveguide_platform.other` (unguided beam through printed slabs; the paper calls it propagation
   loss); check against D411. Could be dropped to notes if material attenuation is out of scope. Abstract pairs 5 % / 10 % with
   0.022 / 0.025 dB/mm "respectively", reversed against Sec. 5.3 and Fig. 9; Sec. 5.3 / Fig. 9 used.
4. moralesalvarado2026 reflection term 0.17 dB: printed as the total of both faces, but R = 0.0389 gives 0.17 dB per face. Printed
   value kept with a note. Four loss-budget terms entered as `insertion_loss_db` with `loss_breakdown`.
5. moralesalvarado2026 wavelength: measured rows use the 636.6 nm setup laser; the paper's Table 2 and simulation say 635 nm.
6. izumisawa2026 ADC crosstalk: text "below approximately -20 dB" entered as gt 20, but the Fig. 8(b) traces peak near -16 dB around
   1550 nm. Wavelength span from the axis, `wavelength_inferred`.
7. izumisawa2026 Fig. 9 upper-port labels (-13.5, -11.9 dB) entered as `extracted_from_figure`; text gives only the worst values
   (bottom port).
8. izumisawa2026 MIPS design row: its 32.56 um follows ref. [12] per p.3; the -30 dB value is this paper's own simulation.
9. luo2014 ring row `wdm.mrr` with one design-stated metric (linewidth >= 15 GHz, `author_estimate`), D396 / D400: it carries the ring
   geometry that mode_converter cannot. Could merge into notes if a design-only metric is judged too thin.
10. luo2014 edge-coupling row: aggregate 10 dB for both interfaces, scope `fiber_to_fiber`, `author_estimate`; the chip-side coupler
    is not described. The link IL rows are also `fiber_to_fiber`.
11. luo2014 expected 1.5 dB on the fabricated row as `author_estimate` (condition says not measured). Methods unit glyphs: the
    text layer prints micrometre lengths as "mm"; renders show um.
12. anelli2024 IL scope `device_total` (paper: not net, includes ICL pigtail coupling); platform `other` (leonsaval2014 precedent);
    fab empty.

## Registry gaps (skipped value + locator + proposed definition)

- `gap_nm` for mode_converter (already listed in earlier batch reports): luo2014 240 / 200 / 200 nm (p.5), 200 and 280 nm designs
  (p.3); izumisawa2026 ADC 210 / 190 nm (p.6 Fig. 8(a)). Definition: coupling gap of a directional-coupler or ring mode (de)MUX.
- `il_nonuniformity_db` or `wdl_db` for mode_converter: sun2025 0.94 dB over 1500-2100 nm (p.5).
- `min_bend_radius_um` for mode_converter: izumisawa2026 5 um (p.6 Fig. 8(a)).
- SWG slotted MMI: slot width ws 400 nm, Si segment widths a_core 110 nm and a_slot 134 nm (izumisawa2026 p.3 Fig. 3). Proposed
  `slot_width_nm`, `swg_segment_width_nm` for splitter.
- Y-branch junction angle: moralesalvarado2026 9.4 deg (p.5). Proposed `junction_angle_deg` for splitter.
