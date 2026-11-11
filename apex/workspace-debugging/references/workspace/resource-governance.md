# APEX Workspace Resource Governance

Use this reference for APEX Workspace-level limits and usage metadata, such as APEX file usage, application counts, sessions, and service requests. Use the Manage Service File Utilization report to identify APEX workspace storage pressure. Database storage, tablespace quotas, CPU/I/O, Resource Manager configuration, and infrastructure capacity belong to the DB skill.

For Generative AI token limits or usage per APEX workspace/application, use [ai-token-monitoring.md](../monitoring/ai-token-monitoring.md).

## Inspect Supported APEX Metadata

Workspace resource columns vary by APEX release and managed service. Check the installed public APEX metadata before selecting fields:

```sql
SELECT view_name,
       comments
FROM apex_dictionary
WHERE view_name IN ('APEX_WORKSPACES', 'APEX_WORKSPACE_SCHEMAS')
ORDER BY view_name;
```

```sql
SELECT table_name,
       column_id,
       column_name,
       data_type
FROM all_tab_columns
WHERE table_name IN ('APEX_WORKSPACES', 'APEX_WORKSPACE_SCHEMAS')
ORDER BY table_name,
         column_id;
```

Use only discovered, documented APEX workspace columns to review APEX file-storage limits, workspace/application counts, and APEX activity. Keep the query scoped to the target workspace and time window.

## Recommendations

- Change an APEX workspace limit only after confirming the current APEX value, target workspace, requested limit, expected APEX-side effect, and user authorization.
- Do not treat an APEX file-storage limit as a database tablespace or schema quota. Do not infer database capacity from APEX metadata.
- APEX 26.2 lets Workspace administrators request an increase to the Web Service request limit through Make a Service Request. Confirm the current limit, requested increment, Workspace, request history, and effect before submitting. The service request does not diagnose or repair ORDS, network, or database capacity.
- If the evidence points to database storage, resource groups, CPU/I/O, waits, or infrastructure, hand that portion to the DB skill.
