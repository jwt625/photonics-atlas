# lit_276 batch report

Papers: lit:clemmen2009, lit:foster2007, lit:linnenbank2016, lit:turnerfoster2010. Page-1 titles match the source
rows; no garbled text layer. Total 12 components / 51 metric rows. `merge_component_staging.py --dry-run`:
+12 components, +51 metrics, 0 errors (two pre-existing warnings on other batches: cmp_lit_guo2024a_exc02,
cmp_lit_ni2025b_pimmwc). verified_on 2026-11-25.

## lit:clemmen2009 (5 components / 20 metrics)

CW SFWM photon-pair generation in ePIXfab SOI structures: straight wire, Sagnac loop, racetrack ring.

- `cmp_lit_clemmen2009_si_wire_500x220_11p3mm` (waveguide_platform.straight, 4): 4 +/- 1 dB/cm (method not stated,
  C band inferred), 500 x 220 nm, 11.3 mm.
- `cmp_lit_clemmen2009_grating_coupler` (fiber_chip_coupler.grating, 2): in/out coupling loss 8 +/- 1 dB (straight and
  Sagnac structures) and 7.5 +/- 1 dB (ring), scope unspecified (per coupler or the in + out sum not stated).
- `cmp_lit_clemmen2009_sagnac_dc_isolated` (splitter.directional_coupler, test structure, 3): coupling factor 62 %
  at 1540 nm ("estimated" from transmission measurements on an isolated copy), 52 % at 1520 nm, 72 % at 1560 nm.
- `cmp_lit_clemmen2009_sagnac_loop_mirror` (reflector.loop_mirror, 4): measured pump extinction 12.5 +/- 2.5 dB at
  1540 nm; loop 10 mm, 500 x 220 nm.
- `cmp_lit_clemmen2009_racetrack_l43` (resonator.ring, 7): FWHM 35 pm, FSR 12 nm, finesse ~350 (the paper's
  arithmetic, derived), cavity length 43 um, 500 x 220 nm ring and bus.

Not entered:
- All photon-pair metrics (no registry parameter, D250): pair flux vs pump power (Fig. 3(b), 5(c)), SNR 11.3 at 9 MHz
  (straight, p.8), SNR 4x lower and generation efficiency 7x lower in the Sagnac loop (p.10), residual pump 6-16 dB
  lower than the straight wire at equal pair flux (Fig. 4(b)), ring pair flux 0.3 MHz at 0.4 mW, 2 MHz/nm spectral
  density, ~10 dB lower pump power than the straight wire, SNR peak 30, pair-emission linewidth ~150 pm (p.10).
- Fiber-to-fiber pump transmission 20 dB (p.6-7): stated once for "the Si-waveguide" in the setup, structure not
  named (D159); in component notes.
- Predicted values: 12 dB Sagnac extinction from the 62/38 ratio, theoretical fluxes (78 MHz, 11 MHz), SNR 69 / 250 /
  225; FIMMWave beta2 -0.7 ps2/m, Aeff 0.064 um2, gamma 280 /W/m (simulated; no parameter for gamma / dispersion).
- Field enhancement F = 110 +/- 20 (p.6; author estimate, no parameter).
- Resonance positions 1528.0, 1540.0 / 1540.1, 1552.1 / 1552.2 nm (in notes). Mode splitting not entered: no number
  printed and the positions are rounded to 0.1 nm, so the splitting is not determined.
- 800 nm / 3 um access waveguides: no loss value (geometry in core_material).

Fab / facility: "Our structures were fabricated by the ePIXfab at IMEC with 193 nm deep UV lithography" (p.5 Sec. 3)
-> fab `org_imec`, process_name "ePIXfab at IMEC, 193 nm deep UV lithography" (acoleyen2012 precedent). Missing
org: **ePIXfab** (fab role, as printed "the ePIXfab at IMEC", lit:clemmen2009 p.5 Sec. 3). No facility; acknowledgments
are grants and staff thanks only.

## lit:foster2007 (6 components / 23 metrics)

CW FWM wavelength conversion in 300 nm tall Si channel nanowaveguides (Cornell).

- `cmp_lit_foster2007_si_fwm_wc_300x500` (frequency_converter.other, 6): TM max on/off conversion efficiency -9.6 dB
  (10.96 %, pump 1550 nm, 140 mW), > -11 dB across the C band (> 7.94 %), -12 dB (6.31 %) for 1477 -> 1672 nm with the
  1568 nm pump (FOD phase matching); 500 nm wide, 300 nm tall, 1.8 cm.
- `cmp_lit_foster2007_si_fwm_wc_300x650` (frequency_converter.other, 5): TE max -10.4 dB (9.12 %, 350 mW), > -11 dB
  across the C band; 650 nm, 300 nm, 1.8 cm.
- `cmp_lit_foster2007_si_fwm_wc_300x750` (frequency_converter.other, 4): TE peak ~-14 dB (3.98 %) read off Fig. 4 at
  the 1550 nm pump, 100 mW (extracted_from_figure, +/- 1 dB); 750 nm, 300 nm, 2 cm.
- `cmp_lit_foster2007_si_wg_300h_w500_650` (waveguide_platform.straight, 3): 1-1.5 dB/cm range over the four
  500-650 nm guides (n = 4; per-width values not printed), 300 nm, 1.8 cm.
- `cmp_lit_foster2007_si_wg_300x750` (waveguide_platform.straight, 4): 3 dB/cm, 750 x 300 nm, 2 cm.
- `cmp_lit_foster2007_inverse_taper_lensed_fiber` (fiber_chip_coupler.edge, 1): coupling loss 7-13 dB across the
  guides, scope unspecified (per facet not stated), low-power output corrected for propagation loss (loss_breakdown).

