# Batch report ofc_09 (OFC 2026, facts only, 2026-10-20)

Transcribed by the coordinator from the batch agent's final report. Dry run: 0 errors; 12 components, 55 metrics from
6 of 11 papers. No e-mail addresses. Prompt rule added for this batch: a value in a sentence that carries a citation
is cited work unless the paper clearly reports it as its own result.

## Per paper (components / metrics)

- W4B.5 (1/13, fab org_imec, ISIPP50G MPW): dual-layer poly-Si/Si 2D GC multiplexing 8 fiber modes into an FMF
  (fiber_chip_coupler.grating): measured peak per-coupler loss LP01x 1.9 dB at 1547.1 nm, LP11ax 2.4 at 1552.9,
  LP11bx 2.1 at 1594.7, LP21bx 2.3 at 1594.7; 1-dB BW ~20 nm; simulated 1.83 / 2.07 dB at 1550 nm (~34 nm) and
  1.98 / 2.15 dB at 1611 nm (~28 nm); period 552 nm, etch 70 nm (design).
- Th2A.7 (1/3, fab org_imec, iSiPP50G): MEMS phase shifter, 3-dB bandwidth 1.36 MHz (text Fig. 3 = caption Fig. 2);
  30 um phase section, 400 nm width (design). v_pi not entered (ambiguous "from 5 to 30 V").
- Th1D.6 (1/8, fab empty): Ge:silica microring 1.5 mm diameter: at 1550 nm Q_i 329M and Q_L 278M (Lorentzian fit),
  Q_L 276M from ring-down (derived from 227 ns photon lifetime); Q_i 566M best at 1064 nm; Q_i > 1e8 over 458-1550 nm;
  propagation loss 0.0007 dB/cm (author_estimate: ng not stated); radius 750 um (derived); core 10 um.
- Tu2D.4 (6/16, fab org_stmicroelectronics, PIC100G, Tables 1-2): Si rib 0.6 / 0.35 dB/cm (1310 / 1550 nm); SiN strip
  TE / TM 0.6 / 0.5 at 1310, 0.35 / 0.55 at 1550; Si/SiN transition per_component TE / TM < 0.1 / 0.6 dB at 1310,
  < 0.1 / 0.17 at 1550; O-band SiN edge coupler taper + transition < 0.7 dB TE, < 0.6 dB TM per_coupler, PDL < 0.2 dB,
  simulated overlap loss < 0.15 dB; Ge PD 11 nA at -1 V, 1.0 A/W, 80 GHz at -1 V; TiN heater P_pi 15.5 mW.
- Th2A.8 (1/3, fab empty): meta-lens pair for detachable FAU coupling: 1-dB lateral tolerance +/-18 um (simulated),
  +/-2 um meta-lens to PIC (author_estimate), beam ~70 um (design). No measured coupling loss reported.
- M2E.5 (2/10, fab empty): slot nanobeam cavity Q_L 2300 / 2570 (C / L band inferred), extinction 13.7 / 4.9 dB,
  mode spacing 30 nm (paper's "FSR"), simulated Q_i 4.2e5 / 9.9e4; 4-channel Kerr switch contrast 5.2 dB at 52 fJ/bit
  and 3.2 dB at 27 fJ/bit (extinction_db), 4 channels.
- W1G.7, M1D.5, W3J.5, Th1A.2, W2A.28: no rows (system, review, network or setup-source papers).

## Judgment calls

J1 W4B.5 as fiber_chip_coupler.grating (measured quantity is coupling loss). J2 Th1D.6 566M and > 100M as q_intrinsic.
J3 Tu2D.4 fab ST (PIC100G presented as ST's platform); PD subtype ge_waveguide is a guess (flag for audit); SiN film
per band inferred. J4 imec fab for W4B.5 and Th2A.7; authors' release post-processing in notes. J5 W1G.7 / M1D.5
sources treated as setup / system.

## Registry gaps reported

phase_shift_max_pi; mech_resonance_khz; gap_nm for phase_shifter; n_channels for fiber_chip_coupler; m2_beam_quality,
divergence_half_angle_deg, emission_angle_deg; switching_energy_fj_per_bit; comb_span_ghz; photon_lifetime_ns.
No missing orgs.
