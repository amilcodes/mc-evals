# EDA as of late 2026, frontier LLMs/agents, and what a redstone piston-door agent harness should borrow

Notes on sourcing. Items marked **[fetched]** were read in this session, either from the primary source or from a named secondary. Items marked **[canonical, not re-fetched]** are well-known papers or docs cited from prior knowledge. Their URLs are canonical, but I did not re-read their numbers this session, so the writer should treat their specific figures with moderate confidence. Research date: 2026-11-16.

---

## 1. Core EDA pipeline concepts and which ones carry over to a tick-accurate redstone circuit

### Takeaway
The EDA pipeline is a sequence of representation changes, each with a cheap local check and a global signoff check: RTL, then an AIG (and-inverter graph) with rewriting, then a mapped cell netlist, then placement and routing, then STA (static timing analysis), with equivalence checking gating every step. Almost all of it transfers to redstone. The parts that transfer best are: (1) a canonical logic IR, (2) a library of verified cells used in technology mapping, (3) STA-style path and slack reporting in game ticks, and (4) SAT/BMC equivalence checking (bounded model checking) between a spec and a placed build. Placement and routing transfer least directly, because redstone "wires" are themselves 3D blocks with interference rules (quasi-connectivity, block updates, signal-strength decay), so routing is entangled with logic.

