# lit_106 distill report (2026-11-08)

Batch: ferrotti2016, dagostino2018, kiani2023, soltanian2022, coratozanarella2026 (laser family). All five cached
texts match their source rows (page-1 titles checked); none is a correction / erratum; no garbled text layer.
Output: 23 components, 156 metric rows. `merge_component_staging.py data/_staging/components/lit_106 --dry-run`:
+23 components, +156 metrics, errors 0 (the one printed warning concerns another batch's row, `cmp_lit_ni2025b_pimmwc`).
Contract note: the brief named `lit_106_INSTRUCTIONS.md`, which does not exist; `BATCH_INSTRUCTIONS.md` (with the `lit`
addendum) was followed. The brief names this report `lit_106_REPORT.md` (the skill says `BATCH_REPORT.md`).

## Per paper

### ferrotti2016 (9 components, 57 metrics)
- `dbr_laser_p195` / `dbr_laser_p197` (laser.heterogeneous, other): threshold 48 mA, series resistance 7.1 / 4.5 ohm,
  max fiber power 37 / 52 uW (through MZM at max transmission + output GC), emission 1303.5 nm @100 mA / 1315.8 nm
  @150 mA, heater tuning up to 8.5 nm, Fig. 22(b) top heater power 1506 mW (p197 only), period, III-V length / width,
  Si thickness.
- `iii_v_si_mode_transformer` (waveguide_platform.transition): simulated > 90 % coupling, 100 um length, 100 nm gap,
  Si widths 0.6 / 1.55 um, III-V 5 um, stack thicknesses.
- `si_thickness_transition` (500 -> 300 nm Si rib, transition): simulated loss about 1 % (0.044 dB), 65 um, 125 nm tip.
- `bragg_front` / `bragg_back` (reflector.bragg): simulated R about 70 % / about 100 %, front 35-85 % for +/-4 nm etch,
  kappa 79 /cm, lengths 150 / 700 um, 10 nm etch, periods 195-197 nm, duty 0.5, 3 um rib.
- `grating_coupler` 4.2 dB per coupler, `mmi` 0.1 dB, `si_waveguide` 0.8 dB/mm -> 8 dB/cm (loss breakdown of the
  stand-alone MZM run, "estimated from additional measurements on the same wafer": measured; the dB/cm row derived).
- Not entered: Si MZM metrics (ER 6.2 / 18.5 dB static, 3.9 / 7.1 dB dynamic, EO bandwidth 28 / 23 GHz, S21 -6 dB
  25.5 / 14 GHz, simulated 2.14 V cm, transmitter ER 4.7 / 2.9 dB, doped-section loss 1.5 dB/mm, doping loss
  0.7 dB/mm): EO-atlas territory (rule 2), candidate for that atlas. Fiber-to-fiber totals -15 / -18 dB (path totals),
  routing loss 3.4 dB (waveguides + bends, path total). Simulated MQW confinement 16 %, gap-tolerance curve (no
  parameter). Bragg-wavelength shift 6.15 nm per 1 nm period (derived from two lasers, not a component metric).
- Fab empty: passive fabrication sentences (p.18-19), authors at CEA-Leti, STMicroelectronics and INL (szelag2017 /
  D433 precedent). SOITEC named as SOI wafer supplier (note only).

### dagostino2018 (1 component, 10 metrics)
- `ccl_laser` (laser.tunable, inp): threshold 20 mA per SOA, fiber power up to 9 dBm, SMSR > 40 dB (90 mA; and over the
  tuning range at 70 mA), coarse tuning 26 nm measured and 28 nm design (Fig. 7(b) parameters = the fabricated device),
  mode spacing 87 pm, lasing near 1546.3 nm (Fig. 9(b) read), 3.6 mm cavity, 10 um SOA pitch. TEC 15 C on all
  measured rows.
- Fab org_smart_photonics (acknowledged "for the fabrication of the devices"), facility org_nanolab_tu_e (provided the
  fabrication facilities; dagostino2015 precedent). process_name empty: only "generic integration approach" printed.
- Not entered: pi-Michelson test structure (330 um imbalance, Fig. 6): only a normalized reflection plot, its doubled
  FSR (about 0.95 nm peak spacing on the plot) has no reflector parameter; no row. MIR-pi BPM coefficients
  |Cb| 0.79 / |Cx| 0.21 and 70 % resonant-imaging fraction (simulated, no parameter). Linewidth "MHz" (no number).
  Coarse tuning step about 1 nm (no parameter fits).

### kiani2023 (6 components, 49 metrics)
- `tm_disk_laser_r20` / `_r30` (laser.other, other): pump thresholds launched 0.997 / 0.918 mW and absorbed
  0.531 / 0.505 mW (derived, uW -> mW, on-chip via own measured coupling loss, D394), on-chip double-sided power up to
  2 mW / about 2.6 mW (derived, D394), emission 1930 nm (single-mode) / 1872 nm (multi-mode), radius.
- `tm_disk_r20` / `_r30` (resonator.disk, D396 cross-noted): Q_i 9.6e5 / 9.4e5 near 1530 nm and 4.6e5 / 4.8e5 at
  1900 nm (author_estimate, D403: regime only asserted), loaded Q from inset labels (measured), losses 0.60 / 0.54 and
  0.97 / 0.90 dB/cm (author_estimate), FSR 5.0 / 3.53 nm (around 1510 nm) and 8.6 / 5.9 nm (around 1900 nm),
  extinction 3.2 / 3.5 dB, geometry (radius, bus 450 / 400 nm, gap 0.4 um, 20.8 um pulley length, 220 nm Si, 2 um BOX,
  385 nm coating).
- `edge_coupler` (fiber_chip_coupler.edge): 7.0 +/- 0.2 dB per facet (1520-1620 nm), 6.7 +/- 0.1 dB around 1900 nm,
  0.18 um tip, 0.45 um start.
- `teo2_tm_film` (waveguide_platform.other, witness film): <= 0.3 dB/cm at 1510 nm, <= 0.6 dB/cm at 638 nm (prism
  coupling), thickness 320-385 nm.
- Fab org_amf on the Si-based rows ("fabricated on the AMF wafer-scale SOI platform", p.2) with process_name "AMF
  wafer-scale SOI platform, 193 nm DUV"; foundry chip post-processed by the authors (first-person sputtering): the
  authors' org should also be fab (Contract v7 / D419) but is missing from the registry (below). Film row fab empty
  for the same reason.
- Not entered: slope efficiencies 5.9 / 11.3 % (R20) and 6.7 / 12.2 % (R30), bidirectional 13.4 % (no
  optical-slope-efficiency parameter); gap / concentration population of Fig. 9 and the 1825-1939 nm span across
  devices (population, not one device); simulated pulley cross-over ratios (Fig. 2(d)); film refractive indices.
  Author's earlier laser [23] values (580 uW, 16 / 2.5 mW thresholds) are cited, not entered (rule 3).

### soltanian2022 (4 components, 21 metrics)
- `dual_wtl` (laser.tunable, other): 111 nm combined tuning, threshold about 60 mA, differential series resistance
  about 10 ohm, Lorentzian linewidth about 20 kHz at 1530 nm, Vernier FSR about 55 nm (design, author_estimate),
  top waveguide-coupled power about 8 dBm (Fig. 7 read, on-chip after the combiner), SOA coupon length 1 mm. Stage 15 C.
- `ring_r27` / `ring_r29p3` (resonator.ring, D400 intracavity): FSR about 4 nm, loaded Q about 15000, IL about 1.7 dB
  (all design statements from the assumed platform loss, author_estimate), radius, 300 nm gap.
- `si_waveguide` (waveguide_platform.straight): about 1 +/- 0.15 dB/cm (author_estimate, origin not stated), 400 nm Si,
  180 nm etch, 2 um BOX.
- Fab: org_imec on all rows (PICs "fabricated in imec's SiPh pilot line", p.1-2) with process_name "imec SiPh pilot line,
  200 mm SOI, 400 nm Si, 180 nm etch"; org_iii_v_lab added on the laser row (SOA fabrication "carried out by III-V Lab",
  p.3; D515 per-component rule). Printing step passive, no printing org.
