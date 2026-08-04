#!/usr/bin/env python3
"""Initialize a diligence project with one stable judgment and state file."""

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


JUDGMENT_TEMPLATE = """# {name} 项目判断与 todo

最近更新：{today}

## 当前一句话判断

待阅读首批材料后填写。

## 项目核心逻辑

## 已核验信息

## 公司/来源自述

## 团队技术背景与可信度

## 估值与融资

## 主要风险与待核验

## Memory Graph 联想

## 当前核心 todo

## 判断变化记录
"""


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
    parser.add_argument(
        "--project-status",
        choices=["active", "archived"],
        help="Defaults from whether --project-dir is under 项目/归档/.",
    )
    args = parser.parse_args()
    if "/" in args.project_name or "\\" in args.project_name:
        parser.error("project-name cannot contain path separators; use aliases")
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
    inferred_archived = "归档" in project_dir.parts
    values["project_status"] = (
        args.project_status
        or ("archived" if inferred_archived else "active")
    )
    if values["project_status"] == "archived":
        values["process_stage"] = "archived"
    for name in ("原始资料", "解析文本", "输出文档"):
        (project_dir / name).mkdir(parents=True, exist_ok=True)
    state_path = project_dir / "输出文档" / f"{args.project_name}_项目状态.json"
    if state_path.exists():
        raise SystemExit(f"Refusing to overwrite existing state: {state_path}")
    judgment_path = (
        project_dir / "输出文档" / f"{args.project_name}_项目判断与todo.md"
    )
    if not judgment_path.exists():
        legacy_candidates = sorted(
            (project_dir / "输出文档").glob("*项目判断*todo*.md")
        )
        if legacy_candidates:
            raise SystemExit(
                "A non-canonical running judgment already exists; rename it "
                f"to {judgment_path.name} before initialization: "
                f"{legacy_candidates[0]}"
            )
        judgment_path.write_text(
            JUDGMENT_TEMPLATE.format(name=args.project_name, today=str(date.today())),
            encoding="utf-8",
        )
    today = str(date.today())
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
        "running_judgment_path": relative(judgment_path, workspace_root),
        "created_at": today,
        "updated_at": today,
    }
    state_path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"Initialized project state: {state_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
