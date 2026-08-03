#!/usr/bin/env python3
"""Build a portable context-package/v1 from a local diligence project."""

from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime
from pathlib import Path
from typing import Any


PACKAGE_TYPES = {
    "new_context", "state_update", "workflow_output", "resource_update",
    "strategy_input", "graph_delta", "outcome"
}
VISIBILITY = {"organization", "organization_core", "project_team", "restricted"}


def relative(path: Path, root: Path) -> str:
    try:
        return path.resolve().relative_to(root.resolve()).as_posix()
    except ValueError:
        raise SystemExit(
            f"Local package path must stay inside the workspace root: {path.resolve()}"
        ) from None


def local_locator(path: Path, root: Path) -> dict[str, str]:
    return {
        "backend": "local",
        "kind": "folder" if path.is_dir() else "file",
        "uri": relative(path, root),
    }


def normalize_ref(value: Any, workspace_root: Path) -> dict[str, str] | None:
    if isinstance(value, dict):
        if all(value.get(key) for key in ("backend", "kind", "uri")):
            locator = dict(value)
            if locator["backend"] == "local":
                path = Path(str(locator["uri"])).expanduser()
                if not path.is_absolute():
                    path = workspace_root / path
                locator["uri"] = relative(path, workspace_root)
            return locator
        return None
    text = str(value or "").strip()
    if not text:
        return None
    if text.startswith(("http://", "https://")):
        backend = "feishu" if any(
            token in text for token in ("feishu.cn", "larksuite.com")
        ) else "web"
        return {"backend": backend, "kind": "url", "uri": text}
    path = Path(text).expanduser()
    if not path.is_absolute():
        path = workspace_root / path
    return local_locator(path, workspace_root)


def artifact(
    artifact_id: str,
    collection: str,
    title: str,
    path: Path,
    workspace_root: Path,
) -> dict[str, Any]:
    return {
        "artifact_id": artifact_id,
        "collection": collection,
        "title": title,
        "locator": local_locator(path, workspace_root),
    }


