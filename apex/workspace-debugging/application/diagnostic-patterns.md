# APEX Diagnostic Patterns

Use the matching pattern as a hypothesis, not as a diagnosis. First record the visible symptom, affected request and target; distinguish observed facts from inferred causes. Capture only redacted evidence allowed by [live-browser-debugging.md](../references/diagnostics/live-browser-debugging.md). Source, component, Debug/Trace, application import and repair belong to APEXlang; general database and privilege investigation belongs to the DB skill. If a companion skill is unavailable, respect the limits in [SKILL.md](SKILL.md); only the separately documented MLE creation fallback is available for the relevant `ORA-01031` case.

## Page Items and Dynamic Actions

| Pattern | Evidence to establish through the owning skill |
| --- | --- |
| Browser item appears populated but server reads `NULL` or an old value | Correlate the same item, request and time; with APEXlang check how the item is maintained and whether its value reaches the server. Do not assume all requests share the same session state. |
| Item omitted from AJAX submission | With APEXlang identify the actual server consumer and check the applicable action's **Items to Submit** or the refreshed region's **Page Items to Submit**. The omission is a cause only when that request needs the current value. |
| Dynamic Action does not fire | Record trigger, element and observed interaction; hand off event, conditions, initialization and affected elements to APEXlang. A missing console message alone does not prove that the action did not run. |
| AJAX request returns an error | Capture interaction, redacted request status and timing; correlate the server error with APEXlang Debug/Trace where authorized. The visible AJAX message may wrap an underlying error. |

## Page Builder and Charts

| Pattern | Evidence to establish through the owning skill |
| --- | --- |
| Builder cannot open a page that is listed or appears in runtime | Compare workspace, application, page, target environment and working-copy context; a listed page is not proof that rendering succeeded. Route component and import analysis to APEXlang. |
| A page template reference may no longer resolve | With APEXlang verify the referenced template in the page's current theme and compare a suitable working page; differing IDs alone are not a defect. Follow the template-reference guidance in [triage-matrix.md](triage-matrix.md). |
| Chart shows `JSON.WRITER.CLOSE_OBJECT` | Treat it as a symptom, not a root cause; correlate the failing chart request with APEXlang Debug/Trace and the underlying SQL or rendering error. Missing-table and privilege causes are hypotheses only. |
| Chart series has a failing SQL source | APEXlang identifies the installed series, source and underlying error; DB checks objects and privileges as needed. Do not infer a missing table from an empty chart. |

## SQL, Identities and Privileges

| Pattern | Evidence to establish through the owning skill |
| --- | --- |
| `ORA-00942` on a referenced table or view | DB verifies the actual execution identity, object resolution, synonyms and applicable access; missing object and missing access are distinct possibilities. |
| Definer-rights PL/SQL works interactively but not in a stored program | DB checks the program's rights model, resolved object and effective privileges in that context; interactive role access alone does not establish stored-program access. |
| `ORA-01031` | Identify the exact operation, object, identity and context; hand off to DB. Do not infer which grant is missing from the error alone. For MLE creation or execution, follow [mle-grant-debug.md](mle-grant-debug.md). |
| Import uses an unexpected execution identity | Distinguish login, parsing schema, object owner and actual installer/DDL identity; establish the latter from reliable evidence before proposing a grant. APEXlang owns import details; DB owns privilege checks. |
| Connection points to a different PDB or database | DB verifies service, container and user on the selected connection and compares them with the confirmed application target before further queries or changes; a connection label alone is not evidence. |

## MLE, Links and Deployment

| Pattern | Evidence to establish through the owning skill |
| --- | --- |
| `CREATE [OR REPLACE] MLE MODULE` fails | Record exact DDL failure and actor, then follow [mle-grant-debug.md](mle-grant-debug.md); use DB or the limited fallback for a verified creation-privilege problem. |
| Executing JavaScript through MLE fails | Distinguish module calls from dynamic execution and identify the failing operation, actor and language/module/environment permissions. Route execution and dynamic MLE privileges to DB; the local fallback does not cover them. |
| MLE environment may refer to a missing module | With APEXlang/DB inspect the relevant environment mapping, module and owner through supported metadata; distinguish an absent module from an import-name mismatch or missing access. |
| URL checksum or Session State Protection failure | Capture the safe link context and error; APEXlang checks link generation, target items, checksum and session context. Do not recommend disabling protection as a shortcut. |
| Supporting Objects are missing or only partly installed | APEXlang reviews install summary, failed statements, object status and script dependencies; DB handles database causes. Retry only the appropriately scoped reviewed work with required authorization. |
| Exported APEXlang and installed application differ | APEXlang verifies app identity, workspace, working copy, export provenance and component state; compare supported artifacts before choosing a repair. A local file alone does not establish the installed state. |
| APEX/SQLcl or APEXlang version may be incompatible | APEXlang checks the installed APEX release, actual SQLcl/compiler version, source metadata and relevant release guidance; compare validation output from the intended tool before concluding that components are invalid. |

## References

- [APEX session state and AJAX](https://docs.oracle.com/en/database/oracle/apex/26.2/apxdc/understanding-ajax-and-redirect.html)
- [APEX Dynamic Action debugging](https://docs.oracle.com/en/database/oracle/apex/26.2/htmdb/debugging-dynamic-actions.html)
- [APEX URL tampering protection](https://docs.oracle.com/en/database/oracle/apex/26.2/htmdb/preventing-url-tampering.html)
- [MLE JavaScript privileges](https://docs.oracle.com/en/database/oracle/oracle-database/26/mlejs/system-and-object-privileges-required-working-javascript-mle.html)
- [Oracle Database role behavior in PL/SQL](https://docs.oracle.com/en/database/oracle/oracle-database/26/dbseg/configuring-privilege-and-role-authorization.html)
