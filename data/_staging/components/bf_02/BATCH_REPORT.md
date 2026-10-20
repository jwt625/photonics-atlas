# Batch report bf_02 (2026-10-20)

Transcribed by the coordinator. Dry-run 0 errors: 16 components, 33 metrics. qiu2026a: no rows.

Incident: the shared scratchpad let this agent run bf_05's build.py once (13:26), writing header-only CSVs into bf_05; bf_05's own build rewrote them at 13:27. Later batches use private scratch subfolders.

- guo2026 (4/13): TFLT GC at 532 nm (4.5 dB loopback_half measured), 0.4 / 1.0 um ridge waveguides, Ti TOPS. Not entered: 1.5 um waveguide loss (EO row 1.7 dB/cm), 3.5 dB per coupler (same simulation as the 45 %), MMI / bend / taper (no metric), TFLN comparison modulator and MZM ER (EO). Sidewall 60 deg design_target (method not stated). GC not linked to guo2026-b.
- bankwitz2026 (1/4): foundry-PDK 2x2 DC: fitted bar-port ratios 27 / 71 / 80 % (derived), stated mean 75 % (n = 3, std 4 %); band inferred. Not entered: InP DFB seed (vendor typical, setup), fiber amplifier, SNSPD (setup), GCs (no value). Foundry unnamed.
- kharel2021 (1/1): GC on quartz-handle TFLN 6 dB per facet at 1560 nm (per_coupler, loss_breakdown, author_estimate). fab_org_ids = org_hyperlight (all authors HyperLight, "we fabricated"). Not entered: EO-row losses, RF electrode data.
- murai2025 (1/1): MMI 0.1 dB simulated excess. Not entered: 0.7 dB/cm (EO), 0.1 dB Si-TFLN transition (prospective, cited), 0.5 um alignment (cited).
- qiu2026a (0): BTO DC phase shifters "< 5 mW combined" (Pockels, total), EC fiber-to-fiber loss in EO row, ITLA / amplifiers setup.
- vanackere2023 (3/7): printed LN-coupon taper transition 2.7 dB measured and 0.25 dB simulated per coupon (two tapers + 2 mm hybrid section; insertion_loss_db per_component), taper 45 um, tip 200 nm design / ~300 nm SEM; SiN 1x2 MMI 0.3 dB excess (cascade, derived); SiN GC 9 dB (18 dB for both halved, derived). Not entered: 1.8 dB abrupt transition (cited ref. 45), 9.5 nm FSR (modulator).
- lu2020 (2/2): Y-junction pair ~1.4 dB device_total; lensed-fiber facet ~3 dB per facet; both author_estimate, 1550 nm inferred; from Supplementary Note 5 (supplement/text.md). Not entered: 0.22 dB/mm (EO).
- li2026 (1/1): LTOI inverse-taper EC typical fiber-to-fiber 5.2 dB (printed -5.2); facilities EPFL CMi + Institute of Physics cleanroom. Not entered: MMI (no value), HHI PD (setup).
- taghavi2026 (2/2): AMF GC ~10.5 dB per coupler (measured), hosts taghavi2026-a/-b, fab org_amf; photonic wire bond fiber array -> on-chip EC ~12 dB mean per channel (fiber_chip_coupler.edge for now). Not entered: 2 dB potential (cited ref. 57), ring values (EO).
- lee2020 (1/1): Si3N4 inverse-taper EC 10-12 dB per facet (range), L band inferred from the 1586.2 nm resonance; facilities CUNY ASRC NanoFab, Columbia Nano Initiative. Not entered: ring values (EO), simulated mode losses.

Gaps: fiber_chip_coupler.photonic_wire_bond subtype; tuning_power_mw for phase_shifter (aggregate, scope in condition); platform si_polymer_hybrid.
Decision asked: authors' company fabrication ("we fabricated", all HyperLight) -> fab_org_ids. Coordinator: adopted for contract v3 (authors' org when the paper states the authors fabricated it and that org is unambiguous).
