# CRM Rules

Conventions for handling leads and contacts.

## Where the CRM lives

- **Offline source (works everywhere, incl. web sessions):** the Excel workbook `Spencer_Kommons_CRM_v3.xlsx` in `references/crm/`. This is the working source of truth today.
- **Live Google Sheet (desktop only, via MCP):** Spreadsheet ID `1XBCVRrnUnERB2vY7CTUopj-hQPgRtNa9`. Readable/writable only when the `google-sheets` MCP is connected on Claude Code **desktop** (see `references/sops/google-sheets-mcp-setup.md`). Not reachable from the web sandbox.
- Keep the two in sync. Until the Google Sheet is confirmed live and converted to a **native** Sheet (not an uploaded `.xlsx`), treat the repo workbook as authoritative.

## Workbook Structure

Five sheets, all keyed by a stable ID:

1. **🔥 Active Leads** — live prospects to work. Cols: `ID, Name, Nationality, Language, WhatsApp, WeChat ID, Contact Source, Platform / Referral, Lead Type, Status, Priority, Area, Budget (RM), Size, Beds, Property Type, Property Name, Unit No., Last Contact, Next Follow-Up, Notes, Tags`.
2. **✅ Done Deals & Relationship Bank** — closed clients, past tenants, referral sources. Nurture for repeat & referrals. Adds `Lease Start, Lease End, Referral Potential`.
3. **📅 Follow-Up Schedule** — every touchpoint logged. Cols: `ID, Contact Name, Nationality, Follow-Up Date, Channel, Priority, Status, Purpose / Topic, Outcome / Notes, Next Action, Appointment Date & Time, Follow Up Next Date, Language, Done?, Remarks`.
4. **💰 Pipeline & Deals** — viewing → offer → LOO → SPA → completion. Cols: `Deal ID, Client Name, Nationality, Project / Address, Area, Type, Stage, Transaction Price (RM), Comm %, Est. Comm (RM), LOO Date, SPA Date, VP / Move-in, Days to Close, Notes`.
5. **📊 Dashboard** — summary stats (contacts, active, done, GCI YTD, pipeline value, est. commission, referral network).

## Conventions

- **IDs:** leads are `L###` (e.g. `L057`), deals are `D###` (e.g. `D002`). IDs are the join key across sheets — a lead in Active Leads keeps its `L###` when it becomes a deal/done deal.
- **Priority tags:** `Hot 🔥` / `Warm 🌤️` / `Cold ❄️`. Keep the emoji — that's the existing convention.
- **Dates:** `DD/MM/YYYY`.
- **Currency:** RM. Default commission is **2%** unless stated.
- **Language** is a first-class field — every lead has a preferred language; follow-ups must match it.

## Core Rules

- **Never auto-create or auto-edit a contact/row** without confirming with Spencer first.
- **Always resolve IDs to real names** when referring to a lead — never surface a bare `L###` without the name.
- **Don't invent data.** If a field (phone, language, source, status, budget) is missing, flag it rather than guessing.
- **Preserve the schema** — when editing the workbook, keep columns, sheet names, and tag formats exactly as above.

## Follow-Up

- The daily follow-up triage (see `projects/lead-follow-up-system/`) prioritizes **Hot → Warm → Cold**, then by `Next Follow-Up` / `Follow-Up Date`.
- When suggesting a follow-up, draft the message in the lead's **preferred language** (Mandarin for most China/local-Chinese clients, English for the rest).
- Log the touchpoint in the Follow-Up Schedule and advance the `Next Follow-Up` date.
