# SPIRAL, transform algebra, and spatial HLS

SPIRAL is directly relevant to this project. It provides a mature answer to a question that a tensor-graph prototype can overlook: **which algorithm should be implemented, and which algebraic structure should remain available while implementation decisions are made?** This note distinguishes historical paper results, inspected source, and our proposed transfer to programmable PE arrays.

## What the original work contributes

Xiong, Johnson, Johnson and Padua's [SPL compiler (PLDI 2001)](https://spiral.ece.cmu.edu/pub-spiral/abstract.jsp?id=9) represents signal-transform algorithms as structured formulas and compiles them to C/Fortran. The accompanying [SPIRAL overview (Proceedings of the IEEE 2005)](https://spiral.ece.cmu.edu/pub-spiral/abstract.jsp?id=1), especially its system overview and search discussion, treats both algorithm selection and implementation choices as optimization variables. A search space of decompositions is richer than choosing a tile size for one fixed implementation. Empirical timing guides the search; it does not prove optimality over every mathematically possible algorithm.

Franchetti, Voronenko and Püschel's [Sigma-SPL paper (PLDI 2005)](https://spiral.ece.cmu.edu/pub-spiral/abstract.jsp?id=3), sections 3–4 and Tables 1–3, makes loops and index maps explicit. A gather `G_f` denotes `y[i]=x[f(i)]`; a permutation has a bijective index map. This lets a permutation compose into an adjacent gather instead of surviving as a separate array pass. The general structural rewrite is followed by domain-specific index simplification; the paper does not claim that every complicated index function automatically becomes cheap.

Milder, Franchetti, Hoe and Püschel's [hardware-generation paper (TODAES 2012)](https://doi.org/10.1145/2159542.2159547), sections 3–4, extends SPL to HSPL with **streaming reuse** (parallel copies replaced by one unit used over time), **iterative reuse** (cascaded stages replaced by a feedback datapath), and streaming permutations. It represents width/depth choices and lowers them to RTL. Its buffer and feedback treatment is essential prior work for this survey, rather than an incidental historical reference.

## A complete small derivation

Use the negative-exponent, unnormalized DFT convention. Let

`F2 = [[1,1],[1,-1]]`, `D = diag(1,1,1,-i)`, and `(P*x) = [x0,x2,x1,x3]`.

Then

`F4 = (F2 ⊗ I2) D (I2 ⊗ F2) P`.

Following the expression from right to left gives:

1. Gather the even and odd inputs: `[x0,x2]` and `[x1,x3]`.
2. Apply two independent butterflies, obtaining `e0=x0+x2`, `e1=x0-x2`, `o0=x1+x3`, `o1=x1-x3`.
3. Multiply `o1` by `-i`.
4. Form `y0=e0+o0`, `y2=e0-o0`, `y1=e1-i*o1`, and `y3=e1+i*o1`.

The companion command `python3 tools/check_spiral_formula.py --output build/research/spiral-four-point.json` verifies all 16 matrix coefficients using exact Gaussian integers, represented as pairs of Python integers. It does not approximate complex exponentials numerically and does not execute SPIRAL. A complete coefficient identity establishes equality of these linear maps for arbitrary complex input in exact arithmetic; implementation rounding remains a separate issue.

For first-stage butterfly j, the ordinary contiguous gather is `r_j(t)=2*j+t`. With `p=[0,2,1,3]`, composition gives `p(r_0(t))=[0,2]` and `p(r_1(t))=[1,3]`. Instead of creating a temporary permuted array, a local implementation can read the original array through those composed indices. This is the Sigma-SPL mechanism at the size-four instance, not a new optimization invented here.

## When a permutation still moves data

A logical gather does not identify a physical location. Define a layout map

`L(s) = (owner_PE, memory_bank, byte_offset, lane)`.

An index rewrite can remove a temporary array while still requiring communication. Suppose the original block layout puts x0,x1 on PE0 and x2,x3 on PE1, and stage one assigns the even butterfly to PE0 and the odd butterfly to PE1. The initial gather requires x2 to move to PE0 and x1 to move to PE1. If the producer instead supplies an even/odd distribution, these transfers can be absorbed into the interface layout; that changes the interface contract, and is not a free transformation of a fixed ABI.

After stage one, PE0 owns e0,e1 and PE1 owns o0,o1. Assign stage-two outputs y0,y2 to PE0 and y1,y3 to PE1, with the twiddle applied locally on PE1. This realization exchanges e1 from PE0 to PE1 and o0 from PE1 to PE0. The other values remain local. The result layout is frequency-interleaved across PEs. A consumer may accept that layout; a consumer demanding contiguous ownership needs another transformation or a different stage placement.

