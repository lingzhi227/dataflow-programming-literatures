# Phase 3: full-paper reading notes

Reviewed 2026-09-10. Eight main papers were read; downloads and selective searches are labelled separately. Notes summarize findings; design questions are our interpretation, not claims made by the authors.

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
