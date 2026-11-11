# APEX Workspace Removal

Use this reference for removing APEX Workspace metadata or an APEX schema mapping. Treat removal as destructive. Database users, schemas, objects, and tablespaces are owned by the DB skill and are never dropped by this workflow.

Before live inventory or removal, verify the supported APEX release, apply the APEX Admin Identity Gate, and inspect the installed `APEX_INSTANCE_ADMIN.REMOVE_WORKSPACE` or `REMOVE_SCHEMA` signature.

## Inventory

List the exact workspace, its schema mappings, APEX users, and applications before asking for confirmation. Use supported APEX views and inspect columns if their shape differs by release.

```sql
SELECT workspace_id,
       workspace,
       workspace_display_name,
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

```sql
SELECT workspace_name,
       user_name,
       is_admin,
       is_application_developer
FROM apex_workspace_apex_users
WHERE workspace_name = UPPER(TRIM(:workspace_name))
ORDER BY user_name;
```

If the workspace has applications, list them with `APEX_APPLICATIONS` and make the application impact explicit. This workflow inventories APEX metadata; it does not inspect or export application artifacts. Route artifact backup or review to APEXlang.

## Confirmation

Show the inventory and ask for a fresh exact confirmation in English for the current target. Do not accept a prior confirmation, implied approval, screenshot, `yes`, or `y`.

```text
To remove APEX workspace <WORKSPACE_NAME> and its listed APEX metadata, reply exactly: YES, I confirm that I want to remove this APEX workspace and its listed APEX metadata.
```

For schema mapping removal only, show the exact workspace and schema, then request a separate fresh confirmation for that mapping.

## Remove APEX Metadata Only

After the confirmation, use the supported APEX API with database dropping disabled:

```sql
BEGIN
    APEX_INSTANCE_ADMIN.REMOVE_WORKSPACE(
        p_workspace        => :workspace_name,
        p_drop_users       => 'N',
        p_drop_tablespaces => 'N');
END;
/
```

For a single schema mapping, use the installed `REMOVE_SCHEMA` signature. Removing the APEX mapping does not drop its database schema or objects.

Never set `p_drop_users` or `p_drop_tablespaces` to `Y` from this skill. If the user also wants database cleanup, stop and hand that work to the DB skill with its own identity and confirmation rules.
