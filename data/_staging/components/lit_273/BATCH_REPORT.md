# Batch lit_273 report

Papers: lit:tokushima2016, lit:zhao2015, lit:subramanian2012a, lit:xu2017d (all grating couplers). Distilled
2026-11-24 under the pic-component-distill skill (Contracts v4-v7). Page-1 titles match the source rows; no garbled
text layer; no correction / erratum. Totals: 19 components, 139 metric rows. Validation:
`merge_component_staging.py data/_staging/components/lit_273 --dry-run` -> +19 components, +139 metrics, 0 errors (the
two WARN lines printed concern other batches).

Benchmark-table values of other works (xu2017d Table I) are not entered (rule 3); only each paper's own results.

## lit:tokushima2016 (4 components, 30 metrics)

Components:
- `dual_center_folded_gc_r11` (fabricated, soi): dual-center folded 35-nm shallow GC with 11 um bends to a 50 um-core
  MMF. Peak eta_GC -2.23 dB at 1320 nm (per_coupler, reference_structure, derived: the paper subtracts SSC and waveguide
  loss from reference elements); 1-dB tolerance 89 nm (1269-1358 nm); back reflection about -23 dB over 1.30-1.34 um
  (derived from the oscillation depth via Eq. (3)); fiber tilt 12.0 deg; STEM geometry (198 nm Si, 3024 nm BOX, 2652 nm
  over-cladding, 36.2 nm depth, 503 nm pitch, groove fraction 0.686 -> tooth 0.314); Table I segment length / width,
  taper length, 340 nm waveguide width.
- `dual_center_folded_gc_r5` (fabricated, soi): same with 5 um bends; only a Fig. 8 peak read (about -2.8 dB near
  1.29-1.30 um, extracted_from_figure).
- `uniform_gc_35nm_design` and `uniform_gc_70nm_design` (design): Section II 2D-FDTD model gratings; simulated back
  reflection (< -20 dB up to 1.35 um; -26.6 dB comparison point; 70 nm: < -20 dB only below 1.28 um) and their design
  geometry.

Not entered and why:
- 0.5-dB wavelength tolerance 68 nm (1284-1352 nm, p.9): no `bw_0p5db_nm` for fiber_chip_coupler (gap below).
- Simulated eta_up -1.94 dB / eta_dir -1.47 dB at 1330 nm for the as-fabricated structure (p.8), the 0.76 dB "extra
  loss" vs eta_dir (p.9), Section II eta_up vs eta_dir statements (p.3): no directionality / upward-emission parameter.
- Far-field 5 % divergences (5.8 / 12.6 / 11.6 / 21.8 / 22.8 deg, p.5), required NA values: `beam_divergence_deg` not
  allowed for fiber_chip_coupler.
- Simulated 25 Gb/s rise / fall 1.36 ps (p.7) and the 5-8 ps estimates (p.10): no parameter for this class.
- Grating-segment group index about 10 / 20 (p.10, from FSR): `group_index` not allowed for fiber_chip_coupler. Single-mode
  waveguide ng 4.3 (calculated) not entered (no waveguide row with a measured value).
- Emission-angle dispersion -0.10 deg/nm and angle ranges (p.2, p.9): no parameter for this class.
- Single-center folded GC (Fig. 4(a)) and the 7-um dual-center variant (Fig. 5(c)): design-only, no value under a
  registry parameter -> no row.
- 1x2 MMI "expected" back reflection < -40 dB (p.4, p.11): design expectation, `back_reflection_db` not allowed for
  splitter; no MMI row.
- SSC loss and waveguide loss: measured but no values printed.

Fab / facility: fab empty (passive "was fabricated on an SOI wafer", p.8; no org named). Acknowledgment thanks a staff
member for managing sample preparation (p.11): not a fabrication or facility statement. No missing orgs.

## lit:zhao2015 (4 components, 20 metrics)

Components:
- `focusing_gc_700nm_snoi` (fabricated, sin): focusing Geometry-A GC on 700 nm LPCVD Si3N4. Peak -3.7 dB at C band
  (loopback_half, derived: waveguide loss subtracted and pair split equally, both stated), 1-dB bandwidth 54 nm, 2D-FDTD
  50.7 % at 1550 nm (simulated), geometry (1.00 um pitch, 400 nm etch, FF 0.367, 700 nm core, 3 um BOX, 30 periods,
  8 deg, 70.2 um length, 70.2 x 19.7 um footprint).
