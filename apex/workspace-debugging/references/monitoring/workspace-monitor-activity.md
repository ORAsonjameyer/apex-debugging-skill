# Workspace Monitor Activity

Use this reference for APEX Workspace Monitor Activity and its Workspace-level context. It covers observations available in the Workspace dashboard and reports; it does not diagnose application source or database internals.

Official source: Oracle APEX 26.2 Administration Guide, [Monitoring Activity within a Workspace](https://docs.oracle.com/en/database/oracle/apex/26.2/aeadm/monitoring-activity-within-a-workspace.html):

```text
https://docs.oracle.com/en/database/oracle/apex/26.2/aeadm/monitoring-activity-within-a-workspace.html
```

## Workspace Reports

- **Page Views** and **Page View Analysis**: use for aggregate Workspace usage, trends, most-viewed pages, and weighted page performance. For a Workspace-wide time-series query, see [activity-log.md](activity-log.md). Use the live browser reference for interactive reproduction.
- **Developer Activity**: use for Workspace-level Builder changes, detailed application edits, and component-utilization summaries. Treat usernames and timestamps as sensitive; source/component interpretation belongs to APEXlang.
- **Sessions**: use for a limited, read-only Workspace session inventory and hourly session trends. Session detail can expose page views, background processing, browser data, and session-state item values; do not copy or analyze the values here.
- **Environment**: use for browser, user-agent, operating-system, and external-click summaries. Redact internal URLs, hostnames, schema names, proxy details, and version data unless needed.
- **Login Attempts**: use for Workspace login triage. Treat usernames, IP addresses, and failure messages as sensitive. Route database audit policy or external identity-provider investigation to its owner.
- **Application Errors**: establish whether a reported APEX error is present in the selected Workspace and time window. Use live browser triage to reproduce it and observe browser facts; route source/component diagnosis to APEXlang.
- **Workspace Schema Reports**: use Workspace Schemas for mapping context. Schema tablespace and database privilege reports are database evidence; route their interpretation and remediation to the DB skill.
- **Web Service Activity, automation logs, and archived activity**: use only to establish Workspace report presence, count, or time window. Route application behavior and source analysis to APEXlang; route ORDS, endpoint, network, or database infrastructure investigation to the DB skill.
- **Generative AI service utilization**: use [ai-token-monitoring.md](ai-token-monitoring.md) for Workspace token limits and aggregate Workspace utilization. Route app-level behavior or attribution to APEXlang.

The Active Session Detail page also exposes controls for a session's APEX Debug level and Trace Mode. Recognize the control and route any request to enable, change, interpret, or analyze Debug/Trace to APEXlang; do not operate those controls here. Session details can include session-state values, so do not use them for app behavior diagnosis. For interactive reproduction and redacted browser observations, use [live-browser-debugging.md](../diagnostics/live-browser-debugging.md).

For Manage Service operations such as cache/session cleanup, Workspace settings, data dictionary cache, file utilization, log retention, user preferences, and saved reports, use [workspace-service-admin.md](../workspace/workspace-service-admin.md).

## Live Checks

Before MCP-backed Workspace report queries, apply the APEX Admin Identity Gate and supported-version/MCP guards in `apex/workspace-debugging/SKILL.md`. APEX dictionary views and columns vary by release; inspect only the public Workspace views needed for the request:

```sql
SELECT view_name,
       comments
FROM apex_dictionary
WHERE view_name IN ('APEX_WORKSPACE_ACTIVITY_LOG', 'APEX_ACTIVITY_LOG')
ORDER BY view_name;
```

```sql
SELECT table_name,
       column_id,
       column_name,
       data_type
FROM all_tab_columns
WHERE table_name IN ('APEX_WORKSPACE_ACTIVITY_LOG', 'APEX_ACTIVITY_LOG')
ORDER BY table_name,
         column_id;
```

Use documented public APEX views only; do not query internal APEX repository objects. Filter to the requested Workspace and time window. Do not retrieve application item values, request bodies, payloads, cookies, tokens, or authorization headers.

## Handoffs And Review

- Workspace usage trends and schema mappings remain in this skill.
- Live browser reproduction and console/network observations use `../diagnostics/live-browser-debugging.md`. Application source/component diagnosis and Debug/Trace interpretation go to APEXlang. Keep Workspace report observations here; hand off only the report analysis that needs application or database expertise.
- Database accounts, privileges, storage, auditing, performance, and ORDS infrastructure go to the DB skill.

Before sharing results, redact sensitive values, summarize bulk logs, and identify evidence that was routed to another skill rather than analyzed here.
