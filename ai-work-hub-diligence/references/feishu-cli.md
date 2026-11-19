# Feishu/Lark CLI Workflow

Use this reference when the user provides Feishu/Lark links or when Feishu access is not yet configured.

## Select the workspace entry point

Read the workspace instructions for the approved CLI, profile and account. Run commands from the workspace root. With the standard workspace launcher, use:

```bash
lark() { ./.tools/lark-workhub "$@"; }
```

For a new installation that uses the project-local CLI directly, install `@larksuite/cli` under `.tools/` if needed and use the configured profile. For example:

```bash
lark() { LARKSUITE_CLI_CONFIG_DIR="$PWD/.home/.lark-cli" ./.tools/node_modules/.bin/lark-cli "$@"; }
```

Select one entry point and keep it for diagnostics, login and fetching. A launcher may preflight credential writes before the upstream CLI runs. If it reports a read-only credential store, retry the **same** command in an authorized writable environment, or report the storage blocker. Switching executables, moving or linking credentials, or overriding `HOME` would bypass that check.

For an authentication or scope error, use `lark doctor`, `lark auth status --verify` or `lark auth check --scope "<scope names>"` as appropriate. A first login or confirmed expired authorization follows the organization's existing app, user identity and required scopes. Request write capability only for an authorized write. Confirm restored access by reading the intended source.

## Fetch Documents

Fetch by URL or token:

```bash
lark docs +fetch --doc "<url>" --as user --format pretty
```

For machine-readable output:

```bash
lark docs +fetch --doc "<url>" --as user --format json
```

Save long outputs into the project folder before analyzing:

```bash
lark docs +fetch --doc "<url>" --as user --format pretty > "项目/<项目名>/解析文本/<date>_飞书文档.md"
```

## Fetch Minutes And Original Transcript

When a link is a minutes/smart-minutes page:

1. Fetch the provided link if `docs +fetch` can read it.
2. Search or inspect the fetched content for the original transcript link, often labeled `文字记录`, `原文`, `妙记`, or a linked docx URL.
3. Fetch the original transcript separately.
4. Save both files:

```text
项目/<项目名>/解析文本/<date>_智能纪要.md
项目/<项目名>/解析文本/<date>_文字记录.md
```

If the minutes cannot be fetched by document URL, try minutes search using the meeting title or known date:

```bash
lark minutes +search --query "<meeting title or company>" --as user --format pretty
```

Then use any returned document/minutes links or tokens to fetch the content.

Never rely only on smart minutes when original transcript/content is available.

## Follow Nested Feishu Links

After fetching a Feishu document or smart minutes:

1. Search the fetched local file for Feishu URLs:

```bash
rg -n "https://[^ ]*feishu.cn|https://[^ ]*larksuite.com" "项目/<项目名>/解析文本"
```

2. For each relevant linked BP, datapack, transcript, appendix, or meeting note, fetch and save it.
3. Skip unrelated calendar, profile, emoji, or navigation links unless they affect the investment judgment.
4. Record inaccessible links in the running judgment document under `仍需底稿/访谈确认`.

## Create Or Update Feishu Docs

This diligence workflow normally writes local Markdown first. Create or update Feishu docs only when the user asks for shareable Feishu output.

Use the installed CLI help to confirm the exact flags:

```bash
lark docs +create --help
lark docs +update --help
```

Some CLI versions reject unsupported flags such as `--format`, and document create/update may work more reliably when the Markdown path is relative to the workspace root. Prefer minimal flags and validate with:

```bash
lark docs +fetch --doc "<created doc url>" --as user --format pretty
```

Read back the intended title, account/location and requested content before confirming delivery.

## Troubleshooting

- If a command fails with `unknown flag`, rerun `--help` for that subcommand and use the minimal supported flags.
- If search returns nothing, fetch by known URL or ask the user for the exact Feishu link.
- For access denial, distinguish file sharing, CLI scopes and credential storage using the selected entry point. If the original is inaccessible, state which source was readable and how that limits the analysis.
- If terminal output is long, redirect it to a file and analyze the saved file.
- If a link points to a spreadsheet or drive file, use the relevant `sheets`, `drive`, or `docs` command help instead of forcing `docs +fetch`.
