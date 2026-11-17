# Batch lit_165 report

Papers: lit:arianfard2020, lit:yang2018a, lit:lake2016. Distilled 2026-11-16 under the pic-component-distill skill
(Contracts v4-v7). Totals: 17 components, 72 metric rows. `merge_component_staging.py --dry-run`: 0 errors (the only
warning is an existing ni2025b row, not this batch).

Source identity (page-1 check): all three cached texts are arXiv preprints of their registry papers.

- arianfard2020: arXiv 2102.04049v1, printed title "Design of Photonic Filters based on Integrated Coupled Sagnac
  Loop Reflectors"; the registry carries the JLT title "Advanced Multi-Functional Integrated Photonic Filters Based
  on Coupled Sagnac Loop Reflectors" (same DOI and arXiv id in source.json). Same authors and content, so it is
  treated as the same work. Rows note the title difference.
- yang2018a: arXiv 1702.05076v3 (2017-09-17) of the Nature Photonics paper "Bridging ultrahigh-Q devices and photonic
  circuits". Distilled from what the preprint reports; the journal version was not read. Stated in every row's notes.
- lake2016: arXiv 1508.06970v2 (2016-01-12) of the APL paper, with its supplement (pages 6-8).

## lit:arianfard2020 (11 components, 47 metrics; all `row_kind: design`, basis `simulated`)

Theory-only paper (scattering-matrix model, lossless couplers). Platform `soi` as the paper designs on SOI Si wires
(TE). Fab / facility empty (nothing fabricated).

| component | class | metrics |
|---|---|---|
| parallel_mcslr_fano (100 um, t_s 0.74, t_b 0.94) | resonator.other | ER ~13.9 dB, Q ~33700 (q_loaded), IL ~6.3 dB (p.5) |
| parallel_mcslr_il_100ghz (346 um) | wdm.interleaver | CS 100.0053 GHz; per port 1-dB BW, 3-dB BW (ratio x CS), ER, IL (Table II / III); thermal drift ~64 pm/K (Fig. 8(c)) |
| parallel_mcslr_il_50ghz (692 um) | wdm.interleaver | CS, 1-dB / 3-dB BW (ratio x CS), ER, IL per port (Table III) |
| parallel_mcslr_il_200ghz (173 um) | wdm.interleaver | same set (Table III) |
| mzi_il_100ghz (comparison) | wdm.interleaver | CS, 1-dB BW, ER, IL per port (Table II) |
| mcslr_switch_2x2 | switch_fabric.other | crosstalk, ER, IL for cross / bar states (Table IV) |
| zigzag_mcslr_bpf (100 um, t_s = t_b = 0.78) | wdm.other | 3-dB BW 68 GHz (Fig. 10(d) label), IL ~1.9 dB and ER ~10.4 dB read off Fig. 10(a) / 11(a-ii) |
| bpf_cmp_1mrr, bpf_cmp_2cslr, bpf_cmp_3cslr, bpf_cmp_2mrr | wdm.mrr / wdm.other | 3-dB BW 39.16 / 39.22 / 53.76 / 58.72 GHz (Fig. 10(d) labels) |

Not entered:
- Model inputs n_g 4.3350 and 2.4 dB/cm (55 m^-1): taken from the authors' earlier fabricated devices (refs. 33, 40;
  rule 3). Si dn/dT 1.8e-4 /degC (cited, ref. 76).
- Fano slope rate 389 dB/nm (no registry parameter); NRMSD within the 1-dB BW (Table II, no parameter); group-delay
  peak about 18 ps (Fig. 10(b)); design coefficients t_s / t_b and loop / bus lengths L_SLR, L (no parameter; they
  are in the labels).
- Parameter sweeps of Figs. 3, 5, 6, 9, 11 (curves only; only the nominal points are entered for the zig-zag BPF).

Judgment calls:
- Parallel MC-SLR Fano device as `resonator.other` (hybrid FIR / IIR, not a pure Fabry-Perot cavity; wu2018 cascaded
  SLRs were `resonator.photonic_crystal`, D454). Coordinator may prefer `photonic_crystal`.
- Switching unit as its own `switch_fabric.other` row (D158 / D407, D396 cross-note) although Table IV repeats the
  interleaver's Table III ER / IL values.
- 3-dB BW of the Table III designs = printed ratio x printed CS; 1-dB BW of the 50 / 200 GHz designs likewise
  (arithmetic on simulated values stays `simulated`, D83f; formula in notes). The 100 GHz 1-dB BW uses the direct
  Table II GHz values.
- Comparison designs (MZI interleaver, four comparison BPFs) entered as design rows: the paper designs and simulates
  them itself (bai2023 comparison-row precedent).
- IL scope `per_component` with excludes "fiber / chip coupling" for all simulated filter transmissions.
- Thermal drift ~64 pm/K read off the simulated Fig. 8(c) line (lambda_1 at dT = 0 to lambda_2 near 12.5 degC);
  rests on a cited dn/dT; kept `simulated` with reading uncertainty +/- 3 pm/K.
- Table IV footnote points to "Fig. 9b" for points A-D; they are in Fig. 8(b) (noted).

## lit:yang2018a (4 components, 16 metrics)

| component | class | metrics |
|---|---|---|
| ridge_ring_d4p3mm | resonator.ring, silica | Q0 120 M (TE), 205 M (TM) linewidth fits; ring-down Q_L 214 M (measured) and Q0 230 M / 216 M; FSR 15.2 GHz (D1/2pi); radius ~2150 um (derived); bus width ~900 nm; silica thickness ~8.5 um |
| soliton_comb_15ghz | laser.comb, silica | repetition rate ~15.2 GHz; parametric oscillation threshold ~2 mW (waveguide coupled) |
| brillouin_laser_d6mm | laser.other, silica | threshold ~0.8 mW in the waveguide, pumped near 1550 nm; radius ~3000 um (derived) |
| sin_bus_facet | fiber_chip_coupler.edge, sin | coupling ~25 % lensed fiber to SiN waveguide (per_facet, method unspecified); width 3-3.5 um; thickness ~250 nm |

