# APEX Workspace Security Review

Use this checklist after substantial APEX Workspace administration or Workspace report review.

- Live APEX work used the confirmed APEX admin identity and supported APEX version.
- Workspace administrators, developers, end users, parsing schemas, and runtime identities were kept distinct.
- Only documented public APEX views/APIs were used; no internal repository objects were queried or changed.
- Workspace, application, page, session, user, and time scope was limited to what the task required.
- Workspace Activity reports and browser evidence were redacted; no passwords, tokens, cookies, authorization headers, or unnecessary personal values were exposed.
- Destructive Workspace changes had a current target inventory and exact confirmation.
- Application source/component findings were handed to APEXlang; database or ORDS findings were handed to the DB skill.
