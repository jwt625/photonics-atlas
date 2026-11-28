# Batch lit_315 report

Paper: lit:tian2020, "Hybrid integrated photonics using bulk acoustic resonators" (Nature Communications 2020).
Distilled 2026-11-28. Validation: `merge_component_staging.py data/_staging/components/lit_315 --dry-run` -> +5
components, +18 metrics, 0 errors (the 2 warnings are in other batches: guo2024a, ni2025b).

Source copy: the cached file is the arXiv v1 preprint (1907.10177, 41 pages: main text p.1-16, Supplementary
Material p.17-41). Values come from the preprint only; the journal version was not read (D430 / D433). Page-1 title
matches the source row (the title is split across two lines, hence the 0.86 title-check score); not a correction or
erratum. Text layer clean. Supplement locators are written `p.N Supp. <label>`. The Fig. 13(e, f) Q values were read
from the PDF vector marker positions (helper script in the batch scratch folder).

## lit:tian2020 (5 components / 18 metric rows)

| component | class | platform | metrics |
|---|---|---|---|
| cmp_lit_tian2020_disk_ring | resonator.ring | sin | q_loaded TE 1.33-1.64e5 and TM 0.79-0.88e5 over -60 to +60 V (Supp. Fig. 13(e), extracted_from_figure); TE linewidth 1-2 GHz (p.6, author_estimate); radius 118 um, width 1800 nm, core 800 nm, 2.4 um SiO2 to the Mo electrode |
| cmp_lit_tian2020_disk_actuator | phase_shifter.other | sin | tuning -0.2 pm/V (p.11, measured); TE -0.192 / TM -0.195 pm/V derived from the Fig. 13(c) labels (-11.5 / -11.7 pm at +60 V); AlN fundamental thickness resonance about 4-4.3 GHz (p.6); response time < 1 ns (p.11, author_estimate) |
| cmp_lit_tian2020_donut_ring | resonator.ring | sin | q_loaded TE 2.46-2.77e5 and TM 0.70-0.74e5 (Supp. Fig. 13(f), read on the panel (e) scale) |
| cmp_lit_tian2020_donut_actuator | phase_shifter.other | sin | tuning TE +0.0272 / TM +0.0943 pm/V derived from the Fig. 13(d) labels (1.63 / 5.66 pm at +60 V) |
| cmp_lit_tian2020_damped_actuator | phase_shifter.other | sin | AlN resonances about 4.13 GHz (fundamental) and 8.7 GHz (second harmonic) after damping the Si backside (p.14, Fig. 4(e, f)) |

Fab / facility (all 5 rows): fab `org_epfl;org_purdue_university`, facility
`org_center_of_micronanotechnology;org_birck_nanotechnology_center`. The p.16 acknowledgment says "The samples were
fabricated in" the EPFL CMi and the Birck Nanotechnology Center at Purdue University. That names a place, so it sets
fab and facility (D448); the liu2020a and siddharth2024 rows use the same ids. The paper does not say which site made
which part, so both orgs go on every row. The preprint has no author-contributions section. `process_name` is empty:
the Si3N4 "subtractive process" is a generic word cited to ref. 35.

### EO-atlas boundary and class of the AlN acousto-optic modulator (task question)

- The paper's main device is a stress-optic (electro-acousto-optic) microring modulator: an AlN film drives
  high-overtone bulk acoustic resonances (HBAR) in the chip stack. The EO atlas already holds stress-optic rows:
  khalil2026-a (SrTiO3 acousto-optic racetrack, `eo_effect stress_optic`) and montifiore2026-a..d (PZT-actuated
  Si3N4). The EO atlas has no tian2020 row. So I treat the modulation metrics as an **EO-atlas candidate** and did
  not enter them here (rule 2):
  - broadband modulation 3-dB bandwidth 250 MHz around 4.13 GHz and 260 MHz around 8.7 GHz (p.14, Fig. 4(f), TM
    mode, damped device). The abstract (p.1) and p.4 print "4.1 and 8.7 GHz ... 250 MHz each"; this conflicts with
    the 260 MHz on p.14 (D417 note for the EO atlas);
  - the multi-octave S21 response of the HBAR modes over 1-6 GHz, TE strongest near 2 GHz and TM near 4 GHz (p.6,
    Fig. 2(b, c));
  - > 20 dB contrast between resonance and anti-resonance (p.8);
  - 6 GHz square-wave drive (7 Vpp) still visible in the output (p.13, Fig. 4(c)).
  The existing `bw3db_khz` is a baseband cutoff. These numbers are passband widths around a GHz carrier, so storing
  them there would misread as a 250 MHz cutoff.
