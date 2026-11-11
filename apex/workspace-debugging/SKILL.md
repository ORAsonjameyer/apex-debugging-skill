---
name: workspace-debugging
description: Oracle APEX Workspace administration, monitoring, and live browser triage. Diagnose MLE ORA-01031 with the DB skill or a narrow SQLcl MCP fallback; route application source and APEX Debug/Trace to APEXlang.
---

# Oracle APEX Workspace & Debugging

Use this skill for APEX Workspace lifecycle and user administration, existing DB-approved schema mappings, Workspace service settings, reports and health checks, and live browser triage of APEX applications. Load only the reference needed for the task.

Prefer the original APEXlang and DB skills for their respective application and database workflows whenever available. If either is unavailable, continue with the capabilities included here: bounded live browser triage and, for MLE creation `ORA-01031`, the narrow SQLcl MCP fallback. Explain which remaining work is outside those capabilities; do not claim that the fallback replaces either companion skill.

## Routing

- Workspace lifecycle, users, mappings, resource limits, and removal: use `references/workspace/`.
- Workspace service settings, requests, metadata management, and operations: use `references/workspace/workspace-service-admin.md`.
- Workspace dashboards, Monitor Activity, active sessions, and browser-based Workspace administration checks: start with `references/diagnostics/workspace-diagnostics.md` or `references/monitoring/workspace-monitor-activity.md`.
- Broad APEX Workspace status: use `references/monitoring/environment-healthcheck.md`.
- Live reproduction and browser-level investigation of an APEX application: use `references/diagnostics/live-browser-debugging.md`.
- Application symptom classification and bounded handoffs to APEXlang or DB: use `application/SKILL.md`; it reuses the existing Workspace monitoring and live-browser references. For MLE creation `ORA-01031`, follow `application/mle-grant-debug.md`; prefer the DB skill and use its narrow SQLcl MCP fallback only if the DB skill is unavailable.
- Workspace-level activity trends and Workspace administration reports: use the matching reference in `references/monitoring/`.
- Use the original APEXlang skill for application source/exports, component definitions and code-level behavior, `APEX_DEBUG_MESSAGES`, APEX Debug/Trace configuration and interpretation, import, validation, and application locking/working-copy workflows. APEX 26.2 file-level import and the `APEX_APPLICATION_ADMIN` lock/working-copy APIs are application tasks for APEXlang, even when used within a Workspace.
- Database accounts/schemas, grants, quotas, SQL/PLSQL, performance, ORDS, infrastructure, and database security belong to `db/SKILL.md`. The only local exception is the bounded MLE creation privilege fallback in `application/mle-privilege-fallback.md` when the DB skill cannot be found. In APEX 26.2 DB ownership includes instance-wide enablement and network ACL setup for Workspace-Level Network Access Control (`WEBSERVICE_USE_SCHEMA_ACL`).

The Workspace skill may provide Workspace name, APEX user, approved schema mapping, Workspace Activity context, and redacted live-browser observations before a handoff. Its browser triage observes runtime behavior in an existing session and does not duplicate APEXlang source, Debug/Trace, or artifact procedures. A visible MLE creation error is sufficient to start privilege investigation without waiting for APEXlang. Prefer the DB skill for database work; only the explicitly scoped MLE fallback may proceed without it. Use the companion skill's own identity and tool rules after a handoff.

### Hand Off Application Source And APEX Debug Work To APEXlang

When an application task involves source, component definitions, APEX Debug/Trace, `APEX_DEBUG_MESSAGES`, import, validation, application locking, or working copies, check the active skill catalog and use the original APEXlang skill if it is available. If it is absent from the catalog, check configured skill roots and any actual local skill paths already supplied or discovered in the session; inspect the real `SKILL.md` rather than assuming a sibling-repository path. Do not continue those tasks under Workspace guidance. If APEXlang cannot be found, say so plainly and ask the customer to install or activate it, or provide its existing local `SKILL.md` path. Do not copy its procedures into this skill. Pause that portion; independent Workspace work and live browser triage may continue. Prepare a short handoff summary with only Workspace context and observed browser/report facts.

Announce the owner and the action being handed over. An explicit user request for the relevant application or database diagnosis or repair already authorizes the corresponding handoff; do not ask the user to approve the skill switch again. The companion skill's rules and tool-level connection requirements still apply. Use these handoffs:

```text
APEXlang handoff: `apex/SKILL.md` owns this application source, export, import, component-definition, APEX Debug/Trace, and `APEX_DEBUG_MESSAGES` work. Continue within the user's authorized scope.
```

If the original APEXlang skill is unavailable, use a clear notice such as:

```text
Der originale APEXlang-Skill ist in dieser Umgebung nicht verfügbar. Bitte installiere oder aktiviere ihn oder nenne mir seinen vorhandenen lokalen SKILL.md-Pfad. Workspace-Prüfungen und eine begrenzte Live-Browser-Triage kann ich separat fortsetzen; die Quellcode-, Komponenten- und APEX-Debug-Message-Analyse pausiere ich bis dahin.
```

```text
DB skill handoff: `db/SKILL.md` owns this database, schema, privilege, SQL, ORDS, or infrastructure work. Continue within the user's authorized scope using the selected connection.
```

## Workspace Live-Work Gates

Before any live APEX Workspace query or API call through MCP:

