#!/usr/bin/env python3
"""Audit project coverage and workflow consistency across one workspace."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from validate_project import validate


DEFAULT_CONFIG = {
    "exclude_project_dirs": [],
    "require_project_cards": False,
}


def load_config(workspace_root: Path, config_path: Path | None) -> dict:
    path = config_path or workspace_root / ".ai-work-hub.json"
    config = dict(DEFAULT_CONFIG)
    if path.exists():
        value = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(value, dict):
            raise ValueError(f"workspace config must be a JSON object: {path}")
        config.update(value)
    return config


def project_dirs(projects_root: Path, excluded: set[str]) -> list[Path]:
    values: list[Path] = []
    for path in projects_root.iterdir():
        if not path.is_dir() or path.name.startswith(".") or path.name == "归档":
            continue
        if path.name not in excluded and path.relative_to(projects_root).as_posix() not in excluded:
            values.append(path)
    archive = projects_root / "归档"
    if archive.is_dir():
        for path in archive.iterdir():
            if not path.is_dir() or path.name.startswith("."):
                continue
            relative = path.relative_to(projects_root).as_posix()
            if path.name not in excluded and relative not in excluded:
                values.append(path)
    return sorted(values, key=lambda item: item.as_posix())


def card_names(memory_root: Path) -> tuple[dict[str, list[Path]], list[str]]:
    names: dict[str, list[Path]] = {}
    errors: list[str] = []
    card_root = memory_root / "01_项目卡片"
    if not card_root.is_dir():
        return names, errors
    for path in card_root.glob("*.md"):
        first = path.read_text(encoding="utf-8").splitlines()[:1]
        if not first or not first[0].startswith("# 项目卡片｜"):
            errors.append(f"invalid project card title: {path.relative_to(memory_root)}")
            continue
        name = first[0].split("｜", 1)[1].strip()
        names.setdefault(name, []).append(path)
    return names, errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--workspace-root", required=True)
    parser.add_argument("--config")
    args = parser.parse_args()
    workspace_root = Path(args.workspace_root).expanduser().resolve()
    projects_root = workspace_root / "项目"
    config = load_config(
        workspace_root,
        Path(args.config).expanduser().resolve() if args.config else None,
    )
    excluded = {str(value).strip("/") for value in config.get("exclude_project_dirs", [])}
    require_cards = bool(config.get("require_project_cards", False))
    errors: list[str] = []
    warnings: list[str] = []
    projects = project_dirs(projects_root, excluded)
    state_names: set[str] = set()

    for project_dir in projects:
        relative = project_dir.relative_to(workspace_root).as_posix()
        project_errors = validate(project_dir, workspace_root)
        errors.extend(f"{relative}: {item}" for item in project_errors)
        states = list((project_dir / "输出文档").glob("*_项目状态.json"))
        if len(states) == 1:
            try:
                state_names.add(json.loads(states[0].read_text(encoding="utf-8"))["name"])
            except (json.JSONDecodeError, KeyError):
                pass

    cards, card_errors = card_names(workspace_root / "Memory Graph")
    errors.extend(card_errors)
    for name, paths in cards.items():
        if len(paths) > 1:
            errors.append(f"duplicate project cards for {name}: {len(paths)}")
        if name not in state_names:
            warnings.append(f"project card has no audited project state: {name}")
    if require_cards:
        for name in sorted(state_names):
            if name not in cards:
                errors.append(f"project state has no Memory Graph card: {name}")

    obsolete_patterns = (
        "*图谱增量*.json",
        "*Memory_Graph_delta*.json",
        "*MemoryGraph更新*.json",
        "*图谱变更*.json",
    )
    for pattern in obsolete_patterns:
        for path in projects_root.glob(f"**/输出文档/{pattern}"):
            errors.append(
                f"obsolete graph update artifact remains: {path.relative_to(workspace_root)}"
            )

    print(
        f"Audited {len(projects)} projects, {len(state_names)} states, "
        f"{sum(len(value) for value in cards.values())} cards; "
        f"excluded {len(excluded)} configured objects."
    )
    for warning in warnings:
        print(f"WARN: {warning}")
    if errors:
        print(f"FAILED with {len(errors)} error(s)")
        for error in errors:
            print(f"- {error}")
        return 1
    print("OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
