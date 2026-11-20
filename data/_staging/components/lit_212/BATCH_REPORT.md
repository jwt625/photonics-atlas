# lit_212 batch report

Papers: lit:ayan2023, lit:lamont2008, lit:sabapathy2012. Page-1 titles match the source rows. verified_on 2026-11-20.
Dry run of `merge_component_staging.py`: +16 components, +60 metrics, 0 errors. The one warning names the merged
row cmp_lit_ni2025b_pimmwc, which is not in this batch.

| paper | components | metric rows |
|---|---|---|
| ayan2023 | 9 | 34 |
| lamont2008 | 4 | 16 |
| sabapathy2012 | 3 | 10 |

## ayan2023 (Si3N4 meter-long spiral FWM, Optics Express 2023)

Rows:
- 3 x `frequency_converter.other`, 2.2 x 0.67 um, lengths 0.5 / 1 / 1.5 m. Printed maximum CE -10 / -3.7 / -4.6 dB
  (p.5) at about 1.7 W estimated coupled pump (1550 nm). Stored as % `power_conversion_efficiency_pct`, basis
  derived (ding2022 / ye2021 precedent), with the nominal cross-section and length.
- 4 x `frequency_converter.other`, 2.5 x 0.67 um, lengths 0.5 / 1 / 1.5 / 2 m.
  - 2 m: printed "around 3 dB" at 32 dBm (p.6), derived, approx, 1536.5 nm from the Fig. 3(a) inset caption.
  - Fig. 3(b) points at 1.7 W (0.5 / 1 / 1.5 m: -5.0 / -2.3 / +0.5 dB) and at 0.25 W (all four lengths: -21 / -19 /
    -17 / -14 dB): `extracted_from_figure` (+/- 0.3 dB, vector render at 5x), converted to %.
- 1 x `waveguide_platform.straight` population row: propagation loss 2-4.7 dB/m "in our samples" (p.4), entered as
  0.02-0.047 dB/cm, range, derived.
- 1 x `fiber_chip_coupler.edge`: inverse tapers, "total coupling loss is estimated around 5 dB" (p.3). Scope
  device_total (lensed fiber in, lens out; fard2021 precedent), author_estimate.

Not entered:
- One-sided -3 dB normalized-CE bandwidths 48 / 26 / 15 nm (p.5, Fig. 2(d)-(f); 26 nm is only a figure label). There is
  no frequency_converter bandwidth parameter (registry gap, see below).
- Fitted gamma 0.6-0.8 /W/m and simulated gamma 0.75 /W/m: no parameter.
- Simulated GVD and mode-overlap maps (Fig. 1) and simulated CE maps (Fig. 2(a)-(c)).
- Waveguides I-V (2.0 x 0.8 um, ROC 75 / 230 um, 7.4-32 cm, Table 1). The only numbers are the reduced chi-square of the
  CE fit (1.12-4.78 dB), a fit-quality figure with no parameter, and plotted CE without a stated pump power. No rows
  (geometry-only otherwise).
- Temperature results (Fig. 5): CE varies by more than 15 dB with set temperature; up to 10 dB improvement at
  optimized temperature. Relative values, in notes only.
- Parametric gain in the 2 m waveguide (Fig. 3(a) inset): no value printed, so no amplifier row. Cascaded idlers over
  more than 100 nm: no parameter.
- Earlier-work values (ref. 21: -30 dB / 120 nm, -22 dB / 150 nm; ref. 25: 1.7-5 dB/m) are cited work (rule 3).

Fab / facility: empty. "fabricated by the Damascene process [25]" is passive with no org named (D80b, D433). No
facility is acknowledged. process_name is empty ("Damascene process" is a technique name with a citation; it appears
in core_material, as in the riemensberger2022 precedent).

## lamont2008 (As2S3 rib parametric amplifier, Optics Express 2008)

Rows:
- `amplifier.parametric` (65 mm As2S3 rib, TM):
  - on-chip signal gain 32.5 dB at 1610 nm;
  - net (fiber-referred) signal gain 18.8 dB;
  - gain bandwidth 180 nm (measured, criterion not printed);
  - geometry: 2000 nm width, 850 nm thickness, 350 nm etch, 65 mm length.
- `frequency_converter.other` (same waveguide, D396): idler gain 30.6 dB on-chip and 16.8 dB net, stored as % (kuyken2011
  / foster2006 precedent).
- `waveguide_platform.straight`: 0.5 dB/cm "estimated" (method not stated), author_estimate; same cross-section.
- `fiber_chip_coupler.edge`: lensed-fiber facet about 6.9 dB per facet including reflections, measured (D167).

