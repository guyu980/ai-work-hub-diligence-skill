# First-Use Project Setup

Read only for a new project, unknown workspace, naming correction or layout maintenance.

## Resolve Ownership And Path

Confirm an unknown workspace root, never a hardcoded personal path. Infer the canonical company name/alias from the input; ask only if a wrong project is a real risk. Reuse existing projects, including archived ones. A non-project interview or thematic source belongs in `知识来源/`; do not initialize or rename a company project for it.

```text
<root>/项目/<name>/
  原始资料/
  解析文本/
  输出文档/
    <name>_项目判断与todo.md
    <name>_项目状态.json
    01_问题清单/       # dated preliminary/interview questions; on demand
    02_交流纪要/       # dated cleaned Q&A/minutes; on demand
    03_研究与分析/     # reports, models and analysis; on demand
    04_正式交付/       # IC and other formal delivery; on demand
  工作区/              # reproducible process/render artifacts; on demand
<root>/项目/归档/<name>/
```

New material updates the one running judgment, not a parallel update file.

```bash
python3 <skill_dir>/scripts/init_project_state.py --workspace-root "<root>" --project-name "<name>" --sector "<user-defined sector>"
```

Read [project-state.md](project-state.md) before writing state. The initializer refuses a parallel judgment if a legacy running file exists; merge/rename it with link preservation first.

## One-Time Task Naming

When first creating a company project and its name is clear, rename the task to exactly `Project <项目名>` before broader analysis/setup. Use Chinese, English or a familiar abbreviation; no brackets, dates or stage suffix.

1. Use `set_thread_title` or equivalent dedicated tooling.
2. If unavailable/unsuccessful, use the [official Codex App Server](https://learn.chatgpt.com/docs/app-server): `thread/name/set` with `{"threadId":"<current_thread_id>","name":"Project <项目名>"}`.
3. Read back with a dedicated read tool or `thread/read` using `{"threadId":"<current_thread_id>","includeTurns":false}`; confirm `thread.name` exactly.

Use a trusted runtime/session thread ID, not a title guess. A local fallback is `codex app-server` over stdio with the same user's `CODEX_HOME`. For a new connection, send `initialize` with `clientInfo` (`name`, `version`), await response, then `initialized` before requests. Renaming a persisted thread does not need resume/new turns or direct session/database edits.

Report a concrete naming limitation only after checking both routes. A write response without matching readback is unconfirmed. Continue diligence if unavailable. No separate title state or subsequent title checks; rename again only for a user-corrected canonical name. Exclude industry work, batches, recurring reports and system maintenance.

## Maintenance Only

Optional `<root>/.ai-work-hub.json` can exclude explicitly identified fund/system directories and configure card requirements; it must not exempt normal company projects.

Use `audit_workspace.py` for an authorized full audit. Preview `migrate_project_layout.py --all-projects`, then add `--apply` for authorized legacy migration. Preserve linked text and report embedded Office links rather than rewriting archives blindly. Do not run either operation on each ordinary update.