Not entered:
- 3-dB conversion bandwidths (registry gap below): TE 58 nm and TM 48 nm maxima (p.7), > 100 nm for three pumps and
  150 nm at 1538 nm (300 x 750 nm, p.9), 100 nm near the pump plus a 40 nm FOD region (300 x 500 nm, 1568 nm pump, p.9).
- 300 x 550 and 300 x 600 nm guides: only Fig. 2 traces, no printed value; not read (no converter row).
- Fig. 3 pump-power series (20-140 mW) of the 300 x 500 nm TM curve; Fig. 1 simulated dispersion / predicted
  efficiency (-10 dB, ~60 nm, 200 nm range); TPA / FCA < 0.7 dB calculated; 10 Gb/s eye diagrams (no parameter).

Fab / facility: "fabricated as previously described [26,32]" (p.7, passive, D80b) -> fab empty on all rows. Center
for Nanoscale Systems named as funding (p.10), not a facility (foster2006 precedent). No missing orgs.

## lit:linnenbank2016 (0 components)

Free-space double-pass optical parametric generator in a bulk 10 mm long, 0.5 mm thick MgO:PPLN crystal (purchased,
as printed "Covesion Ltd.", p.3) pumped by a fs Yb laser, with cw seeding from a fiber-coupled ECDL. Bulk crystal
part, out of scope (D411); setup lasers are not rows (rule 13). Nothing entered (OPG output powers, pulse durations,
gain and noise dynamics are bulk-system values).

## lit:turnerfoster2010 (1 component / 8 metrics)

- `cmp_lit_turnerfoster2010_si_rib_fwm_wc_w700` (frequency_converter.other, soi_rib, 8): on-off conversion efficiency
  saturating near -18 dB (1.58 %, approx; saturation from 30 mW, operated at 110 mW pump, 1554 nm); geometry 700 nm
  design width, 300 nm height, 30 nm slab, 270 nm etch, 3 um BOX, 3 um PECVD SiO2, 1.5 cm.

Not entered: conversion bandwidth > 837 nm and continuous conversion 1241 -> 2078 nm (1554 nm pump), 1930 / 1760 nm
extent for 1548 / 1560 nm pumps (registry gap); free-carrier lifetime 3 ns (p.5; no parameter); dispersion slope
1.6 ps/nm2 km from measured bandwidths (no dispersion parameter, D81); simulated ZGVD / FOD values; Fig. 2 traces.
Inverse-nanotaper coupling has no loss value (no coupler row).

Fab / facility: "we have designed and fabricated a waveguide" (p.2 Sec. 2), all authors at Cornell University
schools -> fab `org_cornell_university`; "performed in part at the Cornell NanoScale Science and Technology
Facility" (p.5) -> facility `org_cornell_nanoscale_facility` (cardenas2009 precedent). Cornell Center for Nanoscale
Systems is funding only. No missing orgs.

## Judgment calls

1. foster2007 maxima (-9.6 dB TM, -10.4 dB TE) assigned to 300 x 500 nm and 300 x 650 nm from the Fig. 2 traces and
   caption; the text does not name the guide with the value.
2. foster2007 "> -11 dB across the entire C-band" entered on both 300 x 500 (TM) and 300 x 650 (TE) rows: the
   sentence names "the waveguides and polarizations with lowest magnitude of GVD", which the Fig. 2 caption identifies
   as these two (not a D254 family-typical value).
3. foster2007 300 x 750 nm converter row rests on a figure-read efficiency (~-14 dB, Fig. 4); without it the paper's
   headline 150 nm-bandwidth device would have no row because conversion bandwidth has no parameter.
4. dB conversion efficiencies converted to `power_conversion_efficiency_pct` with basis derived (kuyken2011 /
   foster2006 precedent); the figure-read 750 nm value keeps `extracted_from_figure` with the conversion in notes.
5. clemmen2009 Sagnac loop interferometer as `reflector.loop_mirror` with its measured transmission extinction
   (`extinction_db`); the isolated coupler copy is a separate `splitter.directional_coupler` test-structure row.
6. clemmen2009 grating-coupler loss: scope unspecified ("loss due to in and out coupling", per coupler vs sum not
   stated); one GC row with two condition rows (straight / Sagnac vs ring structures).
7. clemmen2009 finesse ~350 derived (paper's arithmetic on FSR / FWHM); ring Q not computed (not printed).
8. foster2007 platform `soi` from the paper's own SOI index-contrast discussion (p.4); BOX not printed.
9. turnerfoster2010 width / etch depth `design_target` (fabricated dimensions not measured in the text).

## Registry gaps

1. Frequency-converter conversion bandwidth (open since lit_07 / lit_212; proposed `bw_3db_nm` widened to
   frequency_converter, or `conversion_bandwidth_nm` with one- / two-sided criterion in condition). Skipped values:
   foster2007 TE 58 nm and TM 48 nm (p.7), > 100 nm and 150 nm (p.9, Fig. 4), 100 nm + 40 nm FOD region (p.9);
   turnerfoster2010 > 837 nm (p.4, Fig. 2(b)).
2. Photon-pair source metrics (D250 deferred): clemmen2009 generated pair flux (MHz), pair spectral density (MHz/nm),
   coincidence SNR (CAR-like) and pair-emission linewidth (p.8, p.10).
3. Free-carrier lifetime (`carrier_lifetime_ns`, waveguide_platform / frequency_converter): turnerfoster2010 3 ns
   (p.5).
4. Waveguide nonlinear parameter gamma (open since lit_212): clemmen2009 280 /W/m simulated (p.5).

## Missing orgs

- ePIXfab: fab, printed "the ePIXfab at IMEC", lit:clemmen2009 p.5 Sec. 3 (5 rows; already reported by earlier
  batches, e.g. acoleyen2012, agazzi2010).
