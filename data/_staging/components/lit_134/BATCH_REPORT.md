# lit_134 batch report

Distilled 2026-11-15. Papers: lit:zhang2019c, lit:yu2025a, lit:yang2020a, lit:zhou2024, lit:park2007.
Validation: `merge_component_staging.py data/_staging/components/lit_134 --dry-run` -> +21 components, +68 metrics,
0 errors. The only warning concerns merged rows of another batch (ni2025b).

| paper | components | metric rows |
|---|---|---|
| zhang2019c | 8 | 28 |
| yang2020a | 9 | 17 |
| park2007 | 2 | 15 |
| yu2025a | 1 | 6 |
| zhou2024 | 1 | 2 |
| total | 21 | 68 |

Page-1 title check: all five cached texts are their source rows' papers. yang2020a is arXiv v1 with a different title
("Inverse-designed photonic circuits for fully passive, bias-free Kerr-based nonreciprocal transmission and routing")
than the Nature Photonics source row; same authors and content, accepted as the same work (D430 / D433), noted on the
rows.

## zhang2019c (Optica 2019, monolithic Ce:YIG isolators, arXiv text)

Rows: Si TM MZI isolator, Si TE MZI isolator, SiN TE racetrack isolator, SiN TE MZI isolator (nonreciprocal.isolator);
MMI 3-dB coupler (splitter.mmi), bare-to-garnet window junction (waveguide_platform.transition), garnet-covered MO
waveguide and bare Si waveguide sections (waveguide_platform.straight).

- Isolation, IL and 10-dB / 20-dB isolation bandwidths measured. Si MZI IL `de_embedded` / `reference_structure`
  (Fig. 3(a), (b) plot a reference Si waveguide on the same chip; the -25 vs -30 dB levels match the 5-6 dB IL). SiN ring
  and SiN MZI IL scope `unspecified` (reference not stated).
- SiN ring isolation wavelength not printed: about 1584.86 nm read off Fig. 4(c)-(d), `wavelength_inferred`.
- p.13 loss budget (MMI 0.7 dB, junction 0.25 dB, MO waveguide 2.2-3.2 dB, bare Si 0.36 dB) entered as
  `author_estimate` / `loss_breakdown`: "parameterized in Supplementary Section 7", which is not in the cached text; no
  measurement shown. Wavelength set to the TM operating point 1574.5 nm with `wavelength_inferred`.
- Footprints derived from the printed mm x mm products.

Not entered: simulated return loss upper limit -24.4 dB (p.8; `back_reflection_db` not allowed for nonreciprocal);
NRPS values (simulated 16.2 / 18.9 rad/cm, measured TE 3.6 rad/cm vs designed 14 rad/cm, p.6 / p.8: printed conflict
16.2 vs 14, D417 note); nonreciprocal resonance shift 15 +/- 2 pm (p.10, no parameter, bi2011 precedent); SiN racetrack
radius 150 um, straight 150 um, gap 1500 nm (radius / gap not allowed for nonreciprocal, and no Q / FSR is printed for a
resonator.ring twin); field stability up to 150 Oe; film Faraday rotation; Table 1 rows of other works (rule 3).

Fab / facility: fab `org_mit` (author contributions p.20: Y.Z. (UESTC + MIT) and Q.D. (MIT) fabricated the isolators;
MIT is the org common to both, D395 / D452). Film deposition by C.W. (UESTC) and T.F. (MIT), site not stated: UESTC not
entered (judgment call for the auditor). Missing facility org: "Shared experimental facilities of CMSE, an NSF MRSEC
under award DMR1419807" (p.19-20 Acknowledgements), facility role, parent MIT (also reported by lit_104 du2018, D535).
SOI wafers from MTI Corp.: supplier note.

## yang2020a (Nature Photonics 2020, Kerr Fano isolator / router, arXiv v1 text)

Rows: Fano isolator (Fig. 1), its racetrack as resonator.ring (D396), the R = 56 % partially transmitting element and
the R = 94 % Lorentzian element (reflector.other), the 4-port isolator-router (nonreciprocal.other, song2025a
precedent), two single-resonator designs (Fig. 3(c) panels 1 / 2) and two cascaded Fano-Lorentzian isolators (panels
3 / 4, delays 44 / 43.75 um).

