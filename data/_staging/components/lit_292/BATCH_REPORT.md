# lit_292 batch report

Distilled 2026-11-26. Papers: lit:wooten2000, lit:yariv2000. Result: 0 component rows, 0 metric rows (header-only
CSVs). Page-1 titles match the source rows for both papers; neither cached file is a correction / erratum.

## lit:wooten2000 (IEEE JSTQE 2000, invited review of LiNbO3 modulators)

Components: 0. Metric rows: 0.

Values not entered and why:
- All modulator metrics (Vpi, chirp, EO response, extinction ratio, RF return loss, bias drift, insertion-loss change,
  field failure rates; p.4-p.12, Figs. 4-5, 11-15, Tables I and III): rule 2 scope (EO atlas).
- Figs. 4 and 5 (p.5) are calculated EO responses of generic modulator designs: modulator metrics, rule 2.
- Thick plated CPW electrode RF loss "<= 0.5 dB cm-1 GHz-0.5" for ">= 15 um" electrodes (p.4, read from the page
  render; the text layer drops the numbers): a generic modulator-electrode statement, not a component of this table
  (rule 2), and no specific device.
- Directional-coupler switch drive voltages (reversed delta-beta 10-20 V, digital optical switch 40-50 V; p.4): class
  typical values with refs. [22]-[27], rules 1 / 3; also EO switching devices (rule 2).
- Linearized CATV modulator directional couplers "coupling angles within 2%" (p.9): a manufacturing tolerance
  requirement, not a measured component result.
- Photorefractive damage "negligible for optical powers less than 100 mW" above 1 um (p.2): material statement, no
  component.
- APE waveguide aging lifetimes (p.2, refs. [12], [13]) and ridge-modulator Vpi values (p.5, ref. [28]): cited, rule 3
  and rule 2.
- Bias drift and insertion-loss stability data (Figs. 11, 12, 14, 15) are attributed to ref. [19] (Maack, a co-author's
  1999 SPIE paper) and Fig. 13 to Minford [55]: reproduced / cited data (D259 / D408) and modulator metrics (rule 2).
- Hybrid-integrated monitor photodetectors (p.6): mentioned with no value.
- No non-modulator component with this paper's own quantitative result was found.

Missing fab / facility orgs: none needed (no rows). Author affiliation printed p.1: JDS Uniphase Corp. (alias
`JDS Uniphase` -> `org_jdsu` exists); no fabrication statement.

Judgment calls: whole paper treated as review + modulator scope; 0 rows.

Registry gaps: none.

## lit:yariv2000 (Electronics Letters 2000, 2-page theory letter)

Components: 0. Metric rows: 0.

- p.1 opens with references 7-8 of the preceding letter in the journal, and p.2 (after this letter's references) holds
  the start of the following letter (an optically pumped lead-salt VCSEL paper by other authors): both ignored as other
  papers.
- The letter derives the ring-waveguide coupling relations (transmission, circulating power, critical coupling,
  FWHM / finesse / Q, add-drop transfer); no fabricated or measured device and no numerically reported component
  performance.
- Parameter values in Figs. 2 and 3 (t = 0.980 / 0.990 / 0.999 / 0.9998, a = 0.9998 to 1.0001, incident power 1 W;
  p.1-p.2) are illustrative inputs of the theory curves, not component results: not entered.

Missing fab / facility orgs: none (no rows). Acknowledgment names funding agencies only (ONR, AFOSR), not facilities.

Judgment calls: theory paper with no component performance -> 0 rows.

Registry gaps: none.
