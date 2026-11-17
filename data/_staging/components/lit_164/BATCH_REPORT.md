# lit_164 batch report

Papers: lit:schuler2016, lit:youngblood2014, lit:shiue2015. Distilled 2026-11-16 (verified_on 2026-11-16).
Validation: `merge_component_staging.py data/_staging/components/lit_164 --dry-run` -> +10 components, +36 metrics,
0 errors, no warnings on batch rows.

| paper | components | metric rows |
|---|---|---|
| schuler2016 | 5 | 16 |
| youngblood2014 | 3 | 10 |
| shiue2015 | 2 | 10 |
| total | 10 | 36 |

Cached-copy identity (page-1 title check): all three are arXiv versions with the journal titles (schuler2016
1610.05526 incl. Supporting Information on text pages 12-19; youngblood2014 1402.7127; shiue2015 1507.00426v3, no
supporting information in the file). Component notes say so. No correction / erratum, no other paper.

`garbled_text_layer`: schuler2016 garbled pages 10-11 are the reference list; elsewhere the text layer renders the
micro and ohm signs as "P" / ":" ("3 Pm", "4 Pm", "14-22 :cm"); checked on a page render of p.3. youngblood2014 drops the micro sign
("0.2 dB/m", "90m", "2.5 m", "3 m"); every value with a unit was checked on page renders (p.4, p.6, p.8, Fig. 2
caption p.12): dB/um, 90 um, 2.5 um, 3 um. Renders of pages not in `figures/` were made into the scratchpad only.

## schuler2016 (5 components, 16 metrics)

Rows: graphene PTE photodetector sample B (Al2O3, best device: 35 / 76 mA/W, 65 GHz, SOI stack); sample A (hBN,
W = 30 um: ~3 / ~18 mA/W); grating coupler (43.7 %, 3.6 dB per coupler, cutback, Supp. Fig. S2(b) labels); 800 nm
strip waveguide (1.5 dB/cm cutback, width label); strip-to-slot mode converter (simulated 98-99 % plateau, Fig. S1).
PD platform `soi_slot`.

Not entered and why:
- Open-circuit responsivities 3.5 V/W (B) and ~0.9 V/W (A): no V/W parameter (registry gap 1).
- Impulse response 30 ps FWHM -> ~15 GHz (0.44 / dt): the paper calls it the setup limit; the heterodyne 65 GHz is
  the bandwidth value.
- Highest RF output power -31 dBm at 1 GHz (19.4 dBm optical input, 1.2 V bias, p.9): no parameter (gap 2).
- Device resistances ~300 / ~110 ohm, R_C + R_U = 254 ohm, mobilities ~2000 / ~1000 cm2/Vs, sigma_min, V_Dirac:
  graphene channel / model quantities, not series resistance.
- Model PC estimate R_I ~ 1e-2 A/W at 400 mV (p.7): calculation, not a measurement.
- Slot gap 80 nm and strip width 250 nm: in core_material only (gap_nm not allowed on photodetector; width_nm would be
  ambiguous between strip and slot). Drain-source separation 4 um in core_material.
- Fabricated mode-converter length: not printed in the text; the Fig. 1(b) inset carries a 10 um label whose meaning
  is not stated (noted, not entered).

Fab / facility: none. Fabrication sentences are passive (p.3); authors at TU Wien (two institutes) and AMO GmbH;
no facility acknowledged. No missing org.

