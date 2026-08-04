---
name: ai-work-hub-diligence
description: Use for live diligence or historical review of invested, passed, or previously screened startups when the user provides a BP, teaser, datapack, model, Feishu/Lark document or minutes link, transcript, interview note, public source, or other project material. Maintains one evolving investment judgment, focused evidence and todo, Memory Graph retrieval and reusable writeback, public and technical-team checks, practical valuation calibration, follow-up reactivation, and confirmed pass archiving. Local project storage is the default; organization deployment and portable Context Packages are optional advanced modes.
---

# AI Work Hub Diligence

## Core Contract

Treat this as a workflow, not a one-time judgment. A single BP, Feishu link, transcript, datapack, or project file should be enough to trigger the workflow: create or locate the project folder, archive the source, read the material, update the running judgment, and return a decision-oriented answer.

Keep one running project judgment/todo document per active project. Update that document as new materials arrive. Do not create a new judgment document for every round unless the user explicitly asks for a separate memo. Create new files for question lists, interview prep, regenerated minutes, and external-facing deliverables.

Also keep one machine-readable project state and one append-only evidence ledger.
Read `references/evidence-contract.md` before creating or updating them. The
running judgment is the human decision document; the state JSON is the current
machine-readable decision; the evidence ledger preserves only claims that
materially affect the judgment, are likely to be disputed, or will matter in a
later review. Do not turn routine source reading into exhaustive claim logging.

Use local project storage by default when a workspace root is available. Reading
a Feishu/Lark link is source intake, not a reason to switch the project to
Feishu storage. Only activate organization storage, hybrid synchronization, or
portable Context Packages when the user explicitly asks for cross-runtime
handoff, canonical Feishu writeback, a shared Context Registry, migration, or a
bridge. Then read `references/advanced-deployment.md`.

When a local AI Work Hub Memory Graph exists, use it as the cross-project knowledge layer: consult it before judging the project and update it after the view changes. The Memory Graph is a local private knowledge base and must not be committed to the public diligence skill repo.

If the user explicitly says not to generate files, run the workflow in chat only and do not create or modify artifacts.

## Historical Project Review

Trigger this mode when the user uploads prior deal materials for an already
invested, passed, or previously screened project. Historical review uses the
same folder, evidence ledger, structured state, Memory Graph card, and generated
indexes as live diligence. It is not a separate archive that cannot re-enter
the pipeline.

Initialize with:

```bash
python3 <skill_dir>/scripts/init_historical_review.py \
  --workspace-root "<workspace_root>" \
  --project-name "<项目名>" \
  --outcome invested|pass|unknown \
  --decision-date "YYYY-MM-DD"
```

Use `--reopen` when a historical pass is now being reconsidered. Preserve
`historical_outcome=pass`; update only the current project status, process stage,
investment decision, play, sizing, price, and confidence.

Historical review must keep two evidence timelines:

1. `decision_time`: facts and claims available when the original investment or
   pass decision was made.
2. `post_outcome` or `current`: later operating results and new follow-up
   evidence.

The review document should cover:

- 当时的信息集
- 当时的投资判断与关键假设
- 事后结果
- 决策质量与结果质量（分开评价）
- 当前重评
- 可复用经验、反例和后续触发器

Do not use hindsight to relabel weak original evidence as verified. Already
invested projects normally enter monitoring. Historical pass projects normally
live under `项目/归档/`, remain searchable as counterexamples, and may be
reactivated without losing their original outcome.

## First Run Setup

Before creating objects or writing artifacts in a new environment, confirm the
user's workspace root. If a current workspace root is obvious, use it and ask
for confirmation only when there is ambiguity.

Suggested default layout:

```text
<workspace_root>/
  项目/
    <项目名>/
    归档/
```

Do not hardcode a personal path. Ask: `你的项目工作区根目录放在哪里？例如 ~/Documents/AI Work Hub。`

If Feishu/Lark links are part of the workflow and the CLI is not yet set up, read `references/feishu-cli.md` and guide the user through installation, login, scope checks, and permission fixes.

## Project Object Contract

### Local Profile

When new project material arrives in local mode:

1. Infer the project name from the BP, file name, Feishu title, company name, or user wording.
2. If the name is ambiguous, ask one short clarification before creating artifacts.
3. Create or locate:

```text
<workspace_root>/项目/<项目名>/
  原始资料/
  解析文本/
    证据账本.jsonl
  输出文档/
    <项目名>_项目状态.json
```

4. Also ensure the archive container exists:

```text
<workspace_root>/项目/归档/
```

