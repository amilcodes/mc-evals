# Search and optimization methods for discrete, cliff-heavy design spaces (applied to Minecraft piston doors)

Scope: which search ideas transfer to minimizing piston-door volume and/or opening ticks, given a cheap, exact pass/fail simulator where one block or repeater edit often breaks the door. Primary sources were read where possible. The STOKE (ASPLOS 2013), RoboGrammar (SIGGRAPH Asia 2020), egg (POPL 2021) and Haaswijk et al. (TCAD 2020) full texts were downloaded and read directly. Items marked UNVERIFIED come from secondary sources or memory and were not confirmed against a primary text.

## Q1. What is the precise discrete analogue of a barrier that keeps search inside the valid set?

### Takeaway
Repulsive Shells works by changing the *metric*: collision avoidance becomes part of the distance, so geodesics (shortest paths) between two valid shapes stay valid. The exact discrete analogue is a design graph G = (D, E), where D is the set of designs and E the set of edit moves, together with a valid set V ⊆ D. Search then happens either (a) on the induced subgraph G[V], meaning only validity-preserving moves (rewrite systems, constraint-preserving operators, death penalty with infinite cost), or (b) with edge weights that grow as the design's margin to failure shrinks (a discrete log-barrier). Option (a) only works if the valid set is *connected* under the chosen moves. That connectivity question is exactly what neutral-network theory and STOKE's search-space analysis study. When G[V] is disconnected, a hard barrier makes the better designs unreachable, and the fix is to add larger moves (macro-moves) or to let search cross invalid designs.

