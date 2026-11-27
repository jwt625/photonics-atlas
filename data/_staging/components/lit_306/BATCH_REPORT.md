# lit_306 batch report

Distilled 2026-11-27. Papers: lit:shastri2021, lit:wang2019. Result: 0 component rows, 0 metric rows (header-only
CSVs). Page-1 titles match the source rows for both papers; neither cached file is a correction / erratum. Both cached
texts are the arXiv versions of the listed Nature Photonics reviews (shastri2021 arXiv 2011.00111 v2, wang2019 arXiv
2005.01948 v1); only the preprint was read, journal versions unread.

## lit:shastri2021 (Nature Photonics 2021 review, photonics for AI / neuromorphic computing)

Components: 0. Metric rows: 0.

Values not entered and why:
- Every device value in the text carries a citation: LNOI modulators up to 110 GHz (ref. [128]) and < 0.5 dB on-chip
  loss / 210 Gb/s (ref. [129]), p.9; 2-bit photonic DACs with an MRR modulator at 128 Gb/s (ref. [130]) and a
  segmented MZM at 100 Gb/s (ref. [131]), p.10; PetaMAC/s/mm2 and attojoule/MAC figures (refs. [32], [33]), p.2.
  Rule 3 (cited work); the modulator and DAC values are also EO-atlas scope (rule 2).
- 100 GHz ITU grid comb spacing (p.9): a generic statement about soliton microcombs, no device.
- Figs. 1-4 (p.17-p.20) are composites reproduced from cited works, each panel tagged with its reference (MRR weight
  bank [37, 38], InP SOA cross-connect [39], MZI mesh [14], multi-planar SiN routing with inter-planar coupler [44],
  PCM synapses [116], spiking lasers [55]-[72], etc.). Several panels (Fig. 1a, 2a, 3a, 4a) are the authors' own
  earlier work (Tait / Shastri / Prucnal refs. [30], [37], [38], [57], [68]): reproduced own work, D259 / D408. Only
  scale bars are legible; no component values are printed in the figures.
- Fig. 5 (p.21) is a concept rendering of a system-in-package; no values.
- No component with this paper's own quantitative result was found.

Missing fab / facility orgs: none needed (no rows). No fabrication statement; acknowledgments name funding agencies
and editorial thanks only.

Judgment calls: whole paper treated as a review whose values all come from cited work (rule 3, D259 / D408; empty
paper is a valid outcome per the brief).

Registry gaps: none.

## lit:wang2019 (Nature Photonics 2019 review, integrated photonic quantum technologies)

Components: 0. Metric rows: 0.

Values not entered and why:
- All quantitative device results in the text are cited: Si MZI 65 dB on-off ratio (ref. [41]), p.2; HOM visibilities
  100.1 +/- 0.4 % (ref. [18]) and 100.0 +/- 0.4 % (ref. [25]), p.2; SFWM source heralding efficiency 52 % / 50 % and
  indistinguishability 95 % / 91 % (refs. [47], [48]), p.2; QD source purity / extraction / indistinguishability
  (refs. [53], [54]), p.3; Si-waveguide SNSPD 91 % detection efficiency, 18 ps jitter, 50 Hz dark count (ref. [26]),
  p.3; TES / SNSPD photon-number resolution (refs. [33], [62], [63]), p.3; QKD state rates, key rates, QBER, HOM
  visibilities 46.5 % / 46 % (refs. [37], [65]-[71]), p.3-p.4; gate / teleportation fidelities (refs. [76], [78],
  [81]), p.5. Rule 3.
- Figs. 2-6 (p.9-p.13) are stated in each caption as "Figure reproduced from" the cited works (refs. [14], [26], [37],
  [41], [44], [57], [58], [65], [67], [73], [76]-[82], [85], [87], [97], [105], [115], [118]); caption values (chip
  areas 2 x 6 mm2 / 2 x 32 mm2 / 1.2 x 0.5 mm2 / 1.3 x 3 mm2 / 4.9 x 2.4 mm2, component counts 671 / 58 TOPSs / 82 MMIs,
  SNSPD > 90 % efficiency) belong to those works. Fig. 6b (ref. [44], Wang et al. Science 2018) is the first author's
  own earlier device: reproduced own work, D259 / D408. Fig. 6a scaling chart compiles cited devices.
- Fig. 1 (p.9) is a milestone timeline with citations; no component values.
- Boxes 1-2 (p.8) are tutorial descriptions (DC / MMI beamsplitters, MZI), no values.
- No component with this paper's own quantitative result was found.

Missing fab / facility orgs: none needed (no rows). Fig. 6 caption says the cited ref. [44] device "was fabricated using
the standard CMOS process" (no org, cited work). Acknowledgments list grants only.

Judgment calls: whole paper treated as a review whose values all come from cited work (rule 3, D259 / D408).

Registry gaps: none.
