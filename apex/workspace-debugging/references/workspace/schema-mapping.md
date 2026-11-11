# APEX Workspace Schema Mapping

Use this reference only to inspect or change APEX workspace-to-schema mappings. The schema must already exist and be approved for APEX use by the DB owner. Database user/schema creation, eligibility checks, privileges, quotas, and remediation belong to the DB skill.

For `APEX_INSTANCE_ADMIN` ownership, identity requirements, package signature checks, and API safety, read [instance-admin-api.md](instance-admin-api.md) first.

## Mapping Guardrails

- Map only an application-owned schema approved by the DB owner.
- Never map Oracle-maintained, APEX platform, ORDS runtime, DBA/admin, or shared service accounts, or personal developer accounts in production.
- Do not use `DBA_USERS`, privilege views, quota views, or generic database queries to select or validate a candidate here. Ask the DB skill to confirm that the schema is provisioned and suitable.
- Do not grant or revoke privileges from this skill. Do not use APEX-managed grant options as a shortcut for DB provisioning.

## Inspect Existing Mappings

Use supported APEX metadata to check which schemas are already mapped:

```sql
SELECT workspace_name,
       schema
FROM apex_workspace_schemas
WHERE workspace_name = UPPER(TRIM(:workspace_name))
ORDER BY schema;
```

Check installed columns if the target APEX release exposes a different shape. Do not query internal APEX repository tables.

## Add A Schema Mapping

Confirm the workspace and DB-approved schema name with the user. Check the installed `APEX_INSTANCE_ADMIN.ADD_SCHEMA` signature, then use only the APEX mapping arguments supported by that release:

```sql
BEGIN
    APEX_INSTANCE_ADMIN.ADD_SCHEMA(
        p_workspace => :workspace_name,
        p_schema    => :schema_name);
END;
/
```

Do not pass privilege-grant options. If the schema is not provisioned, approved, or usable, stop and hand that part to the DB skill. If `ADD_WORKSPACE` already created the mapping, verify it rather than adding it again.

## Remove A Schema Mapping

Schema mapping removal is an APEX metadata change. Inventory the target workspace and mappings, show the exact schema mapping to remove, then follow the confirmation and protocol requirements in [removal.md](removal.md). This removes the APEX mapping only; it does not drop a database user or objects.

## Boundary

Workspace-to-schema mapping and APEX metadata remain here. Database schema/user provisioning, grants, quotas, tablespaces, and schema migration belong to the DB skill. APEX application source or artifact inspection belongs to APEXlang.
