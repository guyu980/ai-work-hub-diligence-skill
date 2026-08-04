# AI Work Hub Diligence

[中文说明](README.zh-CN.md)

A Codex skill for continuous startup and investment diligence. Give it a BP, Feishu/Lark link, datapack, transcript, meeting note, financial model, or project update; it maintains one evolving judgment instead of producing disconnected reviews.

## What You Get

- A consistent project folder with original sources, parsed text, and outputs.
- One running investment judgment and core todo.
- Separate dated question lists and cleaned meeting minutes.
- Source labels that distinguish verified evidence, company claims, and open questions.
- Public and technical-team checks when they can change the decision.
- Practical valuation calibration using relevant listed and private comparables.
- Retrieval from and writeback to the optional private AI Work Hub Memory Graph.
- Archiving and reopen gates for confirmed passes.

The default output is decision-oriented: `invest`, `continue`, `pause`, or `pass`, followed by the few reasons and next actions that matter.

## Default Workflow

```text
New material
  -> locate or create the project
  -> archive and read the source
  -> compare with the current judgment
  -> run only relevant public/team/valuation checks
  -> update the same judgment and core todo
  -> sync reusable learning to Memory Graph
```

Default local structure:

```text
<workspace_root>/
  项目/
    <project>/
      原始资料/
      解析文本/
      输出文档/
    归档/
```

Feishu/Lark is normally an intake source, not a storage mode. For meeting records, the workflow reads both smart minutes and the original transcript/content whenever permissions allow.

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

## Advanced Deployment

Ordinary diligence needs only local project folders. Organization storage, hybrid synchronization, bridges, Context Registries, and portable Context Packages are documented in [`advanced-deployment.md`](ai-work-hub-diligence/references/advanced-deployment.md) and activate only when explicitly requested.

## Repository Boundary

This public repository contains workflow instructions, scripts, schemas, and fictional sanitized examples. Never commit real BPs, transcripts, customer names, project judgments, Feishu tokens, or generated Memory Graph contents.

Contributions should arrive through pull requests. Repository owners review and merge them.

License: [MIT](LICENSE)
