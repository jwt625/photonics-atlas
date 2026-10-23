# Batch lit_07 report (distill subagent, 2026-10-23, condensed by the coordinator)

Dry-run `batch lit_07: +44 components, +205 metrics; errors 0`. Quotes only for open_license_ok (liu2022,
riemensberger2022). Not yet audited or merged (paused by the owner).

## Per paper (components / metrics)

- liu2022 (7 / 32): 21 cm Er:Si3N4 EDWA (on-chip net gain 30 dB, off-chip 24 dB, on-chip output 21.6 / 17.78 dBm, PCE
  ~30 / ~60 %, NF 7.1 dB fiber-referred); 50 cm EDWA 55 mW (17.40 dBm derived); gain-coefficient reference waveguides (one
  row, three Er concentrations, D165); Er-doped 100 GHz ring (kappa_0, losses author_estimate); 0.5 m spiral (OFDR);
  UHNA7 edge coupler (2.9 / 3.3 dB per facet, back-reflection derived); implant-boundary transition (simulated). Fab
  org_epfl, facility CMi. Not entered: Psat,in (Fig. S8(c) mixes two amplifiers, D159), comb-amplification gains (sample
  unclear), model values, Kerr comb resonators (setup sources, D160).
- riemensberger2022 (3 / 16): CW Si3N4 parametric amplifier 2 m spiral (peak gain 12 dB, net fiber-to-fiber le 2 dB
  derived, gain bandwidth 20 nm); spiral waveguide (0.025 dB/cm best, power handling > 38.45 dBm, ng author_estimate,
  geometry); inverse-taper edge coupler 2.5 dB per facet. Fab org_epfl, facility CMi. Supp. Table I row not entered
  (conflict with main text).
- tao2024 (3 / 11): strip-loaded NP-PMMA EDWA (internal net gain 17.7 / 4.0 dB derived, D166; gain bandwidth 60 nm);
  cutback waveguide 1.8 / 4.3 dB/cm; G657A butt facet 6.34 / 3.94 dB per facet. Fab org_jilin_university.
- akin2024 (5 / 15): InGaP SHG waveguide (128,000 %/W/cm2, 3280 %/W, 170 pm/K); InGaP waveguide 0.8 dB/cm author_estimate;
  R = 5 um ring (Qi ~6e5 / 1-2e5); ring radius series (D165); resonant ring SHG 440,000 %/W. Fab UIUC. Not entered: SPDC
  (D250), cited coupler efficiencies, tuning range (gap).
- lu2020 (1 / 12): Si3N4 photo-induced SHG microring (2,500 %/W, absolute 22 % / ~36 %, Qi / QL pump and SH, pm/K,
  geometry). Fab empty (passive).
- suntsov2021 (2 / 11): APE/RPE diced PPLN ridge SHG (510 %/W, ~25 / 49 %/W/cm2 derived, ~70 % conversion, period 18.2
  um); ridge waveguides 0.15 / 0.27 dB/cm. Fab empty (Helmut Schmidt University missing).
- white2024 (5 / 11): ULS Kerr ring isolator (14 dB derived; 17.7 dB extracted_from_figure); ULS ring linewidth 69.2 MHz;
  conventional ring 15 dB at 185 mW; free-running DFB 51 kHz; self-injection-locked hybrid 89 Hz (laser.sil). Fab
  Stanford + UW (D80b), facilities SNSF / SNF ("performed at"). Supplementary not cached.
- yan2024 (7 / 26): MO MZI isolator / 4-port circulator TM (isolation 28 dB, crosstalk, IL 2.7 dB, 20-dB isolation
  bandwidth 29 nm, heated values, simulated 240 nm), design rows, 400 nm SiN waveguide 0.4 dB/cm, SiN to MO-SiN junction,
  adiabatic 3-dB coupler. Fab empty (unnamed foundry). CeYIG thickness 130 vs 150 nm noted.
- zhang2017 (3 / 14): Bi:TIG and Ce:YIG Faraday-rotation isolators on SOI (11 / 8 dB, losses 3.8 / 4.6 dB, all
  author_estimate: idealised waveplate assumption); SiO2-clad SOI waveguides 11.2 TE / 14.7 TM dB/cm. Fab empty (Glasgow,
  Minnesota missing).
- liu2018 (8 / 57): graded-SiGe Bragg gratings (rejection 21.6 dB; ~9.3 / 11.5 dB extracted_from_figure; simulated kappa),
  three Fabry-Perot resonators (resonator.bragg; bw3dB, QL derived, transmission), two Bragg mirrors (reflectivity
  author_estimate). Fab empty (C2N platform facility missing). Not entered: cited 3 dB/cm and values computed from it.

## Orgs missing

University of Surrey Ion Beam Centre (liu2022 Supp. Note 2, facility; parent exists); Helmut Schmidt University Hamburg
(suntsov2021, fab); University of Glasgow, University of Minnesota (zhang2017, fab); James Watt Nanofabrication Centre
(staff thanks only); Minnesota Nano Center (borderline); Plateforme de Micro-Nano-Technologie / C2N (liu2018, facility,
"performed at").

## Judgment calls for the audit

On-chip EDWA output power `derived` (extends D166; garciablanco2025 m3 kept measured: needs a ruling); D165 array rows;
sub-component rows (white2024 ring, liu2018 mirrors); classes (liu2018 resonator.bragg, yan2024 isolator with circulator
note, white2024 laser.sil); figure readings; inferred wavelengths; IL scope unspecified (yan2024, liu2018).

## Registry gaps proposed

frequency_converter: tuning_range_nm, acceptance bandwidth, output power, radius_um; nonreciprocal: xt_bandwidth_nm,
period_nm; resonator: reflectivity_pct. Deferred: Kerr splitting, SPDC rate, PL lifetime, noise reduction.