- Fig. 1 device: isolation best 24.7 dB and mean 21.9 dB (minimum 13.4 dB in the condition), IL 1.3 dB
  (`de_embedded`, normalized to a straight waveguide with grating couplers, p.6 Methods). Loaded Q 7.3e3 (Fano fit,
  measured).
- Reflectivities 56 % / 94 % `simulated`: the figures show only simulated optimization trajectories next to the
  labels; no measured reflectivity. Methods 60 / 80 / 99 % targets not tied to a device: notes.
- Single / cascaded devices: IL `derived` from the printed T (0.96, 0.82 in text and labels; 0.99, 0.98 panel labels).
  The text's shared "95 - 99 % (0.04 - 0.22 dB)" for both cascades and the "T > 99 % over NRIR > 6 dB" claim are notes
  only (D254); Fig. 3(b) puts the panel 3 device near T = 0.95 against its 0.99 label (D417 note).
- Router: three values read off Fig. 2(b) at 500 dpi (`extracted_from_figure`, +/- 0.3 dB): S12 about -2 dB, S21 about
  -19 dB (contrast about 17 dB, same definition as the Fig. 1(b) arrow), S23 about -12.7 dB. Fig. 3(b) places this
  device near T = 0.6, consistent. Auditor may prefer to drop figure reads.

Not entered: every NRIR value (3.9 / 5.5 / 0.1 / 3.1 / 2.9 / 6.3 dB; no parameter; the Fig. 1 printed operating range
4.55-8.15 dBm spans 3.6 dB, not 3.9, D417 note); Methods gap 200 nm / interaction length 18.3 um / PTE offset 2.28 um
(not tied to one device while the single-resonator series varies the gap, D159); ranging to 60 m, 0.02 m std (system).

Fab / facility: fab `org_stanford_university` (contributions p.7: K.Y.Y. and J.S. fabricated with assistance, D395);
facility `org_stanford_nanofabrication_facility` + `org_stanford_nano_shared_facilities` ("fabricated in" both, p.7;
pre-merger names, D80d / D448). No missing orgs.

## park2007 (IEEE PTL 2007, hybrid AlGaInAs-Si evanescent amplifier)

Rows: hybrid SOA (amplifier.soa, platform `other` like the merged bonded III-V-on-Si SOAs davenport2016 /
keyvaninia2012) and its angled AR-coated facet to a lensed fiber (fiber_chip_coupler.edge, platform empty because the
stack at the facet is not stated).

- Judgment call: the 5 dB per-facet coupling is printed as "measured ... from the measured insertion loss of 20 dB at
  long wavelengths", but 2 x 5 dB leaves 10 dB of in-device loss the paper never states. Entered `author_estimate` /
  `loss_breakdown` (D428 / D437), and the chip-referred rows that rest on it (13 dB chip gain, 11 dBm Psat, 5-8 dB
  internal NF) are `author_estimate` too. Alternative under D166 / D167: `measured` for 5 dB and `derived` for the
  dependent rows. The 3 dB fiber-to-fiber gain, 20 dB IL and 10-13 dB NF are `measured`.
- 11 dBm Psat additionally lies just past the Fig. 4(a) data (points end near 10.45 dB gain, D435).
- 62 nm gain FWHM entered as `gain_bandwidth_nm` with the FWHM criterion (bw_fwhm_nm not allowed for amplifier, the
  paper does not equate FWHM with 3 dB).
- Fig. 5 NF points (about 13.5 / 10.3 / 9.8 dB) sit slightly outside the printed 10-13 dB range (D417 note).
- 7.5 ohm series resistance `author_estimate` (no measurement shown).

Not entered: thermal impedance 40 K/W (laser-only parameter); residual facet reflectivity 5e-4 (no amplifier
reflectivity parameter); material-gain fit g0 / Jtr; 70 % injection efficiency and 15 cm-1 loss (cited from ref. [3],
rule 3); calculated confinement and Psat curves; projected > 20 dB gain; AR coating "(~5%)" (meaning not stated).

Fab / facility: fab empty (passive fabrication sentences; authors UCSB + Intel; sample-preparation thanks to two named
people without an org, D84b needs the org). No facility named. No missing orgs.

