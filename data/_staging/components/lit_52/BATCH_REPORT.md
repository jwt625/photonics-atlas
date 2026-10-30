# Batch lit_52 report (distill subagent, 2026-10-30)

Classes: chip_chip_coupler, free_space_emitter, laser. Papers: lindenmann2012, soganc2013, cabezon2012, sun2013,
moser2011. All five sources are `restricted_local_only`, so the rows hold facts and locators only. Dry-run result:
`batch lit_52: +14 components, +91 metrics; errors 0`. The only WARN is the pre-existing one on ni2025b. The CSVs are
ASCII only and contain no e-mail, street or building text. Page-1 title and authors match the source row for all five
papers. None is a correction, an erratum or a different paper. No text layer is garbled. Not audited, not merged.

## Per paper (components / metrics)

- **lindenmann2012** (4 / 26). Photonic wire bonding (PWB) prototype, KIT.
  - `pwb_soi_soi`, class chip_chip_coupler.photonic_wire_bond.
    - Net PWB loss, normalized to an SOI reference structure (scope per_component, measured): 1.6 dB mean over
      1530-1565 nm (error bound +/-0.4 dB), and 2.5 dB mean over 1240-1580 nm (+/-1.2 dB).
    - 1-dB bandwidth > 300 nm (author_estimate, extrapolated).
    - Geometry: 60 um Si taper, 80-100 nm tip range of the chip, 500 x 220 nm Si, 2 um BOX, PWB about 2 um wide.
  - `pwb_prototypes_2_4`: three further prototypes on the same chip, 2.0 / 2.1 / 2.8 dB in the C band. Per-device
    taper lengths are not stated, so they form one population row (D165) with one metric row per prototype.
  - `pwb_transition_design` (row_kind design): the CST model. Transition loss < 0.5 dB per interface (simulated)
    for tips up to 100 nm, plus its geometry (32 um Si taper, 760 x 450 nm polymer taper start, 1.4 x 1 um PWB).
  - `soi_gc`: 1-dB bandwidth about 38 nm (author_estimate, origin not stated).
- **soganc2013** (5 / 38). Flip-chip adiabatic SOI-to-polymer couplers, IBM Research - Zurich.
  - `flipchip_3seg` (three-segment Si taper, 700 um) and `flipchip_1seg` (single taper, 800 um), class
    chip_chip_coupler.evanescent.
    - Lowest per-coupler loss within +/-2 um offset (Table 2 / Table 3): TE / TM at 1530 / 1550 / 1570 nm,
      `transition_loss_db` (dangel2018 precedent), statistic best.
    - Basis derived: the paper's Eq. (1) takes the two-coupler channel, subtracts the reference channel and the SOI
      excess loss, and halves the result (D80a).
    - FD-BPM < 0.2 dB for the three-segment design (simulated).
    - Geometry includes the polymer core 7 x 3.5 um as lower_width_nm / layer2_thickness_nm (derived from um).
  - `polymer_wg`: 0.8 dB/cm at 1550 nm, cutback, measured.
  - `polymer_fiber_facet`: SMF coupling about 1.5 dB per facet, cutback.
  - `soi_wg`: about 5.1 dB/cm, derived from the difference between two samples.
- **cabezon2012** (1 / 7). `vgc_vgc`, class chip_chip_coupler.other: two ePIXfab vertical grating couplers face to
  face between two chips.
  - About 8 dB per interface (author_estimate: it subtracts about 2 dB of propagation that rests on cited values).
  - 10.1 dB derived (24.4 - 14.3 dB), scope device_total; it includes the output-chip propagation.
  - 25 % simulated (2D-FDTD).
  - Geometry: 70 nm etch, 220 nm Si, 440 nm access waveguide, grating area about 160 um2.
- **sun2013** (3 / 14). 64 x 64 nanophotonic phased array (NPA), MIT.
  - `nanoantenna` (free_space_emitter.grating_emitter): 51 % upward emission at 1550 nm (3D FDTD, simulated), with
    3.0 x 2.8 um grating, 5 teeth, 110 nm partial first-groove etch, 220 nm Si, 2 um BOX and 3.6 um cover oxide.
  - `npa_8x8_active` (free_space_emitter.other): steering about 6 deg, vertical and horizontal (measured), 64 pixels,
    9 um pitch.
  - `doped_si_heater` (phase_shifter.thermo_optic): P_pi about 8.5 mW (measured) and 2.5 kOhm including the contacts
    (derived, kOhm -> ohm).