### Cited Findings
- **Production flow stack used in a 2026 agentic study:** Yosys 0.60 (synthesis + ABC optimization + LEC), OpenSTA 2.7.0 (static timing), Slang 10.0.13 (SystemVerilog elaboration), and the SkyWater sky130A standard-cell timing library. The loop is compile, then synth, then STA, then propose patch, then syntax check (Slang), then LEC, then re-synth/STA, then accept only if Fmax improves. **[fetched]** — [Xie, Garg, Renau, "Are Skills Enough?", ICLAD 2026](https://renau.github.io/docs/iclad26.pdf)
- **A cheap pre-filter before an expensive check pays off.** The same paper runs Slang before synthesis/LEC because it is "significantly faster and produces richer diagnostic messages", and reports that "this pre-filter eliminates most wasted synthesis cycles." **[fetched]** — [ICLAD 2026 paper](https://renau.github.io/docs/iclad26.pdf)
- **Wall-clock time goes to the verifier, not the LLM.** LLM inference is only 25.8% of runtime on average. Synthesis and LEC take about 75%. The paper concludes that "faster EDA tools would therefore yield larger end-to-end speedups than faster LLM inference." **[fetched]** — [ICLAD 2026 paper](https://renau.github.io/docs/iclad26.pdf)
- **Sequential equivalence is checked at the top boundary, which permits internal retiming.** "LEC is run at each benchmark's designated top boundary, so internal retiming is allowed but externally visible cycle behavior must match the reference." **[fetched]** — [ICLAD 2026 paper](https://renau.github.io/docs/iclad26.pdf)
- **Yosys EQY** is "a front-end driver program for Yosys-based formal hardware equivalence checking." Its config has gold/gate designs, recode, match, collect, and partition sections, and per-partition strategies (`sat`, `sby`, `dummy`). In other words, it splits a design into matched fragments and proves each one separately, which makes checking incremental and local. **[fetched, ToC level only]** — [EQY docs](https://yosyshq.readthedocs.io/projects/eqy/en/latest/)
- **ABC** represents logic as AIGs and optimizes them with local DAG-aware rewriting (`rewrite`/`rw`), refactoring (`refactor`/`rf`), and balancing (`balance`/`b`). Standard scripts such as `resyn2` chain these together. Technology mapping (`map`, `&if`) covers the AIG with library cells or LUTs (lookup tables) through cut enumeration. **[canonical, not re-fetched]** — [ABC home page](https://people.eecs.berkeley.edu/~alanmi/abc/); Mishchenko, Chatterjee, Brayton, "DAG-aware AIG rewriting," DAC 2006
- **OpenROAD / OpenROAD-flow-scripts (ORFS)** is the open RTL-to-GDS flow: floorplan, global placement, detailed placement, CTS (clock-tree synthesis), global routing, and detailed routing, with OpenSTA for timing. Its many tunable flow parameters are what ORFS-agent tunes (see section 4). **[canonical]** — [The OpenROAD Project](https://theopenroadproject.org/); [ORFS-agent, arXiv 2506.08332](https://arxiv.org/abs/2506.08332) **[fetched]**
- **Localization is the important bridge between the verifier's report and the editable source.** The ICLAD paper's locator floods outward through the netlist from the critical-path endpoints to recover RTL modules. "Accurate but coarse localization outperforms precise but uncertain localization." The probabilistic line-level linker (SynAlign) scored 17.2% worse on average for Custom agents. **[fetched]** — [ICLAD 2026 paper](https://renau.github.io/docs/iclad26.pdf)

### Inferences (EDA concept → redstone analogue)
- **RTL/spec → door spec as a timed I/O trace.** "Input lever/button at tick t; door blocks open by tick t+k; closed by tick t+m; no extra blocks moved; holds state." This is the "gold" model. Write it as a small FSM (finite state machine) or truth table over (input, tick), not as prose.
- **AIG → a canonical redstone logic IR.** Before any blocks exist, lower the design to a graph of {OR (dust merge), NOT (torch), delay (repeater k ticks), pulse-gen, T-flip-flop, observer-pulse, sticky/non-sticky piston actuation}. AIG-style local rewrites carry over directly, for example removing double torch inversions, merging repeaters, and sharing a pulse generator across pistons. Redstone also has rewrites with no AIG counterpart: replace a torch+repeater with an observer, or use quasi-connectivity (QC) to drop a wire.
- **Technology mapping → covering the IR with a library of verified modules** (see section 6). The cost per cell is block count, volume, and tick delay.
- **Placement and routing → voxel placement with interference checks.** Unlike ASIC wires, redstone dust connects to neighbors, powers blocks, triggers QC, and decays over 15 blocks. "Routing" therefore needs a design-rule checker (DRC) for unintended adjacency. This is the redstone analogue of DRC/LVS (layout vs. schematic), and probably the main place where a cheap static checker saves engine runs.
- **STA → "tick-STA".** Redstone is effectively synchronous at game-tick granularity, so delays are discrete and mostly known statically (repeater 1–4 redstone ticks, torch 1 rt, piston extend 0 rt start/2 gt motion, and so on). A static pass can report per-path arrival time, "slack" against the spec's open/close deadline, and the critical path. It can also flag races, where two signals reach the same piston within the same tick and update-order issues decide the outcome. This is cheaper than simulation and gives localized feedback.
- **Equivalence checking → (a) trace equivalence on the real engine against the spec FSM over all input sequences up to bound N, which is BMC-like, plus (b) symbolic equivalence on the logic IR before placement.** The EQY idea of partitioning into matched fragments maps to verifying each module instance in isolation, then verifying only the glue.
- **Retiming-at-boundary → allow internal timing freedom.** Only the externally visible door behavior (which blocks are where at which tick) should be checked, not internal signal timing. This is the right level of abstraction for "minimal door" scoring.
- **Cheap pre-filter → schema/DRC validation before the engine run.** The ICLAD Slang pre-filter result suggests a fast static validator with rich diagnostics will cut wasted engine runs, especially if the real-engine sim is the bottleneck (as synth/LEC is in EDA).

### Gaps
- I did not fetch the EQY partitioning/strategy pages, so I can't confirm whether EQY emits counterexample traces on failure. (SBY-based strategies normally produce VCD traces, but this is from memory.)
- I did not re-read ABC docs or the DAG-aware rewriting paper for exact command semantics.

---

## 2. LLMs in EDA, 2023–2026: benchmarks, domain models, AlphaChip, AlphaEvolve, OpenAI Jalapeño

### Takeaway
Spec-to-Verilog generation on early benchmarks is close to saturated: frontier models score about 90% on VerilogEval-Human. Harder benchmarks (CVDP, ChipBench) remain around 30–37%. The verified "LLM touched real silicon" results are narrow and verifier-gated. AlphaEvolve proposed a Verilog bit-width simplification that passed verification and went into a TPU. OpenAI says its models helped design Jalapeño, and the 10% matmul-area figure is OpenAI's own unverified claim. AlphaChip remains contested. The independent replication (Cheng/Kahng et al., v3 March 2026, accepted to IEEE TCAD) still disputes its claims.

### Cited Findings
**Benchmarks**
- **VerilogEval** (NVIDIA, Liu, Pinckney, Khailany, Ren; ICCAD 2023) is spec-to-Verilog on HDLBits-derived problems, scored by simulation. **[canonical]** — [arXiv 2309.07544](https://arxiv.org/abs/2309.07544)
- **RTLLM** (Lu et al., ASP-DAC 2024) is an open benchmark of about 30 design-level RTL generation tasks, checked for syntax, functionality, and design quality. **[canonical, task count from memory]** — [arXiv 2308.05345](https://arxiv.org/abs/2308.05345)
- **Saturation:** an NVIDIA-hosted community leaderboard (not peer-reviewed) lists Claude Opus 4.6 at 90.8% on VerilogEval-Human V1 over 10 rollouts, GPT-5.3 Codex at 89%, and Gemini 3.1 Pro at 86.3%, and describes a plateau. **[search snippet only]** — [NVIDIA explainer space](https://nvidia-llm-rtl-errors-explainer.hf.space/)
- **CVDP** (NVIDIA, 2025) was built because prior benchmarks are "increasingly saturated". At launch, Claude 3.7 Sonnet, GPT-4.1, and Llama 3.1 405B reached ≤34% pass rate on code generation. **[search snippet]** — [arXiv 2506.14074](https://arxiv.org/html/2506.14074v1)
- **ChipBench** (Jan 2026) reports Claude-4.5-opus at 30.74% on Verilog generation and 13.33% on Python reference-model generation. The multi-agent MAGE system scores 95% on VerilogEval but only 37% on ChipBench. **[search snippet]** — [arXiv 2601.21448](https://arxiv.org/pdf/2601.21448)
- **Agentic CVDP (Mar 2026):** "naive agentic wrapping around frontier models can degrade performance" relative to optimized single-pass prompting. Structured harnesses "can match and sometimes exceed" non-agentic baselines. The open-vs-closed model gap is attributed to "higher crash rates and weaker interpretation of tool output". **[fetched abstract]** — [Yubeaton, Garg, Hegde, arXiv 2603.19347](https://arxiv.org/abs/2603.19347)

**Domain-adapted models**
- **ChipNeMo** (NVIDIA, 2023) applied domain-adaptive continued pretraining, SFT, and domain-adapted retrieval on LLaMA2 to three internal tasks: an engineering assistant chatbot, EDA script generation, and bug summarization/analysis. **[canonical]** — [arXiv 2311.00176](https://arxiv.org/abs/2311.00176)
- 2026 work still trains RTL-specialized models (for example ACE-RTL, which claims up to +21.45% pass rate over Claude 4 and GPT-5 baselines on CVDP). However, the leading agentic results in sections 3–4 use general frontier models with tools. **[search snippet]** — [ACE-RTL, arXiv 2602.10218](https://arxiv.org/html/2602.10218v2)

**AlphaChip and its controversy**
- **Original claim:** RL macro placement producing floorplans comparable to or better than humans in under 6 hours, used in TPU generations. **[canonical]** — [Mirhoseini et al., Nature 2021](https://www.nature.com/articles/s41586-021-03544-w)
- **Independent reassessment, v3 (10 Mar 2026; accepted to IEEE TCAD):** builds a stronger multi-threaded "go-with-the-winners" simulated-annealing baseline and new sub-10nm testcases (7nm Ariane, ASAP7), evaluated with commercial P&R post-route PPA. Says some claims, including scalability and the pre-training methodology, "remain unconfirmed". All data and flows are public in the MacroPlacement GitHub repo. **[fetched abstract]** — [Cheng, Kahng, Kundu, Wang, Wang, arXiv 2302.11014v3](https://arxiv.org/abs/2302.11014v3)
- **Markov's CACM meta-analysis,** using Cheng/Kahng data: Circuit Training took 32.31 h, simulated annealing 12.5 h, and Cadence's commercial macro placer 0.05 h. Markov is quoted as saying "It's not better than annealing." **[search snippet via CACM coverage]** — [CACM "Updates spark uproar"](https://cacm.acm.org/news/updates-spark-uproar)
- **A 2025 update reportedly confirmed** that under full routing, Circuit Training "never produced shorter wire length than the commercial tool while using far more computation." **[secondary summary only]** — [bits&chips](https://bits-chips.com/?p=234065)
- **Google's rebuttal, "That Chip Has Sailed"** (Nov 2024), argues Cheng et al. did no pre-training. It says Nature's April 2024 investigation "found entirely in our favor" and chose an addendum over a correction. I could not independently verify the Nature outcome. **[search snippet]** — [arXiv 2411.10053](https://arxiv.org/html/2411.10053v1)

**AlphaEvolve TPU Verilog**
- **AlphaEvolve (14 May 2025)** "proposed a Verilog rewrite that removed unnecessary bits in a key, highly optimized arithmetic circuit for matrix multiplication." The proposal "had to pass robust verification methods" and "was integrated into an upcoming Tensor Processing Unit." Other numbers in the same post: 0.7% of Google fleet compute recovered by a Borg heuristic, a 23% matmul kernel speedup (1% of Gemini training time), up to 32.5% FlashAttention kernel speedup, and 48 scalar multiplications for 4×4 complex matmul. **[fetched]** — [DeepMind blog](https://deepmind.google/discover/blog/alphaevolve-a-gemini-powered-coding-agent-for-designing-advanced-algorithms/)

**OpenAI Jalapeño: what is verified**
- **Real product, real claims.** Jalapeño is an OpenAI + Broadcom LLM-inference accelerator, announced 24 June 2026, with an architecture talk at Hot Chips (25 Aug 2026). OpenAI's primary page exists but returned HTTP 403 to my fetch, so the claims below come via secondary sources. — [OpenAI page (403)](https://openai.com/index/openai-broadcom-jalapeno-inference-chip/); [The Register](https://www.theregister.com/systems/2026/08/25/openais-upcoming-jalapeno-chip-looks-like-itll-be-an-inference-beast/5292052)
- **Claims attributed to OpenAI (Richard Ho, Chris Leary)** in IEEE Spectrum (14 Sep 2026) **[fetched]**:
  - Concept to first silicon in under 20 months, and 9 months from first RTL to tape-out.
  - An average team of fewer than 100 people, excluding Broadcom.
  - AI-guided design cut matmul-unit area by **10% vs an optimized human baseline** (Hot Chips 2026).
  - A DeepSeek MLA kernel went from 0.31% to 88.94% of theoretical ceiling in about 40 hours after silicon returned in May 2026.
  - No quantified verification results.
  - Broadcom did most of the backend, so AI was less useful there.
  - Ho: "We're not saying that anyone can come and just build state-of-the-art, frontier AI/ML accelerator chips" with only Codex.

  Andrew Kahng called the schedule "likely best in class today". Spectrum notes that the figures are OpenAI's and not independently verified. — [IEEE Spectrum](https://spectrum.ieee.org/llms-for-chip-design)
- **Another secondary source** (Neoteo, 25 Sep 2026) says the models helped with design exploration, shortened design/measurement/verification loops, and optimized arithmetic circuits. It says they were most useful in software-like front-end work using **XLS** (Google's HLS toolchain) and that engineers made the final decisions. It cites no primary document. **[fetched]** — [Neoteo](https://www.neoteo.com/en/how-openai-used-ai-in-jalapeno-chip-design)
- **An "8% SIMD area reduction"** appears only in a search snippet attributed to SemiAnalysis, and IEEE Spectrum does not report it. **Unverified.** — [SemiAnalysis (paywalled, not fetched)](https://newsletter.semianalysis.com/p/openai-jalapeno-better-than-nvidia)
- **Inconsistency to note:** Spectrum's summary calls the 10% "AI-guided physical design", while Neoteo puts AI's value in front-end/arithmetic work and says backend AI use was limited. The Hot Chips slides themselves were not reviewed.

**Vendor agentic EDA (2026)**
- **Synopsys AgentEngineer** runs on an "Autopilot Platform" announced 28 Sep 2026. Synopsys reports more than 50 customer engagements, with GA (general availability) planned for end of 2026.
- **Cadence ChipStack "AI Super Agent"** (Feb 2026) targets front-end design and verification and is marketed as "Level-5" autonomy.
- **Speedups are vendor-reported:** "40x faster RTL validation" (NVIDIA citing Cadence) and "up to 50x" (Synopsys). Unite.AI notes that every performance figure comes from the companies selling the tools.
- **[search snippets]** — [Tom's Hardware](https://www.tomshardware.com/tech-industry/semiconductors/the-state-of-agentic-ai-in-chip-design-tools-in-2026-cadence-synopsys-and-siemens-all-pitch-autonomous-engineers); [Futurum](https://futurumgroup.com/insights/cadence-and-synopsys-accelerate-agentic-eda-race-at-computex); [Unite.AI](https://www.unite.ai/synopsys-hands-chip-verification-to-autonomous-ai-agents/)

### Inferences
- **The successful LLM-in-silicon results share a structure: the LLM proposes and a formal or simulation verifier disposes.** Examples are AlphaEvolve's verified Verilog rewrite and OpenAI's arithmetic-circuit work. None of them has the LLM replace placement, routing, or SAT engines.
- **The "Piston Door Bench" grader is analogous to the verification gate.** Making the gate fast and informative matters more than model choice.
- **Saturation pattern:** easy benchmarks saturate fast, then harder long-horizon benchmarks reset scores to about 30%. Expect the same for redstone, where single-module doors are easy and multi-piston flush doors with timing constraints are hard. Plan a tiered benchmark.

### Gaps
- I could not read OpenAI's primary Jalapeño post (403) or the Hot Chips slides. The exact design task behind the 10% figure (arithmetic circuit vs. physical design) is unresolved.
- I did not find exact VerilogEval/RTLLM original-paper pass@1 figures in this session.
- I found no lab chip-design result from Anthropic, or from any other lab, beyond DeepMind and OpenAI.

---

## 3. Verifying the two agentic-EDA claims made by another AI

### Takeaway
**Claim (a) is accurate.** The averages are exact (Skills 22.8% vs Custom 21.6% average Fmax gain, with mandatory sequential SAT-based LEC). The reader should know three caveats: each cell is a single trajectory, a no-skills coding agent got about 0–5%, and the paper's real finding is that the tool and verification loop matters more than orchestration style. **Claim (b) is accurate for the 350 MHz target** (DeepSeek-V4-Preview: FluxEDA 97.94 vs Claude Code + EDA Skills 11.67, an 8.39× ratio). It is close at 700 MHz (90.99 vs 11.67). However, the comparison rests on single runs from a benchmark built by FluxEDA's own authors, and other cells in the same table contradict a clean "harness ≫ skills" story.

### Cited Findings
**(a) "Are Skills Enough? An Agentic Frequency Optimization View for Large Chips"** — Jiahan Xie, Sakshi Garg, Jose Renau (UC Santa Cruz), ICLAD 2026, PDF dated 2026-08-12. **[fetched and fully read]** — [renau.github.io/docs/iclad26.pdf](https://renau.github.io/docs/iclad26.pdf)
- **Setup:**
  - Designs: CVA6 (Core, LSU), SoomRV Frontend, Vortex (Core, FPU), and Dino (SingleIssue, DualIssue), ranging from 1K to 39K LoC and from 11.5K to 671K gates.
  - Models: Opus 4.6 / Claude Code 2.1.75, GPT-5.3-codex / Codex CLI 0.114.0, and gemini-3.1-pro-preview / Gemini-cli 0.33.1, all at default (medium) effort.
- **Abstract:** "Skills and Custom agents achieve similar average Fmax gains (22.8% vs 21.6%)" with "mandatory SAT-based equivalence checking."
- **Checked arithmetic.** Table V averages for the S config are 27.5 / 20.1 / 20.7, which give a mean of 22.8. The C averages are 19.7 / 23.8 / 21.2, which give 21.6.
- **Per-model averages across config variants:**

  | Model | Skills | Custom |
  |---|---|---|
  | Opus 4.6 | 26.8% | 13.9% |
  | GPT-5.3 | 12.7% | 10.5% |
  | Gemini 3.1 | 17.5% | 18.5% |

  Best-config wins per target: Opus favors Skills 4–3, GPT favors Custom 6–1, Gemini favors Custom 4–3. "Neither paradigm consistently dominates."
- **Baseline coding agent without skills (CA) averages 0.0% (Opus), 5.3% (GPT), and 0.0% (Gemini).** "Claude CLI never invokes external tools to verify compilation or equivalence," so it shows the most syntax and LEC failures. Codex and Gemini CLIs sometimes discover yosys or iverilog, but "neither invokes a timing analysis tool even when explicitly instructed to improve frequency."
- **Locator:** enabling it adds +13.3% Fmax for Custom but only +4.5% for Skills, because Skills agents self-localize by grepping. Claude Code's S-L (no flood locator) beat S by about 5%. Technique ("ware/tech") prompts add +8.5% (C vs C-W) and +6.8% (S vs S-W).
- **Cost:** Skills use more tokens, with median S/C ratios of 32× (Opus), 23.4× (GPT), and 14.7× (Gemini). Runtime is similar, with median ratios of 1.01×, 0.75×, and 1.05×.
- **Emergent behavior:**
  - On Vortex, Claude Code grepped instantiation sites to find the real memory-banking bottleneck. When those files and signals were manually injected into the Custom pipeline, "all models achieved comparable improvements."
  - On Dino, Claude Code misidentified the ALU as the bottleneck, but its edit let synthesis retime the datapath anyway, which the paper calls "serendipitous".
- **Path dependence:** feeding other models' optimized outputs to GPT-5.3 improves them "but does not reach the Fmax it achieves from the original code," which suggests that "early architectural decisions strongly influence the final achievable frequency." Model diversity also helps when one model stalls.
- **Statistical caveat (from the paper itself):** "Each numeric cell is one completed optimization trajectory, not a repeated-seed mean… we therefore use these tables descriptively, not as statistical significance tests."
- **LEC details:** "sequential SAT-based logic equivalence checking," implemented with Yosys 0.60 per Table II. Failures go back to an LLM "LEC fixer" prompt for up to M retries.

**(b) FluxBench / "Can AI Agents Really Complete RTL-to-GDS? Lessons from Benchmarking Tool-Interactive EDA Workflows"** — Jinyuan Deng, Zhengrui Chen, Xufeng Wei, Tianyu Xing, Chenyi Wen, Qi Sun, Cheng Zhuo. Per fluxbench.net the authors are from Zhejiang University and **ChipFlux**, which builds FluxEDA. The paper is arXiv 2607.17528, v1 20 Jul 2026; **v2 withdrawn**; v3 23 Jul 2026. **[fetched]** — [fluxbench.net](https://fluxbench.net); [arXiv 2607.17528](https://arxiv.org/abs/2607.17528)
- **Task:** PicoRV32 RTL-to-GDS with commercial EDA tools (synthesis → P&R → timing ECO) at 350 MHz and 700 MHz targets. The site also lists NVDLA nv_small, but the case-study table is PicoRV32 only. The study has 24 runs: 3 architectures × 4 models × 2 targets.
- **Scoring:** overall = 20% stage score + 80% result score. Stage gates are sequential. The result score (area, power, setup WNS/TNS, hold WNS/TNS) is **zero unless all process gates pass**. Completion is judged from design artifacts, not from agent messages.
- **The DeepSeek-V4-Preview numbers:**

  | Architecture | 350 MHz score | 700 MHz score |
  |---|---|---|
  | FluxEDA | 97.94 ($0.56, 120.8 min) | 90.99 |
  | Claude Code + EDA Skills | 11.67 ($0.64, 111.7 min) | 11.67 |
  | Plain Claude Code | 13.33 | 10.00 |

  The "8.39×" headline is 97.94 / 11.67. The ~98 vs ~12 claim is therefore **accurate**.
- **Inconsistencies in the same table that complicate the story:**
  - **Claude Sonnet 5 in plain Claude Code scored 87.05 (350) / 81.33 (700), but with EDA Skills it scored 11.67 / 11.67.** Adding skills hurt it badly.
  - **GLM-5.2 with EDA Skills scored 95.97 (350)**, essentially matching FluxEDA's 97.72.
  - Kimi K3 in plain Claude Code scored 82.33 at 700 MHz but 13.33 at 350 MHz.
  - Every FluxEDA cell is between 90.99 and 98.26, so the structured harness is robust *across models*. The scores of 10–13.33 look like a floor: a partial stage score with the result score zeroed.
- **Paper's stated lessons:**
  - Skills improve subtask understanding but do not ensure long-horizon completion.
  - "Low-level tool-interface mismatches," such as version- and mode-dependent Tcl, are a major failure source.
  - Token ROI varies up to 141× among agents with similar progress.
  - Robust agentic EDA needs "structured tool interfaces, persistent design context, controlled execution, and process-level evaluation."
  - Secondary summaries add that general agents fall into failure loops, repeating wrong commands or failing to recover from a corrupted design state. **[alphaxiv summary]** — [alphaxiv overview](https://www.alphaxiv.org/overview/2607.17528)
- **The site's own caveat:** the results do not establish reliability across arbitrary designs or industrial signoff flows.

### Inferences
- **(a) and (b) are not contradictory, because they test different things.** In (a), the coding agent with skills is given a *tight, verifier-gated loop on a fixed, working design* (edit RTL, then compile, LEC, and STA), so the failure states are recoverable: revert the patch. In (b), the agent has to *drive a long, stateful, version-sensitive tool flow* (P&R on commercial tools), where a corrupted design database or a wrong Tcl command breaks everything downstream. That is the regime where a structured harness with persistent state wins.
- **For Piston Door Bench**, a build is a long stateful process only if the agent builds block by block in a live world. If instead the agent emits a complete declarative design, simulates it, and gets a report back, the regime looks like (a), and a lightly structured skills-style agent should do fine. The bigger lever is the verifier interface.
- **Both studies are n=1 per cell.** The FluxBench table's own variance (Sonnet 87 → 12 when skills are added) shows the noise is large enough that single-run harness comparisons are weak evidence. Piston Door Bench should run multiple seeds per cell.
- **Conflict of interest:** FluxBench is authored by the company that sells FluxEDA. The ICLAD paper has no comparable product interest.

### Gaps
- I did not read the full FluxBench paper's methodology for how "EDA Skills" were written. Poorly written skills could explain the Sonnet collapse. I also don't know why v2 was withdrawn.
- I could not find a "FluxEDA" architecture description in the arXiv abstract. The name appears only on the FluxBench site.

---

## 4. Bitter-lesson dynamics: does general learning+search beat hand-engineered heuristics in EDA?

### Takeaway
The pattern is mixed, and it is not "LLMs replace solvers". General learning has *not* displaced core combinatorial engines: SAT, analytical placement, routing, STA, and LEC. Learned RL macro placement (AlphaChip) failed to beat strong annealing or commercial baselines in independent tests. What *is* being bitter-lessoned is the **outer loop**: hand-written flow scripts, parameter tuning, solver heuristics as code, and RTL rewriting. In each case an LLM (often with evolutionary search) proposes and an exact solver or verifier checks. Even SAT solving now has a competition-winning solver whose heuristics an LLM evolved.

### Cited Findings
- **RL macro placement is not established as superior.** Cheng/Kahng v3 (March 2026) still reports unconfirmed scalability and pre-training claims against strong simulated-annealing and commercial baselines. The CACM coverage cites 32.31 h for Circuit Training, 12.5 h for SA, and 0.05 h for the commercial tool. **[fetched / snippet]** — [arXiv 2302.11014v3](https://arxiv.org/abs/2302.11014v3); [CACM](https://cacm.acm.org/news/updates-spark-uproar)
- **LLM agent tuning OpenROAD flow parameters (ORFS-agent, Kahng group):**
  - Six benchmarks on ASAP7/SKY130HD, compared against the OR-AutoTuner (Bayesian optimization) baseline.
  - Thinking-model backends (Sonnet 4.6, Kimi K2.5) improve wirelength by up to 1.0%, effective clock period by up to 1.3%, and co-optimization objectives by up to 2.7%, **with 40% fewer iterations**.
  - Over a Sonnet 3.5 backend, they improve by up to 7.5%, 3.1%, and 4.0%.
  - Open-weight Kimi K2.5 stays within 0.24% of Sonnet 4.6.
  - Retrieval tools speed early convergence but not final quality.
  - **[fetched]** — [arXiv 2506.08332](https://arxiv.org/abs/2506.08332)
- **LLM-evolved SAT heuristics won a competition:**
  - AESAT's AE-Kissat-MAB won first place in the main track of SAT Competition 2025 (IJCAI 2026). The authors describe it as the first LLM-enhanced solver to win.
  - NVIDIA's SATLUTION evolves whole solver repositories with planning and coding agents. Trained only on 2024 data, it reports the lowest PAR-2 (penalized average runtime) on the 2025 benchmark, ahead of the 2025 winners.
  - Both are self-reported. **[search snippets]** — [IJCAI 2026 AESAT](https://www.ijcai.org/proceedings/2026/257); [SATLUTION, arXiv 2509.07367](https://arxiv.org/html/2509.07367v1)
- **Earlier ML-guided SAT:** NeuroCore (Selsam & Bjørner, 2019) used a GNN to periodically refocus CDCL (conflict-driven clause learning) variable branching in MiniSat/Glucose and solved more SATCOMP problems. The learned component is a *heuristic inside* an exact solver, not a replacement for it. **[canonical]** — [arXiv 1903.04671](https://arxiv.org/abs/1903.04671)
- **RL for logic synthesis:** DRiLLS (Hosny et al., ASP-DAC 2020) used an A2C agent to choose sequences of ABC transformations, the same rewrite/refactor/balance commands, to minimize area under a delay constraint. It reported results comparable to or better than expert scripts on EPFL benchmarks. The learned part chooses *which verified transformation to apply next*, and ABC still performs the transformations. **[canonical, numbers not re-fetched]** — [arXiv 1911.04021](https://arxiv.org/abs/1911.04021)
- **LLM-guided e-graph rewriting:** ASPEN (MLCAD 2025, NVIDIA/Ren group) uses LLMs to generate e-graph rewrite rules for datapath optimization, so equivalence holds by construction. **[cited in ICLAD paper, fetched]** — [ICLAD 2026 refs](https://renau.github.io/docs/iclad26.pdf); [IEEE Xplore 11189222](https://ieeexplore.ieee.org/document/11189222)
- **Verifier-gated LLM rewriting of real RTL** gives 10–30% Fmax gains on processor-scale designs (ICLAD 2026, section 3). AlphaEvolve's TPU bit-width rewrite is another example (section 2).
- **Search over model trajectories matters.** ICLAD 2026 reports path dependence: early choices limit final Fmax, and model diversity rescues stalled runs. This argues for population or tree search over full designs rather than one long greedy agent trajectory. **[fetched]** — [ICLAD 2026](https://renau.github.io/docs/iclad26.pdf)
- **Vendor framing (2026):** Cadence, Synopsys, and Siemens all pitch "autonomous engineer" agents that orchestrate existing engines. None claims to replace the engines. **[snippet]** — [Tom's Hardware](https://www.tomshardware.com/tech-industry/semiconductors/the-state-of-agentic-ai-in-chip-design-tools-in-2026-cadence-synopsys-and-siemens-all-pitch-autonomous-engineers)

### Inferences
- **Bitter-lesson reading for EDA in 2026:** general methods (LLMs plus search such as evolution or MCTS) are displacing *human-written heuristics and scripts*, the "glue" and the "rules of thumb". They are not displacing *exact solvers and verifiers*. Those verifiers are the reward signal that makes the general search work. Better compute makes the verifier more valuable, not less.
- **For redstone:** do not try to learn the simulator or ask the LLM to "reason out" tick timing. Keep the real-engine sim as the oracle, and add cheap exact sub-solvers where they exist: tick-STA, a DRC/adjacency checker, a small SAT/BMC over the logic IR, and maybe a brute-force or ILP placer for small module layouts. Let the LLM do the part humans currently do: pick topologies, choose which rewrite to try, and decide which module to swap.
- **A DRiLLS-style "agent picks the next verified transformation" setup** fits a redstone rewrite library well. Each rewrite (merge repeaters, observer substitution, QC trick) is pre-verified for equivalence under stated conditions, and search picks the sequence.
- **SATLUTION/AESAT suggest a second-order move:** let the LLM evolve the *harness's own heuristics*, such as candidate-ranking functions or module-selection policies, scored against a benchmark set.

### Gaps
- I did not re-fetch DRiLLS or NeuroCore numbers.
- I found no 2025–26 independent evidence that learned (non-LLM) placement or routing beats commercial tools in production. The DREAMPlace-style GPU analytical placement is compute-scaling, not learning, and was not re-verified here.
- The AESAT/SATLUTION competition claims were not independently verified against the official SAT Competition 2025 results page.

---

## 5. Interface lessons: structured outputs, persistent state, counterexamples, incremental verification

### Takeaway
There is strong and consistent evidence that **the tool and verification interface matters as much as, or more than, model choice** for agentic hardware tasks. In ICLAD 2026, no-tools agents got about 0–5% while tool-gated agents got about 20%. In FluxBench, a structured harness put all four models at 91–98, while unstructured setups ranged from 10 to 96 depending on the model. On agentic CVDP, naive agent wrapping *hurts* and structured harnesses help. Open-model gaps trace back to tool-output interpretation and crashes.

### Cited Findings
- **The tool loop dominates:** CA (no skills or tools) scored 0.0 / 5.3 / 0.0% versus about 20–24% with the verifier-gated loop for the same models (ICLAD 2026). Claude Code without skills "never invokes external tools to verify compilation or equivalence." **[fetched]** — [ICLAD 2026](https://renau.github.io/docs/iclad26.pdf)
- **The harness compresses model variance:** with FluxEDA, all 8 model×target cells score 90.99–98.26. With Claude Code ± skills, cells range from 10.00 to 95.97, and the same model can swing about 75 points between architectures. **[fetched]** — [fluxbench.net](https://fluxbench.net)
- **Failure sources, per the FluxBench authors:** "low-level tool-interface mismatches," especially version- and mode-dependent Tcl. Their prescription is "structured tool interfaces, persistent design context, controlled execution, and process-level evaluation." **[fetched abstract]** — [arXiv 2607.17528](https://arxiv.org/abs/2607.17528)
- **Agentic CVDP:** naive agentic wrapping degrades performance, while structured harnesses match or exceed. The open-vs-closed gap comes from "higher crash rates and weaker interpretation of tool output." **[fetched abstract]** — [arXiv 2603.19347](https://arxiv.org/abs/2603.19347)
- **Rich diagnostics reduce retries.** Slang's richer messages let the syntax-fixer "converge in fewer retries." LEC failures are fed back into a dedicated fixer prompt. **[fetched]** — [ICLAD 2026](https://renau.github.io/docs/iclad26.pdf)
- **Structured hints beat model cleverness on parameter choice.** In SoomRV, "when the register-array structure and banking configuration space are made explicit in the prompt, agents consistently select better schemes." **[fetched]** — [ICLAD 2026](https://renau.github.io/docs/iclad26.pdf)
- **Localization is part of the interface.** A coarse-but-accurate locator beat a precise-but-probabilistic one. Wrong localization "mislead[s] the agent into modifying irrelevant procedural blocks." **[fetched]** — [ICLAD 2026](https://renau.github.io/docs/iclad26.pdf)
- **Process-level grading:** FluxBench scores completion "from design artifacts rather than agent progress messages." **[fetched]** — [fluxbench.net](https://fluxbench.net)
- **Model choice still matters, but less.** ORFS-agent's open Kimi K2.5 stays within 0.24% of Sonnet 4.6 inside the same harness. Upgrading from Sonnet 3.5 to thinking models was worth up to 7.5%. **[fetched]** — [arXiv 2506.08332](https://arxiv.org/abs/2506.08332)

### Inferences (concrete harness recommendations for Piston Door Bench)
1. **Return a structured verdict, not logs.**
   - Pass/fail per spec clause (opens by tick X, closes by tick Y, flush, no stray blocks).
   - Per-piston actuation timeline.
   - A **minimal counterexample trace**: the shortest input sequence and tick at which the observed state diverges from the spec, plus a diff of expected vs actual block positions. This is the analogue of an LEC/BMC counterexample or a VCD waveform.
2. **Add tick-STA output to every run:** critical path from input to each piston, arrival tick vs deadline (slack), and same-tick race warnings. This is the "timing report" the agent localizes from.
3. **Add localization:** map each failed clause back to the specific module instance or blocks responsible, coarse but accurate (flood outward from the failing piston through the signal graph). ICLAD shows that a wrong fine-grained localization is worse than a correct coarse one.
4. **Persist design state:** keep the current best verified design, a history of tried edits and their verdicts, and the cache of verified modules on the server side. Let the agent apply patches (diffs) rather than resend the whole build. This addresses FluxBench's failure loops and corrupted state.
5. **Run a cheap pre-filter before the real engine:** schema validation, DRC/adjacency, and IR-level symbolic check. Feed rich diagnostics back. This is the Slang lesson, and it matters most if engine runs dominate wall-clock time as synth/LEC do.
6. **Gate on equivalence, grade on cost:** accept only designs that pass the spec, then rank them by block count, volume, and tick latency. This is the "LEC-gated, Fmax-scored" pattern.
7. **Use a stable, version-pinned action API:** avoid free-form commands whose semantics depend on the Minecraft version or tool mode. That is the Tcl-mismatch lesson. Pin the MC version, and expose it in the tool output.
8. **Measure the harness, not just the model:** report score, cost, and runtime ("token ROI"), and run multiple seeds per cell, because both cited studies are n=1 and one shows ±75-point swings.

### Gaps
- I found no study that isolates *counterexample traces specifically* as a variable in LLM hardware agents. The recommendation follows from the LEC-fixer and diagnostics evidence plus CEGIS (counterexample-guided inductive synthesis) practice, not from a direct ablation.
- I found no published ablation of persistent state versus stateless interfaces beyond FluxBench's qualitative claims.

---

## 6. Standard-cell libraries and technology mapping as analogues for a library of verified redstone modules

### Takeaway
Standard-cell design separates *characterizing* a small set of cells once (function, area, delay tables, pin positions) from *mapping* arbitrary logic onto them. Tech mapping is then cut-based covering that minimizes area under delay constraints. A redstone module library (verified pulse extenders, T-flip-flops, piston drivers, 2×2/3×3 door cores, BUD/observer clocks) with characterized footprint, tick delay, and port positions would let the agent and search work at the module level. It would also turn equivalence checking into "verify modules once, then verify glue."

### Cited Findings
- **Liberty-characterized libraries feed the flow.** ICLAD 2026's prompts include "standard-cell library characteristics," and all metrics come from Yosys/ABC mapping onto sky130A. **[fetched]** — [ICLAD 2026](https://renau.github.io/docs/iclad26.pdf)
- **A curated library of verified transformations retrieved by RAG helps.** "Resource-replacement patterns are retrieved on demand via RAG from a curated library" (for example carry-select adders, array banking, pipeline restructuring). Technique prompts plus designware add +6.8 to +8.5% Fmax. **[fetched]** — [ICLAD 2026](https://renau.github.io/docs/iclad26.pdf)
- **ABC technology mapping** (`map` against a genlib/Liberty library, `&if` for LUTs) uses cut enumeration on the AIG and selects covers by area and delay. Structural choices (`dch`) let the mapper pick among equivalent structures. **[canonical]** — [ABC](https://people.eecs.berkeley.edu/~alanmi/abc/)
- **Modular equivalence:** EQY partitions gold and gate designs into matched fragments and proves each with its own strategy. **[fetched, ToC]** — [EQY docs](https://yosyshq.readthedocs.io/projects/eqy/en/latest/)
- **Correct-by-construction rewriting:** ASPEN's LLM-generated e-graph rules keep equivalence by construction. **[via ICLAD refs]** — [IEEE Xplore 11189222](https://ieeexplore.ieee.org/document/11189222)

### Inferences
- **Each library entry should carry a "Liberty for redstone" record:**
  - Logical function (as an IR fragment or FSM).
  - Bounding box and block count.
  - Input and output port coordinates and facings.
  - Input-to-output delay in game ticks, including min/max and pulse-length requirements.
  - Keep-out and adjacency constraints (which neighbors break it: QC, dust connections, slime/honey stickiness, movable vs immovable blocks).
  - Orientation and mirroring variants.
  - Version validity.
  - A stored engine-verified test trace.
- **Technology mapping becomes:** given the spec FSM → logic IR, cover it with library modules to minimize blocks or volume under a tick-latency constraint. For small doors this can be exhaustive or ILP. The LLM is better used for choosing the *topology* (which door family) than for gate-level covering.
- **Hierarchical verification:** verify each module once in the engine, then check composed designs for (a) port timing compatibility via tick-STA and (b) adjacency/DRC violations between modules. Run the full engine sim only as signoff. This mirrors "characterized cells + STA + DRC + final signoff sim".
- **Grow the library from benchmark winners:** this is EDA's designware/IP-reuse loop. Any submitted design that passes the grader and is better than the library entry for its function gets characterized and added. That compounds over runs and lines up with the AlphaEvolve/SATLUTION "evolve the toolkit" pattern.
- **Caveat specific to redstone:** unlike CMOS cells, redstone modules interact through space (power leakage, QC, piston push limit of 12 blocks, block-update order). A purely logical cover can be unbuildable. That is why the adjacency/keep-out fields and a DRC are not optional. This is the redstone analogue of why physical-aware synthesis exists.
- **Minimal doors (the user's goal) often come from cross-module sharing,** such as one observer driving two functions or pistons doubling as wiring. A module library biases search toward modular, non-minimal solutions. Use the library for *feasibility* and seeding, then run a post-mapping "resynthesis/rewriting" pass that tries to merge and share across module boundaries, re-verified by the engine. This mirrors ABC's rewrite-after-map and the ICLAD finding that broad (cross-module) localization enables wins that narrow localization misses.

### Gaps
- I did not find any prior academic work that formalizes Minecraft redstone as a technology library, or that applies EDA tools (Yosys or ABC) to redstone, in this session. Community tools exist (for example Verilog-to-redstone compilers), but I did not search for or verify them here.