5. Save original files or fetched Feishu exports into `原始资料/`.
6. Save extracted text, OCR, Feishu smart minutes, original transcript, and public-source notes into `解析文本/`.
7. Save the running judgment file and generated deliverables into `输出文档/`.

Use one running judgment file, preferably:

```text
<workspace_root>/项目/<项目名>/输出文档/<项目名>_项目判断与todo.md
```

For a new project, initialize structured files with:

```bash
python3 <skill_dir>/scripts/init_project_state.py \
  --workspace-root "<workspace_root>" \
  --project-name "<项目名>"
```

Recommended sections:

- 当前一句话判断
- 项目核心逻辑
- Memory Graph 联想
- 已验证信息
- 公开交叉验证
- 团队技术背景与可信度
- 主要疑点 / 风险
- 交流纪要 takeaways
- 当前核心 todo
- 判断变化记录

Create separate files for each question list, for example:

```text
<date>_初步问题清单.md
<date>_创始人访谈问题清单.md
<date>_客户访谈问题清单.md
<date>_供应商访谈问题清单.md
```

Do not overwrite prior question lists.

## Codex Thread Title

When the project name is clear and tooling exists, title the conversation
`Project 项目名` using the most recognizable working name. Do not guess or put
judgment, valuation, customers, or financing terms in the title.

## Feishu Link Intake

Use `references/feishu-cli.md`. Fetch with user identity when possible; read
smart minutes and the original transcript/content, follow relevant nested
links, and preserve both under `解析文本/`. State any access gap. Save long
material before analysis to avoid truncation.

## Source Intake

For initial BP or preliminary materials:

1. Read the exact source material before using public information.
2. Identify what is company-stated, what is evidenced by data, and what is still an assumption.
3. Record only judgment-changing, reusable, disputed, or high-stakes claims in `解析文本/证据账本.jsonl`, with evidence tier, verification status, decision impact, source path, and locator. Never promote a POC, logo, smart-minutes summary, or company metric beyond its actual source tier. For historical reviews, also set `temporal_scope=decision_time`, `post_outcome`, or `current`.
4. If `Memory Graph/` exists under the workspace root, build a bounded context pack and inspect its source cards before final judgment.
5. When company, founder, product, customer, or technology names are identifiable, perform a lightweight public-information cross-check before final judgment.
6. When a founder, chief scientist, CTO, algorithm lead, research lead, or other core technical person is identifiable, research that person's public technical background and update `团队技术背景与可信度` in the running judgment document.
7. Produce an initial judgment plus a short preliminary question list.
8. Update the project state JSON after the readable judgment is final.
9. Sync the Memory Graph project card. Update sector views, technical themes, valuation references, people cards, or major-event cards only when the round adds reusable knowledge beyond this project.
10. When valuation is decision-useful, capture the company's or source's stated valuation, financing amount, date, round/stage, source, and a short comparability note. Do not seek agreements, payment proof, or closing details by default.

For later datapacks, models, or updates:

1. Inspect the relevant sheets, tables, transcripts, or appended materials.
2. Extract only metrics that affect the investment judgment, such as revenue, users, customers, retention, gross margin, compute cost, backlog, pipeline, team, cap table, and scenario assumptions.
3. Recalculate the view when new data contradicts the prior view.
4. Refresh Memory Graph linkage when the new material changes comparable projects, sector or technical understanding, a useful valuation reference, a high-signal person, or a durable thesis.
5. Update the same running judgment/todo document.
6. If writing artifacts, update the Memory Graph project card and write only the reusable increment to higher-level graph files.
7. If the user explicitly requests organization deployment or cross-runtime handoff, follow `references/advanced-deployment.md`.

## Memory Graph Linkage

Use the `ai-work-hub-memory-graph` workflow when that skill is installed or when a local `Memory Graph/` exists.

Before finalizing a project view, add a concise `Memory Graph 联想` section:

```text
Memory Graph 联想
- 相似项目:
- 反例项目:
- 相关赛道/技术观点:
- 估值锚点:
- 这个项目必须证明的差异点:
```

Keep the section short. It should help the user remember prior work, not become a second memo.

Use the taxonomy already present in the local Memory Graph. If no custom taxonomy exists, use the companion Memory Graph skill's default sectors as a starting point, but treat them as editable defaults rather than mandatory labels.

Do not preserve very low-quality projects as first-class project cards unless they teach a reusable pattern.

## Public Cross-Check

Use public information as validation and calibration, not as a substitute for source reading. Look for:

