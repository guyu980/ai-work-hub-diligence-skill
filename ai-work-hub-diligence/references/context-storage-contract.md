# Context Object And Storage Contract v1

This contract keeps workflow semantics independent from storage. Local files,
Feishu/Lark, and future backends use the same object model and logical
collections; an adapter resolves each logical locator to a physical path,
document, folder, or database record.

## Logical Collections

Every durable context object may use these collections:

| Key | Content |
|---|---|
| `sources` | Original files, transcripts, agreements, and raw exports |
| `structured_context` | Parsed text, evidence ledgers, normalized cards, and machine state |
| `workflow_outputs` | Judgments, question lists, memos, and graph deltas |
| `actions_outcomes` | Actions, execution status, outcomes, and contribution facts |
| `governance` | Formal decisions, resource commitments, overrides, signatures, and payment confirmations |

The physical layout may differ. Semantic keys must not.

## Storage Profiles

### Local

The default project mapping is compatible with existing AI Work Hub folders:

```text
sources            -> 原始资料/
structured_context -> 解析文本/
workflow_outputs   -> 输出文档/
actions_outcomes   -> 输出文档/行动与结果/
governance         -> 输出文档/治理与确认/
```

Use workspace-relative paths in portable artifacts. Never publish a user's
absolute path as an organization-wide locator.

### Feishu/Lark

A typical object folder maps the same collections to:

```text
00_原始资料/
01_结构化Context/
02_Workflow输出/
03_行动与结果/
04_治理与确认/
```

Long-form material belongs in Drive or Docs. Current state and searchable
metadata may live in Base. Store tenant-specific folder tokens, Base IDs,
field IDs, and permission groups in a deployment manifest, never in this
public skill.

### Hybrid

Hybrid mode is allowed only when the object manifest declares one canonical
write target and the synchronization state. A local working copy and an
organization copy must not both silently claim to be current.

## Locator

Use a typed locator instead of a raw path assumption:

```json
{
  "backend": "local",
  "kind": "file",
  "uri": "项目/Example/原始资料/BP.pdf"
}
```

```json
{
  "backend": "feishu",
  "kind": "document",
  "uri": "https://example.feishu.cn/docx/xxx"
}
```

Supported backend values are `local`, `feishu`, `web`, and `other`.
Supported kinds are `file`, `folder`, `document`, `base_record`, and `url`.

## Context Package

Use `context-package/v1` to move work between runtimes or into an
organization context system. The package records:

- package identity, type, actor, runtime, time, and visibility;
- canonical context object identity;
- trigger and source locators;
- artifacts grouped by logical collection;
- optional current state, workflow outputs, graph delta, and proposed actions;
- an optional canonical writeback target.

Validate packages against `context-package.schema.json` before official
writeback. An external package is an input with provenance, not an automatic
formal decision or authority grant.

## Adapter Responsibilities

An adapter must:

1. Resolve logical collections to physical locators.
2. Verify caller access before reading or writing.
3. Preserve source, actor, version, visibility, and last-verified metadata.
4. Deduplicate by package ID and canonical object ID.
5. Return a receipt: accepted, accepted with gaps, needs confirmation, or rejected.
6. Never expand the caller's permissions.

Workflow reasoning and output schema must stay the same across adapters.
