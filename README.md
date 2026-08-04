# AI Work Hub Diligence Skill

[中文说明](README.zh-CN.md)

A Codex skill for iterative startup and project diligence.

It turns BPs, Feishu/Lark links, meeting notes, datapacks, transcripts, and follow-up materials into a running investment judgment, focused question lists, and an organized local project object. Organization storage and cross-agent portability are optional advanced modes.

## What It Does

- Creates or locates a project folder from a BP, Feishu link, or other project material.
- Attempts to title the Codex thread as `Project project name`, using the most recognizable English, Chinese, or Chinese short name.
- Archives source files and fetched Feishu content.
- Reads Feishu smart minutes and tries to fetch the original transcript/content.
- Maintains one running project judgment and todo file.
- Connects the project to a local AI Work Hub Memory Graph when available, including similar projects, counterexamples, sector views, technical themes, and valuation anchors.
- Generates separate question-list files for each diligence round.
- Performs lightweight public-information cross-checks.
- Researches identifiable technical founders, chief scientists, CTOs, algorithm leads, and other core technical people through public technical footprints such as papers, patents, GitHub, and Hugging Face, then keeps the assessment in the same running judgment file.
- Calibrates valuation using relevant public listed comps, private-market comps, and company-specific reverse checks when price matters.
- Gives a crisp investment recommendation: `投`, `继续推进`, `暂缓`, or `不投`.
- Updates the local private Memory Graph project card after a project view changes, if the Memory Graph skill is installed and the user has not requested chat-only work.
- Archives passed projects after user confirmation.
- Logs only judgment-changing, disputed, reusable, or high-stakes evidence instead of mechanically decomposing every source statement.
- Keeps routine valuation capture light; transaction and closing verification is reserved for ownership, return, legal, conflict, or decision-sensitive cases.
- Activates adapters and portable `context-package/v1` files only for explicit organization deployment or cross-agent handoff.

## Default Storage And Advanced Deployment

Normal use keeps the existing local `原始资料 / 解析文本 / 输出文档` layout. Reading a Feishu/Lark source link does not switch the project to Feishu storage.

Read [`advanced-deployment.md`](ai-work-hub-diligence/references/advanced-deployment.md) only when the user explicitly requests canonical Feishu storage, local/organization synchronization, cross-agent handoff, a Context Registry, migration, or a bridge. The public skill never hardcodes tenant-specific Feishu tokens, Base IDs, or a user's absolute path.

In advanced mode, export a local project for another runtime with:

```bash
python3 ai-work-hub-diligence/scripts/build_context_package.py \
  --workspace-root "$HOME/Documents/AI Work Hub" \
  --project-dir "$HOME/Documents/AI Work Hub/项目/Example" \
  --trigger-summary "Diligence state updated" \
  --output /tmp/example-context-package.json
python3 ai-work-hub-diligence/scripts/validate_context_package.py \
  /tmp/example-context-package.json
```

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

## Optional Memory Graph Integration

For cross-project recall, install the companion public skill:

```bash
cd ~/Documents/skills-repos
git clone https://github.com/guyu980/ai-work-hub-memory-graph-skill.git
cd ai-work-hub-memory-graph-skill
ln -s "$(pwd)/ai-work-hub-memory-graph" ~/.codex/skills/ai-work-hub-memory-graph
python3 ai-work-hub-memory-graph/scripts/init_memory_graph.py \
  --workspace-root "$HOME/Documents/AI Work Hub"
```

The generated `Memory Graph/` folder is private and should not be uploaded to GitHub. It lets this diligence skill retrieve prior projects, sector views, technical themes, and valuation anchors before judging a new project, then update the project card after the view changes.

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

The examples are fictionalized and anonymized. They show five common paths:

- BP looks promising, so continue diligence.
- BP has insufficient evidence or material over-claims, so stop active pursuit.
- BP looks promising, then multiple interviews and datapacks update the same running judgment.
- Follow-up materials make valuation a conditional go/no-go question rather than a static first-screen concern.
- A strong technical teaser requires benchmark scope checks, commercial proof, and valuation discipline.

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
- Keep generated `Memory Graph/` knowledge bases out of this repo; only reference the companion public skill.
- After changing the skill, run the skill validator before pushing.

## License

MIT. See [`LICENSE`](LICENSE).
