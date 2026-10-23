# Coordinator rulings for the full-corpus supply review (2026-10-23)

Rulings on questions raised by the full_02 .. full_13 reviewers. The merge owner applies them consistently across all
batches before `--merge` (edit review lines where a batch deviates; record in DevLog-003 as D340-D349).

| # | Question (batches) | Ruling |
|---|---|---|
| R1 | "Samsung Foundry" (full_05 held, full_08 mapped) | Map to `org_samsung_electronics` (business unit; printed form in notes) in every batch |
| R2 | Stanford facilities printed specifically (SNSF / SNF) while the EO import row carries the umbrella `org_nano_stanford` (full_09) | Keep the specific facility_use fact lines (more specific, printed); the umbrella import row stays; not `covered` |
| R3 | Authors' own company / institute as maker (full_05, full_08, full_09) | Fact only when the text explicitly credits fabrication or processing by that org (Intel Fab11x, imec, IME MPW, AIST pilot line, Fraunhofer IZM); otherwise `own_org` / `affiliation` |
| R4 | Network equipment, coherent pluggables, routers, GPUs, datasets (full_05, full_06, full_08, full_09, full_10 split both ways) | Network / transport equipment and commercial modules used in the experimental setup (transponders, ROADMs, OCS, pluggables, line systems) are entered as top-level H with note "category: network / transport equipment in setup" (as full_06 / full_10 did); batches that skipped them (full_05, full_08, full_09) get the missing lines added by the merge owner from their reports. Pure compute / IT gear (GPUs, CPUs, data-centre switches used for compute) and datasets are not entered. Owner question: a dedicated node later |
| R5 | Commercial modulators used in a test transmitter (full_05, full_08, full_09) | C7 with role laser_source (as the reviewers did), note "test-setup modulator"; consistent across batches |
| R6 | FPGA / RFSoC boards as DAC / ADC (full_08) | H6, or top-level H with a note when not clearly a DAC / ADC role |
| R7 | Models printed without a vendor in recall (no candidate, full_05) | Not entered (no vendor inference without a scanner candidate's infer_ok); keep the list in batch notes |
| R8 | Vendor-only lines colliding on usage_id (full_08) | Merge into one line (as done) |
| R9 | Supplementary sections after the reference list not scanned (cai2025, wilson2019; full_05) | Scanner fix (zoning must resume after the reference list when a supplementary heading follows), then a targeted rescan of affected sources only; new candidates go to a small follow-up batch |
| R10 | Reliability equipment (Espec chamber, peel tester; full_09) | Top-level H with a note (I3 stays standard_reference only) |
| R11 | Explicit org_id for printed variants of registry orgs (R&S, HP, Oxford -> Oxford Instruments, ITRI, AGC, ...) | Accepted when the printed form is unambiguous in context; record the printed form in notes; frequent variants become aliases in the next org round (scoped where ambiguous, e.g. "Oxford") |
| R12 | Models printed without a catalogue letter ("Keysight 8199B", "M8195", "2901B") | Kept as printed (never completed from catalogue knowledge); product identity follows the printed model (D317 covers a missing suffix only) |
| R13 | Company platform papers (all authors at the fabricating company) | Same as R3: fact only when the paper names the fab / platform together with a fabrication statement (Intel Fab11x, STMicro PIC100G, TSMC CoWoS-R, ASE, Solinide, Sandia, imec); thanks to a fab team for "support" only is not a fact |
| R14 | Facilities renamed since the paper (Georgia Tech IEN -> Institute for Matter and Systems) | Held under the printed name; the rename goes to the next org round as an org_event candidate, never an alias |

R4 follow-up items reported as skipped (merge owner re-reads these at their locators and adds lines per R4):
full_08: ofc2026 Tu2K.2 (Ciena 6500 line system, Waveserver 5, WaveLogic 5 Extreme), ofc2026 M1B.5 (Nokia 800G ZR OSFP,
IXR-6e router; acknowledgement says Nokia provided them), ofc2026 M1A.3 (Lumentum ROADMs; the Edgecore switch is
compute / IT -> skip). full_09: the Nokia routers / transport nodes and the Broadcom CPO switch it skipped (search the
batch's ofc2026 sources for Nokia / Broadcom). full_05: M2K.3 Lumentum CFP2-DCO and M3J.2 NeoPhotonics CDM were entered
as top-level C: keep C (component products), consistent with C7 modulators (R5).

R4 amendment (after full_04): split by product type. Pluggable / transceiver / transponder / CDM / ICR modules are
component products -> top-level C with note "category: commercial module in setup" (role laser_source is not implied
unless the module is the light source; use the role the validator allows for C and say so in the note). Line systems,
ROADMs, routers, optical circuit switches -> top-level H with note "category: network / transport equipment in setup".
Compute / IT gear (GPUs, CPUs, data-centre switches) and datasets -> not entered. The merge owner harmonizes every batch
to this split (full_04 Nokia transponder -> C, Edgecore switch -> skip; full_06 Arista transceiver / Nokia transponder
-> C; full_10 ROADMs / Polatis OCS -> H, transponders -> C).
R11 note: the printed bare "Oxford" for an instrument maps to org_oxford_instruments; the matcher's bare "Oxford" ->
org_oxford (university) route needs a scoped alias fix in the next org round.
| R15 | Co-author company products (full_02 AMAT / EVG / ZEISS tools, full_07 DuPont / Brewer / AMAT, full_04 stricter) | A named product of a co-author company used in the work is a fact (D296), whatever the authors' affiliation; the company's fab or process line as fabricator needs an explicit fabrication statement (R3 / R13). Harmonize full_04 to this |
| R16 | Stanford facilities (full_07 marked covered by the umbrella import) | R2 wins: specific printed facilities are fact lines; change full_07's verdicts accordingly |
| R17 | Printed vendor name variants (Minicircuit / Mini-Circuits, FEMTO / Femto, PANalytical / Panalytical, PriTel / Pritel, Woollam / J.A. Woollam) | One org request per vendor with all printed variants listed; the org round adds the variants as aliases (printed forms) |
| R18 | Recall lines in OFC papers without a candidate | Locator p.~N computed from the page markers (as full_07 did); pNA only when the text has no marker before the statement |
| R19 | Product names of the authors' own company printed without the vendor (AMAT "Reflexion LK Prime" / "Producer", full_11 skipped, full_02 entered) | A fact needs the vendor printed with the item, in a trademark / registered-mark notice, or in a reference the paper cites for the item (lit:nevlacsil2020 / xu2022 precedent); the affiliation line alone is not enough. Harmonize full_02 (pk 00096 / 00130 AMAT lines, EVG lines where EVG is not printed with the item) |
| R20 | Same probe / instrument printed with full part number vs base model (MPI T110A-GSG0100 vs T110A) | Keep each as printed (R12); product_line only where printed (D326); the products stay separate unless the printed strings fold to the same canonical model |
| R21 | "Thermo Scientific" resolving to org_fei through the gazetteer (full_12 HAAKE RheoStress 6000) | Wrong: Thermo Scientific is a separate brand (owner Thermo Fisher Scientific); fix the gazetteer (no Thermo Scientific -> FEI mapping; FEI stays FEI as printed); the line is held until a Thermo Scientific / Thermo Fisher org exists (next org round) |
| R22 | "Lumerical" printed bare or possessive ("Lumerical's MODE", "Lumerical FDTD") | no_vendor unless the paper prints the company ("Lumerical Inc.", "Ansys Lumerical") with the item or in a cited reference (xu2022 precedent); Lumerical is an Ansys product line since 2020, so the old company id must not be assigned from the product name. Harmonize full_12 (possessive lines -> no_vendor) and any other batch |
| R23 | Discrete electronic dies used in test vehicles (Nuvoton MOSFET, ELSPES capacitors; full_13) | Not entered for now (no category node); listed in batch notes; owner question with R4 |
| R24 | Standards / implementation agreements used in the method (OIF 400ZR frame, full_13) | Fact in K with role standard_reference (the build allows it; add it to the contract table) |
| R25 | Measurement services named without a product ("for high-speed measurements"; full_13) | Not entered (no role); no line |

R4 follow-up additions: full_13 skipped network gear in ofc2026 Th2A.34 (ADTRAN Quadflex / MNC -> C or H per the R4
split; Edgecore / Mellanox switches -> compute / IT skip), Th1C.2 (Arista 7060X6 switch -> skip), W3K.6 (ThinkQuantum QUKY
QKD -> H; Cypress SRAM / FortiGate -> skip), M4A.2 (TIP Phoenix transponder -> C; NEC NOS software -> J if vendor printed).
