# Batch lit_20 report (distill subagent, 2026-10-29)

Dry-run `batch lit_20: +56 components, +348 metrics; errors 0`. ASCII, no e-mail, no addresses, quotes only a few
words. Not audited or merged.

## Per paper (components / metrics)

- dong2010 (4 / 30): undercut Ti-heater racetrack resonators R 4 / 10 um, split as in oz2023 into
  phase_shifter.thermo_optic (2.4 mW per FSR, 4.8 / 2.7 nm/mW as pm/mW derived = FSR / 2.4 mW, rise ~170 / fall ~150 us
  for R 4 only, heater / stack geometry) and resonator.ring (FSR 11.5 / 6.4 nm, Q ~8000 stated once for both, entered on
  both as q_loaded). Not entered: 27 / 21 mW per FSR of the authors' earlier devices (ref. [14], D259), Table 1 literature
  rows, extinction (figure only). Fab org_kotura borderline (D84b: Kotura staff thanked for fabricating, p.7).
  heater_gap_um not entered (reference surface of the 1.2 um top oxide not stated).
- maeder2022 (10 / 93): Pt strip TOPS beside X-cut LNOI ridges, one row per stated geometry: 1.1 x 1.2 mm (P_pi 301 mW
  best), 7.1 x 0.4 mm (V_pi 9.9 V best), 3.1 x 1.2 mm (P_pi 767 mW, Fig. 2(c) label), 3.1 x 1.0 mm (MZI ER 16.3 dB),
  3.1 x 0.8 mm (rise 8.8 / fall 7.5 us, 40 kHz derived from 0.35/tau_r, > 100 kHz small signal), 3.1 x 0.4 / 0.6 mm
  (> 100 kHz), 1.1 x 0.4 / 0.6 / 0.8 mm (> 50 kHz, stated for all six Fig. 5(a) devices). Fab org_eth_zurich ("we
  fabricated"), facilities ScopeM, BRNC, FIRST. Not entered: EO phase-shifter values (EO metrics), VpiL 0.4 / 1.0 V cm
  (no parameter), Fig. 2(d) scatter (points not tied to geometries), simulated Fig. 2(b), 0.5 dB / 33 min stability.
- wang2016 (4 / 27): JFE n-implant heater in the small rings (rise 0.6 us large-signal with pre-emphasis, 4 us small
  signal, fall 19 us, 2.9 nm/mW), small dual-ring wdm.mrr (8.4 dB per ring, > 15 dB contrast at +/-10 nm, ~25 nm tuning,
  FSR > 40 nm), large dual-ring wdm.mrr (2.5 dB per ring, 25 dB contrast, FSR 850 GHz author_estimate), inverse-taper
  edge coupler (~10 dB/facet with a fiber array, author_estimate). Fab org_sandia_national_laboratories (MESA MPW run).
  Not entered: Fig. 5(b) caption 24 / 47 us for the large rings (text p.10 says not measured; conflict), R 1.7-5.9 kohm
  and dC 0.12 nF (ring size of the measured banks not stated, D159), 3.2 / 33 uW/GHz (gap), fitted JFET parameters, the
  first-batch ~10 dB contrast (ref. [27]).
- zhu2019 (17 / 60): OFC paper. Eight measured TiN-heater TOPS types from Table 1 (SOI / a-Si:H x trench / none x AlN
  block / none; mean P_pi and "speed" = 0.35/max(rise, fall) as bw3db_khz derived, about 6 devices each, n_samples empty),
  simulated P_pi on the SOI no-trench rows (18.0 / 14.5 mW), simulated 2 / 5 um AlN variants and Si3N4 type-1/2/3
  proposals (row_kind design, Fig. 4(e)), four straight waveguides (2.6 / 2.8 / 3.4 / 3.5 dB/cm). a-Si:H rows platform
  other. Fab empty (passive "were fabricated", all authors A*STAR IME; D80b). Not entered: Fig. 3(c) single-device
  10.2 / 8.4 mW (trench type not stated), improvement percentages, simulated metal-induced loss in dB/cm (D250), tau sums.
- lemieuxleduc2025 (3 / 31): transfer-printed Ge0.89Sn0.11 membrane MSM detectors on SOI, design EC and ECGAC
  (photodetector.ge_waveguide per wang2022a precedent): responsivity at 2330 nm for 0.1-1.0 V from the Fig. 5(c)/(d)
  labels (ECGAC 0.361 A/W at 1 V), basis author_estimate (waveguide power rests on the estimated 12.9 dB SGC loss);
  dark current 50-90 uA range (both designs) and ~66 uA (Fig. 5(a) device) as nA derived; SGC 12.9 dB author_estimate
  with design geometry (period 1.22 um, FF 0.66 undefined, 10 deg). Not entered: simulated absorbed fractions (no
  parameter), family responsivity 0.1-0.2 A/W, 3.1 um cutoff (authors' earlier work, D259), SU-8 gap 160 nm (gap).
- maiti2020 (3 / 21): strained MoTe2 MSM detectors on a Si ring (photodetector.graphene per flory2020): device 1
  (40 nm, 10 mA/W, EQE 1 %) and device 2 (60 nm, 468 mA/W, EQE 37 %) at -2 V, ref on_chip, author_estimate (Pinput from
  estimated GC and waveguide losses, Supp. not cached); loaded ring finesse ~1.6 and 1550.75 nm resonance. Not entered
  (D159): dark current ~13 nA at -1 V, NEP 90 pW/Hz^0.5, 3-dB bandwidth 35.6 MHz at 2 V; the text does not say which
  device (see coordinator item 2). Fab empty (six institutions, passive methods).
- reddy2020 (3 / 12): fiber-packaged MoSi SNSPDs on a SiO2 / aSi DBR stack, active-area diameter 50 um (SDE 98.0 +/-
  0.5 %, four devices A-D, 450 ohm series resistor), 35 um (~96 %) and 20 um (~94 %) read off the Fig. 3 inset
  (extracted_from_figure, +/-1 %). quantum_efficiency_pct with ref_plane module (D155), platform empty. Fab empty:
  "we deposited" but authors at NIST and U. Calgary, site not stated (bock2010 precedent). Not entered: fill factor
  0.57 (not allowed for photodetector), latching bias 0.49-0.52 V, Fig. 4 pulse shapes, DBR (geometry only).
- liu2021a (5 / 42): Damascene Si3N4 ring 40.6 GHz FSR, 2200 x 950 nm (kappa0 6.5 MHz most probable over 10,197 TE00
  resonances as statistic typical, Q0 30e6 / 20e6 TM derived, wafer map <= 7.5 MHz, single-resonance comb and sideband
  values at 1550.6 nm, ring-down 8.4 MHz le, 1.0 dB/m as 0.01 dB/cm derived), spirals 0.5 / 1.0 / 1.4 m (best 1.7 / 2.4
  / 4.1 dB/m; Fig. 4(f) per-sample readings at 1520 / 1550 / 1630 nm entered as derived with the reading in notes;
  length and footprint), facet coupling 33 % / 4.8 dB fiber-to-fiber. Fab org_epfl ("We fabricate"), facility
  org_center_of_micronanotechnology. Not entered: kappa_abs ~0.2 MHz and absorption-limited Q 1e9 (gap), D2 224 kHz,
  per-defect 1-2 dB extra loss, spiral turn gap 4 um.
- ono2016 (7 / 32): Si-wire to Au/air MIM slot converters (mode_converter.converter, platform other per D71): sample A
  400 nm taper (3.3 dB per converter cutback, 3.5 dB sim, 7.5 / 8.2 dB device total), 600 nm taper 50 x 20 nm slot
  (1.7 dB, 1.4 dB sim), 70 nm slot series Au 20-40 nm (1.2-1.3 dB), 200 nm taper series (< 3 dB), butt joint (~4 dB),
  simulated 20 nm-gap optimum (0.95 dB, design); MIM slot waveguide 1.8 dB/um measured, 1.3 dB/um simulated (as dB/cm,
  derived / simulated). Fab org_ntt borderline (all authors NTT, two dual Tokyo Tech). Not entered: field enhancement
  41, effective area, reference samples B / C transmissions, w_gap (gap).

## Fab / facility organizations missing from the registry

- Microsystems and Engineering Sciences Applications (MESA) facility, Sandia National Laboratories (wang2016 p.4 Sec.
  2.1): candidate facility_org_ids for the four wang2016 rows (fab already org_sandia_national_laboratories).
- Ecole Polytechnique de Montreal / Polytechnique Montreal (lemieuxleduc2025 p.1 affiliation; all authors): fab_org_ids
  candidate only if "we demonstrate the fabrication and integration" (p.1) is ruled a D80b fab statement.

## Judgment calls for the coordinator

1. dong2010 / wang2016 heater-on-ring papers split into phase_shifter.thermo_optic + resonator.ring / wdm.mrr rows
   (oz2023 precedent), so rise / fall times sit on the heater row.
2. maiti2020: the abstract pairs 0.5 A/W with the dark current and NEP, while p.11 implies the NEP device is not
   device 2; dark current, NEP and 35.6 MHz bandwidth left out of both device rows (D159).
3. Borderline fab orgs: dong2010 org_kotura (staff thanked for fabricating), ono2016 org_ntt (dual affiliations),
   lemieuxleduc2025 (org missing), reddy2020 empty (NIST + Calgary).
4. Responsivities resting on estimated coupler losses entered as author_estimate (lemieuxleduc2025, maiti2020); EQE
   computed from them kept author_estimate (D256a analogue).
5. liu2021a "most probable" (histogram mode) as statistic typical; Fig. 4(e) wavelength inferred as 1550 nm because the
   Fig. 4(f) 1550 nm points equal the stated best values.

## Registry gaps (value actually skipped)

- `tuning_power_uw_per_ghz` (uW/GHz; phase_shifter, wdm, resonator): heater power per GHz of resonance shift.
  wang2016 3.2 uW/GHz small ring and 33 uW/GHz large ring (p.11).
- `kappa_abs_mhz` (MHz; resonator, wdm): absorption-limited loss rate kappa_abs / 2 pi from a thermal-response
  measurement (method in notes). liu2021a mean ~0.2 MHz, ~0.4 MHz near 1520 nm (p.7, Fig. 5(e)); also proposed in lit_11.
- `vpil_v_cm` (V cm; phase_shifter): voltage-length product of a non-EO phase shifter. maeder2022 TOPS 0.4 V cm
  (7.1 um x 0.4 mm) and 1.0 V cm (p.3).
- gap_nm widened to mode_converter: Si-taper-to-metal gap of a plasmonic converter. ono2016 w_gap 40 nm fabricated,
  20 nm simulated optimum (p.3-4).
- gap_nm widened to photodetector (waveguide-to-absorber spacer of an evanescently coupled transferred absorber).
  lemieuxleduc2025 SU-8 160 nm (p.10).
- fill_factor widened to photodetector (SNSPD meander wire width / pitch). reddy2020 0.57 (p.2).