## yu2025a (APL 2025, UV quantum frequency conversion, arXiv text with supplement)

Row: PPLN ridge-waveguide DFG converter 369 -> 456 nm (frequency_converter.sfg_dfg; in scope as a chip-scale waveguide
converter, yang2026 / kazama2021 precedents). Platform empty (ridge type and stack not stated, D422); fab empty (source
not stated).

- 41.4 % conversion rate at 82 mW coupled pump `measured` (Eq. (1) fit at the operating point, inside the data range);
  Table S2 best point 44.44 % at 83.86 mW added as `best` (the "up to 41.4 %" wording conflicts with it, D417 note).
- 49 % peak at 152 mW `author_estimate` (fit beyond the 99.96 mW data range, D435). Photon-number rate 51.2 % `derived`
  (authors' frequency-ratio conversion). 795.3 %/W low-power slope `measured` (fit of own data). Poling period 2.9 um.

Not entered: waveguide coupling 20 % (369 nm) / 50 % and 54 % (pump) (coupling_efficiency_pct not allowed for
frequency_converter); 1.434 % / about 1 % overall QFC efficiency (setup level: objective transmission, fiber coupling);
> 70 % efficiency retention over 10 h; 456 nm output powers; g2(0) and lifetime results.

Fab / facility: none stated. No missing orgs.

## zhou2024 (HPLSE 2024, MIR dual-comb via IPDFG in chirped PPLN)

Row: input facet of the chirped PPLN waveguide butt-coupled from a PM HNLF (fiber_chip_coupler.edge, kazama2021
precedent): coupling efficiency 60 % `measured` (stated directly, D167), band 1-2 um inferred from the launched
supercontinuum; width 15 um.

The PPLN converter itself is not a row: its stated outputs (0.7 mW MIR power, 2.4-4.2 um idler span, integrated RIN
0.87 %) have no frequency_converter parameter, so a converter row would be geometry-only (rule 9). Waveguide length
25 mm and periods 23-32 um ("consistent with our previous study [35]") kept in core_material. HNLF, prisms, EDFA and
the dual-comb system are setup. Fab / facility: none stated; platform empty (D422). No missing orgs.

## Missing orgs

| name as printed | role | locator | rows |
|---|---|---|---|
| Shared experimental facilities of CMSE, an NSF MRSEC (MIT) | facility | lit:zhang2019c p.19-20 Acknowledgements | all 8 zhang2019c rows |

## Registry gaps (skipped value, locator, proposed definition)

- Nonreciprocal intensity range (NRIR) for Kerr isolators: yang2020a 3.9 / 5.5 / 0.1 / 3.1 / 2.9 / 6.3 dB (p.3-6,
  Fig. 1(b), 2(b), 3(c)); `nonreciprocal_power_range_db` = ratio of input powers over which the device isolates
  (nonreciprocal; white2022 isolation threshold is related).
- Nonreciprocal resonance shift: zhang2019c 15 +/- 2 pm (p.10); `nonreciprocal_shift_pm` (nonreciprocal; bi2011 / du2018
  precedents also skipped it).
- NRPS: zhang2019c measured 3.6 rad/cm (p.8); `nrps_rad_per_cm` (nonreciprocal / phase_shifter).
- back_reflection_db (return loss) on nonreciprocal: zhang2019c simulated -24.4 dB upper limit (p.8) (also D535).
- radius_um / gap_nm on nonreciprocal (ring isolators): zhang2019c 150 um / 1500 nm (p.10) (D535 lists radius).
- thermal_resistance_k_per_w on amplifier: park2007 40 K/W (p.2).
- Amplifier facet residual reflectivity: park2007 5e-4 (p.3); `facet_reflectivity` (amplifier, laser), linear.
- coupling_efficiency_pct on frequency_converter (lens-coupled input of a nonlinear waveguide): yu2025a 20 % / 50 % /
  54 % (p.2, p.10 Supp.).
- Frequency-converter output power and output span: zhou2024 0.7 mW MIR (p.4), 2.4-4.2 um (p.5); integrated RIN of a
  converter output 0.87 % (p.5) (rin_integrated_pct is laser-only).
