# Batch report bf_07 (2026-10-20)

Transcribed by the coordinator. Dry-run 0 errors: 26 components, 72 metrics. Contract v3 applied mid-run (authors' org as fab: mohl2025 IBM Research Zurich, ogiso2024 NTT Innovative Devices; linewidth_mhz used for kappa_0/2pi: coordinator added kappa_intrinsic_mhz / kappa_ext_mhz / mode_splitting_ghz afterwards (D73) and these rows go to the audit patch).

- churaev2023 (7/18, facility CMi): LN adiabatic taper transition < 0.1 dB (derived from 2-10 transitions), straight LN-edge transition ~1 dB, Si3N4 EC < 2.5 dB per facet (abstract only, author_estimate), 100 GHz ring, 21 GHz ring (host -c), 50 GHz dimer (Fig. 4f Q as q_loaded, exponents from the figure), W-splitter (on-chip IL <= 1 dB as excess_loss_db: sum of both ports vs reference). "Up to" Q -> le + best; THz converted to nm by the agent. Not entered: 8.5 dB/m (EO), Si3N4 < 3 dB/m (cited), "hundreds of resonances Q > 4e6" (three designs), Dint and dimer splitting 4.6 GHz (now mode_splitting_ghz). BRNC operations-team thanks not entered.
- liu2025b (2/3): 1 um rib < 0.4 dB/cm (wafer map); UHNA EC 2 dB per facet (host -b). Not entered: EO-row values; GCs (no performance).
- zhang2024 (1/1): lensed-fiber facet ~5 dB per facet (EO notes only before).
- mohl2025 (2/4, fab IBM Research Zurich): photonic molecule (Qi ~1e5; mean kappa_0 776 MHz at RT; Table V kappa_a,0 2 GHz author_estimate model parameter); UHNA EC ~5 dB scope unspecified (reflection probing). Not entered: FSR (EO), 200 nm coupling "bandwidth" (definition not stated), splice losses, projected 1 dB, microwave resonator.
- hess2026 (2/2, fab Polariton): GC ~2.8 dB each (author_estimate, budget term); ring heater bw3db_khz 25 (derived by the paper from the rise time). Not entered: FWHM-normalized drift 0.048 / 0.054 /K, 63 K/ms estimate.
- axline2026 (9/41): GC with attached fiber array ~6 dB RT + six cryogenic per-device values (Table B.1); TFLT waveguide 0.25 dB/cm "as low as" (ring_extraction); witness rings and an all-design statistics row (median kappa_0); five coupled-racetrack designs (kappa_0 per supermode, L, s1, s2). kappa_0 entered as linewidth_mhz with "intrinsic" in condition (to repoint). No fab (Miraex / EPFL). Not entered: kappa_ext (now kappa_ext_mhz), minimum splitting, g0, microwave Q, FSR (EO), simulated 0.12 / 0.28 dB/m.
- yin2026 (1/1, fab AMF MPW): coupler 6 dB per facet (edge subtype assumed from "per facet").
- tatarczak2026 (1/1, fab Coherent: all authors, PD teams thanked): InP backside-illuminated PD flip-chipped on a TIA, combined BW > 100 GHz; host empty. Not entered: responsivities 0.7 / 0.5 A/W (link-simulation assumptions).
- xue2026 (0): 0.3 dB/cm in EO row; facility AEMD SJTU named (no rows).
- ogiso2024 (1/1, fab NTT Innovative Devices): DC heater P_pi < 20 mW. Not entered: 2.3 dB per facet (cited [4]), cross-waveguide curves.

Gaps: intrinsic vs loaded linewidth, kappa_ext, mode splitting (added, D73); thermal_drift_norm_per_k.
