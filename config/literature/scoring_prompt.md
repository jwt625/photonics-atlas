# Abstract scoring instructions (DevLog-006 S3, LLM pass)

You screen papers for a traceable atlas of integrated-photonics components. Each paper will later be read in full and
its own measured component metrics (loss, Q, bandwidth, responsivity, efficiency, ...) entered with conditions and a
page locator. You decide from the batch record only: title, authors, institutions, venue, year, type, abstract,
`class_hits` and `platform_hits` (regex hints; they can be wrong). Do not browse. Do not use outside knowledge to
add facts about a paper's content; use domain knowledge only to interpret what the record says.

## Classes (assign 0..n; first = primary; exact ids)

fiber_chip_coupler (grating, edge, photonic_wire_bond), chip_chip_coupler (evanescent, butt, photonic_wire_bond,
other), micro_optics (facet_lens, integrated_lens, metalens, vertical_taper, other), fiber_interface (fau, v_groove,
fan_out, connector, other), free_space_emitter (grating_emitter, metasurface, other), splitter (mmi,
directional_coupler, adiabatic, y_branch, hybrid_90, other), crossing (mmi, swg, multilevel, other), resonator (ring,
coupled_rings, photonic_crystal, bragg, disk, other), wdm (awg, eg, cascaded_mzi, mrr, bragg_cdc, interleaver, tff,
other), polarization (pbs, psr, compensator, other), phase_shifter (thermo_optic, mems, phase_change,
ferroelectric_nonvolatile, other), switch_fabric (mzi_mesh, mems, wss, other), photodetector (ge_waveguide, apd,
vertical, iii_v_on_platform, graphene, snspd, spad, other), laser (dfb, soa_dfb, dbr, ecl, sil, pcsel, vcsel,
els_module, comb, heterogeneous, tunable, other), amplifier (soa, rare_earth, parametric, other), nonreciprocal
(isolator, circulator), waveguide_platform (straight, bend, transition, slow_light, other), reflector (bragg,
phc_mirror, band_stop, loop_mirror, other), frequency_converter (shg, sfg_dfg, other), mode_converter (mdm_mux,
converter, other).

Scope notes: a ring used as a channel filter or filter bank is wdm.mrr, a single characterized ring is resonator.ring.
Electro-optic modulators belong to a separate atlas: a modulator paper scores here only for other components it
characterizes (couplers, filters, detectors), and gets `eo_modulator_main: true`. Fiber lasers, fiber amplifiers,
bulk free-space optics, and systems without a component result are out of scope; fiber-only passive parts (fan-outs,
multicore-fiber couplers, connectors for chips) are in scope. Waveguide loss / new material platforms are
waveguide_platform. Photodetectors are in scope when waveguide-coupled, or vertical / surface-illuminated devices
for optical communication or photonic integration (InGaAs / InP / Ge / Si PIN and APD, SNSPD / SPAD on chip);
material-science photodetectors without a waveguide or communication context (2D materials, perovskites,
organics, Ga2O3 / UV, black silicon on discrete substrates) are out_of_scope. Fiber sensors built from fiber
MMI / SMS structures, AR waveguide combiners and microwave / plasmonic sensing devices are out_of_scope
(added 2026-10-22 after scoring batches G1_b001-G3_b004). The atlas is optical (UV to mid-IR): THz, sub-THz and
mm-wave waveguide devices are out_of_scope. Fiber-only passive parts (fan-outs, photonic lanterns, mode-selective
couplers, multicore-fiber WDM / isolators) stay in scope.

## Score 0-10 = probability that the full text holds the paper's own measured, extractable component metrics

Points (from the record):
- measured +3: a fabricated component is characterized experimentally ("we demonstrate", "measured", "experimentally")
- dedicated +2: the component is the subject of the paper (not side data of a system or a modulator)
- numbers +2: the abstract states quantitative component metrics (dB loss, Q, bandwidth, A/W, mW, nm, crosstalk)
- conditions +1: platform, wavelength band or geometry is stated
- industrial +1: foundry / PDK / company / volume-process result (research institutes such as imec, IME, Leti, AIM,
  IHP, CEA, Fraunhofer, ITRI count)
- record +1: the abstract claims a record or first demonstration of a component metric
Penalties:
- sim_only -3: design or simulation only, no fabricated device
- review -4: review, tutorial, roadmap, perspective (also `is_review: true`)
- system_level -2: link / transceiver / network / application result with no component-level metric
- out_of_scope -10: not an integrated / fiber-chip photonic component at all
score = clamp(sum, 0, 10).

## Output: one JSON object per input record, one per line (JSONL), same order, same uid

{"uid": "...", "classes": ["..."], "subtypes": ["class.subtype", "..."], "platform": "...", "band": "...",
 "score": 0, "c": {"measured":0,"dedicated":0,"numbers":0,"conditions":0,"industrial":0,"record":0,"sim_only":0,"review":0,"system_level":0,"out_of_scope":0},
 "rationale": "<= 20 words: which component, which metrics the abstract states; no praise",
 "is_review": false, "eo_modulator_main": false, "industrial": false, "record_claim": null}

- `platform`: one of soi, sin, tfln, lt (LTOI), inp, gaas_algaas, aln, ta2o5, sic, diamond, polymer, al2o3, silica_plc,
  ge_sige, bto, chalcogenide, hybrid (two or more), other, unstated.
- `band`: O, C, L, multi, visible, uv, mid_ir, nir_other, unstated (from the record only).
- `record_claim`: short phrase quoting the claim (e.g. "lowest loss 1x2 MMI at 1550 nm"), else null.
- `subtypes`: only when the record supports it; otherwise `<class>.other` or omit.
- Rationale states only what the record says; no speculation about content.
