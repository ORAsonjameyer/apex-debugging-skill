# APEX Workspace Administration UI Checks

Use this reference only to inspect APEX Workspace Administration screens, dashboards, Monitor Activity, Manage Service, or Active Sessions in an already authenticated browser session. For live APEX application reproduction or browser evidence, use [live-browser-debugging.md](live-browser-debugging.md). Application exports, source/component diagnosis, and APEX Debug/Trace analysis belong to APEXlang.

## Scope

The Workspace-side browser pass can:

- navigate to the requested Workspace administration report;
- inspect Workspace, user, activity, active-session, service-request, utilization, and other Manage Service metadata visible in that UI;
- record the Workspace, report name, time window, and visible Workspace-level status;
- identify whether the next step belongs to APEX Workspace administration, APEXlang, or the DB skill.

Do not inspect or modify application source, page components, or application runtime behavior here. Do not read browser cookies, tokens, authorization headers, request bodies, session-state values, or preference values. This browser reference is for read-only checks; use `workspace-service-admin.md` for a requested state change and its confirmation gate.

## Environment Confirmation

Before attaching to or interacting with a browser, confirm the environment. For test or production, show the Workspace and read-only administration scope, then require a fresh exact uppercase `YES`. This does not authorize state changes or actions in an application.

Use only the user's existing authenticated session. Do not ask for APEX passwords, cookies, session IDs, bearer tokens, or browser profile secrets in chat.

## Evidence And Handoff

Capture only the smallest Workspace evidence needed: report name, Workspace, time window, counts, and visible status. Use a redacted screenshot only when the Workspace administration UI state is necessary to explain a finding.

For live application reproduction or browser DevTools evidence, switch to [live-browser-debugging.md](live-browser-debugging.md). For source/component diagnosis, Debug-message interpretation, APEX Debug/Trace, or artifact work, announce the APEXlang handoff. For database, ORDS, or infrastructure findings, announce the DB skill handoff. Route identity-provider findings to their identity-provider owner.

Before substantive browser inspection, use [workspace-protocol.md](workspace-protocol.md) and the output-path rule in `apex/workspace-debugging/SKILL.md`.
