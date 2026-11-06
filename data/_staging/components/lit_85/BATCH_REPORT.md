# lit_85 batch report (amplifier, frequency_converter, nonreciprocal), 2026-11-06

Dry-run: +18 components, +88 metrics, 0 errors (one existing warning on merged row ni2025b, not from this batch).

Page-1 title check: kao2026, li2025a and zhao2025a match their source rows. wang2018 and sohn2021 are arXiv preprints
titled differently from their journal source rows (wang2018: "Ultrahigh-efficiency second-harmonic generation in
nanophotonic PPLN waveguides" vs Optica 5, 1438 "... wavelength conversion in nanophotonic periodically poled lithium
niobate waveguides"; sohn2021: "Electrically driven linear optical isolation through phonon mediated Autler-Townes
splitting" vs Nat. Photon. "... optical isolation through phonon-mediated photonic Autler-Townes splitting"). Same
authors, same results, arXiv ids match the source rows: accepted as the same works (D427 / D433 precedent), not stopped.
li2025a's own reference 6 prints the Optica title for the wang2018 authors. No cached file is a correction or erratum.
Supplements: kao2026 Supplementary Sections 1-3 and li2025a Supplementary notes 1-3 not cached; sohn2021 carries its
supplement (p.13-25). sohn2021 p.22 (Table S1) has a garbled text layer: its values were read from the page render.

| paper | components | metrics |
|---|---|---|
| kao2026 | 2 (amplifier.parametric, frequency_converter.shg) | 13 |
| li2025a | 2 (frequency_converter.sfg_dfg, fiber_chip_coupler.edge) | 14 |
| wang2018 | 3 (frequency_converter.shg x2, fiber_chip_coupler.edge) | 13 |
| zhao2025a | 3 (frequency_converter.shg, resonator.ring, fiber_chip_coupler.edge) | 17 |
| sohn2021 | 8 (nonreciprocal.isolator x3, resonator.ring x3, fiber_chip_coupler.grating x2) | 31 |

## Not entered, and why

kao2026
- Pump efficiency up to 15.3 dB/(W mm) (p.3), squeezing 0.8 dB at 110 mW (p.4), SNR improvement approaching 6 dB,
  5.6 dB lower noise floor, BER 0.1 % -> 0.0008 % (p.4-5): no registry parameter (component notes).
- Adapted poling period (Fig. 1(e), curve between the 4.5 and 4.6 um ticks) and measured film thickness profile
  (about 580-610 nm): curves only, not read.
- Edge couplers below 1 dB and > 20 dB projected net gain (p.5): cited [38] / projection.

li2025a
- On-chip idler power 13.2 dBm (p.4; 20.94 mW in Table 1): no output-power parameter on frequency_converter.
- Setup PC / WDM losses (0.4-0.5 dB): equipment (rule 13). Simulated 400 nm theoretical bandwidth, flat OO response,
  calculated eye diagrams: no parameter. Fig. 3(g) temperature points (about 430 %/W/cm2 near 50 C, read) not entered.
- Facet SEM label 5.079 um (Fig. 3(c)): the feature it measures is not identified in the text.
- Table 1 rows of other works: not entered.

wang2018
- Corrected-model peak (about 3000 %/W-cm2 in Fig. 3(c)), generic Fig. 1(c) calculation (> 4000 %/W-cm2): only the
  device-specific ideal 4500 entered as simulated.
- Duty cycle ~39 % (fill_factor not allowed on frequency_converter), GVM 150 fs/mm, no photorefractive damage at
  ~10 MW/cm2, SH power ~117 mW: component notes.
- 0.03 dB/cm LN waveguide loss (p.1): cited [23]. RPE ~90 %/W-cm2: other work.

zhao2025a
- 0.23 / 0.25 dB/cm and ~1 nm roughness (p.2): ref. [25]. 814 %/W record: ref. [28].
- Surface roughness 0.27 nm (AFM), simulated n_eff 1.8656 / 2.0797, poling 400 V / 5 ms, electrode gap ~7 um: no
  parameter (notes).

sohn2021
- Fig. S4 775 nm dressed-state isolator (delta 1.5 GHz, BW_5dB = 218 MHz label, about 9.5 dB contrast read): the text
  does not say whether it is the Fig. 3(b) device with another mode pair or a separate device (D159); values in the
  773 nm isolator notes.
- Optical Q of 10^7 at 780 nm and 3.5 x 10^6 at 1550 nm (p.4): resonator and Q type not named (D159), notes.
- Sideband suppression ~20 dB or more (p.7), IC/IL figure of merit (Table S1), Gph, RF drive power, IDT pitch /
  aperture / angle (Table S2), electromechanical transduction ~40 %, S11 dip near 3 GHz: no parameter on
  nonreciprocal (notes). Total loss rates kappa1 / kappa2: equivalent to the entered loaded Q.
- Table S1 rows of other works: not entered.

## Missing fab / facility orgs

None. Registry ids used: org_the_university_of_texas_at_austin (kao2026), org_zhejiang_university (li2025a),
org_harvard_university + facility org_center_for_nanoscale_systems (wang2018),
org_university_of_illinois_urbana_champaign (sohn2021). zhao2025a fab empty (passive fabrication sentences, no
contributions; D80b). Wafer suppliers (NANOLN for wang2018, Shanghai Novel Si Integration Technology for zhao2025a)
are notes only.

## Judgment calls

1. li2025a efficiency rows (48.6 %, ~20 %, > 710 and > 100 %/W/cm2) `author_estimate`: the on-chip powers rest on the
   assumption that the idler coupling loss equals the signal's (p.4; rule 4, D394 analogue). Alternative: `measured`
   as for the other on-chip normalized efficiencies in this batch (wang2018, zhao2025a), which use calibrated
   per-wavelength coupling losses without such an assumption.
2. wang2018 fab org_harvard_university: first-person poling / patterning plus fabrication "in part" at Harvard CNS
   (p.4), following D419 (koyaz2026). The authors span five orgs; alternative: fab empty (D433 hiratani2024).
3. sohn2021 Fig. 4 isolator wavelength 1526 nm (caption and Table S2) over the p.8 text "1538 nm"; RF 3.04 GHz
   (caption, table) over "3 GHz" (p.8).
4. sohn2021 isolator insertion losses `measured`, scope `de_embedded`, excludes the grating couplers (kim2026
   precedent, same group and method); grating-coupler minima ~5 / ~7 dB `measured` per D167. Kappa_ext rows
   `author_estimate` (extraction not described; D403 analogue). Loaded Q rows from Table S2 `measured`.
5. kao2026 net gain 10 dB `derived` (23.5 - 13.5 dB); printed both "up to 10 dB" (p.1) and "over 10 dB" (p.3, p.5),
   entered without qualifier. Device 2 "over 15 dB" kept on the same row (design not stated to differ) though its
   Fig. 2(c) points read about 14.3 dB (D417).
6. wang2018 53 % conversion put on the 1440 nm row (Fig. 4 inset label 2600 %/W-cm2); wavelength left unspecified
   because p.4 prints SH "at 775 nm" while that guide phase-matches near 1511 nm. Platform lnoi_rib for wang2018 from
   the slab drawn in Fig. 1(a) (etch depth not stated).
7. QPM / peak wavelengths read off figures with `wavelength_inferred` (kao2026 1548 nm, wang2018 1511 / 1621 nm);
   li2025a and zhao2025a coupling-loss wavelengths inferred from the stated operating points / scan ranges.
8. zhao2025a waveguide width 1000 nm from the Cr mask strip (p.2) and the Fig. 2(e) label; the etched ridge top width
   is not stated separately. Design poling period 3.62 um `design_target` (fabricated period not stated).

## Registry gaps (value skipped + locator + proposed definition)

- `output_power_dbm` on frequency_converter: li2025a 13.2 dBm on-chip idler (p.4), wang2018 ~117 mW SH (p.4).
  Definition: generated (SH / idler / sum) output power, reference plane in ref_plane.
- Bandwidth on frequency_converter (D419 / D429 candidates): li2025a NCE > 100 %/W/cm2 over 90 nm (p.5).
  Definition: wavelength span over which the stated efficiency criterion holds (criterion in condition).
- `sideband_suppression_db` on nonreciprocal (D419 candidate): sohn2021 ~20 dB (p.7). Definition: carrier-to-strongest
  modulation sideband ratio at the output, positive dB.
- Pump-normalized parametric gain dB/(W mm) on amplifier: kao2026 15.3 (p.3); chang2026 1.21 skipped earlier.
  Definition: on-chip gain per pump power per length as stated.
