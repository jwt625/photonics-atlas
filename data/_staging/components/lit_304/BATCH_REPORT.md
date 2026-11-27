# lit_304 batch report

Distilled 2026-11-27. Paper: lit:shekhar2024 (arXiv 2305.15820 v2, 40 pages; published as Nature Communications 2024,
"Roadmapping the next generation of silicon photonics"). Page-1 title matches the source row; not a correction or
erratum; `garbled_text_layer` false. Dry run `merge_component_staging.py data/_staging/components/lit_304 --dry-run`:
+0 components, +0 metrics, 0 errors.

| paper | components | metric rows |
|---|---|---|
| shekhar2024 | 0 | 0 |

## lit:shekhar2024 (perspective / roadmap, no own measurements)

No rows. The paper reports no device the authors fabricated, measured, simulated or derived for this work: no methods
section, no fabrication sentence, and the author contributions (p.23) list only writing, figure creation and editing.
Pages 23-40 are references; there is no appendix or supplement. Every quantitative statement is either credited to
cited work (rule 3, D259 / D408) or a generic technology-level statement that belongs to no specific component:

- p.2 Fig. 1 component count per PIC vs year: "adapted from [1, 2]" (cited data, D259a figure rule).
- p.4 waveguide width "400-500 nm" for silicon platforms: generic statement, no device.
- p.5 photonic wire bonds tolerating up to 30 um offset ([47] context); fiber-receptor die assembly tolerant to > 10 um
  displacement [48]: cited.
- p.5 Table 1 (modulator topologies: optical BW > 10 nm / < 0.1 nm): technology-level comparison; modulator content
  is EO-atlas scope in any case (rule 2).
- p.6 Table 2 and p.6-8 text (p-n modulators "60 GHz or even higher", Pockels > 100 GHz [57, 67-70], BTO poling ~1 V
  [65], n_BTO 2.38 / n_Si 3.47 at 1550 nm, < 350 C bonding anneal): cited or generic; modulators are EO scope.
- p.8-9 heaters "1-10 us response time"; thermal insulation > 10x power reduction [76]; folded waveguides > 100x [77];
  LC phase shifters < 1 V, nA current [78, 79]; NOEMS < 1 V, negligible IL [87]: cited or generic, no component.
- p.11 Table 3 laser-attach coupling loss (> 2 dB, 1 dB, few dB per technique): technology-level comparison table,
  not a device value. p.11 laser WPE "about 10%"; linewidth down to 1 Hz [98, 103, 104]: generic / cited.
- p.12 heterogeneous lasers "sub-dB coupling loss" ([14, 18, 19, 22] context): generic, no device.
- p.20 FMCW lasers < 100 kHz linewidth, phase shifters 10s of nW: requirements, not results.
- p.21 SiN waveguide loss 0.5 dB/m [123]: cited.
- p.22-23 conclusions (WPE > 20%, fiber-to-PIC IL < 0.5 dB): forecasts.
- p.10 Fig. 3, p.4 Fig. 2, p.16 Fig. 4: illustrative renditions, no data.

Missing fab / facility orgs: none needed (no component rows; acknowledgments p.23 list technical discussions and
grants only).

Judgment calls: none beyond treating the comparison tables (Tables 1-5) as technology-level summaries (not entered,
lit_231 fontaine2022 precedent).

Registry gaps: none.
