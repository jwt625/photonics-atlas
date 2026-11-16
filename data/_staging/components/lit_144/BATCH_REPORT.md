# lit_144 batch report

Distilled 2026-11-15 under the pic-component-distill skill (Contracts v4-v7, DevLog-007 rulings through D578). Papers:
riedhauser2025, errandoherranz2019, xiang2022, runge2015. Page-1 titles match the source rows for all four. Totals:
5 components, 47 metric rows. `merge_component_staging.py data/_staging/components/lit_144 --dry-run`: +5 components,
+47 metrics, 0 errors (the one WARN printed concerns merged row cmp_lit_ni2025b_pimmwc, not this batch).

## riedhauser2025 (APL Photonics 2025, arXiv v1 text with supplement on p.11-20): 2 components / 15 metrics

- `cmp_lit_riedhauser2025_bto_ring_r100` (resonator.ring, bto_on_oxide_substrate): kappa_0 / 2pi per-device medians
  430-870 MHz (range, n = 8) and their mean 510 MHz; Q0 2.22e5-4.50e5 (derived from kappa_0 by the paper); total
  propagation loss 86-174 dB/m stored 0.86-1.74 dB/cm (derived); absorption-limited loss 10.9 (+5.8 / -0.4) dB/m
  stored 0.109 dB/cm (median, author_estimate); Fig. S2 typical resonance kappa_ex 822 MHz, kappa_0 314 MHz; simulated
  n_g,eff 2.19; geometry R 100 um, film 225 nm, ridge height 110 nm (etch_depth_nm), slab 115 nm (derived), top width
  1.6 um, BOX 3 um.
- `cmp_lit_riedhauser2025_edge_coupling` (fiber_chip_coupler.edge, platform empty): fiber-to-fiber transmission about
  -20 dB stored as 20 dB `fiber_to_fiber`, device-to-device spread < +/- 1 dB in condition.
- Not entered (no registry parameter): kappa_abs / 2pi median 55 (+29 / -2) MHz (p.6; Table S5 48-139 MHz per device),
  absorption-limited Q_abs 3.8e6 (p.7 Table 1), Kerr n2 of the mode 1.7e-18 and of BaTiO3 1.8e-18 m2/W (p.6, Table S4),
  thermo-optic resonance shift -4.92 GHz/K measured / -4.42 GHz/K corrected (p.17, Fig. S6; resonance wavelength not
  stated, so no pm/K conversion), simulated confinement 63 % and n_eff 1.67, FEM dT/dP_abs 903 K/W, backscatter rate
  mu 998 MHz (Fig. S2), Table S5 per-device kappa_0 of the pump resonances. Table 1 values for SiO2, Si3N4, LiNbO3, GaP,
  AlGaAs and the 923 pm/V Pockels coefficient are cited (rule 3). Introduction losses (70, 200-600, < 200 dB/m) cite
  the authors' and others' earlier work (rule 3, D259).
- Orgs: fab `org_ibm_research_zurich` (author contributions p.8: D.C. fabricated the sample; acknowledgment p.8: devices
  fabricated at BRNC at "IBM Research Europe, Zurich"), facility `org_binnig_and_rohrer_nanotechnology_center` (D448).
  No missing org. Alias note for the org round: "IBM Research Europe, Zurich" (p.8) -> org_ibm_research_zurich (as
  D425 "IBM Research Europe, Rueschlikon").
- Judgment calls: (1) kappa_0 basis `measured` although D403 asks for the coupling regime: the paper fits resolved
  doublets with kappa_ex and kappa_0 as separate fit parameters (Fig. S2: 822 vs 314 MHz), and a resolved doublet's dip
  depth is not symmetric in kappa_0 / kappa_ex (ji2024 precedent, D465); the auditor should confirm. (2) Absorption
  loss `author_estimate` (rests on FEM dT/dP_abs and V_eff; wang2024b precedent). (3) Ridge height 110 nm and the
  1.6 um top width `measured` / `derived`-from-printed because the sentence cites the SEM / FIB images Fig. 1(a),(b)
  and says "at the top of the ridge"; the paper does not say design vs measured. (4) Fig. S2 single-resonance
  kappa_ex / kappa_0 entered with 1500-1600 nm `wavelength_inferred` (resonance wavelength not stated). (5) Edge
  coupling: platform left empty (D422; facet waveguide not described).

