# SQLcl MCP fallback for MLE creation privileges

Use this narrow fallback only when the DB skill cannot be found and the reported APEX operation is `CREATE [OR REPLACE] MLE MODULE` or `CREATE [OR REPLACE] MLE ENV` failing with `ORA-01031`. Prefer the DB skill when available. This is not a generic database administration or arbitrary SQL workflow. The entry point, user choices, documentation comparison, authorization, and safe retry rules remain in [mle-grant-debug.md](mle-grant-debug.md).

## Connection and identity

1. Use SQLcl MCP, not APEX SQL Workshop. Discover saved connections if needed and let the user select the relevant connection with the question picker. If a connection is already active, follow the MCP tool's rule to ask before switching. Do not guess an alias, accept a preselected option as an answer, request passwords, or assume that an APEX browser session is a database login.
2. Immediately after connecting, follow the connector's required schema-information step with brief output and a narrowly scoped object-name filter. Check `SESSION_USER`, `CURRENT_USER`, `CURRENT_SCHEMA`, `ISDBA`, PDB and service. Verify that the selected development/test/production target and the application target match. Treat the application parsing schema, DDL execution identity, module owner and administrative connection as separate facts. Do not use `SYS` or `SYSDBA` for this fallback; a user-selected `SYSTEM` connection without `SYSDBA` can be used for database privilege work after verifying its PDB. This does not authorize Workspace administration APIs under `SYSTEM`.
3. Establish the relevant application schema and privilege-check identity from reliable installed-app evidence and, when needed, the user's explicit confirmation. If the recipient, PDB or execution context is unresolved, report the uncertainty and stop before granting. Ownership of an unrelated table or the name of an MCP connection is not proof of the historical DDL identity.

Read-only context query through MCP `sql_run`:

```sql
SELECT SYS_CONTEXT('USERENV','SESSION_USER') AS session_user,
       SYS_CONTEXT('USERENV','CURRENT_USER') AS current_user,
       SYS_CONTEXT('USERENV','CURRENT_SCHEMA') AS current_schema,
       SYS_CONTEXT('USERENV','ISDBA') AS is_dba,
       SYS_CONTEXT('USERENV','CON_NAME') AS con_name,
       SYS_CONTEXT('USERENV','SERVICE_NAME') AS service_name
FROM dual
```

SQLcl MCP may write its own SQL audit records. Do not log credentials, session identifiers, SQL bodies or application data in the redacted protocol.

## Read-only privilege checks

Use only the checks needed for the failing operation and installed release. First discover whether the database has the relevant privilege name:

```sql
SELECT name
FROM system_privilege_map
WHERE name IN ('CREATE MLE', 'CREATE ANY MLE', 'EXECUTE DYNAMIC MLE')
ORDER BY name
```

When connected as the actual relevant user, compare direct grants to the current session's enabled privileges. These queries describe the MCP session, not necessarily the historic APEX DDL context:

```sql
SELECT 'DIRECT_USER' AS source, privilege
FROM user_sys_privs
WHERE privilege IN ('CREATE MLE', 'CREATE ANY MLE', 'EXECUTE DYNAMIC MLE', 'CREATE PROCEDURE')
UNION ALL
SELECT 'ENABLED_SESSION', privilege
FROM session_privs
WHERE privilege IN ('CREATE MLE', 'CREATE ANY MLE', 'EXECUTE DYNAMIC MLE', 'CREATE PROCEDURE')
ORDER BY 1, 2
```

To check a different verified schema, a user-selected administrative connection with access to `DBA_SYS_PRIVS` and `DBA_ROLE_PRIVS` may inspect that schema, `PUBLIC` and its nested role grants. Substitute the exact database-verified schema name as a safely quoted SQL string literal; do not interpolate raw user input. These rows show grants and role paths, not whether roles were enabled or usable in a definer-rights execution context.

```sql
WITH role_tree AS (
  SELECT DISTINCT granted_role
  FROM dba_role_privs
  START WITH grantee = '<VERIFIED_SCHEMA>'
  CONNECT BY NOCYCLE PRIOR granted_role = grantee
), principals AS (
  SELECT '<VERIFIED_SCHEMA>' AS grantee FROM dual
  UNION SELECT 'PUBLIC' FROM dual
  UNION SELECT granted_role FROM role_tree
)
SELECT p.grantee, p.privilege, p.admin_option
FROM dba_sys_privs p JOIN principals g ON g.grantee = p.grantee
WHERE p.privilege IN ('CREATE MLE', 'CREATE ANY MLE', 'EXECUTE DYNAMIC MLE', 'CREATE PROCEDURE')
ORDER BY p.grantee, p.privilege
```

If the installed release and operation make a JavaScript language-object privilege relevant, the same `principals` CTE can be joined to `DBA_TAB_PRIVS` using `GRANTEE`, with `OWNER='SYS'`, `TABLE_NAME='JAVASCRIPT'` and `PRIVILEGE='EXECUTE'`. Oracle's database guide says that from update 23.9 this grant is no longer required to execute JavaScript in the user's own schema, whereas APEX 26.2 documentation still lists it. Do not grant it solely because a query returns no rows. Do not assume `EXECUTE DYNAMIC MLE` is required for stored-module creation. If dictionary access or the execution context is insufficient, report that limit rather than declaring a privilege absent.

## Minimal authorized grant and verification

Only when the user has authorized the repair and the missing right, exact recipient and target PDB have been established, use the user-selected administrative SQLcl MCP connection to apply the minimal grant required by the installed release and failing operation. For a confirmed missing own-schema creation privilege, the candidate is:

```sql
GRANT CREATE MLE TO <VERIFIED_SCHEMA>
```

`<VERIFIED_SCHEMA>` is a placeholder, not executable SQL. Use the exact verified database identifier, quoted safely according to Oracle identifier rules; never insert unchecked user input. Do not grant `ANY` privileges, a broad role, `ADMIN OPTION`, or unrelated rights. Follow tool-level approval and connection-switch rules. If the user requested diagnosis-only, no grants, or a separate go-ahead, report the candidate and wait without granting, retrying, or soliciting a contradictory approval.

If the selected administrator cannot inspect or issue the targeted grant, report the failed permission and stop. Do not grant additional administrative rights or silently change connections.

Only if the target release and the actual operation demonstrably require JavaScript language-object access and that grant is missing, the separate narrow candidate is `GRANT EXECUTE ON SYS.JAVASCRIPT TO <VERIFIED_SCHEMA>`. Do not bundle it with `CREATE MLE` by default. If a call specification, dynamic `DBMS_MLE` execution, cross-schema access, or another privilege needs repair, this fallback ends; use the DB skill or database owner for that separate work.

After the grant, repeat the applicable read-only check and report whether the intended grant is present. Retry only the affected MLE script if the user authorized the retry or asked for the objects to be created and the live installer can isolate it without rerunning unreviewed or destructive work. Use the existing APEX UI for that bounded retry; do not edit or reconstruct application source. Verify the object names and statuses and report any remaining errors. A grant or a valid object alone does not prove that the complete application works.

References: [Oracle MLE system privileges](https://docs.oracle.com/en/database/oracle/oracle-database/26/mlejs/system-and-object-privileges-required-working-javascript-mle.html), [MLE release changes](https://docs.oracle.com/en/database/oracle/oracle-database/26/mlejs/changes-this-release-oracle-javascript-developers-guide.html), and [APEX `MLE_LANGUAGES` settings](https://docs.oracle.com/en/database/oracle/apex/26.2/aeapi/APEX_INSTANCE_ADMIN.Available-Parameter-Values.html).
