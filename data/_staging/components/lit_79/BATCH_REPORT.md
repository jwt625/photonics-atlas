# Batch report: lit_79 (micro_optics, free_space_emitter)

Date: 2026-11-04. Result: 22 components, 153 metric rows; `merge_component_staging.py --dry-run`: 0 errors. All five cached texts match their source rows (page-1 check). yulaev2022 page-1 title differs in wording from the registered journal title (same authors, abstract, DOI in source.json); no correction / erratum files.

| paper | components | metric rows |
|---|---|---|
| wessling2022 | 3 | 12 |
| gissibl2016 | 11 | 46 |
| yulaev2022 | 2 | 27 |
| gagino2024 | 4 | 53 |
| poulton2022 | 2 | 15 |

## wessling2022

Rows: GaN lens 1 / 2 / 3 on diamond (`micro_optics.integrated_lens`, platform `other`). The only registered performance value is the measured focal-spot FWHM (700-800 nm, one range for all three, `beam_diameter_um`, derived unit conversion, wavelength 525 +/- 50 nm in condition).

Not entered:
- Focal lengths and NA (Table 1, p.8), no parameter; held in component notes.
- Roughness 1.4 nm r.m.s. lens (p.4), 0.4 nm mesa bottom (p.3); suspension yield > 85 %, N = 210 (p.11); RMS deviation of the fits 30-50 / 40-110 nm (p.6).
- Printed lens on the GaN/AlN waveguide facet (p.8): no performance number (mode image at 1630 nm only; alignment about +/-1 um; ROC 3.3 um design with FDTD image without a number). Geometry-only, no row (rule 9). Waveguide 1.2 um x 2 um at the facet, 850 nm GaN on 350 nm AlN, 600 nm SiO2 cladding.
- Fig. 1(b) ROC 16 um and Fig. 3(a)-(b) bowed test devices: no performance value.

Fab / facility: fab empty (only "we developed" / passive statements, no named fabricating author; D80b). James Watt Nanofabrication Centre (University of Glasgow, p.9) applies only to the facet-lens PIC chip, which has no row, so it is unused. University of Strathclyde is not in the registry but is not needed by any row.

## gissibl2016

Rows: six spherical lenses D = 50-300 um, one toric lens, donut shaper, top-hat shaper (`micro_optics.facet_lens`, platform `polymer`), left- and right-handed chiral photonic crystal (`polarization.other`). The text layer renders micro as `m`: every dimension was checked on the page renders.

Not entered:
- Toric lens -95.8 / -75.8 um (Fig. 3(b)): topography only, no row (rule 9). Bare fibre D = 0 um reference (w about 1.7 mm at 20 mm, Fig. 2(b)): not a component. Fig. 1(b)-(c) model devices: no measured value.
- Total transmittance up to nearly 70 % at 808 nm (p.3): lens not identified, in notes (D159).
- RMS roughness 43 nm, flat films below 10 nm (p.3); surface deviation below 1 um (p.3, Fig. 2(e)): no parameter.
- Simulated beam-width curves in Figs. 2-3: not read, measured points entered.
- Chiral selectivity bandwidth roughly 50 nm (p.5): level not stated, no parameter on `polarization` without converting (notes). Rod and layer distances: `pitch_um` / `period_nm` are not registered for `polarization` (core_material).
- "heights of 250-300 um and 120 um" for the Fig. 4 optics (p.8): the 120 um cannot be assigned, not entered.

Fab: `org_university_of_stuttgart`, from "T.G. performed ... direct laser writing" (p.9) with T.G.'s affiliation (D395). Nanoscribe thanked for help with lens fabrications (p.9): thanks, not entered.

## yulaev2022

Rows: NZI grating emitter (`free_space_emitter.grating_emitter`), standing-wave resonance (`resonator.other`, D396, holds wavelengths, Q, thermal drift). Fab: NIST, "DAW fabricated samples" (p.21).

Not entered:
- Simulated 0.01 % reflection and 0.4 % transmission (p.10): `back_reflection_db` not registered on `free_space_emitter`, notes; no dB conversion.
- Fig. 2(e) far field: a field |E| plot, width not read as power FWHM.
- Measured resonance width from Fig. 3(i): baseline ambiguous, not read.
- Evanescent expander, inverted taper: no own number. Mode conversion ratio about 2.1e5: no parameter.

## gagino2024

Rows: OPA emitter (`free_space_emitter.other`), SOA gain path (`amplifier.soa`), star coupler (`splitter.other`), EOPM (`phase_shifter.other`), all platform `inp`, cross-noted (D396). Fab: `org_smart_photonics`, MPW run stated (p.3).

