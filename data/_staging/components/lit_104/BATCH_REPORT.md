# lit_104 batch report (distill, 2026-11-08)

Papers: liu2019, bonneville2024, du2018, huang2016, jung2018. All five cached texts match their source rows (page-1
title); none is a correction / erratum. liu2019 `garbled_text_layer` pages 13-14 hold only references: no value comes
from them; its Table 1 was read from the page render (p.19). du2018 and liu2019 are ACS "Just Accepted" manuscripts.

Totals: 18 components, 106 metric rows. Dry run (`merge_component_staging.py ... --dry-run`): +18 / +106, 0 errors
(the only warning printed belongs to another batch, ni2025b).

## Per paper

### bonneville2024 (6 components, 33 metrics)

- `edwa_12p9cm` amplifier.rare_earth: internal net gain 33.5 dB at 1532 nm (derived, D166), 19.5 dB at 1550 nm (Fig. 4(c)
  read), on-chip output 10.2 dBm (derived, D394), PCE about 15 % (author_estimate: on-chip pump power not printed),
  length, width, film thickness 786 nm (measured), cladding / BOX 8 um.
- `edwa_9p3cm`, `edwa_4p9cm` sibling lengths (rule 9): Fig. 4(c) peak gains at 1532 / 1550 nm (extracted_from_figure,
  +/-0.5 dB reading); 4.9 cm carries the printed 3.5 dB/cm (derived, rests on the derived gain).
- `al2o3er_waveguide` waveguide_platform.straight (D396 cross-class row of the spirals): IR-camera total losses 2.3 /
  1.7 dB/cm (1532 / 1550 nm, incl. Er absorption) and 0.41 dB/cm from the Fig. 2(a) 1640 nm fit legend.
- `ring_r300` resonator.ring (test structure): Q_i 6.4e5 and 0.46 dB/cm at 1636.1 nm, both author_estimate (D403: the
  fit assumes critical coupling; the dip is about 8.5 dB), radius 300 um, gap 1.4 um.
- `nanotaper_ssc` fiber_chip_coupler.edge: lumped per-facet loss 25 dB (1532), about 15.5 dB (1550), 7.5 dB (1480 pump),
  derived (loss_breakdown formula p.6 incl. the derived gain); simulated 4 dB at the 303 nm tip; tip 150 nm design and
  303 nm SEM-measured; 2 mm taper; fiber MFD 10.0 um (author_estimate, origin not stated).
- Not entered: signal enhancement about 63 dB (no parameter); 79 % simulated overlap; Er concentration 3.9e20 cm-3;
  Table 1 other works.
- Conflicts flagged in notes: gain 33.3 dB (p.2) vs 33.5 dB (p.6, p.8, Table 1); on-chip output 10.2 dBm (p.7) vs 10.2-13.6
  dBm (abstract) vs 13.2 dBm (Table 1); coupling loss -25 dB (p.7) vs -25.4 dB (abstract); 33.5 dB tied to -30.2 dBm
  launched in text but the highest Fig. 4(c) point sits near -24 dBm; Fig. 2(a) legend 1640 nm vs caption 1630 nm.

### du2018 (3 components, 10 metrics)

- `gesbse_ceyig_ring_isolator` nonreciprocal.isolator (platform other, GeSbSe on Ce:YIG/YIG): isolation 40 dB, IL 3.0 dB
  (best, on_chip_excess; spectra normalized to the off-resonance level), wavelength 1560.16 nm read off Fig. 4(b), TM;
  width 650 nm (SEM), GeSbSe 360 nm, 3 um oxide.
- `ceyig_racetrack_resonator` resonator.ring (same racetrack, D396): 17.5 dB/cm author_estimate (computed from Q_L and
  ER, coupling regime not stated, D403).
- `gesbse_reference_racetrack` resonator.ring (reference without MO layers): 3.8 dB/cm measured (method unspecified),
  2.7 dB/cm author_estimate (minus the FDTD 1.1 dB/cm junction term).
