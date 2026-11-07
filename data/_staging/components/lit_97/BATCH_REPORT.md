# lit_97 batch report (2026-11-06)

All six cached texts match their source rows (page-1 title / arXiv id); none is a correction, erratum or another paper. No garbled text layer flagged. ji2026 is the arXiv v1 preprint (2501.06936, 2025-01-12, titled "Full C- and L-band tunable erbium-doped integrated lasers via scalable manufacturing"); the source row has the same arXiv id and the Nature Communications 2026 title: same work, journal version unread (D430 / D433). kiewiet2026's source row is the arXiv record itself. Dry-run: +22 components, +131 metrics, 0 errors (the one warning, ni2025b m18 / m4, is an existing merged row).

| paper | components | metrics |
|---|---|---|
| ji2026 | 6 (laser.tunable 1; resonator.ring 2; fiber_chip_coupler.edge 2; chip_chip_coupler.butt 1) | 41 |
| kiewiet2026 | 8 (laser.heterogeneous 1; laser.tunable 2; resonator.ring 2; reflector.loop_mirror 1; fiber_chip_coupler.edge 1; waveguide_platform.straight 1) | 31 |
| kumar2022a | 1 (laser.heterogeneous) | 9 |
| shindo2023 | 2 (laser.soa_dfb) | 14 |
| spiga2016 | 3 (laser.vcsel) | 20 |
| yamaoka2024 | 2 (laser.heterogeneous; fiber_chip_coupler.edge) | 16 |

## Not entered, and why

ji2026
- Slope efficiency about 24 % (optical-to-optical, on-chip, Fig. 3(E), p.5): no laser % slope parameter (W/A only).
- Frequency drift < 15 MHz over 6 h (Fig. 4(E)), self-reflection tolerance 14 dB, injection -30 to +10 dBm, operation up to 125 C: no parameter.
- Tunable MZI loop mirrors (Supp. Note 3, Fig. S3 / S4): transmission tunable 0-1, fitted k1 = k2 = 0.09 (1550 nm), k1 0.16 / k2 0.3 (1480 nm); the paper does not say which of the two mirrors Fig. S3 shows (D159), and Fig. 2(G) prints no values: no rows.
- Gain 2.28 dB/cm and loss 1.98 dB/m used in the Supp. simulation "matching values measured" (measurement not shown); Er concentrations / lifetimes, mode area 3.02 um2, overlap about 30 %, SRIM profile: simulation inputs.
- Vernier heater tuning efficiency 620.6 GHz/W (p.4, Fig. 2(F)): no GHz/W parameter; conversion to pm/mW would need an assumed wavelength. In the ring notes.
- Simulated edge-coupler losses are entered (0.56 dB fiber, 0.97 dB pump diode); comparison values in Fig. 1(B) are other works (rule 3).
- Cavity length about 18 cm (TRN model input), film roughness / uniformity / anneal shrinkage: model inputs or process data.