- Company basics: official site, registry/profile pages, financing history, product pages,备案/domain state, hiring pages, and historical positioning.
- Founder/team: school and employer history, public bios, LinkedIn/Google Scholar/Semantic Scholar/DBLP/personal pages, GitHub/Hugging Face, patents, papers, conference talks, prior startups, and open-source contributions.
- Technology proof: papers, arXiv, model cards, Hugging Face/GitHub repos, benchmarks, demos, patents, and reproducible evaluation details.
- Commercial proof: customer announcements, case studies, procurement/tender records, customer press releases, app/store traffic, and evidence that logos represent real usage or paid contracts.
- Industry calibration: comparable companies/products, mainstream technical route, customer purchasing behavior, pricing or cost benchmarks, and whether claimed growth or margin is plausible.

When public evidence is thin, stale, inconsistent, or only company-stated, say so explicitly. Treat strong private claims such as `全球前三`, huge orders, top customer logos, famous-school/lab affiliations, or breakthrough model performance as verification items.

## Technical Team Background

For AI or deep-tech projects, treat identifiable technical leaders as a diligence input. Do this on the first interaction where the person is known, not only when the user explicitly asks.

Trigger when materials mention a founder, co-founder, chief scientist, CTO, VP/R&D, algorithm lead, research lead, professor, lab PI, principal engineer, or similar core technical role. In later rounds, repeat the check when new core technical people are named.

For each relevant person:

1. Resolve identity carefully, especially for common Chinese names, English names, aliases, school profiles, and current/prior employer pages.
2. Check public technical footprint: papers, patents, Google Scholar/Semantic Scholar/DBLP, arXiv, conference pages, GitHub, Hugging Face, Papers with Code, personal site, talks, prior startups, and major open-source or product contributions.
3. Assess relevance to the company's claimed technical route, not just prestige. Note whether the work maps to the product, model, data pipeline, hardware stack, robotics/embodied AI, inference system, or other claimed moat.
4. Distinguish evidence strength:
   - `已核验`: public source supports the fact.
   - `公司自述`: appears only in BP, teaser, minutes, or company materials.
   - `仍需确认`: name ambiguity, unclear employment boundary, paper authorship ambiguity, weak link to product, or unclear full-time commitment.
5. Look for red flags: decorative advisor risk, thin publication record relative to claims, stale or unrelated papers, no code footprint for code-heavy claims, employer/IP/non-compete overlap, exaggerated school/lab affiliation, or unclear role in prior work.

Write findings into the same running judgment document under `团队技术背景与可信度`; do not create a separate background report unless the user asks. Keep it short:

```text
团队技术背景与可信度
- 人员A: 已核验的教育/工作/论文/代码信号；与项目技术路线的相关性；仍需确认事项。
- 人员B: ...
- 对投资判断的影响: 上修 / 中性 / 下修，以及原因。
```

If web access or public sources are unavailable, state that the check was not completed and add it to current todo.

## Decision Standard

Default to an investment time-allocation lens. Lead with one of:

- `投`
- `继续推进`
- `暂缓`
- `不投`

If the evidence points to weak founder-market fit, weak fit with the user's investment theme, poor valuation discipline, or a story that relies more on financing narrative than verified traction, say `不投` or `move on` directly.

For AI investment work, first test whether the company is truly AI-native and relevant to mainstream AI investor logic.

Real AI thesis fit:

- AI-native team
- proprietary product or technical insight
- strong workflow or data loop
- self-driven customer pull
- low-friction repeatability
- measurable AI ROI

Adjacent or narrative fit:

- traditional software, SI, channel, government-resource, or industrial digitization company using AI/Agent language without clear AI-native product advantage

If a project is only an adjacent or narrative fit for an explicitly AI-focused investor, default to `不投 / move on` unless there is unusually strong verified commercial traction at an attractive valuation.

Use `继续推进` when evidence is directionally attractive and the next diligence step can realistically confirm a live investment decision. Use `暂缓` only when a key blocker should stop normal deal-process time until resolved.

When discussing deal participation, keep the conclusion to two layers:

- **Investment judgment**: `投`, `继续推进`, `暂缓`, or `不投`.
- **Recommended play**: combine role and sizing in one natural phrase.

Use practical mappings:

- `领投` / `共同领投`: only when conviction supports a main position; usually standard to heavy position.
- `跟投`: can be standard or small position, depending on conviction, allocation, and round access.
- `小额 option`: small or symbolic check only; use when the project is worth tracking but not ready for a main position.
- `暂缓`: do not force role or sizing; state the missing signals that must be filled before resuming.

