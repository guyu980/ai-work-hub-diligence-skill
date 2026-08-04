#!/usr/bin/env python3
"""Validate one AI Work Hub diligence project folder."""

from __future__ import annotations

import argparse
import json
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
def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-dir", required=True)
    args = parser.parse_args()
    project_dir = Path(args.project_dir).expanduser().resolve()
    errors: list[str] = []
    for name in ("原始资料", "解析文本", "输出文档"):
        if not (project_dir / name).is_dir():
            errors.append(f"missing directory: {name}")
    state_candidates = list((project_dir / "输出文档").rglob("*_项目状态.json"))
    if len(state_candidates) != 1:
        errors.append(f"expected one project state JSON, found {len(state_candidates)}")
        state = {}
    else:
        try:
            state = json.loads(state_candidates[0].read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            errors.append(f"invalid state JSON: {exc}")
            state = {}
    if state:
        if state.get("schema_version") != 2:
            errors.append("state schema_version must be 2")
        for key, allowed in ENUMS.items():
            if state.get(key) not in allowed:
                errors.append(f"invalid {key}: {state.get(key)!r}")
        if (
            state.get("intake_mode") == "historical_review"
            and state.get("historical_outcome") == "not_applicable"
        ):
            errors.append(
                "historical_review requires a historical_outcome"
            )
        if (
            state.get("intake_mode") == "historical_review"
            and state.get("review_status") == "not_applicable"
        ):
            errors.append("historical_review requires a review_status")
        if (
            state.get("intake_mode") == "live"
            and state.get("historical_outcome") != "not_applicable"
        ):
            errors.append(
                "live intake must use historical_outcome=not_applicable"
            )
        if not state.get("judgment_display"):
            errors.append("judgment_display is required")
    if errors:
        print(f"FAILED with {len(errors)} error(s)")
        for error in errors:
            print(f"- {error}")
        return 1
    print(f"OK: {project_dir.name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
