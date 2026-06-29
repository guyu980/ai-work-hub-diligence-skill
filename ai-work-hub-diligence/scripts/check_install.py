#!/usr/bin/env python3
"""Check a local ai-work-hub-diligence skill installation."""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from dataclasses import dataclass, asdict
from pathlib import Path


SKILL_NAME = "ai-work-hub-diligence"


@dataclass
class CheckResult:
    name: str
    status: str
    detail: str


def run_command(args: list[str], cwd: Path | None = None, env: dict[str, str] | None = None, timeout: int = 20) -> tuple[int, str]:
    try:
        completed = subprocess.run(
            args,
            cwd=str(cwd) if cwd else None,
            env=env,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            timeout=timeout,
        )
        return completed.returncode, completed.stdout.strip()
    except FileNotFoundError:
        return 127, f"command not found: {args[0]}"
    except subprocess.TimeoutExpired:
        return 124, f"command timed out after {timeout}s"


def add(results: list[CheckResult], name: str, status: str, detail: str) -> None:
    results.append(CheckResult(name=name, status=status, detail=detail))


def check_skill_folder(results: list[CheckResult], skill_dir: Path) -> None:
    skill_md = skill_dir / "SKILL.md"
    if skill_md.exists():
        add(results, "skill folder", "ok", f"found {skill_md}")
    else:
        add(results, "skill folder", "fail", f"missing {skill_md}")


def check_codex_link(results: list[CheckResult], skill_dir: Path) -> None:
    codex_home = Path(os.environ.get("CODEX_HOME", Path.home() / ".codex")).expanduser()
    link = codex_home / "skills" / SKILL_NAME
    if not link.exists() and not link.is_symlink():
        add(results, "codex symlink", "fail", f"missing {link}")
        return

    try:
        resolved_link = link.resolve()
        resolved_skill = skill_dir.resolve()
    except OSError as exc:
        add(results, "codex symlink", "fail", f"cannot resolve {link}: {exc}")
        return

    if resolved_link == resolved_skill:
        add(results, "codex symlink", "ok", f"{link} -> {resolved_skill}")
    else:
        add(results, "codex symlink", "warn", f"{link} points to {resolved_link}, expected {resolved_skill}")


def check_git(results: list[CheckResult], repo_root: Path) -> None:
    code, out = run_command(["git", "rev-parse", "--is-inside-work-tree"], cwd=repo_root)
    if code != 0 or out.strip() != "true":
        add(results, "git repo", "warn", "not inside a git work tree")
        return

    _, remote = run_command(["git", "remote", "get-url", "origin"], cwd=repo_root)
    code, status = run_command(["git", "status", "--short"], cwd=repo_root)
    if code == 0 and status:
        add(results, "git repo", "warn", f"repo has local changes; origin={remote or 'none'}")
    else:
        add(results, "git repo", "ok", f"repo clean; origin={remote or 'none'}")


def check_workspace(results: list[CheckResult], workspace_root: str | None) -> Path | None:
    if not workspace_root:
        add(results, "workspace root", "warn", "not provided; pass --workspace-root to check project folders and Feishu CLI")
        return None

    root = Path(workspace_root).expanduser().resolve()
    if root.exists() and root.is_dir():
        add(results, "workspace root", "ok", str(root))
    else:
        add(results, "workspace root", "fail", f"missing directory: {root}")
        return root

    project_dir = root / "项目"
    if project_dir.exists():
        add(results, "project folder", "ok", str(project_dir))
    else:
        add(results, "project folder", "warn", f"{project_dir} does not exist yet; the skill can create it on first project")
    return root


def lark_cli_path(workspace_root: Path) -> Path:
    return workspace_root / ".tools" / "node_modules" / ".bin" / "lark-cli"


def check_feishu(results: list[CheckResult], workspace_root: Path | None, verify_auth: bool, feishu_url: str | None) -> None:
    if workspace_root is None:
        add(results, "feishu cli", "warn", "workspace root unavailable; skip Feishu checks")
        return

    cli = lark_cli_path(workspace_root)
    home = workspace_root / ".home"
    if cli.exists():
        add(results, "feishu cli", "ok", str(cli))
    else:
        add(results, "feishu cli", "warn", f"missing {cli}; install @larksuite/cli in <workspace_root>/.tools")
        return

    if home.exists():
        add(results, "feishu home", "ok", str(home))
    else:
        add(results, "feishu home", "warn", f"missing {home}; login will create local auth state")

    env = os.environ.copy()
    env["HOME"] = str(home)

    if verify_auth:
        code, out = run_command([str(cli), "auth", "status", "--verify"], cwd=workspace_root, env=env, timeout=30)
        if code == 0:
            add(results, "feishu auth", "ok", "auth status verified")
        else:
            add(results, "feishu auth", "warn", compact(out))

    if feishu_url:
        code, out = run_command(
            [str(cli), "docs", "+fetch", "--doc", feishu_url, "--as", "user", "--format", "pretty"],
            cwd=workspace_root,
            env=env,
            timeout=45,
        )
        if code == 0 and out:
            add(results, "feishu fetch", "ok", "test link fetched successfully")
        else:
            add(results, "feishu fetch", "fail", compact(out) or "fetch failed with no output")


def compact(text: str, limit: int = 240) -> str:
    one_line = " ".join(text.split())
    if len(one_line) <= limit:
        return one_line
    return one_line[: limit - 3] + "..."


def print_human(results: list[CheckResult]) -> None:
    label = {"ok": "OK", "warn": "WARN", "fail": "FAIL"}
    for result in results:
        print(f"[{label.get(result.status, result.status.upper())}] {result.name}: {result.detail}")


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="Check local ai-work-hub-diligence installation.")
    parser.add_argument("--workspace-root", help="User workspace root, for example ~/Documents/AI Work Hub")
    parser.add_argument("--verify-feishu-auth", action="store_true", help="Run lark-cli auth status --verify")
    parser.add_argument("--feishu-url", help="Fetch a Feishu/Lark test document URL with user identity")
    parser.add_argument("--json", action="store_true", help="Print machine-readable JSON")
    args = parser.parse_args(argv)

    skill_dir = Path(__file__).resolve().parents[1]
    repo_root = skill_dir.parent
    results: list[CheckResult] = []

    check_skill_folder(results, skill_dir)
    check_codex_link(results, skill_dir)
    check_git(results, repo_root)
    workspace = check_workspace(results, args.workspace_root)
    check_feishu(results, workspace, args.verify_feishu_auth, args.feishu_url)

    if args.json:
        print(json.dumps([asdict(result) for result in results], ensure_ascii=False, indent=2))
    else:
        print_human(results)

    return 1 if any(result.status == "fail" for result in results) else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
