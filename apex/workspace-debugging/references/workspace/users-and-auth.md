# APEX Workspace Users, Groups, And Authentication

Use this reference for APEX accounts, roles, groups, and account status within one Workspace. The [APEX 26.2 Administration Guide](https://docs.oracle.com/en/database/oracle/apex/26.2/aeadm/managing-users-in-a-workspace.html) covers single and bulk account creation, user maintenance, groups, and the Users dashboard.

APEX Workspace accounts are distinct from application end-user authentication, database login users, parsing schemas, ORDS/APEX runtime accounts, and APEX instance administrators. Instance Administrator and `INTERNAL` workspace account administration belongs to instance administration, outside this skill.

## Workspace User Tasks

- Review user names, roles, lock/expiry status, and group membership for the confirmed Workspace. Use the Users dashboard for summary status; use Manage Users and Groups for the specific account.
- Create one or multiple Workspace accounts, edit Workspace roles or component access (including Data Reporter where enabled), lock or unlock an account, and manage user groups only for the confirmed Workspace.
- Before changing or removing an account, show the exact user, Workspace, intended role/status change, and practical effect. Require fresh explicit confirmation for the exact change.
- A Workspace administrator may manage workspace groups, but groups do not replace application authorization or database grants. Route application authorization rules to APEXlang and database-enforced access to the DB skill.

MCP-backed reads and changes must use the confirmed APEX admin identity from `apex/workspace-debugging/SKILL.md`. Do not inspect or change APEX accounts under `SYS`, `SYSDBA`, parsing schemas, Workspace users, ORDS/APEX runtime accounts, generic deployment users, or unknown identities. `SYSTEM` is permitted only under the exact uppercase `YES` confirmation in the APEX Admin Identity Gate.

## Password Handling

- Do not ask the user to paste a password into chat or put a password in a skill, example, script, SQL literal, protocol, or tool log.
- Use the APEX UI or a verified public API with the site's approved secret-entry mechanism. Inspect the installed API signature before generating version-sensitive calls.
- Do not use or invent a shared fallback password, even for a demo account. If the environment only supports setting a password directly, stop and ask for an approved secret-handling path.
- If bulk account creation in the target UI assigns one shared password to multiple users, do not use it. Use an approved invitation/identity workflow or create accounts through the site's secure per-user process.

## Database Username Sign-In

If a sign-in screen explicitly asks for `Database Username`, the request concerns database authentication. Identify the distinction, then hand database user creation, password policy, grants, quotas, or lock remediation to the DB skill. Do not create a database account from this Workspace workflow or reuse the APEX admin connection for database work.

## API Use

For documented APEX Workspace user metadata, inspect `APEX_WORKSPACE_APEX_USERS` and its available columns before querying. `APEX_INSTANCE_ADMIN.UNLOCK_USER` is limited to an APEX-managed Workspace account; resolve the installed package/synonym and inspect arguments as described in [instance-admin-api.md](instance-admin-api.md). For other user-management APIs, verify the public API documentation and installed signature first.

Summarize only the confirmed Workspace and account changes. Treat names, email addresses, lock status, and login evidence as sensitive. Do not expose passwords, password hashes, authentication tokens, or unrelated user records.
