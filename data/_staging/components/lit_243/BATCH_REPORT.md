# lit_243 batch report

Papers: lit:nishi2017 (JSTQE 2017, invited QD laser paper), lit:tadokoro2009 (PTL 2009, 1.3 um InGaAlAs RWG DFB),
lit:oishi1997 (PTL 1997, 2.0 um InGaAs-InGaAsP BH DFB), lit:menna2002 (ECOC 2001, 1310 nm high-power FP / DFB). Page-1
titles match the source rows (tadokoro2009 title differs only in the degree-sign markup). None is a correction or
another paper. verified_on 2026-11-22. Dry run: +7 components, +45 metrics, 0 errors. All four are laser papers; no
EO-atlas overlap (host_device_ids empty).

## Components / metric rows

| component | class | platform | metrics |
|---|---|---|---|
| cmp_lit_menna2002_fp_rwg_3mm | laser.other | inp | 6 (chip 825 mW, ex-fiber 630 mW, divergence 30.2 / 13.4 deg, ~1310 nm, 3 mm) |
| cmp_lit_menna2002_dfb_3mm | laser.dfb | inp | 6 (chip > 450 mW, ex-fiber 315 mW, SMSR ~30 dB, 1309.1-1310.8 nm Fig. 3 read, kappa ~3.3 cm-1 design, 3 mm) |
| cmp_lit_tadokoro2009_rwg_dfb | laser.dfb | inp | 13 (Ith 8.4 mA, T0 72 K, > 5 mW to 105 C, SMSR > 35 dB, 4 lasing wavelengths 25-85 C, 3 fr figure reads, kappa ~100 cm-1, 200 um) |
| cmp_lit_oishi1997_dfb_bh_4qw | laser.dfb | inp | 10 (Ith 15-35 mA, 5 mW per facet, 2027 nm, SMSR ~30 dB, T0 ~45 K, 125 pm/K, divergence 32 / 37 deg, 600 um, 1.5 um stripe) |
| cmp_lit_nishi2017_fp_qd_mass | laser.other | gaas | 2 (> 10 mW RT-100 C, ~0.25 W/A) |
| cmp_lit_nishi2017_dfb_qd | laser.dfb | gaas | 6 (lasing peaks 25 / 100 / 125 / 150 C, 25 C threshold ~70 mA, 150 C max ~4.2 mW; all Fig. 9 reads) |
| cmp_lit_nishi2017_qd_13ch | laser.other | (empty) | 2 (~300 mW total, 13 channels) |

Per paper: menna2002 2 / 12, tadokoro2009 1 / 13, oishi1997 1 / 10, nishi2017 3 / 10.

## Values not entered and why

menna2002
- Fiber coupling efficiency 78 % (FP) and 63-68 % (DFB): property of a COTS aspheric lens pair (bulk optics, D411); the
  laser class has no coupling parameter. The ex-fiber powers carry the lens pair in `includes`.
- About 4 % coupling penalty of the COTS lens aperture (p.2): bulk-optics remark.
- About 0.4 nm longitudinal-mode broadening in the dashed current ranges of Fig. 2: no parameter. Resolution-limited
  half-widths: instrument limit, not a device value.
- Ridge width 3-5 um: a design range for single-mode operation; the measured device's width is not printed.
- Lifetime testing on T-cBN submounts is mentioned, no result printed.
- Optimization results for 1310 nm DFB lasers "will be presented at the conference": no values.
- Prior 315 mW record (ref. /1/), 1 W pump lasers (/2/), 440 mW 1550 nm DFB (/3/): cited (rule 3).

tadokoro2009
- Relaxation-oscillation slope (D factor) 3.3 / 2.5 / 2.1 GHz/mA^1/2 at 25 / 85 / 100 C (abstract, p.2, p.3): no
  parameter (registry gap, already a candidate list item).
- Linewidth enhancement (alpha) factor about 2.7 at 25 C and its Fig. 4 temperature dependence: no parameter (gap).
- Bragg-gain-peak detuning about -5 nm at 25 C (p.2) and the Fig. 4 detuning curve: no parameter.
- 25 Gb/s NRZ results: dynamic ER 6 dB at 2.2 Vpp, ER changes after 10 km (0.21 / 0.11 / 0.25 / -0.03 dB), error-free
  after 10 km SMF up to 85 C, maximum power penalty 2 dB: system-level, no parameters.
