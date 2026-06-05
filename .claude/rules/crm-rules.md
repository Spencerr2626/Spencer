# CRM Rules

Conventions for handling leads and contacts. Currently the CRM is a manual Excel file (migration planned — see `projects/crm-setup/`).

## Core Rules

- **Never auto-create or auto-edit a contact** without confirming with Spencer first.
- **Always resolve IDs/codes to real names** when referring to a lead — never surface raw row numbers or codes.
- **Don't invent data.** If a field (phone, language, source, status) is missing, flag it rather than guessing.

## Lead Status Convention

Tag every lead by temperature:

- **Hot** — ready to transact / actively viewing.
- **Warm** — engaged, needs nurturing.
- **Cold** — gone quiet, needs re-activation.

Track at minimum: name, contact, **source** (referral / iProperty / PropertyGuru / WeChat), **preferred language**, status, and **next-action date**.

## Follow-Up

- The daily follow-up triage (see `projects/lead-follow-up-system/`) prioritizes hot → warm → cold.
- When suggesting a follow-up, also draft the message in the lead's preferred language.
