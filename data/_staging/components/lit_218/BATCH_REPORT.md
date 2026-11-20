# lit_218 batch report

Papers: lit:huang2016b, lit:campbell1988, lit:ye2015, lit:lenox1999, lit:franco2005 (photodetector family). All five
cached texts match their source rows (page-1 titles checked). No paper had component rows before this batch. Values
from text layers were checked against page renders where the text layer drops symbols (franco2005 +/- values,
campbell1988 OCR-like text, ye2015 "OJ pF" = 0.3 pF). Figure reads use PyMuPDF renders of the cached PDFs at 5-12x zoom.

Validation: `uv run --offline python scripts/merge_component_staging.py data/_staging/components/lit_218 --dry-run`
-> +26 components, +135 metrics, 0 errors (one pre-existing warning on a merged row of another paper).

Totals: 26 components / 135 metric rows (measured 31, derived 16, extracted_from_figure 32, author_estimate 5,
simulated 1, design_target 50).

## lit:franco2005 (1 component / 13 metrics)

- `cmp_lit_franco2005_ingaas_inp_apd_on_gaas`: photodetector.apd, platform `other` (InP-lattice-matched epi transferred
  to SI-GaAs by epitaxial layer transfer, InP substrate removed). Mean breakdown 34.28 V, mean dark current 10.20 nA at
  90 % Vbr (n = 10), mean responsivity 5.9 A/W at 2 V below breakdown, gain > 40, max bandwidth 6.4 GHz at M = 7.5,
  GBP ~80 GHz at M = 30, five Fig. 4 bandwidth reads (M = 5 / 10 / 15 / 20 / 30), 900 nm absorber, 45 um junction.
- Not entered: mean punch-through 18.26 +/- 0.27 V (no parameter); +/- spreads are in notes (statistic `std` rows not
  added); p-i-n reference diode (no value of its own).
- Fab empty: passive wording, authors at three orgs (Solid State Scientific Corporation; AFRL/SNHC; University of
  Massachusetts Lowell Photonics Center; p.1 footnote); epi "grown commercially" (grower not named). No missing org
  needed for a row.

## lit:campbell1988 (2 components / 11 metrics)

- `cmp_lit_campbell1988_sagm_apd` (Figs. 3 / 5 devices): GBP 70 GHz measured and 72 GHz calculated (simulated), 8 GHz
  low-gain ceiling, 0.2 pF RC-estimate capacitance (author_estimate, origin not stated), Fig. 3 top gain ~35 at ~62 V
  (figure read), absorber 1.8-2.8 um range.
- `cmp_lit_campbell1988_sagm_apd_3um_ar` (Fig. 4 device, 3 um absorber, thinned substrate, AR coating): external QE
  > 90 % over 1.2-1.45 um, 75 % at 1.5 um, Fig. 4 responsivity reads 1.07 A/W (1.40 um) and 1.01 A/W (1.3 um).
- Not entered: dark current "< 50 nA at 90 % of breakdown" (abstract) and "typically 5-150 nA" with 1.5-6 nA primary
  multiplied dark current (p.2): breakdown voltage not printed (bias required) and the two statements disagree; gain
  "as high as 40" (bias not printed; Fig. 3 device read instead); calculated fields, free-carrier absorption 95 /cm,
  RC roll-off 11.5 GHz, 2.2 ps transit time (model values / no parameter); relative "10-15 % lower" QE statement.
- Fab `org_bell_labs` borderline (AT&T Bell Laboratories; first-person substrate thinning / AR coating sentence p.3 +
  thanks "for assistance with device fabrication" p.5, D84b). No missing org.

## lit:lenox1999 (2 components / 13 metrics)

- `cmp_lit_lenox1999_rc_sacm_apd_m200`: QE ~70 % at 1580 nm (unity gain), dark current < 10 nA at 90 % Vbr, gain > 50,
  breakdown ~24 V (figure read), unity-gain bandwidth 24 GHz, GBP 290 GHz, parasitic capacitance < 30 fF, F(M) 3.2 /
  5.1 at M = 10 / 20 (Fig. 1 diamonds), 60 nm absorber, 14 um mesa.
