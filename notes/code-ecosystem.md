# Compiler implementations and Pragma

Snapshot date: 2026-09-10. Read-only inspection of pinned source files and documentation. None of these toolchains was built or benchmarked for this report. Stars are a dated discoverability metric, not evidence of correctness.

## cornell-zhang/allo

- Repository: https://github.com/cornell-zhang/allo
- Commit: `8bafb0dcee27c96a72872184d2b106c59c8a1414`
- Stars: 409; primary language reported by GitHub: Python.
- Last push reported: 2026-09-08T03:56:54Z; license: Apache-2.0.
- Documentation assessment: Strong: installation, tutorials, backend docs and examples.

Inspected Schedule.compose and the dialect declarations. Composition replays primitives and updates function/buffer references; current code also distinguishes stateful globals across instances. Useful for hierarchical schedules and explicit interfaces. The current README cites Dato for task-based dataflow; the 2024 paper alone is not a complete description of the current project.

Inspected sources:

- [README.md](https://raw.githubusercontent.com/cornell-zhang/allo/8bafb0dcee27c96a72872184d2b106c59c8a1414/README.md)
- [mlir/include/allo/Dialect/AlloOps.td](https://raw.githubusercontent.com/cornell-zhang/allo/8bafb0dcee27c96a72872184d2b106c59c8a1414/mlir/include/allo/Dialect/AlloOps.td)
- [allo/customize.py](https://raw.githubusercontent.com/cornell-zhang/allo/8bafb0dcee27c96a72872184d2b106c59c8a1414/allo/customize.py)
## Xilinx/mlir-air

- Repository: https://github.com/Xilinx/mlir-air
- Commit: `47af4e590d0c501bcd901d9d8c0d45d3829d8a90`
- Stars: 147; primary language reported by GitHub: Python.
- Last push reported: 2026-09-10T09:08:26Z; license: MIT.
- Documentation assessment: Strong: compute model, dialect/pass reference, runtime and target-specific examples.

Inspected AIR channel definitions. Channels have explicit backend mechanisms, including DMA streams, packet routing and cascade links. Current code documents constraints and a GPU symmetric-heap form whose lowering is still planned. Current README advertises NPU/GPU lowering and expanded LLM examples; this is later than the reviewed 2025 paper. Do not label the entire current implementation single-core-only based on that paper.

Inspected sources:

- [README.md](https://raw.githubusercontent.com/Xilinx/mlir-air/47af4e590d0c501bcd901d9d8c0d45d3829d8a90/README.md)
- [mlir/include/air/Dialect/AIR/AIR.td](https://raw.githubusercontent.com/Xilinx/mlir-air/47af4e590d0c501bcd901d9d8c0d45d3829d8a90/mlir/include/air/Dialect/AIR/AIR.td)
## spcl/dace

- Repository: https://github.com/spcl/dace
- Commit: `d0382068e63487334367728ccb687efab46041e2`
- Stars: 592; primary language reported by GitHub: Python.
- Last push reported: 2026-09-10T07:08:41Z; license: BSD-3-Clause.
- Documentation assessment: Strong: tutorials, SDFG API, transformation and code-generation guidance.

Inspected validate_state: structural validation covers graph membership, acyclicity within a state, nested nodes, matching scope connectors and access descriptors. Useful precedent for diagnostics and separation between control states and dataflow within states. Structural validation is not a universal proof of backend execution correctness.

Inspected sources:

- [README.md](https://raw.githubusercontent.com/spcl/dace/d0382068e63487334367728ccb687efab46041e2/README.md)
- [dace/sdfg/validation.py](https://raw.githubusercontent.com/spcl/dace/d0382068e63487334367728ccb687efab46041e2/dace/sdfg/validation.py)
## calyxir/calyx

- Repository: https://github.com/calyxir/calyx
- Commit: `d6bcdc8707fe2f024a7b18a86523bda6f770186a`
- Stars: 613; primary language reported by GitHub: Rust.
- Last push reported: 2026-09-03T04:09:47Z; license: MIT.
- Documentation assessment: Strong: language and source documentation, compiler/IR/optimizer separation.

Inspected Control and StaticControl definitions: sequential, parallel, conditional, repeated and invocation constructs coexist with explicit static control. Useful for making orchestration visible and mixing scheduling styles. Calyx targets hardware generation; it is not an already available CSL backend.

Inspected sources:

- [README.md](https://raw.githubusercontent.com/calyxir/calyx/d6bcdc8707fe2f024a7b18a86523bda6f770186a/README.md)
- [calyx/ir/src/control.rs](https://raw.githubusercontent.com/calyxir/calyx/d6bcdc8707fe2f024a7b18a86523bda6f770186a/calyx/ir/src/control.rs)
## MeshInfra/WaferLLM

- Repository: https://github.com/MeshInfra/WaferLLM
- Commit: `fd1c2daae37cd68706c03fc8009887ecee9900f8`
- Stars: 121; primary language reported by GitHub: Python.
- Last push reported: 2026-06-12T18:28:45Z; license: Apache-2.0.
- Documentation assessment: Useful: module-specific build/run guides and communication library layout; version caveats must be read carefully.

Inspected decode CSL: explicit DSR allocation, mapped local arithmetic, KV arrays and multiple intermediate buffers. The current README targets WSE-3/SDK 2.10.0 and says original OSDI results used WSE-2/SDK 1.x. Running the current code on another target is therefore a new validation, not automatic reproduction of the paper. No experiments were run in this audit.

Inspected sources:

- [README.md](https://raw.githubusercontent.com/MeshInfra/WaferLLM/fd1c2daae37cd68706c03fc8009887ecee9900f8/README.md)
- [Decode/README.md](https://raw.githubusercontent.com/MeshInfra/WaferLLM/fd1c2daae37cd68706c03fc8009887ecee9900f8/Decode/README.md)
- [Decode/src/decode.csl](https://raw.githubusercontent.com/MeshInfra/WaferLLM/fd1c2daae37cd68706c03fc8009887ecee9900f8/Decode/src/decode.csl)

## Pragma: strengths and the main architectural boundary

Audited publication snapshot: [MIMD_dataflow at dc14c0d](https://github.com/lingzhi227/MIMD_dataflow/tree/dc14c0df54b12cb9e47ae710e2215084154c9570). This is not an assertion about uninspected development workspaces.

- `lib/Frontend/frontend.py` parses typed operations, input ranges and explicit dataflow policies. A general-purpose C++ frontend is not established by this code.
- `lib/IR/ir.py:verify` selects many specialized verification paths from operator combinations/counts and policies. This makes whole-pattern support a central mechanism.
- `lib/IR/projected_cache_ffn_ir.py:canonical` then checks the exact 35-node topology, its edges, residual structure, shared normalization, acyclic prefix and full coverage. Therefore the coarse dispatch alone is **not evidence of accepting invalid graphs**. The maintainability/generalization concern is that a new composition requires another family-specific path.
- `lib/Transforms/projected_cache_ffn_plan.py:plan` derives parent ranges and enforces specific shape, precision, 16-way sharding and operation policies. This is meaningful engineering, but is not a generic arbitrary-graph scheduler.
- `lib/Analysis/region_lifetimes.py:verify` checks declared storage overlap and resource leases. Its own scope explicitly excludes arbitrary CSL control flow, dynamic stack, compiler/SDK temporaries and diagnostic storage. The next layer should connect these declared contracts to actual lowering completion events.
- `lib/Conversion/projected_cache_ffn_codegen.py` assembles the concrete composed backend and exports its ports; the file organization is not evidence of an implemented MLIR dialect.

Retain the mathematical references, explicit precision/range contracts, bounded profiles, frozen generated sources and run receipts. Historical SDK qualification (141 bounded profiles in the publication documentation) must remain version-specific. The composed 35-node candidate is described as pending full SDK qualification in this snapshot. Neither claim was revalidated by running the SDK here.

## Benchmark reuse

Use PolyBench kernels for regular loop transformations; existing Pragma numerical solvers for feedback/state; Allo composition examples for interface changes; WaferLLM mesh operators for spatial communication; and small residual/attention graphs for persistent state and buffer reuse. Compare compiler-generated results with both a mathematical reference and pinned manual CSL. Report simulation time separately from device cycles. No benchmark suite is sufficient by itself to establish general programmability.
