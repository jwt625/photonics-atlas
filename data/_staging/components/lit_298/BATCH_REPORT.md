# lit_298 batch report

Distilled 2026-11-27. Papers: lit:fan2017, lit:hamrouni2024, lit:kim2005 (Optics Express open-access versions). Result: 3
component rows, 10 metric rows; `merge_component_staging.py --dry-run`: +3 components, +10 metrics, 0 errors (the two
warnings printed concern merged rows of other sources). Page-1 titles match the source rows; none of the cached files is
a correction / erratum or another paper. No text layer was garbled.

## lit:fan2017 (fiber-laser pumped femtosecond OPG, Tianjin University / ECNU)

Components: 0. Metric rows: 0.

The only nonlinear element is a bulk 25 x 8.5 x 1 mm 5 % MgO:PPLN crystal in an oven with seven poling gratings, pumped
in free space through lenses (p.6 Sec. 3, Fig. 3): out of scope (D411; kourogi1993 / zhang2025e bulk-crystal precedents).
Values not entered and why:
- OPG signal tuning 1420-1560 nm, 2.1 W at 1474 nm, ~36 % pump-to-signal conversion, 350 fs signal pulses, 29.5 / 30 um
  poling periods (p.6-7, Fig. 4): bulk crystal, D411.
- RMS RIN 43.02 % / 1.95 % (10 Hz-5 MHz) below / above saturation, 7.37 % / 0.37 % with CW seeding, timing jitter 9.3 fs
  and up to 50 fs (p.8-9, Figs. 6-7): system output of the bulk OPG, D411.
- Simulated RIN / timing-jitter spectra (Fig. 1): bulk OPG model, D411.
- Yb-fiber oscillator / amplifier pump (53 MHz, 6 W, 100 fs, 34 nm FWHM): fiber laser, out (D80f); PPKTP cross-correlator,
  dichroic mirrors, PBS / HWP: bulk optics or setup equipment (rule 13).
- 30 mW CW seed laser diode at 1470 nm, 0.044 nm FWHM (p.9): seed source of the setup, not a device under test (rule 13).
Missing orgs: none (no fabrication or facility statement).

## lit:hamrouni2024 (TFLN-on-sapphire supercontinuum, Neuchatel / Stanford / NTT Research)

Components: 1. Metric rows: 5.
- `cmp_lit_hamrouni2024_facet_objective` (fiber_chip_coupler.edge, lnos_rib): coupling efficiency ~1.5 % including the
  reflective-objective transmission and ~10 % beam-to-mode overlap excluding it (both author_estimate, p.3-4); waveguide
  cross-section at the facet: 1520 nm top width, 931 nm film, 608 nm etch (design_target, p.3 Fig. 1(a)).

Values not entered and why:
- The PP-TFLN waveguide itself (frequency_converter.shg; 5 mm, nominal poling period 6.30 um, 27 pairs spanning
  6.30 +/- 0.135 um in 10 nm steps): no registry performance value is printed (no conversion efficiency, no propagation
  loss), so a geometry-only row is not entered (rule 9); its geometry sits on the facet row and its poling period / length
  in the component notes.
- Supercontinuum 360-2660 nm at 45 pJ within -55 dB, harmonic onsets at 2 / 7 / 12 pJ, harmonic merging 20-25 pJ, FH-SH
  overlap above 22 pJ, f-2f beatnote 25 dB below f_rep and 13 dB SNR (p.4-7): no registry parameter (gaps below).
- Simulated GVM 6 fs/mm, GVD 20 fs2/mm and < 5 fs2/mm (p.3, Fig. 1(b)) and the 7.5 fs/mm GVM deduced from the 27 THz SH
  spectral zero spacing (p.4): dispersion has no parameter (D81 / D250 rejected).
- Output collection efficiency ~35 % (p.4): cited from ref. [30], rule 3.
- Fabrication yield "close to 100%" (p.3): no parameter (yield_pct is a candidate, D706 owner list).
- Driving OPO (2090 nm, 130 nm FWHM, ~40 fs estimated, 300 mW, 100 MHz), reflective objectives, APD, OSAs: setup
  equipment (rule 13).
