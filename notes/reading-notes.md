# Reading notes

Reviewed 2026-09-10. The initial eight main-text readings below are retained, followed by targeted readings that substantially revised the manuscript. Downloading or indexing a file is not full-paper reading. Section-level scope is also recorded in [metadata.json](../papers/metadata.json). Design implications are our synthesis.

## Kahn (1974): stream semantics

[The Semantics of a Simple Language for Parallel Programming](https://www.cs.columbia.edu/~sedwards/papers/kahn1974semantics.pdf) · [@kahn1974]

**Read scope:** Full body, five-page author copy; scanned text read with OCR. Equations in OCR are not reliable enough for verbatim transcription.

**Problem.** Define parallel programs independently of execution interleaving.
**Method.** Sequential processes communicate through ordered, single-producer/single-consumer channels. Reads block on a specified channel; sends do not block. Stream histories are ordered by prefix, and continuous process functions define a least fixed point. Compositional reasoning follows from this semantic construction.
**Evidence.** A mathematical treatment with small feedback examples, not a hardware benchmark. Fair execution matters for producing the whole history rather than only a prefix.
**Limitations.** Unbounded channels are part of the abstraction. Determinism does not establish finite-buffer executability or deadlock freedom after inserting blocking writes. Arrival-dependent choice is outside the basic deterministic model.
**Design question.** Keep mathematical stream semantics separate from a physical, bounded communication protocol; require an explicit refinement argument between them.

## Dennis and Misunas (1975): executable dataflow

[A Preliminary Architecture for a Basic Data-Flow Processor](https://www.cs.cmu.edu/~15740-f20/papers/dennis-75.pdf) · [@dennis1975]

**Read scope:** Full seven-page paper; extracted text, including decision and two-level memory sections.

**Problem.** Execute data-driven graphs with conditionals and iteration on a parallel machine.
**Method.** Instructions become enabled when operands arrive. Actors also require empty output arcs. Links duplicate tokens; decision actors, gates and controlled merges express branches and feedback. Instruction cells communicate through arbitration, distribution and control networks. Active instructions occupy a cache backed by instruction memory.
**Evidence.** Detailed architectural formats, receiver state transitions and a worked loop execution; no measured contemporary benchmark suite.
**Limitations.** The conclusion explicitly leaves arrays, concurrent procedure activation and vector parallelism for further work. This is a preliminary machine design, not proof that arbitrary graph programs map efficiently.
**Design question.** Readiness, output capacity, reset and control-token behavior deserve explicit semantics. A graph edge alone does not specify a runnable protocol.

## Kung (1982): families of systolic schedules

[Why Systolic Architectures?](https://www.eecs.harvard.edu/~htk/publication/1982-kung-why-systolic-architecture.pdf) · [@kung1982]

**Read scope:** Full ten-page article, OCR; historical numerical examples are not contemporary device estimates.

**Problem.** Obtain useful concurrency without letting communication and I/O dominate computation.
**Method.** Regular arrays retain and reuse data locally. Convolution examples compare stationary inputs, weights or results; broadcast versus local movement; and different flow rates. Designs trade utilization, temporary storage, latency and wiring complexity. Matrix factorization, stencils and other applications broaden the perspective.
**Evidence.** Architectural examples and analytical reasoning, not a modern reproducibility benchmark. Some schedules leave alternating bubbles; interleaving independent work can improve utilization at a storage cost.
**Limitations.** Finite internal memory and external I/O still bound performance. There is no universal optimal systolic mapping for all algorithms.
**Design question.** Represent an algorithm separately from its space-time mapping, with explicit communication and storage costs. Preserve several schedule families rather than equating matrix multiplication with one array layout.

## Allo (PLDI 2024): composable customization

[Allo: A Programming Model for Composable Accelerator Design](https://www.csl.cornell.edu/~zhiruz/pdfs/allo-pldi2024.pdf) · [@chen2024allo]

**Read scope:** Full main paper through conclusion/artifact, pp. 1–23; references scanned, separate supplementary material not reviewed.

**Problem.** Optimized kernels can compose poorly because interface layouts and schedules interact.
**Method.** Separate algorithms from rewrite-based compute, memory and communication customization. Replay schedules hierarchically; propagate partition types through a dataflow graph; support external HLS kernels. Functional testing is supplemented by equivalence checking for statically interpretable control flow. FIFO sizing uses producer/consumer timing.
**Evidence.** PolyBench and neural models on the U280 toolchain; GPT-2 355M uses W4A8, while the GPU comparison uses FP16. Single-request latency includes host communication. These results are not precision-identical comparisons or evidence about our compiler.
**Limitations.** Static equivalence checking excludes general parametric control. FIFO connection placement and some bufferization remain future work; physical routing still matters. The paper does not prove arbitrary bounded networks deadlock-free.
**Design question.** Adopt compositional interfaces and inspectable schedules; extend beyond memory layout to message ordering, ownership and completion on CSL.

## MACH (2025 preprint): a distributed virtual machine

[A System Level Compiler for Massively-Parallel, Spatial, Dataflow Architectures](https://arxiv.org/abs/2506.15875) · [@vanessendelft2025]

**Read scope:** arXiv:2506.15875v1, full main text and code listings; appendix acronym list inspected.

**Problem.** Program large spatial machines without replicating a complete control program in each small worker memory.
**Method.** A controller/worker virtual machine dispatches RPC kernels, with separate reduction resources. NumPy-like objects distinguish global, local and uniform values. The compiler builds hierarchical intermediate graphs and statically assigns memory using lifetimes. Workers drain argument traffic even when they do not participate in a computation.
**Evidence.** Architecture and detailed lowering examples; the paper is primarily a system/compiler description rather than a comprehensive comparative performance evaluation.
**Limitations.** The demonstrated target languages are **Tungsten and Paint**, not an established public CSL backend. Fusion, multi-wafer execution and richer runtimes are discussed as future work. Directly importing the VM could introduce controller and control-traffic overhead.
**Design question.** Evaluate reusable worker kernels and explicit control as one execution policy; include control/code storage in resource accounting. Do not describe high-level compilation to Cerebras as unexplored prior art.

## MLIR-AIR (2025 preprint): asynchronous hierarchy

[From Loop Nests to Silicon: Mapping AI Workloads onto AMD NPUs with MLIR-AIR](https://arxiv.org/abs/2510.14871) · [@wang2025air]

**Read scope:** arXiv:2510.14871v1; full main body pp. 1–30, including evaluation and future directions; appendix examples not separately reviewed.

**Problem.** Expose placement, distributed memories and asynchronous execution to a compiler.
**Method.** Hierarchical launch/segment/herd constructs describe resource grouping; channels separate transfer endpoints; tokens express ordering and loop-carried dependencies. Passes infer dependencies, broadcast, double buffering, channel merging and memory splitting. AMD lowering produces AIE resources and synchronization.
**Evidence.** Ryzen AI 7840 GEMM experiments report best throughput among repeated trials. Peak utilization depends on precision: the headline 78.7% concerns i16. The attention case is a single-core prototype with head dimension 48, sequence 256 and six time-multiplexed heads, not a complete standard LLaMA deployment.
**Limitations.** Multi-target and cross-device work remains a direction. Source-complexity comparisons vary in whether external microkernels are counted. Tokens and SSA verification alone do not establish all resource/progress properties of a new backend.
**Design question.** Reuse hierarchical async concepts, while defining CSL-specific completion and resource constraints precisely.

## TL (2025 preprint): grid-level mapping

[TL: Automatic End-to-End Compiler of Tile-Based Languages for Spatial Dataflow Architectures](https://arxiv.org/abs/2512.22168) · [@li2025tl]

**Read scope:** arXiv:2512.22168v1; full main body pp. 1–13. A v2 dated 2026-05-12 exists; conclusions here are version-specific.

**Problem.** Tile languages need an explicit mapping of logical tile instances to distributed physical cores.
**Method.** Affine memory accesses expose spatial and temporal reuse. A hardware dialect models cores, memory and interconnect. Mapping, broadcast and load-hoisting choices are pruned for storage capacity, ranked with an approximate performance model, then optionally profiled as a top-k shortlist. Intra-core code generation is delegated to TT-Metalium.
**Evidence.** GEMM and non-causal FlashAttention on Wormhole n300d; three logical array configurations use the same physical platform. Top-5 GEMM profiling outperforms the fully static top-1 selection. Reported mean prediction error is 17%.
**Limitations.** Two operators and one hardware family do not establish general multi-platform portability. Small shapes expose unmodeled overhead. Ranking estimates are not cycle-accurate performance guarantees.
**Design question.** Separate mapping legality from performance ranking; keep measured and predicted results distinguishable, and support bounded search rather than unbounded simulator tuning.

## WaferLLM (OSDI 2025): algorithms constrained by a wafer

[WaferLLM: Large Language Model Inference at Wafer Scale](https://www.usenix.org/system/files/osdi25-he.pdf) · [@he2025]

**Read scope:** Full main paper, printed pp. 257–270, including limitations; downloaded proceedings PDF includes cover and references.

**Problem.** Map LLM computation onto many small memories connected by a large mesh.
**Method.** PLMR captures parallelism, nonuniform latency, local memory and routing limits. MeshGEMM interleaves a cyclic communication schedule; MeshGEMV uses hierarchical reduction. Prefill/decode use different layouts, and KV shifting balances storage across neighboring cores.
**Evidence.** Hardware experiments on WSE-2, including complete LLaMA3-8B and LLaMA2-13B. Results for 34B/72B use subsets of layers with scaled estimates. The GPU comparisons target per-request throughput rather than a general multi-user serving objective.
**Limitations.** Pipeline bubbles and local-memory constraints remain. Reported KV capacity gains concern the compared wafer mapping, not a universal storage advantage over PagedAttention. Broad device forecasts and comparative assertions need separate evidence before reuse.
**Design question.** Make algorithm families, layout transitions and persistent state first-class; never promote a kernel result or extrapolated model result into an end-to-end qualification claim.

## Constructive algorithm design: targeted expansion

The local systolic library index contained 120 PDF files, including books, duplicate versions and theses. Tables of contents and selected originals guided the audit. The selection retained methods that change algorithm construction: invariant choice, localization, space/time allocation, retiming and stateful numerical organization. It did not treat the index as 120 fully read papers or as a required citation quota.

**Program invariants — Chandy and Misra (1986).** The repeated program is a simultaneous multiple assignment, so all right-hand sides observe the old state. Step-indexed invariants derive flow timing and initialization while the program is constructed. This differs from proving a hand-drawn network correct afterward, and does not itself solve physical resource assignment. Read Sections 1–2.5 and the beginning of the band-matrix example; not the complete LU derivation. [Original](https://doi.org/10.1007/BF01661171).

**FLAME — Gunnels et al. (2001).** The partitioned postcondition exposes partial results that can serve as loop invariants. The five presented LU invariants generate algorithm alternatives under the paper's progress assumptions; they are not an exhaustive enumeration of all factorizations. The survey derives the spatial implications of maintaining a Schur complement eagerly versus delaying a panel update. Original article pp. 427–432, corresponding to PDF pp. 22–27 of the later 318-page collected TOMS volume; the entire collection was not read. Unpivoted LU needs valid pivots, not merely a nonsingular full matrix. [Article](https://doi.org/10.1145/504210.504213).

**Equation synthesis — Dezan et al. (1991).** Alpha du Centaur carries equations through reindexing, communication localization, I/O pipelining and control generation toward circuit forms. Index transformations must change domains and all affected occurrences. Time-dependent conditions require control streams; PE-only conditions can specialize cells. Read printed pp. 324–330 and the start of the correlator example. No tool or chip reproduction. [Article](https://doi.org/10.1109/ASAP.1991.238911).

**Broadcast propagation — Wong and Delosme (1992).** The subject is a restricted affine-dependence class with translations and rank-deficient broadcast maps. The general construction needs more than choosing one nullspace vector: unimodular bases and conditional propagation directions establish reachability. Selecting a useful basis also involves geometry, path lengths, inverse-basis entries and global cycle displacements. The sufficient linear longest-path criterion is not a universal deadlock test for finite software queues. Read Sections 1, 2.1, 3.2 (including Theorem 4's proof) and 4.1–4.3; not every canonical-form proof or reported experiment. [Article](https://doi.org/10.1016/0743-7315(92)90111-Y).

**Allocation and time — Rao and Kailath (1988).** Processor projection and scheduling are different maps. Variable-specific affine offsets can order zero-displacement dependencies that a shared purely linear schedule cannot. Their global-step abstraction admits at most one computation of each variable kind per processor per step, rather than one machine instruction. Changing a projection basis can preserve grouping while changing physical edge geometry. Read the introduction, regular-iteration definitions and original pp. 264–267; not the full appendix. [Article](https://doi.org/10.1109/5.4402).

**Retiming — Leiserson and Saxe (1991).** Integer vertex lags move registers through a fixed synchronous graph. Edge nonnegativity and invariant cycle-register totals define a precise legal transformation space; optimizing that space differs from changing the recurrence or adding arbitrary FIFO depth. Sections 2–3 were read. The paper refers its functional-equivalence proof to earlier work; the survey does not claim to have checked that separate proof or initialized software-channel equivalence. [Article](https://doi.org/10.1007/BF01759032).

**Streaming triangularization — Gentleman and Kung (1982).** Boundary cells generate elimination parameters; interior cells apply them. Givens boundary square roots/reciprocals can limit common throughput, motivating different arithmetic formulations and, for discussed square-root-free forms, scaling and extra diagonal communication. The survey's rotation equations use an independently specified sign convention and zero case. Read the general-array, orthogonal-triangularization and on-the-fly least-squares sections. The event was in 1981, but SPIE publication/copyright is 1982. [Article](https://doi.org/10.1117/12.932507).

**Interval DP — Dhrif and Sarkar (1992).** The matrix-chain recurrence has regular candidate domains despite a value-dependent minimum. The linear organization stores staged diagonal results; the mesh overlaps diagonals and forwards completed values. Their six-neighbor, synchronized/unit-step model matters to the asymptotic statements. Constant local computation state does not price an arbitrary independently supplied weight table or all reconstruction outputs. Read Sections 1–2, 3.1–3.3 and 4.1–4.3. [Article](https://doi.org/10.1080/00207169208804035).

**Stream and memory endpoints — iWarp (1990).** Program-access gates expose communication queues in the register namespace, while logical channels multiplex physical links. Memory-buffered and direct-stream endpoints can be combined for one message. These are different access and resource organizations, not names for one universal send API. Read Sections 2–3.2; no processor reproduction. [Article](https://doi.org/10.1109/ISCA.1990.134510).

## Additional formal and compiler readings

| Source | Inspected scope | Finding used in the manuscript |
|---|---|---|
| Karp–Miller–Winograd (1967) | Sections 1–3: definitions and scheduling statements | Equation kinds differ from dynamic lattice instances; free/unit-time scheduling is not fixed-PE allocation. |
| Alpha (1991) / Wilde RR-2295 (1994) | 1991 publisher record/related introduction; 1994 domain/type/denotation, affine dependence and reductions | Reindexing must transform domains; unbounded-precision reduction laws need a separate machine numerical policy. |
| Lee–Parks (1995) | Stream semantics and actor/coordination distinction | Continuity and deterministic stream meaning do not establish finite-buffer progress. |
| Geilen–Basten (2003) | Sections 2–5 | Bounded/effective KPN assumptions, local artificial deadlock and maximality against the unbounded network delimit the positive scheduling result. |
| Stuijk et al. (2008) | Timed-CSDF model and throughput/buffer exploration | Output reservation and input-credit return occur at different firing boundaries; the conservative abstraction has stated timing conditions. |
| Feautrier (1992) / Vivien (2002) | Feautrier primary records; Vivien Sections 2–5 | Minimal affine schedule dimension is a restricted optimality claim, not physical latency optimality. |
| Rau (1994) | Primary record and abstract only | Used as historical attribution for modulo scheduling; no full-paper or implementation claim. |
| Raw (1998) | Sections 5–6 | Computation and communication instructions are scheduled together; delay tolerance relies on a good initial schedule and static ordering. |
| DRESC (2003) | Sections 2–3 | MRRG couples placement/routing/time. Penalized temporary overuse is a search mechanism, not an accepted physical implementation. |
| Halide (2013) | Sections 2–3.2 | Fusion, storage and recomputation trade off locality and parallelism. |
| Exo (2022) | Sections 2.4, 3, 4 and 5.1–5.5 | Real-number core, restricted control and configuration effects delimit checked rewrites; user-provided instruction semantics remain trusted. |
| DaCe (2019) | Sections 3–4.3 | State transitions, explicit data movement and scopes are more expressive than a stateless tensor DAG. |
| Calyx (2021) | Sections 2.2–4.2 | Structural hardware and explicit control/completion make different decisions visible. |
| TACO (2017) | Sections 3–5 | Storage formats determine iteration order; merge lattices express union/intersection cases; the original iteration-graph restriction matters. |
| ATL (2022) | Sections 3, 6.1 and 9 | Verified real-valued tensor rewrites are distinct from verified end-to-end spatial lowering. |
| CRUSH (2025) | Sections 3–4.3 | Credit-based sharing preserves the relevant property from a deadlock-free pre-sharing circuit under its model. |
| ElasticMiter (2025) | Sections 2.2, 3 and 4.1–4.3 | Equivalence considers input consumption as well as output values and includes eventual-propagation/context assumptions. |
| IRON (2025) | Sections II–V and pinned ObjectFifo sources | Worker code and object availability are distinct layers; current source must be distinguished from the paper's version. |
| FlashAttention (2022) | arXiv v2 Sections 2.2/3.1, Algorithm 1 and theorem statement | Blocking maintains rescaled normalization statistics; the survey derives the merge relation and its valid-state conditions. |
| Demmel et al. (2008), LAWN 204 | Sections 4.1 and 5.3 plus surrounding tree discussion | A reusable QR factorization retains transformations and their tree association. Not a complete reading of the 136-page report. |
| Templates (1994), second edition | Netlib CG and computational-aspects sections | Inner products synchronize distributed iterations; preconditioners have different communication graphs. Not a complete-book rereading. |

Exact source URLs and bibliographic identities are in [metadata.json](../papers/metadata.json). The SPIRAL/SPL/Sigma-SPL/HSPL reading and worked transform are detailed in [spiral-and-spatial-hls.md](spiral-and-spatial-hls.md). The source/section scope above limits claims; a listed implementation was not automatically built or tested.
