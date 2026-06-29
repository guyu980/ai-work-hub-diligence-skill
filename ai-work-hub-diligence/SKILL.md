---
name: ai-work-hub-diligence
description: Use for iterative startup or project diligence when the user provides a BP, teaser, datapack, model, Feishu/Lark document link, Feishu minutes link, transcript, interview note, public source, or any project-related material and expects automatic project-folder setup, source-first reading, public-information cross-check, Codex thread title naming, an initial or updated investment view, short question lists, founder/team/customer/supplier interview prep, running judgment/todo maintenance, or archiving of passed projects.
---

# AI Work Hub Diligence

## Core Contract

Treat this as a workflow, not a one-time judgment. A single BP, Feishu link, transcript, datapack, or project file should be enough to trigger the workflow: create or locate the project folder, archive the source, read the material, update the running judgment, and return a decision-oriented answer.

Keep one running project judgment/todo document per active project. Update that document as new materials arrive. Do not create a new judgment document for every round unless the user explicitly asks for a separate memo. Create new files for question lists, interview prep, regenerated minutes, and external-facing deliverables.

If the user explicitly says not to generate files, run the workflow in chat only and do not create or modify artifacts.

## First Run Setup

Before creating folders or writing artifacts in a new environment, confirm the user's workspace root. If a current workspace root is obvious, state it and ask for confirmation only when there is ambiguity. Use the confirmed root consistently.

Suggested default layout:

```text
<workspace_root>/
  项目/
    <项目名>/
    归档/
```

Do not hardcode a personal path. Ask: `你的项目工作区根目录放在哪里？例如 ~/Documents/AI Work Hub。`

If Feishu/Lark links are part of the workflow and the CLI is not yet set up, read `references/feishu-cli.md` and guide the user through installation, login, scope checks, and permission fixes.

If the user asks to verify a local installation, prefer running `scripts/check_install.py` from this skill folder before manual debugging.

## Project Folder Contract

When a new project material arrives:

1. Infer the project name from the BP, file name, Feishu title, company name, or user wording.
2. If the name is ambiguous, ask one short clarification before creating artifacts.
3. Create or locate:

```text
<workspace_root>/项目/<项目名>/
  原始资料/
  解析文本/
  输出文档/
```

4. Also ensure the archive container exists:

```text
<workspace_root>/项目/归档/
```

5. Save original files or fetched Feishu exports into `原始资料/`.
6. Save extracted text, OCR, Feishu smart minutes, original transcript, and public-source notes into `解析文本/`.
7. Save the running judgment file and generated deliverables into `输出文档/`.

Use one running judgment file, preferably:

```text
<workspace_root>/项目/<项目名>/输出文档/<项目名>_项目判断与todo.md
```

Recommended sections:

- 当前一句话判断
- 项目核心逻辑
- 已验证信息
- 公开交叉验证
- 主要疑点 / 风险
- 交流纪要 takeaways
- 当前核心 todo
- 判断变化记录

Create separate files for each question list, for example:

```text
<date>_初步问题清单.md
<date>_创始人访谈问题清单.md
<date>_客户访谈问题清单.md
<date>_供应商访谈问题清单.md
```

Do not overwrite prior question lists.

## Codex Thread Title

When the primary project name is clear, try to title the current Codex conversation:

```text
Project [<项目名>]
```

Use Codex thread-title tools when available. If the tool is unavailable, the current thread cannot be identified confidently, or the user asks not to rename the conversation, continue the diligence workflow without blocking.

Do not guess between multiple project names. Do not include judgment, valuation, customer names, financing terms, or other sensitive details in the thread title.

## Feishu Link Intake

When the user provides a Feishu/Lark link, default to source-first reading. Do not rely only on the AI-generated smart minutes.

Use the Feishu CLI workflow in `references/feishu-cli.md`.

Minimum behavior:

