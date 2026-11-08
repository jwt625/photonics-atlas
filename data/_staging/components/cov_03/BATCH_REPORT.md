# cov_03 batch report (2026-11-07)

Papers: beals2026, ji2020, ma2000, masanovic2003, rizzo2023, sun2024, tian2025, yu2016. All eight cached texts match their source rows (page-1 title); none is a correction, an erratum or another paper. Three are not the version of record: ji2020 is the authors' manuscript of the LPR article, tian2025 is the Research Square preprint v1 of the OQE article, and yu2016 is the arXiv v1 of the Optica article (accepted as the same works, D430 / D433 precedent; noted on the rows). No source has `garbled_text_layer`. The ma2000 and masanovic2003 text layers lose symbols and numbers next to Greek or italic glyphs, so their values were read from the page renders. No existing rows of these sources were in `data/components/`. Dry run: +26 components, +117 metrics, 0 errors. The one warning (ni2025b m18 / m4) is on an existing merged row, not from this batch.

| paper | components | metrics |
|---|---|---|
| beals2026 | 3 (resonator.other 2; laser.comb 1) | 13 |
| ji2020 | 2 (resonator.ring 1; laser.comb 1) | 10 |
| ma2000 | 3 (splitter.mmi 3) | 27 |
| masanovic2003 | 1 (splitter.mmi 1) | 8 |
| rizzo2023 | 9 (laser.comb 1; fiber_chip_coupler.edge 3; waveguide_platform.straight 1; resonator.disk 1; phase_shifter.thermo_optic 2; wdm.interleaver 1) | 23 |
| sun2024 | 4 (resonator.other 1; resonator.ring 1; laser.comb 1; photodetector.other 1) | 17 |
| tian2025 | 2 (splitter.other 2) | 12 |
| yu2016 | 2 (resonator.other 1; laser.comb 1) | 7 |

## Fab statements and orgs

- beals2026: K.J.M. (Columbia EE) fabricated the devices (p.8 Author contributions), plus 'We fabricate' (p.9). Fab = org_columbia_university. Work was performed in part at the Cornell NanoScale Facility (p.8), so facility = org_cornell_nanoscale_facility.
- ji2020: 'we fabricate' both resonator types on one wafer (p.4), and all authors are at Columbia. Fab = org_columbia_university; facility = Cornell NanoScale Facility (p.6).
- ma2000: the only statement is 'our design, fabrication' and measurement (p.1). All authors are at Northwestern ECE. Fab = org_northwestern_university, which is borderline (question 1). The paper made use of the "MRSEC Control Facilities of Northwestern University" (p.1 footnote; facility). This facility is missing from the registry.
- masanovic2003: 'We fabricated the new splitter' (p.2), and all authors are at UCSB. Fab = org_ucsb. No facility is named.
- rizzo2023 (AIM-fabricated): the Si transmitter and receiver chips were fabricated "through the AIM MPW service" in "a commercial 300-mm foundry" (p.2, p.4). Methods (p.11) say fabrication was done as part of the AIM Photonics 300-mm MPW, and AIM Photonics is thanked for chip fabrication (p.13). Fab = org_aim_photonics (D398); the foundry itself is not named. The Si3N4 comb chip was fabricated by X.J. (Columbia; p.13 Author contributions; 'we thermally grew ...' p.11), so fab = org_columbia_university, and the Cornell NanoScale Facility is the facility (p.13). Optelligent did the packaging (p.12); it is a packaging org, not a fab org, and it is missing from the registry. Analog Photonics is thanked only for PDK support (not entered).
- sun2024: Ligentec is acknowledged for SiN microresonator fabrication (p.7), so fab = org_ligentec on the ring and comb rows. The CC-MUTC PD was "designed and fabricated" by J.S.M. and A.B. (UVA; p.7 Author contributions), and Freedom Photonics is acknowledged for MUTC PD fabrication (p.7). Fab = org_university_of_virginia;org_freedom_photonics (D80b, two orgs). The coil cavity's fabricator is not stated, so its fab field is empty.
- tian2025: made "in a nanofabrication facility at SiPhotonIC Technologies in Denmark" (p.4 Sec. IV; p.5 Acknowledgment). SiPhotonIC is missing from the registry; fab is not entered.
- yu2016: no fabrication statement (the device is described in ref. [14]). Facility = Cornell NanoScale Facility (p.7).

