# lit_54 distill report (2026-10-30)

Classes: phase_shifter, photodetector, waveguide_platform. Papers: pfeifle2012 pernice2012 chen2018a fang2008 mauthe2020
schuck2013 kang2008a. All seven cached texts match their `lit:` source rows (page-1 title / authors); none is a
correction / erratum or flagged `garbled_text_layer`. All are `restricted_local_only`: facts and locators only.
Generator: session scratchpad `lit_54/gen.py`.

Dry-run: `batch lit_54: +33 components, +216 metrics; errors 0` (only the pre-existing WARN on cmp_lit_ni2025b_pimmwc-m18).

| paper | components | metrics |
|---|---|---|
| pfeifle2012 | 0 | 0 |
| pernice2012 | 13 | 81 |
| chen2018a | 2 | 15 |
| fang2008 | 6 | 47 |
| mauthe2020 | 3 | 17 |
| schuck2013 | 7 | 43 |
| kang2008a | 2 | 13 |
| total | 33 | 216 |

## pfeifle2012 (0 rows; EO-atlas candidate)

Silicon-organic hybrid liquid-crystal-clad strip-loaded slot phase shifter (KIT). Per the coordinator and skill rule 2 the
device metrics belong to the EO atlas (it already holds orientational LC-cladding rows, e.g. taghavi2024). Nothing else in
the paper carries a stated number: grating couplers and strip-to-slot converters have no values. Values for the EO atlas,
with locators:
- Large signal (100 Hz sawtooth, +/-5 V, no bias): 35 pi at 5 V for L = 1.7 mm (21 pi/mm, UpiL 0.24 V mm); peak slope
  20 pi/V near 1.3 V, which gives UpiL 0.085 V mm (p.11, Fig. 6(b)).
- Small signal (1 V sawtooth on a DC bias, Table 1 p.12): 3.9 / 8.0 / 12.7 pi/V, UpiL 0.44 / 0.21 / 0.13 V mm at
  9 / 8 / 7 V bias. Below 7 V bias the device degraded permanently (ion adsorption, p.13).
- Excess loss below 4.5 dB for 35 pi, FOM about 68 pi (p.13). Slot-waveguide propagation loss above 17 dB/mm (imperfect
  fabrication: slot etched 1 um into the BOX, electrode gap 2 um instead of 4 um) plus 16 dB/mm added by the LC (p.13).
- Resistance 1.7 GOhm / 280 MOhm / 3 MOhm at 1 / 5 / 10 V; about 1 nW at 1.3 V (p.13).
- Geometry: h 220 nm, rail width 240 nm, slot about 120 nm, slab 60 nm (1e17 cm-3 As), 2 um BOX, 193 nm DUV (p.9).
- Fab: passive voice ("were produced"), all authors at KIT (no fab org). KNMF appears only in the support / funding list
  (p.18).

## pernice2012 (13 components / 81 metrics)

Rows: travelling-wave NbN SSPDs I-IV (Table 1: OCDE, dark count rate at 99 % Ic, system efficiency) plus geometry; the
meander comparison detector V (3 % OCDE); two 100 nm detectors of the Fig. 3 pulse-length series (L = 10 / 40 um,
decay time as recovery_time_ns); the NbN-covered waveguide (measured 0.98 dB/um and simulated 1 dB/um as
prop_loss_db_per_cm, ding2019 precedent); the 750 x 110 nm Si waveguide (4.3 dB/cm, group index 3.58 measured / 3.6
simulated); two 5.8 mm meander rings (gap 100 / 200 nm: spectral Q 14,000 / about 24,000 and the authors' time-domain Q
11,900 / 22,900 and 67 pm as derived); the focusing GC (13.1 dB peak, 16.4 dB band average); the 50/50 splitter
(imbalance <= 0.2 dB). Jitter 18.4 ps on device III. Fab org_yale_university (author contributions p.10).

Not entered: best / system NEP (no parameter); critical current 28.2 uA "for typical 100-nm wide devices" (D254 family
value, notes on III / IV); > 97 % absorption of a 20 um detector (no parameter); kinetic inductance 0.91 nH/um; pulse
FWHM 505 / 1226 ps; PicoHarp jitter 50 / 46 ps (instrument-dominated); ring-down detector at 86 % Ic, about 15 %
efficiency, < 1 Hz (detector geometry not stated, D159); round-trip delay 72.7 ps.

## schuck2013 (7 components / 43 metrics)

