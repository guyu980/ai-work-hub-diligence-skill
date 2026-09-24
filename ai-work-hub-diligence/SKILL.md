---
name: ai-work-hub-diligence
description: Continuous investment diligence for a single company using BPs, datapacks, Feishu originals and project updates. Maintain one evolving judgment and focused next actions, prepare dated questions or minutes, and connect relevant prior knowledge. Route non-project expert interviews and thematic sources to ai-work-hub-memory-graph.
---

# AI Work Hub Diligence

## Operating Contract

This is a continuous investment workflow, not a one-off summary.

Hard requirements:

- One project has one running judgment/todo document. Update it in place.
- New question lists, interview guides, and regenerated minutes are separate dated files.
- Read the supplied material before public research. For Feishu minutes, read the original transcript/content as well as smart minutes.
- Distinguish verified facts, company/source claims, and unresolved items.
- Lead with an investment view and the evidence that could change it.
- Keep todo short and decision-relevant.
- Use local project storage when a workspace exists. Feishu is an intake source unless the user explicitly requests organization storage.
- Consult and update the private Memory Graph when it exists, but do not copy private graph content into this public skill repository.
- Confirm that the input is owned by one company before initializing a project. Route reusable cross-project expert interviews and thematic materials through the Memory Graph knowledge-source workflow instead.
- During new-project initialization, rename the Codex task once to exactly `Project <项目名>` as soon as the project identity is clear.
- If the user asks for chat-only work, do not create or modify files.

Before writing structured state, read `references/project-state.md`.

## Decision-First Depth

Spend effort on the variables that can change the user's current decision. A first screen needs a clear business/technical thesis, its strongest counterargument, price context when relevant, and the next useful question, not a complete transaction audit.

- Use BP, interview and datapack figures as attributed company inputs. Accurate attribution does not require independent verification of every figure. Lack of independent confirmation alone is not an adverse finding or a mandatory todo.
- Deepen a check when a material contradiction, implausible claim or unresolved decision variable could change the action. Specify what the answer changes; prefer existing evidence or a focused question before requesting extensive records.
- Do not default to contracts, payment trails, full customer lists, legal/IP audits, benchmark reproduction or site testing. These may be appropriate for a specific material issue or an explicitly requested later-stage workstream.
- Distinguish analyst-proposed price/operating thresholds from observed evidence. Explain their basis; use ranges or qualitative milestones when precision is unsupported.
- Keep internal analysis as deep as needed, but expose only the decisive reasoning. Risks need not all become tasks; defer low-value work, especially for paused or passed projects. No useful next action is a valid outcome.
- On a material update, reconsider the central thesis and strongest opposing explanation before editing the prior conclusion. On a minor update, revise only the affected content. Do not repeat background searches or every workflow check on every turn.

Public skills stay model-agnostic. Use stronger reasoning or independent research in parallel only where the question benefits; the owning agent integrates the conclusion and writes shared project/graph files.

## Route The Request

| Input or request | Required action |
| --- | --- |
| First BP or project material | Initialize project, archive source, make an initial judgment, create a short preliminary question list |
| Non-project expert interview or thematic material | Do not initialize a project; route to `ai-work-hub-memory-graph` and `知识来源/` |
| Follow-up datapack or note | Compare with prior state, update the same judgment/todo, record only material deltas |
| Feishu/Lark link | Follow `references/feishu-cli.md`; save smart minutes and original content, including relevant nested links |
| Founder, customer, supplier, or expert interview prep | Create a new focused, dated question file |
| Regenerate minutes | Reconstruct questions and answers from the original transcript; summarize only where useful |
| Historical invested or passed project | Follow `references/historical-review.md`; separate decision-time evidence from later outcomes |
| Existing investment, fund vehicle, deal terms or portfolio update | Keep the current business judgment as the baseline; do the requested operating/transaction work without restarting BP screening. Detailed budgets, holdings and clauses stay in project/fund papers |
| Confirmed pass | Record reopen gates, move the project under `项目/归档/`, and keep it searchable |

## Resolve The Workspace And Project

Confirm the workspace root on first use when it is not already clear. Never hardcode a personal path in the public workflow.

