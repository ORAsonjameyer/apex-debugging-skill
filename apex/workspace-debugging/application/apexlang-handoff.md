# APEXlang Debugging Handoff

Use the original APEXlang skill for application source, components, APEXlang definitions, application Debug/Trace, APEX_DEBUG_MESSAGES, error-log interpretation, imports, validation, and application changes.

## Handoff Summary

Carry forward only:

- application name or ID, alias, and page;
- environment and approximate local time window;
- expected versus observed behavior;
- whether the issue reproduced and the minimal safe user journey;
- redacted browser console/request facts, if available;
- Workspace report name and event time, if relevant;
- protocol or evidence path outside this repository;
- the specific APEXlang question or next action.

Do not attach source, exports, session values, request bodies, HAR files, cookies, credentials, or Debug dumps unless the APEXlang workflow requests and safely handles them.

Example handoff:

> APEXlang handoff: the Workspace/browser pass reproduced <SYMPTOM> in app <APP_OR_ALIAS>, page <PAGE>, on <ENVIRONMENT> at <LOCAL_TIME>. Expected <EXPECTED>; observed <OBSERVED>. Redacted browser fact: <STATUS_OR_CONSOLE_SUMMARY>. Workspace report evidence: <REPORT_AND_TIME_WINDOW_OR_NONE>. Protocol: <EXTERNAL_PATH>. Please continue with the original APEXlang workflow for <SOURCE_COMPONENT_DEBUG_OR_ARTIFACT_QUESTION>.

## If APEXlang Is Unavailable

Check configured skill roots and actual local paths already supplied or discovered in the session before declaring APEXlang unavailable. If it cannot be found, say so and ask the user to activate/install it or provide its existing local SKILL.md path. Pause source, component, Debug/Trace, and artifact analysis. Continue independent Workspace work, bounded live browser observation, and separately authorized DB diagnosis. Do not reconstruct APEXlang procedures in this folder.