Not entered:
- Calculated gamma about 9900 /W/km, Aeff 1.2 um2, and dispersion +30 ps/nm/km: no parameter.
- Simulated gain spectra and gain vs pump power (Fig. 6, Fig. 7).
- Projected about 30 dB net gain with 0.8 dB/facet inverse tapers: rests on a cited coupler (ref. 27).
- Cited silicon results (ref. 11: +1.8 dB, 80 nm).

Fab / facility: empty. Deposition, lithography and etch are described in the passive voice with no org named (D80b).
The acknowledgment names ARC funding only.

## sabapathy2012 (fs-laser-written Er:GeGaS amplifier, Optical Materials Express 2012)

Rows:
- `amplifier.rare_earth`:
  - relative gain 1.0099 dB (1541 nm) and 0.5435 dB (1550 nm), measured;
  - 2.524 / 1.359 dB/cm, derived (the paper's division by 0.4 cm);
  - fiber-to-fiber insertion loss 2.58 dB at 1600 nm, measured;
  - length 4 mm.
- `waveguide_platform.straight`: 1.6 dB per 4 mm, entered as 4.0 dB/cm at 1600 nm, author_estimate (rests on the
  calculated Fresnel term; D163 precedent).
- `fiber_chip_coupler.edge`: 0.22 dB/facet mode mismatch (measured) and 0.28 dB/facet Fresnel (calculated from the index
  measured at 514 nm, author_estimate). These are two per_facet rows with includes / excludes.

Not entered:
- Sum per facet (0.50 dB): not printed.
- Glass index 2.41 at 514 nm and band gap 2.4 eV: material values.
- Writing-series parameters: in core_material / notes.
- Ref. 15 / 19 relative gains of 2.5 dB: cited work.

Fab / facility: empty. "we report the synthesis and fabrication" names no fabricator, and the authors are split
between the Indian Institute of Science and Heriot-Watt University (D80b, D395). The thanks (glass-synthesis support,
SV University; discussions, Heriot-Watt and Optoscribe) are not fab or facility statements. UKIERI and EPSRC are
funding.

## Missing fab / facility orgs

None. No fab or facility org is stated in any of the three papers.

## Judgment calls for the auditor

1. lamont2008 headline gains (32.5 / 18.8 dB signal, 30.6 / 16.8 dB idler) are `simulated`. The paper says the output
   peak powers "were calculated from the simulation" and the gain is "estimated from simulation". The simulation
   reproduces the measured spectrum (Fig. 4), but the gain is not read from the data. Alternative: `author_estimate`.
2. lamont2008 180 nm gain bandwidth is `measured` with "criterion not printed". The text attributes it to the recorded
   spectra (Fig. 5(a)); the Fig. 5 caption attributes "over 180 nm" to simulations.
3. ayan2023 CE basis is `derived` (dB -> %). The reference planes of Pi and Ps are not printed, and the coupled pump
   power is an estimate (a condition, not an input of the ratio). Alternative: `author_estimate`, if the auditor
   reads CE as on-chip idler over coupled signal (li2025a, D462).
4. ayan2023 Fig. 3(b) figure-read CE rows on the 2.5 um series (7 values). They were added because each sibling length
   needs a performance metric and the text prints only the 2 m value. Drop them if figure-only rows are unwanted here.
5. ayan2023 loss range 2-4.7 dB/m is a population row (D165) rather than notes-only (D159). The samples are "our
   samples" and are not tied to one waveguide.
6. sabapathy2012 platform `glass` (fs-laser-written bulk glass precedents such as camus2020 BGG). The chalcogenide film
   rows of lamont2008 use `other`.
7. sabapathy2012 relative gain is a signal enhancement with fluorescence subtracted, not net / internal gain. It is
   entered in gain_db with the definition in the condition (bonneville2020 D580 precedent).

## Registry gaps

- frequency_converter conversion bandwidth (proposed `bw_3db_nm` widened to frequency_converter, or
  `conversion_bandwidth_nm`, with the one-/two-sided criterion in condition). Skipped values: ayan2023 one-sided -3 dB
  bandwidths of 48 nm (0.5 m, p.5), 26 nm (1 m, Fig. 2(e)) and 15 nm (1.5 m, p.5). Same gap as li2025d (110 nm).
- Waveguide nonlinear parameter `gamma_per_w_per_m` (waveguide_platform / amplifier / frequency_converter; fitted or
  calculated in condition). Skipped values: ayan2023 0.6-0.8 /W/m fitted (p.6); lamont2008 about 9.9 /W/m calculated
  (p.4).
