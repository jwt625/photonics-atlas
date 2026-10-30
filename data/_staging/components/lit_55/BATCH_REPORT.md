# lit_55 distill report (2026-10-30)

Classes: phase_shifter, photodetector, waveguide_platform (plus the fiber-chip couplers the papers characterize).
Papers: mcnab2003, cavalier2011, vlasov2004, derose2011, kang2008, yin2007, vivien2009, campenhout2010. All eight are
`restricted_local_only`: facts and locators only. Page-1 titles and authors match the source rows; none is a
correction / erratum or a 1-page file; no `garbled_text_layer` flag. Nothing from these sources was merged before.

Result: 35 components, 285 metric rows. Dry-run: `batch lit_55: +35 components, +285 metrics; errors 0` (only the
pre-existing WARN on cmp_lit_ni2025b_pimmwc-m18).

Renders read: mcnab2003 p.3 (Fig. 1), p.8 (Fig. 4), p.12 (Table 1); vlasov2004 p.9 (Fig. 4); cavalier2011 p.8 (Fig. 5,
Fig. 6, also the embedded images); derose2011 p.4 (Fig. 2), p.5 (Table 1, Fig. 3); campenhout2010 p.2 (Fig. 2, Fig. 3).

## Per paper

| paper | components | metrics | rows |
|---|---|---|---|
| mcnab2003 | 4 | 27 | strip WG 450 x 220 (waveguide_platform.straight), F-S spot-size converter (fiber_chip_coupler.edge), membrane W1 PhC WG (slow_light), strip-to-PhC butt coupler (waveguide_platform.other) |
| vlasov2004 | 4 | 23 | strip WG 445 x 220 (straight), 90-degree bends R = 1 / 2 / 5 um (bend, three sibling rows) |
| cavalier2011 | 1 | 9 | NbN SNSPD array under a Si3N4 rib on sapphire (photodetector.snspd) |
| derose2011 | 15 | 106 | Ge waveguide n-i-p PD, the 15 W x L variants of Table 1 (ge_waveguide) |
| kang2008 | 2 | 16 | 30 um Ge/Si SACM APD (apd, platform other: bulk Si), co-fabricated Ge/Si PIN reference (vertical) |
| yin2007 | 4 | 42 | Ge WG PD A 7.4 x 50 and B 4.4 x 100 (ge_waveguide), Si rib WG (straight), facet lateral taper (edge) |
| vivien2009 | 2 | 24 | butt-coupled Ge pin PD 15 x 3 um (ge_waveguide), SOI rib WG (straight) |
| campenhout2010 | 3 | 38 | NiSi slab heaters w = 1 / 2 / 3 um (phase_shifter.thermo_optic, sibling rows) |

## Values deliberately not entered

- mcnab2003: uncorrected PhC cut-back slope 20.7 +/- 2.4 dB/cm (superseded by the printed 24.2 corrected value, in
  notes); 2 mm PhC attenuation 5.6 dB normalized on the reference circuit (mixed scope, notes); 12 nm low-loss
  bandwidth, 1512 nm cutoff, lattice constant 445 nm, hole radius 0.37a, slab 0.5a (no parameters; notes); fiber
  misalignment 3-dB tolerance +/- 1 um (D250: 3-dB tolerances rejected); coupling repeatability < 0.2 dB (no
  parameter); "about 1 dB" butt-coupler difference at 1505 nm (includes the 29 um PhC; superseded by the 1.3 dB pair
  bound).
- vlasov2004: R = 1 um TE 0.2-0.3 dB/turn "at longer wavelengths" (span not stated; Fig. 4 rises beyond about
  1550 nm with dips; noted); R = 5 um TM (negligible, no number); Table 1 / Table 2 comparison values of other works;
  0.1 dB coupling repeatability and 0.5 dB/cm error bound (notes); TM cutoff 1400 nm (notes).
- cavalier2011: SiN test-waveguide loss about 15 dB/cm (cut-back) and end-fire coupling loss about 15 dB (p.4-5): the
  introduction (p.3) says the waveguide-development studies are recalled from the authors' ref. 8 (IEEE TAS 2011), so
  D259 / D259a applied (see question 1); total attenuation about 32 dB (estimate built on those values); 0.25 % mode
  exposure (from the PhD thesis, ref. 13); Tc 11.7 K, Jc 9.3 / 10.7 MA/cm2, SNR up to 1e4 (no parameters); meander
  SNSPD-A I-V (role and optical coupling not stated).
