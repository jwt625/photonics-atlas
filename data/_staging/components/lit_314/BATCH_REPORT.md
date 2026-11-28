# lit_314 batch report

Distilled 2026-11-28. Paper: lit:ludlow2015 (arXiv 1407.3493 v2, 86 pages; published as Reviews of Modern Physics
87, 637 (2015), "Optical atomic clocks"). Page-1 title matches the source row; not a correction or erratum;
`garbled_text_layer` false. Dry run `merge_component_staging.py data/_staging/components/lit_314 --dry-run`:
+0 components, +0 metrics, 0 errors.

| paper | components | metric rows |
|---|---|---|
| ludlow2015 | 0 | 0 |

## lit:ludlow2015 (review, no own measurements of in-scope parts)

No rows. The paper is a review of trapped-ion and optical-lattice clocks (Secs. I-VII, pp.3-70; references
pp.70-86). It has no methods or fabrication section and reports no integrated / chip-scale photonic component or
fiber-coupled passive part that the authors made, measured or simulated for this work. Every quantitative statement
is either credited to cited work (rule 3, D259 / D408), an atomic-physics quantity (clock shifts, polarizabilities,
magic wavelengths, linewidths; not a component parameter), or concerns bulk / free-space apparatus (D411):

- p.10-11 Sec. III.A reference cavities: ULE / crystalline two-mirror Fabry-Perot cavities with "finesse approaching
  10^6", long spacers, crystalline coatings: bulk optics (D411) and credited to cited work (rule 3).
- p.11 Sec. III.A spectral hole burning, optical-fiber delay lines (Kefelian et al., 2009): cited, no values.
- p.11-12 Sec. III.B noise-cancelled fiber links ("worse than 10^-14 at one second" per km without cancellation,
  "below 10^-17 at one second" with it): cited (Foreman et al., 2007b; Williams et al., 2008); a fiber link is also
  not a component class in the registry.
- p.12 Sec. III.C / Fig. 1 frequency combs, microstructured fibers for broadening: generic description, no values.
- p.19-21 Sec. V.A ion traps (Figs. 2-3, microstructured / laser-machined segmented electrodes): RF electrode
  structures, not photonic components; geometries credited to cited work.
- p.27 / p.42 Tables I, IV (atomic parameters, magic wavelengths), p.31 / p.56 Tables II, V (systematic shift
  budgets), p.33 / p.58 Tables III, VI (absolute frequencies): atomic-clock quantities from cited work.
- Figs. 7-8, 12-19: clock spectroscopy, stability and comparison data reproduced from cited work ("Reproduced with
  permission", e.g. p.54 Fig. 15, p.64 Fig. 19), D259a figure rule; none is a component metric.
- References (p.72, p.76) list two "unpublished measurement, private communication" items (Chou 2014; Huntemann 2014): clock
  results attributed to other researchers, not values of this paper, and not component metrics.

Missing fab / facility orgs: none needed (no component rows).

Judgment calls: none beyond applying the lit_304 shekhar2024 / errandoherranz2019 review precedent (0 rows).

Registry gaps: none.
