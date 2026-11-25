# Batch lit_287 report

Distilled 2026-11-25. One paper. `merge_component_staging.py data/_staging/components/lit_287 --dry-run`: +3 components, +38 metrics, 0 errors (the two WARN lines belong to merged guo2024a / ni2025b rows).

## lit:jongebloed2026 (Optics Express 34(3) 4522, 2026; Nd-doped polycrystalline Al2O3 waveguide amplifier at 1064 nm)

Page-1 title matches the source row; not a correction; text layer clean (figure values from page renders and the PDF vector data).

| component | class | metrics |
|---|---|---|
| cmp_lit_jongebloed2026_nd_al2o3_spiral_amp_5p5cm | amplifier.rare_earth | 19 |
| cmp_lit_jongebloed2026_al2o3nd_inverse_taper_edge_coupler | fiber_chip_coupler.edge | 11 |
| cmp_lit_jongebloed2026_al2o3nd_film_slab | waveguide_platform.other | 8 |

- Amplifier: external (fiber-to-fiber) gain 14.5 / 11.9 / 5.6 / 3.3 dB (measured), internal gain 19.9 dB and 3.6 / 4.1 dB/cm (derived, D166), fiber-to-fiber NF 8.5 dB (measured) and internal NF 4.5 dB (derived), off-chip output power 3.4 dBm, saturation output power 4.8 dBm; geometry (length, footprint, design and STEM widths, STEM height and sidewall angle, BOX, cladding).
- Edge coupler: measured cutback loss 4.0 +/- 0.6 dB per facet at 1064 nm; simulated 0.7 dB per facet (1064 nm), about 18.7 % and at least 7.3 dB per facet (805 nm); tip width, taper length, waveguide-end width / height, tip sidewall angle, fiber MFD at 1064 / 805 nm.
- Film: slab (prism-coupling) loss at 405 / 451 / 521 / 636 / 978 nm read from the Fig. 2(e) vector data; background loss about 0.08 dB/cm at 1064 nm (author_estimate, lambda^-4 fit extrapolated, D435); VASE film thickness; BOX.

### Values not entered and why
- Internal net gain at the 14.5 dB point (14.5 + 2 x 4.0 = 22.5 dB): not printed; only the 4.1 dB/cm per-length figure is entered.
- Gain, output and NF curves of Fig. 6, 8, 9 beyond the printed values: not read. Fig. 6(a) y tick labels are not evenly spaced (13, 9, 6, 3, 0, ..., -13 on equal intervals), so figure reads of that panel are unreliable.
- Simulated bend loss vs radius (Fig. 1(d)) and the 300 um minimum bend radius: no printed loss value; min_bend_radius_um is not allowed on amplifier rows (noted on the component).
- Nd3+ concentration about 2.2e20 ions/cm3, excited-state lifetime 184 us (Fig. 3(b)), PL spectrum, refractive index 1.733 at 1064 nm: no registry parameter (notes only).
- Nd3+ absorption about 3.56 dB/cm at 521 nm over the scattering fit: material absorption used for the concentration estimate, in film-row notes; not a loss row.
- Tip height 160 nm: no tip-thickness parameter (in core_material / notes).
- System loss 13.4 dB and the fiber WDMs / splitters / OSA: measurement setup (rule 13).
- Nd:YAG 295 us, Nd-silicate 313 us lifetimes, ref. [34] 14.4 dB internal gain: cited values (rule 3).

### Missing fab / facility orgs
None to add. No fabrication statement names a fabricator (passive verbs, p.4-5): fab empty (D80b). CMAM (Centro de Microanalisis de Materiales, Universidad Autonoma de Madrid; Acknowledgement, p.11) is thanked for RBS beam time on calibration samples, not fabrication, so it is not a facility under the garciablanco2025 / bonneville2024 precedent; it is also not in the registry. The FIB milling thanks go to a named person (staff thanks, D84b).

### Judgment calls (auditor please check)
1. NF 8.5 dB conditions: the abstract ties it to the 14.5 dB / -14.9 dBm point ("under those conditions"). The body (p.10) ties it to -22.4 dBm signal and 22 dBm pump, and Fig. 9(b) shows about 13 dB near -15 dBm signal. The body conditions are used and the conflict is in the notes.
2. psat_out_dbm 4.8 dBm: the paper calls it the "saturation output power", but it equals the maximum of Fig. 8(b), and no compression criterion is given (noted). D580 deleted a psat value that the paper never called a saturation power; here the paper does.
3. output_power_dbm 3.4 dBm: the text says "up to 3.4 dBm" for Fig. 6(b). Assigning it to the 0.1 dBm incident-signal trace comes from the figure.
4. gain_db 11.9 / 5.6 / 3.3 dB: no pump power is printed for these points. The condition says "highest pump of the Fig. 6(a) sweep" (about 22.2 dBm from the vector data; that number is in the notes only).
5. Internal NF 4.5 dB derived as 8.5 - 4.0 (input-facet correction); the paper prints the result without the arithmetic.
6. Film slab losses are entered as a waveguide_platform.other row, following the bonneville2020 film rows. The 978 nm point's wavelength comes from the text ("up to 978 nm").
7. Edge coupler 4.0 dB is `measured` with method cutback. The cutback structures and whether index-matching gel was used are not stated. test_structure is left empty.
8. Two width_nm rows on the amplifier (1000 design, 1040 STEM), both `derived` (um -> nm, D157/D256). The 650 nm height is `measured` (printed in nm on the STEM figure).
9. cladding_thickness_um 7 (approx, derived) = 1 um LPCVD + 6 um PECVD as printed.
10. Polarization left empty on the gain / NF rows: the TE single-mode design is stated, the measurement polarization is not.

### Registry gaps
- `tip_thickness_nm` (fiber_chip_coupler, waveguide_platform, mode_converter): tip height of a vertically tapered inverse taper; skipped 160 nm (p.2, p.6 Fig. 4(b)). Same gap as the chrysostomidis2021 30 nm vertical taper tip.
- `dopant_concentration_cm3` (amplifier, laser): active-ion concentration (method in notes); skipped 2.2e20 ions/cm3 (p.4). Same gap as the garciablanco2025 Er concentration.
- `excited_state_lifetime_us` (amplifier, laser): upper-level lifetime of the gain medium; skipped 184 us (p.5 Fig. 3(b)).
- `min_bend_radius_um` on amplifier (spiral amplifiers): skipped 300 um (p.3). Same gap as garciablanco2025 450 um.
