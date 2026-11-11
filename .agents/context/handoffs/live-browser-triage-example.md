# Live Browser Triage Example

This example describes an application runtime symptom. Use the Workspace skill's live browser workflow for the first bounded reproduction and browser-level evidence. Do not inspect application source or analyze APEX Debug messages here.

```text
In the APEX application, clicking “Add post” shows: “Something went wrong extracting/storing the EXIF information.” The environment is test, the user is already signed in, no additional evidence is available, and local Downloads may be used for a protocol.
```

Follow `workspace/references/diagnostics/live-browser-debugging.md`: confirm the application/page scope and browser action, record only redacted visible/console/network facts, and keep the protocol outside this repository. Hand source/component or APEX Debug/Trace analysis to APEXlang. Hand generic database, ORDS, AWR/ASH, SQL Monitor, or infrastructure investigation to the DB skill.