## errandoherranz2019 (JSTQE 2019 review, arXiv text): 0 components / 0 metrics

- Review article ("The field of ... MEMS for PICs is reviewed", p.1). Every device value (phase shifters, couplers,
  switches, the Fig. 12-13 figure-of-merit plots and the Sec. III comparison) is cited from other works, including the authors'
  own earlier papers (rule 3, D259). Appendix A-B (p.13) describes the authors' own estimates computed from cited values
  (phase shift from wavelength shift / FSR, IL from Q_int and FSR with assumed taper losses): values computed from cited
  values are not entered (rule 3). No new measurement, simulation or fabricated device of this paper. Nothing to stop on.

## xiang2022 (Optica 2022): 2 components / 21 metrics

- `cmp_lit_xiang2022_lateral_rt_ge_si_apd` (photodetector.apd, soi): primary responsivity 0.93 A/W at -4.7 V
  (on_chip, GC loss excluded); Fig. 3(b) peak about 70 A/W at about -14 V for -25 dBm (extracted_from_figure); dark
  current 4.5 nA at -4 V and 100 uA at -14 V (stored 100000 nA, derived); breakdown about -14 V (100 uA criterion);
  maximum gain 75.1 / 34.5 / 12.8 / 7.2 at -25 / -21 / -15 / -11 dBm (bias -14 V); 3-dB bandwidth 48 GHz at -14 V,
  1.7 GHz at -5 V, 48.3 GHz at -15 V (-15 dBm input); GBP about 615 GHz; geometry w_Ge 0.5 um, H_Ge 260 nm (derived),
  L_Ge 5 um, ridge 0.74 um, SOI 220 nm, shallow etch 70 nm, BOX 2 um.
- `cmp_lit_xiang2022_gc` (fiber_chip_coupler.grating, soi): about 5.4 dB at 1310 nm, `loopback_half`, measured (GC
  pair + straight waveguide test structure; no pair total printed, D167 / D452).
- Not entered: receiver sensitivity at KP4-FEC (BER 2.4e-4) -21.3 / -17.8 / -12.6 dBm for 50 / 80 / 100 Gbps NRZ at
  -13.5 V and -13.2 / -11.3 dBm for 25 / 50 Gbaud PAM4 at -12.5 V (p.5-6, Fig. 7), reference PIN PD -13.7 dBm at
  50 Gbps, -4 V, 7.6 dB improvement (no parameter); eye-diagram SNRs and TDECQ 2.99 dB; simulated Ge absorption
  93.3 % (5 um) / 97.7 % (8.6 um) / TM0 89.8 % (absorption efficiency, not a QE); doping-region widths (no parameter);
  "> 30 GHz for |Vbias| > 10.5 V" range statement; ~0.5 dB optimized GC (cites ref. [38]); Table 1 rows of other works
  (rule 3). The reference PIN PD on the same chip has no own value besides the sensitivity: no row (rule 9).
