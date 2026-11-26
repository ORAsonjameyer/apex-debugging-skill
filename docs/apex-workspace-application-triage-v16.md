# APEX Application & Workspace Triage — V16

Visual one-pager: [PNG](apex-workspace-application-triage-v16.png) ([SVG](apex-workspace-application-triage-v16.svg)). Operational details: [Application triage](../apex/workspace-debugging/application/SKILL.md), [MLE grant debugging](../apex/workspace-debugging/application/mle-grant-debug.md), [SQLcl MCP fallback](../apex/workspace-debugging/application/mle-privilege-fallback.md), and [support case handoff](../apex/workspace-debugging/references/diagnostics/support-case-handoff.md).

## Live triage

- Confirm environment, workspace, application, and page when known.
- Reproduce in the signed-in browser and record one redacted, timestamped protocol.

## Diagnose and verify

- Classify the failing layer and gather the minimum useful evidence.
- For MLE privileges, begin with the selected relevant Workspace schema identity.
- Apply authorized fixes and verify the result within the responsible skill's scope.

## Route by owner

- **APEXlang skill:** application source, components, Debug/Trace, and imports.
- **DB skill:** SQL, grants and MLE, ORDS, and infrastructure.
- **Workspace skill:** users, mappings, services, monitoring, and health.
- **MLE fallback:** creation privilege only, when the DB skill is unavailable.

## Safety

- A missing grant alone does not prove the cause; confirm the relevant identity and context.
- Protect credentials, session identifiers, payloads, and personal data.
- Follow the applicable environment, identity, and authorization gates for live work and changes.

For version-specific API and view support, check the active APEX release.

## Support case handoff

On request, prepare a redacted support-case draft from existing evidence for user review; do not send it automatically.
