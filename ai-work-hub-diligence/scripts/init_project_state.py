#!/usr/bin/env python3
"""Initialize schema-v2 diligence state and an evidence ledger."""

from __future__ import annotations

import argparse
import json
from datetime import date
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


def relative(path: Path, root: Path) -> str:
    try:
        return path.relative_to(root).as_posix()
    except ValueError:
        return str(path)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--workspace-root", required=True)
    parser.add_argument("--project-name", required=True)
    parser.add_argument("--project-dir")
    parser.add_argument("--sector", default="")
    parser.add_argument("--intake-mode", default="live")
    parser.add_argument("--historical-outcome", default="not_applicable")
    parser.add_argument("--review-status", default="not_applicable")
    parser.add_argument("--historical-decision-date", default="")
    parser.add_argument("--review-as-of", default="")
    parser.add_argument("--decision", default="observe")
    parser.add_argument("--play", default="tbd")
    parser.add_argument("--position-size", default="tbd")
    parser.add_argument("--price-view", default="unknown")
    parser.add_argument("--process-stage", default="screening")
    parser.add_argument("--confidence", default="medium")
    parser.add_argument("--judgment-display", default="观察")
    args = parser.parse_args()
    values = {
        "intake_mode": args.intake_mode,
        "historical_outcome": args.historical_outcome,
        "review_status": args.review_status,
        "project_status": "active",
        "process_stage": args.process_stage,
        "investment_decision": args.decision,
        "recommended_play": args.play,
        "position_size": args.position_size,
        "price_view": args.price_view,
        "confidence": args.confidence,
    }
    for key, value in values.items():
        if value not in ENUMS[key]:
            parser.error(f"invalid {key}: {value}")

    workspace_root = Path(args.workspace_root).expanduser().resolve()
    project_dir = (
        Path(args.project_dir).expanduser().resolve()
        if args.project_dir
        else workspace_root / "项目" / args.project_name
    )
    for name in ("原始资料", "解析文本", "输出文档"):
        (project_dir / name).mkdir(parents=True, exist_ok=True)
    evidence_path = project_dir / "解析文本" / "证据账本.jsonl"
    evidence_path.touch(exist_ok=True)
    judgment_candidates = sorted(
        (project_dir / "输出文档").glob("*项目判断*todo*.md")
    )
    judgment_path = judgment_candidates[0] if judgment_candidates else None
    state_path = project_dir / "输出文档" / f"{args.project_name}_项目状态.json"
    if state_path.exists():
        raise SystemExit(f"Refusing to overwrite existing state: {state_path}")
    actions_path = project_dir / "输出文档" / "行动与结果"
    governance_path = project_dir / "输出文档" / "治理与确认"
    object_manifest_path = (
        project_dir / "输出文档" / f"{args.project_name}_context_object.json"
    )
    today = str(date.today())
    object_root_ref = {
        "backend": "local",
        "kind": "folder",
        "uri": relative(project_dir, workspace_root),
    }
    payload = {
        "schema_version": 2,
        "type": "project_state",
        "project_id": f"project:{args.project_name}",
        "name": args.project_name,
        "aliases": [],
        "primary_sector": args.sector,
        "tags": [],
        **values,
        "historical_decision_date": args.historical_decision_date,
        "review_as_of": args.review_as_of,
        "judgment_display": args.judgment_display,
        "stage": "",
        "valuation": "",
        "summary": "",
        "blocking_gates": [],
        "watch_signals": [],
        "related_projects": [],
        "counterexamples": [],
        "source_refs": [],
        "storage_profile": "local",
        "object_root_ref": object_root_ref,
        "object_manifest_path": relative(object_manifest_path, workspace_root),
        "context_package_ref": "",
        "running_judgment_path": (
            relative(judgment_path, workspace_root) if judgment_path else ""
        ),
        "evidence_ledger_path": relative(evidence_path, workspace_root),
        "evidence_backfill_status": "complete",
        "created_at": today,
        "updated_at": today,
    }
    object_manifest = {
        "schema_version": "context-object/v1",
        "object_id": payload["project_id"],
        "object_type": "project",
        "title": args.project_name,
        "storage_profile": "local",
        "canonical_write_target": object_root_ref,
        "collections": {
            "sources": {
                "backend": "local",
                "kind": "folder",
                "uri": relative(project_dir / "原始资料", workspace_root),
            },
            "structured_context": {
                "backend": "local",
                "kind": "folder",
                "uri": relative(project_dir / "解析文本", workspace_root),
            },
            "workflow_outputs": {
                "backend": "local",
                "kind": "folder",
                "uri": relative(project_dir / "输出文档", workspace_root),
            },
            "actions_outcomes": {
                "backend": "local",
                "kind": "folder",
                "uri": relative(actions_path, workspace_root),
            },
            "governance": {
                "backend": "local",
                "kind": "folder",
                "uri": relative(governance_path, workspace_root),
            },
        },
        "current_state_ref": {
            "backend": "local",
            "kind": "file",
            "uri": relative(state_path, workspace_root),
        },
        "evidence_ledger_ref": {
            "backend": "local",
            "kind": "file",
            "uri": relative(evidence_path, workspace_root),
        },
        "visibility": "restricted",
        "created_at": today,
        "updated_at": today,
    }
    object_manifest_path.write_text(
        json.dumps(object_manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    state_path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"Initialized project state: {state_path}")
    print(f"Context object manifest: {object_manifest_path}")
    print(f"Evidence ledger: {evidence_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