- Not entered: nonreciprocal resonance shift 44 +/- 4 pm and its 1540-1590 nm dispersion (no parameter); MO-oxide loss
  13.7 dB/cm and 270 dB/cm absorption; Fig. 1 loss breakdown of the authors' earlier device (ref. 6, D259); the
  500 nm x 80 um oxide vertical taper (geometry only, no measured value: not a row).

### huang2016 (2 components, 16 metrics)

- `ring_circulator_4port` nonreciprocal.circulator (soi, bonded Ce:YIG, microstrip electromagnet): four measured
  adjacent-port isolations 11.0 / 8.6 / 11.0 / 6.7 dB (Table 2), simulated 12.0 dB at saturation, forward-path IL
  9.7-12.4 dB (de_embedded: normalized to a silica-clad reference waveguide), crosstalk 6.2-11.3 dB, 4 ports, Si
  230 x 600 nm.
- `ring_circulator_6port`: isolation 14.4 dB (best, IR23) and 2.5 dB (IR61), IL 10.1-14.3 dB (scope unspecified: the
  6-port normalization is not restated), 6 ports.
- Not entered: 400 ps magneto-optic rise time and 8.5 dB eye extinction, about 40 mW microstrip power (parameters not
  allowed for nonreciprocal, see gaps); ring radius 20 um (radius_um not allowed); resonance split 0.35 / 0.25 nm; K =
  10.45 % design; 8.7 dB bus loss (computed from cited Ce:YIG loss, rule 3); Table 2 simulated values at 0.35 nm split.
- Text inconsistency noted: p.5 calls the smallest pair IR14, Table 2 labels it IR41.

### jung2018 (4 components, 22 metrics)

- Fiber-coupled micro-optic SDM isolators (C-lens collimators with a bulk isolator core): kept in scope as fiber-coupled
  passive parts (D411 / D424; karki2019 bulk isolators precedent), platform other.
- `fmf2_collimator_pair` fiber_interface.other: per-mode IL at L = 10 / 30 / 50 mm (LP01 0.7 / 0.8 / 1.1, LP11 1.0 /
  1.5 / 2.8 dB), MDL 0.3 / 0.7 dB, beam diameters (ranges), back reflection 32 dB (C band).
- `fmf2_isolator` nonreciprocal.isolator: peak isolation 43 dB at 1559 nm, > 32 dB over the C band, isolator-core added
  loss about 0.1 dB (de_embedded).
- `fmf4_collimator_pair` fiber_interface.other: MDL 0.3 / 1.1 dB at L = 10 / 30 mm (1550 nm inferred).
- `mcf32_isolator` nonreciprocal.isolator: mean IL about 1.4 dB (incl. two splices), core-to-core variation < 1.4 dB,
  neighbouring-core crosstalk > 40 dB, isolation about 43 dB at 1559 nm and > 32 dB over the C band, 32 cores.
- Not entered: conclusion "< 1 dB IL and < 0.5 dB MDL" for the few-mode isolators (holds for the 2- and 4-mode-group
  devices collectively, working distance not given; D159); 4-mode-group isolator (isolation stated identical to the
  two-mode-group one, same core; no own row); modal extinction values (include a 10 km spool); MCF fiber XT -55 dB/km
  (fiber property); back reflection of the MCF isolator (parameter not allowed); Fig. 3(a) per-mode losses.

### liu2019 (3 components, 25 metrics)

- `qd_soa_on_si` amplifier.soa (iii_v_on_si_epi): G0 39 / 34.1 / 25.8 / 23.4 dB and Ps 23 / 24.1 / 21.8 / 23.1 dBm at
  20 / 40 / 60 / 70 C (derived, on-chip via measured coupling losses, D166; Ps = fit parameter of Eq. (2), not a
  compression point), fiber-to-fiber min NF 8.5 / 6.6 / 9.1 / 8 dB (Table 1, measured), on-chip output at 2.3 mW input
  (Table 1 mW converted to dBm, derived), > 20 dBm at 0 dBm input, gain bandwidth > 100 nm (20 C) and 21 nm (70 C) at
  the > 20 dB criterion, 3-dB gain bandwidth about 14 nm, series resistance 0.96 ohm (Fig. 2(d)), 5 mm length, 5-11 um
  tapered ridge.