- Not entered: III-V/Si adiabatic tapers (180 um, 4 -> 0.6 um) and 50 um Si tapers (geometry only, no performance:
  not a row); 100 pm fine-tuning step; MMI combiner, Sagnac mirror, grating coupler (no values).

### coratozanarella2026 (3 components, 19 metrics)
- `sil_laser` (laser.sil, sin): coarse tuning up to 9.5 nm (about 779-789 nm), free-space output up to 30 mW before
  isolators (ref_plane module), intrinsic linewidth about 0.7 kHz and beta-separation about 506.7 kHz (derived,
  kHz -> Hz), SMSR > 50 dB and about 53 dB (Fig. 2(b) label), emission about 783.3 nm (figure read) and near 780.246 nm
  (Rb set point).
- `mrr` (resonator.ring): loaded linewidth about 1.63 GHz (derived to MHz, 780 nm inferred), power coupling about 10 %
  (design), widths 450 nm / 8 um, 275 nm SiN, 4 um BOX, 2.5 um cladding.
- `fpld` (laser.other, platform empty, D422): commercial FP laser diode, about 90 mW free-running at 120 mA, MFDs
  2.7 / 1.4 um, FSR about 38 GHz.
- Fab org_toptica_photonics (author contributions: the first author, TOPTICA Photonics Inc., fabricated the PICs) and
  facility org_cornell_nanoscale_facility ("performed in part at" CNF) on the laser and MRR rows; FPLD vendor not
  named -> fab empty.
