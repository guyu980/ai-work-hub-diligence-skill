# Historical Review

Use this mode for an already invested, passed, or previously screened project. It uses the normal project folder, state, evidence ledger, project card, and retrieval path.

Initialize when needed:

```bash
python3 <skill_dir>/scripts/init_historical_review.py \
  --workspace-root "<workspace_root>" \
  --project-name "<项目名>" \
  --outcome invested|pass|unknown \
  --decision-date "YYYY-MM-DD"
```

Use `--reopen` for a prior pass that is being reconsidered. Preserve the original `historical_outcome`; update only the current process and decision fields.

Keep three time scopes explicit:

- `decision_time`: information available when the original decision was made.
- `post_outcome`: later evidence that explains what happened.
- `current`: evidence relevant to a new decision now.

The review should cover the original information set and assumptions, later results, decision quality, outcome quality, current re-rating, and reusable lessons. Do not use hindsight to upgrade weak original evidence.

For an invested project, separate old-position value from a new-money decision. Use final share price, Cap Table, and dilution when return math matters; do not infer ownership value from post-money alone.