- **moser2011** (1 / 6). `vcsel_850_2um` (laser.vcsel; in scope: the registry laser subtypes list `vcsel`).
  Oxide-confined 850 nm VCSEL with a 2 um aperture.
  - Threshold 0.12 mA.
  - SMSR > 40 dB.
  - Relaxation resonance frequency at 0.66 / 1.2 mA and 25 / 55 C: 7.2 / 8.2 / 12.0 / 13.4 GHz.

## Values deliberately not entered

- **lindenmann2012**
  - The chip-to-chip PWB of Fig. 2(b) (about 100 um span, 25 / 12 um offsets) has geometry only, so it has no row
    (rule 9).
  - "No degradation up to 100 mW over weeks" (p.6): power_handling_dbm is not allowed for chip_chip_coupler. See
    registry gaps.
  - Error vector magnitude (EVM) and bit error ratio (BER) of the 5.25 Tbit/s transmission are link metrics, not
    entered.
  - Fig. 1(c) per-tip curves were not read.
  - TPP resist bulk absorption of 0.5-3 dB/cm is a general statement, not entered.
- **soganc2013**
  - Highest misalignment loss within +/-2 um (Tables 2-3): the values themselves are not entered (see registry gaps).
    Only the implied 1-dB tolerance is entered: tol_1db_lateral_um > 2 um (3-seg) and < 2 um (1-seg), derived, TE /
    TM rows. Check this call.
  - Fig. 8 offset curves were not read.
  - Fiber-to-fiber totals (5.2 / 5.0 / 3.2 dB) are in notes.
  - Temperature insensitivity to 70 C has no parameter.
  - Cited values not entered: material loss 0.6 dB/cm [30] and the thermal-shock test [31].
- **cabezon2012**
  - 3-dB lateral (about 3 um) and longitudinal (8 um) tolerances: no parameter, D81 / D250 defer 3-dB tolerances.
  - Vertical period of about 0.8 um: not entered.
  - System spectrum (3-dB lobes 1544-1557 nm, 4 dB dip at 1552 nm): it includes two fiber-VGC couplers, so it is not
    entered.
  - Fiber-to-VGC about 5 dB and taper 0.2 dB are cited. The about 4 dB VGC-to-MMF estimate is computed from cited
    values (rule 3).
  - VGC period 630 nm and 25 periods: period_nm / n_periods are not allowed for chip_chip_coupler. See registry gaps.
  - No separate fiber_chip_coupler.grating row: it has no clean own performance value.
- **sun2013**
  - The passive 64 x 64 and 32 x 32 arrays have no row. Their only number is the emission uniformity
    (sigma / mu = 13 %, Fig. 3(d)), and no parameter exists for it.
  - Supp. Figs. 1-4 are not cached.
  - No emission angle is printed.
- **moser2011**
  - No parameter yet (see registry gaps): differential quantum efficiency 28.3 / 22.2 %, dissipated power, D-factor
    12.0 GHz/mA^0.5, K-factor 0.42 ns (abstract 0.41 ns, conflict noted), damping offset 8.1 GHz, energy-to-data
    ratio (EDR) and heat-to-bit-rate ratio (HBR) in fJ/bit.
  - 850 nm is nominal, so no center_wavelength_nm row.
  - S21 3-dB bandwidth and L-I powers are not printed (figure only), not read.
  - Table I values of other groups are not entered.

## Fab / facility orgs

| paper | org as printed | locator | status |
|---|---|---|---|
| lindenmann2012 | European silicon photonics platform ePIXfab (SOI waveguide fabrication) | p.11 Acknowledgments | missing from the registry. MPW / fab role (D398) on `pwb_soi_soi`, `pwb_prototypes_2_4`, `soi_gc` |
| cabezon2012 | ePIXfab (standard SOI technology; SOI MPW services acknowledged) | p.1 Sec. 1; p.5 Acknowledgments | missing. Fab role (D398) on `vgc_vgc` |

Entered:

- lindenmann2012 PWB rows: org_karlsruhe_institute_of_technology ("we fabricated PWB interconnects", all authors
  KIT).
- soganc2013 coupler, polymer waveguide and fiber facet rows: org_ibm_research_zurich ("we fabricated single-mode
  polymer waveguides ... established a flip-chip bonding process", all authors IBM Zurich; D399 for the assembled
  coupler).

Left empty:

- soganc2013 SOI waveguide: passive voice, and the thanks go to an individual.
- sun2013: the 300-mm CMOS foundry is not named; APIC Corporation is thanked without a fabrication statement.
- moser2011: no fabrication statement, and the authors sit at two orgs (TU Berlin, VI Systems GmbH).
- KNMF (lindenmann2012) appears only in the funding list, so it is not a facility (D83e).

## Judgment calls

