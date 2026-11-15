---
name: apex-application-diagnostics
description: Triage APEX runtime symptoms and MLE creation privilege errors, using the DB skill or a narrow SQLcl MCP fallback; route source-level debugging to APEXlang.
---

# APEX Application Diagnostics

Use this add-on for application runtime symptom intake and routing. It adds an application-focused entry point while keeping APEXlang source and Debug/Trace procedures in the original APEXlang skill.

First apply the matching local triage case and collect the available, permitted browser or Workspace evidence. Resolve what the local workflow supports, and bring in APEXlang or DB for the specific source, trace, or database question that remains. Continue local observation and verification alongside those handoffs; do not require a companion skill merely to begin a documented local check. A generic error alone is not proof of a particular cause.

Prefer APEXlang and the DB skill for their respective domains when available. If either is missing, use the local browser-triage capabilities and the scoped MLE creation privilege fallback where applicable; identify any remaining work that requires the missing companion skill.

## Choose the Owner

| Need | Owner |
| --- | --- |
| Reproduce the reported page behavior and capture visible UI, browser console, or redacted request metadata | This add-on, using [live-browser-debugging.md](../references/diagnostics/live-browser-debugging.md) |
| Review Workspace activity, application-error presence, sessions, or page-performance ranking | Workspace monitoring, using [workspace-monitor-activity.md](../references/monitoring/workspace-monitor-activity.md) |
| Inspect or change application source, components, APEXlang files, application Debug/Trace, APEX_DEBUG_MESSAGES, imports, validation, application locks, or working copies | Original APEXlang skill |
| Investigate SQL, database schemas/privileges, database performance, ORDS, network ACLs, or infrastructure | DB skill; only MLE creation privilege errors have a local fallback when it is unavailable |
| Change Workspace accounts, mappings, settings, caches, sessions, or service requests | Workspace references, beginning with [workspace-service-admin.md](../references/workspace/workspace-service-admin.md) |

APEX 26.2 adds file-level APEXlang import and application lock/working-copy APIs. These remain application-development workflows owned by APEXlang even when invoked from an APEX Workspace. See [Oracle APEX 26.2 New Features](https://docs.oracle.com/en/database/oracle/apex/26.2/htmrn/new-features.html).

## Triage Flow

1. Capture the application or alias, page, environment, affected user type, expected result, observed result, time window, and whether the issue reproduces.
2. Use [triage-matrix.md](triage-matrix.md) to choose the smallest useful evidence source.
   For recurring application, privilege, MLE, checksum, and deployment symptoms, consult [diagnostic-patterns.md](diagnostic-patterns.md) for targeted hypotheses, evidence, and handoffs. These are not confirmed causes or automatic repair instructions.
   For `ORA-01031` while creating or running MLE modules or environments, including an identified MLE runtime action, start with [mle-grant-debug.md](mle-grant-debug.md). Use the DB skill for privilege checks and authorized repair without requiring APEXlang or a Debug/Trace lookup first. If the operation or identity remains unclear, gather the necessary evidence and hand off additional component or trace analysis only when needed. If DB cannot be found, the [SQLcl MCP fallback](mle-privilege-fallback.md) handles only the documented MLE creation privilege case.
3. For live reproduction, follow the existing browser procedure. Do not duplicate its authentication, confirmation, privacy, or protocol steps here.
4. If source, component, APEX Debug/Trace, or application artifact work is needed, check whether APEXlang is active and make a visible handoff before continuing.
5. If the cause may be in SQL, database security, ORDS, network access, or infrastructure, announce the handoff and continue with the DB skill within the user's authorized scope. A prior explicit request for DB diagnosis or repair is already authorization for the handoff. If the DB skill is unavailable, use the local fallback only for MLE creation privileges; other DB work still needs the DB skill.
6. Report what was observed, what remains unknown, the evidence limits, and the next owner.

## Boundaries

- Browser login does not authorize APEX MCP, SQL, or database access. Apply each skill's own identity and confirmation requirements.
- Do not inspect application source, APEX exports, component definitions, APEX_DEBUG_MESSAGES, session-state values, request/response bodies, credentials, or internal APEX repository objects here.
- A Workspace Application Errors report can establish that an error was recorded. The source-level meaning and fix belong to APEXlang.
- Keep app debugging evidence outside this repository. Use redacted summaries and preserve only facts needed for the next owner.
