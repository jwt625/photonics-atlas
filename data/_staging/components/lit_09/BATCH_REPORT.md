# Batch lit_09 report (distill subagent, 2026-10-23, condensed by the coordinator)

Dry-run `batch lit_09: +77 components, +423 metrics; errors 0` (log `logs/merge_component_staging_20261023T014503.jsonl`).
D256 unit-form self-check applied (flory2020 0.2 A/W and tossoun2019 0.01 nA kept as printed). Not yet audited or
merged (paused by the owner).

## Per paper (components / metrics)

- baghdadi2021 (2 / 13): dual-slot NOEM phase_shifter.mems (phase 1.792 pi derived, V_pi 0.85 V derived, IL < 0.04 dB
  per_component, bw3db 260 kHz, mech resonances, geometry); GC ~9 dB author_estimate scope unspecified. Fab Lightmatter
  (own release step; foundry only cited [24]).
- cheung2023 (7 / 38): III-V/Si charge-trap memory MZI (phase_shifter.other: endurance 100, 4 levels, retention 24 h,
  phase shifts derived, power < 2e-8 mW author_estimate, two conflicting ERs ~10 / ~1.78 dB both entered with notes),
  MZI DC, ring filter wdm.mrr, Si waveguides, bends, GC. Fab HPE; UCSB nanofab facility borderline. Fig. 7(b) values
  treated as cited (D259).
- dong2021 (8 / 26): AlN piezo-optomechanical SiN phase shifter (phase_shifter.other per hosseini2015; MZI IL 3.5 dB at
  737 nm, ER ~30 dB at 5 K, ~5 ns, mech resonance, 17 pF), 4x4 MZI mesh, SiN waveguides (author_estimate per D76), test
  ring, wide waveguide, Euler bend, taper, edge coupler 15 dB per facet. Holding power not entered (cited input).
- murray2015 (9 / 78): folded TO phase shifters D1-D5 unetched / underetched (P_pi 14 down to 0.095 mW, MZI IL
  author_estimate, ER > 20 dB, rise / fall on the Fig. 8 devices, geometry). Fabricated at IME (check fab ids in audit).
- seo2025 (9 / 90): TiW-heater TO phase shifters type-1 / type-2 x L = 210 / 240 / 270 um (P_pi mean of 6, IL de_embedded
  incl. MMIs, rise / fall means, geometry; simulated values on L = 240), rib waveguide 1.5 dB/cm, focusing GC 6 dB, MMI
  0.2 dB. Applied Nanotools platform.
- alexander2026 (20 / 66): 16 lateral Si SPAD variants (breakdown + geometry), device 03 PDE 1.95 % (two breakdown values
  15.0 / 15.50 V noted), vertical SPAD, SiN waveguide 2.70 dB/cm derived, edge coupler, Si-SiN transition. AMF. Family-
  level DCR / afterpulsing not entered (D159 / D254).
- flory2020 (4 / 23): MoTe2/graphene PDs (45 nm / 40 um responsivities, EQE, 12 GHz; 35 nm / 33 um >= 24 GHz; 11 nm /
  20 um > 30 GHz, ~50 GHz author_estimate), GC ~7.5 dB. FIRST Center mapped to org_first_center_for_micro_and_nanoscience.
- nozaki2016 (6 / 30): InGaAs PhC PD (photodetector.other, inp_membrane; responsivity 0.98 A/W author_estimate, dark
  current, 28.5 GHz, capacitances, series R, saturation), L / Wct siblings, resistor-loaded PD.
- tossoun2019 (3 / 29): InAs QD waveguide PD/APDs 11 x 30 / 60 / 90 um (bandwidths, dark current, densities incl. one
  printed value inconsistent with its inputs (flagged), responsivities author_estimate, GBP 240 GHz, gain ~45). Fab empty.
- ding2022 (9 / 30): 2 um multimode Si spirals (0.28 dB/cm), other widths, Euler S-bend, GC ~4.2 dB, four FWM
  frequency_converter.other rows (dB efficiencies stored as % derived). IMECAS MPW.

## Orgs missing / not entered

NQFF Singapore (characterization support, borderline); CINT (funding wording, D80c); foundry only by citation
(baghdadi2021); FIRST Center printed variant (alias candidate).

## Judgment calls for the audit

baghdadi2021 fab = Lightmatter; cheung2023 HPE fab + UCSB borderline facility + two ERs; murray2015 / seo2025 MZI-level
IL / ER on phase_shifter rows (D158); dong2021 piezo as phase_shifter.other; alexander2026 PDE basis measured and 16
breakdown-only rows; nozaki2016 platform inp_membrane, photodetector.other (D152); tossoun2019 attribution of the 60 um
values from context; ding2022 FWM as frequency_converter.other with dB -> %.

## Registry gaps proposed

thermal_crosstalk_pi (phase_shifter); conversion_efficiency_db (frequency_converter); light_to_voltage_efficiency_v_per_w
(photodetector); vpil_v_cm (low priority, EO atlas scope); fsr_nm for phase_shifter; retention_time_s for wdm.
