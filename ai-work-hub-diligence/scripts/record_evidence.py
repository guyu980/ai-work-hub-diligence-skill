#!/usr/bin/env python3
"""Append one validated claim to a project's evidence ledger."""

from __future__ import annotations

import argparse
import hashlib
import json
from datetime import date, datetime
from pathlib import Path


TIERS = {
    "contract_or_original",
    "customer_confirmed",
    "public_verified",
    "company_claim",
    "inference",
    "legacy_migrated",
}
STATUSES = {
    "confirmed", "partial", "unverified", "disputed", "stale", "superseded"
}
IMPACTS = {"high", "medium", "low"}
TEMPORAL_SCOPES = {"decision_time", "post_outcome", "current", "unknown"}


def existing_ids(path: Path) -> set[str]:
    result: set[str] = set()
    if not path.exists():
        return result
    for number, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not raw.strip():
            continue
        value = json.loads(raw)
        if not isinstance(value, dict):
            raise ValueError(f"{path}:{number}: expected a JSON object")
        result.add(str(value.get("evidence_id", "")))
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--ledger", required=True)
    parser.add_argument("--project-id", required=True)
    parser.add_argument("--claim", required=True)
    parser.add_argument("--tier", required=True, choices=sorted(TIERS))
    parser.add_argument("--status", required=True, choices=sorted(STATUSES))
    parser.add_argument("--impact", required=True, choices=sorted(IMPACTS))
    parser.add_argument(
        "--temporal-scope",
        default="current",
        choices=sorted(TEMPORAL_SCOPES),
    )
    parser.add_argument("--source", action="append", default=[])
    parser.add_argument("--locator", default="")
    parser.add_argument("--observed-at", default=str(date.today()))
    parser.add_argument("--supersedes", action="append", default=[])
    parser.add_argument("--notes", default="")
    args = parser.parse_args()
    if not args.source:
        parser.error("at least one --source is required")
    ledger = Path(args.ledger).expanduser().resolve()
    ledger.parent.mkdir(parents=True, exist_ok=True)
    canonical = "|".join(
        [
            args.project_id,
            args.claim,
            args.tier,
            args.temporal_scope,
            args.observed_at,
            *sorted(args.source),
        ]
    )
    evidence_id = "ev-" + hashlib.sha256(canonical.encode("utf-8")).hexdigest()[:16]
    if evidence_id in existing_ids(ledger):
        raise SystemExit(f"Duplicate evidence record: {evidence_id}")
    record = {
        "schema_version": 2,
        "evidence_id": evidence_id,
        "project_id": args.project_id,
        "claim": args.claim,
        "evidence_tier": args.tier,
        "status": args.status,
        "decision_impact": args.impact,
        "temporal_scope": args.temporal_scope,
        "source_refs": args.source,
        "source_locator": args.locator,
        "observed_at": args.observed_at,
        "recorded_at": datetime.now().astimezone().isoformat(timespec="seconds"),
        "supersedes": args.supersedes,
        "notes": args.notes,
    }
    with ledger.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(record, ensure_ascii=False, separators=(",", ":")))
        handle.write("\n")
    print(json.dumps(record, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
