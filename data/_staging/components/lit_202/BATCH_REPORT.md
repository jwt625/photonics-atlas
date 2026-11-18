# Batch lit_202 report

Distilled 2026-11-18 (verified_on 2026-11-18). One paper. Dry run: `merge_component_staging.py data/_staging/components/lit_202 --dry-run` -> +2 components, +26 metrics, 0 errors (one WARN concerns an already merged row of another paper, cmp_lit_ni2025b_pimmwc).

## lit:horst2009 (IEEE PTL 21(23), 2009, 3 pages)

Page-1 title matches the source row. Text layer clean; Figs. 4-5 read from the page-3 render.

Components / metric rows: 2 / 26

| component | class | metrics |
|---|---|---|
| cmp_lit_horst2009_echelle_extreme | wdm.eg | 13: IL 3.5 dB measured (de_embedded, normalized to a straight waveguide), theoretical IL 2.5 dB (simulated, device_total), 3-dB width 2.4 nm, crosstalk 16 dB, peak-wavelength spread < +/-0.2 nm (8 devices), 8 channels, 3.2 nm spacing, footprint 50000 um2 (250 x 200 um), 38 mirrors, order 20, 500 nm waveguides, 220 nm Si, 2 um BOX |
| cmp_lit_horst2009_echelle_conservative | wdm.eg | 13: IL 3 dB measured (best, abstract "minimum"), theoretical IL 0.5 dB, IL non-uniformity 0.5 dB, 3-dB width 1.8 nm, crosstalk 19 dB, spread < +/-0.2 nm, 8 channels (Fig. 5 count), footprint about 102000 um2 (about 600 x 170 um), 55 mirrors, order 20, about 500 nm strip waveguides, 220 nm Si, 2 um BOX |

Fab: org_ibm_watson on both rows (p.2 Sec. III-A: wafers "processed on a standard 200-mm CMOS line at the IBM Watson Research Center"). process_name as printed with e-beam lithography and RIE. No facility statement; no acknowledgment section. Platform soi (Si strip waveguides, slab free-space region).

Values not entered and why:
- 2.6 um at the Conservative I/O tapers: printed as the mode width at the input / output waveguides, not a waveguide or taper width; `port_width_um` would guess which dimension it is. In component notes.
- Channel spacing of the Conservative layout: not stated for it (same channel grid only implied by Sec. IV-A). In notes.
- Corner-mirror "each facet should reflect 100 %" (p.3 Sec. III-B): theoretical TIR statement, no device value.
- Process details: cited to refs. [6], [7] (rule 3).
- Free-space-region size / ellipse geometry: not printed (and D444: no fpr_length_um from footprints).
- Cladding: not stated.

Missing fab / facility orgs: none (org_ibm_watson exists; printed "IBM Watson Research Center", p.2 Sec. III-A).

Judgment calls:
- (a) The device-to-device peak-wavelength difference "below +/-0.2 nm" (p.3 Sec. IV-A) is stated jointly for the two layouts and other devices on the wafer (8 devices measured). Entered as `wavelength_spread_nm` 0.2 (lt, range, n_samples 8) on both rows with a cross-note rather than kept in notes (D254 concerns a typical value put on one representative row; here the value describes each layout's devices). The coordinator may prefer notes only.
- (b) Abstract "channel-to-channel variation of 0.5 dB" assigned to the Conservative row: it sits in the same clause as the 3 dB minimum IL, which Sec. IV-B gives for the Conservative layout, and matches the Fig. 5 peak spread (about -2.7 to -3.6 dB read); Fig. 4 (Extreme) peaks spread about 1.7 dB. Abstract 3 dB "minimum" -> `statistic: best` on the Conservative IL; the Extreme 3.5 dB has no statistic (not stated).
- (c) "Extinction ratio between channels" (16 / 19 dB; abstract "channel-to-channel isolation") entered as `crosstalk_db` with the wording in condition (type adjacent / non-adjacent not stated); not `extinction_db` (not a notch or on/off contrast).
- (d) "Theoretical loss" 2.5 / 0.5 dB entered as `simulated` (calculated design performance, D82a), scope device_total (brouckaert2007 precedent for simulated echelle IL), method empty (not stated).
- (e) Measured IL scope `de_embedded`, method reference_structure (spectra normalized to a straight waveguide; majority convention for wdm, 121 vs 17 per_component). Wavelength: C band inferred (1.5 um window, channel peaks about 1530-1554 nm in Figs. 4-5). Polarization TE (only TE guided, p.2 Sec. III-A).
- (f) 8 channels / 3.2 nm on the Extreme row: the abstract ties them to "the example presented here" (footprint 250 x 200 um = Extreme; Sec. V also credits Extreme with the channel count and spacing). n_channels design_target and spacing author_estimate (bogaerts2010 / brouckaert2007 precedent: design spacing, no separate measured value). Conservative n_channels 8 is `extracted_from_figure` (curve count in Fig. 5).
- (g) Footprints are products of printed dimensions (`derived`); Conservative `approx` ("approximately 600 x 170 um").

Registry gaps: none confirmed. (A `mode_width_um` geometry parameter for echelle / AWG I/O apertures would take the 2.6 um value; not proposed further without a second source.)