Before resolving a project name, check ownership. A source is project material when its main purpose is to evaluate or update one named company, including a customer, supplier, founder, team, or expert call conducted for that company. A cross-project expert interview, course, podcast, meeting, or thematic document with reusable value belongs in `知识来源/` through `ai-work-hub-memory-graph`. A formal systematic thematic report belongs in `行业研究/` through `ai-work-hub-deep-research`. Do not create a project folder or rename the task for either non-project case.

Default local object:

```text
<workspace_root>/
  项目/
    <项目名>/
      原始资料/
      解析文本/
      输出文档/
        <项目名>_项目判断与todo.md
        <项目名>_项目状态.json
        01_问题清单/        # 按需创建
        02_交流纪要/        # 按需创建
        03_研究与分析/      # 按需创建
        04_正式交付/        # 按需创建
      工作区/               # 按需创建；可重建的过程文件
    归档/
```

Infer the project name from the company, BP title, Feishu title, filename, or
user wording. Ask one short question only if creating the wrong project is a
real risk.

Treat task naming as a one-time initialization action, not a per-round check.
When the first material creates a new project, resolve the name and title the
Codex task before broader source reading, research, or folder creation:

1. Use exactly `Project <项目名>`, with no brackets, date, stage, or action suffix.
   Prefer the clearest Chinese name, English name, or familiar abbreviation.
