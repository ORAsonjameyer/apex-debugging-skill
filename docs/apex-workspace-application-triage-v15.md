# 🧭 APEX Application & Workspace Triage — V15

Visual one-pager: [PNG](apex-workspace-application-triage-v15.png). Operational details: [Application triage](../apex/workspace-debugging/application/SKILL.md), [MLE grant debugging](../apex/workspace-debugging/application/mle-grant-debug.md), and the [SQLcl MCP fallback](../apex/workspace-debugging/application/mle-privilege-fallback.md).

## 🔎 Live triage

- Confirm environment, workspace, application, and page.
- Reproduce in the signed-in browser and record one redacted, timestamped protocol.

## 🧪 Diagnose and verify

- Classify the failing layer and gather the minimum useful evidence.
- Start with the selected Workspace identity.
- Check permissions; apply authorized fixes and verify the result.

## 🔀 Route by owner

- **APEXlang:** application source, components, Debug/Trace, and imports.
- **DB:** SQL, grants and MLE, ORDS, and infrastructure.
- **Workspace:** users, mappings, services, monitoring, and health.
- **MLE fallback:** creation privilege only, when the DB skill is unavailable.

## 🛡️ Safety

- A missing grant alone does not prove the cause; confirm runtime identity.
- Protect credentials, sessions, payloads, and personal data.
- Production changes require explicit authorization.

For version-specific API and view support, check the active APEX release.