## Missing orgs (name as printed + locator)

- SiPhotonIC Technologies (Denmark): tian2025 p.4 Sec. IV and p.5 Acknowledgment. Fab org candidate (company) for both tian2025 rows.
- MRSEC Control Facilities of Northwestern University: ma2000 p.1 footnote ('made use of'). Facility candidate, parent org_northwestern_university, for the 3 ma2000 rows.
- Optelligent: rizzo2023 p.12 Methods and p.13 Acknowledgements. Packaging company; it would not be entered on these rows under the current rules.

## Not entered, and why

beals2026
- Thermal nonlinear coefficient ~72 W^-1 m^-1 (p.3, Fig. 2(e)), heat transfer coefficient 1.9 x 10^3 W m^-1 K^-1 (p.9), and dispersion beta2 -40 / -32.8 ps2/km (Ext. Fig. 1(c),(f) fit labels): no registry parameter.
- Minimum pump power to reach the soliton regime: 232 mW (active kick) vs 627 mW (heater kick) (p.5 Fig. 3(a)). This depends on the technique and is not an OPO threshold (question 2).
- Soliton existence time up to 4.2 days vs 50 ms (p.4-5), breathing frequency ~350 MHz, soliton number up to ~50, automation 50 of 50: no parameter (in notes).
- The LLE simulation inputs (FSR 16.0367 GHz, alpha, theta, L = 8.8757 mm, p.11) are simulation parameters.
- Minimum arm spacing (50 / 20 um): no resonator parameter (in notes). Supplementary Information (heater calibration, thermal paste) is not cached.

ji2020
- Comparison constant-radius ring (R 131 um, same FSR): only a transmission spectrum showing HOM dips (Fig. 2(c)), no performance value, so no row (rule 9).
- Comb span 1097-2040 nm (126 THz): no parameter. Simulated ~95 % fundamental-mode power and ~7 dB HOM suppression (p.3, Fig. 1(c)), and the GVD design curve (Fig. 4(c)): no parameter, in notes.
- Background-intensity sensitivity limit of 4 %: measurement limit.

ma2000
- No absolute excess loss is given: Fig. 2 is normalized to the output at the 1.55 um optimum (p.2), so only the 1-dB width (MMI3) is entered. The 2-dB (MMI2) and 4-dB (MMI1) widths of about 80 nm have no parameter.
- MMI2 width: the text says 3 um (p.1) but Table I says 3.2 um for W_AG 0.6 um. Not entered (D159); the conflict is in the notes.
- Table I calculated lengths, the TM optimum length (48.5 um), and the length / width tolerances (8 / 0.26 um and 2 / 0.1 um): in notes.
- TE-TM excess-loss difference below 1 dB "for most of the device lengths" (Fig. 3): not a single-device PDL value.
- S-bend loss estimated below 0.05 dB (p.2): an estimate for a part with no data of its own.

masanovic2003
- Standard 1x2 MMI splitter (780 um, same output spacing): near-field image only, so no row.
- MMI-1 / MMI-2 widths of the fabricated device are not printed. The access width X = 2 um and the 50 % reduction come from a design calculation (Fig. 2), not the fabricated device.
- Fig. 4(a) minimum excess loss (~0.3 dB near 1550-1565 nm) essentially equals the simulated inherent loss by construction (Eq. 5), so it was not read.

rizzo2023
- Modulator metrics: EO bandwidth 15 GHz at 0 V, 80 pm/V, ER / IL trade-off (Ext. Data Fig. 2(b),(c),(e)). These are modulator properties outside the component classes. The microdisk's Q / linewidth / FSR are on a resonator.disk row (jayatilleka2021 precedent).
- Receiver microring add-drop filters and Ge PDs: no quantitative filter or PD value in the main text (the Supplementary Notes are not cached).
- PDK splitters (three-port and four-port 3 dB), crossing and thermo-optic phase shifter of Fig. 3(d): images only.
- Chip sizes (4.15 x 1.1 mm transmitter, 3.1 x 1.1 mm receiver) and the 465 Gb/s/mm shoreline density: link-level values, not component metrics.
- Comb: "25 lines with on-chip power above -3 dBm" (p.2) is inferred by the authors from the 3 dB coupler loss. The 41 % conversion efficiency of similar devices is cited (ref. 27). The resonator Q of the comb rings is not printed.
- Two-channel crosstalk power penalty < 1 dB (p.6): a link penalty, not a component crosstalk value.

