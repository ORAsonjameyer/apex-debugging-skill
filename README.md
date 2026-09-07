# Oracle APEX Workspace Skill

This repository contains the `workspace` Agent Skill for Oracle APEX administration workflows. It provides operational guardrails, routing guidance, references, and deterministic read-only helpers for APEX workspace and instance administration.

## What It Provides

- Workspace lifecycle planning, inventory, verification, schema mapping, user administration, recovery, and removal safeguards.
- APEX deployment, export, import, promotion, patching, and post-deployment review guidance.
- APEX runtime monitoring using supported APEX APIs, public metadata views, activity logs, page-performance evidence, debug/error context, REST activity, and background-job context.
- Browser-assisted APEX debugging for an already signed-in browser session, including reproduction, Developer Toolbar review, console and network metadata, and APEX-side correlation.
- Static review of APEX application exports (`.sql` and `.apx`) without requiring database access.
- AI token-limit and usage-evidence checks for supported APEX environments.
- Local protocol-file guidance for state-changing work, debugging, and customer-evidence analysis.
- Version-aware checks for supported APEX releases and runtime discovery of version-sensitive APIs, views, columns, and package signatures.

The included tools are optional planning and analysis helpers. They do not execute SQLcl, ORDS, generic database administration, or customer-specific workflows.

## Scope Boundaries

This skill owns the APEX administration layer only. It does not:

- Generate or materially modify APEX application artifacts.
- Perform generic SQL, PL/SQL, schema, user, grant, quota, tablespace, backup, recovery, SQL tuning, AWR/ASH, SQL Monitor, ORDS, or infrastructure work.
- Query or modify internal APEX repository tables as a shortcut.
- Create logging tables, protocol tables, triggers, packages, instrumentation, or other database objects for skill operation.
- Store customer exports, reports, logs, screenshots, HAR files, or derived evidence in the repository.

This repository performs no APEXlang application or artifact work. Whenever an APEX application is created or changed with APEXlang, the APEXlang skill must be available and active. If a debugging case genuinely requires APEXlang-specific artifact inspection or changes, this repository announces and hands off to the APEXlang skill. If that skill is unavailable, application or artifact work stops. Application generation, artifact changes, and APEXlang execution remain outside this repository. Generic database, SQLcl, performance, security, migration, and ORDS work is handed to the DB skill.

## Cross-Skill Collaboration

The companion domain `SKILL.md` files are authoritative:

- APEX application development: `apex/SKILL.md`
- Generic Oracle Database and related database operations: `db/SKILL.md`

Before maintaining this repository, compare the proposed capability with those source skills. Existing checks, scripts, APIs, workflows, or security controls must be reused by reference and handoff, not copied into this skill.

Before an action owned by a companion skill is used, the user must see and confirm a visible handoff. The target skill's own `SKILL.md`, references, identity rules, connection, and confirmation gates then apply. Connections and privileges must not be silently reused across skills.

Example announcements:

```text
APEXlang skill handoff: `apex/SKILL.md` owns this APEX application or artifact work. Confirm the switch before continuing.
```

```text
DB skill handoff: `db/SKILL.md` owns this generic database, SQL, performance, ORDS, or schema work. Confirm the switch before continuing.
```

## Roles and Identity Model

The skill distinguishes the following identities; they are not interchangeable:

- APEX instance administrator for APEX Administration Services and the `INTERNAL` workspace.
- Dedicated database account with `APEX_ADMINISTRATOR_ROLE` for routine instance-level APEX administration.
- Workspace administrator or developer for workspace-scoped UI work.
- Application parsing schema and application database-login user.
- ORDS/APEX runtime account.
- Database administrator or diagnostic/performance identity owned by the DB/ORDS skills.

Routine live APEX administration uses a confirmed, dedicated non-`SYS`/`SYSTEM` APEX admin identity whenever available. The active identity is verified with `SESSION_USER`, `CURRENT_USER`, and `ISDBA` before live MCP-backed APEX queries or changes.

Routine APEX administration is blocked for `SYS`, `SYSDBA`, `ISDBA = TRUE`, parsing schemas, workspace schemas, workspace users, ORDS/APEX runtime accounts, generic deployment users, and unknown identities.

`SYSTEM` is an explicit exception only for APEX-admin-scoped work, without `SYSDBA`, after identity verification, visible scope and risk details, safe password handling, and a fresh reply of exactly `YES` in uppercase. Passwords are never requested or printed in chat, scripts, SQL text, protocol files, or logged tool calls.

The APEX Instance Administrator bootstrap path is separate. Where Oracle requires it, `apxchpwd.sql` may use `SYS AS SYSDBA`; that path is not a routine APEX admin session and must not be used for ordinary workspace creation, imports, monitoring, or API automation.

## Evidence and Output Handling

- File-only analysis explicitly states when no database access is needed.
- For customer `.sql` or `.apx` exports, the skill asks once for additional runtime evidence such as APEX Activity Log, Page Performance, Debug, HAR/Network, AWR/ASH, SQL Monitor, ORDS logs, or deployment logs.
- Customer-specific reports require a user-confirmed external output path before writing.
- Debugging and state-changing workflows require a local protocol file outside the skill tree.
- Protocols record scope, identity category, actions, observations, evidence references, handoffs, and final status while redacting secrets and sensitive payloads.
- Large artifacts remain local; responses use focused excerpts and compact summaries to reduce token usage.

## Supported Versions

The skill uses Oracle APEX 26.1 documentation as its primary reference and supports APEX 26.1, 24.2, and 24.1 as defined by the skill's version gate. Version-sensitive APIs, views, columns, and arguments are checked against the target instance when live access is available.

## Repository Layout

```text
workspace/
├── SKILL.md
├── references/
│   ├── debugging/
│   ├── deployment/
│   ├── monitoring/
│   ├── security/
│   └── workspace/
└── tools/
```

Load only the routed reference needed for the current task. Do not treat this README as a replacement for `workspace/SKILL.md` or the routed references.

# IMPORTANT TO READ
I accept no liability for the use of this skill; it supports only officially supported Oracle APEX versions and invokes or uses only original, documented Oracle APEX functionality.
