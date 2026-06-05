# SOP: Connect the CRM to Claude Code via Google Sheets (MCP)

Goal: let Claude read **and write** the CRM live in Google Sheets — no more download/upload of the `.xlsx`.

Server used: **[`xing5/mcp-google-sheets`](https://github.com/xing5/mcp-google-sheets)** (service-account auth, runs via `uvx`).

> **Where this works:** **Claude Code on desktop**, where you control the MCP config + network. It will **not** work in the Claude Code **web** session — that sandbox blocks Google's network and has no Google credentials. Do this setup on your Mac/PC.

---

## Overview

```
Claude Code (desktop) ──> mcp-google-sheets (uvx) ──> Google Sheets API ──> your CRM sheet
                                  ▲
                     authenticates as a Google
                     "service account" you create
```

A **service account** is a robot Google user with its own email. You share a Drive **folder** with that email; the MCP server acts as it.

The repo already contains a ready-to-use **`.mcp.json`** — you only need to (a) do the Google Cloud side and (b) set two environment variables.

---

## Prerequisites

- **Claude Code desktop** installed.
- **uv / uvx** installed (runs the server): `curl -LsSf https://astral.sh/uv/install.sh | sh`
  - macOS "spawn uvx ENOENT" → use the full path, e.g. `/Users/<you>/.local/bin/uvx`, in `.mcp.json`.

## Step 1 — Put the CRM in a Drive folder as a Google Sheet

1. In Google Drive, create a folder, e.g. **"Spencer CRM"**.
2. Upload `references/crm/Spencer_Kommons_CRM_v3.xlsx` into it.
3. Open it → **File → Save as Google Sheets** (native format).
4. Grab two IDs from the URLs:
   - **Spreadsheet ID:** `https://docs.google.com/spreadsheets/d/`**`<SPREADSHEET_ID>`**`/edit`
   - **Folder ID:** open the folder → `https://drive.google.com/drive/folders/`**`<FOLDER_ID>`**

> Note: Sheets may not render the dashboard's drawings identically. The data carries over fine; rebuild dashboard visuals natively if you care about them.

## Step 2 — Create a service account + key

1. <https://console.cloud.google.com/> → create a project (e.g. "spencer-crm").
2. **APIs & Services → Library** → enable **Google Sheets API** *and* **Google Drive API**.
3. **APIs & Services → Credentials → Create credentials → Service account** (name e.g. `crm-bot`).
4. Open it → **Keys → Add key → Create new key → JSON** → downloads a `.json`. **Keep it secret.**
5. Copy the service account **email** (e.g. `crm-bot@spencer-crm.iam.gserviceaccount.com`).

## Step 3 — Share the folder with the service account

In Drive, right-click the **"Spencer CRM" folder → Share** → paste the service account email → **Editor** → Share. (Sharing the folder covers the sheet inside it.)

## Step 4 — Store the key file safely

- Save the JSON key **outside the repo**, e.g. `~/.config/spencer-crm/service-account.json`.
- **Never commit it.** `.gitignore` already blocks service-account key patterns.

## Step 5 — Configure the MCP server

The repo's **`.mcp.json`** already defines the server using two env vars (so no secrets/paths live in the repo):

```json
{
  "mcpServers": {
    "google-sheets": {
      "command": "uvx",
      "args": ["mcp-google-sheets@latest"],
      "env": {
        "SERVICE_ACCOUNT_PATH": "${GOOGLE_SHEETS_SA_PATH}",
        "DRIVE_FOLDER_ID": "${GOOGLE_DRIVE_FOLDER_ID}"
      }
    }
  }
}
```

Set the two variables in your shell profile (`~/.zshrc` / `~/.bashrc`), then restart your terminal:

```bash
export GOOGLE_SHEETS_SA_PATH="$HOME/.config/spencer-crm/service-account.json"
export GOOGLE_DRIVE_FOLDER_ID="<FOLDER_ID from Step 1>"
```

(Prefer the CLI instead of the file? `claude mcp add google-sheets --env SERVICE_ACCOUNT_PATH=$GOOGLE_SHEETS_SA_PATH --env DRIVE_FOLDER_ID=$GOOGLE_DRIVE_FOLDER_ID -- uvx mcp-google-sheets@latest`)

## Step 6 — Launch & verify

1. Start Claude Code **desktop** in this repo. It will prompt to approve the `google-sheets` MCP server — approve it.
2. Run `/mcp` → confirm `google-sheets` is **connected**.
3. Ask: *"List my spreadsheets"* then *"read the Active Leads tab of the CRM."*
4. Test one small **write** on a scratch cell before trusting live data.

## Step 7 — Point the assistant at the sheet

Once live, tell me the **Spreadsheet ID** and I'll update `context/work.md` + `.claude/rules/crm-rules.md` to treat the Google Sheet as the source of truth (and keep the repo `.xlsx` as a periodic backup).

---

## Security notes

- The JSON key = edit access as that service account. Treat it like a password. Never paste it in chat or commit it.
- **Least privilege:** the service account should only have access to the "Spencer CRM" folder.
- The CRM holds client **PII** (names, phones, WeChat IDs) — keep folder sharing tight (you + service account only). Do **not** leave the sheet on "anyone with the link."
- If the key leaks: delete it in Cloud Console (**Keys → delete**) and create a new one.

## Fallback

Not ready? Stay on the repo `.xlsx` — I edit it, you sync. Revisit at first hire.