sun2024
- Optical 3-dB comb bandwidth 4.6 THz (no parameter in THz; not converted to nm). Phase noise of -114 / -115 dBc/Hz at 10 kHz (100 GHz carrier): no parameter.
- PD mmWave output power of 9 dBm at 100 GHz (18.3 mA, -2 V; Fig. 4(d)): no PD RF output-power parameter (registry gap below).
- Reference lasers, extended-DBR pump laser and VCOs: purchased setup equipment (rule 13).

tian2025
- Coupling-loss standard deviation over the central 8 channels: 0.269 dB (squeezed) vs 0.701 dB (conventional), i.e. normalized-power std 0.057 vs 0.129 (p.5). The headline metric has no registry parameter (registry gap below). Max-min non-uniformity was read from Fig. 6 instead (0.7 dB / 2.1 dB, extracted_from_figure).
- Simulated coupling efficiencies (62.53 % / 49.07 %) and coupling-efficiency non-uniformity (0.6407 / 1.0125): coupling_efficiency_pct is not allowed for splitters. The equivalent simulated losses 2.039 / 3.092 dB are entered.
- FPR length 8 um (fpr_length_um is wdm-only), auxiliary taper widths / lengths (Table I), and the 14 x 4 um coupling region: in notes. The lower layer is printed as a 3 um thick "silicon substrate", so box_thickness_um is not entered.
- Edge coupler loss of 2 dB (in and out, origin not stated): used only as the excluded term.

yu2016
- PIN-based detector bandwidth 13 GHz at -15 V (p.3): rests on the free-carrier lifetime of ref. [42], so it is cited (rule 3).
- Comb span 2.4-4.3 um (70-121 THz): no parameter. The 35 mW soliton pump power at 2.8 um and the bias tuning path: in notes.
- Simulation inputs (GVD -102 ps2/km, 3PA coefficient, FCA cross section): simulation parameters.

## Judgment calls