Five NbTiN-on-Si3N4 SSPD nanowire designs (60/25, 60/40, 75/40, 75/25, 90/25 nm/um; Table 1 DEoc at 768 and 1542 nm)
with nanowire geometry; on the 75 nm / 40 um row the dark count rates (100 / 2 mHz mounted, 50 / 1 mHz unmounted,
7.7 Hz daylight, 1.6 K; mHz values converted, derived), critical currents 18 uA (dark-count device) and 16 uA (jitter
device), jitter 48.4 / 51.5 ps FWHM, decay time 1.2 ns. Two SiN grating couplers (about 11 dB at 1542 nm, 13 dB at
768 nm, typical, per_coupler). Fab org_yale_university (C.S. fabricated, p.6).

Not entered: Table 1 attenuation per um and atot (simulation vs measurement not stated), NEPmin, DEoc/(Rdc dt); Ic range
13-20 uA (family statement); rise constant 223 ps, kinetic inductance 0.75 nH/um, return current 3.8 uA; waveguide
width (600 nm visible / 1 um telecom: two values for one row).

## chen2018a (2 components / 15 metrics)

Transfer-printed GaAs MSM PDs: 70 x 70 um2 normal-incidence (photodetector.vertical, platform other: printed on
high-resistivity Si) and 30 x 30 um2 on a SiN grating coupler (photodetector.iii_v_on_platform, sin). Averages over the
nine finger designs (n 9): dark current 22 / 7.2 nA at 2 V, responsivity 0.117 A/W (fiber) / 0.1 A/W (waveguide,
author_estimate: how the waveguide power was obtained is not described), QE 17.2 % (derived as printed; recomputation
17.1 %), bandwidth about 20 GHz (para-1, large PD), simulated capacitance < 90 / < 30 fF; absorber 500 nm GaAs,
active-area dimensions. Fab empty (authors at HUST and Ghent University - imec, D154).

Not entered: SiN GC period 718 nm / fill factor 52 % / 300 nm etch (no photodetector parameter, no GC performance =>
no GC row); eyes / BER.

## fang2008 (6 components / 47 metrics)

Poly-Si strip waveguides 700 / 500 / 300 x 250 nm with SiON cladding (wafer C): TE 6.45 / 7.24 / 7.81 and TM 7.11 / 7.32
/ 7.5 dB/cm at 1550 nm (Fig. 4 labels, cut-back), plus the 700 nm C-band rows (6.45 +/- 0.3 TE, 7.11 +/- 0.5 TM);
SiON spot-size converters per width: TE 3.4 / 3.6 / 3.7 and TM 6.7 / 7.2 / 7.8 dB/facet (cut-back intercept, measured,
D167), with tip 150 nm, coupling length 200 um, 6 x 6 um SiON. Platform `other` (poly-Si, no enum value). Fab
org_astar_ime (borderline: "we fabricated", all authors IME, one also Jilin University; D84a / huang2014).

Not entered: simulated 2 dB/facet and <= 0.2 dB (stated for the coupler design, not a width; D254); pair loss 6.8 +/-
0.2 dB (two facets); Fig. 5 scattering-loss simulation and Fig. 6 anneal / height curves (plot-only); roughness 0.46 /
0.4 nm (no parameter).

## mauthe2020 (3 components / 17 metrics)

Monolithic TASE-grown InGaAs lateral p-i-n nanostructure PDs on SOI, 60 / 200 / 500 nm wide (photodetector.
iii_v_on_platform, platform iii_v_on_si_epi): dark current 1.7 / 15 / 36 nA at -2 V; 200 nm device 3-dB bandwidth > 25
GHz at -1.5 V (beyond the about 25-30 GHz measurement capability); geometry (60 nm thick, about 1 um long, widths,
2 um BOX, about 0.06 um2 footprint on the 60 nm row). Fab org_ibm_research_zurich (S.M. designed and fabricated, p.7;
printed as IBM Research Europe, Rueschlikon).

Not entered: responsivity 0.68 A/W / QE 62 % at 1346 nm (device width not stated, D159; incident power estimated);
capacitance < 0.1 fF (general estimate); Fig. 6(a) 60 / 500 nm curves (bias not stated); LED EL (no values).

## kang2008a (2 components / 13 metrics)

30 um Ge/Si SACM APD (photodetector.apd, platform other): GBP 340 GHz (best of 4) and > 300 GHz (all), 3-dB bandwidth
11.5 GHz max (gain <= 20, 1300 nm), 5.88 A/W at punch-through (about -22 V, 1310 nm), 77 fF, breakdown -25 V (10 uA
criterion), dark current density < 19 uA/cm2 (-> 0.019 mA/cm2, derived) up to -5 V and 175 mA/cm2 at 90 % Vbd with gain
8 (bias -22.5 V computed from the printed Vbd), absorber 1 um, 30 um diameter. p-i-i-n reference diode on the same wafer
(photodetector.vertical): primary responsivity 0.55 A/W at 1310 nm, 18 mA/cm2 at -8 V. Minus signs and micro signs are
lost in the text layer; values verified on the page render (p.2). Fab empty (passive Methods; Intel, Numonyx, UCSB, UVA).

