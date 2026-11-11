# Live APEX Browser Debugging

Use this reference when the user wants to reproduce, observe, or narrow an APEX runtime issue interactively in an already-authenticated browser session. It covers live browser triage not provided by the APEXlang skill: visible page behavior, browser console output, and request metadata. It does not replace APEXlang for application source, component definitions, APEX Debug/Trace, or code changes, and it does not replace the DB skill for general database or ORDS work. The only local DB exception is the MLE creation privilege fallback when the DB skill is unavailable.

## Scope

This workflow may:

- reproduce a reported issue through the smallest safe user journey;
- inspect visible page behavior, navigation, screenshots, browser console messages, and network metadata exposed by the browser tool;
- distinguish page-load, submit, AJAX, REST/external-call, static-asset, and client-side symptoms;
- record redacted timestamps, page/application identifiers, request status and timing, and other facts useful for a handoff.

It does not inspect application source or exports, diagnose component definitions, analyze `APEX_DEBUG_MESSAGES`, configure APEX Debug/Trace, modify App Builder settings, or execute database/ORDS diagnostics. Hand off those parts to APEXlang or the DB skill.

## Browser Session And Confirmation

Use only the user's existing authenticated browser session. Never request passwords, cookies, session IDs, bearer tokens, authorization headers, or browser-profile secrets in chat. If the page is open in VS Code's embedded browser and a separate browser provider cannot attach, inspect that existing VS Code window through the available app UI instead; do not open a new session or copy its secret-bearing URL. If neither can access the session, ask the user to make it available or provide redacted static evidence.

Reuse the environment, application, page, symptom, time, and output location already provided in the session. If the environment is unknown, use an interactive question picker when available, with `Lokale Entwicklung`, `Test`, and `Produktion` as choices; include the redacted target and read-only scope in the question. Otherwise ask the same question in text. Do not infer the environment from `localhost`. For test or production, the user must explicitly authorize the identified read-only browser interaction; a structured environment selection that states that scope is sufficient. Discover an unknown page or time from the existing session when safe instead of blocking on repeated questions. A read-only choice does not authorize a submit or external effect. For a state-changing action, use the user's existing explicit authorization for the exact action and target; ask only if it is missing. Prefer a non-production environment.

## Reproduce And Observe

1. Confirm the user's requested target and symptom, and note whether the browser tool can inspect the page visually, navigate/click, read console messages, or inspect network metadata.
2. Reuse the user's selected protocol path, or obtain one before substantive triage or reproduction, and record the initial scope. An initial read-only look at the already-authorized page may establish the missing page and symptom details.
3. Follow the smallest safe click path that can reproduce the reported behavior. Keep the first pass read-only.
4. Record what the user sees and the relevant browser facts. If the Developer Toolbar is already available, use it only to identify the visible application/page context; do not change settings, enable Debug, inspect item values, or edit the application.
5. Summarize whether the behavior reproduced and route any source, APEX Debug/Trace, or database follow-up to the owning skill.

If the browser tool exposes only screenshots or visible page state, report that limit and do not imply that console or network evidence was examined.

## Console And Network Triage

Classify only enough browser evidence to identify the failing layer:

- **Page render:** initial document navigation, redirects, authentication, and static asset loading.
- **Page submit:** submit/accept request, validation or processing symptom, response status, and timing.
- **AJAX:** Dynamic Action, plug-in, lazy-load, or report/grid request that fails or is slow.
- **REST or external call:** visible request status and timing; route ORDS, database, or third-party service investigation to its owner.
- **Client-side symptom:** JavaScript exception, blocked asset, CORS/mixed-content message, or browser cache issue visible in the console.

For each relevant request, retain only method, redacted path shape, status, timing, response-size class, initiator/action, and timestamp. Never inspect or quote request/response bodies, session state, cookies, authorization headers, tokens, or secret-bearing URL values. Do not copy full console dumps, network tables, DOM snapshots, or HAR files into chat.

## Evidence And Protocol

Before substantive browser triage, reuse the user-confirmed protocol directory or exact file path. Ask only if no location has been supplied. Downloads is an available location after a fresh `Ja` confirmation under the output rules in `apex/workspace-debugging/SKILL.md`. Create or update a Markdown protocol before reproducing the issue; use a location outside this repository by default, or the user's explicitly selected location. Use a timestamped name such as `apex-live-browser-protocol-YYYYMMDD-HHMMSS.md`. Record the environment, application/page scope, symptom, authorization, reproduction steps, browser-tool capabilities, redacted observations, evidence path, and any APEXlang or DB handoff. Keep raw customer screenshots, HAR files, console dumps, and logs outside the skill tree.

Capture only the smallest useful facts: application ID or alias, page ID or title, visible error text, local timestamp and timezone, action name, request type/path shape, method, status, timing, response-size class, and whether the symptom reproduced. Do not copy bulk DOM/network output into chat. Redact HAR data before use: remove cookies, authorization headers, session IDs, request bodies, secret-bearing URL values, and unnecessary personal data.

If the browser tool cannot expose console or network details, report that limit and continue with visible behavior only. Do not imply that absent evidence was checked.

## Handoffs

- Application source/export, component-definition diagnosis, code changes, APEX Debug/Trace configuration, or `APEX_DEBUG_MESSAGES` analysis: hand off to APEXlang.
- SQL, schemas, grants, AWR/ASH, SQL Monitor, ORDS pools/gateway, or infrastructure: hand off to the DB skill. If unavailable, only MLE creation `ORA-01031` privilege diagnosis and authorized minimal repair may use the [local fallback](../../application/mle-privilege-fallback.md).
- Workspace users, schema mappings, Workspace administration reports, or APEX Workspace state: return to the relevant Workspace reference.

Carry forward only the confirmed environment, visible symptom, redacted browser facts, and protocol path. Browser authentication does not authorize MCP or SQL access; apply the Workspace APEX Admin Identity Gate independently if a Workspace-owned API or report query is needed.
