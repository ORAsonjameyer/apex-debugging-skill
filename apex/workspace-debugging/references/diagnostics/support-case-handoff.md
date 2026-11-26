# Support Case Handoff

Use this workflow when the user asks for a support case, escalation summary, or
handoff after an APEX investigation, including when the investigation cannot
proceed. It prepares a reviewable draft from the current investigation; it does
not create, submit, or transmit a case.

## Prepare the draft

Use existing conversation evidence, the execution's redacted protocol, and
authorized companion-skill findings. Do not redo diagnosis or make additional
live queries solely to fill the template; mark unavailable information as
unknown. Keep the verified app, environment, operation, and time window only as
needed for support. Retain exact error codes and minimal sanitized excerpts.

Present a copy-ready draft with:

1. **Subject and impact:** the affected function, expected and actual behavior,
   impact and scope, including frequency if known.
2. **Environment:** development/test/production, APEX and database versions,
   application/page and relevant execution context only if established.
3. **Reproduction:** minimal steps, preconditions and result; say when the
   reported failure was not reproduced or a step is unknown.
4. **Evidence:** concise errors, timestamps with timezone, redacted debug
   references or available attachment descriptions, and their origin.
5. **Investigation and changes:** checks, outcomes, authorized changes and
   verification; identify who owns any unfinished APEXlang or DB analysis.
6. **Open questions and request to support:** what remains unknown, the
   specific help requested, and any information the user must supply.

Separate confirmed facts from hypotheses and unknowns. Do not infer a root
cause, environment, version, impact, or successful fix from incomplete evidence.
Note when console, network, database or debug evidence was not examined.

Redact credentials, tokens, cookies, authorization headers, session IDs, request
and response bodies, item values, personal data, secret-bearing URLs and
unnecessary hostnames, object names and application data. A debug ID, application
identifier, object name or sanitized log excerpt may be included only when
needed for the support case; flag it for user review. Do not attach raw logs or
screenshots automatically.

Show the draft to the user for review and editing. Report in chat by default;
write a local file only if the user requests one and an output location is
selected under the skill's existing output rules. When a file is requested,
keep the existing per-execution investigation protocol intact and identify the
support draft as a separate deliverable, not a replacement protocol.

If the user separately requests feedback about the skill, provide a distinct,
short local draft describing the observed obstacle, evidence, proposed
improvement and any measured metrics. Label estimates and unknown metrics; do
not infer token usage. Do not include customer content unnecessarily. The
support case and skill feedback serve different audiences and must not be
combined automatically.

Creating or transmitting a support case, sending feedback, and uploading
attachments require a separate, explicit user instruction identifying the
destination and approved content. This workflow itself never submits or sends.
