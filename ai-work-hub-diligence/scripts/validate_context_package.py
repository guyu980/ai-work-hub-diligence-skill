#!/usr/bin/env python3
"""Validate the core contract of a context-package/v1 JSON file."""

from __future__ import annotations

import argparse
import json
import re
from datetime import datetime
from pathlib import Path
from typing import Any


PACKAGE_TYPES = {
    "new_context", "state_update", "workflow_output", "resource_update",
    "strategy_input", "graph_delta", "outcome"
}
VISIBILITY = {"organization", "organization_core", "project_team", "restricted"}
BACKENDS = {"local", "feishu", "web", "other"}
KINDS = {"file", "folder", "document", "base_record", "url"}
COLLECTIONS = {
    "sources", "structured_context", "workflow_outputs",
    "actions_outcomes", "governance"
}
OBJECT_TYPES = {
    "project", "event", "report", "thesis", "person", "decision_snapshot",
    "capital_resource", "human_capital", "workflow"
}


def check_datetime(value: Any, label: str, errors: list[str]) -> None:
    try:
        parsed = datetime.fromisoformat(str(value).replace("Z", "+00:00"))
    except ValueError:
        errors.append(f"{label} must be an ISO 8601 date-time")
        return
    if parsed.tzinfo is None:
        errors.append(f"{label} must include a timezone")


def check_locator(value: Any, label: str, errors: list[str]) -> None:
    if not isinstance(value, dict):
        errors.append(f"{label} must be an object")
        return
    if value.get("backend") not in BACKENDS:
        errors.append(f"{label}.backend is invalid")
    if value.get("kind") not in KINDS:
        errors.append(f"{label}.kind is invalid")
    uri = str(value.get("uri") or "").strip()
    if not uri:
        errors.append(f"{label}.uri is required")
    elif value.get("backend") == "local":
        parts = Path(uri.replace("\\", "/")).parts
        if (
            uri.startswith(("/", "~/", "~\\"))
            or re.match(r"^[A-Za-z]:[\\/]", uri)
            or ".." in parts
        ):
            errors.append(f"{label}.uri must be workspace-relative")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("package")
    args = parser.parse_args()
    path = Path(args.package).expanduser().resolve()
    try:
        package = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"FAILED: {exc}")
        return 1

    errors: list[str] = []
    required = {
        "schema_version", "package_id", "package_type", "created_at",
        "created_by", "visibility", "object", "trigger", "source_refs"
    }
    for key in sorted(required - set(package)):
        errors.append(f"missing required field: {key}")
    if package.get("schema_version") != "context-package/v1":
        errors.append("schema_version must be context-package/v1")
    if package.get("package_type") not in PACKAGE_TYPES:
        errors.append("package_type is invalid")
    if package.get("visibility") not in VISIBILITY:
        errors.append("visibility is invalid")
    if not str(package.get("package_id") or "").strip():
        errors.append("package_id is required")
    if package.get("created_at") is not None:
        check_datetime(package["created_at"], "created_at", errors)

    actor = package.get("created_by")
    if not isinstance(actor, dict):
        errors.append("created_by must be an object")
    else:
        if actor.get("actor_type") not in {"human", "agent", "automation"}:
            errors.append("created_by.actor_type is invalid")
        if not str(actor.get("actor_id") or "").strip():
            errors.append("created_by.actor_id is required")

    obj = package.get("object")
    if not isinstance(obj, dict):
        errors.append("object must be an object")
    else:
        for key in ("object_id", "object_type", "title"):
            if not str(obj.get(key) or "").strip():
                errors.append(f"object.{key} is required")
        if obj.get("object_type") not in OBJECT_TYPES:
            errors.append("object.object_type is invalid")
        if obj.get("object_root") is not None:
            check_locator(obj["object_root"], "object.object_root", errors)

    trigger = package.get("trigger")
    if not isinstance(trigger, dict):
        errors.append("trigger must be an object")
    else:
        for key in ("trigger_type", "summary"):
            if not str(trigger.get(key) or "").strip():
                errors.append(f"trigger.{key} is required")
        if trigger.get("occurred_at") is not None:
            check_datetime(trigger["occurred_at"], "trigger.occurred_at", errors)

    source_refs = package.get("source_refs")
    if not isinstance(source_refs, list):
        errors.append("source_refs must be an array")
    else:
        if not source_refs:
            errors.append("source_refs must contain at least one locator")
        for index, value in enumerate(source_refs):
            check_locator(value, f"source_refs[{index}]", errors)

    seen_artifacts: set[str] = set()
    artifacts = package.get("artifacts", [])
    if not isinstance(artifacts, list):
        errors.append("artifacts must be an array")
    else:
        for index, value in enumerate(artifacts):
            label = f"artifacts[{index}]"
            if not isinstance(value, dict):
                errors.append(f"{label} must be an object")
                continue
            artifact_id = str(value.get("artifact_id") or "")
            if not artifact_id or artifact_id in seen_artifacts:
                errors.append(f"{label}.artifact_id is missing or duplicated")
            seen_artifacts.add(artifact_id)
            if value.get("collection") not in COLLECTIONS:
                errors.append(f"{label}.collection is invalid")
            if not str(value.get("title") or "").strip():
                errors.append(f"{label}.title is required")
            check_locator(value.get("locator"), f"{label}.locator", errors)

    if errors:
        print(f"FAILED with {len(errors)} error(s)")
        for error in errors:
            print(f"- {error}")
        return 1
    print(
        f"OK: {package['package_id']}; {len(artifacts)} artifact(s); "
        f"object={package['object']['object_id']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
