# APEX Workspace Safety Guardrails

Apply these APEX-specific guardrails to Workspace administration and Workspace report review.

## Workspace Roles And Identity

- Keep workspace administrator, developer, end user, parsing schema, database-login user, ORDS/APEX runtime account, and APEX instance administrator distinct.
- Use the confirmed APEX admin identity for live Workspace APIs and APEX metadata queries, as defined in `apex/workspace-debugging/SKILL.md`.
- Never use `SYS`/`SYSDBA`, a parsing schema, an ordinary workspace user, or an ORDS runtime account for routine APEX administration.
- Treat APEX session state, hidden items, read-only items, and client-side checks as application behavior, not security boundaries.

## Supported APEX Interfaces

- Use documented public APEX views and APIs. Do not query or update internal APEX repository objects.
- Check the installed APEX release and version-sensitive view columns or API arguments before live use.
- Scope Workspace queries to the known workspace, application, page, session, user, and time window.

## Evidence And Handoffs

- Treat Workspace Activity reports, session details, and browser evidence as sensitive. Avoid application payload fields and redact secrets or unnecessary personal data. Route Team Development files and application Debug data to APEXlang.
- Do not create database objects for Workspace logging, protocols, diagnostics, or instrumentation.
- Workspace account roles, groups, and APEX Workspace settings stay here. Application authorization rules, source, exports, components, and runtime-code diagnosis belong to APEXlang. Database identities, privileges, auditing, tenant isolation, SQL, ORDS, and infrastructure controls belong to the DB skill, except for the narrowly scoped MLE creation privilege fallback in `application/mle-privilege-fallback.md` when the DB skill is unavailable.