1. Fetch the provided link with user identity when possible.
2. If it is a smart-minutes/minutes page, locate and fetch the original transcript or linked document.
3. If the fetched document contains other Feishu links, follow the relevant links and save their contents too.
4. Save both smart minutes and original transcript/content into `解析文本/`.
5. State clearly if only smart minutes or only the original transcript could be accessed.

Long Feishu materials should be saved locally first, then read from the local files to avoid truncation.

## Source Intake

For initial BP or preliminary materials:

1. Read the exact source material before using public information.
2. Identify what is company-stated, what is evidenced by data, and what is still an assumption.
3. When company, founder, product, customer, or technology names are identifiable, perform a lightweight public-information cross-check before final judgment.
4. Produce an initial judgment plus a short preliminary question list.

For later datapacks, models, or updates:

1. Inspect the relevant sheets, tables, transcripts, or appended materials.
2. Extract only metrics that affect the investment judgment, such as revenue, users, customers, retention, gross margin, compute cost, backlog, pipeline, team, cap table, and scenario assumptions.
3. Recalculate the view when new data contradicts the prior view.
4. Update the same running judgment/todo document.

## Public Cross-Check

Use public information as validation and calibration, not as a substitute for source reading. Look for:

- Company basics: official site, registry/profile pages, financing history, product pages,备案/domain state, hiring pages, and historical positioning.
- Founder/team: school and employer history, public bios, LinkedIn/Google Scholar/personal pages, GitHub, patents, papers, conference talks, and prior startups.
- Technology proof: papers, arXiv, model cards, Hugging Face/GitHub repos, benchmarks, demos, patents, and reproducible evaluation details.
- Commercial proof: customer announcements, case studies, procurement/tender records, customer press releases, app/store traffic, and evidence that logos represent real usage or paid contracts.
- Industry calibration: comparable companies/products, mainstream technical route, customer purchasing behavior, pricing or cost benchmarks, and whether claimed growth or margin is plausible.

When public evidence is thin, stale, inconsistent, or only company-stated, say so explicitly. Treat strong private claims such as `全球前三`, huge orders, top customer logos, famous-school/lab affiliations, or breakthrough model performance as verification items.

## Decision Standard

Default to an investment time-allocation lens. Lead with one of:

- `投`
- `继续推进`
- `暂缓`
- `不投`

If the evidence points to weak founder-market fit, weak fit with the user's investment theme, poor valuation discipline, or a story that relies more on financing narrative than verified traction, say `不投` or `move on` directly.

For AI investment work, first test whether the company is truly AI-native and relevant to mainstream AI investor logic.

Real AI thesis fit:

- AI-native team
- proprietary product or technical insight
- strong workflow or data loop
- self-driven customer pull
- low-friction repeatability
- measurable AI ROI

Adjacent or narrative fit:

- traditional software, SI, channel, government-resource, or industrial digitization company using AI/Agent language without clear AI-native product advantage

If a project is only an adjacent or narrative fit for an explicitly AI-focused investor, default to `不投 / move on` unless there is unusually strong verified commercial traction at an attractive valuation.

Use `继续推进` when evidence is directionally attractive and the next diligence step can realistically confirm a live investment decision. Use `暂缓` only when a key blocker should stop normal deal-process time until resolved.

Treat `领投`, `跟投`, `小额option`, `小仓位`, and `分阶段投` as sizing or structure recommendations after the judgment, not as headline judgment categories.

## Workflow

### 1. Initial BP Review

When the user first sends a BP, teaser, deck, or early materials:

1. Create or locate the project folder unless the user says no files.
2. Archive the source material.
3. Extract/read the source deeply enough to support a view.
4. Run a lightweight public cross-check.
5. Update the running judgment document if writing artifacts.
6. Return:
   - 初步判断: lead with `投`, `继续推进`, `暂缓`, or `不投`.
   - 公开交叉验证: summarize the most important public signals and mismatches.
   - 初步问题清单: around 6-10 core questions only.
   - 下一步建议: a small number of actions, including sizing or structure only after the investment judgment is clear.

Keep the first question list focused. Prioritize questions that decide whether the deal deserves more time.

