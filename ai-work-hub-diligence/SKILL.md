---
name: ai-work-hub-diligence
description: Continuously assess one company from BPs, datapacks, Feishu originals and project updates. Maintain one investment judgment and focused next actions, prepare dated questions or minutes, and recall relevant prior knowledge. Non-project interviews and thematic sources belong to ai-work-hub-memory-graph.
---

# AI Work Hub Diligence

## Ownership And Routing

One company owns one running judgment/todo and one structured state. Update them in place; question lists and cleaned minutes are separate dated files. Respect chat-only requests.

- New BP/material: locate or initialize the project, read it, give an initial view and a short preliminary question list.
- Follow-up datapack/interview: compare with the existing view and update the same files.
- Interview preparation/minutes: produce the requested dated deliverable; do not invent a new investment review.
- Invested company, fund or transaction: inherit the current business view and work on the requested operating/transaction question. Keep detailed holdings, budgets and clauses in their existing papers.
- Non-project expert interview, podcast or thematic source: use `ai-work-hub-memory-graph`; no company folder or project title.
- Explicit formal deep research: use `ai-work-hub-deep-research`; its report is not a second running judgment.
- Confirmed pass: update the final view and reopening signals, then move the whole folder under `项目/归档/`. Do not archive solely on the agent's recommendation.

Confirm an unknown workspace path on first use. Reuse known paths and project aliases later. For **new-project setup only**, read [project-setup.md](references/project-setup.md): layout, initializer and one-time `Project <项目名>` naming. Naming uses dedicated tooling → official App Server → readback. Do not check titles again on subsequent updates.

## Core Loop

1. Read the current judgment/state and the few relevant existing sources. Retrieve useful prior projects, mechanisms, counterexamples and prices when Memory Graph is available.
2. Read the actual new material, reusing parsed originals. For Feishu links, read [feishu-cli.md](references/feishu-cli.md) when access/setup is needed; find original text/transcript as well as smart minutes and follow relevant nested links. State any access limit.
3. Identify what reinforces, changes or challenges the thesis. On a material change reconsider the strongest opposing explanation; on a minor change edit only the affected content.
4. Resolve uncertainties only to the depth that can change the next action. Write the current view, decisive reasons and worthwhile next questions into the same judgment.
5. Finalize the readable view, then synchronize state using [project-state.md](references/project-state.md). Record meaningful dated changes, not a transcript of every operation.
6. Write durable learning to the optional Graph, validate this round's affected files and read back the result.
7. Reply with the current view, what changed and the few useful next actions. No useful action or no material Graph delta is a valid result.

Do not repeat background searches, initialization, full-workspace audits or every reference on each turn.

## Analytical Scale

An initial screen needs the business/technical logic, strongest counterargument and decision-changing questions. Attributed BP/interview/datapack figures are usable; lack of independent verification alone is neither a negative finding nor a mandatory todo.

Deepen a check when a contradiction or gap could change action, price, ownership math or closing risk. Do not default to contracts, bank records, complete customer lists, legal/IP audits or engineering reproduction. Keep proposed thresholds distinguishable from observed facts and explain their basis. Risks need not all become tasks; important analysis has no mechanical item cap.

Use source labels where meaningful: `已核验`, `公司/来源自述`, `待核验`. A faithful transcript confirms what was said, not the operating claim. Source attribution is not a demand to verify every sentence.

For identifiable technical founders/leaders whose contribution matters, use [technical-team.md](references/technical-team.md). Research them when first encountered, add newly identified material leaders later, and maintain the assessment inside the running judgment, not separate biographies for every employee.

When price matters, use [valuation.md](references/valuation.md): stated price/round/date/financing, operating maturity and the most informative comparables. Separate observed company/market prices from the analyst's reasonable price. Do not request agreements merely to complete a valuation table.

For retrospective invested/passed projects, use [historical-review.md](references/historical-review.md). Distinguish decision-time evidence, subsequent outcomes and today's choice.

## Running Judgment

Follow the existing document where usable. Put the current decision and business logic first, followed by decisive facts, strongest counterargument, material team/valuation context, useful memory connections and core todo. Keep period, unit, actual/forecast and source next to important metrics. Keep transaction details linked rather than replacing company positioning with the latest legal task.

Use stage-appropriate language:

- `投`: evidence and price support an active investment decision.
- `继续推进`: worth the next diligence step; not a capital commitment. Ordinary early-stage unknowns do not by themselves require `暂缓`.
- `暂缓`: do not advance until named, material signals arrive.
- `不投`: evidence, price, fit or priority does not justify further work.

Participation clarifies, rather than duplicates, the recommendation: `领投` normally implies a standard/concentrated position; `跟投` may be standard/small; `小额 option` describes a small exposure with meaningful upside and unresolved proof, not a synonym for follow-on or staged funding. Do not add investment-purpose or funding-cadence dimensions.

Questions prioritize what could change the next action. Cleaned minutes reconstruct clear questions and answers from the original, preserve speakers when known, remove filler without changing meaning, and disclose unrecoverable portions. Use the purpose-based folders in the setup reference.

## Memory Linkage

With a private Graph available, use `ai-work-hub-memory-graph` for retrieval and shared writes. Read useful matches, not every layer. Explain the analogy and its limit; omit empty lists of peers or price anchors.

At the next natural project update, inspect **selected material external signals** already on the card. Merge a still-useful question into the existing core todo or interview list; retire it if the new material resolves it. Do not copy every news item into tasks or create another follow-up queue.

After finalizing the project state, `sync_project.py --skip-rebuild` refreshes the compact header, not the prose. Reread the card and update its business thesis, decisive facts and next signals from the finalized judgment. Apply Graph content through the companion hash-checked `write_graph.py` batch, then validate/read back. On conflict reread and merge.

Reusable changes belong in the relevant existing sector/theme/valuation object; repetitive news that only restates a known concern stays in the source/report. Rewrite the current synthesis when an assumption changes. Higher-level pages link the authoritative company decision instead of keeping another live price/participation copy. Public news and maintenance never silently change formal investment decisions.

## Acceptance

Check the actual new source coverage, consistency of judgment/state/date, any dated deliverable and the affected links/Graph reasoning. Formatting or rereading alone does not advance the content-as-of date. State exact limitations; do not treat a plan, sync hash or successful tool call as verified analysis.

```bash
python3 <skill_dir>/scripts/validate_project.py --workspace-root "<root>" --project-dir "<project_dir>"
```

Full-workspace audit and migration are maintenance operations, not routine diligence. Private materials and generated knowledge never belong in this public repository.
