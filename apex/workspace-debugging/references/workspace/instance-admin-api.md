# APEX APIs for Workspace Administration

Use this reference for documented APEX APIs that create, inspect, or change Workspace metadata. It does not cover generic APEX instance configuration, application administration, or database administration.

Official source: Oracle APEX 26.2 API Reference, `APEX_INSTANCE_ADMIN`:

```text
https://docs.oracle.com/en/database/oracle/apex/26.2/aeapi/APEX_INSTANCE_ADMIN.html
```

Oracle documents execution by `SYS`, `SYSTEM`, and database users granted `APEX_ADMINISTRATOR_ROLE`. This skill still applies the APEX Admin Identity Gate from `apex/workspace-debugging/SKILL.md`; do not use `SYS` or `SYSDBA` for routine Workspace work.

## Workspace APIs

Use only the API needed for the requested Workspace task and load its matching workflow reference:

- `ADD_WORKSPACE`: create Workspace metadata. See [lifecycle.md](lifecycle.md).
- `REMOVE_WORKSPACE`: remove Workspace metadata. See [removal.md](removal.md).
- `ADD_SCHEMA`: map an existing, DB-approved schema to a Workspace. Do not provision database accounts or grant privileges here. See [schema-mapping.md](schema-mapping.md).
- `REMOVE_SCHEMA` and `GET_SCHEMAS`: inspect or change Workspace schema mappings. See [schema-mapping.md](schema-mapping.md).
- `GET_WORKSPACE_PARAMETER` and `SET_WORKSPACE_PARAMETER`: inspect or change Workspace-level settings. See [resource-governance.md](resource-governance.md).
- `UNLOCK_USER`: unlock an APEX-managed Workspace user only after confirming the exact user and Workspace. See [users-and-auth.md](users-and-auth.md).

Do not use this reference for instance-wide parameters, application IDs or metadata, saved application reports, subscriptions, instance administrators, cloud credentials, web entry points, email configuration, logs or retention, or Resource Manager settings. Use [live-browser-debugging.md](../diagnostics/live-browser-debugging.md) for interactive reproduction; route application source/component, APEX Debug/Trace, and artifact work to APEXlang, and database or instance-wide work to its owning skill.

## Verify Before Use

Before generating a call:

1. Verify the installed APEX version and supported-version gate.
2. Verify the active identity with the APEX Admin Identity Gate.
3. Resolve the installed package or synonym and inspect `ALL_ARGUMENTS` before relying on version-sensitive parameters.
4. Load the matching Workspace workflow.
5. For state changes, create or update the local protocol and require explicit confirmation of the exact Workspace and action.

`APEX_INSTANCE_ADMIN` can be a synonym for the installed package. Resolve the target before checking procedure arguments:

```sql
WITH apex_instance_admin_target AS (
    SELECT owner, object_name AS package_name
    FROM all_objects
    WHERE object_name = 'APEX_INSTANCE_ADMIN'
      AND object_type = 'PACKAGE'
    UNION ALL
    SELECT table_owner AS owner, table_name AS package_name
    FROM all_synonyms
    WHERE synonym_name = 'APEX_INSTANCE_ADMIN'
)
SELECT DISTINCT a.owner,
       a.package_name,
       a.object_name,
       a.overload,
       a.sequence,
       a.position,
       a.argument_name,
       a.in_out,
       a.data_type,
       a.defaulted
FROM apex_instance_admin_target t
JOIN all_arguments a
  ON a.owner = t.owner
 AND a.package_name = t.package_name
WHERE a.object_name = UPPER(:procedure_name)
ORDER BY a.owner, a.package_name, a.overload, a.sequence;
```

## Safety Review

Before sharing a runnable step, verify that it uses a documented API for the installed release, targets only the confirmed Workspace, and leaves database account/schema provisioning and application changes to their owning skills. Never query or update internal APEX repository tables directly.