- The actuator itself (DC resonance tuning, AlN resonance, response time) fits the existing class
  `phase_shifter.other`. Lit precedents for AlN / PZT piezo actuators on Si3N4: liu2020a, lihachev2022,
  siddharth2024, dong2019. Each ring is a separate `resonator.ring` row with a cross-note (D396). There is no
  modulator class in this registry, and I did not force one.

### Values not entered and why

- Power efficiency 5 nW per pm of resonance tuning (p.3, p.11): `tuning_power_mw` is a total power for a stated
  range, and `tuning_efficiency_pm_per_mw` is defined for heater or self-heating input. The paper does not say how
  the power was obtained (leakage or dynamic). Kept in notes; registry gap below.
- HBAR acoustic FSR about 17.5 MHz (average 17.515 MHz, reference mode 3.0145 GHz; p.5, p.9 Fig. 3(c, d)),
  mechanical linewidth about 3 MHz and mechanical Q about 1000 (p.5-6), SiO2-layer envelope period about 490 MHz
  (p.6): no parameter (see gaps). I did not put the 17.5 MHz in `mech_resonance_khz`. The paper calls it an FSR
  between overtones, not a fundamental mode; liu2020a's ~17 MHz was printed as the "fundamental HBAR mode".
- Calculated effective electromechanical coupling k_t,eff^2, maximum 0.15 % near 4.3 GHz (p.28 Supp. Fig. 10(a)),
  and the 1D Mason / transfer-matrix model S11 (Supp. p.17-29): model outputs, no parameter.
- COMSOL modes at 2.041 GHz (Disk, p.7 Fig. 2(h, i)) and 2.125 GHz (Donut, p.35 Supp. Fig. 14(g, h)), and static
  stresses (about 2 MPa, 1 nm displacement scale; Supp. p.30-32 Figs. 11-12): simulated single HBAR modes or stress
  maps, with no parameter for one overtone of a comb.
- Electromechanical crosstalk -60 dB between adjacent actuators (p.8; p.36-37 Supp. Fig. 15). It was measured on a
  different chip: three actuators on one ring, 500 um Si substrate, 7 um SiO2. `crosstalk_db` is not allowed on
  `phase_shifter`, so this would be a row with no allowed performance value. I did not create the component.
- Material constants: AlN e33 about 1.55 C/m2 (cited, ref. 34, p.5); intrinsic AlN k_t^2 6.5 % (model input,
  p.22); breakdown field > 100 V/um (generic AlN property in a comparison with PZT, p.4). None is a device result.
- Cited comparisons: thermal tuning about 1 mW/pm and about 1 ms (refs. 16-17, p.2-3), and the PZT / SAW work (refs.
  24-26, 29). Excluded under rule 3.
- "Nearly -12 pm under positive 60 V" (p.33) and the 0.4 pm shift for 2 Vpp (p.11): already covered by the Fig. 13(c)
  label rows and the -0.2 pm/V row; not entered again.
- Edge coupling (lensed fiber to inverse taper, about 100 uW into the chip, p.15): no coupling value, so no row.
  Setup items (-5 dBm RF drive, 12 GHz photodiode, VNA) are not components (rule 13).
- Disk-device geometry: the ring sits 3 um inside the actuator edge (Donut: 5 um inside the inner edge), and the Si
  substrate is 230 um. No parameter, so both are in core_material. The Fig. 1(b) "3um" vertical label runs from the
  Si3N4 top to the Si; the lower cladding below the core is not printed, so `box_thickness_um` is not entered.
- Donut ring radius and cross-section are not restated, so not entered (only "same structure" from the Fig. 11
  cross-sections, in notes).
- S21 roll-off from about 9.5 GHz, attributed to the TM optical Q (p.13): not a component parameter.