Not entered:
- Table 1 literature rows; 150 nm 3 dB gain bandwidth (authors' earlier work, p.2; D259); mREV method numbers from ref. 43; 35 dB/mm and 20 mW of ref. 27.
- Supplement figures (S2-S13): supplement not cached.
- Current density and input power of Fig. 2(f): operating sweep, not entered.
- EOPM leakage below 500 uA: no parameter (notes).

## poulton2022

Rows: 8,192-element OPA (`free_space_emitter.other`), tunable laser (`laser.tunable`). Platform empty on both (paper says silicon photonics and silicon wafers, stack not stated; D422 / D423). Fab empty: passive "fabricated", commercial foundry named only for the CMOS, all authors at Analog Photonics (D80b).

Not entered:
- LiDAR system (p.5-6): about 50 mW emitted, 10 % target at about 35 m; system-level, no row. Transmit / receive OPA and coherent detector have no component numbers. EO phase shifters: microwatt level is cited from ref. 11, no own number, no row.
- Table I rows of other work. Splitter tree: no number.
- 400 mW radiated, 5 W linear input, yield above 95 %, 2.5 W CMOS: no parameter on `free_space_emitter` (notes).
- Laser chirp 75 THz/s over 17.5 us (1.3 GHz): no parameter (notes).
- Insertion loss about 11 dB has `band: unspecified`: no wavelength stated; 0.65 lambda at 1 um pitch was not used to infer one.

## Judgment calls (for the audit)

1. `beam_diameter_um` used beyond its "at the interface" definition: focal-spot FWHM (wessling2022), 1/e2 diameter at a stated distance (gissibl2016), donut outer and peak-to-peak width (gissibl2016). Each states the definition in condition.
2. gissibl2016 stored diameters are figure-read radii doubled; basis stays `extracted_from_figure` with the reading in notes.
3. Negative printed lens radii stored as magnitudes (printed sign in notes), so that the row keeps a usable radius; the registry has no sign rule for `lens_radius_um`. Basis not moved to derived for this reason.
4. gissibl2016 `extinction_db` values come from two transmittance readings at a wavelength I selected inside the band the figure marks (1560 / 1570 nm); the paper prints no contrast number. Delete if figure-derived contrast is not acceptable.
5. `mfd_fiber_um` for the top hat (6 um) is a design beam size, not a fibre mode (stated in condition).
6. wessling2022 lenses on diamond as `integrated_lens` (no subtype for a printed lens on a substrate surface); no facet attachment.
7. yulaev2022 `resonator.other` row added under D396 so Q, resonance wavelengths and thermal drift have a home.
8. gagino2024 EOPM uses `phase_shift_pi` = 2 with the 6.4-9.1 V range in condition, instead of halving to `v_pi_v` (the phase-voltage relation is not stated as linear). InP EOPM kept as `phase_shifter.other` as for the merged p-i-n rows (lu2016a, feng2011), although the class label reads non-EO; poulton2022 has no such row.
9. gagino2024 values with no stated wavelength use the device range with `wavelength_inferred: true` (star coupler, HG SLSR, 20 dB design SLSR).
10. gagino2024 `pitch_um` 160 on the amplifier is the printed SOA spacing; centre-to-centre not stated.
11. gagino2024 gain row at 1600 nm is negative (-1.2 dB, net loss), kept with sign as read.

## Missing fab / facility orgs

None needed by a row. Printed, unused: University of Strathclyde (wessling2022 p.1), James Watt Nanofabrication Centre (wessling2022 p.9).

## Registry gaps (skipped value + locator, proposed definition)

| proposed parameter | classes | skipped values | definition |
|---|---|---|---|
| `focal_length_um` (open candidate, D432 / D443) | micro_optics | wessling2022 p.8 Table 1: f_air measured 4.5 / 2.0 / 1.5 um (+/- 1.0), FDTD 4 / 2 / 1, GO 6 / 3 / 2, f_dia FDTD 14 / 7 / 5 | focal length; medium, reference surface and wavelength in condition |
| `numerical_aperture` | micro_optics | wessling2022 p.8 Table 1: NA_dia 1.0 / 1.4 / 1.7; p.7: about 0.67 in air | numerical aperture as stated, medium in condition |
| `rms_roughness_nm` (open candidate, D432) | micro_optics | wessling2022 p.4 1.4 nm, p.3 0.4 nm; gissibl2016 p.3 43 nm, below 10 nm | RMS surface roughness, method in notes |
| `surface_error_rms_nm` / peak deviation (open candidate, D432) | micro_optics | gissibl2016 p.3 below 1 um (peak, not RMS) | deviation of a measured surface from design; statistic in condition |
| `output_power_dbm` on free_space_emitter | free_space_emitter | poulton2022 p.4 400 mW radiated; p.6 about 50 mW | radiated optical power, ref plane in ref_plane |
| `power_handling_dbm` on free_space_emitter | free_space_emitter | poulton2022 p.4 linear up to 5 W input | as registered |
| `power_consumption_w` on free_space_emitter (open candidate, D432) | free_space_emitter | poulton2022 p.4 2.5 W | as registered |
| `element_yield_pct` | free_space_emitter, switch_fabric | poulton2022 p.4 above 95 % at R2 above 0.8 | working element fraction, criterion in condition |
| `chirp_rate_thz_per_s` | laser | poulton2022 p.5 75 THz/s, 17.5 us, 1.3 GHz | linear frequency chirp rate, duration and excursion in condition |
| `back_reflection_db` on free_space_emitter | free_space_emitter | yulaev2022 p.10 about 0.01 % slab reflection | as registered |
| selectivity bandwidth, `bw_nm` with level in condition | polarization | gissibl2016 p.5 roughly 50 nm | span of the stated selectivity, level not given |

## Coordinator decisions

1. Keep or delete figure-derived contrast in gissibl2016 (judgment call 4).
2. Keep the wider use of `beam_diameter_um` or wait for a dedicated focal-spot parameter (judgment call 1).
3. Sign rule for `lens_radius_um` (judgment call 3).