2. First use `set_thread_title` or equivalent dedicated task-title tooling.
3. If the dedicated tool is absent or cannot perform the rename, use the
   [official Codex App Server](https://learn.chatgpt.com/docs/app-server):
   `thread/name/set` with `{"threadId":"<current_thread_id>","name":"Project <项目名>"}`.
   Get the current thread ID from trusted runtime/session context, not a title
   match or a guess. Use the current user's session store; a local fallback is
   `codex app-server` over stdio with the same `CODEX_HOME`. On a new connection,
   send `initialize` with `clientInfo` (`name` and `version`), wait for its
   response, then send the `initialized` notification before thread requests.
4. After either route, read back the title through a dedicated read tool or
   `thread/read` with `{"threadId":"<current_thread_id>","includeTurns":false}`.
   Confirm `thread.name` exactly matches the requested title; a write response
   alone is not confirmation. Renaming a persisted thread does not require
   `thread/resume`, a new turn, or direct edits to Codex database/session files.

Report naming as unavailable only after checking both the dedicated tool and
official App Server routes; missing UI controls or a missing title tool alone
is not enough. Respect permission boundaries. If neither route is usable,
state the specific limitation and continue diligence. If the write succeeded
but readback is unavailable or mismatched, report the title as unconfirmed,
not successfully renamed.

Record no separate title state and do not inspect or recheck the title on
later datapacks, meetings, or judgment updates. Rename again only if the user
corrects the canonical project name.

Do not apply this convention to cross-project batches, industry research,
recurring reports, or skill/system maintenance.

Initialize structured files when needed:

```bash
python3 <skill_dir>/scripts/init_project_state.py \
  --workspace-root "<workspace_root>" \
  --project-name "<项目名>" \
  --sector "<用户定义或默认主赛道>"
```

The initializer creates the three durable folders, one stable running judgment,
and one project state. Output subfolders and `工作区/` are created only when
needed. It refuses to create a parallel judgment when a legacy non-canonical
running file already exists; rename or merge that file first.

For a mixed workspace, optional workspace settings live in
`<workspace_root>/.ai-work-hub.json`:

```json
{
  "schema_version": 1,
  "exclude_project_dirs": ["funds", "system-design"],
  "require_project_cards": false
}
```

Use exclusions only for genuine non-company objects. Do not use them to hide an
unfinished project migration.

Store originals or fetched exports in `原始资料/`; durable OCR, parsed text,
transcripts, and public checks in `解析文本/`. Keep only the stable judgment and
state directly under `输出文档/`; classify other durable outputs by purpose:

- `01_问题清单/`: preliminary questions, interview guides, follow-up questions,
  and company-facing information requests;
- `02_交流纪要/`: cleaned meeting minutes and reconstructed Q&A; raw or smart
  minutes remain in `解析文本/`;
- `03_研究与分析/`: deep research, valuation, financial models, cross-checks,
  transaction reviews, and other substantive analysis;
- `04_正式交付/`: IC memos, investment reports, decks, formal committee minutes,
  and final external deliverables.

Classify by purpose, not file extension. Do not create a separate `情况更新`
folder: new facts update the stable judgment. If a detailed update must remain
as a standalone workpaper, place it in `02_交流纪要/` or `03_研究与分析/`
according to its main content.

Put reproducible OCR pages, render caches, slide-build directories, temporary
scripts, and other non-deliverable artifacts in project-level `工作区/`. Durable
source extracts stay in `解析文本/`; final outputs stay in `输出文档/`. Agents
should ignore `工作区/` unless a requested deliverable must be regenerated.

For a legacy workspace, preview the complete move plan before applying it. The
migrator preserves file contents, rewrites local text links and paths, and
reports Office files that may still embed old local paths:

```bash
python3 <skill_dir>/scripts/migrate_project_layout.py \
  --workspace-root "<workspace_root>" --all-projects
python3 <skill_dir>/scripts/migrate_project_layout.py \
  --workspace-root "<workspace_root>" --all-projects --apply
```

## Run The Core Loop

For every substantive project input:

1. Locate the project and read the current judgment, state, latest relevant sources, and any linked `知识来源/` core notes surfaced by Memory Graph retrieval.
2. Archive or fetch the new source. Read tables, appendices, original transcript, and relevant nested links when available.
3. Identify what is genuinely new, what confirms the prior view, and what contradicts it.
4. Resolve the few decision-relevant uncertainties. Run public, team, valuation or transaction work only to the depth justified by this stage and question.
5. Update the same running judgment and core todo. Add a short dated change log.
6. Update the project state after the human-readable judgment is final. Keep the few decision-relevant facts and source boundaries in the running judgment.
7. Use the relevant Memory Graph context before final judgment. If durable knowledge changed, update the card's substance as well as its state fields, then rebuild and validate once after the batch.
8. Reply with the current decision, why, what changed, and the few next actions that matter.

Do not turn the workflow into source-by-source narration or exhaustive claim extraction.

## Source Discipline

Use these source labels in readable outputs:

- `已核验`: supported by original documents, customer confirmation, or reliable public evidence.
- `公司/来源自述`: stated in a BP, datapack, minutes, founder/FA message, or unverified model.
- `待核验`: ambiguous, missing, stale, inconsistent, or dependent on follow-up.

Smart minutes are navigation, not final evidence. Keep company claims and forecasts attributed, without treating attribution as a request to verify everything. A faithful transcript proves what was said, not the underlying operating result. Use source labels where they matter; avoid repetitive disclaimers for every sentence.

For public and technical-team checks, read `references/technical-team.md`. Research identifiable technical leaders when their background can change confidence in the claimed technology; keep the assessment inside the running judgment.

## Judgment And Output

The running judgment should normally contain:

```text
当前一句话判断
项目核心逻辑
Memory Graph 联想
关键事实与经营情况（期间、实际/预测、来源就地标明）
团队技术背景与可信度
估值与融资
主要风险与待核验
交流纪要 takeaways
当前核心 todo
判断变化记录
```

The exact sections may follow the existing project file. Do not create parallel versions merely to match this outline.

Keep the business thesis distinct from the latest task. A fund-budget or legal-clause update must not replace company positioning in the project summary. Selected metrics use comparable periods, units and actual/forecast labels; do not duplicate a topic under separate source-tier narratives or build a claim-by-claim ledger.

Lead with one of:

- `投`: evidence and price support an active investment decision.
- `继续推进`: worth spending diligence time; key proof is still missing.
- `暂缓`: do not advance until named signals arrive.
- `不投`: current evidence, price, fit, or priority does not justify further work.

Then express participation separately:

- `领投`: normally implies a standard or concentrated position and enough conviction to shape the round.
- `跟投`: may imply a standard or small position depending on evidence, price, and access.
- `小额 option`: a small position used only when upside is meaningful and explicit proof gates remain; it is not a synonym for `跟投` or `分阶段投资`.
- `不参与`: no current capital deployment.

Do not add unnecessary dimensions such as investment purpose or funding cadence. Participation, position size, and price view should clarify the recommendation rather than repeat it.

## Valuation

Read `references/valuation.md` when price is decision-relevant.

Default capture is light: date, round/stage, stated valuation, financing amount, source, operating maturity, and comparability note. Separate company/market price from the internal reasonable price.

Use the most informative listed or private comps, not an exhaustive survey of all markets. Explain business-model and maturity differences and what drives the plausible price range. Transaction documents are needed only where a specific uncertainty affects ownership math, marking, returns or closing/legal risk, or for an explicit transaction review.

## Follow-Up Deliverables

Question lists prioritize questions that could change the next action. Do not convert all risks into document requests; use stage-appropriate questions in professional language. Save each round separately, for example:

```text
输出文档/01_问题清单/YYYY-MM-DD_初步问题清单.md
输出文档/01_问题清单/YYYY-MM-DD_创始人访谈问题清单.md
输出文档/01_问题清单/YYYY-MM-DD_客户访谈问题清单.md
输出文档/01_问题清单/YYYY-MM-DD_供应商访谈问题清单.md
```

Save regenerated or cleaned minutes under `输出文档/02_交流纪要/`. For these
minutes:

- follow the original conversation order unless a topic grouping is clearer;
- preserve who asked and who answered when identifiable;
- reconstruct clear questions and answers from the transcript;
- remove filler and repetition without changing meaning;
- separate unresolved questions and follow-up actions;
- note any section that could not be recovered from the source.

## Memory Graph Linkage

If `<workspace_root>/Memory Graph/` exists, use the companion `ai-work-hub-memory-graph` workflow.

Before finalizing, retrieve compact Memory Graph matches and inspect the source cards behind useful results. Add only a short `Memory Graph 联想` section:

```text
- 相似项目:
- 反例项目:
- 相关赛道/技术主题:
- 估值锚点:
- 这个项目必须证明的差异点:
```

After the project view changes:

- refresh the compact project header from finalized state with `sync_project.py --skip-rebuild`, then reread the card and prepare its current thesis, decisive facts and next signals; sync does not rewrite prose;
- link relevant non-project source notes when they materially support the judgment; do not copy their full content into the project;
- put reusable cross-project learning in the most direct sector map, technical theme, valuation anchor, high-signal person card, or durable event card;
- keep company-specific details in the project object;
- rewrite current understanding in affected higher-level objects when the conclusion changes; a dated news append alone is not a thesis update;
- apply content through the companion `write_graph.py` batch writer with hashes captured when reading; it serializes shared writes, rejects stale versions and rebuilds once. On conflict reread and merge, not overwrite. Validate and read back affected reasoning afterward;
- sector/theme pages link the authoritative project judgment instead of repeating current participation or price thresholds. Valuation pages retain dated comparable observations, not a second live transaction model;
- when a new public signal conflicts with the current thesis, state the affected assumption and useful reassessment action. Do not silently change a formal decision or revive an archived project.

Do not create a separate thesis ledger. Reusable investment views belong in sector maps, technical themes, valuation anchors, project counterexamples, or this skill's decision rules.

## Archive And Reactivate

Archive only after the user confirms the pass. Before moving the folder:

- update the final judgment and state;
- record the concrete signals that would justify reopening;
- sync the Memory Graph if the project is worth preserving as a counterexample.

Move the full project folder to `项目/归档/<项目名>/`. A later material update can reactivate it without erasing the original decision history.

## Completion Check

Before declaring the round complete, verify:

1. The exact new source was read; Feishu original content was attempted.
2. The same running judgment and core todo were updated.
3. Evidence labels match the real source quality.
4. The recommendation, participation, position, and price view do not contradict each other.
5. Public/team/valuation checks were run only where material.
6. Any question list or minutes file is separate and dated.
7. The output root contains only the stable judgment and state; other outputs
   are purpose-classified, and reproducible artifacts are isolated in `工作区/`.
8. Memory Graph retrieval/writeback is complete when available, or the failure is stated.
9. Confirmed passes were archived with reopen gates; historical reviews preserve time boundaries.
10. Validate the changed project and affected links/state. Reserve a full workspace audit for maintenance, migrations or cross-project changes; unrelated pre-existing errors do not justify expanding a normal diligence turn.

```bash
python3 <skill_dir>/scripts/validate_project.py \
  --workspace-root "<workspace_root>" \
  --project-dir "<project_dir>"
```
