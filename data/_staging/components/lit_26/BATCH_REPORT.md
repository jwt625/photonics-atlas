# Batch lit_26 report (distill subagent, 2026-10-29)

Dry-run `batch lit_26: +44 components, +340 metrics; errors 0`. ASCII, no e-mail or addresses, no quotes beyond org
names as printed. All seven cached texts match their source rows (title / authors on page 1). Not audited or merged.

## Per paper (components / metrics)

- chen2026a (3 / 22): FHD Ge:silica rings (ge_silica). 1.5 mm ring: Qi 329 M / QL 278 M (Fig. 2(c)), ring-down QL
  276 M (derived from 227 ns), weak-coupling Qi series 458-1550 nm (566 M at 1064 nm best), 0.07 dB/m -> 0.0007 dB/cm
  (author_estimate, ng not stated), simulated 130 um bend radius. 3 mm array (D165): Qi 50-400 M, n 54. Reflow test
  (27 rings): mean 0.9 M -> 56.4 M, best 1.1 M -> 132 M. Not entered: Fig. 3(b, c) plot-only values, mode splitting
  (no value), film index. Fab org_caltech (contributions: two Caltech authors fabricated); Southampton ORC prepared
  the FHD wafers (supplier, note). Facility org_ucsb_nanofabrication_facility (borderline: support of the facility
  and its staff); KNI in funding / staff thanks not entered. Same work as merged ofc2026:Th1D.6 (cross-noted).
- zhang2020 (1 / 15): Euler-bend multimode Si racetrack (Reff 29 um, 1.6 um wide). QL ~1.3e6, FWHM 1.20 pm,
  loss 0.3 dB/cm (fit, derived), Qi ~2.3e6 (derived from loss and ng ~3.8), ng author_estimate, FSR 0.9 nm, simulated
  0.25 dB/cm and 0.63 % power coupling, geometry. Wavelength 1524 nm inferred from the Fig. 5(a) axis (design 1550 nm).
  Not entered: Table 1 values of other works, simulated mode-excitation ratios. Fab: "Institute of Microelectronics,
  China" MPW foundry (p.4) mapped to org_institute_of_microelectronics_chinese_academy_of_sciences (see decisions).
- li2026 (7 / 30): AGF dense array (waveguide_platform.other; IL < 1 dB, widths 410-550 nm), AGF-modulated
  waveguide 4.16 dB/cm and straight reference 3.72 dB/cm (both derived, fringe-ER extraction), AGF DCs 60:40 / 70:30
  (target split author_estimate, Lc 27.9 / 23.1 um, gap 200 nm), TO phase shifter (~39 mW per 2 pi,
  author_estimate), 2D OPA (FoV 120 x 14.5 deg, 0.14 deg/nm, beamwidths 4.1 / 1.2 deg, SLL bound and Fig. 7(d)
  values). Not entered: crosstalk and pitch of the array, 0.77 dB splitter variation (gaps), SLL -18.2 dB (text
  pairs it with theta, Fig. 7(d) labels 17.9 dB on the theta scan; D156), theoretical SLL -23 dB, 32-channel
  Gaussian tree (no number). Fab org_shanghaitech_university (contributions); facility
  org_shanghaitech_material_and_device_lab (borderline: thanked for technical support).
- lin2019 (1 / 11): asymmetric Y-junction family, 11 r1 designs as one array-level row (D165): measured excess loss
  < 0.5 dB (derived from cascades), imbalance 0-18 dB (PSR magnitude), simulated 0.22-0.36 dB and 1-dB BW > 100 nm,
  geometry. Not entered: per-design PSRs (Fig. 3(a) / 4 plot only, image mirrored in the cache), PSR slope vs r1,
  simulated temperature dependence. Fab org_applied_nanotools (EBL at Applied Nanotools stated, p.3).
- xu2018 (1 / 17): SWG-slot adiabatic 3-dB coupler. Split "3 +/- 0.27 dB" per port converted to 47.1-53.3 %
  (derived), simulated 3 +/- 0.33 dB and +/- 0.73 dB likewise (simulated), excess loss mean 0.20 / max 0.74 dB (half
  of MZI excess, derived), MZI ER >= 24.2 dB, simulated IL < 0.08 / < 0.13 dB, Table 1 geometry. Not entered: Bragg
  wavelength / cutoff (simulated), Table 2 other works. Fab org_applied_nanotools.
