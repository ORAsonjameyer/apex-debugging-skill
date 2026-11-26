# APEX Workspace AI Token Limits

Use this reference only for APEX AI token-limit governance and aggregate utilization at the Workspace level. Application-specific AI service configuration, prompts, component behavior, and per-application token attribution belong to APEXlang. Provider billing and model pricing are external to this skill.

Official APEX references for supported releases:

```text
https://docs.oracle.com/en/database/oracle/apex/26.2/htmdb/viewing-generative-ai-service-utilization.html
https://docs.oracle.com/en/database/oracle/apex/26.2/htmdb/viewing-generative-ai-service-history.html
https://docs.oracle.com/en/database/oracle/apex/26.2/htmdb/creating-generative-ai-service-objects.html
```

## Workspace Scope

- Confirm the target Workspace and whether the request concerns a configured token limit, remaining Workspace tokens, or aggregate Workspace utilization.
- Use the documented APEX Administration UI or public API supported by the installed release for that Workspace-level value.
- Do not infer a Workspace-level total from a service-level or application-level counter. Do not attribute shared-service totals to an application.
- Route app-specific usage, AI service configuration, instrumentation, or prompt/output analysis to APEXlang.
- Route provider billing, tenancy billing, model pricing, and external quota management outside this Workspace skill.

## Live-Work Gate

For MCP-backed APEX checks, apply the identity, supported-version, and MCP guards in `apex/workspace-debugging/SKILL.md`. Inspect installed public APEX metadata before relying on a release-specific view, column, or API. Do not query internal APEX repository objects.

For a state change to a Workspace token limit, identify the exact Workspace, current value, requested value, supported APEX setting/API, and expected Workspace-level effect. Record the action in the Workspace protocol and require explicit confirmation before changing it.

## Evidence And Privacy

Summarize the Workspace limit or aggregate utilization, the report/API and time window used, and any evidence gaps. Do not retrieve or include prompts, completions, embeddings, item values, credentials, provider endpoints, or per-app attribution unless that work is explicitly handed to APEXlang.