- `cmp_lit_lenox1999_rc_sacm_apd_m400`: GBP 130 GHz, ~11 GHz low-gain bandwidth (Fig. 5 read).
- Not entered: k ~ 0.18 (no parameter); bottom-DBR reflectivity ~95 % (earlier work, ref. [14], rule 3); Fig. 1
  homojunction InAlAs APD data (authors' earlier work refs. [8], [9], D259a); peak-response wavelength 1.58 um vs 1.55 um
  design (no photodetector parameter; in condition).
- Fab `org_the_university_of_texas_at_austin` ("We have designed and fabricated", all authors at the Microelectronics
  Research Center, UT Austin). No facility (no acknowledgment section).

## lit:ye2015 (3 components / 20 metrics)

- `cmp_lit_ye2015_design1_d60`: 1.3 A/W ("up to", qualifier le) at -10 V, 2 um; QE 81 % (authors' conversion, derived);
  8.92 uA dark current at -10 V; 6.5 GHz; ~0.3 pF; 2500 nm absorber; 60 um mesa.
- `cmp_lit_ye2015_design1_d50`: 1.7 uA at -5 V ("as low as", best).
- `cmp_lit_ye2015_design2_d50`: 0.93 A/W (le) at -10 V, QE 58 % derived, 2.88 uA at -10 V, 0.52 uA and 26.6 mA/cm2 at
  -5 V, ~10 GHz at -10 V (modulator-limited, noted), ~0.3 pF, packaged-module responsivity 0.52 A/W (`ref_plane
  module`, includes the 45-degree angled-fiber coupling), 2000 nm absorber, 50 um mesa.
- Not entered: Fig. 2(c) leakage density vs diameter for 100-500 um Design-1 mesas (plot only; each diameter would be a
  separate row with a figure read only); ideality factors 1.50-1.52, background doping 1e15 cm-3; BER 1e-12 at -9.9 dBm
  and eye results; RC-limited "10 GHz can be expected"; the implied module coupling loss (not printed as a value).
- Fab `org_tyndall_national_institute` ("we propose, fabricate and characterize", all authors at Tyndall). No facility.
- Temperature 20 C kept in condition text (temperature_k left empty).

## lit:huang2016b (18 components / 78 metrics)

- `cmp_lit_huang2016b_gc`: input grating coupler, 15 dB per_coupler author_estimate ("estimated ... as shown in
  Supplement 1"; supplement not cached).
- `cmp_lit_huang2016b_apd_w4_l10` (device of Figs. 1(d), 2(a)-(c), 3): breakdown -10 V (100 uA criterion), dark current
  < 0.1 nA to -1 V, 1 mA/cm2 at -2 V, 1 A/cm2 (1000 mA/cm2, derived) at -9 V with gain 5, bandwidth 25 / 27 GHz at gain 5
  and 23 / 25 GHz at gain 12 (raw measured / RF-loss-corrected derived), GBP 276 / 300 GHz (derived products), C 32 fF
  and R 10 ohm from the circuit-model fit (measured), QE ~59 % (Fig. 1(e) read), stack geometry.
- `cmp_lit_huang2016b_apd_w4_l50`: best responsivity 1.05 A/W and QE 84 % (author_estimate, see judgment 1), Fig. 2(d)
  ~16.3 GHz.
- `cmp_lit_huang2016b_apd_w4_l30`: wire-bonded receiver APD max bandwidth 20 GHz, QE 70 % (author_estimate), Fig. 2(d)
  ~20.4 GHz.
- 14 length / width series rows (4 um x 25 / 75 / 100 / 150; 6 um and 8 um x 10 / 25 / 50 / 75 / 100): Fig. 1(e) QE reads
  (+/- 1 pp) and Fig. 2(d) bandwidth reads (+/- 0.3 GHz) with W / L geometry.
- Not entered: DC / AC punch-through about -2 / -6 V (no parameter; CV in the uncached supplement); inductance 280 pH;
  transit-time limit 29 GHz and the Fig. 2(e) model map (40 GHz at 200 nm Ge, not fabricated); eye SNRs, 30 Gbps eyes;
  wire-bonded APD dark current 0.5 uA at gain 5 / 20 uA at gain 12 (bias not printed); receiver sensitivities -22.5 /
  -25 dBm (12.5 Gbps) and -16 dBm (25 Gbps), k ~ 0.05 fit; TIA noise / offset current; 1310 nm expectations.
- Fab `org_astar_ime` ("The Si-Ge APDs are fabricated at Institute of Microelectronics (IME), Singapore", p.5). No
  process name printed.

## Judgment calls for the auditor

1. huang2016b: responsivity 1.05 A/W, QE 84 % and QE 70 % set `author_estimate` because they are referenced past the
   grating coupler using its "estimated" -15 dB loss (supplement not cached); the Fig. 1(e) QE reads stay
   `extracted_from_figure` with the same note. Alternative: `measured` if the supplement shows a measured GC loss (wen2022
   / D517 precedent).
2. huang2016b: GC row given fab `org_astar_ime` (same die as the APDs named in the IME sentence); strict per-component
   reading (D515 / D463) would leave it empty.
3. huang2016b: 14 series rows built from figure reads only (rule 9 sibling rows by W x L); the 4 x 100 um bandwidth
   marker (3.3 GHz) is an outlier read as plotted. The 4 x 30 um row carries both the wire-bonded receiver die and the
   Fig. 2(d) series marker (same design, different die).
4. huang2016b: bandwidth / GBP rows set `wavelength_nm 1550` with `wavelength_inferred` (the pulse laser wavelength is
   not printed; testing "near 1550 nm" is stated for the device). GBP 276 / 300 GHz `derived` (12 x 23 / 12 x 25,
   xiang2022 D587).
5. campbell1988: split into two rows (Figs. 3 / 5 devices vs the 3 um AR-coated Fig. 4 device); the 3 um absorber is
   outside the printed 1.8-2.8 um wafer range (D417 note). Fab `org_bell_labs` borderline (D84b).
6. campbell1988: avalanche gain entered as the Fig. 3 top-marker read (~35 at ~62 V) instead of the printed "as high
   as 40" (no bias).
7. lenox1999: bias for the < 10 nA dark current and > 50 gain, and the 24 V breakdown row, come from Fig. 3 reads
   (rouvie2008 precedent for figure-read bias). Bandwidth / GBP rows 1550 nm `wavelength_inferred`.
8. franco2005: platform `other` for InP-based epi bonded to SI-GaAs (zhang2022e D664 bonded-APD precedent); `inp` would
   be the alternative. n_samples 10 only on breakdown and dark current (the ten-device sentence names the I-V data).
9. ye2015: "up to" responsivities entered with qualifier `le` per skill rule 7, although the printed value is the -10 V
   end point of the bias sweep; capacitance ~0.3 pF entered on both D60 and D2-D50 rows (inset shows both, "nearly the
   same"). Packaged-module responsivity kept on the chip row with `ref_plane module` (D437 practice).

## Missing fab / facility orgs

None needed for a row. (franco2005 author orgs Solid State Scientific Corporation, AFRL/SNHC, UMass Lowell Photonics
Center are not fab orgs here: no fabrication statement.)

## Registry gaps (skipped value + locator, proposed definition)

- `punch_through_voltage_v` (photodetector): franco2005 18.26 +/- 0.27 V mean (p.2 Sec. III); huang2016b DC ~-2 V / AC
  ~-6 V (p.2 Sec. 3A). Definition: bias at which the depletion reaches the absorber (DC or AC as stated in condition).
- `ionization_ratio_k` (photodetector, already a D436 candidate): lenox1999 k ~ 0.18 (p.1, p.2), huang2016b k ~ 0.05
  (p.4-5, sensitivity fit).
- `rx_sensitivity_dbm` (photodetector, already a D436 / D443 candidate): huang2016b -25 dBm at 12.5 Gbps, -16 dBm at
  25 Gbps (p.1, p.5); ye2015 BER 1e-12 at -9.9 dBm, 10 Gbit/s (p.3).
- `multiplied_dark_current_na` (photodetector): campbell1988 1.5-6 nA primary multiplied dark current at 90 % of
  breakdown (p.2; bias not printed).
- `inductance_ph` (photodetector): huang2016b 280 pH (p.3 Sec. 3B, circuit-model fit).
- `ideality_factor` (photodetector): ye2015 1.50-1.52 (p.2 Sec. IV.A).
- `center_wavelength_nm` widened to photodetector (resonant-cavity peak response): lenox1999 1.58 um (p.2 Sec. III).
