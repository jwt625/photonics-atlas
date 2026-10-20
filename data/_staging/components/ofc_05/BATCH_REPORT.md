# Batch report ofc_05 (OFC 2026, facts only, 2026-10-20)

Transcribed by the coordinator from the batch agent's final report. Dry run: 0 errors; 19 components, 67 metrics.
No e-mail addresses, ASCII only; host_device_ids empty; no facility orgs.

## Per paper (components / metrics)

- M2A.4 (1/4): QD mode-locked comb laser, 100 GHz spacing, 16 lines within 3 dB, -1.02 to 1.20 dBm per line;
  power uniformity 2.22 dB derived from the range; O band inferred. MRM values (Q 4300, ER > 18 dB, 27 pm/V, 45 GHz)
  belong to the EO atlas; 130 nm SOI foundry not named; epitaxy from prior work. No fab org.
- Th3A.5 (1/3): PW/NW avalanche PD in 28 nm bulk CMOS (platform other): 0.114 A/W at -14.3 V, 0.150 A/W best at
  -14.6 V, 850 nm inferred; bandwidth 3.38 GHz from the S-parameter fit (measured, D76). Not entered: 6.3 GHz model
  transit-time bandwidth, optical window, receiver results. MPW foundry not named.
- Tu3J.7 (1/6, fab org_lumentum, D72): DFB section of the differential-drive EA-DFB: threshold < 15 mA (n=4, 55 C),
  wavelengths 1271 / 1294 / 1311 / 1323 nm, SMSR > 40 dB. Not entered: EO bandwidth, ER, TDECQ; HTOL drift < 2 %.
- W3E.2 (4/10): 8-ch tilted sampled-grating DFB array (threshold 25 mA, spacing ~2.4 nm / ~300 GHz, SMSR > 50 dB);
  conventional sampled-grating reference (threshold 60 mA); 11-ch array with varied ridge width (SMSR > 50 dB);
  Y-branch combined array (SMSR > 50 dB, 4.8 nm odd/even spacing). Material and band not stated (platform empty).
  Fab empty (passive "are fabricated").
- Th2A.46 (2/6): 400 um QD mode-locked comb laser (100 GHz, 1312 nm, 25 lines within 3 dB; vendor not stated);
  Innolume QD SOA (fab org_innolume, purchased device): gain 18 dB best, 20 dBm saturation output, both
  author_estimate (origin not stated). Not entered: RIN and linewidth (sentence cites [5]), undefined 53 nm bandwidth.
- M3F.6: no rows (OCS architecture talk).
- Tu3C.4 (1/10, fab org_imec, iSiPP300): 8-ch TOPIC-ring WDM filter: 3-dB width 83 GHz mean; spacing 374 GHz mean;
  IL 0.88 dB mean, scope unspecified, O band inferred; channel isolation >= 19.1 dB; tuning 3.80 mW per pi per ring
  (edge 4.00-4.02, inner 3.68-3.78); FSR >= 3.2 THz (author_estimate); 8 channels; footprint 1600 um2 (derived).
- W4K.3 (4/6): fs-laser-written borosilicate glass PIC: tunable 90-deg hybrid IL 1.17 dB average (scope unspecified),
  PDL < 0.1 dB, phase error 0.9 deg (from +/-0.9 deg phase stability); waveguide ~0.1 dB/cm at 1550 nm and fiber
  interface 0.2 dB per facet (author_estimate); TO phase shifter 70 mW for 2 pi (not halved). Fab not stated.
- Th1F.5 (1/13): SiN coupled-ring Kerr comb: spacing 300 / 200 / 100 GHz; lines within 3 dB 19 / 27 / 57; line counts
  above power thresholds as output_power_dbm (qualifier gt, n_samples); width 1600 nm, thickness 620 nm (design).
  Not entered: pump-to-comb efficiency 63.6 / 48.1 / 33.6 % (no parameter); FSR, gap, GVD (not allowed for laser).
- Th3F.8 (3/8, fab org_amf, stated MPW): 61-port fan-shaped Ge PD 0.87 A/W mean of 3 ports on-chip (author_estimate:
  on-chip power uses the typical 4.1 dB GC loss), dark 15.1 nA and 16.4 GHz at -3 V, 61 ports, Ge length 7 um; AMF PDK
  reference PD 6.9 nA and 23.8 GHz at -3 V; test GC 4.1 dB typical per coupler (author_estimate).
- M1C.4 (1/1): fiber mode-selective-coupler mode mux (platform other): crosstalk > 19 dB for the whole link (mux +
  33.6 km FMF + demux). Fab not stated. J5: drop if fiber devices are out of scope.
- Th3J.3: no rows (commercial setup lasers with datasheet linewidths).

## Judgment calls

J1 Tu3J.7 four wavelengths as one design row with per-device wavelength conditions. J2 passive voice -> fab empty
(W3E.2, W4K.3, Th1F.5). J3 unstated origin -> author_estimate (D76). J4 W4K.3 phase stability as phase_error_deg.
J5 M1C.4 fiber mode mux under mode_converter. J6 W4K.3 Table 1 values taken as measured.

## Registry gaps reported

pump_to_comb_efficiency_pct (laser.comb); cmrr_db (hybrid_90); fsr_ghz and gap_nm for laser.comb;
max_photocurrent_ma (photodetector); RSMS slope dB/nm and reliability power drift % (low priority). No missing orgs.
