# Substantive research revisions

This record describes changes in the argument and evidence behind the 10 September 2026 manuscript. It is a research revision history, not a claim of external peer review or publication acceptance.

| Revision | Finding or correction | Effect on the survey/prototype |
|---|---|---|
| Scope beyond the initial collection | The initial 38-paper conceptual overview could not support a compiler-level design argument. | Replaced the short overview with a TeX manuscript, explicit mathematical objects, worked programs and source-specific assumptions. |
| Existing CSL facilities | SdkLayout already provides physical regions, ports and routing facilities. | Removed any implication that connecting regions itself was a missing or novel capability; distinguished it from algorithm/interface composition. |
| Formula-level prior art | Sigma-SPL and HSPL already express index composition, streaming permutations and hardware reuse. | Added algorithm algebra to the design, a four-point FFT/layout derivation and an explicit novelty boundary. |
| Protocol implementation review | A reader identity initially failed to distinguish a mismatched release version. | Corrected the prototype to track actor, token and version together; retained negative checks. |
| Evidence interpretation | Small integer-valued binary32 batches produce exact SUMMA observations but do not stress general rounding. | Separated indexing/version evidence, floating-point policy, simulator wall time and PE-local compute cycles. |
| Constructive breadth | The first complete 28-page draft overemphasized preservation and checking. | Audited the systolic-library index, read selected originals, and rewrote the introduction, selection thesis and design synthesis around algorithm construction plus realization. Added invariants, localization, FIR, retiming, streaming QR and interval DP. |
| FIR finite boundary | Unconditional final forwarding would produce an unmatched token after the consumer's finite output domain ended. | Specified startup seeds and exactly N consumed tokens per downstream input channel; suppressed the last forward. Distinguished average work bounds from constant integer initiation intervals. |
| Search versus acceptance | A strict legality predicate does not require a legality-first exploration order. | Explained DRESC's temporarily infeasible candidates and separated heuristic search from final acceptance. |
| Source identity and layout | Conference dates, reprints, collected volumes and current repositories are different evidence objects. Long paths and a split short listing impaired readability. | Corrected Dennis/SPIE/FLAME version notes, completed primary bibliography metadata, pinned current source interfaces and iterated the rendered PDF. |

The frozen prototype experiments were not expanded during the constructive breadth revision. The broader compiler remains proposed work. Read scope and unreplicated claims remain explicit in the [reading notes](reading-notes.md) and manuscript appendices.