- Fig. 2 L-I powers at other temperatures (e.g. about 22 mW at 100 mA, 25 C): figure only, not cited by the text; not
  read.

oishi1997
- Current-tuning rate 0.004 nm/mA (abstract, p.2, p.3): static current tuning is not fm_efficiency_ghz_per_ma (D83g);
  no nm/mA laser parameter (gap).
- Facet AR reflectivity R = 10 %: no laser parameter (notes).
- Wide-ridge FP test lasers (Fig. 1, two- and four-well wafers, pulsed): only ln(Jth) vs 1/L plots, no printed device
  value; threshold current density has no parameter. F-P devices of the same wafer: "at the same range", no values.
- PL peak 1.995 um: wafer property (notes).
- Fig. 4 / Fig. 5 wavelength-current-temperature maps and mode hopping: the printed tuning rates cover them.

nishi2017
- Section II QD material data (density 5.9e10 cm-2, 20 nm / 7 nm dot size, PL widths 38 / 23.8 meV, gain 50-60 cm-1
  from ref. [17]): material / wafer properties, no component.
- FP threshold current density about 1000 A/cm2, DFB about 1500 A/cm2, 13-channel < 800 A/cm2: computed from
  dimensions the paper does not print; no parameter (gap: threshold current density).
- Lifetime > 300,000 h at 85 C, 10 mW APC, 50 % current-increase criterion (Fig. 8): no lifetime parameter (D81
  rejected); > 3 million FP lasers shipped: market fact.
- Fig. 10 high-temperature QD laser (CW lasing at 220 C, > 1 mW, 2 um mesa, 1200 um, HR/HR): the sentence presenting it
  cites ref. [20] (rule 3 / D259); not entered.
- Fig. 13 single-stripe laser 0.5 dB power decrease 25 -> 70 C at 20 mW: the sentence ("In the measurement ...")
  follows the ref. [25] interposer result and the sample is not identified; no parameter for power change over
  temperature either.
- T0 303 K (ref. [29]), 10.3 Gb/s DFB operation (ref. [19]), wafer-bonded > 100 C (ref. [26]), isolator-free I/O core
  (ref. [31]): cited.
- DFB 100 C threshold: the Fig. 9(a) 100 C trace is hidden under the 125 C trace near onset (not read).
- DFB thermal drift from the four Fig. 9(b) peaks (~95 pm/K) not computed (figure-read arithmetic).

## Missing fab / facility orgs

- Princeton Lightwave Inc. (menna2002 p.1 affiliation line; two authors "contractor from Sarnoff Corporation"): fab,
  borderline, for cmp_lit_menna2002_dfb_3mm only. Basis: "These results encouraged us to apply the same active region
  design to fabrication of long-cavity high-power DFB lasers" (p.2 Characterization Results); all authors list Princeton
  Lightwave Inc. The FP device sentences are passive ("are fabricated", p.1), so the FP row stays empty. Not in
  organizations.csv / org_aliases.csv (only org_princeton_photonics_suzhou, unrelated). Fab left empty pending the org.
- QD Laser, Inc. (nishi2017 p.1 affiliation footnote): not in the registry; no fabrication statement names it (passive
  "mass-productive QD lasers were fabricated", p.6), so no fab role; listed for the org round only.
- Alias requests for existing org_ntt: "NTT Photonics Laboratories" (tadokoro2009 p.1 footnote; also proposed in D695)
  and "NTT Opto-electronics Laboratories" (oishi1997 p.1 footnote).
- No facility statements in any of the four papers (nishi2017 MEXT project funding is a grant, D80c).

## Judgment calls (for the auditor)

(a) tadokoro2009 fab org_ntt borderline: the only first-person process sentence is about controlling the doping profile
    during crystal growth (p.1 Sec. II); all authors NTT; staff thanked for epitaxy and processing without an org.
    Follows luo2015 (D704). Alternative: empty (D80b strict).
(b) oishi1997 fab org_ntt: "We have fabricated DFB BH lasers" (p.1) plus one-org authorship (D72).
(c) menna2002 fab empty on both rows; Princeton Lightwave Inc. reported as a missing org with a borderline fab role on
    the DFB row only (first-person "apply ... to fabrication").
