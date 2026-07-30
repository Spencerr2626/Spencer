# Monthly Progress Report

Generate Spencer's branded **one-page business progress report (PDF)** from the live CRM.

## When to use

- **Month-end (scheduled):** produce the standing month-end report automatically.
- **On demand:** when Spencer asks for "my progress", "progress report", "how am I doing", or "make me the progress PDF".

## What it does

Reads `references/crm/Spencer_Kommons_CRM_v3.xlsx` (Dashboard + Pipeline sheets) and renders a
one-page A4 PDF into `reports/Spencer_Progress_Report_<YYYY-MM-DD>.pdf` containing:

- **Hero band** — GCI realized (YTD), signed & advanced total, projected-if-closed.
- **Under contract / near-close** — table of signed/advanced pipeline deals + your commission.
- **Early pipeline** — viewing/shortlisting-stage deals.
- **Snapshot** — active leads, done deals, pipeline value, est. commission.
- **Momentum line** — auto-written from the numbers.

The report is **data-driven**: it always reflects whatever is currently logged in the CRM.
Deals are auto-classified by their Pipeline `Stage` text (done / signed / early).

## Steps

1. Make sure the CRM is current (log any pending updates first).
2. Ensure Python deps are available (fresh containers have no venv):
   ```bash
   python3 -m venv /tmp/venv 2>/dev/null; /tmp/venv/bin/pip install -q openpyxl reportlab
   ```
   (The system CJK font `wqy-zenhei` is used automatically for Chinese names; the script
   falls back gracefully if it is missing.)
3. Generate, passing today's date explicitly (avoids sandbox clock drift):
   ```bash
   /tmp/venv/bin/python .claude/skills/monthly-progress-report/generate.py <YYYY-MM-DD>
   ```
4. **Send the PDF to Spencer** (SendUserFile, display: render).
5. **Commit** the new PDF in `reports/` to the working branch and push.

## Notes

- Keep the report to **one page**. If deals grow long, tighten column widths in `generate.py`
  rather than spilling to a second page.
- GCI realized is read from Dashboard cell `J5`; the projection = realized GCI + sum of
  signed/advanced pipeline commissions.
- Numbers come straight from the CRM, so accuracy depends on the CRM being up to date.
