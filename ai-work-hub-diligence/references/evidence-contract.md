# Diligence State And Evidence Contract

The project folder is the source of truth. The Memory Graph is a compiled,
cross-project view. Generated indexes are caches and must be rebuildable.

For non-local deployments, read `context-storage-contract.md`. The canonical
project object is the source of truth, whether its locator resolves to a local
folder or a Feishu object root. The state and evidence schemas do not change
with the backend.

## Project State

Keep one machine-readable state file beside the running judgment:

```text
项目/<项目名>/输出文档/<项目名>_项目状态.json
```

Required fields:

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
  "blocking_gates": [],
  "watch_signals": [],
  "related_projects": [],
  "counterexamples": [],
  "source_refs": [],
  "storage_profile": "local",
  "object_root_ref": {},
  "context_package_ref": "",
  "running_judgment_path": "",
  "evidence_ledger_path": "",
  "evidence_backfill_status": "complete",
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

`storage_profile`, `object_root_ref`, and `context_package_ref` are optional for
legacy local projects. New cross-runtime or Feishu-compatible projects should
populate them. Source references may be typed locators from
`context-package/v1`; local projects may retain workspace-relative strings for
backward compatibility.

## Evidence Ledger

Keep append-only claim records in:

```text
项目/<项目名>/解析文本/证据账本.jsonl
```

One line is one judgment-changing, reusable, disputed, or high-stakes claim.
Do not create ledger entries merely to restate every BP paragraph, meeting
answer, or datapack field:

```json
{
  "schema_version": 2,
  "evidence_id": "ev-<stable-id>",
  "project_id": "project:<项目名>",
  "claim": "客户已完成一期验收并日常使用",
  "evidence_tier": "customer_confirmed",
  "status": "confirmed",
  "decision_impact": "high",
  "temporal_scope": "current",
  "source_refs": ["项目/<项目名>/解析文本/2026-07-24_客户访谈.md"],
  "source_locator": "客户A访谈，第12-18分钟",
  "observed_at": "YYYY-MM-DD",
  "recorded_at": "ISO-8601 timestamp",
  "supersedes": [],
  "notes": ""
}
```

Evidence tiers:

1. `contract_or_original`: executed contract, bank record, original transcript,
   original data export, audited or signed original.
2. `customer_confirmed`: customer, supplier, or other counterparty confirms it.
3. `public_verified`: reliable public source independently supports it.
4. `company_claim`: BP, company datapack, founder statement, or smart minutes.
5. `inference`: analyst calculation or interpretation.
6. `legacy_migrated`: retained historical conclusion without claim-level
   backfill; never treat it as upgraded evidence.

Statuses:

- `confirmed`, `partial`, `unverified`, `disputed`, `stale`, `superseded`

Decision impact:

- `high`, `medium`, `low`

Temporal scope:

- `decision_time`: information available at the original investment/pass decision.
- `post_outcome`: information learned only after that decision.
- `current`: new information from a current follow-up.
- `unknown`: timing cannot yet be established.

Never silently edit an old evidence line when a claim changes. Add a new record,
mark the old record `superseded` in a maintenance pass, and link the new
`evidence_id` through `supersedes`.

## Graph Delta

Use a graph delta only when a material diligence round adds reusable
cross-project knowledge or when an advanced deployment handoff needs a portable
change envelope:

```json
{
  "schema_version": 2,
  "project": "<项目名>",
  "relations_add": [],
  "thesis_proposals": [],
  "sector_proposals": [],
  "valuation_proposals": [],
  "event_triggers": []
}
```

Project-state and project-card updates may sync automatically. Apply clear,
source-backed reusable updates directly to their existing sector, technical,
valuation, thesis, person, or event destination. Ordinary public news belongs
in the related project card's dated `外部动态` section and does not require a
separate review-queue file.

For normal valuation observations, record project, date, round/stage, stated
valuation, financing amount, currency, source context, and a short comparability
note. Transaction status, payment proof, special rights, and closing detail are
optional and should be added only when they affect ownership, portfolio marking,
return math, closing risk, legal rights, source conflict, or the investment
decision. Keep internal fair value separate from observed or company-stated
market price.

## Source Rules

- Source paths are arrays, not semicolon-packed prose.
- Smart minutes are `company_claim` unless checked against the original
  transcript.
- A POC is not an order; a logo is not customer confirmation; an advisor figure
  is not audited data.
- Public news may create a review trigger but must not automatically change an
  investment decision.

## Historical Review

Historical projects use the same folder, state, evidence, card, and graph
contracts. Set `intake_mode=historical_review` and preserve the original outcome
separately from the current reassessment.

- Already invested: usually `historical_outcome=invested`,
  `investment_decision=invested`, `process_stage=monitoring`.
- Historical pass: usually `historical_outcome=pass`,
  `investment_decision=pass`, `project_status=archived`.
- Reopened historical pass: keep `historical_outcome=pass`, but update the
  current `investment_decision`, `process_stage`, and `project_status`; never
  erase the original pass.

Separate decision quality from outcome quality. Do not use evidence marked
`post_outcome` to claim the original decision was obvious. Historical pass
projects may be highly valuable counterexamples and should remain retrievable.