Not entered: D2/2pi = 6.4 kHz (dispersion, no registry parameter, D81); pump power as low as 61 mW for stable
soliton operation (no parameter; not a threshold); FROG pulse period 66.5 ps (= round-trip time, no pulse width
printed); Brillouin "Hertz-level" linewidth (no number); first-Stokes power (Fig. 4 inset only, clamped by cascade);
pump-Stokes beat note near 10.88 GHz (axis label); Q of the 6.0 mm Brillouin devices (not reported); simulated
single-mode cutoff width ~1200 nm (Fig. 6).

Judgment calls:
- All intrinsic Q values (linewidth fits and ring-down Q0) `author_estimate` per D403: the coupling regime is neither
  stated nor determined from the data (fixed pulley bus; unlike lee2012, no gap sweep). The ring-down loaded Q 214 M
  is `measured` (Fig. 2(c) label; consistent with tau = 0.35 us amplitude decay). Coordinator may revisit if the
  journal version states the regime.
- Ridge ring as `resonator.ring` (annular ridge after the interior ring-aperture undercut; the paper says "ridge
  ring"); lee2012 wedge disks of the same group are `resonator.disk`.
- Wavelength for the Q and coupling rows: `c_band` with `wavelength_inferred` (Q scans print no wavelength; mode
  family measured 1530-1580 nm, pumping near 1550 nm).
- Fab `org_caltech` from the author-contributions statement (KYY, DYO, SHL fabricated; all Caltech). Facility
  `org_kavli_nanoscience_institute`: KNI is acknowledged in the same sentence as the DARPA DODOS award; entered as a
  borderline facility acknowledgement (D80c), flagged for the audit (could be read as a program acknowledgement,
  D83e). Staff thanks (PECVD SiN process, ALD, SEM) not used.

## lit:lake2016 (2 components, 9 metrics)

| component | class | metrics |
|---|---|---|
| gap_microdisk_d6p52um | resonator.disk, platform other | unloaded Q 1.1e5 (TE{27,1,1}, ~1545 nm) and 2.8e4 (TE{19,3,1}, ~1554 nm), author_estimate (D403); Q ~9600 at 772.2 nm (q_loaded, unqualified); fitted Q_t ~1.0e4 (derived); radius 3.26 um (derived) |
| gap_microdisk_shg | frequency_converter.shg, platform other | normalized outside efficiency 44 %/W (4.4e-4 /mW, best point at Pcrit 0.35 mW), 38 %/W (fit, 3.8 +/- 0.2e-4 /mW), 17.8 %/W (low P); absolute efficiency 0.015 % (1.5e-4) |

Not entered: calculated GaP thermo-optic coefficients and differential tuning coefficient eta (0.176 calculated,
0.181 fit; no registry parameter); SH detuning estimates -34 to -28 pm; Pcrit 0.35 mW (in conditions only); third
harmonic generation (not quantified); disk thickness (not stated).

Judgment calls:
- Two printed maxima: 4.4e-4 /mW at Pcrit (body, p.4) vs 3.8e-4 /mW in the abstract (">") and conclusion ("maximum
  ... for P = Pcrit"), which is the Fig. 4(c) fit of scaled data. Both entered with their definitions; 44 %/W carries
  `statistic: best`.
- All /mW efficiencies converted to %/W (x 1000 x 100) and the absolute fraction to % -> `derived` (D82d). The 38 %/W
  fit value rests on model scaling (D76) and is `derived` in any case.
- `ref_plane: fiber` for the efficiencies: powers are fiber-taper powers immediately before / after the disk with
  asymmetric taper loss accounted (p.3).
- Platform `other` (suspended GaP microdisk; substrate not stated, not in the enum; hausmann2014 diamond precedent).
  Platform could instead be left empty under D422 if the coordinator reads "GaP microdisk, undercut" as not stating a
  platform.
- Fab / facility empty: "fabricated following Mitchell et al." names no org (D80b); acknowledgements are individuals
  and funding agencies (NRC, CFI, iCORE/AITF, NSERC, CNPq), not facilities.

## Missing fab / facility orgs

None. org_caltech and org_kavli_nanoscience_institute exist in the registry. lake2016 and arianfard2020 name no
fabricating org or facility.

## Registry gaps (skipped values + proposed definitions)

- `slope_rate_db_per_nm` (resonator / wdm): ER divided by the wavelength separation of the Fano peak and dip.
  arianfard2020 389 dB/nm (p.5, simulated).
- `nrmsd_pct` (wdm): normalized RMS deviation of the passband within the 1-dB BW (flatness). arianfard2020 Table II
  (33.92 / 47.3 % MC-SLR; 55.43 / 60.09 % MZI, simulated).
- `group_delay_ps` (wdm, resonator): peak group delay of a filter passband. arianfard2020 about 18 ps (Fig. 10(b),
  simulated, figure reading).
- `dispersion_d2_khz` (resonator): second-order dispersion D2/2pi of a mode family. yang2018a 6.4 kHz (p.5, measured);
  D81 rejected dispersion earlier, listed only as a confirmed skipped value.
- Laser soliton-operation pump power (laser.comb): minimum pump for stable soliton operation. yang2018a 61 mW (p.5).
