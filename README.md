# AI Work Hub Diligence

[中文说明](README.zh-CN.md)

A Codex skill for continuous startup and investment diligence. Give it a BP, Feishu/Lark link, datapack, transcript, meeting note, financial model, or project update; it maintains one evolving judgment instead of producing disconnected reviews.

## What You Get

- A consistent project folder with original sources, parsed text, and outputs.
- One-time task naming as `Project <project>` when a new project is initialized.
- One running investment judgment and core todo.
- Separate dated question lists and cleaned meeting minutes.
- Source labels that distinguish verified facts, company claims, and open questions.
- Public and technical-team checks when they can change the decision.
- Practical valuation calibration using relevant listed and private comparables.
- Retrieval from and writeback to the optional private AI Work Hub Memory Graph.
- Automatic routing of reusable non-project interviews and thematic materials without creating false projects.
- Archiving and reopen gates for confirmed passes.

The default output is decision-oriented: `invest`, `continue`, `pause`, or `pass`, followed by the few reasons and next actions that matter.

## Depth And Effort

Go deep on the decisive business, technical and price questions, not every possible risk. Use attributed company figures for screening; request additional evidence only for a material uncertainty that can change the next action. Initial screens do not default to transaction audits, bank records or engineering tests. Important updates revisit the thesis; minor updates change only the affected content. Validate the changed project, reserving full-workspace audits for maintenance.

The skill is model-agnostic; select models in your runtime settings.

## Default Workflow

```text
New material
  -> classify project material versus a non-project knowledge source
  -> for a new project only, infer the name and rename the task
  -> locate or create the project
  -> archive and read the source
  -> compare with the current judgment
  -> run only relevant public/team/valuation checks
  -> update the same judgment and core todo
  -> sync reusable learning to Memory Graph
```

Task naming uses a dedicated title tool first, then the official Codex App Server
(`thread/name/set`) as a fallback, followed by title readback. Only report a
limitation after checking both routes. This is an initialization action, not a
title check on every update.

Default local structure:

```text
<workspace_root>/
  项目/
    <project>/
      原始资料/
      解析文本/
      输出文档/
        <project>_项目判断与todo.md
        <project>_项目状态.json
        01_问题清单/        # created on demand
        02_交流纪要/        # created on demand
        03_研究与分析/      # created on demand
        04_正式交付/        # created on demand
      工作区/               # optional reproducible process artifacts
    归档/
```

The output root holds only the running judgment and project state. New facts
update the running judgment instead of creating parallel "update" versions.
Other durable outputs are grouped by purpose. OCR pages, slide-build trees,
render caches, and similar reproducible artifacts belong in optional `工作区/`.

Feishu/Lark is normally an intake source, not a storage mode. For meeting records, the workflow reads both smart minutes and the original transcript/content whenever permissions allow.

An expert interview, course, podcast, meeting, or thematic document that is not owned by one company does not enter `项目/`. The `ai-work-hub-memory-graph` Skill lightly analyzes it under `知识来源/`; this Skill takes over only when it changes a specific project judgment.

## Install From GitHub

```bash
mkdir -p ~/Documents/skills-repos ~/.codex/skills
cd ~/Documents/skills-repos
git clone https://github.com/guyu980/ai-work-hub-diligence-skill.git
ln -s "$(pwd)/ai-work-hub-diligence-skill/ai-work-hub-diligence" \
  ~/.codex/skills/ai-work-hub-diligence
```

If the destination already exists, inspect it before replacing it. A Git clone plus symlink makes updates simple:

```bash
cd ~/Documents/skills-repos/ai-work-hub-diligence-skill
git pull --ff-only
```

Restart or reload Codex if the skill does not appear immediately.

Optional install check:

```bash
python3 ai-work-hub-diligence/scripts/check_install.py \
  --workspace-root "$HOME/Documents/AI Work Hub"
```

Initialize or validate a workspace project:

```bash
python3 ai-work-hub-diligence/scripts/init_project_state.py \
  --workspace-root "$HOME/Documents/AI Work Hub" \
  --project-name "Example" \
  --sector "AI-native applications"
python3 ai-work-hub-diligence/scripts/audit_workspace.py \
  --workspace-root "$HOME/Documents/AI Work Hub"
```

Preview and then apply a legacy-layout migration:

```bash
python3 ai-work-hub-diligence/scripts/migrate_project_layout.py \
  --workspace-root "$HOME/Documents/AI Work Hub" --all-projects
python3 ai-work-hub-diligence/scripts/migrate_project_layout.py \
  --workspace-root "$HOME/Documents/AI Work Hub" --all-projects --apply
```

The migrator preserves the two core files, classifies other outputs by purpose,
and rewrites local paths and relative links in text files. It reports links
embedded in Office files instead of rewriting those archives blindly.

For workspaces that also contain funds, system designs, or other non-company
objects under `项目/`, list only those objects in `.ai-work-hub.json`. The audit
still requires every included project to have the standard folders, one stable
judgment, and one project state.

## Use It

Initial review:

```text
Use $ai-work-hub-diligence to review this BP, create the project object, and give me an initial judgment plus a short question list.
```

Follow-up:

```text
Use $ai-work-hub-diligence. Read this Feishu meeting link, including the original transcript, then update the same judgment and core todo.
```

Interview preparation:

```text
Use $ai-work-hub-diligence to prepare a focused customer interview question list for this project.
```

Chat only:

```text
Use $ai-work-hub-diligence to assess this material, but do not create files.
```

For a non-project expert interview, use the companion Memory Graph Skill:

```text
Use $ai-work-hub-memory-graph to organize this expert interview. It is not owned by one project; preserve the original, create one core note, and route only reusable changes into the graph.
```

## Optional Memory Graph

Install the companion skill when you want new projects to recall prior projects, counterexamples, sector views, technical themes, valuation anchors, durable events, and high-signal people:

```bash
cd ~/Documents/skills-repos
git clone https://github.com/guyu980/ai-work-hub-memory-graph-skill.git
ln -s "$(pwd)/ai-work-hub-memory-graph-skill/ai-work-hub-memory-graph" \
  ~/.codex/skills/ai-work-hub-memory-graph
python3 ai-work-hub-memory-graph-skill/ai-work-hub-memory-graph/scripts/init_memory_graph.py \
  --workspace-root "$HOME/Documents/AI Work Hub"
```

The generated `Memory Graph/` is private workspace data. Do not upload it to this public repository.

## Feishu Setup

The skill does not ship tenant credentials. On first use, Codex follows [`feishu-cli.md`](ai-work-hub-diligence/references/feishu-cli.md) to install the CLI, authenticate the user, request the smallest required scopes, and verify the exact linked document.

## Repository Boundary

This public repository contains workflow instructions, scripts, schemas, and fictional sanitized examples. Never commit real BPs, transcripts, customer names, project judgments, Feishu tokens, or generated Memory Graph contents.

Contributions should arrive through pull requests. Repository owners review and merge them.

License: [MIT](LICENSE)