- `qd_soa_input_facet_coupling` / `qd_soa_output_facet_coupling` fiber_chip_coupler.edge: 4 / 8.1 dB per facet to lensed
  SMF (measured from fiber vs integrating-sphere L-I curves), O band inferred.
- Not entered: WPE 19.7 % (40 C) and 14.8 / 7.7 / 10.4 % (gap); NF "as low as 6.1 dB" of abstract / intro (conflicts
  with 6.6 dB on p.10 and Table 1); ASE ripple < 0.05 dB; AR reflectivity about 4e-3; 8 deg tilt; lifetime projection
  (rests on ref. 20).

## Fab / facility orgs

- Fab empty on all 18 rows: every fabrication sentence is passive or the authors span several orgs (D80b).
- Facility set: du2018 `org_mit_microsystems_technology_laboratory` (fabrication facility support, p.14).
- Missing from the registry (not entered):
  - "MESA + Nanolab clean-room facilities" (University of Twente, Enschede, NL), bonneville2024 p.2 Sec. 2, role
    facility (film deposition performed there). Parent `org_university_of_twente` / `org_mesa_plus_institute_for_nanotechnology`
    exist; the facility itself has no id.
  - "CMSE, an NSF MRSEC" (MIT Center for Materials Science and Engineering, Cambridge MA, US), du2018 p.14 Funding
    ("used shared experimental facilities"), role facility.
- Suppliers in notes only: MTI Corp. (du2018 oxide wafers), OFS Fitel Denmark (jung2018 two-mode-group fiber),
  NAsPIII/V (liu2019 GaP-on-Si template).

## Judgment calls

1. bonneville2024 internal gain and on-chip output power `derived` (signal-enhancement method minus own measured losses;
   D166 / D394); the lumped coupling losses `derived` (printed formula with own measured terms and the derived gain).
2. bonneville2024 Al2O3:Er3+ film thickness 786 nm `measured` (printed as the resulting layer thickness, index by VASE;
   measurement method for the thickness not named).
3. bonneville2024 sibling spirals entered as own rows with figure-read gains (rule 9); 3.5 dB/cm on the 4.9 cm row.
4. du2018 isolator wavelength 1560.16 nm read off Fig. 4(b) (no wavelength printed with 40 dB / 3.0 dB), as the
   ghosh2012a precedent; resonator / reference losses C band inferred.
5. huang2016 6-port IL scope `unspecified` (only the 4-port normalization is described).
6. jung2018 in scope (fiber-coupled passive part); collimator pairs as `fiber_interface.other` (mdl_db / back reflection
   allowed there); "<1 dB / <0.5 dB" conclusion bounds left in notes (D159).
7. liu2019 facet coupling rows as `fiber_chip_coupler.edge`, one per facet design (5 um vs 11 um ridge ends), measured.

## Registry gaps (skipped value + locator + proposed definition)

- `wpe_pct` for amplifier: liu2019 SOA WPE 19.7 % (p.10, Table 1 p.19; also 14.8 / 7.7 / 10.4 %). Proposal: widen
  `wpe_pct` to amplifier, def "(P_out - P_in) / (I V) for an electrically pumped amplifier, as defined by the paper".
- Nonreciprocal resonance shift / split: du2018 44 +/- 4 pm (p.10), huang2016 0.35 / 0.25 nm (p.4, p.7); bi2011
  precedent. Proposal: `nonreciprocal_shift_pm` (nonreciprocal, resonator) "CW / CCW or forward / backward resonance
  wavelength split at the stated field / current".
- Switching speed of reconfigurable nonreciprocal devices: huang2016 rise time 400 ps (p.5 Fig. 6) and about 40 mW
  microstrip power (p.4). Proposal: allow `rise_time_us` and `power_consumption_w` for nonreciprocal.
- `back_reflection_db` for nonreciprocal: jung2018 MCF isolator -32 dB over the C band (p.7).
- `radius_um` for nonreciprocal (ring isolators / circulators): huang2016 R = 20 um (p.3).