kiewiet2026
- Microgear fit rates (internal 0.52 GHz, external 0.20 GHz, mu 0.67 GHz): the printed Q values are reproduced only with the rates as half-widths (Q = f0 / (2 gamma) at 793.6 nm), so they are not entered as kappa_*_mhz (energy decay rates); 2 mu splitting not entered (convention not stated). Q_L and Q_i entered as derived.
- Coupling efficiency about 50 % (from the authors' earlier work [30], rule 3); Table I row of [30] and other works (rule 3).
- Grating-coupler loss of the microgear laser output: measured on a reference waveguide but not printed.
- RSOA net gain (Supp. Fig. S1) and Supp. Notes 2-4: not in the cached text.
- Projections (50 Hz / 90 Hz linewidths, 10-20 mW, 50 mA threshold): not results.
- Vernier laser threshold (Fig. 6(c)) and laser 2 output power: not printed.

kumar2022a
- "Close to 50 dB" suppression in Fig. 3(a) belongs to the external tunable bandpass filter, not the laser SMSR; FWM peaks > 30 dB below the lasing modes: no parameter; 64 Gb/s SNR / ER with an external ring modulator: link result.

shindo2023
- EAM / modulation metrics (EO 3-dB bandwidth about 20 GHz, chirp about 0, DER about 9.6 dB, OMA 10.5 dBm, BER, 38.4 dB loss budget, dispersion penalties): EO-atlas candidate (skill rule 2).
- SOA-length series (75 / 100 / 150 / 175 um, CoC): only OMA / DER / EO responses (modulation), so no rows; new vs conventional MQW about 1.9 dB higher maximum intensity (relative only); aging tests (N = 30, 85 C, 200 mA, 8000 h; N = 15, 55 C, 2000 h): no parameter.
- Facet reflectivities (AR estimated < 1e-9, HR about 0.7): no laser parameter; in core_material.

spiga2016
- DQE (52 % to 37 % for 5 um, Fig. 3(a)), internal loss / internal quantum efficiency (Fig. 4(a)), D-factor 10.1 / 12.5 GHz/mA^0.5, K-factor 165 / 172 ps, effective thermal conductivity 48 W/(K m): no parameter.
- Roll-over currents 10.5 / 6.6 mA, 130 fJ/bit heat-to-data ratio, ER 8.7 dB / OMA 5 dBm (estimated), BER results: no parameter or link metrics.
- Mirror reflectivities 99.4 / 99.9 %: no laser parameter (in core_material).
- 3 um bandwidth: Fig. 5(a) caption shows only the 4 um device.

yamaoka2024
- Thermal resistance 10.8e3 K/W per 1 um active length (p.5): normalized per length and resting on the typical dlambda/dT 0.09 nm/K from the authors' ref. [14]; registry has no per-length Rth. Calculated Rth / f3dB vs SiO2 thickness (Fig. 2): simulation.
- SiOx mode-field diameter 3.5-4 um: stated for the authors' earlier SSC design (p.2, refs. [13], [19]); rule 3.
- Energy cost 1.3 / 1.2 pJ/bit, BER / transmission results: no parameter.
- Ridge / mesa width, SiOx core and taper dimensions: not printed.

## Missing orgs (registry)

- "Varian Semiconductor, Applied Materials" (ji2026 p.1 affiliation; author contributions p.8 name the implanters): mapped to org_applied_materials; Varian Semiconductor (unit) is not in organizations.csv / org_aliases.csv (alias candidate).
- Walter Schottky Institut, Technische Universitaet Muenchen (spiga2016 p.1): not needed by a row (fab empty).
- No other missing org is needed by a row.

## Judgment calls

1. kiewiet2026 fab: Vernier lasers, rings, Sagnac mirror, edge coupler and platform waveguide -> org_imec ("SiN ... fabricated on a 200-mm SiN platform of imec", p.6; imec co-authors provided the wafer, p.12; D455). Microgear laser and reflector fab empty: the in-house EBL SiN has no named fabricator, and the coupon fabricators (M.K., S.C.) carry the joint Ghent University - imec / imec affiliations (D433, D395).
2. ji2026 fab: org_epfl (contributions: X.J., Z.Q. fabricated the Si3N4 samples) plus org_applied_materials on the Er-implanted laser row only (contributions name the implanters, D80b two-org rule); facility org_center_of_micronanotechnology (acknowledgment: samples fabricated in CMi) on all rows.
3. ji2026 one laser row for the design with die IDs per metric (D165), not one row per die. On-chip pump threshold 17.5 mW author_estimate (on-chip referencing not described; D460 franken2025, D431). Lorentzian linewidth 77.3 Hz (pi h0, derived) entered; abstract / summary 95 Hz is a printed conflict (D417), in notes.
4. ji2026 input / output edge couplers as two rows: "widths tapering from 0.42 um at the input and 0.5 um at the output" may mean two tip widths or one taper's ends; no width rows (D102). The 0.97 dB pump-diode coupling is a chip_chip_coupler.butt row on the same physical coupler (D396).
5. Intracavity rings (ji2026 Vernier pair, kiewiet2026 microgear and Vernier MRR) -> resonator.ring (D400). kiewiet2026 microgear Q_i derived, not author_estimate: the joint transmission / reflection t-CMT fit fixes under-coupling (D403; D455 / D465 analogue).
6. On-chip laser powers that subtract a measured coupler loss (kiewiet2026 22 mW, 0.37 W/A, 9.4 %, 0.4 mW, 0.2 %) derived (D394).
7. yamaoka2024 and spiga2016 extend the authors' conference papers ([18] / [6]); values kept because the results sections and figures present them without attribution (D408). yamaoka2024 p.2 does credit 2.7 dB / 7.3 dBm / 57 GHz to [18]; weak point for the audit.
8. yamaoka2024 SSC loss 2.7 dB per_facet derived (difference of the PD-detected and HNAF-coupled powers, as the paper defines it); the printed maxima give 2.8 dB (D417 note). kappa 250 /cm derived (spectral fit, itoh2024 precedent).
9. spiga2016 5 um threshold 1.3 mA assigned from the printed 0.7-1.3 mA range plus "increases with the area"; 3 um uses the explicit 0.67 mA. Rth 7950 K/W derived from the printed 0.612 nm/mW / 0.077 nm/K (the paper's Eq. (5) definition; no Rth number printed). Several output powers, wavelengths and one SMSR are figure reads (extracted_from_figure, uncertainty in notes).
10. shindo2023 rows are the two TOSA AXELs (1358 / 1304 nm, laser.soa_dfb, fab org_ntt by first-person fabrication with all authors at NTT, D399); modulated Pavg kept on the laser rows (theurer2026 precedent) with ref_plane fiber and the TOSA optics in includes.
11. kumar2022a laser.heterogeneous (hybrid III-V/Si DFB; laser.dfb also fits); fab org_intel ("fabricated in Intel's silicon photonics fab").
12. kiewiet2026 mode-hop-free range 45 GHz converted to 0.095 nm (derived, at about 795.75 nm read from the Fig. 7(d) axis); 0.3 nm fine tuning entered as printed.
13. kiewiet2026 imec platform loss < 0.6 dB/cm entered as author_estimate (platform figure; no measurement shown).

## Registry gaps (skipped value + locator, proposed definition)

- laser optical slope efficiency in %: ji2026 about 24 % (p.5 Fig. 3(E)); `slope_efficiency_pct` (laser): optical-to-optical or photon-number slope efficiency as defined by the paper. Same gap for spiga2016 DQE 37-52 % (Fig. 3(a)).
- tuning efficiency in GHz per W: ji2026 620.6 GHz/W (p.4); `tuning_efficiency_ghz_per_w` (resonator, wdm, laser, phase_shifter).
- mode-hop-free tuning range in frequency: kiewiet2026 45 GHz, > 140 GHz fine tuning (p.8); `tuning_range_ghz` (laser).
- per-length thermal resistance: yamaoka2024 10.8e3 K/W at 1 um (p.5); or a definition note on thermal_resistance_k_per_w allowing a length normalization in condition.
- relaxation-frequency D-factor (GHz/mA^0.5) and damping K-factor (ps): spiga2016 p.5.
- internal loss (1/cm) and internal quantum efficiency: spiga2016 Fig. 4(a) (with D431 / D433 candidates).
- maximum operating temperature: ji2026 125 C (p.8; D431 candidate).
- reflectivity / tuning on the laser cavity mirrors of a loop-mirror reflector: tuning_power_mw on reflector (D430 candidate), ji2026 about 600 mW (Supp. p.15).
