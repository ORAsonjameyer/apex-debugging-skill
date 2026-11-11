# APEX Workspace Activity Reports

Use this reference for a query-based Workspace time series from `APEX_WORKSPACE_ACTIVITY_LOG` or `APEX_ACTIVITY_LOG` when a report needs aggregation or time buckets beyond the standard Monitor Activity page. For report navigation and other Workspace Monitor Activity surfaces, start with [workspace-monitor-activity.md](workspace-monitor-activity.md).

## View Pre-Check

APEX view columns vary by release and privilege. Inspect `APEX_DICTIONARY`, `ALL_OBJECTS`, and `ALL_TAB_COLUMNS` before version-specific SQL. Do not query internal APEX repository tables.

## Workspace Usage Trends

Use the narrowest supported APEX view and limit the query to the Workspace and time window:

```sql
SELECT TRUNC(view_date, 'HH24') AS hour_start,
       workspace,
       COUNT(*) AS page_events,
       COUNT(DISTINCT apex_session_id) AS apex_sessions,
       COUNT(DISTINCT application_id) AS applications,
       ROUND(AVG(elapsed_time), 3) AS avg_elapsed_seconds,
       MAX(elapsed_time) AS max_elapsed_seconds
FROM apex_workspace_activity_log
WHERE view_date >= :start_time
  AND view_date <  :end_time
  AND workspace = :workspace_name
GROUP BY TRUNC(view_date, 'HH24'),
         workspace
ORDER BY hour_start,
         page_events DESC;
```

Use Workspace Monitor Activity to drill into its documented reports. Use [live-browser-debugging.md](../diagnostics/live-browser-debugging.md) for interactive reproduction of one application's page behavior. Hand source/component diagnosis and APEX Debug-message interpretation to APEXlang.

## Boundary

This reference summarizes Workspace activity only. Use [live-browser-debugging.md](../diagnostics/live-browser-debugging.md) for interactive application reproduction; source/component and APEX Debug/Trace diagnosis belongs to APEXlang. Database performance evidence belongs to the DB skill.
