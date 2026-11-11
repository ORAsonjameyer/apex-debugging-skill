# Workspace Administration Protocol

Use this reference before substantive live Workspace administration, Workspace report review, Workspace state changes, or Workspace customer-evidence analysis. Live APEX application browser triage has its own reference. Application source/component diagnosis and APEX Debug/Trace analysis belong to APEXlang; database diagnosis and changes belong to the DB skill.

## Location

Create or update a local Markdown protocol outside the skill tree before the workflow starts. Do not create database tables or other database objects for protocol storage.

Do not write protocol files into `workspace/`, `references/`, `tools/`, tests, committed documentation, or another repository path unless the user explicitly asks for a sanitized generic skill artifact.

Ask for a user-confirmed output directory or exact Markdown path. The local operating-system Downloads folder is a valid location. If no path is provided, offer Downloads and continue only after a fresh `Ja` reply; this confirms the file location only. Use a timestamped filename such as `apex-workspace-protocol-YYYYMMDD-HHMMSS.md`.

## Required Content

Record concise, redacted facts:

- local date/time and timezone;
- environment classification: development, test, production, managed service, or unknown;
- requested Workspace administration task and exact Workspace scope;
- affected Workspace user or active session only when needed to identify the target;
- active APEX admin identity category or browser-session category;
- required environment, `SYSTEM`, and state-change confirmations;
- whether evidence came from Workspace Administration UI, a supported APEX view/API, or a user-provided Workspace report;
- actions taken and whether they were read-only or state-changing;
- relevant Workspace observations and error text, with unnecessary identifiers removed;
- handoffs to APEXlang or DB when the request crosses skill boundaries;
- final status, limitations, and next step.

Do not use this protocol to document application-level Debug messages, page/component diagnosis, database findings, or companion-skill workflows. Record only the Workspace handoff context needed to continue there.

## Evidence Handling

- Append short updates instead of restating the whole case.
- Reference report names, time windows, and local file paths instead of copying bulk evidence.
- Keep customer exports, application/debug logs, database reports, and screenshots outside chat and the repository; the owning skill governs their analysis.
- Summarize open questions, confirmed Workspace facts, and next steps so the same evidence is not reprocessed.

## Redaction

Never include passwords, cookies, session IDs, bearer tokens, OAuth secrets, API keys, authorization headers, request bodies, item values, or unnecessary personal data. Do not include full secret-bearing URLs or customer hostnames unless required and redacted.

## Updates

Record an update before and after a Workspace state change, after each substantive Workspace report check, and before or after a handoff. For a test or production Workspace browser check, record the exact scope and the required uppercase `YES` confirmation.

End with a compact summary of the Workspace evidence reviewed, any Workspace change, evidence not reviewed because it belongs to another skill, and the next owner.
