---
name: daily-lead-followup
description: Spencer's daily lead follow-up triage. Use when Spencer asks who to follow up with today, wants his daily follow-up list, asks "who should I contact", or wants draft follow-up messages for his CRM leads. Reads the Kommons CRM workbook, surfaces due/overdue follow-ups (Hot > Warm > Cold), and drafts a ready-to-send message per lead in their language.
---

# Daily Lead Follow-Up

Spencer's #1 automation: every day, tell him exactly who to follow up with and give him a message he can send. The biggest business risk is leads going cold — this skill prevents that.

## When to use

- "Who do I follow up with today?" / "Daily follow-up" / "Who's gone cold?"
- "Draft my follow-ups" / "Who should I contact this week?"

## Step 1 — Run the triage

The CRM is `references/crm/Spencer_Kommons_CRM_v3.xlsx`. Run the helper (it needs `openpyxl` — `pip install openpyxl` if missing):

```bash
python3 .claude/skills/daily-lead-followup/triage.py
```
- Defaults to today in **GMT+8** and a **+2 day** horizon.
- Override with `--date YYYY-MM-DD` (e.g. to plan ahead) or `--horizon N`.

The script outputs three buckets — **⚠️ OVERDUE**, **📌 DUE TODAY**, **🔜 UPCOMING** — sorted Hot → Warm → Cold, each with purpose, next action, appointment, and context pulled from both the Follow-Up Schedule and Active Leads sheets.

### Also run the Lease Radar (every morning)

Spencer asked to be notified when **tenancy renewals** and **check-ins / move-ins** are around the corner. Run this alongside the triage so it surfaces automatically in the morning brief:

```bash
python3 .claude/skills/daily-lead-followup/lease_radar.py
```

- Reads lease Start/End from **✅ Done Deals** and VP/Move-in from **💰 Pipeline & Deals**.
- Buckets: **⚠️ Just expired** (confirm renewed/vacated), **🔁 Renewals due** (≤60d), **🔑 Check-ins/Move-ins** (≤30d).
- Surface anything that appears — a lease ending = renewal commission + a possible new listing; a check-in = make sure the move-in goes smoothly. Offer to prep the renewal TA or a check-in reminder.

## Step 2 — Present the priority list

Lead with the answer (no preamble — see `communication-style.md`):

- **Overdue first** — these are the urgent ones; call them out.
- Then **due today**, then a short look-ahead.
- For each: name + ID, priority, channel (WhatsApp/WeChat), and the one-line "why".
- Flag anything off: unparseable/`TBC` appointment dates, a Hot lead with no next follow-up date, or CRM/dashboard drift.

## Step 3 — Draft a message per lead

For every overdue + due-today lead, draft a ready-to-send follow-up:

- **Language:** match the lead's `Language` field. Mandarin for most China/local-Chinese clients (簡短、親切), English for the rest. If a lead is on **WeChat**, the message is almost certainly Mandarin.
- **Tone:** warm, professional, non-pushy, client-first — Spencer's brand. Short. No fluff. No emojis unless natural.
- **Make it specific:** reference the actual property/purpose/next action from the triage (e.g. "源 1,500–1,800 sq ft 的 Mont Kiara 单位", "the RM4.5mil+ options at MK 10"), not a generic "just checking in".
- Keep each draft to 2–4 sentences. Give Spencer a clean block he can copy per lead.

## Step 4 — Offer to log it

After Spencer sends messages, offer to update the CRM: advance `Next Follow-Up` / `Follow Up Next Date`, set `Last Contact`, and note the outcome in the Follow-Up Schedule. **Never edit the workbook without confirming first** (see `.claude/rules/crm-rules.md`). If he confirms, edit the `.xlsx` with `openpyxl`, preserving sheet names, columns, ID format, and the `Hot 🔥 / Warm 🌤️ / Cold ❄️` tags, then remind him to commit.

## Notes

- Respect all of `.claude/rules/crm-rules.md` (schema, IDs `L###`/`D###`, dates `DD/MM/YYYY`, never auto-create/edit without confirmation).
- This is read-first, write-only-on-confirmation.
