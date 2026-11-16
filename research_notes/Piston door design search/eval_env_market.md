# Market for AI evals and RL environments sold to frontier labs (2025–2026), and where a Minecraft piston-door simulator fits

Source-quality note: some findings below came through search-engine summaries rather than pages fetched directly, and are marked "(search summary; not fetched)". Pages fetched directly: Epoch AI FAQ, TechCrunch Sept 2025, the AfterQuery blog, the Latent Space Good Start Labs interview, the Mechanize blog, Prime Intellect's scaling-environments post, Scale's AgentEnv post, the HF "RL environments 2026" blog, the SciCrafter arXiv abstract, the micro1 homepage, the GameLab/Arkadium about page, and GitHub/adamholter. rl-list.com could not be fetched (SSL error).

## Q1. What do the vendors sell, to whom? (and who is "tinier labs"?)

### Takeaway
Three groups sell to frontier labs. (a) Expert-labor/data incumbents (Mercor, Surge, Scale, Handshake, Turing, micro1) have added RL-environment arms. (b) Boutique environment builders (Mechanize, AfterQuery, Good Start Labs) build a small number of high-fidelity environments and task packs. (c) Open hubs and infrastructure (Prime Intellect Environments Hub, OpenEnv, Tinker) mostly serve smaller labs and open-source work. Most demand is for coding, computer-use app clones and enterprise workflows. Games are a small niche, served mainly by Good Start Labs, Scale's AgentEnv game plugins and GameLab (Arkadium). No vendor called "Tinier Labs" exists in search results. The closest matches are Thinking Machines' Tinker (a training API, not an environment vendor) and Onix "Tiny Labs" (small language models, unrelated).