(d) menna2002 DFB: one design row for the two Fig. 2 devices (same design, rule 9); > 450 mW and 315 mW ex-fiber are
    device (1) by the Fig. 2 curves / label. kappa_per_cm 3.3 approx `author_estimate` from the printed design target
    kappaL ~ 1 with L = 3 mm (D82a); drop it if design kappaL arithmetic is not wanted.
(e) menna2002 FP center wavelength 1310 nm approx `measured` from the printed Fig. 1 label (barbarin2006 precedent);
    DFB wavelength range 1309.1-1310.8 nm is a Fig. 3 read (`extracted_from_figure`), not the title's 1310 nm.
(f) menna2002 output temperatures: FP rows 291.15 K from the Fig. 1 label Tc = 18 C (text says heatsink 18-20 C); DFB
    rows 293.15 K (Fig. 2 / Fig. 3 / abstract 20 C).
(g) tadokoro2009 "> 5 mW up to 105 C" entered at 378.15 K with ref_plane unspecified (the paper does not name the
    facet / plane); SMSR > 35 dB with the -20 to 100 C span and Ith + 5 mA bias in condition (no temperature_k).
(h) tadokoro2009 three relaxation-oscillation figure reads (highest plotted point per temperature, Fig. 3) added so the
    fr data have a home while the D factor has no parameter; the 25 C slope 3.3 GHz/mA^1/2 itself is not entered.
(i) oishi1997 threshold 15-35 mA one `range` row (typical spread, with the abstract's 15 mA / 600 um in condition);
    length 600 um `design_target` although the abstract ties it only to the 15 mA devices (noted on the row and
    component). Center wavelength 2027 nm `derived` from the printed 2.027 um; the Fig. 2 render peak reads ~2027.7 nm
    (noted, printed value kept). 0.125 nm/K -> 125 pm/K `derived`.
(j) nishi2017 Fig. 7 FP and Fig. 9 DFB values entered as this paper's own (D80i: neither the figures nor the value
    sentences carry a citation; the paragraphs cite refs. [18] / [19] for earlier work), while Fig. 10 (sentence cites
    ref. [20]) and Fig. 13 (follows ref. [25]) are left out. Fig. 9 wavelength / threshold / power reads are figure-only
    values (the text gives only "single mode up to 150 C" and "lowest threshold near 100 C").
(k) nishi2017 0.25 mW/mA -> 0.25 W/A `derived` (unit form change, D256); 13-channel 300 mW read as the total of all
    channels (Fig. 12 "20 mW/channel" line at about 260 mW confirms total power); 13-channel platform left empty
    (substrate not stated for that device, D422), FP / DFB rows `gaas` ("QD lasers on GaAs substrates", p.3; Fig. 9
    caption "on GaAs").
(l) Laser class choices: FP lasers `laser.other` (luo2015 precedent), DFBs `laser.dfb`.

## Registry gaps (skipped value + locator + proposed definition)

- `d_factor_ghz_per_sqrt_ma` (laser): relaxation-oscillation frequency slope vs sqrt(I - Ith). tadokoro2009 3.3 / 2.5 /
  2.1 GHz/mA^1/2 at 25 / 85 / 100 C (p.1 Abstract, p.2 Sec. II, p.3 Sec. IV). Also listed earlier as "D-factor / MCEF".
- `alpha_factor` (laser): linewidth enhancement factor as measured (method in notes). tadokoro2009 ~2.7 at 25 C (p.2
  Sec. III, Fig. 4).
- `current_tuning_nm_per_ma` (laser): static wavelength shift per mA of injection current. oishi1997 0.004 nm/mA (p.1
  Abstract, p.2-3 Sec. III).
- `threshold_current_density_a_per_cm2` (laser): nishi2017 ~1000 (FP, p.3), ~1500 (DFB, p.4), < 800 (13-channel, p.5)
  A/cm2; all computed from unprinted dimensions, so they would be author_estimate. Existing candidate.
- `detuning_nm` (laser): Bragg-wavelength minus gain-peak detuning. tadokoro2009 ~-5 nm at 25 C (p.2).
- `max_operating_temperature_k` (laser): nishi2017 DFB single-mode lasing at 150 C (p.4); tadokoro2009 > 5 mW up to
  105 C. Existing candidate.
- `facet_reflectivity_pct` (laser): oishi1997 AR R = 10 % (p.2).
