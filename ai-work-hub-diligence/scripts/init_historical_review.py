#!/usr/bin/env python3
"""Initialize an invested, passed, or unknown historical-project review."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from datetime import date
from pathlib import Path


REVIEW_TEMPLATE = """# {name}｜历史项目复盘

- 复盘基准日: {review_as_of}
- 历史结果: {outcome}
- 历史决策日期: {decision_date}
- 当前复盘状态: pending

## 一句话重评

## 当时的信息集

只写在历史决策时已经可获得的事实、公司自述和推断。

## 当时的投资判断与关键假设

## 事后结果

只写历史决策之后才发生或才获得的信息。

## 决策质量与结果质量

分别评价判断过程是否合理，以及项目结果是否好；不要用结果倒推当时判断。

## Memory Graph 联想

- 相似项目:
- 反例项目:
- 相关赛道/技术主题:
- 估值锚点:

## 当前重评

- 当前投资判断:
- 建议打法:
- 价格判断:
- 判断置信度:

## 可复用经验

## 后续跟进触发器

## 当前核心 todo
"""


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--workspace-root", required=True)
    parser.add_argument("--project-name", required=True)
    parser.add_argument(
        "--outcome",
        required=True,
        choices=["invested", "pass", "unknown"],
    )
    parser.add_argument("--decision-date", default="")
    parser.add_argument("--review-as-of", default=str(date.today()))
    parser.add_argument("--sector", required=True)
    parser.add_argument("--project-dir")
    parser.add_argument(
        "--reopen",
        action="store_true",
        help="Keep a historical pass active for renewed diligence.",
    )
    args = parser.parse_args()
    workspace_root = Path(args.workspace_root).expanduser().resolve()
    if args.project_dir:
        project_dir = Path(args.project_dir).expanduser().resolve()
    elif args.outcome == "pass" and not args.reopen:
        project_dir = workspace_root / "项目" / "归档" / args.project_name
    else:
        project_dir = workspace_root / "项目" / args.project_name

    if args.outcome == "invested":
        decision = "invested"
        process_stage = "monitoring"
        judgment = "已投；历史项目复盘中"
    elif args.outcome == "pass" and not args.reopen:
        decision = "pass"
        process_stage = "archived"
        judgment = "不投 / pass；历史项目复盘"
    elif args.outcome == "pass":
        decision = "observe"
        process_stage = "screening"
        judgment = "历史曾 pass；现重新评估"
    else:
        decision = "observe"
        process_stage = "screening"
        judgment = "历史项目；待复盘"

    init_script = Path(__file__).with_name("init_project_state.py")
    subprocess.run(
        [
            sys.executable,
            str(init_script),
            "--workspace-root",
            str(workspace_root),
            "--project-name",
            args.project_name,
            "--project-dir",
            str(project_dir),
            "--sector",
            args.sector,
            "--intake-mode",
            "historical_review",
            "--historical-outcome",
            args.outcome,
            "--review-status",
            "pending",
            "--historical-decision-date",
            args.decision_date,
            "--review-as-of",
            args.review_as_of,
            "--decision",
            decision,
            "--process-stage",
            process_stage,
            "--judgment-display",
            judgment,
        ],
        check=True,
    )
    state_path = project_dir / "输出文档" / f"{args.project_name}_项目状态.json"
    state = json.loads(state_path.read_text(encoding="utf-8"))
    if args.outcome == "pass" and not args.reopen:
        state["project_status"] = "archived"
    state["running_judgment_path"] = (
        project_dir
        / "输出文档"
        / f"{args.project_name}_项目判断与todo.md"
    ).relative_to(workspace_root).as_posix()
    state_path.write_text(
        json.dumps(state, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    review_path = workspace_root / state["running_judgment_path"]
    review_path.write_text(
        REVIEW_TEMPLATE.format(
            name=args.project_name,
            review_as_of=args.review_as_of,
            outcome=args.outcome,
            decision_date=args.decision_date or "待确认",
        ),
        encoding="utf-8",
    )
    print(f"Historical review initialized: {project_dir}")
    print(f"Review document: {review_path}")
    print("Separate decision-time information from later outcomes in the review.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
