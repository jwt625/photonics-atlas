# Batch lit_57 report (distill subagent, 2026-10-30)

Classes: fiber_chip_coupler, fiber_interface, polarization (plus waveguide_platform / chip_chip_coupler rows the papers
characterize). Dry-run: `batch lit_57: +23 components, +147 metrics; errors 0` (only the pre-existing WARN on
cmp_lit_ni2025b_pimmwc-m18). All 7 papers `restricted_local_only`: facts and locators only. Page-1 title / authors match
the source rows for all 7; none is a correction / erratum; no `garbled_text_layer` flag. almeida2003 and shoji2002 text
layers drop micro / +/- / minus signs: every value checked on the page renders. shoji2002 text.md page 1 starts with the
tail of a preceding Electronics Letters article (circuit paper) and page 2 ends with the head of the next one (Yokoi et
al.); only the Shoji letter was used. Rows built by a scratchpad script.

## Per paper (components / metrics)

- shoji2002 (2 / 14): Si inverse taper in 3 x 3 um polymer overlay (fiber_chip_coupler.edge): 0.8 dB per conversion
  at 1560 nm = (3.6 - 2.0 OLCR wire loss) / 2, loopback_half / loss_breakdown / derived; 3.6 dB fiber_to_fiber (abstract
  prints 3.5 dB, noted); PDL ~0.5 dB of the whole sample; design tip 60 nm, taper 200 um, overlay 3 x 3 um, Si 0.3 x 0.3
  um (derived, printed um). Si wire (waveguide_platform.straight): 2.0 dB / 1.09 mm OLCR -> 18.35 dB/cm derived. Not
  entered: Fig. 2 calculated conversion-loss curves, TEC fibre connection loss < 0.05 dB (setup).
- almeida2003 (2 / 18): Si nanotaper (edge): IL 3.3 +/- 0.3 dB TM, 6.0 +/- 0.4 dB TE at 1550 nm per_coupler / cutback
  / author_estimate (xi times 3D-FDTD c_wt); 9.2 dB (12 %) fiber_to_fiber TM; 1 dB lateral tolerance +/-1.2 um TE;
  facet reflection < -48 dB simulated; SEM geometry (tip 100, taper 40 um, 470 x 270 nm, 82 deg); 3 um BOX / cladding;
  mfd_fiber_um 4.9 specification (design input fiber, typical EDF). Waveguide row: 5 +/- 2 dB/cm (Fabry-Perot), 84 deg.
  Not entered: enhancement xi 7.0 / 8.2 (no parameter); simulated partial terms (0.26 dB mismatch at 120 nm, < 0.25 dB
  and 1.5 dB conversion, 0.4 dB TM optimum).
- taillaert2006 (9 / 46): fabricated uniform SOI GC (31 % / 5.1 dB per coupler, sqrt(T) loopback_half derived; 10.2 dB
  two-coupler; 1 dB bw ~40 nm; simulated 37 % / 40 nm / reflection < -20 dB on the same row since it is the same
  design; 630 nm / 70 nm / ff 0.5 / 10 deg / 1 um BOX / 400 um taper / 12 um grating width, mfd 10.4 specification);
  oxide-clad variant (34 %); 5 simulated design rows (Table I 44 / 53 / 79 %; nonuniform 61 %; nonuniform + Si/SiO2
  reflector 92 %, < 1 dB over 1532-1567 nm, reflection < -24 dB, 100 nm grooves); InP membrane GC uncoated (19 %
  measured, 34 % simulated) and with 240 nm Al2O3 (30 % measured, 54 % simulated for the 260 nm design, peak ~1560 nm
  from Fig. 13). Not entered: 69 % gold-mirror coupler (p.8, attributed to ref. 20 "to be published", D259); 0.5 dB
  alignment / angle / distance tolerances (no parameter, D250); Fig. 13 corrected-theory curve; coupling length 3.8 um;
  9 nm/deg angle shift.
