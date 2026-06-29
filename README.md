# AI Work Hub Diligence Skill

A Codex skill for iterative startup and project diligence.

It turns BPs, Feishu/Lark links, meeting notes, datapacks, transcripts, and follow-up materials into a running investment judgment, focused question lists, and an organized project folder.

## What It Does

- Creates or locates a project folder from a BP, Feishu link, or other project material.
- Archives source files and fetched Feishu content.
- Reads Feishu smart minutes and tries to fetch the original transcript/content.
- Maintains one running project judgment and todo file.
- Generates separate question-list files for each diligence round.
- Performs lightweight public-information cross-checks.
- Gives a crisp VC-style recommendation: `投`, `继续推进`, `暂缓`, or `不投`.
- Archives passed projects after user confirmation.

## Install

Clone this repo:

```bash
git clone <repo-url>
```

Link the skill into Codex:

```bash
ln -s "$(pwd)/ai-work-hub-diligence" ~/.codex/skills/ai-work-hub-diligence
```

If a skill with that name already exists, back it up first:

```bash
mv ~/.codex/skills/ai-work-hub-diligence ~/.codex/skills/ai-work-hub-diligence.backup
ln -s "$(pwd)/ai-work-hub-diligence" ~/.codex/skills/ai-work-hub-diligence
```

## First Use

Ask Codex to use the skill and provide a BP or Feishu/Lark link:

```text
Use $ai-work-hub-diligence to review this BP, create a project folder, and give an initial judgment plus a short question list.
```

For a follow-up meeting note:

```text
Use $ai-work-hub-diligence. Here is the Feishu minutes link; read the smart minutes and original transcript, then update the running judgment and core todo.
```

For an interview list:

```text
Use $ai-work-hub-diligence to prepare a founder interview question list for this project.
```

## Feishu/Lark Setup

See [`ai-work-hub-diligence/references/feishu-cli.md`](ai-work-hub-diligence/references/feishu-cli.md).

The skill expects a project-local `@larksuite/cli` installation where possible, plus user authorization for reading documents, minutes, wiki/drive files, and any write actions the user requests.

## Updating The Skill

This repo should be the source of truth.

After editing:

```bash
git status
git add ai-work-hub-diligence README.md .gitignore
git commit -m "Update diligence skill"
git push
```

Users can update with:

```bash
git pull
```

## Do Not Commit

Do not commit local project materials, Feishu auth state, tokens, `.home`, `.tools`, `node_modules`, private deal notes, or user-specific local overrides.
