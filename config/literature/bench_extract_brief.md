# Benchmark-citation extraction brief (DevLog-019, B2)

You read prefilter packets of cached photonics papers and record the other works that each paper's comparison table
or trend / benchmark plot cites. Local reads only: no web access, no downloads, no edits outside your output file.

## Input

A batch file lists packet paths (one per line, relative to the repo root). Each packet (`cache/literature/bench/packets/<corpus>__<id>.md`)
holds candidate regions (text lines of a table or a figure caption, with a page render path for lit / EO papers) and
either the parsed reference entries the regions cite or the raw reference section. The full text file path is on
line 2 of the packet; read more of it (Read with offset / limit) only when a table is cut off or the reference
section is missing from the packet.

## What counts (D1200)

A benchmark item is a table or figure that sets values of OTHER works (with reference tags) next to each other or
next to this paper's result: comparison / state-of-the-art tables, summary tables in reviews, trend / evolution plots,
scatter plots of reported devices. Not: tables of this paper's own designs, simulation-vs-measurement figures, setup
or process tables, figures merely "adapted from [n]", text-only mentions outside a table / figure.

Many regions are false positives; reject them silently (status line only). For a figure, open the page render (Read
on the PNG) only when the caption says it compares or plots other works; read the reference tags from the legend or
point labels. If the plot labels points by author / year instead of tags, map them to the reference list by author
and year; if a label cannot be mapped, record it with `ref_num: null` and the label text.

## Output

Write JSONL to the output path given in your task, one object per line, two record types:

1. One `item` per accepted benchmark row (one cited work in one table / figure):
```json
{"type": "item", "citing": "lit:abe2025", "region": 2, "kind": "table|figure", "locator": "Table 2, p.5",
 "topic": "SiN AWG demultiplexers", "class": "wdm.awg", "ref_num": 6,
 "ref": "C. R. Doerr and K. Okamoto, \"Advances in silica planar lightwave circuits,\" J. Lightwave Technol. 24(12), 4763-4789 (2006).",
 "row_label": "SiO2 WG [6]", "platform": "silica PLC",
 "values": [{"metric": "adjacent crosstalk", "value": "~-40", "unit": "dB"}, {"metric": "on-chip loss", "value": "0.75", "unit": "dB"}]}
```
2. One `paper` status line per packet:
```json
{"type": "paper", "citing": "lit:abe2025", "status": "ok|no_benchmark|refs_missing", "n_items": 7, "note": ""}
```

Field rules:

- `citing`: `<corpus>:<id>` from the packet header (`lit:`, `eo:`, `ofc2026:`).
- `ref`: the reference entry as printed in the paper's list, cleaned of line-break hyphens; one entry only (split
  "[3]-[5]" into three items). If the entry is missing from the packet and the text file, `ref: ""` and status
  `refs_missing`. Keep DOIs / arXiv ids when the entry prints them.
- `class`: one of the atlas class keys `family.subtype` below; `modulator.<type>` for electro-optic / electro-absorption
  modulators (mzm, ring, eam, other); `out_of_scope.<short>` for non-component content (DSP, transmission systems,
  fiber spans, sensors, networking, ML). Use the class of the cited work's device, not of the citing paper.
- `values`: the cited row's numbers exactly as printed (with "~", "<", ranges); metric names as in the column header;
  for plots, read values only when points are labelled or clearly on a grid, else `[]`. Skip rows for "this work".
- `topic`: <= 8 words, plain words.
- No addresses, no prose copied from the paper beyond the reference entry and the row label / column headers.

Atlas class keys: fiber_chip_coupler.{grating, edge, photonic_wire_bond, other}; chip_chip_coupler.{evanescent, butt,
photonic_wire_bond, other}; micro_optics.{facet_lens, integrated_lens, metalens, vertical_taper, other};
fiber_interface.{fau, v_groove, fan_out, connector, other}; free_space_emitter.{grating_emitter, metasurface, other};
splitter.{mmi, directional_coupler, adiabatic, y_branch, hybrid_90, other}; crossing.{mmi, swg, multilevel, other};
resonator.{ring, coupled_rings, photonic_crystal, bragg, disk, other}; wdm.{awg, eg, cascaded_mzi, mrr, bragg_cdc,
interleaver, tff, other}; polarization.{pbs, psr, compensator, other}; phase_shifter.{thermo_optic, mems,
phase_change, ferroelectric_nonvolatile, other}; switch_fabric.{mzi_mesh, mems, wss, other};
photodetector.{ge_waveguide, apd, vertical, iii_v_on_platform, graphene, snspd, spad, other}; laser.{dfb, soa_dfb,
dbr, ecl, sil, pcsel, vcsel, els_module, comb, heterogeneous, tunable, other}; amplifier.{soa, rare_earth,
parametric, other}; nonreciprocal.{isolator, circulator, other}; waveguide_platform.{straight, bend, transition,
slow_light, other}; reflector.{bragg, phc_mirror, band_stop, loop_mirror, other}; frequency_converter.{shg, sfg_dfg,
other}; mode_converter.{mdm_mux, converter, other}.

Pilot rules (2026-11-15):

- Region windows are cut by line counts; if a table runs past the window, read the rest from the text file. If you
  find a benchmark table or figure outside the packet regions, record it with `region: null` and its locator.
- A table may exist only in the page render (text layer empty): read it from the PNG.
- Trend plots whose points are unlabelled but whose caption, legend or describing sentence lists the plotted works'
  reference tags (e.g. "EBL [3-8], DUV [9-14]"): one item per listed reference, `values: []`, note `caption_refs`.
  Only when no tags at all can be tied to the plot: no items, note `unlabelled_plot` (status `no_benchmark` unless
  other regions yield items).
- Parsed reference entries can be wrong (appendix paragraphs numbered 1-3, page footers, author bios appended):
  check each entry looks bibliographic; take the right entry from the text file; strip footer / bio text.
- Whole PICs, transceivers or subsystems (WDM receiver chip, coherent transmitter) -> `out_of_scope.pic`; fibers and
  fiber amplifiers / gain fibers -> `out_of_scope.fiber`.
- Cells printed as not reported ("/", "-", "—", "N/A") are left out of `values`; `platform` is "" when not printed.

## Final reply

Return only: packets done, items written, papers with status ok / no_benchmark / refs_missing, and any packet you
could not process with the reason. Do not paste items into the reply.
