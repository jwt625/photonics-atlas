# Batch report pilot_2 (2026-10-20)

Transcribed by the coordinator from the subagent's final message (subagents cannot write report files).

Result: 20 components, 63 metric rows; merge dry-run 0 errors, 0 warnings. host_device_id values checked against EO devices.csv; fab_org_ids against organizations.csv. No network, no git, no e-mail addresses, no source text beyond a few words.

## Per paper

- li2025b (suspended GaAs): 3 components, 10 metrics. GC focusing (7.0 dB per coupler at 1540 nm from the two-GC structure halved; Fig. 11(c) readings 7.4 / 8.5 dB at 1550 / 1560 nm; width 15 um, pitch 889 um design); Y-splitter (1.0 dB excess, derived, de_embedded; figure readings 0.9 / 1.4 dB); racetrack (per-resonance loss ~3.3-4.0 dB/cm over 1541-1558 nm from Fig. 14(b); gap 385 nm design). Not entered: Q_loaded, FSR, ER, 3.71 dB/cm mean (in EO row li2025b-b); 5.5 dB/cm (in li2025b-a; conflicts with 3.71 dB/cm in App. C); 13.8 dB budget term (EO); 2.4 dB/cm (cited [31]); Euler bend radius and tethers (no result). Fab not stated (wafer source only: a national epitaxy facility, not in the registry).
- hulyal2026 (OFC, restricted): 2 components, 5 metrics. AWG (106 GHz spacing, 85 GHz 3-dB BW, 5 dB IL scope unspecified, 8 channels design); edge taper (4 dB, scope unspecified). Not entered: FSR (no number), cascaded-AWG crosstalk "below -20 dB" (no parameter, G1), 10 dB full-chain loss (includes the MZM), cited AWG IL. Platform empty (EO row has none; rib/strip not stated).
- liu2026d (visible/NIR TFLN, fab Luxtelligence): 8 components, 28 metrics. Three edge couplers (19 dB/facet at 488 nm, 16 dB/facet at 640 nm, 3.0 dB/facet at 940 nm; simulated counterparts; tips), 1x2 and 2x2 MMI (~1.5 dB each at 488 nm, de_embedded), three TOPS (P_pi at 445-940 nm; 39.2 mW at 461 nm by the in-situ method; 750 um; 293.15 K). Not entered: TO 3-dB bandwidths 6.4-7.8 kHz (G2), heater resistance ~80 ohm (G3), relaxation constants (EO), mode filters (no result), hypothetical tip widths, SI tables (not cached), Table 2 (other works). Inconsistency noted: Table 1 6.4 kHz vs text 6.6-7.8 kHz.
- wu2025 (BEOL TFLN on CUMEC SiPh): 5 components, 18 metrics. Si-TFLN VAC (> 97 %, 0.11 dB derived by the authors, per_interface; taper 200 um, tip 180 nm), Si-SiN transition (0.06 dB; 35 um), SiN edge coupler (1.6 dB TE per_coupler, 7.5 um MFD fiber; 350 nm tip), Si TOPS (17.1 mW), Ge PD (55 nA at -1 V; > 0.8 A/W 1540-1560 nm, figure readings 1.2 / 0.85 A/W; 47 / 56 GHz at -1 / -2 V; 55 um). CUMEC set on Si-side components only. Not entered: typical MMI 0.3 dB (projection input), simulated VAC tolerance (criterion unstated), 0.27 dB/cm (cited), link bandwidth, projected < 1.5 dB IL.
- didier2026 (LN on sapphire, mid-IR; cleanrooms BRNC, FIRST): 2 components, 2 metrics. Straight waveguide 1.0 dB/cm at 3.7 um by cutback (other points already in EO rows); TOPS P_pi 1420 mW at 4 um (caption 1.43 W, text 1.42 W). Not entered: mid-IR GCs (SI not cached), TOPS length (caption 1.34 mm vs legend 0.22 cm), heater gap (G3), facet loss (intercept not stated), setup equipment (external T2SL detector, QCL sources). Fig. 3(d) stray marker = legend symbol.

## Organizations not in the registry

National epitaxy facility (wafer source, li2025b p.7); ShanghaiTech Material and Device Lab (external detector fab, didier2026 p.7/p.9; parent ShanghaiTech University exists); NanoLN, NGK Insulator (wafer suppliers, not checked).

## Judgment calls

1. liu2026d per-facet "estimated" values entered as author_estimate (p.9 also calls them measured; from test structures).
2. li2025b halved GC loopback = measured; Y-splitter by differencing = derived.
3. Test structures linked to the EO device whose loss budget uses them.
4. One host per design when a design spans several EO rows (others named in notes).
5. Racetrack that is itself an EO device classed resonator.ring; only values the EO row lacks.
6. Platform not copied where the component sits on another layer (wu2025 Si parts soi / si_sin_multilayer); liu2026d keeps lnoi_rib although the paper says fully etched strip.
7. c_band inferred where no wavelength is stated (noted).
8. "as low as" not a statistic; "exceeding" -> gt.
9. Fiber MFD of a measurement or simulation in `condition`, not mfd_fiber_um.
10. Geometry already in the EO row not re-entered.
11. Figure readings only where unambiguous, qualifier approx, reading uncertainty in notes.

## Gaps reported (G1-G14)

G1 WDM crosstalk of unstated type; G2 phase-shifter modulation bandwidth (kHz); G3 heater resistance and heater gap; G4 loss scope for a single component (per_component); G5 taper geometry on layer transitions; G6 VAC: transition_loss_db vs insertion_loss_db per_interface; G7 required wavelength when the source gives none; G8 basis for "estimated" values from test structures, and for assumed simulation inputs; G9 PD dark-current density, cutoff wavelength, active area (only if setup equipment is in scope); G10 tolerances with a non-1-dB criterion; G11 laser tuning range; G12 platform lnoi_strip and components on another layer than their EO host; G13 validator should check host_device_id against EO devices.csv; G14 rule 2 wording (does geometry count; one or several hosts).
