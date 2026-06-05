# Decision Log

Append-only. When a meaningful decision is made, log it here.

Format: [YYYY-MM-DD] DECISION: ... | REASONING: ... | CONTEXT: ...

[2026-06-05] DECISION: Store the live CRM workbook (Spencer_Kommons_CRM_v3.xlsx) in the repo at references/crm/ and commit it. | REASONING: The container is ephemeral, so the assistant needs the data committed to use it across sessions; the repo is private. | CONTEXT: File contains client PII (names, phone numbers, WeChat IDs). Keep the repo private. Revisit if collaborators are ever added.

[2026-06-05] DECISION: Keep the existing Excel CRM (v3) — no migration to Notion/Follow Up Boss for now. | REASONING: The v3 workbook is well-structured and fast for a solo agent; the real bottleneck is daily follow-up + listing supply, not the tool. | CONTEXT: Reconsider a shared cloud CRM only when the first hire needs concurrent access.
