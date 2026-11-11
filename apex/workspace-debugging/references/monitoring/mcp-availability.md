# APEX Workspace MCP Availability Guard

Use this guard when a Workspace administration task needs live APEX views or APIs through MCP. This does not troubleshoot the DB client or provide generic database operations; those belong to the DB skill.

## Before APEX Live Work

- Confirm the MCP transport is available and the intended APEX admin connection is active.
- Verify the active identity before Workspace queries, including read-only checks.
- Confirm the requested Workspace and connection name when needed.
- Use the smallest available client-side check. Do not run DDL, generic DB diagnostics, or destructive SQL as a connectivity test.

## Stop Condition

If MCP reports a closed transport, unavailable server, or disconnected channel, stop the Workspace workflow. Do not infer APEX state from stale context, screenshots, prior results, or another UI session.

```text
APEX Workspace check paused: the MCP transport is unavailable, so I cannot safely verify or change Workspace state. I will resume after the APEX MCP channel is available.
```

An open APEX browser session does not prove the MCP channel is available:

```text
Your APEX browser session may still be connected, but this Workspace workflow needs the separate APEX MCP channel. I cannot use browser state as confirmation for an MCP-backed Workspace change.
```

## Recovery

After MCP becomes available again:

1. Repeat the availability check and verify the intended APEX admin identity.
2. Re-read the Workspace state relevant to the interrupted action.
3. For interrupted Workspace creation, inspect only the planned Workspace, its schema mappings, and its APEX Workspace users using [lifecycle.md](../workspace/lifecycle.md#interrupted-provisioning).
4. Classify each planned Workspace metadata item as present, missing, or unknown. Do not retry from assumptions.
5. Ask for fresh confirmation before removing any present Workspace metadata; use [removal.md](../workspace/removal.md).

Do not inspect database users, grants, tablespaces, customer objects, or application artifacts as part of Workspace recovery. Route those items to the DB skill or APEXlang.

## Minimal Workspace Re-Read

Use only the supported public APEX metadata relevant to the interrupted task. For example, verify the workspace row:

```sql
SELECT workspace_id,
       workspace,
       schemas,
       apex_developers,
       apex_workspace_administrators
FROM apex_workspaces
WHERE workspace = UPPER(TRIM(:workspace_name));
```

For schema mappings or APEX Workspace users, use the scoped verification queries in [lifecycle.md](../workspace/lifecycle.md). Apply the installed-version column check before using version-sensitive fields.

## Guardrails

- Do not continue after a transport failure because a previous query succeeded.
- Do not treat a browser APEX session as proof of MCP availability.
- Do not retry an interrupted Workspace create or removal without fresh Workspace metadata.
- Do not use this guard for database-client setup or database-state recovery.