1. Spiral and coil resonators are resonator.other (heim2025 precedent): the beals2026 Euler spirals and the sun2024 4 m coil. The ji2020 tanh-bend multimode resonator is resonator.ring (a closed single loop with a variable radius; radius_um is not entered, min_bend_radius_um 80). The yu2016 microresonator is resonator.other with an empty platform, because this text does not state the shape or the substrate stack (D422 / D423).
2. Kerr / soliton combs are a laser.comb row beside the resonator row (D396; wilson2019 / wang2021 precedent). Line spacing follows D83b: beals2026 and sun2024 use repetition_rate_ghz (they call it repetition rate and detect the RF tone); rizzo2023 and yu2016 use channel_spacing_ghz (line / mode spacing, no pulse characterization).
3. beals2026 repetition rate 16.0328 GHz is read from the printed RF-axis offset of Fig. 1(d), with the tone at 0 MHz (extracted_from_figure, +/- 5 MHz).
4. Intrinsic Q and intrinsic linewidth are author_estimate throughout (D403): no paper determines the coupling regime from the data. The exception is yu2016, which gives only a loaded Q. Its overcoupled regime is verified, but only the loaded Q is stated.
5. ma2000: the Fig. 2 normalized excess-loss bandwidth with a 1 dB limit (MMI3) is entered as bw_1db_nm, because the normalization is to the peak at the optimum wavelength. Imbalance "within +/-0.5 dB" is entered as imbalance_db 0.5 le for each MMI, polarization both (the text states TE and TM).
6. masanovic2003: the measured excess loss of Eq. (5) adds the BPM-simulated inherent loss (0.29 dB), so it is author_estimate. The 80-nm window edges are not printed, so wavelength_nm / wavelength_max_nm hold the Fig. 4(a) span (1510-1600 nm, inferred) and the condition says so. The imbalance span 1500-1600 nm is the Fig. 4(b) axis (100 nm stated).
7. rizzo2023 packaged coupling loss of 2.5 dB/facet is entered as loopback_half derived: the only stated isolation is Ext. Data Fig. 2(f) (5 dB across a coupler pair). The bare-die lensed-fibre 5 dB/facet is on a separate row, because the chip differs and identity with the packaged coupler is not stated (D159). The coupler platform is empty (layer not identified for this chip).
8. rizzo2023 AIM waveguide ~2.5 dB/cm is author_estimate (process value, origin not stated). The microdisk heater 0.5 nm/mW became 500 pm/mW (derived, unit conversion). The p_pi_mw values (25.6 mW microdisk, 25 mW RMZI arm) are entered as printed; C band is inferred from the figure axes.
9. sun2024 coil and ring values: the sentences cite refs. 9 / 10, 12 for the device type, but the values are presented as this device's. They are entered as this work's (D80i borderline, question 3). The PD responsivity and bandwidth are stated without the measurement shown, so they are entered as measured with a note. Ref. 44 (the group's 110 GHz design) has different values, so these are not copies of it.
10. tian2025: the total insertion loss excluding the edge couplers is a 1x10 total-power loss, so it goes in excess_loss_db. It is author_estimate because the subtracted 2 dB edge-coupler term has no stated origin. The squeezed device's channels 5-8 are mirrored from 1-4 (stated defect), noted on each row.
11. yu2016: pump-to-comb efficiency 40 % = 32 mW / 80 mW, entered as derived (D80a). Reference planes of the threshold and output power are not stated (ref_plane unspecified / empty).

## Registry gaps (value skipped + locator + proposed definition)

- `loss_std_db` (splitter, wdm): standard deviation of the per-port insertion loss across output ports, in dB. Skipped: tian2025 p.5 values 0.269 / 0.701 dB (and the normalized-power std 0.057 / 0.129).
- `bw_2db_nm` / a generic `bw_xdb_nm` with the level in condition (splitter, coupler): full width within X dB of the peak. Skipped: ma2000 p.2 MMI2 (2 dB, ~80 nm) and MMI1 (4 dB, ~80 nm).
- `comb_span_thz` (laser.comb): optical span of a comb, with its definition (3-dB, -X dBm, full) in condition. Skipped: ji2020 p.4 (1097-2040 nm, 126 THz), yu2016 p.4 (70-121 THz), sun2024 p.2 (3-dB 4.6 THz). This is also recorded in earlier batches (wang2021 notes).
- `gvd_ps2_per_km` (resonator, waveguide_platform): measured group-velocity dispersion beta2. Skipped: beals2026 Ext. Fig. 1(c),(f) (-40 / -32.8 ps2/km).
- `rf_output_power_dbm` (photodetector): RF power delivered at a stated frequency and photocurrent. Skipped: sun2024 p.4 Fig. 4(d) (9 dBm at 100 GHz, 18.3 mA, -2 V).
- `thermal_nonlinear_coeff_per_w_per_m` (resonator): thermal nonlinear coefficient. Skipped: beals2026 p.3 (~72 W^-1 m^-1, 16 GHz device). Low priority.

## Questions for the coordinator

1. ma2000 fab: the only statement is 'our design, fabrication' and measurement (p.1), and all authors are at Northwestern. Entered as org_northwestern_university (read as "our process", D84a). Recommendation: keep. Empty it if the coordinator reads it as a "we developed"-type phrase (D80b).
2. beals2026: should the minimum pump power for soliton access (232 mW active kick vs 627 mW heater kick, Fig. 3(a)) go in pump_threshold_mw with the technique in condition? Recommendation: no. It is a control-technique figure of merit, not a device threshold, so keep it in notes.
3. sun2024 coil / ring values sit in sentences that cite refs. 9 / 10, 12 (device-type citations of the same groups). Entered as this work's (D80i borderline). Recommendation: keep. The 1550 / 1600 nm pair and the 100 GHz FSR match this experiment.
4. rizzo2023: should Optelligent (packaging, p.12) be registered as an org for a future packaging-role field? Recommendation: register it as a company with no role on these rows.
5. tian2025 registry gap `loss_std_db`: recommendation is to add it. Star-coupler and AWG papers commonly report non-uniformity as a std, and max-min readings from figures are less precise.