These two-word counts describe the stated scalar butterfly interfaces and fixed placement. They are not an information-theoretic lower bound for every FFT implementation. The matrix identity proves no route feasibility, bank-port availability, queue depth, or safe overwrite. Those need the physical layout and event protocols in addition to the formula.

## Space versus time is already explicit in HSPL

For an n-input block A, `I_m ⊗ A` can instantiate m parallel blocks. Streaming reuse with width w uses `w/n` parallel instances over `mn/w` input groups, assuming n divides w and w divides mn. This distinguishes algorithmic repetition from hardware replication. Indexed blocks also need to retain the iteration-dependent coefficients and controls.

A cascade of k stages can similarly reuse a depth-d block over k/d passes when d divides k. The 2012 paper's feedback analysis requires the reused datapath to buffer the full vector before its head returns to collide with the tail. Its latency/throughput formulas depend on the given fully pipelined model and whether feedback is used; they are not general predictions for a CSL task network.

For a programmable PE array, the analogous choices include PE replication, sequential local kernels, resident coefficients, feedback messages and retained state. The new work would be to preserve the formula's ordering and layout through a backend with bounded queues, local software tasks and its own completion semantics. Merely naming these choices would not advance beyond HSPL.

## Current code evidence

Inspected source is pinned to SPIRAL commit `577b2c1268476c885fbb9984b9e06174f71b5386` (retrieved 2026-09-10). No build or benchmark of this checkout has been performed.

| Source | Inspected evidence | Bound on interpretation |
|---|---|---|
| `namespaces/spiral/paradigms/common/dft.gi`, `DFT_tSPL_CT` | Applicability conditions, divisor-pair choices, tagged tensor/twiddle decomposition | A source-level decomposition rule; this inspection does not validate every enabled search configuration |
| `namespaces/spiral/paradigms/stream/rules.gi`, `DFT_tSPL_Stream` and related rules | Stream-width/radix conditions and alternative streamed DFT forms | Current code vocabulary is not assumed identical to the 2012 paper's notation |
| `namespaces/spiral/paradigms/distributed/sigmaspl.gi`, `GathRecv`, `ScatSend`, `GathDist`, `ScatDist` | Explicit distributed communication constructs with packet size, processor count and processor identity | It would be false to claim SPIRAL only handles local addressing or has no communication representation |

[The pinned distributed source](https://github.com/spiral-software/spiral-software/blob/577b2c1268476c885fbb9984b9e06174f71b5386/namespaces/spiral/paradigms/distributed/sigmaspl.gi) is particularly important for avoiding an artificial novelty claim. The inspection does not establish support for arbitrary stateful actors, nor does it establish the absence of such support elsewhere in the project.

## Consequences for the proposed compiler

A single low-level actor graph is too early a common denominator. Preserve at least three forms of algorithm structure until their transformations are exhausted:

- Iteration/dependence domains for affine numerical loops, as in GEMM.
- Structured transform formulas and symbolic index maps, as in FFT.
- Explicit state and stream contracts for dynamic or recurrent computations.

They can meet at a physical plan with typed buffers, layouts, persistent-state ownership, actor bodies and communication events. A rewrite should record the identity it uses and its side conditions, including divisibility and index-map domain/range. A layout rewrite should report any ownership changes; a backend must materialize the resulting movement or demonstrate that it was absorbed into a compatible producer/consumer interface.

Search should keep these decisions coupled. For example, a formula with fewer multiplications can require more communication; a larger streaming width can increase bandwidth pressure; loop fusion can remove a temporary but enlarge live storage or destroy a feasible bounded stream schedule. Cost functions need measured backend data and explicit feasibility constraints. A formula tree gives search structure; it does not make global cost additive or ensure that optimizing each subtree independently optimizes the composition.

The current companion implements the exact FFT identity/layout witness and the separate SUMMA protocol checker. It has **not** implemented a general SPL frontend, a SPIRAL-to-CSL compiler, or a unified three-backend scheduler. These are concrete design directions grounded in prior work, not completed functionality.

## Reading and publication scope

The technically inspected core is Sigma-SPL sections 3–4 and Milder et al. sections 2–4 (especially sections 3.1–3.5 and 4.1–4.4), plus selected source definitions above. The 2001 SPL and 2005 SPIRAL overview records provide context; no uninspected experiment is treated as independently reproduced. The essential papers are indexed in the bibliography. Their available preprints have redistribution restrictions, so the repository provides citations and links; the downloaded copies remain private study material.