- zaoui2012 (4 / 27): Al backside-mirror GC, 600 nm: 1.63 dB / ~69 % at 1539 nm (Eq. (2) halves the two-coupler loss
  after setup loss: loopback_half derived), 1 dB bw 48 nm, 3 dB bw ~78 nm, simulated -0.82 dB / 56 / 91 nm, geometry
  (600 nm, ff 0.5, 70 nm, 250 nm Si, 3 um BOX, 9 deg design, 10 um access waveguide). No-mirror reference: ~3.2 dB from
  Fig. 5 (extracted, consistent with the labelled 1.6 dB gain), simulated 2.2 dB / 45 / 78 nm / reflection ~12 dB.
  595 / 605 nm siblings: peaks read from Fig. 4 (~1.7 dB near 1526 / 1555 nm, extracted_from_figure). Not entered:
  -0.76 dB at dBOX 2.95 um (sweep point).
- chee2012 (2 / 17): HPW three-core DC PBS, fabricated (6.4 um, 340 nm SOI): IL 2.8 TE / 6.0 TM and ER 12.3 bar /
  13.9 cross (mean 1530-1600 nm, normalized to a reference waveguide -> per_component / reference_structure; ER as
  per_db with Eq. 3 / 4 definitions); FDTD with measured-approx parameters (1.0 / 7.7 dB, 11.2 / 20.8 dB) on the same
  row. Design row (6.5 um, 220 nm): IL < 0.5 dB, ER > 15 dB simulated. Not entered: 15 dB ER bandwidth 70 nm, cross ER
  40 dB (beyond accuracy), tolerances, no-air-gap variant simulation, XTEM dimensions (no role parameters).
