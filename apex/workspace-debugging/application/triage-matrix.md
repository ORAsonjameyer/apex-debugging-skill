# APEX Application Triage Matrix

Use this matrix to route an application symptom without copying another skill's diagnostic procedure.

| Symptom | First useful check here | Next owner when deeper analysis is needed |
| --- | --- | --- |
| Page does not load, redirects unexpectedly, or renders incorrectly | Reproduce once in the signed-in browser; note URL shape, visible message, and whether the issue is consistent | APEXlang for page/component logic; DB for gateway, ORDS, or infrastructure |
| Button submit or validation behaves unexpectedly | Record the visible action, expected result, actual result, and redacted request status/timing if available | APEXlang for validations, processes, conditions, and component definitions |
| Dynamic Action, report/grid refresh, or other AJAX interaction fails | Identify the triggering interaction and the failing request's method, redacted path shape, status, and timing | APEXlang for application behavior; DB for SQL/database work |
| JavaScript exception, blocked asset, CORS, or mixed content appears | Capture the concise console message and the associated asset/request metadata; do not collect request bodies | APEXlang for application JavaScript/assets; DB or the network owner for gateway, ACL, or infrastructure |
| APEX application error appears | Establish whether the Workspace Activity or Application Errors report has an event in the requested time window; reproduce in browser if safe | APEXlang for error-log interpretation, Debug/Trace, APEX_DEBUG_MESSAGES, source, and remediation |
| Page appears slow | Use the APEX Workspace Performance dashboard to identify pages with high weighted page activity, then capture browser timing for the reported journey | APEXlang for application/component analysis; DB for SQL execution, AWR/ASH, SQL Monitor, or database performance |
| REST or web-service call fails | Record only visible request status, redacted endpoint shape, timing, and the user-facing result | APEXlang for application call configuration; DB for ORDS, network ACL, database, or infrastructure |
| `ORA-01031` while creating or executing MLE modules or environments, including during an APEX application import | Follow [mle-grant-debug.md](mle-grant-debug.md): inspect the failure, then prefer DB for effective privilege checks; use structured choices for any missing environment or connection selection | APEXlang for the import artifact/path; DB skill for privileges and grants; if unavailable, the [limited SQLcl MCP fallback](mle-privilege-fallback.md) handles MLE creation privileges only |
| Login, role, or access differs between users | Capture the visible symptom and user type without collecting credentials or session values | Workspace skill for APEX Workspace accounts/groups; APEXlang for application authorization; identity-provider owner for SSO |

For a live browser session, use [live-browser-debugging.md](../references/diagnostics/live-browser-debugging.md). For Workspace report definitions and limits, use [workspace-monitor-activity.md](../references/monitoring/workspace-monitor-activity.md). This matrix is a routing aid, not an application-code or database troubleshooting manual.

## Evidence Limits

- Record only observations exposed by the browser tool. State explicitly when console or network metadata is unavailable.
- Do not inspect DOM dumps, HAR bodies, cookies, session identifiers, authorization headers, item values, passwords, tokens, or personal data unrelated to the symptom.
- Do not enable or change APEX Debug/Trace from this add-on. The APEX 26.2 Active Session Detail page exposes those controls; route requests to operate or interpret them to APEXlang.
- A Workspace dashboard metric or browser timing identifies a symptom and scope; it does not establish a database root cause.
