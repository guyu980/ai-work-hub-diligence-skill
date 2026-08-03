#!/usr/bin/env python3
"""Validate one AI Work Hub diligence project folder."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


ENUMS = {
    "intake_mode": {"live", "historical_review"},
    "historical_outcome": {"not_applicable", "invested", "pass", "unknown"},
    "review_status": {
        "not_applicable", "pending", "in_progress", "reviewed", "refresh_due"
    },
    "project_status": {"active", "archived"},
    "process_stage": {
        "screening", "diligence", "ic", "closing", "monitoring", "archived"
    },
    "investment_decision": {
        "invest", "continue", "pause", "pass", "observe", "invested"
    },
    "recommended_play": {
        "lead", "co_lead", "follow", "small_option", "none", "tbd"
    },
    "position_size": {"standard", "small", "symbolic", "tbd"},
    "price_view": {
        "cheap", "reasonable", "expensive", "unacceptable", "unknown"
    },
    "confidence": {"low", "medium", "high"},
}
TIERS = {
    "contract_or_original", "customer_confirmed", "public_verified",
    "company_claim", "inference", "legacy_migrated"
}
STATUSES = {
    "confirmed", "partial", "unverified", "disputed", "stale", "superseded"
}
IMPACTS = {"high", "medium", "low"}
TEMPORAL_SCOPES = {"decision_time", "post_outcome", "current", "unknown"}
LOGICAL_COLLECTIONS = {
    "sources", "structured_context", "workflow_outputs",
    "actions_outcomes", "governance"
}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-dir", required=True)
    args = parser.parse_args()
    project_dir = Path(args.project_dir).expanduser().resolve()
    errors: list[str] = []
    for name in ("原始资料", "解析文本", "输出文档"):
        if not (project_dir / name).is_dir():
            errors.append(f"missing directory: {name}")
    state_candidates = list((project_dir / "输出文档").glob("*_项目状态.json"))
    if len(state_candidates) != 1:
        errors.append(f"expected one project state JSON, found {len(state_candidates)}")
        state = {}
    else:
        try:
            state = json.loads(state_candidates[0].read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            errors.append(f"invalid state JSON: {exc}")
            state = {}
    if state:
        if state.get("schema_version") != 2:
            errors.append("state schema_version must be 2")
        for key, allowed in ENUMS.items():
            if state.get(key) not in allowed:
                errors.append(f"invalid {key}: {state.get(key)!r}")
        if (
            state.get("intake_mode") == "historical_review"
            and state.get("historical_outcome") == "not_applicable"
        ):
            errors.append(
                "historical_review requires a historical_outcome"
            )
        if (
            state.get("intake_mode") == "historical_review"
            and state.get("review_status") == "not_applicable"
        ):
            errors.append("historical_review requires a review_status")
        if (
            state.get("intake_mode") == "live"
            and state.get("historical_outcome") != "not_applicable"
        ):
            errors.append(
                "live intake must use historical_outcome=not_applicable"
            )
        if not state.get("judgment_display"):
            errors.append("judgment_display is required")
    manifest_candidates = list(
        (project_dir / "输出文档").glob("*_context_object.json")
    )
    if len(manifest_candidates) > 1:
        errors.append(
            f"expected at most one context object manifest, found {len(manifest_candidates)}"
        )
    elif manifest_candidates:
        try:
            manifest = json.loads(
                manifest_candidates[0].read_text(encoding="utf-8")
            )
        except json.JSONDecodeError as exc:
            errors.append(f"invalid context object manifest: {exc}")
            manifest = {}
        if manifest:
            if manifest.get("schema_version") != "context-object/v1":
                errors.append("context object schema_version must be context-object/v1")
            if manifest.get("object_type") != "project":
                errors.append("context object object_type must be project")
            collections = manifest.get("collections")
            if not isinstance(collections, dict):
                errors.append("context object collections must be an object")
            else:
                missing = LOGICAL_COLLECTIONS - set(collections)
                if missing:
                    errors.append(
                        "context object missing logical collections: "
                        + ", ".join(sorted(missing))
                    )
    ledger = project_dir / "解析文本" / "证据账本.jsonl"
    if not ledger.exists():
        errors.append("missing evidence ledger")
    else:
        seen: set[str] = set()
        for number, raw in enumerate(ledger.read_text(encoding="utf-8").splitlines(), 1):
            if not raw.strip():
                continue
            try:
                item = json.loads(raw)
            except json.JSONDecodeError as exc:
                errors.append(f"evidence line {number}: invalid JSON: {exc}")
                continue
            evidence_id = str(item.get("evidence_id", ""))
            if not evidence_id or evidence_id in seen:
                errors.append(f"evidence line {number}: missing/duplicate evidence_id")
            seen.add(evidence_id)
            if item.get("evidence_tier") not in TIERS:
                errors.append(f"evidence line {number}: invalid evidence_tier")
            if item.get("status") not in STATUSES:
                errors.append(f"evidence line {number}: invalid status")
            if item.get("decision_impact") not in IMPACTS:
                errors.append(f"evidence line {number}: invalid decision_impact")
            if item.get("temporal_scope") not in TEMPORAL_SCOPES:
                errors.append(f"evidence line {number}: invalid temporal_scope")
            if not item.get("source_refs"):
                errors.append(f"evidence line {number}: source_refs is required")
    if errors:
        print(f"FAILED with {len(errors)} error(s)")
        for error in errors:
            print(f"- {error}")
        return 1
    print(
        f"OK: {project_dir.name}; "
        f"{len(seen) if ledger.exists() else 0} evidence record(s)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