- thomson2007 (2 / 20): fs-laser-inscribed MCF fan-out (fiber_interface.fan_out, glass): IL ranges per configuration
  (SMF-SMF 3.1-5.4, FVA-MCF optimized 3.4-5.9, simultaneous 3.9-6.5, mean 5.0 dB), per-facet coupling 0.5 (SMF-28) /
  0.8 dB (MCF), on-chip 2.1-4.4 dB (authors' subtraction, derived), PDL < 0.12 dB, crosstalk < -26 dB (1540-1600 nm),
  MCF MFD 10.9 measured, SMF-28 10.4 specification, pitches 50 / 250 um, 4 ch, 25 mm, cross-section 13.5 x 10.2 um
  (derived). Straight reference waveguide: 3.3 dB fiber_to_fiber, 0.92 dB/cm derived ((3.3 - 1.0) / 2.5).
- barwicz2016 (2 / 5): compliant polymer interface (fiber_chip_coupler.other, platform polymer, dangel2018 precedent):
  1.6 dB peak per_coupler, wdl_db 0.6 dB over ~100 nm and all polarizations, 2 um lower oxide. Chip-to-chip
  (chip_chip_coupler.butt), port B: 1.1 dB per_interface derived (roundtrip / reference, halved), 75 um converter.

## Values deliberately not entered (key ones)

- barwicz2016 Fig. 6 O-band metamaterial converter, -1.3 dB peak with 0.8 dB penalty over 100 nm, fibers self-aligned
  in V-grooves (p.4, abstract): the sentence presenting Fig. 6 cites ref. [16] (authors' own OFC 2015 Th3F.3) and the
  caption says "More information is found in [16]". Treated as reproduced own earlier work (D259 / D259a); no component
  row (no other metric). Top open question.
- barwicz2016: Monte Carlo 3 sigma < +/-1.3 um (ref. [12]), re-alignment < 1.5 um / +/-1-2 um (refs. [21]-[22]),
  -2.4 dB of ref. [24]: cited. V-groove parallel fiber assembly has no own metric: no row.
- taillaert2006 69 % gold mirror (ref. 20).

## Organizations

- Missing from the registry: Heriot-Watt University (thomson2007 p.1 affiliation; p.2 "we use ultrafast-laser
  waveguide-inscription to ... fabricate", all authors at Heriot-Watt -> fab org for both thomson2007 rows once
  registered). Institut fur Mikroelektronik Stuttgart (IMS CHIPS; zaoui2012 p.1 affiliation 2; not needed: fab empty
  because "we" spans two orgs). University of St Andrews (taillaert2006 p.2; not needed).
- Set: shoji2002 org_ntt ("we fabricated samples", all authors NTT Telecommunications Energy Laboratories; umeki2010
  precedent for org_ntt); almeida2003 facility org_cornell_nanoscale_facility (performed in part at the Cornell
  Nanofabrication Facility, p.3).
- Left empty: almeida2003 fab (passive); taillaert2006 (Ghent + St Andrews); zaoui2012 (Stuttgart INT + IMS); chee2012
  (passive, all IME; D80b); barwicz2016 (acknowledgment: "most" chips fabricated at IBM Watson MRL, Fig. 6 device at the
  IBM Microelectronics Foundry; the chips of the entered rows are not named, so org_ibm_watson not set; coordinator may
  rule otherwise).

## Judgment calls

1. taillaert2006 simulated basic grating values (37 %, 40 nm, < -20 dB) on the fabricated row: same physical design
   (630 nm, 70 nm, ff 0.5, 10 deg, 1 um BOX, air; Sec. 3 compares the measurement to "the simulation results"). The
   fill factor 0.5 is the design value; Sec. 3 does not restate it.
2. taillaert2006 InP rows: scope unspecified (the two-coupler method is described for SOI only). Oxide-clad SOI 34 %:
   loopback_half / measured (Sec. 3.2 efficiency definition, arithmetic not shown, D167 analogue).
3. Wavelengths read from figures (taillaert2006 Fig. 11 ~1550 nm, Fig. 13 ~1560 nm; zaoui2012 no-mirror ~1535 nm;
   barwicz2016 figure spans) flagged wavelength_inferred.
4. chee2012 IL normalized to a reference waveguide: per_component / reference_structure (skill rule 6), not de_embedded
   (merged polarization rows split 7 / 8 between the two).
5. almeida2003 IL as author_estimate (rests on simulated c_wt); 9.2 dB treated as TM at 1550 nm (stated in that context).
   The paper calls 2 x 3.3 dB plus 13 mm at 5 dB/cm "consistent" with 9.2 dB; the printed numbers do not add up to it
   (entered as printed).
6. thomson2007 per-waveguide values as range rows (n 4) with the per-waveguide list in notes, not 12 rows; 0.92 dB/cm
   straight-waveguide loss is our arithmetic on the paper's own measured values (derived).
7. zaoui2012 595 / 605 nm sibling rows from figure readings only (labelled curves, +/-0.1 dB, +/-5 nm).
8. shoji2002 0.8 dB as loopback_half / loss_breakdown (wire loss subtracted, then halved; includes polymer waveguide and
   fibre-polymer connection shares).

## Registry gaps (skipped value + locator)

- polarization gap_nm / bus geometry (confirms lit_40): chee2012 waveguide spacing d 200 nm, HPW gap g 75 nm (design),
  XTEM gap 11 nm (p.4, p.8).
- fiber_interface `mfd_chip_um` (mode field of the fan-out waveguide at its facet): thomson2007 15.8 x 11.8 um (p.4).
- ER bandwidth for polarization (`er_bandwidth_nm`, deferred D250): chee2012 15 dB-ER bandwidth 70 nm (simulated only).
- Coupling-efficiency enhancement ratio (cutback with / without coupler): almeida2003 xi 7.0 / 8.2 (p.2); one paper,
  low priority.
- 0.5 dB alignment tolerances (D250 stands): taillaert2006 p.5 / p.7.
- wdl_db for chip_chip_coupler: barwicz2016 0.1 dB penalty over 100 nm (p.9, Fig. 13).

## Open questions

1. barwicz2016 -1.3 dB Fig. 6 value: removed as own earlier work [16] (D259a) or kept as the paper's headline result?
2. barwicz2016 fab org_ibm_watson from "most of the photonic chips were fabricated" at the MRL with only the Fig. 6
   device named as an exception?
3. Register Heriot-Watt University (fab for thomson2007).
