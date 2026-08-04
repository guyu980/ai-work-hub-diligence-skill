# Project State Contract

The project folder is the source of truth. The running judgment is the complete
human-readable view, the project state stores the current machine-readable
decision, and the Memory Graph is a compressed cross-project view.

## Project State

Keep one state file beside the running judgment:

```text
项目/<项目名>/输出文档/<项目名>_项目状态.json
```

Required shape:

```json
{
  "schema_version": 2,
  "type": "project_state",
  "project_id": "project:<项目名>",
  "name": "<项目名>",
  "aliases": [],
  "primary_sector": "",
  "tags": [],
  "intake_mode": "live",
  "historical_outcome": "not_applicable",
  "review_status": "not_applicable",
  "historical_decision_date": "",
  "review_as_of": "",
  "project_status": "active",
  "process_stage": "diligence",
  "investment_decision": "continue",
  "recommended_play": "tbd",
  "position_size": "tbd",
  "price_view": "unknown",
  "confidence": "medium",
  "judgment_display": "继续推进",
  "stage": "",
  "valuation": "",
  "summary": "",
  "blocking_gates": [],
  "watch_signals": [],
  "related_projects": [],
  "counterexamples": [],
  "source_refs": [],
  "running_judgment_path": "",
  "created_at": "YYYY-MM-DD",
  "updated_at": "YYYY-MM-DD"
}
```

Enums:

- `intake_mode`: `live`, `historical_review`
- `historical_outcome`: `not_applicable`, `invested`, `pass`, `unknown`
- `review_status`: `not_applicable`, `pending`, `in_progress`, `reviewed`, `refresh_due`
- `project_status`: `active`, `archived`
- `process_stage`: `screening`, `diligence`, `ic`, `closing`, `monitoring`, `archived`
- `investment_decision`: `invest`, `continue`, `pause`, `pass`, `observe`, `invested`
- `recommended_play`: `lead`, `co_lead`, `follow`, `small_option`, `none`, `tbd`
- `position_size`: `standard`, `small`, `symbolic`, `tbd`
- `price_view`: `cheap`, `reasonable`, `expensive`, `unacceptable`, `unknown`
- `confidence`: `low`, `medium`, `high`

Do not mix decision, role, sizing, and price into one enum. Keep
`judgment_display` as the readable combined conclusion.

## Source Boundaries

Keep source quality in the running judgment rather than a separate claim
ledger. Use short sections or labels for:

- `已核验`: original documents, customer confirmation, or reliable public facts;
- `公司/来源自述`: BP, datapack, founder, FA, meeting, or forecast claims;
- `待核验`: missing, stale, inconsistent, ambiguous, or disputed information.

Record only the facts that materially support or challenge the investment view.
Do not restate every BP paragraph, meeting answer, parameter, or transaction
status. Link the most useful original or parsed sources through `source_refs` or
inside the running judgment.

Smart minutes are navigation. Read the original transcript when available. A
POC is not an order, a logo is not customer confirmation, and an advisor figure
is not audited data.

## Historical Review

Historical projects use the same state and running judgment. Preserve these
time boundaries in the review document:

- `decision_time`: information available at the original decision;
- `post_outcome`: information learned only after that decision;
- `current`: information relevant to a new decision now.

Keep the original outcome separate from the current reassessment. Do not use
later results to make the original decision look obvious.

## Memory Graph

Sync the project state and project card after the running judgment changes.
Write only reusable cross-project learning to the most direct sector, technical,
valuation, event, or person object. Generated JSONL indexes are caches and must
be rebuilt rather than hand-edited.
