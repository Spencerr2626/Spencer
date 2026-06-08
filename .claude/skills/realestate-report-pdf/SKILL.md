---
name: realestate-report-pdf
description: Professional PDF Property Report Generator — compiles all PROPERTY-*.md analysis files into a polished, client-ready PDF with score gauges, comparison tables, financial projections, and investment recommendations
version: 1.0.0
author: AI Real Estate Analyst
tags: [realestate, report, pdf, professional, client-ready, property-report]
command: /realestate report-pdf
output: PROPERTY-REPORT.pdf
---

# Professional PDF Property Report Generator

You are the PDF Report Generator for the AI Real Estate Analyst system. When invoked with `/realestate report-pdf`, you scan for all existing PROPERTY-*.md files in the current directory, extract the key data, scores, and analysis, compile everything into a structured JSON payload, and generate a polished, client-ready PDF report using the dedicated Python script.

**DISCLAIMER: For educational/research purposes only. Not financial or investment advice. All estimates are AI-generated approximations. Always verify with licensed real estate professionals before making any purchase or investment decisions.**

---

## PURPOSE

Markdown reports are great for working analysis, but clients, agents, and investors need professional PDF deliverables. This skill transforms raw analysis files into a visually polished PDF with score gauges, data tables, financial projections, charts, and a clear investment recommendation — the kind of report you can attach to an email, present in a meeting, or hand to a lender.

---

## TRIGGER

This skill activates when the user runs:
- `/realestate report-pdf` — generate a PDF from all available analysis files
- `/realestate report-pdf <address>` — generate a PDF for a specific property
- Also triggered by "generate PDF", "create PDF report", "make a client report", or "professional report"

---

## EXECUTION PIPELINE

### STEP 1: CHECK FOR PDF GENERATION SCRIPT

First, verify the dedicated Python script exists:

```bash
ls ~/.claude/skills/realestate/scripts/generate_realestate_pdf.py 2>/dev/null
```

**If the script exists:** Use it directly (proceed to Step 2).
**If the script does not exist:** Generate the PDF inline using ReportLab (follow all steps and build the PDF generation code dynamically).

### STEP 2: SCAN FOR ANALYSIS FILES

Search the current working directory for all PROPERTY-*.md files:

```bash
ls -t PROPERTY-*.md 2>/dev/null
```

**Primary data sources (check for all of these):**

| File Pattern | Data It Contains | PDF Section |
|-------------|-----------------|-------------|
| `PROPERTY-ANALYSIS-*.md` | Full analysis with composite Property Score | Cover page, all sections |
| `PROPERTY-COMPS-*.md` | Comparable sales, price per sqft, value estimate | Comp Analysis section |
| `PROPERTY-RENTAL-*.md` | Rental income, cash flow, cap rate | Cash Flow Projections section |
| `PROPERTY-NEIGHBORHOOD-*.md` | Schools, safety, walkability, demographics | Neighborhood Scores section |
| `PROPERTY-INVEST-*.md` | Investment scenarios, ROI, strategies | Investment Analysis section |
| `PROPERTY-MARKET-*.md` | Market conditions, trends, inventory | Market Conditions section |
| `PROPERTY-FLIP-*.md` | Rehab budget, ARV, flip profit estimate | Flip Analysis section |
| `PROPERTY-COMMERCIAL-*.md` | NOI, cap rate, lease analysis | Commercial Analysis section |
| `PROPERTY-MORTGAGE.md` | Payment calculator, affordability | Mortgage section |
| `PROPERTY-COMPARE.md` | Side-by-side comparison | Comparison section |
| `PROPERTY-LISTING-*.md` | MLS listing description | Listing section |
| `PROPERTY-SCREEN-*.md` | Screener results | Screening section |

**Find the most recent version of each:**

```bash
ls -t PROPERTY-ANALYSIS-*.md 2>/dev/null | head -1
ls -t PROPERTY-COMPS-*.md 2>/dev/null | head -1
ls -t PROPERTY-RENTAL-*.md 2>/dev/null | head -1
ls -t PROPERTY-NEIGHBORHOOD-*.md 2>/dev/null | head -1
ls -t PROPERTY-INVEST-*.md 2>/dev/null | head -1
ls -t PROPERTY-MARKET-*.md 2>/dev/null | head -1
```

**If no previous data exists:**
1. Recommend the user run `/realestate analyze <address>` first for the best results
2. If the user insists, ask for the property address and run a quick data collection using WebSearch to build the data structure from scratch
3. At minimum, run the equivalent of `/realestate quick <address>` to populate basic scores

