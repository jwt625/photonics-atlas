# lit_233 batch report

Papers: lit:takiguchi1996, lit:zheng2023a, lit:ong2020, lit:doerr2005. Page-1 titles match the source rows; no
garbled text layer; none is a correction. verified_on 2026-11-20. Dry run of `merge_component_staging.py`: +7
components, +106 metrics, 0 errors; the one warning names the merged row cmp_lit_ni2025b_pimmwc, not in this batch.

| paper | components | metric rows |
|---|---|---|
| takiguchi1996 | 2 | 6 |
| zheng2023a | 2 | 32 |
| ong2020 | 1 | 61 |
| doerr2005 | 2 | 7 |

## takiguchi1996 (lattice-form variable group-delay dispersion equalizer, silica PLC, JSTQE 1996)

Rows:
- `wdm.cascaded_mzi` equalizer (9 tunable-coupler MZIs + 8 delay MZIs): fiber-to-fiber loss 14.4 dB (mean over the
  Fig. 3 settings, measured; wavelength 1549 nm inferred from the Fig. 3 axis); FSR 50 GHz (design, author_estimate);
  8 delay stages; delta L 4138 um and min bend radius 5000 um (printed in mm, derived).
- `splitter.other` monitor tap: coupling ratio 0.04 -> 4 % (author_estimate: design vs measured not stated).

Not entered:
- Dispersion -681 to +786 ps/nm measured, -857 to +857 ps/nm calculated (p.1, p.5): no dispersion parameter.
- Operational range 16.3 GHz (p.5): defined as the smaller of the 1-dB-down transmittance and monotonic-delay regions;
  not a bw_1db_ghz.
- Loss variation within 0.4 dB over dispersion settings (p.5): il_nonuniformity_db is a channel / port spread.
- Core size printed "7.0 um^2" (p.2, p.5): no area parameter, side not stated. Si substrate 76 x 88 mm: substrate.
- Tunable-coupler 0-1 range and 0.01 pi phase accuracy: cite ref. [12] (rule 3). Fig. 5-7: numerical studies of other
  designs.

Orgs: fab empty. Passive "was fabricated ... by FHD and RIE [12]" (p.5); acknowledgment thanks four named people "for
fabricating the PLC device" without naming their org (D84b needs the staff's org, D543). No facility. No missing org.

## zheng2023a (8-channel LWDM on Si-LN hybrid platform, PTL 2023)

Rows:
- `wdm.cascaded_mzi` LWDM: 8 channels, 4.5 nm spacing (measured, after EO phase correction), average crosstalk ~12.8 dB
  (`crosstalk_db`, type not stated), 3-dB widths 3.7-4.8 nm, IL 7.5-10.4 dB (p.3; conclusion prints 7.6-10.4 dB,
  conflict noted), Table II "This work" IL 8.9 dB (statistic not defined), tuning power ~0 mW per channel
  (author_estimate); 3 stages; Table I delta L of MZIs A-G (7 rows); Si ridge 380 nm / 70 nm etch, 15 um taper, Si
  220 nm, BOX 2 um.
- `waveguide_platform.transition` Si-LN VAC: loss "normally less than 0.2 dB" (lt, typical, measured), simulated
  coupling > 99 %; 100 um taper 380 -> 180 nm, LN ridge 2 um (derived), LN 500 nm, LN etch 250 nm and 60 deg sidewall
  (measured, see judgment 2), SiO2 cladding 0.6 um (derived), BOX 2 um.

Not entered:
- LN EO phase shifters: VpiL about 3 V.cm DC measured, 2.32 V.cm simulated at 1 GHz (p.3); 1 mm length, 4 um gap. No
  phase_shifter VpiL parameter; no other performance metric, so no phase-shifter row. EO-atlas candidate.