### Cited Findings
**Market structure / incumbents**
- Scale AI, Surge and Mercor are all building RL environments. Surge's CEO Edwin Chen reports a "significant increase" in lab demand, and Surge set up an internal organization to build environments — [TechCrunch, Sept 2025](https://techcrunch.com/2025/09/16/silicon-valley-bets-big-on-environments-to-train-ai-agents/)
- Mercor pitches RL environments for domain-specific tasks (coding, healthcare, law) and has worked with OpenAI, Meta and Anthropic. Valued at $10B at the time — [TechCrunch](https://techcrunch.com/2025/09/16/silicon-valley-bets-big-on-environments-to-train-ai-agents/)
- Scale AI ($29B valuation after Meta's $14B investment) lost Google and OpenAI as data customers and now builds agent and RL environments (head of product for agents/RL envs: Chetan Rane) — [TechCrunch](https://techcrunch.com/2025/09/16/silicon-valley-bets-big-on-environments-to-train-ai-agents/)
- Scale open-sourced **AgentEnv** (post dated 10/5/2026). It says every RL environment Scale builds runs on it: composable blocks (apps such as Slack/Gmail, data artifacts, rules), tasks built as graphs of steps, and 48 built-in step types. Grading can be rubric-based or a strict check, and can cover trajectory and/or outcome. Stated quality criteria are realistic, accurate (reward reflects real behavior, not setup noise) and scalable — [Scale Labs, AgentEnv](https://labs.scale.com/blog/introducing-agentenv)
- AgentEnv plugins include a **"Minecraft/Catan/Poker RL Env"** ("Frontier models play poker, CATAN and Minecraft with and against each other") and an OpenCiv3 plugin — [Scale Labs](https://labs.scale.com/blog/introducing-agentenv)
- Epoch names Mercor, Surge, Handshake and Turing as data providers in the RL-environment market — [Epoch AI Gradient Updates, Jan 12 2026](https://epoch.ai/gradient-updates/state-of-rl-envs)
- Mercor reports a $2B annualized gross revenue run rate, double the figure four months earlier. The Information reports Mercor pays 60–70% of topline to contractors. Mercor agreed to acquire RL-environment startup Deeptune — (search summary; not fetched) [Dealroom, Jul 6 2026](https://dealroom.co/news/137121-mercor-doubles-to-2b-gross-revenue-run-rate-as-ai-labs-buy-expert-data/); [The Information](https://feature.theinformation.com/articles/handshake-mercor-revenue-surges-demand-human-contractors-train-ai)
- Handshake crossed $1B gross ARR (Apr 2026). Sacra estimates ~$450M net. Handshake bought Cleanlab in Jan 2026 to expand into evals and RL environments — (search summary; not fetched) [Dealroom](https://dealroom.co/news/127345-handshakes-arr-crosses-1b-as-ai-training-revenue-surges/); [Sacra](https://sacra.com/research/handshake-indeed-for-data-labelers/)
- Surge revenue is reported as ~$1.2B for 2024 (TechCrunch: "$1.2 billion in revenue last year from AI labs"). One secondary source claims ~$2B gross run rate in mid-2026, but the figures don't reconcile — [TechCrunch](https://techcrunch.com/2025/09/16/silicon-valley-bets-big-on-environments-to-train-ai-agents/); (search summary) [Enterprise DNA](https://enterprisedna.co/resources/ai-map/company/surge-ai)

**micro1 (Realm)**
- micro1 sells **Realm**, described as "RL environments that mirror real-world scenarios to generate world-class human data for agentic actions." It also sells **Cortex** ("contextual evaluation platform" for agents), expert robotics data, and public benchmarks (Dual-Arm Sim, MissionReport, Medical Index). The homepage lists no game environments and no revenue or customer numbers — [micro1.ai](https://micro1.ai/)
- micro1's roadmap ties Realm to a planned reward-model-as-a-service API, giving a W-2 taxation RL environment as an example — (search summary; not fetched) [micro1 roadmap](https://www.micro1.ai/roadmap)

**Mechanize**
- Founded ~6 months before Sept 2025 with the goal of "automating all jobs." It starts with coding-agent environments and aims to supply "a small number of robust RL environments" rather than many simple ones. It offers $500K salaries to the engineers who build them. Two sources say it has worked with Anthropic; both companies declined comment — [TechCrunch](https://techcrunch.com/2025/09/16/silicon-valley-bets-big-on-environments-to-train-ai-agents/)
- Mechanize argues that spending well under ~$500/task is inefficient and predicts tasks will cost "a few thousand dollars per task" within a year, moving toward full-time domain experts and away from procedural generation (Aug 18 2025) — [Mechanize blog](https://www.mechanize.work/blog/cheap-rl-tasks-will-waste-compute/)

**AfterQuery**
- Sells expert-built task datasets (e.g., "Office Agent" tasks resembling GDPval). See Q2 for the NVIDIA verification — [AfterQuery blog, Jul 2 2026](https://www.afterquery.com/blog/how-afterquery-helped-nvidia-hill-climb-gdpval)

**Good Start Labs**
- Sells "data and learning environments," mainly to frontier labs for RL. Products include game-play trajectories (observations, decisions, actions, outcomes), custom data for game publishers, and full games played end to end. It raised $3.6M (General Catalyst, Inovia, Every, angels) and was spun out of Every — [Latent Space](https://latent.space/p/good-start-labs)

**GameLab (Arkadium)**
- A division of Arkadium that uses games "as structured environments to study reasoning, strategy, and behavior." It builds "systems for training, evaluation, and benchmarking" and sells "rare, structured, exclusive human decision data." It lists Google DeepMind and Meta AI as "Frontier Model Partners" and thanks Good Start Labs — [GameLab about](https://gamelab.com/about)

**Prime Intellect (Environments Hub)**
- Launched an RL Environments Hub ("Hugging Face for RL environments") aimed at smaller developers. Its main business is compute — [TechCrunch](https://techcrunch.com/2025/09/16/silicon-valley-bets-big-on-environments-to-train-ai-agents/)
- As of Oct 27 2025: 400+ environments/evals crowdsourced in two months. Bounties run ~$100–500 for open-access tasks and larger amounts (~$1K–5K+, partly garbled on page) for application-only tasks, with "hundreds of thousands of $" committed in grants. Domains: AI research, frontier evals, browser automation, theorem proving, subject QA, legal/finance. Games are not listed. Sponsors can fund bounties for custom environments — [Prime Intellect blog](https://primeintellect.ai/blog/scaling-environments-program)
- A later claim of 2,500+ hub environments comes from a secondary site only — (search summary; unverified) [dailyaiworld](https://dailyaiworld.com/blogs/prime-intellects-rl-environment-hub-hits-2500-open-source)

**OpenEnv / infrastructure**
- Mercor and Fleet AI sit with Prime Intellect on OpenEnv's technical committee. 4,000+ HF Spaces carry the openenv tag. Labs mostly assemble their RL stacks in-house (GLM-5: 10k+ verifiable environments; Cursor: hundreds of thousands of concurrent sandboxes) — [HF blog, Sept 11 2026](https://huggingface.co/blog/sergiopaniego/rl-environments-2026)

**"Tinier labs"**
- Tinker is Thinking Machines Lab's managed fine-tuning/RL API, launched in private beta Oct 1 2025. Environments and RL algorithms are user code. Its cookbook connects to Prime Intellect's Environments Hub, and its page shows a Mercor case study ("Validate how RL environments improve agents on professional tasks") — (search summary) [Thinking Machines Tinker](https://thinkingmachines.ai/tinker/); [Tinker docs verifiers recipe](https://tinker-docs.thinkingmachines.ai/cookbook/recipes/verifiers-rl/)
- A search for "Tinier Labs" found no such company. The nearest name is Onix "Tiny Labs" (Montreal, small language models, launched Sept 28 2026), which is unrelated — (search summary) [Webull/Onix](https://www.webull.com/news/15656133740397568)

### Inferences
- "Tinier labs" most likely means **Tinker (Thinking Machines)**, or the user meant "tinier labs" literally (smaller/neo-labs, which Prime Intellect targets). Tinker is a *buyer-side channel*: an environment published in verifiers/Environments Hub format becomes trainable on Tinker for free. It is not a vendor that would pay for one.
- Game environments do have a commercial channel (Good Start Labs, GameLab, Scale's AgentEnv plugins), but it is a small, multiplayer/strategy-game niche. No vendor visibly sells construction or physics-engineering game environments.

### Gaps
- Turing's specific environment offerings and pricing were not researched (only named by Epoch).
- No identifiable "Habitat-like game-env shop" was found beyond Good Start Labs, GameLab/Arkadium and Scale's plugins. Meta's Habitat is an embodied-AI simulator, not a vendor.
- rl-list.com mentions a "$500M gross run rate (TechCrunch, Aug 2026)", a "$100M+ raise at $4B (Forbes, Sept 2026)", "Prime Intellect $130M led by Radical Ventures (Jul 8 2026)" and "Mechanize $9.1M at $500M post (Apr 24 2026)". All came via a search summary of an aggregator that could not be fetched, so the subjects and figures are **unverified**.

## Q2. Verify: (a) NVIDIA used AfterQuery office-work tasks to post-train Nemotron 3 Ultra; (b) Good Start Labs builds game-engine reward environments and runs private pre-release evals

### Takeaway
(a) **Supported by the vendor's own account; independent check pending.** AfterQuery says it is "the only data partner named in the Nemotron 3 Ultra technical report," which refers to "AfterQuery (AQ) tasks that share important latent structure with GDPval." This research did not read the NVIDIA report directly. (b) **Game-engine rewards: confirmed** by the founder interview. **Private pre-release evals: weakly supported.** The only evidence is Duffy saying in a podcast that they evaluated GPT-5 with OpenAI ahead of release. No evals product or recurring pre-release service was found.

### Cited Findings
- AfterQuery: NVIDIA used its Office Agent tasks for Nemotron 3 Ultra (550B-A55B LatentMoE). A strong model generated full trajectories, and intermediate decision points were reused as pivots (PivotRL, arXiv 2603.21383) during the MOPD (multi-teacher on-policy distillation) stage. GDPval: student 28.9 → 35.3 (no warmup) → 46.7 (warmup), against a teacher at 49.5. BrowseComp: 31.0 → 44.4. HLE: 25.6 → 26.7. Pricing and task counts not disclosed — [AfterQuery blog, Jul 2 2026](https://www.afterquery.com/blog/how-afterquery-helped-nvidia-hill-climb-gdpval)
- Nemotron 3 Ultra technical report is on HF Papers (2606.15007). Release date Jun 4 2026 per Artificial Analysis — (search summary; not fetched) [HF papers](https://huggingface.co/papers/2606.15007.md); [Artificial Analysis](https://artificialanalysis.ai/es/articles/nvidia-nemotron-3-ultra-released)
- Nuance on the claim: the method is **on-policy distillation with AfterQuery-derived pivots**, not classic RL post-training on AfterQuery environments. The +20.9% net win-loss figure refers to a Nemotron 3 *Nano* student — [AfterQuery blog](https://www.afterquery.com/blog/how-afterquery-helped-nvidia-hill-climb-gdpval)
- Good Start Labs: some tasks use "the game engine as the verifiable source of rewards." Duffy calls RL environments "one of the most reliable ways to teach models anything you could verify." The interview does not mention private or pre-release evals — [Latent Space](https://latent.space/p/good-start-labs)
- Duffy (podcast transcript) says the team worked with OpenAI to evaluate GPT-5 "kind of ahead of release" — (search summary; not fetched) [Every podcast transcript](https://api.every.to/podcast/transcript-13dc9405-c841-458d-9923-618a58f4b9f1)
- AI Diplomacy harness for evaluating any LLM on full-press Diplomacy, published at AAAI — [AAAI](https://ojs.aaai.org/index.php/AAAI/article/view/41067)

### Inferences
- Both claims are broadly right but overstated. "Post-trained with AfterQuery tasks" is true in a distillation/pivot sense. "Runs private pre-release evals" rests on one self-reported GPT-5 engagement.

### Gaps
- The NVIDIA Nemotron 3 Ultra technical report was not read to confirm the AfterQuery naming independently.
- No Good Start Labs evals product page was found (gamelab.com/products/evals returned 404 and belongs to Arkadium's GameLab, not Good Start Labs).

## Q3. Deal sizes, per-environment/per-task pricing, and lab spend

### Takeaway
The best-sourced numbers come from Epoch's Jan 2026 interview-based FAQ (18 interviewees) and The Information via TechCrunch:
- **Per task:** $200–$2,000 per task, with ~$20K rare (complex SWE).
- **Per environment:** ~$20K per UI-gym website clone, up to ~$300K for a high-fidelity Slack-class clone.
- **Contracts:** six to seven figures per quarter. One neolab cited $300–500K.
- **Exclusivity:** exclusive deals cost ~4–5x more.
- **Lab spend:** Anthropic leaders reportedly discussed >$1B on RL environments over a year.

### Cited Findings
- Anthropic leaders discussed spending >$1B on RL environments over the next year (The Information, Sept 2025). TechCrunch frames this as discussion, not confirmed spend — [TechCrunch](https://techcrunch.com/2025/09/16/silicon-valley-bets-big-on-environments-to-train-ai-agents/); [Epoch](https://epoch.ai/gradient-updates/state-of-rl-envs)
- Per-task: "multiple interviewees" gave $200–$2,000 per task. ~$20K per task is rare (complex SWE) — [Epoch, Jan 12 2026](https://epoch.ai/gradient-updates/state-of-rl-envs)
- Contracts often run six to seven figures per quarter. A neolab researcher reported $300K–$500K contracts — [Epoch](https://epoch.ai/gradient-updates/state-of-rl-envs)
- UI gyms (website replicas) cost ~$20K each (per SemiAnalysis), and Slack-class replicas ~$300K — [Epoch](https://epoch.ai/gradient-updates/state-of-rl-envs)
- Exclusive deals cost ~4–5x non-exclusive (two founders independently) — [Epoch](https://epoch.ai/gradient-updates/state-of-rl-envs)
- Requests for RL environments outnumber requests for benchmarking environments by ~10–20x (one startup employee) — [Epoch](https://epoch.ai/gradient-updates/state-of-rl-envs)
- Compute spend dwarfs environment spend (OpenAI 2026 R&D compute projected ~$19B) — [Epoch](https://epoch.ai/gradient-updates/state-of-rl-envs)
- Mechanize compute math: 500K tokens × $15/M × group size 64 = $480 per task per run, or ~$2,400 lifetime at 5 reuses. Hence spending <$500/task on data is "cheap tires on a Ferrari" — [Mechanize, Aug 2025](https://www.mechanize.work/blog/cheap-rl-tasks-will-waste-compute/)
- Nathan Lambert reports top labs spending "$10M+ for single environments" — [HF blog, Sept 2026](https://huggingface.co/blog/sergiopaniego/rl-environments-2026)
- Prime Intellect open bounties: ~$100–500 per environment (open access), with larger application-only bounties — [Prime Intellect](https://primeintellect.ai/blog/scaling-environments-program)

### Inferences
- A single-domain game environment sold non-exclusively plausibly prices like a UI gym (~$10K–$50K) or as a task pack at $200–$2,000/task. A 200–500-task pack would be $40K–$1M nominal. This is extrapolation, not a reported price for any game environment.
- Open-hub bounties (~$100–5K) set the floor for publishing openly.

### Gaps
- No reported price for any game-based environment or game task pack.
- No 2026 The Information article with updated lab spend was located.

## Q4. What buyers want, and are game/spatial environments in demand (with transfer evidence)?

### Takeaway
Buyers rank **reward-hacking robustness ("soundness")** first. Next come **difficulty calibration** (non-zero but <~70% pass rates, a "smooth gradient"), **diversity/compositionality**, **verifiability**, and **quality at scale**. Demand is dominated by coding, computer-use app clones and enterprise workflows. Games barely appear in Epoch's demand map. Transfer evidence from games exists but is modest and mostly from vendors or academics: ViGaL arcade→multimodal math (ICLR 2026), Diplomacy→Tau2/AssetOpsBench, and 1830→Finance-Agent (only for one harness design). Math is cited as a category that "doesn't transfer as well."

### Cited Findings
- "Soundness matters most: high reward must mean the task was actually solved, not hacked." "Reward hacking is a big issue." Robust graders take "many many iterations" — [Epoch](https://epoch.ai/gradient-updates/state-of-rl-envs)
- Difficulty: 0% or 100% pass rates give no signal. Suggested minimum ~2–3%, or ≥1 success in 64–128 rollouts. Retire tasks at ~70%. "A very important feature of the RL environment is a smooth gradient: diversity in the difficulty of the tasks" — [Epoch](https://epoch.ai/gradient-updates/state-of-rl-envs)
- "Maintaining quality while scaling is the number one bottleneck." "Domain knowledge and expert level prompting is more important than ML skills for creating tasks" — [Epoch](https://epoch.ai/gradient-updates/state-of-rl-envs)
- Demand areas: coding (moving toward GitHub/Linear/IDE environments), computer-use clones (Excel, Airbnb, Bloomberg), enterprise workflows (expense reports, CRM, ERP), finance, bio, shopping and health. Math may be declining because it "doesn't transfer as well." Games are **not discussed** as a category — [Epoch](https://epoch.ai/gradient-updates/state-of-rl-envs)
- Skeptics: Ross Taylor says "people are underestimating how difficult it is to scale environments." OpenAI's Sherwin Wu is "short" on RL environment startups. Karpathy is "bullish on environments… bearish on reinforcement learning specifically" — [TechCrunch](https://techcrunch.com/2025/09/16/silicon-valley-bets-big-on-environments-to-train-ai-agents/)
- Lab practice in 2026 centers on coding sandboxes and app mocks (Gmail, Notion, Slack). Games and Minecraft are not discussed. The nearest spatial example is Blender-scene environments — [HF blog](https://huggingface.co/blog/sergiopaniego/rl-environments-2026)
- Transfer (game→other):
  - Good Start Labs trained a 30B model on 1830; "only the terminal-agent design improved performance on the Finance-Agent benchmark." Duffy: "every environment we've built also improves tool use downstream" — [Latent Space](https://latent.space/p/good-start-labs)
  - Diplomacy fine-tuning of Qwen3-235B gave >10% on Hanabi/Wordle and gains on Tau2 and AssetOpsBench — (search summary) [Every](https://every.to/playtesting/we-trained-an-ai-on-a-board-game-it-became-a-better-customer-support-agent-299b5938-09dd-4881-803f-aea21f0d461f)
  - ViGaL: RL on Snake/Rotation for Qwen2.5-VL-7B improved MathVista, MathVerse, MMMU and VSI-Bench (3D spatial) with no in-domain math data. RL beat SFT, and difficulty control stabilized training. ICLR 2026 — (search summary) [arXiv 2506.08011](https://arxiv.org/abs/2506.08011)
- Spatial weakness in game evals: in FLE, Claude 3.5 Sonnet completed only 7/24 lab-play tasks and showed "limitations in spatial planning." BALROG found models do worse with visual observations — (search summary) [FLE arXiv 2503.09617](https://arxiv.org/html/2503.09617v1); [BALROG arXiv 2411.13543](https://arxiv.org/abs/2411.13543v2)

### Inferences
- A piston-door environment's strongest selling points line up with what buyers rank highest. A real game engine as grader means high soundness and low reward-hacking surface. Parameterized door sizes give a natural difficulty ladder. Changed-physics variants act as held-out families. Its weakest point is relevance: buyers fund economically valuable domains and want transfer evidence, which Piston Door Bench does not yet have.
- The repair/adaptation framing ("diagnose a broken system from traces, then fix it") maps better onto buyer priorities (debugging, tool use, reading execution traces) than "design a minimal door." Tick-trace feedback is close to how coding agents read logs.
- A buyer would likely want a small transfer study (e.g., RL on repair tasks → gains on a SWE/debugging or spatial benchmark) before paying more than open-hub prices.

### Gaps
- No buyer statement explicitly asking for spatial-reasoning or game environments was found.
- "Held-out families" is not discussed explicitly in Epoch's FAQ.

## Q5. Precedents for game-based environments and whether any were bought

### Takeaway
Game environments (MineDojo/MineRL/Voyager, FLE, BALROG with NetHack/Crafter, TextArena, AI Diplomacy) have spread as **open research benchmarks**. No public evidence shows a frontier lab *buying* one from its academic creators. Commercial game environments exist today as vendor products (Good Start Labs, GameLab/Arkadium, Scale AgentEnv's Minecraft/Catan/Poker/Civ3 plugins). Revenue appears to come from trajectory data and custom environments, not from licensing a published benchmark.

### Cited Findings
- FLE was built by researchers including Anthropic's Akbir Khan as an open-source eval. Lab-play has 24 challenges. No model card using FLE or BALROG was found — (search summary) [The Decoder](https://the-decoder.com/factorio-joins-growing-list-of-video-games-doubling-as-ai-benchmarking-tools/); [FLE](https://arxiv.org/html/2503.09617v1)
- Scale AgentEnv includes a Minecraft/Catan/Poker RL env plugin and an OpenCiv3 plugin, so a top vendor treats Minecraft as one environment among many inside its framework — [Scale Labs, Oct 2026](https://labs.scale.com/blog/introducing-agentenv)
- GameLab (Arkadium) sells exclusive human game-decision data and names Google DeepMind and Meta AI as "Frontier Model Partners" — [GameLab](https://gamelab.com/about)
- Good Start Labs sells game trajectories and environments to frontier labs ($3.6M raised) — [Latent Space](https://latent.space/p/good-start-labs)
- Open Minecraft research platforms (MineRL, MineDojo, Voyager) and BALROG (NetHack, Crafter) are established but research-only. No frontier lab was found publicly sourcing Minecraft environments from an outside vendor — (search summary) [awesome-rl-environments](https://github.com/NafiGit/awesome-rl-environments)

### Inferences
- The precedent is "publish → gain citations/visibility → get hired or partner," not "publish → license." The companies that monetize games did it with services (data, custom environments) and a founder-led eval reputation (AI Diplomacy → Good Start Labs → GPT-5 pre-release work).
- Scale already offers Minecraft inside AgentEnv, so a standalone Minecraft environment competes with a free-to-them plugin unless it offers a distinctive, verifiable task family (engineering/repair under changed physics).

### Gaps
- No disclosed licensing or acquisition of an academic game benchmark by a lab.

## Q6. Concurrent work: RedstoneBench (adamholter) and SciCrafter (arXiv 2604.24697)

### Takeaway
**SciCrafter is real and overlaps closely.** It uses parameterized Minecraft redstone circuits (lamps lit in patterns/timed sequences), on which GPT-5.2, Gemini-3-Pro and Claude-Opus-4.5 plateau at ~26%. It excludes advanced components (comparators, observers) and, by the search summary's account, pistons are not central. **RedstoneBench by adamholter could not be found** on GitHub or the web. MineCEraft (arXiv 2608.28884) is another adjacent Minecraft construction benchmark.

### Cited Findings
- SciCrafter: "Can Current Agents Close the Discovery-to-Application Gap? A Case Study in Minecraft." Zhou Ziheng, …, Yitao Liang, Ying Nian Wu, Demetri Terzopoulos, Xiaofeng Gao. Submitted Apr 27 2026, v2 May 20 2026. Parameterized redstone-circuit tasks (light lamps simultaneously/in timed sequences). Scaling parameters forces discovery over memorization. Frontier models plateau at ~26% under a code-agent scaffold. Knowledge application is the biggest gap, and knowledge-gap identification is becoming a hurdle for frontier models. Framed as a "diagnostic probe"/benchmark, not an RL environment — [arXiv 2604.24697](https://arxiv.org/abs/2604.24697)
- SciCrafter uses buttons, redstone wire, repeaters, torches and lamps, excludes comparators and observers, and wraps the agent interface in MCP — (search summary of PDF) [arXiv PDF](https://arxiv.org/pdf/2604.24697)
- github.com/adamholter lists 101 repos. The popular ones visible include hive-mind-landing-page, aa-plus, clutterbench, etc. No RedstoneBench was visible. Web search for "RedstoneBench" returned nothing — [GitHub adamholter](https://github.com/adamholter)
- MineCEraft: 723 expert-written instructions across 17 categories, programmatically verifiable construction-engineering tasks in Minecraft — (search summary; not fetched) [arXiv 2608.28884](https://arxiv.org/pdf/2608.28884)

### Inferences
- SciCrafter takes the "redstone + frontier agents + discovery" framing first. Piston Door Bench should set itself apart through **pistons/doors (mechanical spatial engineering), minimality optimization, changed-physics adaptation, and tick-trace-driven repair**, and should cite SciCrafter. The changed-physics variant is the clearest novelty against SciCrafter's memorization-avoidance-by-scaling.
- Positioning synthesis from these notes:
  1. **Published research eval:** the most defensible first step. The niche is uncrowded but no longer empty, publication sets priority against SciCrafter/RedstoneBench, and open precedent (FLE, BALROG, AI Diplomacy) shows evals lead to reputation and services.
  2. **Sellable eval:** weak. Labs request RL environments ~10–20x more than benchmarks, and no market for licensed game evals is visible.
  3. **Sellable RL environment:** possible, but only as the repair/adaptation variant with hundreds of parameterized, engine-verified tasks, calibrated pass rates, held-out physics families and a transfer result. Likely channels are Good Start Labs/GameLab-style vendors, Scale/Mercor subcontracting, or Prime Intellect Environments Hub (open, bounty-scale money, Tinker-compatible).

### Gaps
- RedstoneBench's existence, scope and author could not be verified. The user should share the link.
- The full SciCrafter PDF was not read to confirm whether pistons appear at all.