- derose2011: NEP column of Table 1 (no parameter; printed in each row's notes); lowest dark current density about
  40 mA/cm2 at 1 V (Fig. 3(a) width averages over 11 measurements, not tied to one variant; D165 / D254); open-circuit
  voltage 0.4 V; built-in field estimate.
- kang2008: breakdown-voltage thermal coefficient 0.05 %/degC (12 mV/K) and keff about 0.1 (no parameters); calculated
  13 GHz transit-limited bandwidth and expected 0.55 A/W responsivity (calculations with literature inputs); APD
  responsivity / gain curve of Fig. 2(b) (no printed number besides the operating gains).
- yin2007: polarization dependence < 1 dB (pdl_db not allowed for photodetector, gap below); pad capacitance 23 fF
  (pad, not the diode); calculated -0.1 dB free-carrier loss and 2-5 % scattering at the Ge transition (calculated /
  unattributed); "below -1 dB" with a vertical taper (cited work); 4.5 um input taper width (an up-taper facet width,
  not an inverse-taper tip; notes only, to keep the edge_taper drawing correct).
- vivien2009: extrapolated external responsivity > 0.8 A/W (rests on cited coupler / loss values); QE x bandwidth
  33.6 GHz (no parameter).
- campenhout2010: excess propagation loss of the silicided rib 25 dB/cm (s = 0.5 um) and < 1 dB/cm (s = 1 um): heater
  width not stated and no per-length phase-shifter loss parameter (D250), kept in notes; Rsh 12.8 ohm fit; simulated
  < 15 mW for w < 0.5 um and the s = 1 um curve (design curves without a specific design); thermal crosstalk > 20 dB
  at 10 um (simulated, no parameter).

## Judgment calls

1. Pair values halved: mcnab2003 F-S converter (Table 1 "for pair" 1 dB -> 0.5 dB) and S-PhC butt coupler (1.3 dB ->
   0.65 dB, `le`) entered as `loopback_half`, `derived`, with the printed pair value and error in notes; the TM
   converter "upper estimate of approximately 2 dB" for the pair -> 1 dB `le`, `author_estimate` (rests on the TM strip
   loss "below 3 dB/cm" of unstated origin).
2. mcnab2003 butt coupler class `waveguide_platform.other` with `transition_loss_db` (one Si layer on both sides;
   xiao2022 / cheng2025 precedent from the lit_48 audit). W1 PhC as `waveguide_platform.slow_light` (xiao2022).
3. Responsivity basis: derose2011 `author_estimate` (coupling and propagation losses "calibrated out", calibration
   origin not stated, skill rule 4); vivien2009 `author_estimate` (reference-branch power corrected with a rib loss
   "~1 dB/cm" of unstated origin and an assumed equal star-coupler split); yin2007 `derived` (input power computed
   from the paper's own measured 3.0 dB facet and 0.55 dB/cm rib losses, D166 analogue); kang2008 PIN `measured`
   (direct, reference plane not stated -> `unspecified`). QE values follow their responsivity basis (printed
   conversions -> `derived` where the responsivity is measured / derived).
4. derose2011: the 1.3 x 4 um2 45 GHz value entered with the Table 1 footnote bias (1 V); the Fig. 5(b) caption says
   2 V (noted). The 37 GHz at 0 V / 30 uA is attributed to the 1.3 x 4 um2 device from the Fig. 5 paragraph context
   ("the photodiode", singular); flagged (question 2). Capacitances `author_estimate` (C = eps A / d). 15 sibling rows
   (skill rule 9).
5. yin2007 bandwidths: optical and electrical (power) 3-dB values both entered as `bw3db_ghz` with the definition in
   `condition` (same measurement).
6. kang2008 APD platform `other` (vertical mesa on bulk Si; cmp_ofc2026_th3a5 precedent); PIN reference as a separate
   `photodetector.vertical` row (it carries the unity-gain responsivity, its own dark current density). Bias for the
   237 mA/cm2 row = 0.9 x -25.8 V = -23.22 V (computed for the required bias condition; noted).
7. cavalier2011: SNSPD critical current 11-14 uA read off the Fig. 5(b) I-V peaks of Nw21-Nw24 (`extracted_from_figure`,
   range, n = 4); dark-count rate <= 30 cps for Ib/Ic up to about 0.69 read off Fig. 6(a). Nanowire width as
   `absorber_width_um` (0.04, derived) and the SiN ridge as `width_nm` (brisson2023 convention).
8. campenhout2010: Rs of w = 2 / 3 um read off Fig. 3(a) (about 27 / 21 ohm); MZI extinction about 25 dB read off
   Fig. 2; s (lateral heater-to-core distance) as `heater_gap_um` with a note; 200 um = five 40 um elements in parallel.
9. Unit rescales of printed um / nm dimensions are `derived` with the printed value in notes (D157 / D256); figure-label
   thickness (kang2008 "i Ge 1um") likewise.
10. Fab orgs: mcnab2003 / vlasov2004 `org_ibm_watson` ("etched in a standard 200mm CMOS line at IBM Watson Research
    Center"); campenhout2010 `org_ibm` (borderline: "standard IBM CMOS technology" STI / NiSi modules, all authors at
    IBM Watson; parent org because the statement names IBM technology, not a site); derose2011
    `org_sandia_national_laboratories` (borderline: "integrated into Sandia National Laboratories CMOS compatible
    silicon photonics process" + "We have fabricated"; authors at Sandia, IQE, MIT); vivien2009 `org_cea_leti`
    (borderline: acknowledgment of the LETI 200 mm clean-room staff "for the fabrication" of the optical structures).
    Empty: cavalier2011 (authors at four orgs, D154), kang2008 ("We designed and fabricated", authors at Intel, UCSB,
    UVA and an independent address), yin2007 (passive processing statement, all authors at Intel, D80b). No shared
    facility is acknowledged in any paper (IBM MRL staff thanks: staff thanks / company cleanroom, D404).

## Missing organizations

None needed: all fab orgs used are in the registry (org_ibm_watson, org_ibm, org_sandia_national_laboratories,
org_cea_leti). Not entered as orgs (no fabrication / facility role stated): IQE Silicon Compounds (derose2011 p.1
affiliation; org_iqe exists), IPAG, CEA-INAC, IMEP-LAHC Grenoble (cavalier2011 p.2 affiliations).

## Registry gaps (confirmed skipped values)

| proposed parameter | class | value, locator | definition |
|---|---|---|---|
| noise_equivalent_power_w_per_rthz | photodetector | derose2011 Table 1 (p.5): 3.8E-14 to 6.6E-13 W/Hz^0.5 for the 15 variants, at 1.5 um | NEP at the stated wavelength / bias |
| breakdown_temp_coeff_pct_per_k | photodetector | kang2008 0.05 %/degC (12 mV/K), 200-340 K, p.4 Sec. 3, p.5 Fig. 3 | (dVbd / Vbd) / dT as defined |
| critical_temperature_k, critical_current_density_ma_per_cm2 | photodetector | cavalier2011 Tc about 11.7 K (p.7, Fig. 5(a)); Jc 9.3 / 10.7 MA/cm2 at 4.2 K (Fig. 5(b) labels, p.7) | superconducting detector film / wire properties |
| pdl_db widened to photodetector | photodetector | yin2007 "measured polarization dependence is smaller than 1dB" (p.4) | polarization-dependent responsivity |
| lattice_constant_nm / hole_radius_nm (repeat of lit_48) | waveguide_platform | mcnab2003 a = 445 nm, r = 0.37a (SEM), p.3 / p.10 | PhC geometry |
| excess loss per length for phase shifters (D250 rejected; listed only) | phase_shifter | campenhout2010 25 dB/cm (s = 0.5 um), < 1 dB/cm (s = 1 um), p.2 | no new proposal |

## Open questions for the audit / coordinator

1. cavalier2011: keep the D259 exclusion of the SiN test-waveguide values (15 dB/cm, 15 dB coupling) given the
   section-level attribution to ref. 8 in the introduction (p.3), or enter them (no citation in the value sentences
   themselves; D408 reads attribution at the value sentence)?
2. derose2011: 37 GHz at 0 V / 30 uA attributed to the 1.3 x 4 um2 device by paragraph context; remove under D159 if
   the context is judged ambiguous. Also the 1 V (Table 1) vs 2 V (Fig. 5(b) caption) bias for the 45 GHz value.
3. Responsivity basis for "calibrated out" losses of unstated origin (derose2011, 15 rows): `author_estimate` here;
   `measured` if the coordinator reads "calibrated out" as an own de-embedding.
4. Borderline fab orgs: campenhout2010 org_ibm, derose2011 org_sandia_national_laboratories, vivien2009 org_cea_leti
   (reasons above).
5. Cross-source note (report only, not in rows): vlasov2004 (same group, p.6) describes the mcnab2003 strip as
   465 x 220 nm (mcnab2003 prints 450 nm) and argues the mcnab2003 12.5 dB/cm at 1330 nm belongs to wavelengths
   shorter than 1300 nm (LED short-wavelength wing). Rows keep each paper's own statements.
