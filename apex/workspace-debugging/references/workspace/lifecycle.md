# APEX Workspace Lifecycle

Use this reference for APEX workspace inventory, creation, and post-create verification. Database account/schema provisioning and privileges belong to the DB skill; application creation and artifacts belong to APEXlang.

For `APEX_INSTANCE_ADMIN` ownership, identity requirements, package signature checks, and API safety, read [instance-admin-api.md](instance-admin-api.md) first. Use [version-notes.md](version-notes.md) for the supported-version gate.

## Before Creating A Workspace

Confirm:

- The installed APEX release is supported.
- Workspace name, description, and whether a deterministic workspace ID is needed.
- The primary schema already exists and has DB-owner approval for APEX use. Route schema provisioning or privilege questions to the DB skill; see [schema-mapping.md](schema-mapping.md) for mapping only.
- Whether to create the first APEX workspace administrator, developer, or end user. Use [users-and-auth.md](users-and-auth.md) for APEX user administration.
- Whether the environment is self-managed or a managed service with restricted instance administration.

For bulk workspace creation, agree on the count, naming method, primary schema, APEX user/contact policy, and exact confirmation scope before generating a plan.

## Identity And Version Gate

Before live APEX queries or changes, apply the APEX Admin Identity Gate in `apex/workspace-debugging/SKILL.md`, verify the installed APEX release, and run the MCP availability guard. Do not create a database account or grant `APEX_ADMINISTRATOR_ROLE` here; route missing identity setup to the DB skill.

## Create A Workspace

Use the Administration Services UI or the documented `APEX_INSTANCE_ADMIN.ADD_WORKSPACE` API. Check installed package arguments before generating a version-sensitive call. Supply an existing, DB-approved primary schema; this workflow creates only APEX workspace metadata and must not provision or grant database schemas.

```sql
BEGIN
    APEX_INSTANCE_ADMIN.ADD_WORKSPACE(
        p_workspace_id   => :workspace_id,
        p_workspace      => :workspace_name,
        p_primary_schema => :primary_schema);
END;
/
```

If the APEX API signature or available schema mapping does not match the target release, use the supported Administration Services UI or stop for version-specific verification. Do not use `SYS AS SYSDBA`, SQLcl setup procedures, or database-account creation from this skill.

For extra schemas, use the mapping-only steps in [schema-mapping.md](schema-mapping.md). For the first APEX workspace user, use [users-and-auth.md](users-and-auth.md).

## Verify APEX Metadata

After creation, verify the workspace and schema mapping using supported APEX views:

```sql
SELECT workspace_id,
       workspace,
       schemas,
       applications,
       apex_developers,
       apex_workspace_administrators
FROM apex_workspaces
WHERE workspace = UPPER(TRIM(:workspace_name));
```

```sql
SELECT workspace_name,
       schema
FROM apex_workspace_schemas
WHERE workspace_name = UPPER(TRIM(:workspace_name))
ORDER BY schema;
```

Verify APEX workspace users through `APEX_WORKSPACE_APEX_USERS` when the workflow creates or updates them. Do not query database account, privilege, or object views here.

## Interrupted Provisioning

If MCP or the workflow stops after a create step may have run, reconnect and inventory the planned APEX workspace, schema mappings, and APEX workspace users before retrying. Do not infer that a failed tool call rolled back.

Report each planned APEX metadata item as present, missing, or unknown. Ask for fresh confirmation before removing any present Workspace metadata; use [removal.md](removal.md). If the interrupted work includes database provisioning, hand that part to the DB skill. If it includes an application artifact, hand it to APEXlang.

## Application Boundary

Workspace setup ends after the Workspace, approved schema mapping, and requested APEX Workspace users are verified. For live browser reproduction, use [live-browser-debugging.md](../diagnostics/live-browser-debugging.md). For application generation, source/export inspection, component diagnosis, or APEX Debug/Trace analysis, announce the APEXlang handoff and continue under `apex/SKILL.md`.
