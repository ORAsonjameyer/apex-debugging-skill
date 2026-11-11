# APEX Application & Workspace Triage — Cheat Sheet V8

Visual one-pager: [PNG](apex-workspace-application-triage-v8.png). Operational details: [Application triage](../apex/workspace-debugging/application/SKILL.md), [MLE grant debugging](../apex/workspace-debugging/application/mle-grant-debug.md), and the [SQLcl MCP fallback](../apex/workspace-debugging/application/mle-privilege-fallback.md).

**Live application debugging, guided MLE privilege diagnosis, and Workspace administration.** Application source and APEX Debug/Trace belong to the original APEXlang skill; general database privileges, grants, SQL, and ORDS belong to the DB skill. A narrow MLE creation privilege fallback is included when the DB skill is unavailable.

**Recommendation:** Prefer APEXlang and the DB skill for their respective domains. If either is unavailable, continue with the local browser-triage and MLE-fallback capabilities where applicable, and state what remains outside their scope.

## Application and Live Debugging

- **Live browser:** use the existing signed-in APEX session, including a browser embedded in VS Code; observe the visible UI, available console, and redacted request metadata.
- **Application symptoms:** classify page, submit, AJAX, JavaScript, REST, performance, or access issues and hand source/component or APEX Debug/Trace work to APEXlang.
- **MLE `ORA-01031`:** identify the failed MLE operation, target PDB, parsing schema/object owner, and execution identity; prefer the DB skill and SQLcl MCP for effective privilege checks. If the DB skill is absent, the bundled fallback handles MLE module/environment creation privilege errors only. The error alone does not name the missing grant.
- **Authorized repair:** if the user authorizes a fix and the missing right and recipient are verified, use the DB skill or the narrow fallback with the selected privileged MCP connection to apply and verify the smallest appropriate grant. Respect an explicit read-only or no-grants instruction. Retry only the affected script when authorized and its effects are understood.
- **Guided choices:** when not already known, use the available question picker for environment (`Lokale Entwicklung`, `Test`, `Produktion`) and for actual discovered database connections. Reuse prior answers and honor the connector's active-connection switch rule. If the exact grant is known and not prohibited, one picker can combine connection selection with explicit approval of that grant.

## Workspace Activities

- **Administration:** lifecycle, APEX Workspace users/groups, approved schema mappings, resources, Manage Service settings, and service requests.
- **Monitoring:** dashboards, Monitor Activity, login attempts, sessions, application-error presence, weighted page-performance reports, activity trends, and Workspace AI-service utilization.
- **Health and tools:** Workspace health checks, the local planning helper, redacted protocol guidance, and version-aware checks of public APIs and views.

## Route by Owner

| Workspace skill | Original APEXlang skill | DB skill |
| --- | --- | --- |
| Live browser observation, symptom routing, Workspace accounts, settings, dashboards, reports and health; limited MLE creation privilege fallback if DB skill unavailable | Application source/components, APEXlang definitions, APEX Debug/Trace, imports, validation, locks, working copies, and application changes | Preferred owner for database accounts/schemas/privileges, MLE checks and grants, SQL, database performance, ORDS, network ACLs, and infrastructure |

The Workspace skill prefers the DB handoff. When the DB skill cannot be found, its local fallback checks MLE creation privileges and can apply the verified minimal grant if authorized; it does not cover general SQL, `ANY` grants, dynamic MLE execution, or database administration. An explicit request for the relevant application or DB diagnosis or repair authorizes its handoff; the chosen connection and its tool rules still apply. A visible MLE error does not require APEXlang to be active before the privilege check begins.

## Safety and Evidence

- **Workspace API identity:** use a confirmed APEX administrator. Never use `SYS` or `SYSDBA`; `SYSTEM` is a narrowly scoped APEX-admin exception requiring a fresh exact uppercase `YES`. DB-owned privilege work follows the DB skill's rules; the MLE fallback may use a user-selected `SYSTEM` connection without `SYSDBA` after verifying its PDB.
- **Workspace administration UI:** for test or production, require the separate fresh exact uppercase `YES` specified by the Workspace administration workflow before attaching.
- **Live UI:** confirm the environment and read-only scope before test or production interaction. A structured environment choice that states the scope can provide this authorization. Use existing explicit authorization for subsequent actions; do not treat a read-only choice as permission to change data.
- **Privacy:** do not expose passwords, cookies, tokens, session IDs, request/response bodies, item values, or unredacted HAR files. SQLcl MCP may audit executed statements.
- **Evidence:** reuse the user's explicitly selected protocol path. Otherwise keep customer evidence outside the repository and ask for a path only when one is required.

## APEX 26.2 Baseline

As of **November 2, 2026**, Oracle lists APEX **26.2, 26.1, 24.2, and 24.1** as supported. APEX 23.2 support ended in May 2026. See [Oracle's APEX support table](https://www.oracle.com/apex/).

APEX 26.2 file-level APEXlang import and application lock/working-copy APIs remain APEXlang workflows. Workspace-Level Network Access Control uses `WEBSERVICE_USE_SCHEMA_ACL`; instance configuration and database ACL work route to DB. See [APEX 26.2 New Features](https://docs.oracle.com/en/database/oracle/apex/26.2/htmrn/new-features.html).
