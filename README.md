# AI Work Hub Diligence Skill

[中文说明](README.zh-CN.md)

A Codex skill for iterative startup and project diligence.

It turns BPs, Feishu/Lark links, meeting notes, datapacks, transcripts, and follow-up materials into a running investment judgment, focused question lists, and an organized project folder.

## What It Does

- Creates or locates a project folder from a BP, Feishu link, or other project material.
- Attempts to title the Codex thread as `Project project name`, using the most recognizable English, Chinese, or Chinese short name.
- Archives source files and fetched Feishu content.
- Reads Feishu smart minutes and tries to fetch the original transcript/content.
- Maintains one running project judgment and todo file.
- Generates separate question-list files for each diligence round.
- Performs lightweight public-information cross-checks.
- Calibrates valuation using relevant public listed comps, private-market comps, and company-specific reverse checks when price matters.
- Gives a crisp investment recommendation: `投`, `继续推进`, `暂缓`, or `不投`.
- Archives passed projects after user confirmation.

## Quick Install

Clone the public repo:

```bash
mkdir -p ~/Documents/skills-repos
cd ~/Documents/skills-repos
git clone https://github.com/guyu980/ai-work-hub-diligence-skill.git
cd ai-work-hub-diligence-skill
```

Link the skill into Codex:

```bash
mkdir -p ~/.codex/skills
ln -s "$(pwd)/ai-work-hub-diligence" ~/.codex/skills/ai-work-hub-diligence
```

If a skill with that name already exists, back it up first:

```bash
mv ~/.codex/skills/ai-work-hub-diligence ~/.codex/skills/ai-work-hub-diligence.backup
ln -s "$(pwd)/ai-work-hub-diligence" ~/.codex/skills/ai-work-hub-diligence
```

Verify:

```bash
ls -la ~/.codex/skills/ai-work-hub-diligence
```

Start a new Codex thread or reload Codex if the skill does not appear immediately.

If cloning fails, check network access, GitHub availability, and whether Git is installed locally.

Optional install check:

```bash
python3 ai-work-hub-diligence/scripts/check_install.py --workspace-root "$HOME/Documents/AI Work Hub"
```

If Feishu/Lark is already configured, also verify auth:

```bash
python3 ai-work-hub-diligence/scripts/check_install.py \
  --workspace-root "$HOME/Documents/AI Work Hub" \
  --verify-feishu-auth
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

For chat-only review without creating files:

```text
Use $ai-work-hub-diligence to review this BP. Do not create files; just tell me the judgment in chat.
```

To archive a project the user has agreed not to pursue:

```text
Use $ai-work-hub-diligence. I agree we should stop active pursuit of this project; archive the project folder.
```

## Virtual Examples

See [`examples/virtual-cases/README.zh-CN.md`](examples/virtual-cases/README.zh-CN.md).

The examples are fictionalized and anonymized. They show three common paths:

- BP looks promising, so continue diligence.
- BP has insufficient evidence or material over-claims, so stop active pursuit.
- BP looks promising, then multiple interviews and datapacks update the same running judgment.

## Feishu/Lark Setup

See [`ai-work-hub-diligence/references/feishu-cli.md`](ai-work-hub-diligence/references/feishu-cli.md).

The skill expects a project-local `@larksuite/cli` installation where possible, plus user authorization for reading documents, minutes, wiki/drive files, and any write actions the user requests.

## Updating The Skill

This repo should be the source of truth.

After editing:

```bash
git status
git add ai-work-hub-diligence examples README.md README.zh-CN.md LICENSE .gitignore
git commit -m "Update diligence skill"
git push
```

Users can update with:

```bash
git pull
```

## Do Not Commit

Do not commit local project materials, Feishu auth state, tokens, `.home`, `.tools`, `node_modules`, private deal notes, or user-specific local overrides.

## Maintenance Notes

- Put core workflow rules in `ai-work-hub-diligence/SKILL.md`.
- Put Feishu/Lark CLI setup, permissions, and troubleshooting in `ai-work-hub-diligence/references/feishu-cli.md`.
- Put install and sharing instructions in the repo README files, not inside the skill folder.
- Put fictionalized onboarding examples in `examples/virtual-cases/`.
- Keep real project materials, private notes, auth state, and credentials out of this repo.
- After changing the skill, run the skill validator before pushing.

## License

MIT. See [`LICENSE`](LICENSE).
