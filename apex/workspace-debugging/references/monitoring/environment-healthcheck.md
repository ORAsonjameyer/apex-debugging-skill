# APEX Workspace Administration Health Check

Use this reference to assess a Workspace administration request using supported APEX Workspace metadata, dashboards, Monitor Activity reports, and Manage Service evidence. It does not assess application source, database health, ORDS, or infrastructure.

## Scope

Check only the requested Workspace administration scope: Workspace availability, approved schema mappings, APEX Workspace user and group status, dashboards and Monitor Activity reports, Workspace settings and service requests, file usage, or availability of the relevant Manage Service surface. Use [live-browser-debugging.md](../diagnostics/live-browser-debugging.md) for interactive application reproduction; route source/component or APEX Debug/Trace analysis to APEXlang. If evidence points to database accounts, privileges, storage, ORDS, or infrastructure, hand it to the DB skill.

## Supported APEX Gate

Before live APEX queries or APIs:

1. Apply the APEX Admin Identity Gate in `apex/workspace-debugging/SKILL.md`.
2. Verify `APEX_RELEASE.VERSION_NO` using `references/workspace/version-notes.md`.
3. Stop for an unsupported release before generating version-sensitive SQL, PL/SQL, or changes.
4. Check public APEX view columns and package arguments against installed metadata and official Oracle documentation.

Use documented public APEX views and APIs only. Do not query or modify internal APEX implementation objects or create database objects for health checks.

## Evidence Intake

Record only what is needed:

- environment type and installed APEX release;
- exact Workspace;
- requested Workspace administration task;
- relevant Workspace Administration UI or Monitor Activity evidence and time window;
- evidence gaps and any skill handoff.

For static Workspace reports or screenshots, state that no database connection is needed. For customer-specific reports, confirm an output path outside this skill tree before writing.

## Check Sequence

1. Confirm Workspace, environment, APEX release, and requested administration scope.
2. Check only the Workspace metadata, dashboard, Monitor Activity report, or Manage Service surface relevant to the request.
3. Record observed status and evidence; do not infer a cause outside the checked Workspace metadata.
4. Route browser reproduction to [live-browser-debugging.md](../diagnostics/live-browser-debugging.md), source/component questions to APEXlang, and database/ORDS/infrastructure questions to the DB skill. For Workspace service operations, follow [workspace-service-admin.md](../workspace/workspace-service-admin.md).

## Status

| Status | Meaning |
|---|---|
| `GREEN` | Supplied supported APEX evidence shows no material issue in the checked Workspace administration scope. |
| `AMBER` | A Workspace metadata or access concern is present, but impact or cause is not established. |
| `RED` | Supported evidence shows the requested Workspace administration surface is unavailable or has an urgent access concern. |
| `UNKNOWN` | Required version, identity, Workspace scope, supported view/API, or evidence is missing. |

State the checked Workspace, evidence and time window, status, confirmed findings, what was not checked, and the owner for each handoff. Do not label application, database, ORDS, or infrastructure health from this check.

## Safety

- Protect APEX identities, session values, and user data; redact evidence before sharing.
- Do not change Workspace state as part of a health check without the normal confirmation and protocol gates.
- Use `references/workspace/version-notes.md` for the version gate and official Oracle APEX documentation for the installed release.
