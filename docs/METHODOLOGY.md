# Review methodology and limits

**Question:** how should Pragma evolve from bounded, validated examples into a reusable compiler for stateful numerical computation on a spatial machine?

Review date: 10 September 2026. This is a design-oriented curated review, not an exhaustive systematic census, independent benchmark reproduction or novelty proof.

## Sequence and evidence

1. **Frontier discovery:** identify at least ten relevant recent works, while retaining earlier foundations. Search full titles and topic combinations around dataflow, spatial compilation, HLS, resource sharing and wafer execution.
2. **Landscape:** build an initial 36-paper selection spanning 1972–2026. Primary discovery roots include conference proceedings, institutional/author pages, arXiv and official project repositories. No citation counts are invented.
3. **Full-text review:** read eight main bodies: Kahn, Dennis/Misunas, Kung, Allo, MACH v1, AIR v1, TL v1 and WaferLLM. Dennis replaced Lee/Messerschmitt in the full-reading set after direct PDF access failed. References/appendices are covered only as stated in each note.
4. **Implementation audit:** inspect pinned source/documentation for Allo, AIR, DaCe, Calyx and WaferLLM, plus the Pragma publication snapshot. No toolchain was built or run.
5. **Synthesis:** compare semantics, mapping, interfaces, finite resources and qualification scope; formulate falsifiable design questions.
6. **Report and collection:** publish the proposal, bibliography, notes and permission-checked mirrors.

Two follow-up records raised the final catalogue to 38: **Dato** because the current Allo repository cites it, and the **2026 Dynamatic/MLIR experience report** because it bears on infrastructure choice. Their reading labels remain targeted. The locally configured paper-discovery helper was unavailable; primary-source web discovery was used instead. No proprietary paper database is implied.

## Limits

- Eight full main-text readings do not mean 38 full reviews. Download status and reading depth are independent.
- Source inspection is bounded to named files at named commits. README claims are not reproduced experiments.
- A public code licence is not a PDF licence. See the separate attribution manifest and access report.
- Literature venues, versions and current implementations can differ. TL v2 is acknowledged but the detailed review concerns v1.
- The selection emphasizes Pragma's compiler design. It undercovers tagged-token history, formal concurrency literature beyond the selected models, complete numerical-method families, production multi-user serving and closed commercial compiler internals.
- Performance figures in reading notes belong to the original authors' evaluated configurations. They do not describe Pragma performance or establish a universal device ranking.

The proposal's architecture, acceptance tests and migration choices are editorial synthesis. They should be evaluated experimentally before being described as implemented or proven.