Examples:

- `投；建议领投或共同领投，标准仓位。`
- `继续推进；建议跟投，小仓位。下一步重点验证客户回款和产品节点。`
- `继续推进；仅保留小额 option，不做主仓位。`
- `暂缓；先补客户回款、合同和产品复测信号。`

## Valuation Calibration

Run valuation calibration when the material mentions financing amount, pre-money/post-money valuation, target ownership, entry price, revenue multiple, ARR, profit, order book, or when the user asks whether the price is attractive. Also run it when a project moves from initial screen to `继续推进` and enough operating data exists.

Keep valuation light in early screens. Expand only when price is material to the decision or the user asks for it.

Use three anchors:

- **Public listed comps**: use relevant US, A-share, and Hong Kong listed companies when they match the real business model. Compare by revenue quality, growth, margin, retention, delivery model, cyclicality, and capital intensity, not by AI label alone.
- **Private-market comps**: use recent same-sector or adjacent financing rounds when available, but treat them as noisy sanity checks unless source quality is strong.
- **Company-specific reverse check**: calculate what the proposed valuation implies on current year and next year revenue/ARR/gross profit/profit/order backlog, and what operating milestones are required to justify the next round.

For normal BP, interview, and datapack work, capture the valuation with a light
default record:

- project, date, round or operating stage;
- stated pre-money or post-money valuation when known;
- financing amount and currency when known;
- source context such as company material, interview, FA material, public source, or transaction document;
- a short comparability note tied to business model and operating maturity.

Do not seek agreements, payment proof,工商 changes, or exact closing status by
default. Deepen transaction verification only when it changes ownership,
portfolio marking, return math, closing risk, legal rights, or the investment
decision; when sources materially conflict; or when the user explicitly asks
for transaction or Cap Table review.

Always keep the observed or company-stated market price separate from the
internal fair-value view. A price can be a useful reference without being fair,
fully verified, or suitable for the current project.

For public-market multiples or recent private comps, use current sources when web access is available; valuation data is time-sensitive. If current data cannot be verified, state that the valuation calibration is directional.

Avoid weak comps. Do not benchmark a project to OpenAI, Anthropic, Palantir, Nvidia, or a hot listed AI name unless the revenue model, defensibility, growth profile, and margin structure are genuinely comparable. If the company is project delivery, SI-like, hardware-heavy, government-resource driven, or channel-dependent, choose comps that reflect that reality.

Recommended output when valuation matters:

- 公司本轮估值 / 融资结构
- 核心经营指标
- 可比上市公司
- 可比一级市场标的
- 隐含倍数与反推
- 合理估值区间
- 当前价格判断: 便宜 / 合理 / 偏贵 / 明显过贵
- 投资判断: 投 / 继续推进 / 暂缓 / 不投
- 建议打法: 领投或共同领投，标准仓位 / 跟投，小仓位 / 小额 option / 仅观察

## Workflow

### 1. Initial BP Review

When the user first sends a BP, teaser, deck, or early materials:

1. Create or locate the local project folder unless the user says no files.
2. Archive the source material under `原始资料/`.
3. Extract/read the source deeply enough to support a view.
4. Run a lightweight public cross-check.
5. If technical founders or core technical people are identifiable, research their public technical background and update `团队技术背景与可信度`.
6. Update the running judgment document under `输出文档/` if writing artifacts.
7. Return:
   - 初步判断: lead with `投`, `继续推进`, `暂缓`, or `不投`.
   - Memory Graph 联想: include similar projects, counterexamples, sector/technical views, and valuation anchors when available.
   - 公开交叉验证: summarize the most important public signals and mismatches.
   - 团队技术背景与可信度: include when technical founders or core technical people are identifiable.
   - 估值校准: include only when financing terms, valuation, or enough operating metrics are available.
   - 初步问题清单: around 6-10 core questions only.
   - 下一步建议: a small number of actions, including sizing or structure only after the investment judgment is clear.

### 2. Follow-Up Material Updates

When the user later provides a datapack, Feishu note, transcript, customer call, founder update, or other project material:

