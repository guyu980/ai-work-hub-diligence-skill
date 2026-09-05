#!/usr/bin/env python3
"""Migrate diligence projects to the purpose-classified output layout."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
import hashlib
import json
import os
from pathlib import Path
import re
from urllib.parse import unquote, urlsplit, urlunsplit
import zipfile
import xml.etree.ElementTree as ET


OUTPUT_CATEGORIES = (
    "01_问题清单",
    "02_交流纪要",
    "03_研究与分析",
    "04_正式交付",
)
STANDARD_ROOT_DIRS = {"原始资料", "解析文本", "输出文档", "工作区"}
TEXT_SUFFIXES = {
    ".css", ".csv", ".html", ".ini", ".js", ".json", ".jsonl",
    ".md", ".py", ".sh", ".toml", ".ts", ".txt", ".xml", ".yaml",
    ".yml",
}
OFFICE_SUFFIXES = {".docx", ".pptx", ".xlsx"}
SKIP_PARTS = {".git", ".venv", "node_modules", "__pycache__"}

QUESTION_MARKERS = (
    "问题清单", "访谈问题", "访谈提纲", "追问清单", "补充尽调清单",
    "资料清单", "待确认事项", "问题优先级", "十问十答", "内部追问提示",
    "复测问题", "访谈计划", "参会提问", "questions",
)
COMMITTEE_MARKERS = (
    "立项会", "决策会", "投决报告", "立项报告", "investment memo",
    "ic memo", "ic报告", "演讲稿", "讲稿", "会上讲法",
)
MINUTES_MARKERS = ("纪要", "交流要点", "访谈整理", "访谈总结")
FORMAL_MARKERS = (
    "hia发布", "协议与交易文件", "专项基金排期", "飞书文档链接",
    "teaser", "executive_summary", "执行概要", "ppt页纲",
)
WORK_MARKERS = ("editppt", "_ocr", "render", "ppt169")

MARKDOWN_LINK_RE = re.compile(
    r"(?P<prefix>!?\[[^\]]*\]\()(?P<target>[^)\n]+)(?P<suffix>\))"
)
HTML_LINK_RE = re.compile(
    r"(?P<prefix>\b(?:href|src)=[\"'])(?P<target>[^\"']+)(?P<suffix>[\"'])",
    re.IGNORECASE,
)


@dataclass(frozen=True)
class Move:
    old: Path
    new: Path
    project_root: Path
    reason: str


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def relative(path: Path, root: Path) -> str:
    return path.relative_to(root).as_posix()


def load_exclusions(workspace_root: Path) -> set[str]:
    path = workspace_root / ".ai-work-hub.json"
    if not path.exists():
        return set()
    value = json.loads(path.read_text(encoding="utf-8"))
    return {str(item).strip("/") for item in value.get("exclude_project_dirs", [])}


def discover_projects(workspace_root: Path, include_excluded: bool) -> list[Path]:
    projects_root = workspace_root / "项目"
    excluded = set() if include_excluded else load_exclusions(workspace_root)
    projects: list[Path] = []
    for path in projects_root.iterdir():
        if not path.is_dir() or path.name.startswith(".") or path.name == "归档":
            continue
        if path.name not in excluded:
            projects.append(path)
    archive = projects_root / "归档"
    if archive.is_dir():
        for path in archive.iterdir():
            if not path.is_dir() or path.name.startswith("."):
                continue
            archive_name = path.relative_to(projects_root).as_posix()
            if path.name not in excluded and archive_name not in excluded:
                projects.append(path)
    return sorted(projects, key=lambda item: item.as_posix())


def category_for_name(name: str) -> str:
    lowered = name.lower()
    if any(marker in lowered for marker in COMMITTEE_MARKERS):
        return "04_正式交付"
    if "访谈纪要" in lowered and "后续核验问题清单" not in lowered:
        return "02_交流纪要"
    if any(marker in lowered for marker in QUESTION_MARKERS):
        return "01_问题清单"
    if any(marker in lowered for marker in MINUTES_MARKERS):
        return "02_交流纪要"
    if any(marker in lowered for marker in FORMAL_MARKERS):
        return "04_正式交付"
    if name.lower() == "pdf" or name.lower().endswith(".pptx"):
        return "04_正式交付"
    return "03_研究与分析"


def is_work_artifact(name: str) -> bool:
    lowered = name.lower()
    return (
        lowered in {"tmp", "临时图片", "editppt_runs", "预览", "__pycache__"}
        or lowered.startswith(("tmp_", "可编辑ppt"))
        or "graph_delta" in lowered
        or any(marker in lowered for marker in WORK_MARKERS)
    )


def work_destination(path: Path, output_dir: Path, project_root: Path) -> Path:
    parts = path.relative_to(output_dir).parts
    if parts and parts[0] in OUTPUT_CATEGORIES:
        parts = parts[1:]
    return project_root / "工作区" / Path(*parts)


def add_move(
    moves: list[Move],
    old: Path,
    new: Path,
    project_root: Path,
    reason: str,
) -> None:
    if old == new:
        return
    moves.append(Move(old.resolve(), new.resolve(), project_root.resolve(), reason))


def plan_project(project_root: Path) -> tuple[list[Move], list[Path]]:
    moves: list[Move] = []
    unresolved: list[Path] = []
    output_dir = project_root / "输出文档"
    project_name = project_root.name
    core_names = {
        f"{project_name}_项目判断与todo.md",
        f"{project_name}_项目状态.json",
    }

    if output_dir.is_dir():
        for child in sorted(output_dir.iterdir(), key=lambda item: item.name):
            if child.name.startswith(".") or child.name in core_names:
                continue
            if child.is_dir() and child.name in OUTPUT_CATEGORIES:
                continue
            if (
                child.is_file()
                and child.suffix.lower() == ".pdf"
                and "_bp_" in child.name.lower()
            ):
                destination = project_root / "原始资料" / child.name
                reason = "misfiled original BP"
            elif child.is_file() and "抽取文本" in child.name:
                destination = project_root / "解析文本" / child.name
                reason = "durable parsed text"
            elif is_work_artifact(child.name):
                destination = project_root / "工作区" / child.name
                reason = "process artifact"
            else:
                category = category_for_name(child.name)
                destination = output_dir / category / child.name
                reason = category
            add_move(moves, child, destination, project_root, reason)

        for category in OUTPUT_CATEGORIES:
            category_dir = output_dir / category
            if not category_dir.is_dir():
                continue
            selected_dirs: list[Path] = []
            for path in sorted(
                category_dir.rglob("*"), key=lambda item: len(item.parts)
            ):
                if any(parent in path.parents for parent in selected_dirs):
                    continue
                if path.is_dir() and is_work_artifact(path.name):
                    add_move(
                        moves,
                        path,
                        work_destination(path, output_dir, project_root),
                        project_root,
                        "nested process artifact",
                    )
                    selected_dirs.append(path)
                elif path.is_file() and path.suffix.lower() == ".py":
                    add_move(
                        moves,
                        path,
                        work_destination(path, output_dir, project_root),
                        project_root,
                        "build script",
                    )

    for child in sorted(project_root.iterdir(), key=lambda item: item.name):
        if child.name.startswith(".") or child.name in STANDARD_ROOT_DIRS:
            continue
        if child.is_file():
            category = category_for_name(child.name)
            add_move(
                moves,
                child,
                output_dir / category / child.name,
                project_root,
                f"root file -> {category}",
            )
            continue
        lowered = child.name.lower()
        if child.name == "Past":
            destination = project_root / "原始资料" / child.name
            reason = "legacy source directory"
        elif lowered.startswith("feishu_minutes"):
            destination = project_root / "解析文本" / child.name
            reason = "durable fetched transcript"
        elif is_work_artifact(child.name):
            destination = project_root / "工作区" / child.name
            reason = "process artifact"
        elif child.name in {"LPA协议"}:
            destination = output_dir / "04_正式交付" / child.name
            reason = "formal deliverable"
        elif child.name in {"条款整理", "投决报告审阅"}:
            destination = output_dir / "03_研究与分析" / child.name
            reason = "substantive analysis"
        else:
            unresolved.append(child)
            continue
        add_move(moves, child, destination, project_root, reason)
    return moves, unresolved


def validate_move_plan(moves: list[Move]) -> None:
    destinations: set[Path] = set()
    old_paths = {move.old for move in moves}
    for move in moves:
        if move.new in destinations:
            raise ValueError(f"duplicate destination in migration plan: {move.new}")
        destinations.add(move.new)
        if move.new.exists() and move.new not in old_paths:
            raise ValueError(f"migration destination already exists: {move.new}")
        for other in moves:
            if move is other:
                continue
            if move.old in other.old.parents or move.new in other.new.parents:
                raise ValueError(
                    "overlapping migration entries are not supported: "
                    f"{move.old} / {other.old}"
                )


def map_path(path: Path, moves: list[Move]) -> Path:
    path = path.resolve()
    for move in sorted(moves, key=lambda item: len(item.old.parts), reverse=True):
        if path == move.old:
            return move.new
        try:
            suffix = path.relative_to(move.old)
        except ValueError:
            continue
        return move.new / suffix
    return path


def old_location(current: Path, moves: list[Move]) -> Path:
    current = current.resolve()
    for move in sorted(moves, key=lambda item: len(item.new.parts), reverse=True):
        if current == move.new:
            return move.old
        try:
            suffix = current.relative_to(move.new)
        except ValueError:
            continue
        return move.old / suffix
    return current


def split_link_title(value: str) -> tuple[str, str]:
    match = re.match(r"^(.*?)(\s+[\"'][^\"']*[\"'])$", value.strip())
    return (match.group(1), match.group(2)) if match else (value.strip(), "")


def rewrite_target(
    value: str,
    old_file: Path,
    current_file: Path,
    workspace_root: Path,
    moves: list[Move],
) -> str:
    target, title = split_link_title(value)
    angled = target.startswith("<") and target.endswith(">")
    clean = target[1:-1] if angled else target
    if not clean or clean.startswith(("#", "mailto:", "data:", "javascript:")):
        return value
    parsed = urlsplit(clean)
    if parsed.scheme in {"http", "https"} or parsed.netloc:
        return value
    raw_path = unquote(parsed.path)
    if not raw_path:
        return value
    if raw_path.startswith("项目/"):
        old_target = workspace_root / raw_path
        workspace_style = True
        absolute_style = False
    else:
        candidate = Path(raw_path).expanduser()
        absolute_style = candidate.is_absolute()
        workspace_style = False
        old_target = candidate if absolute_style else old_file.parent / candidate
    new_target = map_path(old_target, moves)
    if new_target == old_target.resolve():
        if old_file == current_file:
            return value
        new_target = old_target.resolve()
    if workspace_style:
        new_path = relative(new_target, workspace_root)
    elif absolute_style:
        new_path = new_target.as_posix()
    else:
        new_path = Path(os.path.relpath(new_target, current_file.parent)).as_posix()
    rewritten = urlunsplit(("", "", new_path, parsed.query, parsed.fragment))
    if angled:
        rewritten = f"<{rewritten}>"
    return rewritten + title


def project_for_path(path: Path, projects: list[Path]) -> Path | None:
    for project in projects:
        try:
            path.relative_to(project)
        except ValueError:
            continue
        return project
    return None


def text_files(workspace_root: Path, projects: list[Path]) -> list[Path]:
    roots = [*projects]
    memory_root = workspace_root / "Memory Graph"
    if memory_root.is_dir():
        roots.append(memory_root)
    values: list[Path] = []
    for root in roots:
        for path in root.rglob("*"):
            if path.is_relative_to(memory_root / "00_索引"):
                continue
            if not path.is_file() or path.suffix.lower() not in TEXT_SUFFIXES:
                continue
            if any(part in SKIP_PARTS for part in path.parts):
                continue
            values.append(path)
    return sorted(set(values))


def literal_replacements(
    move: Move,
    workspace_root: Path,
    same_project: bool,
) -> list[tuple[str, str]]:
    replacements = [
        (move.old.as_posix(), move.new.as_posix()),
        (relative(move.old, workspace_root), relative(move.new, workspace_root)),
    ]
    if same_project:
        old_project_value = relative(move.old, move.project_root)
        if "/" in old_project_value:
            replacements.append(
                (old_project_value, relative(move.new, move.project_root))
            )
    return replacements


def rewrite_text_references(
    workspace_root: Path,
    projects: list[Path],
    moves: list[Move],
) -> tuple[list[Path], list[str]]:
    changed: list[Path] = []
    warnings: list[str] = []
    for path in text_files(workspace_root, projects):
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            warnings.append(f"non-UTF-8 text skipped: {relative(path, workspace_root)}")
            continue
        original = text
        old_file = old_location(path, moves)

        def markdown_replace(match: re.Match[str]) -> str:
            target = rewrite_target(
                match.group("target"), old_file, path, workspace_root, moves
            )
            return match.group("prefix") + target + match.group("suffix")

        def html_replace(match: re.Match[str]) -> str:
            target = rewrite_target(
                match.group("target"), old_file, path, workspace_root, moves
            )
            return match.group("prefix") + target + match.group("suffix")

        text = MARKDOWN_LINK_RE.sub(markdown_replace, text)
        text = HTML_LINK_RE.sub(html_replace, text)
        owner = project_for_path(path, projects)
        pairs: list[tuple[str, str]] = []
        for move in moves:
            pairs.extend(
                literal_replacements(
                    move,
                    workspace_root,
                    same_project=owner == move.project_root,
                )
            )
        ordered_pairs = sorted(
            set(pairs), key=lambda item: len(item[0]), reverse=True
        )
        placeholders: list[tuple[str, str]] = []
        for index, (old, new) in enumerate(ordered_pairs):
            token = f"@@AIWH_PATH_REWRITE_{index}@@"
            while token in text:
                token += "_"
            if old in text:
                text = text.replace(old, token)
                placeholders.append((token, new))
        for token, new in placeholders:
            text = text.replace(token, new)
        if text != original:
            path.write_text(text, encoding="utf-8")
            changed.append(path)
    return changed, warnings


def moved_file_pairs(moves: list[Move]) -> list[tuple[Path, Path]]:
    pairs: list[tuple[Path, Path]] = []
    for move in moves:
        if move.old.is_file():
            pairs.append((move.old, move.new))
        elif move.old.is_dir():
            for path in move.old.rglob("*"):
                if path.is_file():
                    pairs.append((path, move.new / path.relative_to(move.old)))
    return pairs


def office_reference_warnings(
    workspace_root: Path,
    projects: list[Path],
    moves: list[Move],
) -> list[str]:
    warnings: list[str] = []
    for project in projects:
        for path in project.rglob("*"):
            if not path.is_file() or path.suffix.lower() not in OFFICE_SUFFIXES:
                continue
            if not zipfile.is_zipfile(path):
                continue
            try:
                with zipfile.ZipFile(path) as archive:
                    targets: list[str] = []
                    for member in archive.namelist():
                        if not member.endswith(".rels"):
                            continue
                        try:
                            tree = ET.fromstring(archive.read(member))
                        except ET.ParseError:
                            continue
                        for relation in tree:
                            if relation.attrib.get("TargetMode") != "External":
                                continue
                            target = unquote(relation.attrib.get("Target", ""))
                            if urlsplit(target).scheme.lower() in {
                                "http", "https", "mailto"
                            }:
                                continue
                            targets.append(target.replace("\\", "/"))
            except (OSError, zipfile.BadZipFile):
                continue
            matched = False
            for move in moves:
                needles = [
                    move.old.as_posix(),
                    relative(move.old, workspace_root),
                ]
                if project == move.project_root:
                    project_value = relative(move.old, move.project_root)
                    if "/" in project_value:
                        needles.append(project_value)
                if any(needle in target for needle in needles for target in targets):
                    matched = True
                    break
            if matched:
                warnings.append(
                    "Office file may contain an old local path: "
                    f"{relative(path, workspace_root)}"
                )
    return warnings


def apply_moves(
    workspace_root: Path,
    projects: list[Path],
    moves: list[Move],
) -> tuple[list[Path], list[str]]:
    file_pairs = moved_file_pairs(moves)
    before_hashes = {old: sha256(old) for old, _ in file_pairs}
    for move in moves:
        move.new.parent.mkdir(parents=True, exist_ok=True)
        move.old.rename(move.new)
    changed, warnings = rewrite_text_references(
        workspace_root, projects, moves
    )
    changed_set = {path.resolve() for path in changed}
    for old, new in file_pairs:
        if not new.is_file():
            raise RuntimeError(f"moved file missing after migration: {new}")
        if new.resolve() not in changed_set and sha256(new) != before_hashes[old]:
            raise RuntimeError(f"file content changed unexpectedly: {new}")
    warnings.extend(office_reference_warnings(workspace_root, projects, moves))
    return changed, warnings


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--workspace-root", required=True)
    parser.add_argument("--project-dir", action="append", default=[])
    parser.add_argument("--all-projects", action="store_true")
    parser.add_argument("--include-excluded", action="store_true")
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()
    workspace_root = Path(args.workspace_root).expanduser().resolve()
    all_projects = discover_projects(workspace_root, args.include_excluded)
    if args.all_projects:
        selected = all_projects
    elif args.project_dir:
        selected = [Path(value).expanduser().resolve() for value in args.project_dir]
    else:
        parser.error("use --project-dir or --all-projects")
    unknown = [path for path in selected if path not in all_projects]
    if unknown and not args.include_excluded:
        parser.error(
            "project is not in the managed workspace set: "
            + ", ".join(str(path) for path in unknown)
        )

    moves: list[Move] = []
    unresolved: list[Path] = []
    for project in selected:
        project_moves, project_unresolved = plan_project(project)
        moves.extend(project_moves)
        unresolved.extend(project_unresolved)
    validate_move_plan(moves)

    mode = "APPLY" if args.apply else "DRY RUN"
    print(f"{mode}: {len(selected)} project(s), {len(moves)} move(s)")
    for move in moves:
        print(
            f"- {relative(move.old, workspace_root)} -> "
            f"{relative(move.new, workspace_root)} [{move.reason}]"
        )
    for path in unresolved:
        print(f"UNRESOLVED root entry: {relative(path, workspace_root)}")
    if unresolved:
        print(f"FAILED: {len(unresolved)} non-standard root entries need review")
        return 1
    if not args.apply:
        print("No files changed. Re-run with --apply after reviewing the plan.")
        return 0
    if not moves:
        print("No migration needed.")
        return 0

    changed, warnings = apply_moves(
        workspace_root, all_projects, moves
    )
    print(f"Rewrote references in {len(changed)} text file(s).")
    for warning in warnings:
        print(f"WARN: {warning}")
    print("Migration complete. Run project, workspace, and Memory Graph validation.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