- 0.98 dB/cm LN loss and 0.19 dB per VAC (authors' ref. [29], rule 3); "typical" 0.3 dB foundry MMI loss and the
  0.3 x 6 = 2 dB MMI share (p.4: foundry figure, not measured here).
- Table II rows of refs. [26]-[28].

Orgs: fab `org_chongqing_united_microelectronics_center` ("An MPW foundry (CUMEC, China) was used for the SOI
structure fabrication", p.3) on both rows, process_name "CUMEC MPW (SOI structures)"; LN bonding / etch / electrodes
are passive steps with no org named (authors at three universities), noted. No facility. No missing org.

## ong2020 (wafer-level SiN CWDM cascaded-MZI demux with Bayesian inference, PTL 2020)

Rows (one `wdm.cascaded_mzi` component, platform `sin`):
- Table I, per channel (4): centre wavelength, 1-dB bandwidth, IL at nominal lambda, crosstalk at nominal lambda, IL
  at the passband centre, crosstalk at the passband centre; each as a median row (n = 22, IQR in notes) and a min-max
  range row: 48 rows. IL scope `de_embedded`, method `reference_structure` (adjacent waveguide with the same edge and
  interlayer couplers). Crosstalk Max. / Min. stored as suppression magnitudes; "inter-channel" type not stated ->
  `crosstalk_db`. Centre-wavelength rows: wavelength span = the channel's Table I centre Min. to Max.
- Design: 4 channels, 20 nm grid spacing and FSR 40 / 80 nm (author_estimate), 2 stages, w0 750 nm, h0 400 nm, gap
  400 nm, bend radius 40 um.
- Extracted geometry (D80a derived): least squares width 716 nm / height 402 nm (median, n = 22), Bayesian 717 / 400 nm
  (median, n = 19).

Not entered: 85 deg sidewall (model assumption), +/-50 / +/-40 nm process variation (ref. [17]), Fig. 4 sensitivity
contours (simulated), Bayesian sigma, Fig. 2 spectra.

Orgs: fab empty: "We have designed and fabricated" (p.4) with authors at two orgs (IHPC A*STAR; Silicon Technologies
Centre of Excellence, NTU); design rules cite Compoundtek (ref. [17]) with no fabrication statement: process_name
"(Compoundtek design rules cited, ref. 17)" (Contract v7 cited-PDK style; `org_compoundtek` exists but is not set).
No facility. No missing org.

## doerr2005 (four-stage MZI-type TODC with single-knob control, PTL 2005)

Rows:
- `wdm.cascaded_mzi` TODC: IL 5.5 dB at the ITU grid incl. circulator (device_total, ref_plane module, C band inferred
  from the 100-GHz ITU grid / Fig. 4 axis); FSR 100 GHz (author_estimate, origin not stated); heater power ~650 mW at
  9.5 V (measured, approx); 4 stages; 6.0 um core height and 2.4 x 2.8 cm chip footprint (derived).
- `phase_shifter.thermo_optic` thin-film heater: resistance ~400 ohm.

Not entered: 460 ps/nm tuning range; usable bandwidth ~45 GHz (no level); PDW 58 pm; ITU alignment temperature 33.8 C;
BER penalties and 0.2 dB polarization dependence of sensitivity (system level); centre / outer heater power ratio ~1.4.

Orgs: fab `org_lucent_bell_labs` on both rows: "We made the device of Fig. 2" (p.2), all six authors at Lucent
Technologies, Bell Laboratories (D80b; ghosh1996 precedent). No facility. No missing org.

## Judgment calls for the auditor

1. Class of the two dispersion compensators (takiguchi1996, doerr2005): no TODC class; filed as `wdm.cascaded_mzi`
   (registry subtype text "cascaded MZI / lattice filter") by structure. Alternative: `wdm.other`.
2. zheng2023a LN etch depth 250 nm and sidewall 60 deg `measured`: the paper states W, h and theta "according to our
   fabricated waveguide profiles" (p.3) without a method; `design_target` if the auditor reads them as model inputs.
   W = 2 um kept as design (also stated as the VAC design width).
3. zheng2023a platform `lnoi_loaded_si` for the whole LWDM (light passes Si MMIs / delay arms and LN phase-shifter
   sections) as for the VAC (he2019 / wu2025 precedent); `soi` would describe only the filter-defining Si arms.
4. zheng2023a no LN phase-shifter row (only VpiL stated). A derived v_pi_v (~30 V from 3 V.cm / 1 mm) was not entered.
5. zheng2023a Table II "This work" IL 8.9 dB entered next to the 7.5-10.4 dB range with no statistic.
6. takiguchi1996 monitor tap as a separate `splitter.other` row with a 4 % author_estimate; FSR rows of takiguchi1996
   and doerr2005 as author_estimate (D82a / origin not stated).
7. ong2020 median + range rows per Table I cell group (IQR only in notes; no IQR statistic in the enum).

## Registry gaps (skipped value + locator + proposed definition)

- `dispersion_tuning_range_ps_per_nm` (wdm): takiguchi1996 -681 to +786 ps/nm (p.5, Fig. 3(b)); doerr2005 460 ps/nm
  range (p.1, p.3). "Range of group-delay dispersion settable on the device, ps/nm, signed ends as printed." Earlier
  gap lists (D540, D574, D578) name group delay / dispersion.
- `operational_bw_ghz` or a level-qualified passband (wdm): takiguchi1996 16.3 GHz (p.5, definition above); doerr2005
  usable bandwidth ~45 GHz (p.3, no level).
- `pdw_pm` (wdm, polarization): doerr2005 polarization-dependent wavelength shift 58 pm (p.2). "Centre-wavelength
  difference between TE and TM."
- `vpil_v_cm` on phase_shifter: zheng2023a ~3 V.cm DC measured / 2.32 V.cm simulated (p.3) (D558 lists it).
- Loss variation over tuning states (wdm): takiguchi1996 within 0.4 dB (p.5).
