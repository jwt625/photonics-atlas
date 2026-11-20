# lit_219 batch report

Distilled 2026-11-20 under the pic-component-distill skill (Contracts v4-v7, DevLog-007 rulings through D672).
Papers: duan2012, ye2014, li2015, hayashi1998, nakata2002. Page-1 titles match the source rows; no correction or
erratum; no `garbled_text_layer`. Figure values read from the page renders.

Totals: 16 components, 88 metric rows. `merge_component_staging.py data/_staging/components/lit_219 --dry-run`:
+16 components, +88 metrics, 0 errors.

| paper | components | metrics |
|---|---|---|
| duan2012 | 2 | 20 |
| ye2014 | 9 | 28 |
| li2015 | 3 | 20 |
| hayashi1998 | 1 | 8 |
| nakata2002 | 1 | 12 |

## duan2012 (Opt. Express 2012, Ge/Si SACM APD, 310 GHz GBP)

Components: `apd_d30` (photodetector.apd, normal incidence, 30 um Ge mesa), `pin_d30` (photodetector.vertical,
reference p-i-i-n on the same wafer, test_structure).

Entered: 12 A/W near breakdown, gain ~40 and ~30 (gain from normalization to the 0.3 A/W reference: derived),
~5 uA dark current at gain ~30, Vb ~-29.4 V (100 uA criterion), 8 GHz max bandwidth (gains 30-39), four Fig. 5
bandwidth-vs-gain points (extracted_from_figure), GBP 310 GHz, ~80 fF / ~60 ohm (both rows), absorber diameter and
TEM thickness 1.03 um; reference p-i-i-n 0.3 A/W and ~12 GHz.

Not entered: punch-through ~-28 V (no parameter); simulated field profile (Fig. 3); calculated RC 16.5 GHz,
transit 18.6 GHz and total 13 GHz of the p-i-i-n (rest on saturation velocities cited to ref. [18], rule 3); predicted
primary responsivity (calculation); projected ~10 GHz with thinner Si; Si multiplication layer 703 nm and top Si 213 nm
(no parameter; in core_material).

Judgment calls:
- Fab empty: "we report a Ge/Si APD fabricated using the SEG approach" (p.2) plus a passive process description; no
  fabricator named. All authors A*STAR IME (org_astar_ime exists) - not enough under D80b.
- Platform `other` (kang2008 vertical Ge/Si APD precedent); the device is on 220 nm SOI but light is not guided.
- Bias of the 12 A/W / gain-40 point (-29 V) and of the gain-30 / 5 uA point (-28.4 V) read off Fig. 2(b).
- GBP 310 GHz kept `measured` as printed (8 x 39 = 312; gundlapalli2022 / D671 precedent).

## ye2014 (JLT 2015 invited, InP components at 2 um)

Components: `dm_laser_600um` (laser.other), `wg_pd_3x300` (photodetector.other, D152), `sn_pd_hs` and `sn_pd_d50`
(photodetector.vertical), `dilute_wg` (waveguide_platform.straight), `lensed_fiber_facet` (fiber_chip_coupler.edge),
`mmi_1x4` (splitter.mmi), `hybrid_32x1644` (splitter.hybrid_90), `awg_10ch` (wdm.awg). All platform `inp`, fab empty
(no fabrication statement naming an org; authors at Tyndall and Eblana Photonics).

Entered: laser S21 >6 GHz at 70 mA (10-40 C), 600 um; waveguide PD 0.3 A/W TE fiber-referred at 2 um, 120 nA at
-3 V; surface-normal PD 0.94 A/W, ~6 GHz at -7 V; 50 um device 2 uA / 0.1 A/cm2 at -5 V, <0.3 pF; waveguide <5 dB/cm
at ~1.55 um; lensed-fiber coupling <0.9 dB; 1x4 MMI excess loss 1.54 dB; 90-degree hybrid excess loss 2.2 dB
(incl. MZI), phase error ~10 deg, 32 x 1644 um, 8 um pitch; AWG 4.50 dB mean excess loss per channel, 100 GHz,
108 pm/K, 10 channels, 1 mm min bend radius.