- Orgs: no fab statement naming an org ("fabricated with a standard 180 nm MPW processes provided by silicon
  photonics foundry", p.3 / p.6): fab empty, `process_name` "standard 180 nm MPW process (silicon photonics foundry not
  named)" (D536 printed node wording). No facility named (funding only). No missing org.
- Judgment calls: (1) 0.93 A/W `measured` with the GC loss in `excludes` (printed directly, no arithmetic shown;
  D167 / D452) rather than `derived` (D394 / D166 analogue): auditor to confirm. (2) Gain rows 75.1 / 34.5 / 7.2 carry
  bias -14 V from the sentence "maximal multiplication gain by increasing |Vbias| to 14 V"; Fig. 3(c) top -25 dBm marker
  reads about 73 against the printed 75.1 (note, D417). (3) 1.7 and 48.3 GHz rows `wavelength_inferred` 1310 nm;
  48 GHz and GBP take 1310 nm from Table 1. (4) Platform `soi` (Ge on a shallow-etched Si ridge fed by a strip
  waveguide); a soi_rib reading of the active region is possible.

## runge2015 (ECOC 2015, 3 pages, IEEE copy): 1 component / 11 metrics

- `cmp_lit_runge2015_inp_pin_pd_chip` (photodetector.other, inp; D152 InP-native waveguide PD): responsivity
  > 0.45 A/W over the C-band and typically 0.5 A/W over the O-band (ref_plane unspecified; chip includes the SMF SSC);
  dark current < 2 nA up to 5 V reverse (chip-level, incl. RC-bias network and substrate leakage); 3-dB bandwidth
  130 GHz at 2 V and 120 GHz at 3 V (1550 nm per the Fig. 4 legend, TE); Tab. 1 1-dB compression at 2 V: optical input
  13 / 13.6 / 14.2 dBm and photocurrent 11 / 12 / 13 mA at 95 / 120 / 130 GHz. Reverse biases stored negative (merged
  convention); the paper prints positive values (notes / conditions).
- Not entered: PDL -0.25 to +0.25 dB O- to L-band (p.2, Fig. 1), optical return loss below -30 dB (p.2, Fig. 2),
  3OIP 10 / 9 / 7 dBm at 95 / 120 / 130 GHz, 2 V (p.2, Fig. 6), RF output power at 1-dB compression -2.1 / -5.3 /
  -8.3 dBm (Tab. 1): no parameter on photodetector (registry gaps below). Packaged "100 GHz and above is expected"
  (p.3, projection). 1310 nm response identical to 1550 nm up to 67 GHz (no value).
- Orgs: fab empty (p.1 passive "have been fabricated", all authors Fraunhofer HHI; D80b). Acknowledgment thanks Finisar
  Germany staff for discussion only (no role). No missing org.

## Missing fab / facility orgs

None. All ids used exist in the registry (`org_ibm_research_zurich`, `org_binnig_and_rohrer_nanotechnology_center`).

## Registry gaps (skipped value + locator + proposed definition)

1. `pdl_db` on photodetector: runge2015 PDL within -0.25 to +0.25 dB, O- to L-band (p.2, Fig. 1). Widen pdl_db to
   photodetector (chip-level polarization dependence of responsivity, reference plane in condition).
2. `back_reflection_db` on photodetector (D436 candidate): runge2015 optical return loss below -30 dB, O- to L-band, SMF
   at the SSC facet (p.2, Fig. 2).
3. `oip3_dbm` (photodetector): third-order output intercept point at the stated RF frequency and bias; runge2015
   10 / 9 / 7 dBm at 95 / 120 / 130 GHz, 2 V (p.2, Fig. 6).
4. `rf_output_power_dbm` (photodetector): RF output power at the stated compression point / frequency; runge2015
   -2.1 / -5.3 / -8.3 dBm at 95 / 120 / 130 GHz (p.2 Tab. 1); beckerwerth2021 notes hold similar values.
5. `rx_sensitivity_dbm` (photodetector; D436 / D443 candidate): xiang2022 -21.3 / -17.8 / -12.6 dBm NRZ 50 / 80 /
   100 Gbps and -13.2 / -11.3 dBm PAM4 25 / 50 Gbaud at KP4-FEC (p.5-6, Fig. 7).
6. `kappa_absorption_mhz` and / or `q_absorption` (resonator; D430 candidate): riedhauser2025 kappa_abs / 2pi median
   55 MHz (p.6), Q_abs 3.8e6 (p.7 Table 1); absorption-only share of the intrinsic loss rate (method in notes).
7. `thermal_drift_ghz_per_k` on resonator (D443 candidate on wdm): riedhauser2025 -4.92 GHz/K measured, -4.42 GHz/K
   thermorefractive part (p.17, Fig. S6).
8. Kerr nonlinear index (material / mode property, e.g. `n2_m2_per_w` on waveguide_platform / resonator):
   riedhauser2025 1.7e-18 (mode) / 1.8e-18 (BaTiO3) m2/W (p.6, Table S4). Possibly out of the component scope; listed
   for the coordinator.
