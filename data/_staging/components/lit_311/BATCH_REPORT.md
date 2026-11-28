# lit_311 batch report

Distilled 2026-11-28. Paper: lit:winzer2018.
Result: 0 components, 0 metric rows (header-only `components.csv` / `component_metrics.csv`; empty batch, valid
outcome for a review). `merge_component_staging.py data/_staging/components/lit_311 --dry-run`: 0 errors (2 warnings,
both on merged rows of other batches: guo2024a, ni2025b). No helper script needed.

## lit:winzer2018 (Optics Express 26(18), 2018, invited review, 50 pages)

Page-1 title matches the source row ("Fiber-optic transmission and networking: the previous 20 and the next 20
years [Invited]"); not a correction / erratum; `garbled_text_layer` false, but pp.29-31 and p.40 are multi-column
extractions with broken lines: read on the page renders (`figures/page_29.png`, `page_40.png`); nothing component-level
there. pp.1-10 are the reference list (234 refs); main text pp.10-49.

Components 0 / metrics 0. The paper is a system / network review with no device of its own: no fabricated or
characterized component, no measurement section, no first-person device result. Every quantitative device-level
statement is cited, generic or a system-level projection.

Values not entered and why:
- Fiber values: SSMF CD 17 ps/nm/km at 1.55 um (p.14 Sec. 2.2.1, generic); modern fiber "just over 0.14 dB/km",
  ~20 ps/km.nm (p.23 Sec. 2.3.2, cited refs. [124-126], rule 3); Fig. 17 commercial SMF loss window 1260-1625 nm and
  hollow-core loss predictions (p.38-39; hollow-core curves redrawn from ref. [200], rule 3; the SMF curve is a
  "typical" commercial-fiber curve with origin not stated, and transmission fiber is not a component class in scope,
  D411).
- 100-nm / 13 THz SOA bandwidth (p.39 Sec. 3.3): cited, ref. [15] (rule 3).
- WSS / ROADM: "typical" 40-GHz 0.5-dB passbands on a 50-GHz grid, 5-GHz spectral resolution (p.44 Sec. 3.5),
  high-port-count (e.g. 20) WSS, 1x(D+P) port counts, DxT = 8x16 MCS (p.33 Sec. 2.3.7, architecture description
  citing ref. [163]), LCoS WSS principle (ref. [171]); generic industry values, no device measured (rule 1 / 3).
- PXC bandwidth 1270-1650 nm "today" (p.47 Sec. 3.5): generic commercial statement, no device, no source (rule 1).
- Clos cross-connect sizes (625x1250, 10x10, 125x250, 50x50; p.47), required WSS counts (176 1x440, 5000 1x125000;
  p.45), Table 2 symbol rates / capacities (p.39), Fig. 24 WSS resolution vs superchannel count (p.46): design
  projections / architecture arithmetic, not components (no row; not a design-only component either).
- Transmission-system records (Table 1 p.12, Figs. 1-2, 7-9: interface rates, capacities, SE, reach), transponder
  rates, ADC/DAC bus arithmetic (p.25), data-center floor-area study (Fig. 14, pp.35-36), traffic growth (Fig. 13):
  system / market data, out of component scope.
- Fig. 3-4, 6, 10-12, 15-16, 18-23, 25: conceptual diagrams or figures "after" earlier work (refs. [1], [27], [157],
  [197], [198]; D259 / D408).

Missing fab / facility orgs: none (no component; acknowledgment p.50 thanks individuals for data and discussions
only, no facility).

Judgment calls:
- No design-only rows: the paper's switch-node and Clos scaling (Sec. 3.5) are architecture sizing, not a component
  design with stated performance, so `row_kind: design` does not apply.

Registry gaps: none.
