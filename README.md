# AI Work Hub Diligence

[中文说明](README.zh-CN.md)

**Continuous company diligence.** Connect BPs, datapacks, interviews and updates to one evolving investment judgment rather than disconnected reviews.

## Install And Update

Ask Codex to install the Skill from this repository and inspect any existing installation first. A Git checkout plus one symlink keeps personal and shared versions on the same source:

```bash
mkdir -p ~/Documents/skills-repos ~/.codex/skills
cd ~/Documents/skills-repos
git clone https://github.com/guyu980/ai-work-hub-diligence-skill.git
ln -s "$(pwd)/ai-work-hub-diligence-skill/ai-work-hub-diligence" ~/.codex/skills/ai-work-hub-diligence
```

Inspect an existing destination instead of overwriting it or creating duplicate Skills. Python scripts require Python 3.10+; Graph locking supports macOS/Linux. Reload Codex after installation. To update:

```bash
cd ~/Documents/skills-repos/ai-work-hub-diligence-skill
git pull --ff-only
```

The symlink uses the updated source directly. Keep the private workspace separate.

## Daily Use

Send a BP or project material, or ask:

```text
Use $ai-work-hub-diligence to review this BP, initialize the project and prepare an initial view and short questions.
Read this follow-up Feishu link, including the original transcript, and update the same judgment and core todo.
Prepare the next customer interview questions.
Analyze in chat only, without saving files.
```

Confirm an unknown private workspace path once. New projects use the task title `Project <name>`; subsequent updates do not recheck it. The project keeps originals, parsed text and outputs. The output root contains only the running judgment and state; dated questions, minutes, research and formal deliveries have purpose-based folders. Archive only after a confirmed pass.

Lead with the business thesis, strongest counterargument and next action: invest, continue, pause or pass. Attributed company figures are valid screening inputs. Team research, comparables and further verification scale with materiality, not a default transaction or engineering audit.

For Feishu, seek original text and relevant nested links, not smart minutes alone. The agent uses the [CLI guide](ai-work-hub-diligence/references/feishu-cli.md) to help install, authenticate, request necessary scopes and test access. Credentials are not included.

See [first-use setup and naming](ai-work-hub-diligence/references/project-setup.md) for dedicated tooling → official App Server → title readback, folder layout and maintenance. [Fictional cases](examples/virtual-cases/README.zh-CN.md) illustrate initial screening and iterative updates.

## How The Skills Connect

[Diligence](https://github.com/guyu980/ai-work-hub-diligence-skill) owns current company decisions; [Memory Graph](https://github.com/guyu980/ai-work-hub-memory-graph-skill) owns non-project sources and cross-project synthesis; [Deep Research](https://github.com/guyu980/ai-work-hub-deep-research-skill) owns explicitly requested formal studies. Companions are optional and installable separately. Authorized intelligence tasks discover; Skills do not schedule themselves.

This repository contains generic mechanisms, scripts and fictional examples only. Real projects, knowledge, reports, watchlists, delivery destinations and credentials remain private. Contribute via PR for maintainer review. Model selection belongs in runtime settings.

[Agent instructions](ai-work-hub-diligence/SKILL.md) · [MIT License](LICENSE)