### Judgment calls (for the audit / coordinator)

1. **Damped device as its own row.** The broadband AOM is "the fabricated device" after XeF2 backside roughening and
   a PU / Ni-powder damping layer (p.13). It got a separate `phase_shifter.other` row (substrate stack differs, D32).
   It holds only the two AlN resonance frequencies; its passband widths are EO-atlas candidates. Alternative: drop
   the row and move the two resonances to notes of the Disk actuator.
2. **Response time < 1 ns** (`rise_time_us` 0.001, qualifier lt, author_estimate). The paper prints "sub-ns response
   time" (p.11). The evidence is that the input-output cross-correlation of 20 ns pulses resembles the input
   auto-correlation (Fig. 4(b) inset); no edge time is shown. The condition says it is not a 10-90 % rise time.
   Alternative: notes only.
3. **Per-polarization tuning rows** derived from the Fig. 13(c, d) labels, computed as shift at +60 V divided by
   60 V, `derived`. The fits have R2 > 99 % (caption), but the slopes themselves are not printed. On the Disk
   actuator these sit beside the printed -0.2 pm/V row (polarization not stated with it). Signs are as printed (Disk
   blue-shifts, Donut red-shifts for positive voltage), following the tu3c5 / zhang2015 precedent.
4. **Q from Fig. 13(e, f).** The axis says only "Quality factor (Q)", so the values go in `q_loaded` with a note.
   Each row stores the range over the 13 bias points (statistic range) and the 0 V value in condition. Panel (f) has
   no tick labels and was read on the panel (e) scale; the grid lines line up. Wavelength 1550 nm from the caption's
   "lambda0 (~1550 nm)" (D393, not inferred).
5. **TE linewidth 1-2 GHz** (p.6) taken from the parenthesis after "its linewidth" in the resolved-sideband sentence.
   No fit is shown, so `author_estimate` (D76).
6. Fab EPFL + Purdue on every row comes from the acknowledgment alone (D448), with no per-part split. The Methods
   detail the AlN process steps (Purdue tools are not named), but no sentence assigns the Si3N4 to one site.

### Missing fab / facility orgs

- OEM Group: "100 nm Mo and 1 um polycrystalline AlN films are sputtered on SiO2 cladding through foundry services
  (OEM Group)" (p.15 Methods). This is film deposition only, so it stays a note (D431 ruled "OEM Group note only"
  for lihachev2022). Not in the registry; no request needed unless the coordinator reverses D431.
- No other missing orgs: EPFL, Purdue, CMi and Birck are all in the registry.

### Registry gaps (skipped value, locator, proposed definition)

- `tuning_power_per_pm_nw` (phase_shifter): 5 nW/pm (p.3, p.11). "Electrical power per pm of resonance shift for a
  non-thermal actuator, as stated (power basis in condition)". Alternative: widen `tuning_efficiency_pm_per_mw` to
  piezo / capacitive actuators and store 2e5 pm/mW as derived.
- `acoustic_fsr_mhz` / `mech_q` / `mech_linewidth_mhz` (phase_shifter): 17.5 MHz (17.515 MHz), Q about 1000,
  about 3 MHz (p.5-6, p.9 Fig. 3). Definitions: "frequency spacing of HBAR overtones", "mechanical quality factor of
  the actuator / HBAR mode", "mechanical resonance full width".
- `crosstalk_db` widened to phase_shifter (electrical or acoustic crosstalk between adjacent actuators, type in
  condition): -60 dB (p.36-37 Supp. Fig. 15). The value comes from a separate three-actuator chip.
- A passband modulation width parameter (`mod_passband_3db_mhz` plus carrier frequency) only if the coordinator keeps
  resonant AOM bands out of the EO atlas: 250 MHz at 4.13 GHz, 260 MHz at 8.7 GHz (p.14).

### EO-atlas candidate (for that atlas)

tian2020: AlN-actuated HBAR stress-optic Si3N4 microring modulator. Rows Disk and Donut; damped broadband version.
3-dB bands are listed in the boundary section above. DC tuning -0.2 pm/V. Ring Q, TE linewidth and AlN resonances are
entered here (component rows above).
