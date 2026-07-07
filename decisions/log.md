# Decision Log

Append-only. When a meaningful decision is made, log it here.

Format: [YYYY-MM-DD] DECISION: ... | REASONING: ... | CONTEXT: ...

[2026-06-05] DECISION: Fixed two CRM data inconsistencies — Dashboard Active Leads 8→9, and L034 appointment 6/9/2026→09/06/2026. | REASONING: Active count omitted L039 (Brian Cheah, who is legitimately in both Active Leads and the Done Deals relationship bank); appointment cell had a month/day swap contradicting the reschedule note (9 June). | CONTEXT: Edited the .xlsx surgically via XML (inline strings) to preserve dashboard drawings/formatting that openpyxl would have dropped. Total Contacts stays 58 (unique). Dashboard "Updated" date left at 04 June — Spencer to refresh when he next works the CRM.

[2026-06-05] DECISION: Store the live CRM workbook (Spencer_Kommons_CRM_v3.xlsx) in the repo at references/crm/ and commit it. | REASONING: The container is ephemeral, so the assistant needs the data committed to use it across sessions; the repo is private. | CONTEXT: File contains client PII (names, phone numbers, WeChat IDs). Keep the repo private. Revisit if collaborators are ever added.

[2026-06-05] DECISION: Keep the existing Excel CRM (v3) — no migration to Notion/Follow Up Boss for now. | REASONING: The v3 workbook is well-structured and fast for a solo agent; the real bottleneck is daily follow-up + listing supply, not the tool. | CONTEXT: Reconsider a shared cloud CRM only when the first hire needs concurrent access.

[2026-06-08] DECISION: All real-estate skills (current + future pasted) default to the Malaysian market; localize automatically before committing. | REASONING: Spencer operates exclusively in Malaysian subsale luxury (KL/Mont Kiara); US-default skills (Zillow, $, cap rate, flood zones) need adapting every time. Codified as a standing rule to avoid re-explaining. | CONTEXT: After building realestate-analyze/comps/commercial/compare/report-pdf and running Mont Kiara Damai analysis. Rule lives in .claude/rules/realestate-localization.md.
