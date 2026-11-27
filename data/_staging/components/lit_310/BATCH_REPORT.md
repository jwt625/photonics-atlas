# Batch lit_310 report

Paper: lit:fukuda2008 (Optics Express 16, 4872, 2008). Distilled 2026-11-27. Validation: `merge_component_staging.py
data/_staging/components/lit_310 --dry-run` -> +11 components, +33 metrics, 0 errors (the 2 warnings are in other
batches: guo2024a, ni2025b).

Page-1 title check: text p.1 "Silicon photonic circuit with polarization diversity", matches the source row; not a
correction / erratum. Text layer clean (`garbled_text_layer` false). Fig. 5(c) values read from the PDF vector marker
positions (helper in the batch scratch folder), Fig. 7 from the page render.

## lit:fukuda2008 (11 components / 33 metric rows)

| component | class | platform | metrics |
|---|---|---|---|
| cmp_lit_fukuda2008_si_wire | waveguide_platform.straight | soi | prop loss 2.2 (TE) / 1.7 (TM) dB/cm cutback measured, C band inferred (p.5); width 400, core 200 nm, BOX 3 um |
| cmp_lit_fukuda2008_dc_pbs | polarization.pbs | soi | PER 10 dB cross / 13 dB bar, C band (p.6); IL < 0.5 dB per port, per_component vs plain Si wire (p.6); width / core / BOX |
| cmp_lit_fukuda2008_rotator_35um | polarization.psr | other | IL ~1 dB (TE out, TM in, 1500-1600 nm axis, p.6); PER ~11 dB derived (1550-1560 nm, p.6); length 35 um, Si core 200 x 200 nm, BOX |
| cmp_lit_fukuda2008_rotator_{30,40,45,50,55,60}um | polarization.psr | other | PER 9.8 / 7.7 / 4.4 / 3.9 / 2.2 / 0.5 dB extracted_from_figure (Fig. 5(c)); length_um each |
| cmp_lit_fukuda2008_ring_filter_no_div | wdm.mrr | soi | PDL ~10 dB at the ~1552.3 nm TE resonance (p.7, Fig. 7) |
| cmp_lit_fukuda2008_poldiv_ring_filter | wdm.mrr | other | PDL 1.2 dB at ~1561 nm (p.7, Fig. 7); ring radius 10 um, gap 300 nm |

Fab: `org_ntt` on all 11 rows (first-person "we made SSCs" p.5, "we deposited silicon oxinitride film" p.6-7, "we also
fabricated a polarization-independent wavelength filter" p.7, "we fabricated rotators with various offsets" p.8; all
authors at NTT Microsystem Integration Laboratories, p.1; fukuda2006 precedent for pre-2025 NTT). No facility; the
acknowledgment names only a funding program (SCOPE, Ministry of Internal Affairs and Communications), not entered.
`process_name` empty (only EB lithography + ECR plasma etching printed, no named process).

Values not entered and why:
- Polarization rotation angle: 72 deg max at 35 um (p.6) and the Fig. 5(c) red series (about 71 / 73 / 66 / 53 / 51 /
  40 / 20 deg for 30-60 um): no parameter (registry gap below).
- Rotator design: simulated 45 um for 90 deg rotation and eigenmode indices 1.542 / 1.525 (p.5), second-core size
  840 nm square and SiOxNy index 1.60 (assumed in design, p.5), taper length 10 um (Fig. 5(a), p.6): no parameter on
  `polarization` (taper_length_um, layer2_thickness_nm and an effective-index parameter are not allowed / do not
  exist); kept in core_material / notes.
- Splitter DC length 10 um, gap 480 nm, bend radius 3 um (p.5, Fig. 4(a)): `coupling_length_um`, `gap_nm`,
  `min_bend_radius_um` not allowed on `polarization` (gap confirmed in lit_27; same as fukuda2006).
- Splitter simulated 10 um separation length (p.4): design statement, geometry only.
- Fabrication tolerance (offsets around 30 nm keep rotation over 65 deg, "insertion loss under 1 dB for the diversity
  circuit", p.8): the paragraph attributes details to ref. [14] (authors' GFP 2007 paper, D259 / D408), and offset /
  rotation have no parameter.
- Rotator PER from Fig. 5(b) spectra: the authors say the ripples prevent a direct estimate (p.6); only the
  Poincare-based values were entered. 35 um Fig. 5(c) marker (-10.6 dB) not entered separately (printed ~11 dB used).
- Fig. 7 drop-peak transmittance levels (~-5 dB with, ~-2 dB without diversity): normalization not stated, not
  entered; no linewidth / FSR printed.
- 10 Gb/s eye diagrams (Figs. 8, 9): no parameter.
- SSCs (p.5, design after ref. [12]): no performance value in this paper, no row.
- Intro examples (6.6 ps DGD over 5 cm for 300 +/- 5 nm cores; > 100 GHz TE / TM resonance difference for a 10 um ring
  with 300 +/- 1 nm core, p.2): hypothetical calculations, not components of this paper.
- Cited values: 2D grating coupler "approximately -7 dB" (ref. [7], p.2): rule 3.

Judgment calls (coordinator questions):
1. Splitter values vs ref. [13] (D259 / D408). The p.6 sentence "measured PERs ... in the C-band are 10 and 13 dB ...
   excess loss for the pass light is less than 0.5 dB for each port" repeats the values (and near-identical wording)
   of the authors' ref. [13], which is already in the atlas (lit:fukuda2006 dc_pbs_single m1, m2, m5), and the
   paragraph ends "Details are discussed and demonstrated in Ref. [13]". The value sentence itself carries no
   citation and follows this paper's own Fig. 4(b, c), whose 1400-1700 nm spectra are a different plot from ref.
   [13]'s, so I kept the three rows (D408 / D438 reading) with a cross-note. Recommendation: keep; alternative is to
   delete m1-m3 and the splitter row under D259.
2. Si wire 2.2 / 1.7 dB/cm also equal the lit:fukuda2006 si_wire rows; here stated without citation (p.5), kept with a
   cross-note (D408).
3. Rotator PER 11 dB basis `derived` (the authors computed it from their measured rotation angle; the formula is not
   printed). `measured` (D80a-style standard conversion of own data) is the alternative.
4. Length-series rotators (30-60 um) entered as sibling rows (rule 9) with figure-read PER only; their lengths are the
   labelled x-axis ticks of Fig. 5(c) (`extracted_from_figure`).
5. Platform `other` for the rotators (Si core inside a SiOxNy second core; no Si-in-SiON value) and for the
   diversity circuit (path includes the rotators); the no-diversity ring is `soi`.
6. The no-diversity filter is treated as a separate device from the diversity-circuit ring (resonances ~1552.3 vs
   ~1561 nm; radius / gap stated only for the diversity circuit), so it carries no geometry. PDL wavelengths are the
   Fig. 7 resonance-peak positions (`wavelength_inferred` true).

Missing fab / facility orgs: none (org_ntt in the registry).

Registry gaps:
- `rotation_angle_deg` on `polarization` (performance): polarization rotation angle of a rotator, measured (Poincare
  sphere) or simulated, as printed. Skipped: 72 deg at 35 um (p.6 Sec. 3.3); Fig. 5(c) series 30-60 um.
- Allow `taper_length_um`, `layer2_thickness_nm` / a second-core width, `coupling_length_um`, `gap_nm` and
  `min_bend_radius_um` on `polarization` (geometry). Skipped: rotator tapers 10 um and 840 nm square SiOxNy core
  (p.5-6, Fig. 5(a)); DC 10 um / 480 nm / 3 um (p.5).