1. Save/fetch the new source.
2. Read the new material from source.
3. Record the core takeaways from this round.
4. Refresh the public cross-check when the new material introduces new companies, founders, customers, technical claims, patents, papers, benchmarks, financing claims, or commercial claims.
5. Refresh `团队技术背景与可信度` when the new material introduces new founders, chief scientists, CTOs, algorithm leads, research leads, or other core technical people.
6. Refresh valuation calibration when the new material changes revenue, ARR, profit, order backlog, growth certainty, valuation, round terms, or suggested investment size. Capture the stated market context without escalating to transaction verification unless a deep-verification trigger applies.
7. Refresh Memory Graph project cards and cross-project linkage when the new material changes reusable knowledge.
8. Append only judgment-changing, disputed, reusable, or high-stakes claims to the evidence ledger; supersede prior high-impact claims explicitly rather than silently rewriting history.
9. Update the same running project judgment/todo document and project state JSON.
10. Explicitly state what changed versus the prior view.
11. Keep current todo to 3-5 core items.
12. Sync the project card, apply any clear reusable Memory Graph changes to their existing destination, rebuild indexes, and validate.
13. Use advanced deployment only when explicitly triggered.

### 3. Interview Question Lists

When the user asks for founder, core team, customer, supplier, FA, counsel, or other counterparty questions:

1. Tailor the list to that interviewee.
2. Focus on unresolved gating issues.
3. Create a separate question-list file if writing artifacts.
4. Keep company-facing wording polite and preparation-oriented.

For external-facing versions, avoid internal challenge language such as `红灯`, `必须拿到`, or overtly accusatory phrasing. Prefer `请协助说明`, `希望进一步了解`, and `可否补充`.

### 4. Meeting Note Regeneration

When the user asks to regenerate minutes from Feishu original content:

1. Fetch and save the original transcript/content, not only the smart minutes.
2. Preserve the original question-and-answer structure as much as possible.
3. Clean up order, speaker logic, and wording for readability.
4. Summarize moderately, but do not abstract away important factual detail.
5. Separate `问题`, `答复`, and `补充判断 / 待确认` when helpful.
6. Keep the output traceable to the original conversation.

### 5. Pass And Archive

If the recommendation is `不投` or `move on`, do not archive automatically. Wait for the user to agree that the project is passed or ask to archive it.

When the user agrees to pass:

1. Move the project folder from:

```text
<workspace_root>/项目/<项目名>/
```

to:

```text
<workspace_root>/项目/归档/<项目名>/
```

2. If the archive target already exists, ask before merging or create a dated folder such as `<项目名>_archived_<date>`.
3. Leave active projects directly under `<workspace_root>/项目/`.
4. In the final response, state the archive path.

## Advanced Deployment

Ordinary local diligence and Feishu-link reading do not require a storage
profile decision or Context Package. Read `references/advanced-deployment.md`
only when the user asks to:

- make Feishu/Lark the canonical project store;
- synchronize local and organization copies;
- hand the project to another runtime or Agent;
- connect a Codex-Feishu bridge or organization Context Registry;
- migrate a project collection or Memory Graph; or
- produce a formal portable writeback package.

Keep organization IDs, permissions, locators, adapters, and Context Package
validation out of the normal project path.

## Output Style

For internal diligence:

- Be concrete about `投不投`, `为什么`, `还差什么`, and whether the next action is `继续推进`.
- Be willing to say `不投` as the headline when that is the real judgment.
- Give a valuation range, comfortable entry point, and suggested sizing or structure when material.
- Separate `BP自述`, `公开可验证`, `公开未找到`, and `仍需底稿/访谈确认` when the distinction affects the judgment.
- Separate `好项目且值得推进`, `好项目但价格贵`, `方向好但项目不行`, `项目可赚钱但不适合本基金`, and `完全不该花时间`.

For question lists:

- Keep initial lists short.
- Split by theme only when it improves usability.
- Write questions that can be used directly in the next conversation.

For updates:

- Lead with new takeaways.
- Then state how the view changed.
- End with only the core todo.

## Quality Checks

Before finishing, check:

1. The answer is grounded in the actual BP, datapack, Feishu content, or transcript.
2. Feishu-linked work used the original content as well as smart minutes when available, and relevant nested links were followed or reported inaccessible.
3. The current judgment is explicit, distinguishes what changed, and keeps todo and initial questions short.
4. One running judgment/todo document and one consistent project state are maintained.
5. Public and technical-team checks focus on claims that can change the judgment.
6. The evidence ledger contains the important provenance without exhaustively restating the source.
7. Valuation-sensitive work separates the stated market price from the internal price view and uses deep transaction verification only when material.
8. The Memory Graph project card is current; higher-level graph files contain only reusable increments, and generated indexes were rebuilt rather than hand-edited.
9. Passed projects are archived only after user confirmation; historical reviews preserve decision-time versus later evidence.
10. Advanced deployment is activated only by an explicit cross-runtime or organization-storage request and follows `references/advanced-deployment.md`.
