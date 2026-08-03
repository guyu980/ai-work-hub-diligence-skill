# Feishu/Lark CLI Workflow

Use this reference when the user provides Feishu/Lark links or when Feishu access is not yet configured.

## Setup

Confirm the workspace root first:

```bash
cd "<workspace_root>"
```

Prefer a project-local CLI so auth state and dependencies are reproducible:

```bash
mkdir -p .tools
cd .tools
npm init -y
npm install @larksuite/cli
cd ..
```

Use a workspace-local CLI configuration directory. Do not override the process
`HOME`; the CLI also derives its encrypted credential-storage path from the
real user home, and mixing the two modes can make a valid token appear missing:

```bash
LARKSUITE_CLI_CONFIG_DIR="$PWD/.home/.lark-cli" ./.tools/node_modules/.bin/lark-cli doctor
LARKSUITE_CLI_CONFIG_DIR="$PWD/.home/.lark-cli" ./.tools/node_modules/.bin/lark-cli auth status --verify
```

If not logged in, start device login and ask the user to complete authorization:

```bash
LARKSUITE_CLI_CONFIG_DIR="$PWD/.home/.lark-cli" ./.tools/node_modules/.bin/lark-cli auth login --domain docs,drive,minutes,wiki,im
```

If the workflow needs to create or update Feishu docs, also request document write capability:

```bash
LARKSUITE_CLI_CONFIG_DIR="$PWD/.home/.lark-cli" ./.tools/node_modules/.bin/lark-cli auth login --domain docs,drive,minutes,wiki,im,markdown
```

If the CLI asks for app configuration, guide the user to provide the company-approved Lark app credentials or follow the organization's existing CLI setup. Do not invent app IDs, app secrets, or tokens.

## Permission Checks

Run:

```bash
LARKSUITE_CLI_CONFIG_DIR="$PWD/.home/.lark-cli" ./.tools/node_modules/.bin/lark-cli doctor
LARKSUITE_CLI_CONFIG_DIR="$PWD/.home/.lark-cli" ./.tools/node_modules/.bin/lark-cli auth status --verify
```

For specific scopes, use:

```bash
LARKSUITE_CLI_CONFIG_DIR="$PWD/.home/.lark-cli" ./.tools/node_modules/.bin/lark-cli auth check --scope "<scope names>"
```

### macOS credential-path preflight

On macOS, app/profile configuration and encrypted credentials are separate:

- profile/config: `<workspace_root>/.home/.lark-cli/config.json`
- encrypted credentials: `<real_user_home>/Library/Application Support/lark-cli/`

Older setups may have been created with an overridden `HOME`, leaving valid
encrypted credentials under
`<workspace_root>/.home/Library/Application Support/lark-cli/`. In that case,
running with only `LARKSUITE_CLI_CONFIG_DIR` can report `no_token` even though
the credential file still exists.

Before asking the user to log in again:

1. Confirm `config show` still identifies the expected app and user.
2. Check both credential directories for the matching `.enc` file without
   reading or printing its contents.
3. If the legacy file exists and the real-user directory is empty, repair the
   path with a secure link or migration and re-run `auth status --verify`.
4. Re-login only when no usable encrypted credential remains or server
   verification proves the refresh token is invalid.

Treat a successful verified fetch as the final check. Do not infer that a
missing token means the user changed the configuration.

Common capability gaps:

- Cannot read a document: request document/wiki/drive read permission and confirm the user has file access in Feishu.
- Cannot read minutes: request minutes permission and confirm the user can open the minutes page in Feishu.
- Cannot find the original transcript: fetch the smart minutes first, look for `文字记录`, `原文`, `妙记`, `docx`, or linked document URLs, then fetch those URLs.
- Cannot create or update docs: request document creation/write scopes. In a previously verified setup, successful doc creation required `docx:document:create` and `docx:document:write_only`; scope names may differ by CLI/app version, so confirm with the current CLI help and Feishu app settings.
- Search is weak or blocked: use the exact known URL instead of fuzzy Feishu search.

`doctor` may show local refresh warnings while `auth status --verify` still succeeds. Treat server-side token verification and actual fetch success as the final evidence.

## Fetch A Feishu Document

Fetch by URL or token:

```bash
LARKSUITE_CLI_CONFIG_DIR="$PWD/.home/.lark-cli" ./.tools/node_modules/.bin/lark-cli docs +fetch --doc "<url>" --as user --format pretty
```

For machine-readable output:

```bash
LARKSUITE_CLI_CONFIG_DIR="$PWD/.home/.lark-cli" ./.tools/node_modules/.bin/lark-cli docs +fetch --doc "<url>" --as user --format json
```

Save long outputs into the project folder before analyzing:

```bash
LARKSUITE_CLI_CONFIG_DIR="$PWD/.home/.lark-cli" ./.tools/node_modules/.bin/lark-cli docs +fetch --doc "<url>" --as user --format pretty > "项目/<项目名>/解析文本/<date>_飞书文档.md"
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
LARKSUITE_CLI_CONFIG_DIR="$PWD/.home/.lark-cli" ./.tools/node_modules/.bin/lark-cli minutes +search --query "<meeting title or company>" --as user --format pretty
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
LARKSUITE_CLI_CONFIG_DIR="$PWD/.home/.lark-cli" ./.tools/node_modules/.bin/lark-cli docs +create --help
LARKSUITE_CLI_CONFIG_DIR="$PWD/.home/.lark-cli" ./.tools/node_modules/.bin/lark-cli docs +update --help
```

Some CLI versions reject unsupported flags such as `--format`, and document create/update may work more reliably when the Markdown path is relative to the workspace root. Prefer minimal flags and validate with:

```bash
LARKSUITE_CLI_CONFIG_DIR="$PWD/.home/.lark-cli" ./.tools/node_modules/.bin/lark-cli docs +fetch --doc "<created doc url>" --as user --format pretty
```

Do not claim a Feishu document was created or updated until fetch validation confirms the title/body are non-empty.

## Troubleshooting

- If a command fails with `unknown flag`, rerun `--help` for that subcommand and use the minimal supported flags.
- If search returns nothing, fetch by known URL or ask the user for the exact Feishu link.
- If access is denied, ask the user to open the link in Feishu first and confirm they have permission; then re-run login or request the missing domain/scopes.
- If terminal output is long, redirect it to a file and analyze the saved file.
- If a link points to a spreadsheet or drive file, use the relevant `sheets`, `drive`, or `docs` command help instead of forcing `docs +fetch`.