### STEP 3: EXTRACT DATA FROM ANALYSIS FILES

Read each found file and extract the key data points into a structured format.

### STEP 4: BUILD THE JSON DATA STRUCTURE

Assemble all extracted data into a structured JSON payload for the PDF generator.

### STEP 5: GENERATE THE PDF

Run the PDF generation script:

```bash
python3 ~/.claude/skills/realestate/scripts/generate_realestate_pdf.py
```

**If the script does not exist**, generate the PDF inline using Python and ReportLab. The inline script must produce a PDF with the following sections:

#### PDF SECTIONS AND LAYOUT

**Page 1: Cover Page**
- Report title: "Property Analysis Report"
- Property address (large, centered)
- Property Score gauge (circular, color-coded: green 70+, yellow 40-69, red 0-39)
- Grade and Signal displayed prominently
- Report date
- Disclaimer footer

**Page 2: Property Overview**
- Property details table (price, beds, baths, sqft, lot, year, type)
- Executive summary (2-4 sentences)
- Key findings list (bulleted, top 5)

**Page 3: Comparable Sales Analysis**
- Comp table: address, price, RM/psf, beds/baths, distance, sale date
- Estimated value vs listing price
- Over/under priced assessment with percentage

**Page 4: Cash Flow Projections**
- Rental income estimate
- Monthly expense breakdown table
- Net monthly cash flow (highlighted, green if positive, red if negative)
- Key return metrics: Gross Yield, Net Yield, GRM
- 3-scenario comparison (Conservative, Moderate, Optimistic)

**Page 5: Neighborhood Scorecard**
- School ratings with bar visualization
- Safety rating
- Expat demand assessment
- Amenities & connectivity
- Growth outlook

**Page 6: Investment Analysis**
- Category scores bar chart (all 5 categories)
- Strategy comparison (Buy & Hold vs Renovate & Hold vs Flip)
- Risk level assessment
- RPGT considerations

**Page 7: Market Conditions**
- Market type indicator (buyer/seller/balanced)
- Median PSF trends
- Economic drivers
- Supply pipeline assessment
- MM2H impact

**Page 8: Recommendation & Next Steps**
- Overall recommendation (highlighted)
- Signal with explanation
- Key action items
- Full disclaimer

#### PDF STYLING

| Element | Style |
|---------|-------|
| Colors | Navy (#1B2A4A) headers, dark gray (#333) body, green (#2E7D32) positive, red (#C62828) negative |
| Fonts | Helvetica-Bold for headers, Helvetica for body |
| Score gauges | Circular arc gauges with color gradient (red -> yellow -> green) |
| Tables | Alternating row colors (white/#F5F5F5), navy header row |
| Charts | Horizontal bar charts for category scores and comparisons |
| Footer | Page numbers, disclaimer, generation date |
| Margins | 50pt top, 40pt sides, 50pt bottom |

### STEP 6: VERIFY AND DELIVER

After PDF generation confirm:
- File name and location
- File size
- Number of pages
- Which data sources were included

---

## OUTPUT SPECIFICATIONS

| Spec | Value |
|------|-------|
| File name | `PROPERTY-REPORT.pdf` (or `PROPERTY-REPORT-[ADDRESS].pdf` if address specified) |
| Page size | Letter (8.5" x 11") |
| Orientation | Portrait |
| Pages | 6-10 depending on available data |
| File size | Typically 200KB - 1MB |
| Python dependency | ReportLab (`pip install reportlab` if not installed) |

---

## RULES

1. **Professional quality** — The PDF must look like it came from a real estate analytics firm
2. **Data-driven** — Every number in the PDF must come from the analysis files or live research; never fabricate data
3. **Conservative estimates** — Use the same conservative projections from the analysis files
4. **Complete disclaimer** — Full disclaimer must appear on the cover page and the last page
5. **Graceful degradation** — If some analysis files are missing, mark missing sections as "Not analyzed"
6. **Install dependencies** — If ReportLab is not installed, install it automatically
7. **Color-coded scores** — All scores must be color-coded: green (70+), yellow (40-69), red (0-39)

## DEPENDENCY INSTALLATION

If ReportLab is not available, install it:

```bash
pip install reportlab 2>/dev/null || pip3 install reportlab 2>/dev/null
```

---

**DISCLAIMER: For educational/research purposes only. Not financial or investment advice. All estimates are AI-generated approximations based on publicly available data. Always verify with licensed professionals and conduct your own due diligence before making any purchase or investment decisions.**
