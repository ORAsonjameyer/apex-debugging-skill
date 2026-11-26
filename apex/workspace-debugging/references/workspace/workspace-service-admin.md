# APEX Workspace Service Administration

Use this reference for Workspace-scoped operations exposed from **Manage Service**, Workspace dashboards, and related Workspace Administration pages. It records the Workspace tasks this skill owns and routes adjacent application or database work to its owner.

Oracle documents that some Manage Service functionality may not be available in Oracle Cloud APEX instances. Confirm which page and action are available in the target environment; do not infer a missing feature is a failure.

Official APEX 26.2 references:

- [Manage Service](https://docs.oracle.com/en/database/oracle/apex/26.2/aeadm/using-the-manage-service-page.html)
- [Workspace preferences](https://docs.oracle.com/en/database/oracle/apex/26.2/aeadm/configuring-workspace-preferences.html)
- [Service requests](https://docs.oracle.com/en/database/oracle/apex/26.2/aeadm/making-a-service-request.html)
- [Workspace users and groups](https://docs.oracle.com/en/database/oracle/apex/26.2/aeadm/managing-users-in-a-workspace.html)
- [Workspace session state](https://docs.oracle.com/en/database/oracle/apex/26.2/aeadm/managing-session-state-for-a-workspace.html)
- [Page and region caching](https://docs.oracle.com/en/database/oracle/apex/26.2/aeadm/managing-page-and-region-caching.html)
- [Saved Interactive Reports](https://docs.oracle.com/en/database/oracle/apex/26.2/aeadm/managing-saved-interactive-reports.html)
- [Data Dictionary Cache](https://docs.oracle.com/en/database/oracle/apex/26.2/aeadm/accessing-data-dictionary-cache-from-workspace-administration.html)
- [File utilization](https://docs.oracle.com/en/database/oracle/apex/26.2/aeadm/file-utilization.html)
- [Workspace application build status](https://docs.oracle.com/en/database/oracle/apex/26.2/aeadm/changing-build-status-for-multiple-applications.html)
- [Workspace environment banner](https://docs.oracle.com/en/database/oracle/apex/26.2/aeadm/configuring-environment-banner-for-workspace.html)
- [Extension menu links](https://docs.oracle.com/en/database/oracle/apex/26.2/aeadm/managing-links-on-the-extensions-menu.html)
- [User preferences](https://docs.oracle.com/en/database/oracle/apex/26.2/aeadm/managing-user-preferences.html)
- [Developer Activity and Click Count log purge](https://docs.oracle.com/en/database/oracle/apex/26.2/aeadm/purging-the-developer-activity-and-click-count-log-files.html)
- [Workspace dashboards](https://docs.oracle.com/en/database/oracle/apex/26.2/aeadm/viewing-workspace-dashboards.html)
- [Monitor Activity within a Workspace](https://docs.oracle.com/en/database/oracle/apex/26.2/aeadm/monitoring-activity-within-a-workspace.html)

## Workspace-Owned Work

| Workspace surface | Use it for | Boundary |
| --- | --- | --- |
| Workspace preferences | Review or change Workspace login controls, App Builder/SQL Workshop/Team Development availability, RESTful Services enablement, PL/SQL editing, issue-file settings, and Workspace session timeout. | Confirm Workspace-wide impact. Login controls affect APEX-managed accounts; application authentication remains with APEXlang. The Workspace timeout may be superseded by an application-level timeout. Use only the approved UI/secret path for SMTP credentials and do not expose their values. |
| Workspace messages, environment banner, extension links | Publish Workspace-specific notices, label an environment, or maintain links and subscriptions in the APEX Extensions menu. | These controls apply to Workspace context only. Instance-wide messages, banners, or settings require the instance administrator. |
| Service requests | Review request history and prepare or submit an APEX Workspace request for another Workspace or a Web Service request limit increase. | Schema and storage requests concern database provisioning/capacity; route submission and remediation to DB. For a self-service new Workspace, use [lifecycle.md](lifecycle.md). Termination is a destructive service request: confirm the exact Workspace and data-retention impact, then follow the service owner's process. [removal.md](removal.md) applies only when removing APEX Workspace metadata through APEX administration. The 26.2 Web Service Limit request is a Workspace service request; underlying ORDS, network, or database remediation belongs to its owner. |
| Workspace utilization and file utilization | Identify APEX Workspace file usage and capacity pressure. | Do not equate this with database tablespace usage or delete application/customer files here. Route database storage and quota interpretation to DB; route application artifact ownership to APEXlang. |
| Data Dictionary Cache | View Workspace schema/table cache status and, when stale metadata affects the APEX Create Application/Page wizards, refresh the cache. | Prefer **Refresh Cache Only** for an APEX cache refresh. **Gather Statistics and Refresh Cache** also gathers database statistics; hand that choice to DB. |
| Developer Activity and Click Count logs | Review Workspace developer changes and external-click log availability; purge a named Workspace log only for a stated retention or data-cleanup need. | Show the exact log and scope first; require fresh confirmation before purge. Do not use the logs to reconstruct application source or user journeys. |
| Workspace session state | Review current/recent session inventory, inspect a specific session record when authorized, or run the documented **Report Sessions** preview before removing a session or purging its state by age. | Never disclose item values, collections, or unnecessary session details. Removing session state or a session record can interrupt a user or application; require exact target/age, impact summary, and fresh confirmation. Hand application-specific session-state diagnosis to APEXlang. |
| Application cache | Review cached pages/regions and purge a selected page, region, application cache, or Workspace-level region cache when stale output is the reported issue. | Workspace-wide purges have broad impact; show the exact scope and affected cache count where available, then require fresh confirmation. Cache policy and source behavior belong to APEXlang. |
| Application Build Status | Review and manage Workspace-wide application availability and build status when an APEX Workspace access or editing restriction is requested. | Enumerate every affected app and the resulting run/edit restriction before changing. Require fresh confirmation. This does not perform deployment or alter application artifacts. |
| Saved Interactive Reports and subscriptions | Review a named saved report or subscription and remove it when the owner requests cleanup. | Confirm exact application, page/report or subscription, user/owner, and effect first. Do not change the underlying report definition or application behavior. |
| User Preferences | Identify the preference report or reset target when the issue is Workspace-level account cleanup. | Do not expose preference values. Route preference meaning, application use, and code changes to APEXlang; clear a specific user's preferences only after the exact target, owner, and effect are confirmed. |

For Workspace user roles, group membership, account status, and password handling, use [users-and-auth.md](users-and-auth.md). For aggregate activity and monitoring report definitions, use [workspace-monitor-activity.md](../monitoring/workspace-monitor-activity.md). For broad Workspace health checks, use [environment-healthcheck.md](../monitoring/environment-healthcheck.md).

## 26.2 Network Access Control Handoff

APEX 26.2 adds Workspace/schema-level network access control using the instance parameter `WEBSERVICE_USE_SCHEMA_ACL`. This skill may identify the feature and collect the Workspace symptom or report, but it does not set the instance parameter, create or change database network ACLs, or troubleshoot outbound network infrastructure. Hand those tasks to the DB skill. Legacy SOAP requests are unsupported when this feature is enabled, so include that compatibility concern in the handoff when relevant.

## Live-Work Requirements

Before live Workspace UI, API, or report work:

1. Apply the identity, environment, supported-version, MCP, and protocol requirements in `apex/workspace-debugging/SKILL.md`.
2. Confirm the Workspace and the exact Manage Service or report task.
3. Read only the metadata needed to answer that task. Do not query APEX internal repository objects.
4. Before any service request, preference change, purge, cache operation, account edit, or application status change, show the target, current state, intended effect, and relevant risk; require fresh explicit confirmation for that exact action.
5. Record the operation in the external Workspace protocol and summarize the result with sensitive data redacted.

## Handoff Rules

- **APEXlang is valuable** for source/exports, APEXlang definitions and file-level imports, component behavior, application Debug/Trace controls and message analysis, application session-state behavior, user-preference semantics, cache policy, and artifact changes. This skill can first reproduce a symptom and preserve redacted browser observations in [live-browser-debugging.md](../diagnostics/live-browser-debugging.md).
- **DB is valuable** for database users/schemas, grants, tablespace/quota remediation, statistics collection, SQL performance, ORDS, infrastructure, database security, and the new 26.2 network ACL control.
- A Workspace report's existence or a visible application error may be established here. Its application-source cause or repair goes to APEXlang. A Workspace schema report may be reviewed for Workspace context; database privilege or capacity interpretation and remediation go to DB.
- Do not hand off ordinary Workspace activity trends, APEX user status, Workspace service settings, targeted Workspace cache/session cleanup, or Workspace health checks merely because an APEX application is involved.