Judgment calls:
1. 65 GHz (Fig. 4(b)) does not name the sample; entered on sample B because the abstract ("Extrinsic responsivities
   of 35 mA/W ... The device exhibits a 3 dB-bandwidth of 65 GHz") and the summary attribute it to the device that
   gives 35 / 76 mA/W, and the preceding impulse measurement is on sample B. Alternative (D159 strict): move to
   component notes.
2. Responsivities `author_estimate`: the paper normalizes to in-waveguide power with eta_C ~ 0.4 and states it
   assumes no loss in the 2 mm waveguide and mode converter (rule 4, assumed input); its own 1.5 dB/cm cutback would
   add about 0.3 dB. All are printed in mA/W (conversion noted).
3. Grating coupler and waveguide wavelengths: not printed for the cutback; C band inferred from the 1560 nm
   characterization laser.
4. Mode converter: fabricated row with only simulated values (D80e); value range read across the Fig. S1 plateau
   (5-10 um) because the fabricated length is not printed.

## youngblood2014 (3 components, 10 metrics)

Rows: dual-layer graphene photodetector / modulator (one design: 3.6 mA/W and 0.25 % QE at zero bias, 57 mA/W at
0.4 V on "a different device", 3 GHz photodetection bandwidth, 90 um length, 2.5 um channel, 110 nm SOI stack);
grating coupler (~20 %, author_estimate, origin not stated); bare Si MZI (ER > 40 dB before graphene transfer).

Not entered and why:
- Modulator function: gate-tuned absorption 0.2 -> 0.15 dB/um, 64 % modulation depth, 2.5 GHz modulation bandwidth,
  18 dB added arm loss / ER 1.6 at V_g = 0 (rule 2: EO-atlas candidate; graphene electro-absorption modulator).
- "Less than 0.1dB" excess arm loss: an inference from the MZI extinction, not a separate measurement.
- Electrical / material quantities (CNP +33 V, 1.4e13 cm-2, E_F, mobility 1150 cm2/Vs) and model bandwidths ~6 / ~9
  GHz, model absorption tuning to 5 %: not component metrics or model only.
- Internal efficiency 6-16 % near the contacts (p.6): estimate under a high-field assumption, no locator to own data.

Missing orgs (registry): fab "University of Minnesota" (author contributions p.10: "N.Y. fabricated the devices",
all authors at the University of Minnesota; D72 / D80b) on all 3 rows; facility "University of Minnesota
Nanofabrication Center" and "Characterization Facility" (University of Minnesota, MRSEC network member) (p.10, "Parts of
this work was carried out in") on all 3 rows. fab_org_ids / facility_org_ids left empty until the org round.
Material suppliers (notes): SOITEC Corp. (SOI wafer), Graphene Square Inc. (CVD graphene).

Judgment calls:
1. One component row for the design (rule 9): m1 / m2 from the main device, m3 from "a different device", m4 from
   "the device" of Fig. 4; conditions name the device. The paper never says the second device differs in design.
2. Responsivity and QE rows `author_estimate`: the input-power reference subtracts the input grating coupler (~20 %,
   origin not stated) and the MZ split (Methods p.9).
3. Photodetection wavelength not printed: C band inferred from the stated 1.55 um (0.8 eV) operating point.
4. MZI entered as `splitter.other` with `extinction_db` (D74: extinction of an interferometer built from the
   splitters; splitter type not stated). Alternative: drop the row (test structure for absorption calibration).
5. absorber_width_um = 2.5 um is the source-drain channel across the waveguide ("2.5 um long graphene channel").

## shiue2015 (2 components, 10 metrics)

Rows: hBN/SLG/hBN photodetector (0.36 A/W at V_DS = 1.2 V, 78 mA/W at zero bias, 42 GHz at zero bias, internal QE
16-19 %, 2.2 dB stack insertion loss, 40 um, 520 x 220 nm Si); SiN mode-converter edge-coupler link (11 dB
fiber-to-fiber before stack deposition).

Not entered and why:
- Absorption coefficient 0.055 dB/um (authors' 2.2 dB / 40 um) and 0.043 dB/um (simulated): no
  absorption-coefficient parameter on photodetector (gap 3); the 2.2 dB enters as insertion_loss_db.
- Autocorrelator / nonlinear response: I ~ P^0.47 at 1800 nm (250 fs, 78 MHz), minimum response time ~3 ps (HWHM),
  1.4 uW average / 67 mW peak power, saturation onset above ~50 mW peak: no parameters (gap 4); the saturation
  statement is qualitative.
- Spectral response uniform over 1510-1570 nm and detection range 1500-1800 nm: no parameter for a PD spectral range.
- Minimum device resistance 77 ohm (graphene channel), Hall mobility 40,000-60,000 cm2/Vs (separate stacks on SiO2).
- Drain electrode 200 nm from the waveguide: no parameter (in core_material).

Missing org (registry): facility "Center for Functional Nanomaterials, Brookhaven National Laboratory" (p.9-10:
"Device fabrication was partly carried out at") on both rows. Fab empty: "We fabricated this 2D heterostructure in a
BEOL step on a SOI PIC, which was fabricated in a CMOS-compatible process" (p.2) with authors at MIT, Columbia, IBM
T. J. Watson and ICFO (own org ambiguous, D154); no foundry or process name for the PIC (no process_name: "CMOS-
compatible process" is generic).

Judgment calls:
1. 0.36 A/W `measured` (printed in A/W, in-waveguide power reference whose derivation from the fiber power is not
   stated; noted). 78 mA/W `derived` (mA/W -> A/W, D256).
2. Internal QE 16-19 % `author_estimate`: the 1.7 dB end of the absorbed fraction is the simulated absorption.
3. Stack insertion loss 2.2 dB on the PD row (`derived`, before / after on the same waveguide, scope per_component,
   method reference_structure). Alternative: a separate waveguide_platform row for the graphene-loaded section
   (ding2019 precedent) carrying 0.055 dB/um as 550 dB/cm.
4. Responsivity wavelengths C band inferred (transmission at 1550 nm, c.w. spectral response 1510-1570 nm).
5. SiN mode converters: the design is "as reported previously" (ref. 38, own earlier work), but the 11 dB is a
   measurement on this chip, so it is entered (fiber_to_fiber, platform `sin` per D82f).

## Registry gaps (proposed)

1. `responsivity_v_per_w` (photodetector, V/W): open-circuit photovoltage responsivity of PTE / bolometric
   detectors. Skipped: schuler2016 3.5 V/W (sample B, p.7) and ~0.9 V/W (sample A, p.6).
2. `rf_output_power_dbm` (photodetector): highest RF output power at a stated frequency, optical input and bias.
   Skipped: schuler2016 -31 dBm at 1 GHz, 19.4 dBm optical, 1.2 V (p.9).
3. `absorption_db_per_um` (photodetector; or the D417 "absorbed fraction" candidate): absorber-loaded waveguide
   absorption. Skipped: shiue2015 0.055 dB/um (derived, p.4) and 0.043 dB/um (simulated, p.4-5).
4. `response_time_ps` (photodetector): intrinsic response / carrier relaxation time from pump-probe or
   autocorrelation (definition in condition). Skipped: shiue2015 ~3 ps HWHM (p.8, Fig. 4(c)).

## EO-atlas candidates

youngblood2014 graphene electro-absorption modulator: 64 % modulation depth over 90 um (Fig. 2(e)), 2.5 GHz
modulation 3-dB bandwidth (Fig. 4(b)), absorption 0.2 -> 0.15 dB/um for V_g +33 -> -40 V, 18 dB added arm loss.
