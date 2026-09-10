# Reading routes

Use the [catalogue](../README.md#paper-catalogue) for links and metadata. These routes are conceptual sequences, not an implied chronological genealogy.

| Reader | Suggested sequence | Questions to carry forward |
|---|---|---|
| CUDA/GPU programmer | Roofline → Kung → Triton → TL → WaferLLM | Which locality decisions are familiar, and which become explicit across persistent distributed cores? |
| Programming-language researcher | Kahn → Dennis → Lee/Messerschmitt → StreamIt → DaCe | What is deterministic, where does state live, and which assumptions make scheduling analyzable? |
| HLS researcher | Spatial → Calyx → DASS → Allo → Dato → CRUSH/ElasticMiter | How do interfaces, control, resource sharing and transformations compose? |
| Compiler engineer | Halide/Exo → MLIR → AIR/ARIES → Dynamatic experience report | What should be a reusable abstraction, and what remains target-specific? |
| Cerebras researcher | Kung → WaferLLM → MACH → Pragma design study | Which algorithms exploit a mesh, and what must a CSL compiler verify beyond arithmetic? |

## Vocabulary

- **MIMD:** an instruction/data-stream classification; it does not prescribe a language or communication protocol.
- **Dataflow graph:** a dependency representation; specify whether its edges mean values, streams or actual bounded channels.
- **Systolic algorithm:** a structured space-time schedule emphasizing regular movement and reuse.
- **Static versus dynamic scheduling:** when execution decisions are made; a system may use both at different levels.
- **Spatial mapping:** assignment of work and data to resources across space and time.
- **HLS:** traditionally high-level program to hardware; Pragma uses the term for high-level graph lowering to programs on an existing spatial machine. Keep that distinction explicit.
- **CSL:** Cerebras' target programming language; a low-level CSL implementation is not by itself a high-level programming model.
- **SDF versus SDFG:** synchronous dataflow and DaCe's stateful dataflow multigraphs are different terms and abstractions.

The initial collection emphasizes work useful for Pragma. It does not yet provide exhaustive coverage of tagged-token machines, polyhedral theory, distributed runtime systems, numerical algorithm literature, PyTorch compiler history, or commercial serving implementations.
