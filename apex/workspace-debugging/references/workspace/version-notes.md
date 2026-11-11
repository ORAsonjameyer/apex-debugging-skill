# APEX Workspace Version Notes

Oracle APEX version is the primary version gate for this skill. Check the installed release before version-sensitive Workspace queries, APIs, or changes. Use the current official APEX documentation and the target instance's public metadata; do not infer API compatibility from the database release.

Primary references:

- [Oracle APEX 26.2 Administration Guide](https://docs.oracle.com/en/database/oracle/apex/26.2/aeadm/index.html)
- [Oracle APEX 26.2 Release Notes](https://docs.oracle.com/en/database/oracle/apex/26.2/htmrn/)
- [Oracle APEX 26.2 API Reference](https://docs.oracle.com/en/database/oracle/apex/26.2/aeapi/index.html)
- [Oracle APEX support status](https://www.oracle.com/apex/)

As of October 20, 2026, Oracle's published support table lists:

| Release | General Availability | Support Ends |
| --- | --- | --- |
| 26.2 | October 2026 | April 2028 |
| 26.1 | May 2026 | November 2027 |
| 24.2 | January 2025 | July 2027 |
| 24.1 | June 2024 | December 2026 |

These releases are currently supported. Release 23.2 support ended in May 2026; use it only for explicitly requested legacy compatibility or migration analysis. Recheck Oracle's support table when maintaining this skill.

For APEX 24.2 or 24.1, use that release's official documentation where behavior differs. Do not use older APEX documentation unless the user explicitly asks for legacy compatibility work.

## No Database Access

When no live database connection is available, ask for the installed or target APEX version before making version-sensitive recommendations. If the version is unknown, continue only with version-tolerant static guidance:

- Use APEX 26.2 as the default documentation baseline.
- Do not claim a specific view, column, package argument, or behavior exists in the target instance.
- Mark queries and API calls as pending verification against `APEX_RELEASE`, `APEX_DICTIONARY`, `ALL_TAB_COLUMNS`, and `ALL_ARGUMENTS`.
- Do not generate state-changing SQL or PL/SQL until the supported-version gate can be verified.

## Supported Version Gate

Run this gate before any MCP-backed APEX administration workflow. Continue only after the active connection has passed the APEX Admin Identity Gate in `apex/workspace-debugging/SKILL.md` and the installed version is supported.

```sql
SELECT version_no,
       CASE
           WHEN REGEXP_LIKE(version_no, '^(26\\.2|26\\.1|24\\.2|24\\.1)(\\.|$)')
           THEN 'SUPPORTED'
           ELSE 'UNSUPPORTED'
       END AS apex_admin_skill_support
FROM apex_release;
```

If `APEX_ADMIN_SKILL_SUPPORT` is `UNSUPPORTED`, stop before generating APEX administration SQL, monitoring queries, API calls, or Workspace changes.

Use this message:

```text
Unsupported APEX version detected: <VERSION_NO>. This Workspace skill supports APEX 26.2, 26.1, 24.2, and 24.1 as of October 2026. I will stop before generating version-sensitive APEX SQL or change steps for this environment.
```

Before generating version-sensitive SQL, check `APEX_RELEASE`, public view columns, and package arguments. `APEX_INSTANCE_ADMIN` may be a synonym for the installed package, so resolve it before checking arguments:

```sql
SELECT version_no
FROM apex_release;

WITH apex_instance_admin_target AS (
    SELECT owner,
           object_name AS package_name
    FROM all_objects
    WHERE object_name = 'APEX_INSTANCE_ADMIN'
      AND object_type = 'PACKAGE'
    UNION ALL
    SELECT table_owner AS owner,
           table_name  AS package_name
    FROM all_synonyms
    WHERE synonym_name = 'APEX_INSTANCE_ADMIN'
)
SELECT DISTINCT
       a.owner,
       a.package_name,
       a.object_name,
       a.argument_name,
       a.position,
       a.data_type,
       a.defaulted
FROM apex_instance_admin_target t
JOIN all_arguments a
  ON a.owner = t.owner
 AND a.package_name = t.package_name
WHERE a.object_name IN ('ADD_WORKSPACE', 'ADD_SCHEMA')
ORDER BY a.owner,
         a.package_name,
         a.object_name,
         a.position;
```

Use `ALL_TAB_COLUMNS`, `ALL_ARGUMENTS`, `APEX_DICTIONARY`, and the supported APEX version views before relying on a column or package parameter. Use the `APEX_INSTANCE_ADMIN` reference only for Workspace metadata APIs documented there; do not use it for instance-wide configuration.
