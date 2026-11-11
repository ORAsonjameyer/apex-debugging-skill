# APEX Workspace Safety Messages

Use the relevant message before crossing the corresponding APEX Workspace boundary. If the user already explicitly requested the relevant application or DB action, announce the handoff and continue within that authorization; ask only for authorization that is actually missing.

```text
APEXlang handoff: APEXlang owns this application source, export, component, or code-level debugging work. Continue within the user's authorized scope.
```

```text
DB skill handoff: the DB skill owns this database, schema, privilege, SQL, ORDS, or infrastructure work. Continue within the user's authorized scope using the selected connection.
```

```text
MLE fallback: the DB skill is unavailable. For this MLE creation privilege error only, use the bundled SQLcl MCP fallback within the user's authorized scope; general database work remains outside the fallback.
```

```text
Connection confirmation: SESSION_USER=<SESSION_USER>, CURRENT_USER=<CURRENT_USER>, ISDBA=<ISDBA>. Confirm that this is the intended APEX admin identity for the requested Workspace operation before I continue.
```

```text
SYSTEM confirmation required: SESSION_USER=SYSTEM, CURRENT_USER=SYSTEM, ISDBA=FALSE. Scope: <APEX_WORKSPACE_ACTION>. Targets: <TARGETS>. Reply exactly YES in uppercase to allow this privileged APEX-admin-scoped operation.
```

```text
Protocol file required: this APEX Workspace workflow needs a local protocol path outside the skill tree. Provide a directory or exact Markdown file path. Downloads is available if you confirm `Ja`. This confirms only the output location, not the APEX action.
```

```text
Environment confirmation required: this Workspace administration UI check is classified as <TEST|PRODUCTION>. Scope: <WORKSPACE_AND_READ_ONLY_SCOPE>. Reply exactly YES in uppercase before I inspect the current browser session. This does not authorize state changes.
```

```text
Unsupported APEX version detected: <VERSION_NO>. This Workspace skill supports only APEX 26.2, 26.1, 24.2, and 24.1. I will stop before generating version-sensitive APEX SQL or change steps.
```

```text
APEX MCP availability check failed: the MCP transport is closed, so I cannot safely verify or change APEX state. I will pause until the APEX MCP channel is available again.
```

```text
Safety stop: this Workspace removal is destructive. I will show the exact APEX workspace, mappings, users, and application inventory, then require the exact confirmation from `references/workspace/removal.md`. Database users and objects are outside this Workspace operation.
```

```text
Safety stop: this request would access or change internal APEX repository objects. I will use documented public APEX views or APIs instead.
```

```text
Sensitive evidence: Workspace Activity reports and browser data can contain secrets or personal information. I will use only the smallest necessary redacted excerpts.
```

```text
Workspace state change confirmation required: Workspace=<WORKSPACE_NAME>; action=<ACTION>; target=<EXACT_TARGET>; current state=<CURRENT_STATE>; expected effect=<EFFECT>. Reply exactly YES in uppercase to authorize this specific change. This confirmation does not authorize any other action.
```

```text
Security boundary: APEX session state, hidden items, read-only items, and client-side checks are not security boundaries. Application enforcement belongs to APEXlang; database-enforced access control belongs to the DB skill.
```