- Not entered: about 50 GHz mode-hop-free fine tuning and 10-15 GHz per band (no GHz tuning parameter for laser);
  48 h lock deviation about 25 MHz (wavemeter-limited, not a device metric); chip layout labels visible in the Fig. 2(b)
  micrograph (k2 = 10 %, FSR = 38.00 GHz, tip = 100 nm: layout text, not figure annotations); SWaP comparison and
  device characterization in Supplement 1 (not cached). Platform loss cited from Ref. [10].

## Missing fab / facility orgs (registry check: organizations.csv + org_aliases.csv)
1. McMaster University (Hamilton, ON, Canada) - fab (first-person TeO2:Tm3+ post-processing of the AMF chips),
   kiani2023 p.2 Sec. 2; would join org_amf on the 5 Si-based rows and be the only fab on `teo2_tm_film`.
2. Centre for Emerging Device Technologies (CEDT) at McMaster University - facility (support with the reactive
   sputtering system), kiani2023 p.11 Acknowledgments; parent McMaster University. All 6 kiani2023 rows.
3. TOPTICA Eagleyard Photonics GmbH (Berlin, Germany) - fab for the butterfly packaging of the PIC-laser (author
   contributions name the packaging author, D399), coratozanarella2026 p.9; `sil_laser` row.
- Present and used: org_smart_photonics, org_nanolab_tu_e, org_amf, org_imec, org_iii_v_lab, org_toptica_photonics,
  org_cornell_nanoscale_facility. Wafer supplier SOITEC (org_soitec exists) kept as a note only (ferrotti2016).

## Judgment calls
1. ferrotti2016 Bragg mirrors: one row per mirror type (front / back) with period 195-197 nm as a range, since Table 1
   prints identical reflectivity / kappa / length / etch for both periods; the lasers are split per period (different
   measured values).
2. ferrotti2016 grating coupler / MMI / waveguide losses come from the stand-alone MZM run on another wafer of the same
   process; entered on generic rows with that provenance in notes. Wavelengths inferred as O band.
3. ferrotti2016 1506 mW heater power tied to the 8.5 nm maximum shift by the largest legend entry (extracted_from_figure).
4. ferrotti2016 thick-to-thin Si transition classed `waveguide_platform.transition` (two Si thickness levels; not
   inter-material). Simulated 1 % loss stored as 0.044 dB, basis kept simulated.
5. dagostino2018 Fig. 7(b) design (L1 = 3.6 mm, 25 um imbalance -> 28 nm) entered as simulated on the fabricated row
   because the fabricated device uses exactly these parameters (p.12-13).
6. kiani2023 Q_i and losses author_estimate (D403: "under-coupled" asserted, not shown); loaded Q inset labels entered
   as measured. 30 um / 1900 nm Q_i: text 4.8e5 vs inset 4.9e5, text kept (D417).
7. kiani2023 extinction 3.2 / 3.5 dB printed "at the laser wavelength" but used to compute the absorbed pump fraction;
   kept as printed with the ambiguity in condition / notes.
8. kiani2023 hybrid rows (disk, laser, edge coupler) platform `other` (Si core coated with TeO2:Tm3+; the gain stack is
   not plain SOI). Fab org_amf kept although the chips were post-processed (Contract v7: benchmark excludes such rows).
9. soltanian2022 one laser row for the combined double laser: threshold and series resistance are printed jointly for
   laser 1 and 2 (D159 / D254 avoided by not splitting). Ring design Q / IL / FSR entered on both radii because the
   sentence states them for the ring design generally.
10. coratozanarella2026 FPLD entered as its own row (purchased device characterized: power, MFD, FSR) with fab and
    platform empty; laser row platform `sin` (laser.sil precedent).

## Registry gaps (skipped value + locator + proposed definition)
1. `optical_slope_efficiency_pct` (laser, amplifier): kiani2023 5.9 / 11.3 % (R20) and 6.7 / 12.2 % (R30) single-sided,
   13.4 % bidirectional, p.8-9 Sec. 4.2 / p.10 Sec. 5; shui2026 2.76 % precedent. Definition: "slope of laser output
   power vs optical pump power (W/W, in %), pump reference (launched / absorbed) and output (single / double-sided) in
   condition".
2. `mode_hop_free_tuning_ghz` (laser): coratozanarella2026 about 50 GHz (p.3 Sec. 3, Fig. 3(b)); 10-15 GHz per band
   (Fig. 3 caption). Definition: "continuous (mode-hop-free) frequency tuning span, actuator / feed-forward scheme in
   condition".
3. `fsr_nm` on reflector (or wdm.other for reflective interferometers): dagostino2018 pi-Michelson doubled FSR (Fig. 6,
   p.10; figure-only, about 0.95 nm) - low priority, figure read only.
4. `center_wavelength_nm` on reflector (D433 candidate already listed): ferrotti2016 design Bragg wavelengths
   1303.3 / 1315.7 nm (Table 1, p.9; text prints 1302.6 / 1316 nm).