### Cited Findings
**Repulsive Shells itself (what the barrier is and is not)**
- Repulsive Shells (Sassen, Schumacher, Rumpf, Crane; ACM TOG 2024, Best Paper Award) adds a repulsive energy to an existing shape space so that collision avoidance is part of the Riemannian metric. As a result, "intersection-free shape interpolation or motion extrapolation amount to simply computing geodesic paths." — [Repulsive Shells project page](https://www.cs.cmu.edu/~kmcrane/Projects/RepulsiveShells/index.html)
- The repulsive term is an adaptive tangent-point energy, evaluated in O(n log n) with a fast multipole scheme. The authors contrast it with the IPC barrier, which needs continuous collision detection as a fallback because its logarithmic repulsion does not fully prevent smooth-surface interpenetration. In a leaf example, the leaf approaches self-intersection "only at time t = ∞." — [Repulsive Shells project page](https://www.cs.cmu.edu/~kmcrane/Projects/RepulsiveShells/index.html)
- Counter to the earlier "it's only about motions" reading: the same page also shows *static design optimization*, including packing an octopus into a box, packing bunnies into a sphere, and near-isometric embeddings of a hyperbolic plane and a torus. It also shows that naively penalizing repulsive energy along a trajectory gives undesirable deformation, presented as a failure case. — [Repulsive Shells project page](https://www.cs.cmu.edu/~kmcrane/Projects/RepulsiveShells/index.html)
- In Repulsive Surfaces (Yu, Brakensiek, Schumacher, Crane; ACM TOG 2021), the tangent-point energy penalizes 1/r(x,y), and the contribution "will be very large for points y close in space but distant along the surface." Optimization uses a fractional Sobolev (H^s, 1<s<2) preconditioner that "does not suffer from a mesh-dependent time step restriction." Constraints such as area or volume are supported. — [Repulsive Surfaces project page](https://www.cs.cmu.edu/~kmcrane/Projects/RepulsiveSurfaces/index.html)

**Correctness-preserving rewrite systems (hard barrier through the move set)**
- Equality saturation/e-graphs: an e-graph compactly represents equivalence classes of expressions, closed under congruence. Rewrites add equivalent terms *without destroying* the original (for example, (a×2)/2 stays in the graph after x×2→x≪1 is applied), so every reachable term is provably equivalent to the input. egg adds "rebuilding" (deferred invariant restoration). Over 32 tests, deferred rebuilding gives a geometric-mean 88× speedup on congruence closure and 21× on full equality saturation. Of those 32 tests, 8 hit the 100-iteration limit, i.e., saturation does not always terminate. — [Willsey et al., egg, POPL 2021 (arXiv 2004.03082)](https://arxiv.org/abs/2004.03082)
- egg's Herbie backend is "over 3000× faster" than Herbie's original simplifier. The original had to cap e-graph size and impose a time limit, and simplification "fails altogether" when the timeout is exceeded. This illustrates that rewrite-closed search spaces blow up and need node, iteration or time limits. — [egg paper](https://arxiv.org/abs/2004.03082)
- STOKE's critique of this family: Denali and Equality Saturation "attempt to gain scalability by only considering programs that are known to be equal to the input program," but "rely heavily on expert knowledge. It is unclear whether an expert would know a priori to encode an equality axiom" for STOKE's Montgomery-multiplication rewrite, "or more generally, whether a set of expert written rules could ever cover the set of all interesting program optimizations." — [Schkufza, Sharma, Aiken, Stochastic Superoptimization, ASPLOS 2013 (arXiv 1211.0557)](https://arxiv.org/abs/1211.0557)

**Neutral networks / genotype networks (connectivity of the valid set)**
- Wagner (2008) separates genotype robustness, which is antagonistic to evolvability, from phenotype robustness, which "promotes" evolvability. Phenotype robustness is the average genotypic robustness over a neutral network. Phenotypic evolvability is the number of distinct alternative phenotypes reachable by point mutations from the neutral network. — [Wagner 2008, Proc. R. Soc. B, "Robustness and evolvability: a paradox resolved"](https://www.ieu.uzh.ch/wagner/papers/Wagner_PRS08.pdf); definitions as restated in [arXiv 2002.00363 review](https://arxiv.org/pdf/2002.00363)
- Robustness causes genotype networks, which are large connected sets of genotypes with the same phenotype, and those networks make phenotypic variability easier. — [PMC3282381 review](https://pmc.ncbi.nlm.nih.gov/articles/PMC3282381) (author not confirmed in my search)
- Ebner, Shackleton, Shipman, "How neutral networks influence evolvability," Complexity 7(2):19–33, 2001: the extent of neutral networks affects the interconnectivity of the search space and therefore evolvability. In the CEC 2001 companion (Ebner, Langguth, Albert, Shackleton, Shipman), species on genotype-phenotype maps with extensive neutral networks keep finding adaptive mutations and reach higher optima. — [Ebner et al. preprint](https://stubber.math-inf.uni-greifswald.de/~ebner/resources/uniWu/neutral.pdf); [dblp CEC 2001](https://dblp.org/rec/conf/cec/EbnerLASS01)
- In digital-circuit evolution specifically (closest to redstone), Vassilev & Miller (ICES 2000) built a genotype-phenotype mapping that embeds neutrality and report that it is beneficial when evolving a 3-bit multiplier on an array of logic cells. A later CGP survey says neutral drift "significantly improves the success rate," though some work disputes neutrality claims, including the claim that random search can do better. — [ICES 2000 record](https://gpbib.cs.ucl.ac.uk/gp-html/ICES2000.html); [GECCO 2000 companion](https://gpbib.pmacs.upenn.edu/gecco2000/EH184.pdf); [Springer survey s11047-019-09772-4](https://link.springer.com/article/10.1007/s11047-019-09772-4) (abstract-level only)

**STOKE's search-space picture: the precise failure mode of a hard barrier**
- STOKE Fig. 4: llvm -O0 and gcc -O3 codes "occupy a densely connected part of the space which is easily traversed. Expert code occupies an entirely different region of the space which is reachable only by way of an extremely low probability path." The expert code "has the property that no sequence of small equality preserving transformations connect it to either the llvm -O0 or the gcc -O3 code." The only local path "builds the expert code in place next to the original, all the while increasing its cost, only to delete the original code at the very end." — [STOKE, ASPLOS 2013](https://arxiv.org/abs/1211.0557)

**Constraint-preserving operators and the death penalty (EA constraint handling)**
- Coello's survey (CMAME 191:1245–1287, 2002) groups constraint handling into penalty functions (static, dynamic, annealing, adaptive, co-evolutionary, death), special representations and operators, repair algorithms, separation of objectives and constraints, and hybrids. Repair is aimed at combinatorial problems "in which the traditional genetic operators tend to generate infeasible solutions all (or at least most of) the time." — [Coello 2002 survey (course copy)](https://homes.di.unimi.it/cordone/courses/2024-ae/Lez23-Materiali/constraint-handling.pdf) (OCR-quality copy; wording should be checked)
- The death penalty (discard infeasible candidates) is the cheapest option because infeasibility never has to be measured. Lecture material based on the survey advises using it only in limited cases. — [CTU lecture slides on constraint handling](https://cw.fel.cvut.cz/old/_media/courses/a0m33eoa/prednasky/a0m33eoa_constrainthandling_2012.pdf)

### Inferences
- **Precise definition (my synthesis).** Let c(x) be the objective (volume, ticks) and V the set of working doors. A *hard discrete barrier* is the cost c̃(x) = c(x) for x ∈ V and c̃(x) = +∞ for x ∉ V. Under Metropolis acceptance min(1, exp(−β Δc̃)), every move into the invalid region is accepted with probability exp(−∞) = 0. The chain then lives on the connected component of G[V] that contains the seed. That is the exact analogue of "infinite distance to self-intersection." The design-space "distance" between valid x and invalid y under the barrier metric is ∞, and the distance between two valid designs is the shortest *all-valid* path. If G[V] is disconnected, that distance is also ∞ between components. Repulsive Shells avoids this because its continuous valid set (embedded shapes in a homotopy class) is path-connected and the metric only shrinks steps near the boundary. Discrete door space has no such guarantee.
- **A soft discrete barrier needs a slack function.** The log-barrier −μ·log s(x) requires a positive slack s(x) that tends to 0 at the boundary. For doors, s(x) has to be built: timing slack in ticks before a race or update-order failure, how many of the single-edit neighbors are still valid (Wagner-style mutational robustness), or a robustness score of the kind used in STL falsification (see Q6). With s(x), edge weights such as w(x→y) = 1 + λ/s(y) produce a "repulsive metric" on the design graph. Its geodesics between two known-good doors are neutral paths that stay as far from failure as possible. This is the closest faithful transfer of Repulsive Shells' "collision avoidance in the metric" idea. It is my own proposal and was not found in the literature as such.
- **Geodesic interpolation between two working doors** (the Repulsive Shells use case) maps to finding valid neutral paths between two designs. Glover's path relinking is the classical discrete relative (UNVERIFIED: not fetched). This could recombine two known-good doors without leaving V.
- **E-graph-style rewriting fits a door search only if the rule set is sound for the door's semantics.** Plausible sound rules include: replace a repeater chain by an equivalent-delay chain, move a redstone line along a path that keeps every adjacency-update interaction, and swap a component for a timing-equivalent one. Minecraft has non-local effects (quasi-connectivity, block-update order, piston push limits, 0-tick behaviour), so local rewrites are much harder to prove sound than algebraic rewrites. STOKE's critique applies directly: the best compact doors probably use "distinct algorithms" (different mechanisms) that no small set of equivalence rules connects.

### Gaps
- I could not find a primary-source statement that the Repulsive Shells/Surfaces tangent-point energy is *infinite* for self-intersecting configurations. Neither project page says so. The Repulsive Shells page only says the energy "prevents" self-intersection and gives the t = ∞ leaf example. The property is standard for tangent-point energies at suitable exponents, but I did not verify it from the paper text.
- I found no paper that defines a "discrete log-barrier" for combinatorial local search in this exact form. The barrier-metric construction above is my synthesis.
- I did not read Banzhaf's 1994 genotype-phenotype mapping paper. Only Ebner et al. and Vassilev & Miller were found, and those only at abstract or bibliographic level.
- EDA logic rewriting (e.g., ABC's AIG rewriting by Mishchenko et al.) was not fetched. Its role as a correctness-preserving local rewrite system is inferred from background knowledge only.

## Q2. Counter-evidence: is it better to pass THROUGH invalid designs with a graded penalty?

### Takeaway
Yes, when the valid set is sparse or disconnected under local moves. STOKE is the cleanest evidence. Its correctness term is a *graded* Hamming distance on test cases, not a 0/1 equivalence check. Its synthesis phase starts from random, incorrect code. A strict correctness metric performed about as well as random search. STOKE also documents the limit: when an invalid design differs from the target "by only a single bit" (as a near-miss broken door might), the graded signal is deceptive and synthesis fails. Strategic oscillation (Glover) is the principled middle ground: keep search close to the feasibility boundary and adapt the penalty weight.

### Cited Findings
- **Graded correctness instead of 0/1.** STOKE approximates equivalence with test cases and uses "the number of bits difference in live outputs (i.e., the Hamming distance)." Besides being faster than a theorem prover, this "has the added advantage of producing a smoother landscape than the 0/1 output of a symbolic equality test; it provides a useful notion of 'almost correct' that can help to guide the search." — [STOKE, ASPLOS 2013](https://arxiv.org/abs/1211.0557)
- **Why the validator cannot sit in the inner loop.** Validations per second with the theorem prover are "well below 100." Because MCMC "is effective only insofar as it is able to explore sufficiently large numbers of proposals," proving equivalence inside the inner loop would leave too few proposals to be useful. — [STOKE](https://arxiv.org/abs/1211.0557)
- **Two phases, both of which cross invalid space.** Synthesis "begins with a random starting point (a sequence of randomly chosen instructions)" and uses only the correctness cost. Optimization starts from a correct program and uses correctness plus performance, "which allows it to measure improvement while also allowing it to experiment with 'shortcuts' that (temporarily) violate transformation correctness." — [STOKE](https://arxiv.org/abs/1211.0557)
- **History behind the two phases.** An early single-phase STOKE "was able to consistently transform llvm -O0 code into the equivalent of gcc -O3 code" but "was unable to produce results which were competitive with expert hand-written code." That gap is what motivated the synthesis/optimization split. — [STOKE](https://arxiv.org/abs/1211.0557)
- **Strict vs. improved cost (Fig. 7, Montgomery multiplication).** The "improved" metric rewards a correct value in the *wrong register*: it takes the min Hamming distance over all registers of equal width, plus a small misplacement penalty w_m. "In the amount of time required for the improved cost function to converge to a zero-cost rewrite, the strict version obtains a minimum cost which was only slightly superior to that obtained by a purely random search." The authors call this "an implicit parallelization of the search procedure." — [STOKE](https://arxiv.org/abs/1211.0557)
- **Why synthesis works.** "Synthesis is effective precisely when it is possible to discover portions of a correct rewrite incrementally, as opposed to all at once." Best cost falls as the fraction of final-rewrite instructions present rises. — [STOKE](https://arxiv.org/abs/1211.0557)
- **When it fails: single-bit cliffs.** STOKE could not synthesize three Hacker's Delight benchmarks. Each "produce[s] results which differ by only a single bit from a simple yet completely incorrect alternative" (e.g., round-up-to-power-of-2 vs. return 0). For those three, the optimization phase alone, started from correct code, still matched production-compiler code. Future work calls for a cost function "robust against targets with numerous deceptively attractive, albeit completely incorrect, synthesis alternatives." — [STOKE](https://arxiv.org/abs/1211.0557)
- **STOKE numbers.**
  - The Montgomery multiplication kernel (OpenSSL), started from llvm -O0 (116 lines), came out "16 lines shorter and 1.6 times faster" than gcc -O3, slightly faster than expert hand-written assembly. It is an 11-instruction kernel, formally verified equivalent, and the authors believe it is optimal for x86-64.
  - STOKE used "a large subset of the nearly 400 x86-64 opcodes." For comparison, Massalin's enumerative superoptimizer reached length 12 only by restricting itself to 10–15 opcodes.
  - Early-termination acceptance raised throughput to a peak above 50,000 proposals/s, an "almost 3x improvement."
  - Runs used 40 dual-core 1.8 GHz Opterons with 30-minute budgets per phase. Results match gcc -O3/icc -O3 and sometimes beat both.
  - Source: [STOKE](https://arxiv.org/abs/1211.0557)
- **MCMC framing.** p(R) ∝ exp(−β·c(R)) with Metropolis-Hastings. Well before the limiting behaviour, "MCMC sampling functions as an intelligent hill climbing method which is robust against irregular functions that are dense with local minima." Proposals must be ergodic. — [STOKE](https://arxiv.org/abs/1211.0557)
- **Strategic oscillation.** Glover (1989) alternates search between feasible and infeasible states, concentrating effort near the boundary. The boundary region is defined as feasible states with infeasible neighbours or vice versa. Probe depth into each side is a tunable span parameter. Adaptive move-evaluation weights "induce a strategic oscillation around the feasibility boundary." For integer programs there is a path to an optimum whose infeasible points stay within a distance bound D*. — [ICAPS 2006 DC paper](https://icaps06.icaps-conference.org/dc-papers/paper26.pdf); [Glover, Critical Event TS for MKP](https://leeds-faculty.colorado.edu/glover/258%20-%20Critical%20Event%20TS%20for%20Multidimensional%20Knapsack%20Problems.pdf); [Glover, Adaptive Memory Search for Boolean Optimization](https://leeds-faculty.colorado.edu/glover/fred%20pubs/338%20-%20TS%20-%20BOOP%20I-Adaptive%20Memory%20Search.pdf); [Glover, Infeasible-Feasible Search and Directional Rounding](https://leeds-faculty.colorado.edu/glover/383%20-%20Infeasible-Feasible%20Search%20and%20Directional%20Rounding.pdf) (these are search-snippet-level; theorem details not verified)
- **Penalty vs. repair vs. death penalty (EA).** Penalty factors are "in general, problem-dependent," and a static penalty can be a poor choice over a whole run. A variant assigning zero or very bad fitness to infeasible solutions "may work better in practice" than outright discarding. — [CTU slides on Coello taxonomy](https://cw.fel.cvut.cz/old/_media/courses/a0m33eoa/prednasky/a0m33eoa_constrainthandling_2012.pdf); [Coello 2002 survey copy](https://homes.di.unimi.it/cordone/courses/2024-ae/Lez23-Materiali/constraint-handling.pdf)
- **Minecraft-specific evidence for graded signals.** Medina et al. (GECCO 2023) evolve piston/slime "flying machines" with *no* validity check. Every shape is simulated. Oscillating shapes get small fitness (<10), flyers get a large bonus minus a leftover-block penalty, and stationary shapes stop early. They report fitness alone gives no smooth gradient from stationary to flying, and the jump to flight is sudden. — [Medina, Richey, Mueller, Schrum, GECCO 2023 (arXiv 2302.00782)](https://ar5iv.arxiv.org/html/2302.00782)

### Inferences
- **A piston door's pass/fail is STOKE's worst case.** It is a single boolean computed from a complex process, and STOKE says "any code which performs a complex computation that is reduced to a single boolean value poses a problem for our technique." The transfer is to build a STOKE-style "improved" cost from the simulator trace, giving partial credit for:
  - each door block in its correct open/closed position at each target tick (a Hamming distance over the door aperture across time);
  - each piston firing in the right order;
  - the right signal arriving at a piston on a different but equivalent-delay path (the analogue of "correct value in the wrong register").
- **Run the two-phase split.** Synthesis from random or partial designs with the graded correctness cost. Optimization from known-working doors, with volume and ticks plus correctness, allowing temporary breakage. This mirrors STOKE's split and its explanation of why a single phase only reached "-O3-like" (incremental) improvements.
- **Expect single-bit cliffs.** Many broken doors differ from the working one in one observable bit, e.g., one block left behind, or a 1-tick timing miss that leaves the door identical except for one block. A per-block, per-tick trace distance gives more signal than a final-state distance.

### Gaps
- I did not get the full text of Coello's 2002 survey or Coello & Mezura-Montes' comparative evaluation, so there are no quantitative penalty-vs-repair benchmarks here.
- I found no published controlled comparison of hard-barrier vs. graded-penalty search for *redstone* or other voxel mechanisms.
- STOKE's follow-ups (Sharma et al. on floating-point/loop optimization, CACM 2016 "Stochastic Program Optimization") were not accessible (CACM returned HTTP 403).

## Q3. Macro-moves and grammars: RoboGrammar and graph grammars for mechanisms

### Takeaway
RoboGrammar's grammar enforces *fabricability* by construction, not *function*. The paper says: "Our framework ensures that simulated designs are at least fabricable." The search (Graph Heuristic Search) works over partial derivations with a GNN value function. Rule sequences are macro-moves: each rule adds a whole, validly attached sub-assembly. The "one edit breaks it" problem is partly avoided because edits are rule applications rather than single-part changes. Functional invalidity (self-collision) still happens and is handled by rejection sampling and blocking dead partial designs. For doors, the analogue is a grammar of redstone/piston *modules* that are each valid by construction (e.g., "extend column by one 2-piston stack with matched timing").

### Cited Findings
- **Grammar.** A recursive graph grammar over robot components. "Using only a small set of rules our grammar can describe hundreds of thousands of possible robot designs." There are two rule categories: structural rules (inspired by arthropods; e.g., r3 enforces symmetry of limb pairs, r4 adds body segments) and component-based rules that replace non-terminals with terminals (joints, links). Recursion is capped by a counter of total derivation steps, set to a maximum of 40. — [Zhao et al., RoboGrammar, ACM TOG 39(6) 188, SIGGRAPH Asia 2020](https://people.csail.mit.edu/jiex/papers/robogrammar/paper.pdf)
- **Validity by construction (scope).** "Our framework ensures that simulated designs are at least fabricable... With the appropriate rules, robot grammars enforce the use of a limited set of components and ensure that the components are connected in a feasible manner." The sim-to-real match is not addressed. — [RoboGrammar paper, §10](https://people.csail.mit.edu/jiex/papers/robogrammar/paper.pdf)
- **Residual invalidity.**
  - A simulation can fail, "including self-collision in the starting configuration." The search then retries another random playout from the same leaf.
  - "Simply returning a fixed, low result unnecessarily biases the search towards simpler designs which are less likely to self-collide." This is an explicit argument against the death penalty.
  - "There may be partial designs that no sequence of rule applications can convert into simulable designs." Nodes are blocked after 100 failed playout attempts.
  - These enhancements are described for the MCTS baseline.
  - Source: [RoboGrammar paper, §6.2](https://people.csail.mit.edu/jiex/papers/robogrammar/paper.pdf)
- **Graph Heuristic Search (GHS).**
  - Each episode has a design phase, an evaluation phase and a learning phase. In the design phase, K candidates are built by ε-greedy rule application, taking argmax_a V_θ(P(s_l, a)) with probability 1−ε.
  - One design is evaluated per iteration with MPPI-based MPC. Each partial-design ancestor's label is updated to the max reward of any completion.
  - V_θ is a GNN (GraphSage+BatchNorm, DiffPool layers that reduce node cardinality by 75%, and so on), trained by MSE with Adam. It is isomorphism-invariant, so no transposition table is needed.
  - The ε schedule uses ε0 = 1, ε1 = 0.1, decay 0.3.
  - Source: [RoboGrammar paper, §6.1, §9](https://people.csail.mit.edu/jiex/papers/robogrammar/paper.pdf)
- **Results.** GHS ran for 2,000 iterations against 5,000 for each baseline (an MCTS variant with UCT-RAVE, transpositions and rejection sampling, plus random search). It "consistently finds better designs... in much fewer iterations" on flat, frozen-lake, ridged and wall terrains, averaged over 3 seeds. 2,000 GHS iterations took about 31 h on a 32-core n2-highcpu-32 machine, of which about 20 h was evaluation. Average derivation length of evaluated designs on flat terrain: GHS 24.4, MCTS 24.0, random 11.4. Random search gravitates toward short or simple derivations. Multi-terrain Pareto fronts were found with 20,000 iterations of random search. — [RoboGrammar paper, §9](https://people.csail.mit.edu/jiex/papers/robogrammar/paper.pdf)
- A follow-up, Multi-Objective Graph Heuristic Search (Xu, Spielberg, Zhao, Rus, Matusik; ICRA 2021), extends GHS to multiple objectives, which matters for a volume vs. ticks Pareto front. — [RoboGrammar project page](https://people.csail.mit.edu/jiex/papers/robogrammar/index.html) (not read in detail)

### Inferences
- **The door analogue of RoboGrammar** is a grammar whose terminals are *verified modules*: a piston stack with its timing circuit, a block-feeder, an observer-based pulse generator. Its non-terminals are interface slots (signal in at tick t, footprint). Validity by construction covers "pieces connect"; the simulator still adjudicates interference such as quasi-connectivity crosstalk or update order. Following RoboGrammar, blocked partial designs (after N failed completions) are better than a fixed low reward, which biases toward trivial designs.
- **Macro-moves reconnect G[V].** STOKE's expert code was reachable only by "building the expert code in place next to the original" and then deleting the original. A grammar rule that inserts a whole alternative mechanism in one step is a macro-move that turns that low-probability path into a single edge.
- **The learned value on partial designs** (GHS) suits doors: evaluate partially derived doors by the best completion seen so far.

### Gaps
- I did not find graph-grammar work for *redstone* or for *linkage/mechanism* design beyond RoboGrammar in this pass. Grammar-based mechanism synthesis (e.g., linkage graph enumeration) is not covered by sources here.
- RoboGrammar does not report how often grammar-generated designs fail simulation, i.e., the self-collision rejection rate.

## Q4. Quality-diversity (MAP-Elites, novelty search) and Minecraft/voxel design

### Takeaway
There is direct Minecraft evidence with pistons, slime and observers. MAP-Elites with a *mechanism-aware* behavior descriptor (piston orientation counts) found working flying machines in 70% (original blocks) and 93.3% (with observers) of 30 runs. Pure fitness managed 33% and 46.7%. Descriptors based on block count were no better than pure fitness. QD helps on cliffy mechanism landscapes only if the descriptor separates *functionally different* mechanisms.

### Cited Findings
- **EvoCraft** (Grbic, Palm, Najarro, Glanois, Risi; arXiv 2012.04751, Dec 2020; Springer chapter 2021) is a Minecraft mod with a Python/gRPC API to place and track blocks in a running server. It targets open-ended search for increasingly complex artifacts, including "actuated machines with circuits and mechanical components." It showed promise for static structures, but evolving moving machines was difficult. — [arXiv 2012.04751](https://arxiv.org/abs/2012.04751v1); [ITU project page](https://real.itu.dk/project/open-ended-evolution)
- **Evolving flying machines in Minecraft using QD** (Medina, Richey, Mueller, Schrum; GECCO 2023):
  - Genome: a real-valued vector, 3 values per cell of a 3×3×3 grid (presence > 0.5, type, orientation).
  - Blocks: redstone, quartz, slime, pistons and sticky pistons, plus an "observer" set.
  - Methods: MAP-Elites with crossover vs. a (μ+λ) ES with μ = λ = 20 at equal evaluations.
  - Successes out of 30 (original set / observer set): pure fitness 9 / 14; ME count 3 / 17; ME count+negative space 7 / 16; ME piston-orientation 21 (70%) / 28 (93.3%).
  - ME.PO was significantly better (Fisher exact, Bonferroni) and was the only method to find flyers in all 6 directions with the original set.
  - "A poor descriptor can perform no better than pure fitness."
  - Source: [arXiv 2302.00782](https://ar5iv.arxiv.org/html/2302.00782)
- **Growing 3D artefacts and functional machines with NCA** (Sudhakaran, Grbic, Li, Katona, Najarro, Glanois, Risi; ALIFE 2021): 3D neural cellular automata in Minecraft grow structures "of over 3,000 blocks" (castles, apartment blocks, trees). When trained for regeneration, they can regrow parts of "simple functional machines." — [arXiv 2103.08737](https://arxiv.org/abs/2103.08737)

### Inferences
- **For doors, MAP-Elites descriptors should encode mechanism type,** not size:
  - number and orientation of pistons,
  - whether 0-tick, observer, or repeater-only timing is used,
  - number of distinct timing channels.
  - Then volume and ticks are the objective within each cell.
- **The archive also stores stepping stones across cliffs.** Doors that "almost open" (graded score from Q2) can be elites in their own cells.
- **NCA regeneration** is a robustness idea (recover after damage), but its "simple functional machines" result is far from door scale. It is weak as a direct optimizer for doors.

### Gaps
- I did not fetch primary MAP-Elites (Mouret & Clune 2015) or novelty search (Lehman & Stanley 2011) papers in this pass. They are well known, but no numbers are cited here.
- MarioGPT (Sudhakaran et al. 2023) is a Mario level generator, not Minecraft. It was not investigated because it does not bear on mechanism search.
- The specific functional machines in the NCA paper (e.g., whether a piston "caterpillar" was used) were not confirmed. The abstract only says "simple functional machines."

## Q5. LLM-as-mutation-operator evolutionary search (FunSearch, AlphaEvolve, 2025–2026 follow-ups) and LLM+evaluator loops vs. simpler iteration

### Takeaway
LLM+evaluator loops are effective when an automatic evaluator exists, and a door simulator is an ideal evaluator. Two caveats:
- **Search-method vs. search-space evidence.** AlphaEvolve's ablations show evolution, context, full-file evolution and strong models each help. A February 2026 study, however, finds plain IID sampling or sequential conditioning from an LLM matches or beats ShinkaEvolve on most AlphaEvolve math problems at roughly $20–30 budgets. It concludes that "the primary challenge... is designing good search spaces."
- **Domain fit.** LLMs mutate *code*. For voxel doors, the natural fit is to have the LLM write *generators/parameterizations* (programs that emit door designs), not edit blocks directly.

### Cited Findings
- **AlphaEvolve** (Novikov et al., 18 authors, arXiv 2506.13131, 16 Jun 2025):
  - Results: 4×4 complex matrix multiplication with 48 scalar multiplications, the "first improvement, after 56 years, over Strassen's algorithm in this setting"; improved state of the art for 14 matrix-multiplication targets.
  - Google infrastructure: data-center scheduling recovers "on average 0.7% of Google's fleet-wide compute resources"; 23% average kernel speedup giving 1% reduction in Gemini training time; 32% FlashAttention kernel speedup (15% on pre/post-processing).
  - Open math problems: over 50 problems, matched best known on ~75% and surpassed on ~20%. Kissing number in 11D raised from 592 to 593.
  - Source: [arXiv 2506.13131 (HTML)](https://arxiv.org/html/2506.13131v1)
- **AlphaEvolve design and ablations.** It uses an ensemble of Gemini 2.0 Flash (throughput) and Gemini 2.0 Pro (quality). It uses an *evaluation cascade*: test cases of increasing difficulty, where a candidate advances only if promising at each stage, and small-scale runs "filter out faulty programs early." Ablations on tensor decomposition and kissing number: no evolution (same initial program repeatedly fed), no context, no meta-prompt evolution, no full-file evolution (only loss evolved), small base LLM only. Each component contributes significantly; exact effect sizes appear only in Fig. 8 (not numerically stated in text). — [arXiv 2506.13131](https://arxiv.org/html/2506.13131v1)
- **ShinkaEvolve** (Lange, Imajuku, Cetin; arXiv 2509.19349, 17 Sep 2025): says prior LLM evolution needs "thousands of samples." Adds (1) exploration/exploitation-balanced parent sampling, (2) code-novelty rejection sampling, and (3) a bandit-based LLM ensemble. It found a new state-of-the-art circle packing "using only 150 samples," with further results on AIME agent harnesses, ALE-Bench, and MoE load-balancing losses. — [arXiv 2509.19349](https://arxiv.org/abs/2509.19349)
- **"Simple Baselines are Competitive with Code Evolution"** (arXiv 2602.16805, Feb 2026; NeurIPS 2025 venue listing as "Random Baselines for Simple Code Problems are Competitive with Code Evolution"):
  - *Math bounds.* 9 AlphaEvolve problems, Gemini 2.5 Pro, ~$20 budget. IID random sampling (2,000 programs) matched or exceeded ShinkaEvolve on 4/9. Sequential conditioned sampling (SCS: 6 trials × 10 generations, 1,200 programs) did so on 6/9, and matched or exceeded AlphaEvolve on 4/9. Kissing number 11D: AlphaEvolve 593 / ShinkaEvolve 402 / IID 438 / SCS 438. Circle packing: 2.63586 / 2.63598 / 2.632 / 2.63590. Baselines ran 1–3 h vs. ~10 h for ShinkaEvolve.
  - *Search-space reformulation.* Reformulating the uncertainty inequality (Hermite basis, more coefficients) improved the bound from 0.3521 to 0.3482 for *all* methods.
  - *Agentic scaffolds.* All automated methods dropped >10% from validation to test; majority vote was best on test.
  - *MLE-bench.* SCS beat AIDE on 6/10 Kaggle competitions.
  - *Limitations.* Single ShinkaEvolve run per problem; OpenEvolve only partially run.
  - Source: [arXiv 2602.16805](https://arxiv.org/html/2602.16805v1); [NeurIPS 2025 listing](https://neurips.cc/virtual/2025/131657) (authors not captured in my fetch)
- **FunSearch** (DeepMind; Nature): pairs a pretrained LLM (PaLM 2 originally) with an automated evaluator that "guards against hallucinations and incorrect ideas." Best programs are fed back into a pool, "creating a self-improving loop," with a diversity mechanism against stagnation. It found "the largest cap sets ever found" in some settings, "the largest increase" in 20 years, and online bin-packing heuristics using fewer bins than established ones. A Dec 2024 update uses Gemini 1.5 Flash. — [DeepMind FunSearch blog](https://deepmind.google/discover/blog/funsearch-making-new-discoveries-in-mathematical-sciences-using-large-language-models/)
- **Other 2025–2026 frameworks seen in search results, not verified:**
  - CodeEvolve (arXiv 2510.14150): reportedly includes a "no evolution" ablation, and finds an inspiration-only configuration underperforms the baseline through convergence. — [arXiv 2510.14150](https://arxiv.org/pdf/2510.14150v4)
  - The ADRS study (arXiv 2512.14806) ablates OpenEvolve components. — [arXiv 2512.14806](https://arxiv.org/pdf/2512.14806v2)
  - EvoX (arXiv 2602.23413) claims to beat AlphaEvolve, OpenEvolve, GEPA and ShinkaEvolve on most of ~200 tasks (authors' claim). — [arXiv 2602.23413](https://arxiv.org/pdf/2602.23413v2)

### Inferences
- **On "LLM+evaluator loop vs. single-agent iteration":** AlphaEvolve's "no evolution" ablation (repeatedly re-prompting from the same initial program) is the closest analogue to single-agent iteration without a population, and it was worse. The 2026 baseline study shows *sequential conditioning on a random subset of successful prior programs* (SCS, which is close to "an agent iterating with memory of what worked") is competitive with full evolutionary frameworks at small budgets. The robust lessons:
  - always run a cheap-baseline control,
  - feed back multiple *successful* prior designs,
  - put most effort into the search-space representation, i.e., what the LLM edits.
- **For doors,** LLMs should edit *door-generating programs* (parametric module layouts, timing schedules), and the exact simulator acts as AlphaEvolve's cascade:
  - stage 1: structural legality (piston push limit, no overlap);
  - stage 2: final-state check;
  - stage 3: full tick-by-tick trace;
  - stage 4: robustness to update order or chunk timing.
- **Simulator throughput favors cheap mutation.** At the scale STOKE reached (>50,000 proposals/s), LLM calls are 4–6 orders of magnitude slower per proposal. A hybrid is likely best: the LLM proposes mechanisms or macro-moves, and local MCMC/MAP-Elites tunes blocks.

### Gaps
- FunSearch's exact cap-set numbers were not verified from a primary source. The Nature/PMC pages were blocked (redirect, reCAPTCHA) and the blog gives no numbers. From memory (UNVERIFIED): n = 8 cap set of size 512 vs. prior 496.
- OpenEvolve (open-source AlphaEvolve reimplementation) was not read directly. I found no dedicated OpenEvolve-vs-repeated-sampling ablation.
- AlphaEvolve's numerical ablation effect sizes (Fig. 8) were not extracted.
- I found no LLM-evolution work on Minecraft redstone or voxel mechanisms.

## Q6. Program/hardware superoptimization and exact (SAT/SMT/ILP) synthesis of small circuits: what scale do exact methods reach?

### Takeaway
Exact SAT-based synthesis of optimal logic is practical for roughly 4–5 input functions and about 7–12 two-input gates. It becomes intractable around 6 inputs / ~19 gates unless the DAG topology is supplied, at which point labeling takes 0.12 s. Enumerative superoptimizers reach around 12 instructions over a small opcode set. Stochastic search (STOKE) reaches more opcodes but sacrifices completeness. So exact methods can certify *optimal small sub-circuits* (a door's timing logic abstracted as a Boolean/timed network), not the whole voxel layout.

### Cited Findings
- **Exact synthesis scale.**
  - Knuth found "all 5-variable Boolean functions can be represented using 2-input gate-level networks with at most 12 gates." All 222 4-input NPN classes need at most 7 two-input steps.
  - The 5-input space "is too large to run" exhaustively in their benchmark, so random samples were used. A 1-minute timeout was used on 500 hard random 5-input functions.
  - Source: [Haaswijk, Soeken, Mishchenko, De Micheli, "SAT-Based Exact Synthesis: Encodings, Topology Families, and Parallelism," IEEE TCAD 39(4), 2020](https://si2.epfl.ch/~demichel/publications/archive/2020/winston-exact.pdf)
- **The hard part is topology.** For the 6-input function 0x9ef7a8d9c7193a0f, "the smallest known implementation... uses 19 2-input gates. When a solution topology is given, an SAT solver can find a labeling in 0.12 s on a laptop computer. Without this topology, finding a solution is intractable." The solver must simultaneously find a valid DAG and assign operators. — [Haaswijk et al. 2020](https://si2.epfl.ch/~demichel/publications/archive/2020/winston-exact.pdf)
- **Speedups.** Partial-DAG synthesis solves more than 3× as many hard 5-input functions within 1 minute. Topology-family parallelism is up to 68× faster than single-thread baseline (MultiSolvers up to 9.5×). Symmetry breaking and the encoding choice (SSV vs. fence-based) change timeouts substantially. — [Haaswijk et al. 2020](https://si2.epfl.ch/~demichel/publications/archive/2020/winston-exact.pdf)
- **Classifying functions with exact synthesis** (ISMVL 2017): minimum-length chains for all 4- and 5-input functions over 3-input operators, about 48× parallel speedup. — [Haaswijk et al. 2017](https://si2.epfl.ch/demichel/publications/archive/2017/07965003.pdf)
- **Superoptimization scale.** Massalin's enumerative superoptimizer optimized sequences "of up to length 12," but only by restricting to 10–15 opcodes. STOKE used a large subset of the nearly 400 x86-64 opcodes for an 11-instruction kernel, but "sacrifices completeness." — [STOKE](https://arxiv.org/abs/1211.0557)

### Inferences
- **A two-level decomposition fits doors:**
  - (i) *Abstract timing layer.* Which piston fires at which tick, as a small timed schedule. This is small enough for SAT/SMT/ILP to find tick-optimal schedules exactly, with timing constraints as linear inequalities over tick variables.
  - (ii) *Spatial embedding layer.* Realize the schedule in blocks under Minecraft adjacency and update rules. This is where stochastic/QD/grammar search is needed.
- **"Topology given ⇒ fast."** This mirrors the grammar/macro-move idea. Fix a mechanism template (topology), then exactly solve for parameters such as repeater delays or block positions.

### Gaps
- I found no exact (SAT/ILP) synthesis of Minecraft redstone or pistons. There may be hobbyist redstone compilers or optimizers (e.g., MCHPRS-adjacent tools), but none were verified.
- Kojevnikov–Kulikov–Yaroslavtsev (SAT 2009) circuit-finding and Knuth's TAOCP 7.1.2 were cited only via Haaswijk et al., not read directly.

## Q7. Surrogate/robustness signals: "margin to failure" (slack) on top of a pass/fail verifier

### Takeaway
The established formalism is quantitative (robust) semantics of Signal Temporal Logic. The robustness value is signed: positive means satisfied, negative means violated, and the magnitude is the margin. That turns a pass/fail spec into a continuous objective, used both for falsification (minimize to find failures) and for synthesis (maximize margin). STOKE's Hamming-distance cost is the same idea for programs. For doors, a robustness margin plays both roles from Q1 and Q2: the slack in a discrete log-barrier, and the graded penalty for crossing invalid designs.

### Cited Findings
- Donzé & Maler, "Robust satisfaction of temporal logic over real-valued signals," FORMATS 2010, extends spatial robustness to account for *temporal displacement*, i.e., how far a signal can shift in time and still satisfy the spec. This gives a quantitative semantics for STL. — [secondary: Ferrère et al. 2019](https://research-explorer-playground.test.ista.ac.at//download/6428/8633/2019_ACM_Ferrere.pdf); [STL lecture slides](https://moodle2.units.it/pluginfile.php/329478/mod_resource/content/1/9-SignalTemporalLogic.pdf)
- Robustness sign means satisfaction and absolute value means tolerance. Robust semantics "set off the idea of falsification by optimization," i.e., stochastic search guided by robustness to find violating inputs. An efficient offline algorithm is in Donzé, Ferrère, Maler (CAV 2013). — [STL lecture slides](https://moodle2.units.it/pluginfile.php/329478/mod_resource/content/1/9-SignalTemporalLogic.pdf); [Deshmukh RV'15 talk](https://jdeshmukh.github.io/Papers/rv15talk.pdf) (secondary sources only)
- STOKE: a graded Hamming correctness score "provides a useful notion of 'almost correct' that can help to guide the search," and its "improved" variant (min over equivalent locations plus a misplacement penalty) was decisive. — [STOKE](https://arxiv.org/abs/1211.0557)
- Wagner: genotypic robustness is the fraction of neutral single mutations, a "margin" in edit space rather than parameter space. — [Wagner 2008](https://www.ieu.uzh.ch/wagner/papers/Wagner_PRS08.pdf)

### Inferences
- **Concrete door margins (proposals, not from literature):**
  - (a) *Temporal robustness:* for each piston event, how many ticks earlier or later it could fire before the door fails (the discrete analogue of Donzé–Maler temporal displacement). Compute by perturbing repeater delays ±1 in simulation.
  - (b) *Edit-space robustness:* fraction of single-block or repeater edits within the bounding box that keep the door working (Wagner).
  - (c) *Update-order robustness:* whether the door works under the alternative block-update orderings or directions the game can exhibit. Minecraft redstone is locational and directional, so a door that works at one orientation may fail at another.
- **Use margins three ways:**
  - as a tie-breaker objective (prefer high-margin doors at equal volume and ticks);
  - as the barrier slack s(x) in a weighted design-graph metric (Q1);
  - as the signed robustness that grades broken designs (negative margin = "how badly it fails") for STOKE-style traversal of invalid space (Q2).
- **Cost control:** compute margins only for candidates that pass the cheap stages of the evaluation cascade (AlphaEvolve-style).

### Gaps
- I did not read the Donzé–Maler 2010 paper or Fainekos–Pappas 2009 directly. The details are from lecture slides and citing papers.
- I found no published use of robustness margins for Minecraft redstone or any discrete voxel mechanism. The door-specific margins above are my proposals.
