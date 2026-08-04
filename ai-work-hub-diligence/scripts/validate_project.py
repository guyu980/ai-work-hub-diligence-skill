#!/usr/bin/env python3
"""Validate one AI Work Hub diligence project folder."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


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

DEPRECATED_FIELDS = {
    "card_path",
    "migration_status",
    "hia",
    "historical_review_path",
    "evidence_ledger_path",
    "context_package_path",
}


def infer_workspace_root(project_dir: Path) -> Path | None:
    for parent in [project_dir, *project_dir.parents]:
        if parent.name == "项目":
            return parent.parent
    return None


def load_state(path: Path, errors: list[str]) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        errors.append(f"invalid state JSON: {exc}")
        return {}
    if not isinstance(value, dict):
        errors.append("project state must be a JSON object")
        return {}
    return value


def validate(project_dir: Path, workspace_root: Path | None = None) -> list[str]:
    project_dir = project_dir.expanduser().resolve()
    workspace_root = (
        workspace_root.expanduser().resolve()
        if workspace_root
        else infer_workspace_root(project_dir)
    )
    errors: list[str] = []

    for name in ("原始资料", "解析文本", "输出文档"):
        if not (project_dir / name).is_dir():
            errors.append(f"missing directory: {name}")

    output_dir = project_dir / "输出文档"
    state_candidates = list(output_dir.glob("*_项目状态.json")) if output_dir.is_dir() else []
    if len(state_candidates) != 1:
        errors.append(f"expected one direct project state JSON, found {len(state_candidates)}")
        return errors

    state_path = state_candidates[0]
    state = load_state(state_path, errors)
    if not state:
        return errors

    name = str(state.get("name", "")).strip()
    if not name:
        errors.append("state name is required")
    if "/" in name or "\\" in name:
        errors.append("state name cannot contain path separators; use aliases")
    if state.get("project_id") != f"project:{name}":
        errors.append("project_id must equal project:<name>")
    if name and project_dir.name != name:
        errors.append(
            f"project directory name {project_dir.name!r} must equal state name {name!r}"
        )
    if state_path.name != f"{name}_项目状态.json":
        errors.append("state filename must equal <name>_项目状态.json")
    if state.get("schema_version") != 2:
        errors.append("state schema_version must be 2")
    if state.get("type") != "project_state":
        errors.append("state type must be project_state")
    if not str(state.get("primary_sector", "")).strip():
        errors.append("primary_sector is required before project completion")

    for key, allowed in ENUMS.items():
        if state.get(key) not in allowed:
            errors.append(f"invalid {key}: {state.get(key)!r}")

    archived_location = "归档" in project_dir.parts
    if archived_location and state.get("project_status") != "archived":
        errors.append("project under 项目/归档 must use project_status=archived")
    if not archived_location and state.get("project_status") == "archived":
        errors.append("archived project must be located under 项目/归档")
    if state.get("project_status") == "archived" and state.get("process_stage") != "archived":
        errors.append("archived project must use process_stage=archived")
    if state.get("project_status") == "active" and state.get("process_stage") == "archived":
        errors.append("active project cannot use process_stage=archived")

    if state.get("intake_mode") == "historical_review":
        if state.get("historical_outcome") == "not_applicable":
            errors.append("historical_review requires a historical_outcome")
        if state.get("review_status") == "not_applicable":
            errors.append("historical_review requires a review_status")
    elif state.get("historical_outcome") != "not_applicable":
        errors.append("live intake must use historical_outcome=not_applicable")

    if not state.get("judgment_display"):
        errors.append("judgment_display is required")
    for key in ("blocking_gates", "watch_signals", "source_refs"):
        if not isinstance(state.get(key), list):
            errors.append(f"{key} must be a list")
    for key in sorted(DEPRECATED_FIELDS & state.keys()):
        errors.append(f"deprecated state field must be removed: {key}")

    running_value = str(state.get("running_judgment_path", "")).strip()
    if not running_value:
        errors.append("running_judgment_path is required")
    elif workspace_root:
        running_path = Path(running_value).expanduser()
        if not running_path.is_absolute():
            running_path = workspace_root / running_path
        running_path = running_path.resolve()
        expected = output_dir / f"{name}_项目判断与todo.md"
        if running_path != expected.resolve():
            errors.append(
                "running_judgment_path must point to the stable "
                f"输出文档/{name}_项目判断与todo.md"
            )
        if not running_path.is_file():
            errors.append(f"running judgment does not exist: {running_value}")

    if workspace_root:
        for source_ref in state.get("source_refs", []):
            value = str(source_ref).strip()
            if not value.startswith("项目/"):
                continue
            source_path = (workspace_root / value).resolve()
            if not source_path.exists():
                errors.append(f"source_ref does not exist: {value}")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-dir", required=True)
    parser.add_argument("--workspace-root")
    args = parser.parse_args()
    project_dir = Path(args.project_dir)
    workspace_root = Path(args.workspace_root) if args.workspace_root else None
    errors = validate(project_dir, workspace_root)
    if errors:
        print(f"FAILED with {len(errors)} error(s)")
        for error in errors:
            print(f"- {error}")
        return 1
    print(f"OK: {project_dir.expanduser().resolve().name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