1. **lindenmann2012 class.** The measured PWB links two SOI waveguides on the same chip. I kept
   chip_chip_coupler.photonic_wire_bond because the paper presents it as the chip-to-chip PWB demonstration, and the
   Fig. 2(b) chip-to-chip bond is the same technology without its own data. The alternative is
   waveguide_platform.transition / other. Scope per_component: one PWB link with both transitions, reference
   normalized.
2. **soganc2013 parameter.** transition_loss_db per_component follows the dangel2018 precedent (same group, same
   device type). insertion_loss_db per_interface would also fit. Basis derived because the paper's Eq. (1) halves and
   subtracts (D80a).
3. **soganc2013 tolerance.** The 1-dB lateral tolerance is inferred from "highest misalignment loss within +/-2 um"
   (derived, gt / lt 2 um). If the auditor prefers no inference, delete these 4 rows and keep the values for the
   registry gap below.
4. **soganc2013 fiber facet per_facet.** Supported by the Table 1 term structure and by an arithmetic check against
   the 3.2 dB reference channel. The wavelength (1550 nm) is inferred from the same sentence.
5. **cabezon2012.**
   - Two loss rows: the 8 dB printed estimate (author_estimate) and the 10.1 dB derived difference, which includes
     output-chip propagation (device_total).
   - C band is wavelength_inferred because no wavelength is stated for the laser measurement or the simulation; the
     only band measured is the C-band spectrum (Fig. 8).
6. **sun2013.**
   - The antenna row is `fabricated` with only simulated performance plus geometry (D80e).
   - cladding_thickness_um 3.6 is the "total" cover-oxide thickness, and its reference plane is not stated (noted).
   - The steering and P_pi wavelength is inferred from the 1.55 um laser of the passive measurement.
7. **moser2011.** The threshold temperature is not stated, so temperature_k is left empty and the reason is in the
   notes.

## Registry gaps (proposed definition; skipped value + locator)

| proposed parameter | class | skipped values | definition |
|---|---|---|---|
| power_handling_dbm (widen) | chip_chip_coupler | lindenmann2012 up to 100 mW (20 dBm) over several weeks, no degradation (p.6 Sec. 4) | existing def |
| misalignment_loss_db | chip_chip_coupler, fiber_chip_coupler | soganc2013 highest loss within +/-2 um: 3-seg TE 0.9 / 0.6 / 0.6, TM 0.7 / 0.3 / 0.3; 1-seg TE 2.8 / 2.6 / 2.2, TM 2.3 / 2.0 / 2.0 dB at 1530 / 1550 / 1570 nm (p.10 Tables 2-3) | excess loss at the stated misalignment (offset and axis in condition), positive dB |
| period_nm, n_periods (widen) | chip_chip_coupler | cabezon2012 VGC period 630 nm, 25 periods (p.2 Sec. 2) | existing defs |
| emission_uniformity_pct | free_space_emitter | sun2013 sigma / mu = 13 % over 4,096 pixels (p.3 Fig. 3(d)) | std / mean of the per-element emitted intensity (std / mean definition in condition) |
| differential_quantum_efficiency_pct | laser | moser2011 28.3 % (25 C), 22.2 % (55 C) from the L-I slope (p.3) | already confirmed in the lit_35 audit (fang2006) |
| d_factor_ghz_per_sqrt_ma, k_factor_ns, damping_offset_ghz | laser | moser2011 12.0 GHz/mA^0.5, 0.42 ns (abstract 0.41 ns), 8.1 GHz (p.3 Fig. 2(b); p.2 abstract) | standard small-signal laser figures of merit (D-factor = dfr / dsqrt(I - Ith); K-factor from damping vs fr^2; damping offset gamma_0) |
| energy_per_bit_fj | laser | moser2011 EDR 83 fJ/bit (25 C) / 81 fJ/bit (55 C) at 17 Gb/s; 117 fJ/bit at 25 Gb/s; HBR 69 / 99 fJ/bit (p.2 Abstract, p.4) | electrical energy per transmitted bit at the stated bit rate (total vs dissipated in condition) |
| dissipated_power_mw | laser | moser2011 1.18 mW at 0.66 mA, 2.47 mW at 1.2 mA (25 C), 1.21 mW at 0.66 mA (55 C) (p.3) | electrical minus optical output power at the stated current |

## Top open questions

1. ePIXfab registry row (lindenmann2012, cabezon2012). With it added, set fab_org_ids on 4 rows. lindenmann2012:
   KIT + ePIXfab on the PWB rows, ePIXfab on the GC. cabezon2012: ePIXfab.
2. lindenmann2012: chip_chip_coupler for a same-chip PWB link (call 1)?
3. soganc2013: keep the derived 1-dB tolerance rows (call 3), or move the values to a misalignment_loss_db extension?
