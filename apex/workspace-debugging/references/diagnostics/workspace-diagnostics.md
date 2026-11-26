# APEX Workspace Administration Diagnostics

Use this reference for APEX Workspace Administration dashboards, Monitor Activity, active sessions, Workspace users, and schema-mapping context. It does not diagnose application source, component behavior, or database internals.

## Workspace Dashboard Pass

From the target Workspace, use Administration > Dashboards and review only the report related to the Workspace administration request:

- Workspace: Workspace, application/schema counts, SQL scripts, open service requests, available schemas, and APEX file usage.
- Users: Workspace account status, roles, groups, recent accounts, and user counts.
- Activity: top users/apps/pages, recent logins, and recent APEX errors for the selected interval. Keep the report observation here; use live browser triage for reproduction and route source diagnosis to APEXlang.
- Developer Activity: APEX Builder changes, recent edits, and component-utilization summaries.
- Performance: pages with the worst APEX page performance, calculated from page-event counts and median server-generation time. Use it to identify which pages merit a bounded live browser check; it does not provide a database performance diagnosis.
- Applications: application/page/theme counts, groups, recent applications, and defaults. Route definitions, source, and artifacts to APEXlang.
- Database: database-object summaries by schema. Route object counts, statistics, privileges, and capacity analysis to the DB skill.

Record the Workspace, report name, relevant time window, counts, and visible status. Do not copy bulk reports into chat.

## Monitor Activity

Use [workspace-monitor-activity.md](../monitoring/workspace-monitor-activity.md) for Workspace reports such as Page Views, Developer Activity, Active Sessions, Login Attempts, Environment, Page View Analysis, Workspace Schema Reports, and Archived Activity. The report can establish that an application error or service issue is present; interpretation and diagnosis belong to APEXlang.

Use [workspace-service-admin.md](../workspace/workspace-service-admin.md) for Manage Service settings, requests, file usage, caches, session cleanup, saved reports, and other Workspace metadata operations.

For interactive reproduction, use [live-browser-debugging.md](live-browser-debugging.md). For application error-log interpretation, Debug-message analysis, source/component diagnosis, or code fixes, hand off to APEXlang. For schema/user/privilege changes outside APEX Workspace metadata, hand off to the DB skill.

## Active Session Inventory

Use Active Sessions for a narrow, read-only Workspace session inventory. Expose only the metadata needed to understand Workspace-level session status. Session details can contain application items, URLs, and user data; treat them as sensitive. The Session Detail page also exposes Debug-level and Trace Mode controls; route requests to operate or interpret them to APEXlang. Route application session-state analysis to APEXlang; use live browser triage for interactive reproduction.

## Browser Checks

Use [workspace-admin-ui-checks.md](workspace-admin-ui-checks.md) for Workspace administration pages and reports. Use [live-browser-debugging.md](live-browser-debugging.md) for live reproduction and browser-level investigation of an APEX application. Source/component diagnosis and APEX Debug/Trace evidence belong to APEXlang.

## Boundaries

- Workspace users, Workspace mappings, APEX activity reports, and APEX admin UI context stay here.
- Workspace-wide report summaries and Manage Service operations stay here, subject to the specific confirmation and handoff boundaries in `workspace-service-admin.md`.
- Application source, exports, Debug messages, component behavior, and application fixes go to APEXlang.
- Database accounts, grants, quotas, SQL, performance, ORDS, and infrastructure work go to the DB skill.
- Do not query internal APEX repository objects or create database logging/instrumentation objects.

Before substantive live checks, apply the APEX Admin Identity Gate, supported-version gate, MCP availability guard, and protocol/output requirements in `apex/workspace-debugging/SKILL.md`.
