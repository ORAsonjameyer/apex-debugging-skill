# APEX Workspace & Application Triage — Cheat Sheet V6

Visual one-pager: [PNG](apex-workspace-application-triage-v6.png). Operational details: [Application triage instructions](../apex/workspace-debugging/application/SKILL.md).

**Workspace administration, monitoring, health checks, and bounded live browser triage.** Application source and APEX Debug/Trace belong to the original APEXlang skill; database and ORDS diagnosis belongs to the DB skill.

## What the Workspace Skill Covers

- **Workspace administration:** Workspace lifecycle, APEX Workspace users/groups, approved schema mappings, resources, Manage Service settings and service requests.
- **Workspace monitoring:** dashboards, Monitor Activity, login attempts, sessions, application-error presence, weighted page-performance reports, activity trends, and Workspace AI-service utilization.
- **Health checks:** assess Workspace administration evidence only; report `GREEN`, `AMBER`, `RED`, or `UNKNOWN` with the checked scope and evidence limits.
- **Live browser triage:** reproduce a reported user journey in an existing signed-in session; observe visible behavior, available console messages, and redacted request metadata.
- **Application symptom routing:** classify page, submit, AJAX, JavaScript, REST, performance, or access symptoms and prepare a minimal handoff.
- **MLE grant debugging:** includes `ORA-01031` when an APEX application import executes MLE DDL. Capture the import path, failing DDL, and distinct APEX user, parsing schema/object owner, and database execution identity. APEXlang owns the import artifact/path; DB owns effective privilege checks and grants. See [MLE grant debugging](../apex/workspace-debugging/application/mle-grant-debug.md).

## Route by Owner

| Workspace skill | Original APEXlang skill | DB skill |
| --- | --- | --- |
| Workspace accounts/groups, service settings/requests, dashboards, reports, health check, session/cache operations, and bounded browser reproduction | Application source/components, APEXlang definitions, APEX Debug/Trace, `APEX_DEBUG_MESSAGES`, imports, validation, locks, working copies, and application changes | Database accounts/schemas/privileges, including MLE grants and `ORA-01031`, SQL and database performance, ORDS, network ACLs, and infrastructure |

The Workspace skill can establish that an application error or performance symptom is present. It does not establish the source-code or database root cause.

## Safety Gates

- **Identity:** use a confirmed APEX administrator identity for Workspace APIs. Never use `SYS` or `SYSDBA`; `SYSTEM` is a narrowly scoped exception requiring verified identity and a fresh exact uppercase `YES`.
- **Live UI:** for test or production, confirm the target and read-only scope with a fresh exact uppercase `YES`. Confirm any action with side effects separately.
- **Privacy:** do not request or expose passwords, cookies, tokens, session IDs, request/response bodies, item values, or unredacted HAR files.
- **Evidence:** keep protocols and customer artifacts outside the skill tree. Static review of supplied Workspace reports or screenshots does not require database access.

## APEX 26.2 Baseline

As of **November 2, 2026**, Oracle lists APEX **26.2, 26.1, 24.2, and 24.1** as supported. APEX 23.2 support ended in May 2026. See [Oracle's APEX support table](https://www.oracle.com/apex/).

APEX 26.2 adds file-level APEXlang import and application lock/working-copy APIs; these remain APEXlang workflows. Workspace-Level Network Access Control uses the instance parameter `WEBSERVICE_USE_SCHEMA_ACL`; configuration and database ACL work route to DB. See [APEX 26.2 New Features](https://docs.oracle.com/en/database/oracle/apex/26.2/htmrn/new-features.html).

## Keep Live Browser Triage

Use the existing [Live APEX Browser Debugging](../apex/workspace-debugging/references/diagnostics/live-browser-debugging.md) procedure for bounded UI, console, and request-metadata observations. It does not inspect source, enable or analyze APEX Debug/Trace, or replace APEXlang/DB. When APEXlang is unavailable, pause source-level work and ask the customer to activate it or provide its existing `SKILL.md` path.
