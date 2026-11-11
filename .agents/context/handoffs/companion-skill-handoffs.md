# Companion Skill Handoffs

## APEXlang

The original APEXlang skill is the designated companion for APEX application source, component definitions, APEX Debug/Trace, `APEX_DEBUG_MESSAGES`, and artifact work. Use it whenever application source or artifacts must be created, changed, validated, exported, diffed, or imported, or when code-level/debug-message diagnosis is needed. APEX 26.2 file-level import and `APEX_APPLICATION_ADMIN` application-lock/working-copy APIs are also APEXlang-owned. Use `workspace/references/diagnostics/live-browser-debugging.md` for bounded reproduction and browser-level observation.

```text
APEXlang skill handoff: `apex/SKILL.md` owns this application source, component-definition, APEX Debug/Trace, or artifact work. Confirm the switch before continuing.
```

The Workspace skill may provide Workspace name, APEX Workspace user context, approved schema mappings, dashboard/Monitor Activity context, Workspace service settings, and redacted live-browser observations. Application export, validation, import, promotion, source/component and APEX Debug/Trace diagnosis, and post-import checks remain in APEXlang.

If the original APEXlang skill is unavailable locally, tell the customer and pause the APEXlang-owned portion. Ask them to install/activate the original skill or provide its existing local `SKILL.md` path. Continue independent Workspace work or bounded live browser triage; do not copy or reconstruct APEXlang workflows in this context.

## DB

Use for generic SQL, PL/SQL, SQLcl, schema, user, grant, quota, tablespace, performance, AWR/ASH, SQL Monitor, migration, security, or ORDS work.

```text
DB skill handoff: `db/SKILL.md` owns this generic database, SQL, performance, ORDS, schema, or network ACL work, including APEX 26.2 Workspace-Level Network Access Control setup. Confirm the switch before continuing.
```

After confirmation, follow the target skill's own identity, connection, references, and safety rules. Do not silently reuse the APEX admin connection.