- `inverse_taper_300_to_700nm` (fabricated, sin, waveguide_platform.other): the in-layer inverse taper from the
  300-nm-thick access waveguide to the 700 nm strip; simulated -0.227 dB averaged over 1520-1600 nm; tip 150 nm,
  Lt 20 um, strip width 900 nm.
- `si3n4_strip_700nm` (fabricated, sin, waveguide_platform.straight): 1.5 dB/cm "measured" loss of the 400 um
  interconnecting strip (printed as the subtracted term; method and width not stated; band c_band inferred).
- `grating_geom_b_design` (design, sin): Geometry B comparison, simulated 36.7 % at pitch 1.00 um.

Not entered: 2D-FDTD power budget (71.7 % up, 21.5 % down, 6.8 % back reflection plus through combined, 17.6 % mode
mismatch; p.2) - combined terms / no directionality parameter; 41.6 % and 34.8 % (intermediate design points at pitch
0.98 um, p.2); collapsed-tip penalty 0.29 dB (3D-FDTD estimate, note only); focal length 20.2 um, 15 um taper width at
the 15th period, We 4 um (notes; no clean role parameter); simulated BOX optimum 2.9 um (not the built stack).

Fab / facility: fab `org_huazhong_university_of_science_and_technology` borderline (D84b): passive fabrication text,
all authors at WNLO / HUST, acknowledgment thanks the engineers of the Center of Micro-Fabrication and Characterization
of WNLO "for the support in device fabrication" (p.4-5); facility empty (staff thanks never set a facility; xu2025 /
lu2017 precedent). `org_center_of_micro_fabrication_and_characterization` exists in the registry if the auditor reads the
sentence as facility support.

## lit:subramanian2012a (9 components, 74 metrics)

Components:
- `wire_500nm_unclad` / `wire_500nm_clad` (fabricated, sin, waveguide_platform.straight): cutback loss at 900 nm,
  3.5 +/- 1.7 and 2.8 +/- 0.6 dB/cm (statistic mean, spread definition not stated), geometry.
- Six fabricated GCs (sin): linear GCs etched 70 / 120 / 140 nm and focusing GCs etched 70 / 120 / 220 nm. Per row:
  Table I measured efficiency (loopback_half, measured: per-GC value "determined from the fibre-to-fibre transmission"
  with no arithmetic shown; D452), measured 1-dB bandwidth (+/- in notes), for LGCs the CAMFR theoretical efficiency and
  bandwidth (simulated); period 630 nm, FF 0.5, 20 periods, 10 um grating width, about 220 nm core, 2.4 um BOX, etch
  depth; LGC 140 nm optimum angle 8 deg (measured).
- `gc_dbr_design` (design): simulated 68 % with a three-pair DBR (Fig. 8).

Not entered: 1-dB angular tolerance about 4 deg (p.2; no parameter); Fig. 3 / Fig. 7 simulation sweeps (BOX, period);
refractive index 2.043 (no parameter; core_material); Fig. 4 angle-scan points.

Conflicts kept with notes (D417): abstract "5.7 and 6.5 dB, 26 and 40 nm" matches neither Table I nor the text; FGC
120 nm bandwidth 23 (text) / 24 +/- 1 (Table I) / 25 nm (conclusion); FGC 220 nm 25 nm (text) vs 21 +/- 1 (Table I);
FGC 70 nm Fig. 6 curve about -6.4 dB vs Table I -7.8 dB; DBR oxide 115 nm (text) vs 155 nm (caption). Table I values
entered throughout.

Measured GC rows carry `polarization: unpolarized` (white-light source, unpolarized input, p.2) although the GCs are
TE designs: the printed efficiencies include whatever the unpolarized launch costs.