### 2. Follow-Up Material Updates

When the user later provides a datapack, Feishu note, transcript, customer call, founder update, or other project material:

1. Save/fetch the new source.
2. Read the new material from source.
3. Record the core takeaways from this round.
4. Refresh the public cross-check when the new material introduces new companies, founders, customers, technical claims, patents, papers, benchmarks, financing claims, or commercial claims.
5. Update the same running project judgment/todo document.
6. Explicitly state what changed versus the prior view.
7. Keep current todo to 3-5 core items.

Do not create a long todo list. Keep only actions that matter for deal progress.

### 3. Interview Question Lists

When the user asks for founder, core team, customer, supplier, FA, counsel, or other counterparty questions:

1. Tailor the list to that interviewee.
2. Focus on unresolved gating issues.
3. Create a separate question-list file if writing artifacts.
4. Keep company-facing wording polite and preparation-oriented.

For external-facing versions, avoid internal challenge language such as `红灯`, `必须拿到`, or overtly accusatory phrasing. Prefer `请协助说明`, `希望进一步了解`, and `可否补充`.

### 4. Meeting Note Regeneration

When the user asks to regenerate minutes from Feishu original content:

1. Fetch and save the original transcript/content, not only the smart minutes.
2. Preserve the original question-and-answer structure as much as possible.
3. Clean up order, speaker logic, and wording for readability.
4. Summarize moderately, but do not abstract away important factual detail.
5. Separate `问题`, `答复`, and `补充判断 / 待确认` when helpful.
6. Keep the output traceable to the original conversation.

### 5. Pass And Archive

If the recommendation is `不投` or `move on`, do not archive automatically. Wait for the user to agree that the project is passed or ask to archive it.

When the user agrees to pass:

1. Move the project folder from:

```text
<workspace_root>/项目/<项目名>/
```

to:

```text
<workspace_root>/项目/归档/<项目名>/
```

2. If the archive target already exists, ask before merging or create a dated folder such as `<项目名>_archived_<date>`.
3. Leave active projects directly under `<workspace_root>/项目/`.
4. In the final response, state the archive path.

## Output Style

For internal diligence:

- Be concrete about `投不投`, `为什么`, `还差什么`, and whether the next action is `继续推进`.
- Be willing to say `不投` as the headline when that is the real judgment.
- Give a valuation range, comfortable entry point, and suggested sizing or structure when material.
- Separate `BP自述`, `公开可验证`, `公开未找到`, and `仍需底稿/访谈确认` when the distinction affects the judgment.
- Separate `好项目且值得推进`, `好项目但价格贵`, `方向好但项目不行`, `项目可赚钱但不适合本基金`, and `完全不该花时间`.

For question lists:

- Keep initial lists short.
- Split by theme only when it improves usability.
- Write questions that can be used directly in the next conversation.

For updates:

- Lead with new takeaways.
- Then state how the view changed.
- End with only the core todo.

## Quality Checks

Before finishing, check:

1. The workspace root and project path are clear before writing artifacts.
2. A new BP, Feishu link, or material created or located a project folder unless the user requested chat-only work.
3. The answer is grounded in the user's actual BP, datapack, Feishu content, or transcript.
4. Feishu-linked work used both smart minutes and original content when possible.
5. Relevant nested Feishu links were followed or listed as inaccessible.
6. Identifiable companies, founders, products, customers, technical claims, and industry positioning received a lightweight public cross-check when web access is available.
7. The initial question list is not overbuilt.
8. The latest judgment distinguishes prior view from updated view.
9. The todo list is short and action-oriented.
10. One running judgment/todo document is maintained for the active project.
11. Each new question list is saved as a separate file when artifacts are generated.
12. External-facing wording is polite and sendable.
13. For investment screening, the answer gives a crisp recommendation and does not default to `继续看` when evidence already supports `不投 / move on`.
14. The Codex thread title is set to `Project [<项目名>]` when the project name is clear and thread-title tooling is available.
15. Passed projects are archived only after user confirmation.