def find_one(paths: list[Path], label: str, required: bool = False) -> Path | None:
    unique = sorted({path.resolve() for path in paths if path.exists()})
    if len(unique) > 1:
        raise SystemExit(f"Expected at most one {label}, found {len(unique)}")
    if required and not unique:
        raise SystemExit(f"Missing {label}")
    return unique[0] if unique else None


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--workspace-root", required=True)
    parser.add_argument("--project-dir", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--package-type", default="workflow_output")
    parser.add_argument("--trigger-type", default="diligence_update")
    parser.add_argument("--trigger-summary", required=True)
    parser.add_argument("--actor-type", default="agent", choices=["human", "agent", "automation"])
    parser.add_argument("--actor-id", default="codex")
    parser.add_argument("--runtime", default="codex")
    parser.add_argument("--runtime-version", default="current")
    parser.add_argument("--visibility", default="restricted")
    parser.add_argument("--workflow-id", default="workflow:ai-work-hub-diligence")
    parser.add_argument("--workflow-version", default="current-main")
    parser.add_argument("--source-ref", action="append", default=[])
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()

    if args.package_type not in PACKAGE_TYPES:
        parser.error(f"invalid package type: {args.package_type}")
    if args.visibility not in VISIBILITY:
        parser.error(f"invalid visibility: {args.visibility}")

    workspace_root = Path(args.workspace_root).expanduser().resolve()
    project_dir = Path(args.project_dir).expanduser().resolve()
    output = Path(args.output).expanduser().resolve()
    relative(project_dir, workspace_root)
    if output.exists() and not args.force:
        raise SystemExit(f"Refusing to overwrite existing package: {output}")

    state_path = find_one(
        list((project_dir / "输出文档").glob("*_项目状态.json")),
        "project state",
        required=True,
    )
    assert state_path is not None
    state = json.loads(state_path.read_text(encoding="utf-8"))
    object_id = str(state.get("project_id") or f"project:{project_dir.name}")
    title = str(state.get("name") or project_dir.name)

    ledger_path = project_dir / "解析文本" / "证据账本.jsonl"
    judgment_path: Path | None = None
    running_ref = str(state.get("running_judgment_path") or "").strip()
    if running_ref:
        candidate = Path(running_ref).expanduser()
        judgment_path = candidate if candidate.is_absolute() else workspace_root / candidate
        if not judgment_path.exists():
            judgment_path = None
    if judgment_path is None:
        judgment_path = find_one(
            list((project_dir / "输出文档").glob("*项目判断*todo*.md")),
            "running judgment",
        )

    artifacts: list[dict[str, Any]] = [
        artifact(
            f"artifact:{object_id}:state",
            "structured_context",
            "Project current state",
            state_path,
            workspace_root,
        )
    ]
    if ledger_path.exists():
        artifacts.append(
            artifact(
                f"artifact:{object_id}:evidence-ledger",
                "structured_context",
                "Evidence ledger",
                ledger_path,
                workspace_root,
            )
        )
    judgment_artifact_id = ""
    if judgment_path is not None:
        judgment_artifact_id = f"artifact:{object_id}:running-judgment"
        artifacts.append(
            artifact(
                judgment_artifact_id,
                "workflow_outputs",
                "Running investment judgment",
                judgment_path,
                workspace_root,
            )
        )

    graph_delta: dict[str, Any] | None = None
    graph_candidates = sorted(
        (project_dir / "输出文档").glob("*graph*delta*.json")
    ) + sorted((project_dir / "输出文档").glob("*Graph*Delta*.json"))
    graph_path = find_one(graph_candidates, "graph delta")
    if graph_path is not None:
        graph_delta = json.loads(graph_path.read_text(encoding="utf-8"))
        artifacts.append(
            artifact(
                f"artifact:{object_id}:graph-delta",
                "workflow_outputs",
                "Graph delta",
                graph_path,
                workspace_root,
            )
        )

    source_values: list[Any] = [*args.source_ref, *state.get("source_refs", [])]
    source_refs = [
        locator for value in source_values
        if (locator := normalize_ref(value, workspace_root)) is not None
    ]
    if not source_refs:
        source_refs = [local_locator(project_dir / "原始资料", workspace_root)]

    digest = hashlib.sha256()
    identity = {
        "object_id": object_id,
        "package_type": args.package_type,
        "trigger_type": args.trigger_type,
        "trigger_summary": args.trigger_summary,
        "actor_type": args.actor_type,
        "actor_id": args.actor_id,
        "runtime": args.runtime,
        "runtime_version": args.runtime_version,
        "visibility": args.visibility,
        "workflow_id": args.workflow_id,
        "workflow_version": args.workflow_version,
        "source_refs": source_refs,
    }
    digest.update(
        json.dumps(
            identity,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        ).encode("utf-8")
    )
    digest.update(str(state.get("updated_at", "")).encode("utf-8"))
    for item in artifacts:
        digest.update(item["locator"]["uri"].encode("utf-8"))
        path = workspace_root / item["locator"]["uri"]
        if path.is_file():
            digest.update(path.read_bytes())
    package_id = f"pkg-{digest.hexdigest()[:16]}"

    now = datetime.now().astimezone().isoformat(timespec="seconds")
    workflow_artifacts = [judgment_artifact_id] if judgment_artifact_id else []
    package: dict[str, Any] = {
        "schema_version": "context-package/v1",
        "package_id": package_id,
        "package_type": args.package_type,
        "created_at": now,
        "created_by": {
            "actor_type": args.actor_type,
            "actor_id": args.actor_id,
            "runtime": args.runtime,
            "runtime_version": args.runtime_version,
        },
        "visibility": args.visibility,
        "object": {
            "object_id": object_id,
            "object_type": "project",
            "title": title,
            "aliases": state.get("aliases", []),
            "status": state.get("project_status", "active"),
            "object_root": local_locator(project_dir, workspace_root),
        },
        "trigger": {
            "trigger_type": args.trigger_type,
            "summary": args.trigger_summary,
            "occurred_at": now,
        },
        "source_refs": source_refs,
        "artifacts": artifacts,
        "current_state": state,
        "workflow_outputs": [
            {
                "workflow_id": args.workflow_id,
                "workflow_version": args.workflow_version,
                "summary": str(
                    state.get("judgment_display")
                    or state.get("summary")
                    or "Diligence state updated"
                ),
                "artifact_refs": workflow_artifacts,
            }
        ],
        "writeback": {
            "canonical_target": local_locator(project_dir, workspace_root),
            "requested_operation": "upsert_context_object",
        },
    }
    if graph_delta is not None:
        package["graph_delta"] = graph_delta

    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        json.dumps(package, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"Wrote context package: {output}")
    print(f"Package ID: {package_id}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
