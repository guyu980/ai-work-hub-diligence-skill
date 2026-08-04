# Advanced Deployment

Read this reference only when the user explicitly requests organization storage,
cross-runtime handoff, migration, or a Codex-Feishu bridge. A Feishu document or
minutes link used as a source does not trigger this mode.

## Trigger Routing

- `Read this Feishu link`: use the normal local diligence workflow and
  `feishu-cli.md`.
- `Upload this memo to Feishu`: deliver the requested artifact; keep the local
  project canonical unless the user says otherwise.
- `Keep local and Feishu synchronized`, `hand this project to another Agent`,
  `use Feishu as the canonical store`, or `export the workspace`: activate the
  advanced storage contract below.

## Storage And Adapters

Read `context-storage-contract.md` and resolve one profile:

- `local`: the existing project folder remains canonical;
- `feishu`: an authorized Drive/Docs/Base object is canonical;
- `hybrid`: one side is explicitly canonical and synchronization state is
  visible.

Never infer organization IDs, folder tokens, Base fields, permission groups, or
write authority. Resolve them from the deployment manifest and the caller's
current permissions.

## Context Packages

Use `context-package/v1` only to move work across runtimes or into an
organization context system. Build and validate a package with:

```bash
python3 <skill_dir>/scripts/build_context_package.py \
  --workspace-root "<workspace_root>" \
  --project-dir "<project_dir>" \
  --trigger-summary "<why the handoff exists>" \
  --output "<output.json>"
python3 <skill_dir>/scripts/validate_context_package.py "<output.json>"
```

The package carries provenance, state, artifact locators, and reusable graph
changes. It is sourced input, not formal approval, expanded authority, or an
automatic investment decision. Upsert the existing canonical project rather
than creating a duplicate.