Not entered:
- Waveguide PD bandwidth ">10 GHz [22]" (cited, rule 3); laser 10 Gb/s transmission [18] (cited).
- QCSE MZM (pi phase shift estimated at -4 V for 2 mm, 9 GHz EO bandwidth, 10 Gb/s with ref. [26] "manuscript under
  preparation"): EO-atlas domain (rule 2), listed as an EO-atlas candidate; Fig. 8 photocurrent spectra qualitative.
- Mode size 3.0 x 3.6 um and birefringence <1e-3 (origin and axis not stated); loss at 2 um "similar" (no number).
- Hybrid CMRR >15.6 dB (no parameter; CMRR deferred in D81); FSR 512 GHz (6.82 nm) of the self-referencing MZI delay
  line (test structure); simulated optimum length 1629 um (in notes).
- 20-channel AWG (no values); AWG chip size 11 x 7.7 mm (not tied to the 10- or 20-channel design).
- Discrete-mode laser spectra 1.8-2.1 um (Fig. 1; several unnamed devices).

Judgment calls:
- D259 / D408: the Fig. 2 caption cites the authors' ref. [18] (dynamic characteristics of the same 2 um DM lasers,
  2014) for the eye-diagram inset; the ">6 GHz" S21 sentence has no citation and is kept (D80i). The auditor may rule
  the S21 curves are reproduced from [18]. Similarly, the waveguide PD 0.3 A/W / 120 nA (Fig. 3) has no citation
  while its bandwidth is cited to [22] (the authors' 2013 letter on a packaged 2 um QW PD).
- Waveguide PD: which epitaxy (4-QW or 2-QW) the Fig. 3 device used is not stated; one row by geometry.
- Surface-normal PD split into the "high speed photodiode" (diameter not stated: responsivity, bandwidth) and the 50 um
  device (leakage, density, capacitance) per D159; they may be the same chip. The <0.3 pF capacitance is attached to
  the 50 um row by sentence position.
- 1x4 MMI 1.54 dB `author_estimate`: "was obtained by optimizing the structural dimensions" does not say simulated or
  measured (D76).
- Hybrid excess loss scope `device_total` (includes the MZI test structure); wavelengths of hybrid and AWG rows from
  the figure axes (wavelength_inferred).
- AWG "4.50 dB +/- 0.87 dB" stored as `mean`, n_samples 10, spread type in notes.

## li2015 (PTL 2015, all-Si microring avalanche PD, 40 Gb/s)

Components: `mrr_apd` (photodetector.apd, soi_rib; wang2026h precedent), `mrr_ring` (resonator.ring cross-row of the
same ring, D396), `gc_packaged` (fiber_chip_coupler.grating, soi). Fab org_semiconductor_manufacturing_international on
all three ("fabricated in the standard 0.18 um-CMOS foundry at ... SMIC", p.1), process_name "standard 0.18 um CMOS".

Entered: 48 mA/W at -8 V on resonance (on_chip, derived: unit conversion and bus power from the authors' halving of
the 18 dB fiber-to-fiber loss), avalanche gain 8.7 (relative to -7 V, derived), Vb 8.4 V (Miller fit, derived),
OE bandwidths 22.8 / 20.5 / 10 GHz at -7.9 / -8 / -8.1 V, Cj 40.5 / 30 fF at -1 / -5 V and Rj 32 ohm (S11 fit,
measured), ring geometry; ring ER ~16 dB at 1550.59 nm; GC pair ~18 dB fiber-to-fiber and ~9 dB per side.

Not entered: waveguide loss 16.7 dB/cm (ref. [16], rule 3); electrical bandwidth ~37 / ~49 GHz (estimated with the
[16] model); linear absorption coefficient 0.158 dB/cm (no parameter; assumed overlap and collection efficiency);
ring fit kappa / A / t; Cp, Co, Ro of the equivalent circuit (notes); dark current (only a photocurrent ratio ~8 and a
4.81 uA peak photocurrent printed); 20-40 Gb/s eye diagrams (no data-rate parameter); zigzag period 600 nm (period_nm
not allowed for photodetector; in core_material).

Judgment calls: Rj entered as `series_resistance_ohm` (the paper calls it "resistance of the junction" in the
equivalent circuit); bandwidth rows carry no wavelength (near resonance, not printed); GC wavelength C band inferred.

## hayashi1998 (PTL 1998, microlens-integrated SL-APD, NEC)

Component: `sl_apd_lens` (photodetector.apd, inp). Fab org_nec ("the ... SL-APD we fabricated", p.2; all authors
NEC Corporation).

Entered: QE 64 % at 1.5 um, Vb 39 V (10 mA criterion), dark current 49 nA at M = 10 and 100 nA at M = 20 (Fig. 3
labels; biases about -37.0 / -37.4 V read off Fig. 3), max bandwidth 8.5 GHz, GBP 75 GHz, 100 um junction diameter,
1 um absorber.

Not entered: multiplied dark current 5 nA "estimated" up to gain >50 (no parameter for the multiplied component);
uniform 200 um diameter detecting area (Fig. 4(a); registry gap below); dark currents 7.4 nA at -40 C and 890 nA at
+120 C at 0.95 VB (bias per temperature not printed, rouvie2008 precedent); Vb temperature coefficient 5.9e-4 K-1 (no
parameter); microlens geometry (designed 220 um radius; geometry only, no lens row); Fig. 1 multiplied dark current
density (0.64 / 17 pA/um2) and GB product vs SL thickness (sample set whose 0.23 um devices are the authors' earlier
work [3]-[5]; D159 / D259).

Judgment call: Fig. 3 is called "typical": rows from it carry `statistic: typical`.

## nakata2002 (ECOC 2001, 40-Gb/s waveguide APD, NEC)

Component: `wg_apd_6x5` (photodetector.apd, inp). Fab org_nec ("We fabricated well-defined small mesa APD", abstract;
all authors NEC Corporation).

Entered: Vb 16 V, external QE 43 % at 1.54 um (hemispherical-ended fiber), 90 fF incl. parasitics, 25 ohm parasitic
resistance, fmax 30 GHz (50 ohm), GBP 180 GHz, APD + GaAs HBT preamplifier front-end bandwidths 30 / 28 / 19 GHz at
M = 2 / 3 / 5 (condition says front end), 6 x 5 um mesa, 0.5 um absorber.

Not entered: preamplifier 43 dBOhm and >40 GHz (cited to [8]; electronics); Fig. 3 bandwidth-vs-M points (poor scan);
Fig. 4 second device (~45 um2) and the previous design [7]; Fig. 2 currents (not printed).

Judgment calls: GBP 180 GHz "which was also previously reported [7]" kept as this device's Fig. 3 result (D80i), flagged;
front-end bandwidths kept on the APD row (same physical APD; rule 9) with the configuration in the condition.

## Missing fab / facility orgs

None. org_nec, org_semiconductor_manufacturing_international exist; A*STAR IME (org_astar_ime) and Tyndall
(org_tyndall_national_institute) exist but are not fab orgs here (no fabrication statement). Eblana Photonics (ye2014
p.1 affiliation) has no registry row; not needed as a fab org (no statement).

## Registry gaps

- Detecting-area / aperture diameter for surface-illuminated detectors (hayashi1998 p.3 Fig. 4(a): ~200 um uniform
  response diameter at M = 10). Proposed `aperture_diameter_um` (also a D433 candidate): diameter of the optically
  sensitive area as measured or stated, definition in condition.
- Multiplied (gain-normalized) dark current of APDs (hayashi1998 5 nA, p.3; rouvie2008 precedent). Proposed
  `multiplied_dark_current_na`: primary dark current that is multiplied, gain range in condition.
- Breakdown-voltage temperature coefficient (hayashi1998 5.9e-4 K-1, p.3; rouvie2008 8.7e-4 K-1). Proposed
  `breakdown_tempco_per_k`: (dVB/dT)/VB.
- Common-mode rejection ratio of a 90-degree hybrid (ye2014 >15.6 dB, p.3-4; CMRR deferred in D81).
- period_nm for photodetector (li2015 zigzag PN junction period 600 nm, p.2).
- data_rate_gbps (li2015 40 Gb/s eye diagrams; already listed in D534).

## EO-atlas candidate

ye2014 QCSE strain-balanced MQW MZM at 2 um (p.4-5): pi phase shift estimated at -4 V for 2 mm, 9 GHz small-signal EO
bandwidth (Fig. 9), 10 Gb/s back-to-back (ref. [26], forthcoming).
