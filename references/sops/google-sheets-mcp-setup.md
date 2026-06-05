# SOP: Connect the CRM to Claude Code via Google Sheets (MCP)

Goal: let Claude read **and write** the CRM live in Google Sheets — no more download/upload of the `.xlsx`.

**When to do this:** when you make your first hire (VA/TC) and need shared, concurrent access. As a solo agent the repo `.xlsx` is fine. (See `context/work.md`.)

**Where to do this:** easiest in **Claude Code on desktop**, where you control MCP config + network. The web/remote environment locks down outbound network and MCP, so it may not work there.

---

## Overview (what you're building)

```
Claude Code (desktop)  ──>  Google Sheets MCP server  ──>  Google Sheets API  ──>  your CRM sheet
                                     ▲
                          authenticates as a Google
                          "service account" you create
```

A **service account** is a robot Google user with its own email. You share your sheet with that email, and the MCP server logs in as it.

---

## Step 1 — Put the CRM in Google Sheets

1. Upload `references/crm/Spencer_Kommons_CRM_v3.xlsx` to Google Drive.
2. Open it → **File → Save as Google Sheets** (converts to native format).
3. Keep the 5 sheet tabs and columns exactly as-is (see `.claude/rules/crm-rules.md`).
4. From the URL, copy the **Spreadsheet ID**:
   `https://docs.google.com/spreadsheets/d/`**`<THIS_IS_THE_ID>`**`/edit`

> Note: Google Sheets may not render the dashboard's shapes/drawings identically. The data is what matters; rebuild the dashboard visuals natively if needed.

## Step 2 — Create a Google service account + key

1. Go to <https://console.cloud.google.com/> → create a project (e.g. "spencer-crm").
2. **APIs & Services → Library** → enable **Google Sheets API** and **Google Drive API**.
3. **APIs & Services → Credentials → Create credentials → Service account**. Name it (e.g. `crm-bot`).
4. Open the service account → **Keys → Add key → Create new key → JSON**. A `.json` key file downloads. **Keep it secret.**
5. Copy the service account **email** (looks like `crm-bot@spencer-crm.iam.gserviceaccount.com`).

## Step 3 — Share the sheet with the service account

In Google Sheets → **Share** → paste the service account email → give **Editor** → send. (No email notification needed.)

## Step 4 — Store the key file safely

- Save the JSON key **outside the repo**, e.g. `~/.config/spencer-crm/service-account.json`.
- **Never commit it.** `.gitignore` already blocks common service-account key patterns — keep it that way.

## Step 5 — Add the Google Sheets MCP server to Claude Code

Pick a maintained Google Sheets MCP server (e.g. search "Google Sheets MCP server" — `mcp-google-sheets` is a common Python one runnable via `uvx`). **Read its README for the exact command + env var names** — they vary by server.

Typical pattern with the Claude Code CLI:

```bash
claude mcp add google-sheets \
  --env SERVICE_ACCOUNT_PATH=/Users/spencer/.config/spencer-crm/service-account.json \
  -- uvx mcp-google-sheets
```

Or via a project `.mcp.json`:

```json
{
  "mcpServers": {
    "google-sheets": {
      "command": "uvx",
      "args": ["mcp-google-sheets"],
      "env": {
        "SERVICE_ACCOUNT_PATH": "/Users/spencer/.config/spencer-crm/service-account.json"
      }
    }
  }
}
```

> ⚠️ `SERVICE_ACCOUNT_PATH` is illustrative — confirm the real variable name (some use `CREDENTIALS_PATH`, `GOOGLE_APPLICATION_CREDENTIALS`, etc.) in your chosen server's docs.

## Step 6 — Restart Claude Code & verify

1. Restart Claude Code so it loads the MCP server.
2. Run `/mcp` (or check the tools list) to confirm `google-sheets` connected.
3. Ask: *"List the tabs in spreadsheet `<ID>`"* then *"read the Active Leads sheet."*
4. Once reads work, test a small write on a scratch cell before trusting it with live data.

## Step 7 — Point the assistant at the sheet

Once live, tell me the **Spreadsheet ID** and I'll update `context/work.md` + `.claude/rules/crm-rules.md` so the assistant uses the Google Sheet as the source of truth (and we retire the repo `.xlsx`, or keep it as a periodic backup).

---

## Security notes

- The JSON key = full edit access as that service account. Treat it like a password. Never paste it into chat or commit it.
- Use **least privilege**: this service account should only have access to the one CRM sheet.
- The CRM contains client **PII** (names, phones, WeChat IDs) — keep the sheet's sharing tight (you + service account only).
- If a key leaks: delete it in the Cloud Console (**Keys → delete**) and create a new one.

## Fallback

If MCP setup is more than you want right now, stay on the repo `.xlsx` workflow — I edit it and you sync. Revisit this SOP at first hire.