Fab / facility: fab `org_imec` borderline (D84b / golshani2021 / doerr2010 precedent): "thank IMEC's p-line and
[a named staff member] for the fabrication of the Si3N4 waveguides" (p.4); process text passive; one author at IMEC.
Applied to the GC rows as well (same lithography / RIE flow, p.2). process_name empty (only "193 nm optical
lithography", no named process). Alias candidate: "IMEC's p-line" -> org_imec.

## lit:xu2017d (2 components, 15 metrics)

Components:
- `apodized_sin_on_soi_gc` (fabricated, si_sin_multilayer): best measured -2.5 dB (statistic best, per_coupler, method
  unspecified, band c_band inferred from Table I), 1-dB bandwidth 65 nm; simulated -2.13 dB / 61.23 % at 1567 nm and
  about 63 nm; fiber angle -8 deg; 600 nm SiNx, 220 nm Si (layer2), 2 um BOX.
- `uniform_sin_on_soi_gc` (fabricated, si_sin_multilayer): measured -3.6 dB, 70 nm; simulated uniform-grating optimum
  44.46 % / -3.52 dB (period 0.95 um, FF 0.5, 1.6 um buffer); period 965 nm, FF 0.513 (from 51.3 %).

Not entered: Table I values of other works (rule 3); simulated upward power fraction about 85 % (no parameter); SiO2
buffer 1.6 um (no inter-layer buffer parameter for fiber_chip_coupler); refractive indices (oxide and nitride values
appear swapped in the text, p.2).

Fab / facility: fab empty (passive "patterned by e-beam lithography (EBL) and etched", p.2; no org named). No
acknowledged facility. No missing orgs.

## Judgment calls for the auditor

1. tokushima2016 GCR11: eta_GC -2.23 dB entered as `per_coupler` + `reference_structure` + `derived` (printed formula
   subtracting SSC and waveguide terms); the fiber side is a step-index 50 um MMF, not an SMF (condition). Bandwidth
   also `derived` (width of the reference-subtracted spectrum, doerr2010 precedent).
2. tokushima2016 back reflection -23 dB `derived` (model extraction, D80a) with qualifier approx over 1300-1340 nm;
   polarization left `unspecified` for that test element.
3. tokushima2016 Section II gratings as two `design` rows (they are model gratings; the fabricated segments differ in
   pitch / depth). The -26.6 dB comparison value sits on the 35-nm design row with band o_band inferred.
4. tokushima2016 GCR5 row rests on a single figure read (no printed value).
5. zhao2015 inverse taper as its own `waveguide_platform.other` row (simulated value only, D80e fabricated); the
   1.5 dB/cm strip loss as its own row with method unspecified and band inferred (printed only as a subtracted term).
6. zhao2015 fab HUST borderline from engineer thanks; facility empty.
7. subramanian2012a measured GC rows `loopback_half` + `measured` (no arithmetic shown), `polarization: unpolarized`;
   peak wavelengths: LGC 70 / 140 nm stated (888 / 907.5 nm), others `nir_below_o` inferred.
8. subramanian2012a fab org_imec on all fabricated rows from the p-line thanks.
9. xu2017d measured values `per_coupler` with method unspecified, band c_band inferred; the uniform-grating
   simulation (0.95 um / FF 0.5) is attached to the fabricated 965 nm / 51.3 % row with a condition saying so.
10. Unit conversions entered as `derived` (STEM nm -> um, 1.00 um -> 1000 nm pitch, 51.3 % -> 0.513, groove-fraction
    to tooth-fraction fill factors).

## Registry gaps (skipped value, locator, proposed definition)

- `bw_0p5db_nm` for fiber_chip_coupler: tokushima2016 68 nm (1284-1352 nm), p.9 Sec. V-A. Definition: full width
  where coupling stays within 0.5 dB of its peak.
- Upward directionality / upward emission efficiency (dB or %) for fiber_chip_coupler: tokushima2016 eta_dir -1.47 dB,
  eta_up -1.94 dB (p.8); zhao2015 71.7 % upward (p.2); xu2017d about 85 % upward (p.2). Definition: fraction of guided
  power diffracted upward (eta_up) or upward / (upward + downward) (eta_dir), as defined by the paper.
- `beam_divergence_deg` for fiber_chip_coupler (already a D437 candidate): tokushima2016 5 % full angular widths 5.8 /
  12.6 / 21.8 / 22.8 deg (simulated, p.5).
- `group_index` for fiber_chip_coupler: tokushima2016 grating-segment ng about 10 at 1310 nm and 20 at 1330 nm (p.10).
- Angular 1-dB tolerance of a GC (deg): subramanian2012a about 4 deg (p.2, Fig. 4).
- Inter-layer buffer thickness for dual-layer GCs (`gap_nm` widened to fiber_chip_coupler or a buffer parameter):
  xu2017d 1.6 um SiO2 between SiNx and Si (p.2).
