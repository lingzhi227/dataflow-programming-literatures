# A constructive compiler design for Pragma

This design synthesis accompanies the [full survey](spatial-hls-survey.pdf), especially Sections 4–11. It is proposed research; implemented evidence is identified separately below.

The compiler should preserve a mathematical operation while exposing **alternative algorithms, communication organizations and finite realizations**. A numerical graph followed by one placement pass is too restrictive. For example, an LU invariant can change when panels are updated; QR can maintain a streaming triangular factor or reduce block factors along a tree; a shared FIR read can become propagation or buffered temporal reuse.

## Representations and transformations

| Level | Retained structure | Constructive decisions |
|---|---|---|
| Algorithm | Domains, formulas, state transitions, effects and numerical policy | Invariants, factorizations, reduction objects and traversal alternatives |
| Spatial organization | Dependence relations, shared-value equivalence, interfaces and delayed state | Localization, projection, tiling, folding, permutation absorption and retiming |
| Finite plan | PE ownership, addresses, live allocations, routes, ports and event order | Resource assignment, buffering, local schedules, overlap and compact control |
| Target program | Native local code and communication semantics | CSL tasks/DSDs, AIE ObjectFifo/DMA or Metalium circular-buffer/NoC operations |

These may be separate IRs or structured views inside one infrastructure. The important requirement is preservation of the information needed by transformations and downstream consumers. A common representation is useful only if its operations still have precise semantics.

The historical basis is constructive, not merely diagnostic. [Chandy–Misra](https://doi.org/10.1007/BF01661171) and [FLAME](https://doi.org/10.1145/504210.504213) derive programs from invariants. [Alpha du Centaur](https://doi.org/10.1109/ASAP.1991.238911) transforms recurrence equations through localization and control generation. [Wong–Delosme](https://doi.org/10.1016/0743-7315(92)90111-Y) shows why broadcast propagation must be chosen with geometry and global cycles in mind. [SPIRAL](https://spiral.ece.cmu.edu/pub-spiral/abstract.jsp?id=1) searches algorithm formulas; [HSPL](https://doi.org/10.1145/2159542.2159547) already expresses hardware streaming and iterative reuse. These contributions rule out claiming the general idea of algebra plus spatial search as new.

## What must cross a region interface

A region interface should identify logical coordinates and value versions, element type and numerical relation, ownership/layout, production/consumption patterns, externally visible effects, and completion/reclamation conditions. State initialization and reset are part of the interface. Unknown dynamic rates must remain unknown or constrained by explicit predicates.

The same high-level event order can have different implementations. CSL activation and blocking state can form a join; IRON object acquisition and release express managed buffer availability; a Metalium reader reserves slots, completes NoC reads and publishes them. None licenses replacing every completion with remote-consumer completion. The actual backend adapter must state the relation.

## Search and acceptance

Optimization can explore partial or temporarily infeasible candidates. Final acceptance requires established value/effect semantics, an admissible numerical policy, dependence order, memory/resource feasibility and the relevant safety/progress conditions. An exhausted search is unresolved, not proof of infeasibility.

Cost feedback should identify the failed design choice: a congested cut, a boundary arithmetic bottleneck, overlapping live allocations or instruction-store expansion. It can then motivate a different algorithm, localization basis, tile, reduction tree or interface. Local SRAM capacity, bandwidth and issue throughput are separate constraints; aggregate wafer capacity cannot replace per-PE checks.

## Existing prototype and next implementation

The inspected publication baseline is [dc14c0d](https://github.com/lingzhi227/MIMD_dataflow/tree/dc14c0df54b12cb9e47ae710e2215084154c9570). It already has restricted typed input, numerical policies, family-specific graph verification, resource/lifetime checks, CSL generation and historical bounded qualifications. Family-specific dispatch is not itself a defect, but it constrains how new graph families are added. Existing physical region composition must also be distinguished from generic algorithm construction.

The survey adds a finite event-protocol IR and state explorer, a SUMMA-specific abstraction relation, an unfolded schedule witness and an exact four-point FFT/layout witness. One existing SUMMA profile was compiled and run in SDK 2.10.1; its frozen inputs, outputs and numerical audit are public. These are [bounded supporting results](https://github.com/lingzhi227/MIMD_dataflow/blob/main/docs/research/spatial-contracts.md), not a completed general compiler or a SPIRAL/AIE/Metalium execution result.

A manageable next implementation would select one source contract with two materially different organizations, make their region interfaces explicit, and realize both through a checked CSL adapter. FIR and factorization are useful tests of whether algorithm construction has become a compiler capability. A later target adapter would preserve the source observations through its own native primitives. This staged implementation strategy does not narrow the broader research scope, and is not an instruction to restart the frozen experiments.
