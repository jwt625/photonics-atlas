# lit_296 batch report

Distilled 2026-11-27. Paper: lit:zhu2021 (arXiv v1 preprint, 94 pages, of the Advances in Optics and Photonics 2021
review "Integrated photonics on thin-film lithium niobate"). Result: 0 component rows, 0 metric rows (header-only
CSVs). Page-1 title matches the source row; the cached file is the review itself, not a correction / erratum. Values
below were read from the preprint only.

## lit:zhu2021 (review, Harvard / Caltech / HyperLight authors)

Components: 0. Metric rows: 0.

Method: read the body (p.1-p.73) and checked every figure caption for a reproduction credit. Captions with no credit
(Figs. 1, 3, 4, 10, 12, 13, 21, 22, 34, 40) are the review's own illustrations or simulations; every other figure and
all of Tables 2-6 are reproduced or cited (rule 3, D259 / D408). A sentence scan for numbers with units and no citation
found only material constants, class-typical statements, or summaries of a cited work in the same paragraph.

Values not entered and why:
- Waveguide propagation losses (p.8-p.10, Fig. 7 compilation of refs. [11-20, ...]), fiber-chip coupling 1.7 dB and
  0.54 / 0.59 dB per facet, grating couplers -3.5 / ~-3 dB with 55 nm 1-dB bandwidth (p.12, refs. [120], [128], [121],
  [122]), cavity Q-factors (p.13-p.14, Table 2), SHG / cavity-SHG efficiencies (Tables 5-6), Kerr / EO combs, Raman,
  supercontinuum, acousto-optic, detector, emitter, rare-earth and III-V results (Secs. 3.4-6.5): cited work, rule 3.
- Er-implanted LNOI ring loaded Q 2e5 at 1532 nm, up to 1e6 at 1515 nm, average 5e5 (p.64): summary of ref. [134]
  (the paragraph opens "performed in Ref. [134]"; Fig. 39(b) reproduced from [134]), rule 3.
- SNSPD TE absorption rate "~0.1 dB/um" on partially etched LN (p.62): a class-typical statement about the cited
  demonstrations [421], [422]; no device of this paper, rule 3 / D80i.
- Wafer-scale film / etch-depth variation below 6 nm (p.72, Fig. 44): reprinted from ref. [497], rule 3.
- Modulator material (Vpi, EO bandwidth, CPW loss 0.7-1.1 dB cm-1 GHz-1/2, Fig. 11, Tables 3-4) and the review's own
  modulator simulations (Fig. 12 microwave / optical field of an X-cut MZM with 5 um gap; Fig. 13 simulated EO S21 for
  generic 7 mm / 14 mm MZMs): modulator metrics, rule 2 (EO atlas); also generic illustrations, not devices.
- Review's own GVD simulations (p.35-p.36, Figs. 21-22: beta2 vs wavelength for 700 nm X-cut film, 60 deg etch angle,
  1.5 um top width, 450 nm etch depth, width / etch / film / cladding sweeps): curves only, no printed values, generic
  design study rather than a component, and no registry parameter for GVD (dispersion rejected in D81).
- Fig. 4 simulated mode profiles of four waveguide types and Fig. 34 acoustic displacement profiles: illustrations with
  no performance value.
- Fig. 32 pulse-propagation model (p.52-p.53): reproduced from ref. [296], rule 3.
- Material constants (Table 1, n, r33, d33, n2, dn/dT; p.4-p.5): material data, not component results.
- Fig. 43 proposed microwave photonic receiver (p.71): a proposal adapted from a grant proposal, no values.

Missing fab / facility orgs: none needed (no rows). The acknowledgment (p.73-p.74) states device fabrication for the
Harvard research at the Harvard University Center for Nanoscale Systems; it covers the cited works, not a component of
this review.

Judgment calls: whole paper treated as a review whose only own content is illustrative simulation (modulator,
dispersion, acoustic modes); empty batch per D259 / D408 and rule 2.

Registry gaps: none new (GVD / dispersion already rejected in D81).
