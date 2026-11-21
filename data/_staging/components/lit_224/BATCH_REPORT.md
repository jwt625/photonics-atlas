# lit_224 batch report

Papers: lit:huang2016c, lit:vandekerckhove2023. Page-1 titles match the source rows. verified_on 2026-11-20.
Dry run: `merge_component_staging.py data/_staging/components/lit_224 --dry-run`: +3 components, +14 metrics, 0 errors.

## lit:huang2016c (JSTQE 2016, electrically driven Ce:YIG/Si microring isolator)

Components 2 / metric rows 10.

- `cmp_lit_huang2016c_ring_isolator_r35` (nonreciprocal.isolator, soi, 9 rows): isolation 32 dB near 1555 nm at
  +/-80 mA (measured, p.5 Fig. 8); isolation > 20 dB over the 0.6 nm thermal tuning (measured; span endpoints
  1555.25-1555.85 nm read off the Fig. 9 inset); isolation_bw_nm 0.0097 (derived from the printed 1.2 GHz 10-dB
  bandwidth at 1555 nm, D256); excess loss 2.3 dB per isolator (per_component, loss_breakdown, author_estimate);
  10 dB device loss vs Si reference waveguide (de_embedded, reference_structure, measured; wavelength inferred);
  simulated isolation > 20 dB for a 15 % gap deviation (Fig. 3(c)); width 600 nm, Si 230 nm, BOX 1 um (design_target).
- `cmp_lit_huang2016c_ceyig_bond_interface` (waveguide_platform.transition, soi, 1 row): 1.2 dB FDTD scattering loss
  at the silica-clad / Ce:YIG-bonded interfaces (simulated, device_total).

Not entered, and why:
- Electrical power 9.6 mW at +/-80 mA (1.5 ohm measured microstrip resistance, p.5): no power parameter for
  nonreciprocal (registry gap).
- 0.6 nm thermal tuning range (p.6): tuning_range_nm not allowed for nonreciprocal (registry gap); the > 20 dB
  isolation over it is entered.
- MO resonance split 0.16 nm at 80 mA (p.5), saturation 0.36 nm (p.6), simulated maximum 0.52 nm (p.3): no
  parameter (registry gap).
- Calculated thermal shift 0.0716 nm/C for TM (p.3, Table I): thermal_drift_pm_per_k not allowed for nonreciprocal.
- Ring radius 35 um, design gap about 245 nm, critical power coupling about 11.68 % (p.3): radius_um / gap_nm /
  power_coupling_pct not allowed for nonreciprocal (huang2016 precedent noted the same gap). No resonator.ring row
  made: the ring is characterized only as the isolator (no Q, FSR or extinction printed).
- SGGG thinned to about 5 um (separately measured, 1-2 um variation, p.4); Ti 22 nm / Au 1.5 um microstrip;
  Ce:YIG 400 nm: in core_material only (no allowed layer parameter for nonreciprocal).
- Material values (Ce:YIG loss about 60 dB/cm, Faraday rotation -4500 deg/cm, dtheta_F/dT from ref. [26]):
  material properties / cited input, not component metrics.
- Fig. 1 comparison points of other works (rule 3); Appendix Fig. 11 (100 mA, off critical coupling) has no
  printed number; hysteresis offset about 0.03 nm (p.6) and the 250 mA damage threshold kept in notes.

Missing fab / facility orgs: none. Fabrication is described with passive sentences (p.4 Sec. III), fab empty
(D80b). No facility acknowledged; "Center for Scientific Computing at UCSB" (p.1 funding note) is computing support,
not a fabrication facility.

## lit:vandekerckhove2023 (CLEO/Europe-EQEC 2023, 1-page abstract, transfer-printed PPLN on SiN)

Components 1 / metric rows 4.

- `cmp_lit_vandekerckhove2023_ppln_sin_shg_1mm` (frequency_converter.shg, lnoi_loaded_sin): normalized efficiency
  2500 %/W/cm2 at 1620 nm (author_estimate, see judgment call 1); poling period 3.5 um (electrode period,
  design_target); slab length 1000 um (derived from 1 mm); LN film 300 nm (design_target, D402).

Not entered, and why: SHG spectral bandwidth (no printed value, no frequency_converter bandwidth parameter);
Fig. 1(d) inset powers (no printed values); SiN waveguide thickness and width (not stated); the comparison with
etched LNOI (ref. [2], rule 3).

Missing fab / facility orgs: none. Passive process description (p.1), no acknowledgment section: fab empty (D80b).

## Judgment calls for the auditor

1. vandekerckhove2023 2500 %/W/cm2: the abstract says "measured" from on-chip powers but does not state how the
   coupling losses were obtained; entered `author_estimate` (origin not stated; lukin2019 / zhao2020 precedent).
   The later journal version of this work (lit:vandekerckhove2025, merged) prints the same 2500 %/W/cm2 as
   measured with measured coupling losses; that paper was not used here (rule 1). Alternative: `measured`.
2. huang2016c 1.2 dB interface loss: the paper prints one simulated value for "the interfaces" (plural); entered
   as printed with scope `device_total` instead of halving to a per-interface value (the interface count is only
   implied by the Fig. 2(a) schematic). Alternatives: 0.6 dB per interface (simulated, D83f), or drop the
   transition row and keep the value in the isolator notes.
3. huang2016c 2.3 dB excess loss: `author_estimate` (rests on the simulated 1.2 dB and the eight-isolator
   equivalent-length assumption) although the abstract uses "measure"; scope per_component.
4. huang2016c 10 dB device loss: wavelength not printed with the value; 1555 nm inferred from the Fig. 8 comparison
   with the Si reference trace.
5. huang2016c > 20 dB over the tuning range: value and 0.6 nm span printed; endpoints 1555.25-1555.85 nm read off
   the Fig. 9 inset (+/- 0.05 nm), basis kept `measured`.
6. vandekerckhove2023 platform `lnoi_loaded_sin` follows lit:vandekerckhove2025 / niels2025a for LN printed on top
   of a SiN strip (SiN guides under the LN).

## Registry gaps

- nonreciprocal: `tuning_range_nm` (huang2016c 0.6 nm, p.6), `power_consumption_w` or a mW drive-power parameter
  (9.6 mW, p.5), `thermal_drift_pm_per_k` (0.0716 nm/C calculated, p.3), `radius_um` / `gap_nm` (35 um, about
  245 nm, p.3), and a nonreciprocal resonance-split parameter, e.g. `nonreciprocal_split_nm` = measured CW / CCW
  resonance wavelength split (0.16 nm at 80 mA p.5; 0.36 nm saturated p.6).
- frequency_converter: a phase-matching bandwidth parameter (no printed value in this batch; proposed earlier with
  vandekerckhove2025).