Not entered: keff 0.09 / 0.08, breakdown thermal coefficient 0.05 %/C, receiver sensitivity -28 dBm at 10 Gb/s (TIA
system), primary dark current < 440 nA (bias not numeric), Fig. 4(a) excess noise points (no labels), earlier-device
GBP 47 / 153 GHz (refs 35-36, rule 3).

## Judgment calls (for the audit)

1. schuck2013: one row per nanowire design although the caption says visible / telecom light use 600 nm / 1 um wide
   waveguides (the 768 and 1542 nm DEoc are probably different physical detectors). Splitting would leave the
   dark-count / jitter / Ic values of the "75 nm, 40 um" detector without an identifiable row (D159), while the paper
   itself pairs those dark counts with both wavelengths for its NEP. Waveguide width kept in notes.
2. Cryogenic GC losses (pernice2012 13.1 / 16.4 dB, schuck2013 about 11 / 13 dB) scoped `per_coupler`: the papers use
   them as the fiber-to-waveguide input loss to set the on-chip photon flux; isolation method not described
   (`method unspecified`). Alternative: `unspecified`.
3. pernice2012 system efficiencies (Table 1) entered as quantum_efficiency_pct, ref_plane fiber, `author_estimate`
   (rest on the nominal 50 % split).
4. pernice2012 OCDE wavelength 1550 nm `wavelength_inferred` (operating wavelength stated p.2, not with Table 1);
   temperature 2 K from "Figure 2 ... measured at 2 K" (p.4). Table 1 dark counts carry 1.7 K only for device II (text).
5. pernice2012 ring time-domain Q / linewidth `derived` (authors' conversion of fitted decay times); spectral Q `measured`
   as q_loaded.
6. chen2018a 30 um PD responsivity `author_estimate` (waveguide power reference not described); 20 GHz "bandwidth" as
   bw3db_ghz approx (criterion not spelled out).
7. mauthe2020 subtype `iii_v_on_platform` (monolithic III-V on Si) though free-space illuminated; `vertical` is the
   alternative.
8. kang2008a bias_v -22.5 V on the 90 % Vbd rows is computed (0.9 x -25 V), noted.
9. fang2008 fab IME borderline (D84a); couplers one row per waveguide width (taper ends at the waveguide width).

## Missing organizations / aliases

- "IBM Research Europe", Rueschlikon, CH (mauthe2020 p.1): alias of org_ibm_research_zurich (used as fab org). Alias
  missing in org_aliases.csv.
- Not orgs: R. Cantor (schuck2013 sample preparation, p.6) and B.M. Voronov (pernice2012 NbN deposition, p.10): person
  thanks without an org; not entered.

## Registry gaps (skipped values)

| proposed parameter | class | skipped values, locator |
|---|---|---|
| nep_w_per_rthz (noise-equivalent power, on-chip / system in condition) | photodetector | pernice2012 Table 1 p.5 best NEP 2.2e-19 / 1.1e-19 / 4.3e-19 / 2.5e-19 W/Hz^0.5 and system NEP; schuck2013 Table 1 p.4 NEPmin 8.8e-20 ... 1.1e-17 and 2.1e-20 / 7.1e-20 (p.4) |
| absorbed fraction % (already proposed in the lit_48 audit) | photodetector | pernice2012 > 97 % for L = 20 um (p.4); schuck2013 atot 73.4-99.9 % (Table 1, p.4) |
| ionization_ratio_keff | photodetector (APD) | kang2008a 0.09 (excess noise, p.2) and 0.08 (GBP fit, p.3) |
| kinetic_inductance_nh_per_um (low priority) | photodetector (SNSPD) | pernice2012 0.91 (p.5); schuck2013 0.75 (p.4) |
| gap_nm for photodetector (wire spacing; lit_37 proposed it for ding2019) | photodetector | pernice2012 120 nm wire spacing (p.3); schuck2013 120 % of the wire width (p.2) |
| breakdown_tempco_pct_per_k (low priority) | photodetector | kang2008a 0.05 %/C, 200-380 K (p.2) |
| platform value `poly_si` (optional) | - | fang2008 poly-Si rows entered as `other` |