Fab / facility: fab empty ("We fabricate", p.3, with authors at three unrelated orgs; white2022 / su2017 precedent).
Facilities `org_stanford_nanofabrication_facility`, `org_stanford_nano_shared_facilities` ("Fabrication was performed at",
p.7 Acknowledgments). NTT Research thanked for financial and technical support: not a facility (D80c).
Missing orgs: "Cell Sciences Imaging Facility" (facility; p.7 Acknowledgments, named in the same "Fabrication was performed
at" sentence; Stanford unit). Not in `organizations.csv` / `org_aliases.csv`.

## lit:kim2005 (all-semiconductor X-CPA MOPA, CREOL / University of Central Florida)

Components: 2. Metric rows: 5.
- `cmp_lit_kim2005_rwg_soa_preamp` (amplifier.soa): 16 mW delivered to the tapered-amplifier input at 150 mA, entered as
  12.04 dBm (derived), length 1 mm (derived).
- `cmp_lit_kim2005_tapered_amp_3mm` (amplifier.soa): 1 W maximum average output (30 dBm, derived) at 2.5 A with 16 mW input,
  gain 17.96 dB (derived from the two printed powers), length 3 mm (derived).

Values not entered and why:
- Colliding-pulse hybrid mode-locked laser (600 fs after an external bulk dual-grating compressor, 0.92 ps
  autocorrelation, 45 / ~38 ps chirped pulses from the oscillator, ~285 MHz, > 20 pJ / 39 pJ, 974 nm, 971-977 nm): a
  bench-top free-space cavity with HR, OC, slit and a discrete MQW absorber (Fig. 2(a)); out of scope (D706 resan2005 /
  kim2004, D411 / D642).
- 1 mm inverse-bowtie SOA (IBTSOA; 10 um facet to ~20 um center, 6 deg stripe, 215 mA DC + 285 MHz RF in the cavity,
  pulse picker at 95 MHz): no value of the SOA by itself (rule 9, D706).
- MQW saturable absorber (75 x 8.5 nm In0.18Ga0.82As / 10 nm Al0.35Ga0.65As, excitonic peak 970 nm): part of the bench
  laser; transmission spectrum only.
- Chirped fiber Bragg grating (~1600 ps/nm, 6 nm band at 974 nm, ~0.96 m, PS1060 fiber, 3M): dispersion has no parameter
  and the 6 nm band has no stated level (D82g; D706 kept the same group's CFBG out).
- 56 % coupling of the TA beam into single-mode fiber (p.6): bulk beam-shaping optics (aspheric, cylindrical, 40X
  objective), not a chip coupler; 194 mW after compression, 2.0 nJ, 0.59 ps, 1.4 kW peak, ~16,000x recompression
  (p.6-7): system outputs.
- Preamplifier gain: the ~1.3 mW input is measured after the fiber stretcher and the 16 mW after an isolator and filter,
  so a gain would mix coupling losses; only the output power is entered.
- TA 10.5 nJ per stretched pulse (p.6) and the 238 nJ / 13000x gain of ref. [10] (the authors' LEOS 2004 paper, rule 3 /
  D259): pulse energy has no parameter; ref. [10] values are cited work in any case.

Judgment calls:
1. TA and preamplifier rows: D706 kept kim2004 at 0 rows because no SOA value by itself was printed; this paper prints the
   TA output for a stated input and drive, and the power the preamplifier delivers, so both chips become rows.
2. TA gain 17.96 dB is batch arithmetic (D166, cheung2015 precedent); the 1 W includes an unquantified ASE share ("most"
   of it is signal, p.6), noted in the condition.
3. Preamplifier output plane: the 16 mW is the TA input after an isolator and band-pass filter (Fig. 4), so ref_plane
   `unspecified` with that in the condition.
4. Wavelength 974 nm on the amplifier rows is the oscillator center wavelength (p.5), `wavelength_inferred: true`.
5. Platform empty on both amplifier rows: RWGSOA printed as "InGaAs/AlGaAs" with no substrate, TA material not stated
   (D422 / D423).
6. hamrouni2024 coupling 1.5 % `author_estimate` (not D167 measured): p.4 presents it as the product of two approximate
   terms of unstated origin (D418).

Fab / facility: fab empty on both kim2005 rows. Missing orgs: "Sarnoff" (p.7 Acknowledgments, "for providing IBTSOA and
RWGSOA": fab of `cmp_lit_kim2005_rwg_soa_preamp` per rule 12; already listed in D706 as "Sarnoff Corp."). Supplier-only
(no row): "3M" (CFBG) and "Naval Research Laboratory" (MQW SA), p.7 Acknowledgments.

## Registry gaps (skipped value + locator + proposed definition)

1. `pulse_energy_nj` on amplifier / laser (recurring, D706 Q6): kim2005 TA 10.5 nJ per 9.6 ns stretched pulse (p.6), CPMLL
   39 pJ (p.5); "output pulse energy at the stated repetition rate and reference plane".
2. Supercontinuum / spectral span on frequency_converter: hamrouni2024 360-2660 nm at 45 pJ, -55 dB level (p.5);
   "full span of the generated spectrum at the stated level and pump energy" (comb span was deferred, D418).
3. Pump pulse energy for an onset / threshold on frequency_converter: hamrouni2024 FH-SH overlap > 22 pJ, harmonic onsets
   2 / 7 / 12 pJ on chip (p.2, p.5); "on-chip pulse energy at which the stated process sets in (criterion in condition)".
4. Group-velocity mismatch / dispersion (D81 / D250 rejected, recurring): hamrouni2024 7.5 fs/mm GVM from the SH spectrum
   (p.4), simulated 6 fs/mm and GVD 20 fs2/mm (p.3); kim2005 CFBG ~1600 ps/nm (p.4).
5. `yield_pct` (candidate, D706 owner list): hamrouni2024 waveguide fabrication yield close to 100 % (p.3).
