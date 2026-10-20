---
title: Fresh-context audit of the P1 component pilot (pilot_1 + pilot_2)
date: 2026-10-20
scope: data/_staging/components/pilot_1, pilot_2 vs the 10 papers (EO atlas text and figures)
mode: read-only subagent; report condensed by the coordinator
---

# P1 pilot audit (2026-10-20)

All 146 metric rows and 38 component rows checked at their locators; figure images opened for every figure-derived value; all 10 papers read end to end for misses. Machine checks: host_device_id in EO devices.csv, source ids, parameter-class and units: 0 errors.

## Counts

- Metric rows: 146 checked, 0 wrong values / units / qualifiers, 24 imprecise (convention: scope, basis, parameter choice), 0 unverifiable.
- Component rows: 38 checked, 1 wrong (wu2025 VAC note says the TFLN is not patterned; the paper says no fine patterning and the TFLN waveguide is 1.5 um wide), ~17 imprecise (platform 12, fab org 5).
- Misses: 1 real (berman2026 p.9 Methods: typical fiber-to-fiber loss ~12 dB with lensed fibers, all devices), 2 to list as not entered (berman2026 Fig. 4(g) Q ~7k / 14k unidentified devices; didier2026 Fig. 3(c) loss vs electrode gap).

## Main findings by paper

- valdez2023: MMI 0.2 dB and LN-edge 0.1 dB terms are of unstated origin (basis should be author_estimate, not derived); LN-edge value split into c_band / o_band rows invents band specificity; MMI location contradiction p.3 vs p.11 not noted; lensed-fiber spot size is a vendor specification.
- li2026aa: UHNA4 MFDs are datasheet values (specification); splitter cascade is a reference structure, scope per_component. Batch report wrongly calls the fab facility CAS (it is the HUST WNLO facility; data correct).
- kohli2025: a-Si GC and converters were processed by the authors (LIGENTEC made the SiN wafers, Lumiphase grew the BTO): fab orgs imprecise; BRNC generic thanks correctly excluded.
- berman2026: band-stop PhC is a reflector, not a resonator; period set 415/425/430 discrete; 12 dB fiber-to-fiber miss.
- li2022b: ok (loopback_half for a GC pair).
- li2025b: GC pair halved scoped per_coupler (should be loopback_half, as in pilot_1); 889 um is the test-pair spacing, not a pitch; platform algaas copied from EO where suspended_gaas fits.
- hulyal2026: ok.
- liu2026d: per-facet values from test structures are measured (the paper says both "estimated" and "measured"); MMI "IL per coupler" ~1.5 dB is excess loss, per_component; platform should be a TFLN strip value (fully etched), EO rows share the issue.
- wu2025: VAC 0.11 dB should use transition_loss_db (as the Si-SiN transition and kohli2025); VAC note wrong; PD pre/post-bonding not stated for 55 nA and 47 / 56 GHz.
- didier2026: BRNC / FIRST / IBM Research Zurich come from one acknowledgment of fabrication support (facility-level; IBM omitted); cladding "air" not stated.

## Contract recommendations (adopted unless noted in DevLog-002)

Per-component scope; loopback_half rule; host list validated against EO devices; basis rules (direct test-structure measurement = measured, arithmetic on own measurements = derived, any assumed or cited input or unstated origin = author_estimate); `specification` basis for datasheet values; fab vs facility org columns; inferred-wavelength flag; platform = stack guiding light in the component, add a TFLN strip value; transition_loss_db for every on-chip inter-layer transition and taper/tip/gap geometry for transitions; reflector class; finesse, n_periods, linewidth_pm, slab_thickness_nm, sidewall_angle_deg, bw3db_khz, heater_resistance_ohm, heater_gap_um, tuning_range_nm; crosstalk_db for wdm with type in condition; statistic `typical`; duplicate check including band / statistic / condition; a component needs at least one performance metric. Rejected: PD parameters for off-chip setup equipment (not a PIC component), rib_height_nm, port_separation_um.

## EO atlas follow-ups (read-only here)

liu2026d-* waveguide_platform lnoi_rib (paper: fully etched strip); li2025b-* algaas (suspended GaAs).