- spencer2015 (27 / 206): 24 low-kappa Si3N4 Bragg gratings from Table 1 (8 post, 8 sampled, 8 high-order), each with
  kappa (T-matrix fit, derived), FWHM pm -> nm (derived), peak R dB -> % (derived), length, period (first order),
  thickness stack; lambda/4-shifted 2 mm grating as resonator.bragg (7.6 pm, Q 204 k derived, 0.2 dB/cm, IL 2.5 / 1.1
  dB); 0.5 m spiral (< 5 dB/m C+L, < 3.5 dB/m at 1550, OFDR); polished facet 0.85 dB per facet. Wavelength of grating
  values inferred (design Bragg 1550 nm). Not entered: kappa 30 cm-1 of the shifted grating (gap), post gap / dw /
  burst N (no reflector parameter), wo of sampled / high-order designs except the two Fig. 2 examples. Fab empty
  (passive voice, authors at three orgs).
- wang2017 (4 / 39): circular Bragg mirror (measured IL 0.1-0.32 dB, R ~93-98 % derived, simulated R > 90 % / > 95 %
  bands, 97.6 % at 1550, stopband 500 / 397 nm simulated, N 6, period 362 derived, fill 0.5, footprint 20.38 um2);
  three Fabry-Perot notch filters (resonator.photonic_crystal: IL <= 0.5 dB family bound, FSR 6.34 / 30 nm, coupling
  7.6 / 15 / 1.4 % author_estimate, notch > 5 / > 10 / < 3 dB, Q ~14312 / ~4683). Not entered: simulated PER, taper
  angle / length, simulated > 20 dB notch, earlier-work filter values [21]. Fab empty (passive voice).

## Fab / facility organizations missing from the registry

- "Core Facility Platform of Electronics of ShanghaiTech University" (li2026 p.10 Acknowledgements; thanked for
  technical support, borderline facility).
- "Melbourne Centre for Nanofabrication (MCN)" and "Australian National Fabrication Facility (ANFF)", Victorian Node
  (wang2017 p.11 Acknowledgment, work performed in part there): facility_org_ids for all four wang2017 rows once added.
- Not needed: Max-Optics Technology Co., Ltd (li2026 p.10, company thanked for technical support, not a facility).

## Decisions for the coordinator

1. zhang2020 fab: printed "Institute of Microelectronics, China" (no CAS named) entered as IME CAS; keep or clear.
2. li2026 and chen2026a facility rows are thanks-level acknowledgements of a facility (not of staff only): keep or
   drop (D72 / D84b).
3. xu2018 per-port dB split ratio stored as % (derived); alternative: leave out until a dB split parameter exists.
4. lin2019 and spencer2015 granularity: lin2019 as one family row (per-design values only in a mirrored plot);
   spencer2015 as 24 per-design rows from Table 1.

## Registry gaps (value actually skipped, locator, proposed definition)

- crosstalk_db for waveguide_platform: li2026 dense AGF array, measured crosstalk below -20 dB to nearest and
  second-nearest neighbours over 1500-1600 nm (p.6 Fig. 4(c)), simulated below -30 dB (p.6 Fig. 3(g)). Definition:
  power coupled to a neighbouring waveguide of a dense array / superlattice, positive dB, neighbour order and length
  in condition.
- pitch_um for waveguide_platform: li2026 750 nm array pitch (p.5). Definition: centre-to-centre spacing of a
  waveguide array (re-proposed against D250 with a design value of a fabricated array).
- Split-ratio wavelength variation for splitter (e.g. wdl_db widened to splitter, or split_ratio_variation_db):
  li2026 maximum power variation below 0.77 dB over 1500-1600 nm (p.8); lin2019 simulated split-ratio variation below
  1 dB over 100 nm (p.1). Definition: max minus min of a port's split ratio (dB) over the stated wavelength span.
- kappa_per_cm for resonator: spencer2015 lambda/4-shifted grating, fitted kappa 30 cm-1 (p.6 Sec. 4.2).
  Definition: grating coupling coefficient of a Bragg / phase-shifted grating resonator.
- gap_nm for reflector: spencer2015 post-to-waveguide gap 0.8-1.6 um per design (p.2, p.6 Table 1). Definition:
  lateral gap between a side perturbation (post) and the waveguide.
- taper_length_um for reflector: wang2017 2 um pie-shaped taper before the blades (p.8). Low priority.
- per_db for reflector (simulated only): wang2017 PER above 16.5 dB over 1433-1763 nm (p.8). Low priority.