1. Apply the APEX Admin Identity Gate below.
2. Check the installed APEX release using `references/workspace/version-notes.md`; stop if unsupported.
3. Check MCP availability using `references/monitoring/mcp-availability.md`.
4. Use documented public APEX views and APIs only. Check version-specific view columns and package arguments before use.

### APEX Admin Identity Gate

Use a confirmed APEX admin identity for Workspace APIs and metadata queries. A dedicated non-`SYS`/`SYSTEM` account already granted `APEX_ADMINISTRATOR_ROLE` is preferred. On Autonomous Database or APEX Service, use the service `ADMIN` identity only after the user confirms it is the APEX administration identity for this task.

Verify and show the active identity:

```sql
SELECT SYS_CONTEXT('USERENV', 'SESSION_USER') AS session_user,
       SYS_CONTEXT('USERENV', 'CURRENT_USER') AS current_user,
       SYS_CONTEXT('USERENV', 'ISDBA') AS is_dba
FROM dual;
```

Stop if the identity is `SYS`, `ISDBA = TRUE`, a parsing schema, workspace user, ORDS/APEX runtime account, generic deployment user, or unknown. If the APEX admin account or role needs to be created or repaired, hand that work to the DB skill.

`SYSTEM` without `SYSDBA` is an explicit exception for APEX-admin-scoped Workspace work. Show the verified identity, exact action and targets, and risks; continue only after a fresh reply of exactly `YES` in uppercase. Do not use this exception for database account creation, grants, or generic database work.

### Workspace Administration UI

For Workspace administration UI inspection in test or production, confirm the environment and require a fresh exact uppercase `YES` before attaching to or interacting with the browser. This confirmation is for read-only Workspace UI checks only.

For live application browser triage, follow `references/diagnostics/live-browser-debugging.md`. In test or production, establish the target and explicit read-only authorization before attaching. A structured environment selection that states this scope can provide that authorization. Keep the initial pass read-only; use the user's existing explicit authorization for any subsequent action and ask only when the action is not yet authorized. Route source/component diagnosis and APEX Debug/Trace work to APEXlang.

## Evidence And Protocols

- Static review of Workspace reports or screenshots does not need database access. State that boundary before starting.
- For customer-specific Workspace checks, ask once whether the relevant Monitor Activity, dashboard, Manage Service, active-session, or Workspace administration UI evidence is available. Route source/component analysis and APEX Debug/Trace evidence to APEXlang; route database/ORDS evidence to the DB skill. Live browser triage follows its dedicated reference.
- Report in chat by default unless the user requests a file or the selected workflow requires a protocol. Reuse an explicitly selected output location without asking again. Before writing a customer-specific report without a selected path, obtain the output directory or exact path. Downloads is available after a fresh `Ja` confirmation; this confirms only the output location.
- Before substantive live Workspace administration, state changes, or Workspace report review, read `references/diagnostics/workspace-protocol.md` and create/update the local protocol outside this skill tree. Confirm its output directory or exact file path first.
- Keep customer evidence, exports, reports, logs, screenshots, and protocols outside the skill tree and repository by default; honor an explicit user-selected location. Use redacted excerpts only; do not expose passwords, tokens, cookies, authorization headers, request bodies, item values, or unnecessary personal data.
- Never create database tables, triggers, packages, or other objects for Workspace protocols, logging, or instrumentation.

## Workspace Scope And Safety

- Use documented public APEX views and APIs; never query or update internal APEX repository objects.
- This skill may map an existing schema only after the DB owner has approved it. Schema/user provisioning, quotas, and general privilege checks and grants belong to the DB skill. If that skill is unavailable, only the MLE creation `ORA-01031` fallback may check and, when authorized, grant the narrowly verified privilege.
- APEX workspace users are distinct from database-login users, parsing schemas, runtime accounts, and database administrators.
- Do not create, alter, or drop application or customer-owned database objects from this skill, except for a user-authorized, isolated retry of the failed MLE creation script under the narrow fallback. Do not drop or recreate unrelated objects.
- Treat Workspace activity, session details, login reports, and APEX user information as sensitive. Limit live queries to the relevant workspace and time window.
- Do not expose session-state values or user-preference values during Workspace monitoring. Route application session-state, preference semantics, and authorization behavior to APEXlang; route database-enforced controls and network ACLs to the DB skill.
- Require an exact target and fresh confirmation before a Workspace service request, preference change, log purge, session purge, cache purge, user change, or application availability/build-status change. Follow the narrower workflow in the matching reference.
- Workspace removal requires the inventory and exact confirmation in `references/workspace/removal.md`. This skill removes APEX Workspace metadata only; it never drops database users, schemas, objects, or tablespaces.

## Workspace Planner

The planner is an optional aid for supported APEX Workspace inventory and change checklists. It does not connect to a database or execute SQL:

```bash
node apex/workspace-debugging/tools/workspace-admin-plan.mjs --action inventory --workspace <workspace-name>
```

## Documentation

Use official Oracle APEX documentation for the installed supported release. The primary 26.2 entry points are:

```text
https://docs.oracle.com/en/database/oracle/apex/26.2/aeadm/index.html
https://docs.oracle.com/en/database/oracle/apex/26.2/htmrn/
https://docs.oracle.com/en/database/oracle/apex/26.2/aeapi/index.html
```

Use `references/workspace/version-notes.md` for supported releases and the live version gate. Do not use older APEX documentation unless the user explicitly asks for legacy compatibility work.
