#!/usr/bin/env python3
"""Generate PROPERTY-INVEST-Verve-Suites-MontKiara.pdf from the markdown analysis."""

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, PageBreak
)
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.platypus.flowables import Flowable
from reportlab.pdfgen import canvas as pdfcanvas
import math

# ── Colours ────────────────────────────────────────────────────────────────
NAVY   = colors.HexColor("#1B3A5C")
TEAL   = colors.HexColor("#0A7E8C")
GOLD   = colors.HexColor("#C8A951")
AMBER  = colors.HexColor("#E87722")
RED    = colors.HexColor("#C0392B")
GREEN  = colors.HexColor("#1E8449")
LGRAY  = colors.HexColor("#F5F5F5")
MGRAY  = colors.HexColor("#CCCCCC")
DGRAY  = colors.HexColor("#555555")
WHITE  = colors.white
BLACK  = colors.black

W, H = A4

# ── Score gauge ────────────────────────────────────────────────────────────
class ScoreGauge(Flowable):
    def __init__(self, score, label="Investment Score", width=160, height=90):
        Flowable.__init__(self)
        self.score = score
        self.label = label
        self.width = width
        self.height = height

    def draw(self):
        c = self.canv
        cx, cy = self.width / 2, 28
        r = 44
        # background arc (gray)
        c.setStrokeColor(MGRAY)
        c.setLineWidth(10)
        c.arc(cx - r, cy - r, cx + r, cy + r, 0, 180)
        # score arc
        pct = self.score / 100
        sweep = 180 * pct
        if self.score >= 70:
            ac = GREEN
        elif self.score >= 55:
            ac = AMBER
        else:
            ac = RED
        c.setStrokeColor(ac)
        c.setLineWidth(10)
        c.arc(cx - r, cy - r, cx + r, cy + r, 0, sweep)
        # score text
        c.setFillColor(NAVY)
        c.setFont("Helvetica-Bold", 26)
        c.drawCentredString(cx, cy - 6, str(self.score))
        c.setFont("Helvetica", 9)
        c.setFillColor(DGRAY)
        c.drawCentredString(cx, cy - 18, "/ 100")
        c.setFont("Helvetica-Bold", 9)
        c.setFillColor(NAVY)
        c.drawCentredString(cx, self.height - 10, self.label)

class ScoreBar(Flowable):
    def __init__(self, label, score, max_score=100, width=320, height=18):
        Flowable.__init__(self)
        self.label = label
        self.score = score
        self.max_score = max_score
        self.width = width
        self.height = height

    def draw(self):
        c = self.canv
        bar_x = 120
        bar_w = self.width - bar_x - 40
        bar_h = 10
        bar_y = (self.height - bar_h) / 2
        c.setFont("Helvetica", 8)
        c.setFillColor(DGRAY)
        c.drawString(0, bar_y + 1, self.label)
        c.setFillColor(LGRAY)
        c.rect(bar_x, bar_y, bar_w, bar_h, fill=1, stroke=0)
        pct = self.score / self.max_score
        fc = GREEN if pct >= 0.70 else (AMBER if pct >= 0.55 else RED)
        c.setFillColor(fc)
        c.rect(bar_x, bar_y, bar_w * pct, bar_h, fill=1, stroke=0)
        c.setFont("Helvetica-Bold", 8)
        c.setFillColor(NAVY)
        c.drawString(bar_x + bar_w + 4, bar_y + 1, f"{self.score}")

# ── Helpers ────────────────────────────────────────────────────────────────
def styles():
    s = getSampleStyleSheet()
    base = dict(fontName="Helvetica", fontSize=9, leading=13, textColor=BLACK)

    def ps(name, **kw):
        d = {**base, **kw}
        return ParagraphStyle(name, **d)

    return {
        "h1":    ps("h1",  fontName="Helvetica-Bold", fontSize=20, textColor=WHITE,    spaceAfter=4,  leading=24),
        "h2":    ps("h2",  fontName="Helvetica-Bold", fontSize=13, textColor=NAVY,     spaceAfter=4,  leading=16),
        "h3":    ps("h3",  fontName="Helvetica-Bold", fontSize=10, textColor=TEAL,     spaceAfter=3,  leading=13),
        "body":  ps("body",                                                             spaceAfter=4),
        "small": ps("small", fontSize=7.5, textColor=DGRAY,                            spaceAfter=3),
        "disc":  ps("disc",  fontSize=7,   textColor=DGRAY,  fontName="Helvetica-Oblique", spaceAfter=6),
        "badge": ps("badge", fontName="Helvetica-Bold", fontSize=11, textColor=GOLD,   alignment=TA_CENTER),
        "right": ps("right", alignment=TA_RIGHT, fontSize=8),
        "label": ps("label", fontName="Helvetica-Bold", fontSize=8, textColor=DGRAY),
    }

def hr():
    return HRFlowable(width="100%", thickness=0.5, color=MGRAY, spaceAfter=6, spaceBefore=4)

def sp(n=6):
    return Spacer(1, n)

def section_header(text, st):
    return [
        sp(8),
        Paragraph(text, st["h2"]),
        HRFlowable(width="100%", thickness=1.5, color=TEAL, spaceAfter=6),
    ]

def make_table(data, col_widths, header_bg=NAVY, stripe=True, font_size=8):
    ts = [
        ("BACKGROUND",  (0, 0), (-1, 0), header_bg),
        ("TEXTCOLOR",   (0, 0), (-1, 0), WHITE),
        ("FONTNAME",    (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE",    (0, 0), (-1, -1), font_size),
        ("ALIGN",       (1, 0), (-1, -1), "RIGHT"),
        ("ALIGN",       (0, 0), (0, -1), "LEFT"),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [WHITE, LGRAY] if stripe else [WHITE]),
        ("GRID",        (0, 0), (-1, -1), 0.3, MGRAY),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
        ("RIGHTPADDING",(0, 0), (-1, -1), 5),
        ("TOPPADDING",  (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING",(0,0), (-1, -1), 3),
    ]
    return Table(data, colWidths=col_widths, style=TableStyle(ts), repeatRows=1)

# ── Header / footer ────────────────────────────────────────────────────────
def on_page(canv, doc):
    canv.saveState()
    # header bar
    canv.setFillColor(NAVY)
    canv.rect(0, H - 1.8*cm, W, 1.8*cm, fill=1, stroke=0)
    canv.setFont("Helvetica-Bold", 10)
    canv.setFillColor(WHITE)
    canv.drawString(1.5*cm, H - 1.2*cm, "INVESTMENT ANALYSIS: VERVE SUITES, MONT KIARA")
    canv.setFont("Helvetica", 8)
    canv.setFillColor(GOLD)
    canv.drawRightString(W - 1.5*cm, H - 1.2*cm, "10 June 2026")
    # footer
    canv.setFillColor(NAVY)
    canv.rect(0, 0, W, 1.0*cm, fill=1, stroke=0)
    canv.setFont("Helvetica", 7)
    canv.setFillColor(MGRAY)
    canv.drawString(1.5*cm, 0.35*cm, "Not financial or investment advice. AI-generated estimates. Verify with BOVAEP-registered REN/REA & tax agent.")
    canv.setFillColor(GOLD)
    canv.drawRightString(W - 1.5*cm, 0.35*cm, f"Page {doc.page}")
    canv.restoreState()

# ── Cover page ─────────────────────────────────────────────────────────────
def cover_page(st):
    elems = []
    elems.append(Spacer(1, 2*cm))

    # title block
    title_data = [["INVESTMENT ANALYSIS"]]
    tt = Table(title_data, colWidths=[W - 4*cm])
    tt.setStyle(TableStyle([
        ("BACKGROUND",   (0,0), (-1,-1), NAVY),
        ("TEXTCOLOR",    (0,0), (-1,-1), WHITE),
        ("FONTNAME",     (0,0), (-1,-1), "Helvetica-Bold"),
        ("FONTSIZE",     (0,0), (-1,-1), 24),
        ("ALIGN",        (0,0), (-1,-1), "CENTER"),
        ("TOPPADDING",   (0,0), (-1,-1), 16),
        ("BOTTOMPADDING",(0,0), (-1,-1), 16),
    ]))
    elems.append(tt)
    elems.append(sp(4))

    sub_data = [["Verve Suites · Mont Kiara · Kuala Lumpur"]]
    st2 = Table(sub_data, colWidths=[W - 4*cm])
    st2.setStyle(TableStyle([
        ("BACKGROUND",   (0,0), (-1,-1), TEAL),
        ("TEXTCOLOR",    (0,0), (-1,-1), WHITE),
        ("FONTNAME",     (0,0), (-1,-1), "Helvetica-Bold"),
        ("FONTSIZE",     (0,0), (-1,-1), 13),
        ("ALIGN",        (0,0), (-1,-1), "CENTER"),
        ("TOPPADDING",   (0,0), (-1,-1), 10),
        ("BOTTOMPADDING",(0,0), (-1,-1), 10),
    ]))
    elems.append(st2)
    elems.append(sp(20))

    # score gauge centre
    gauge_data = [[ScoreGauge(59, "Investment Score", 160, 90)]]
    gt = Table(gauge_data, colWidths=[W - 4*cm])
    gt.setStyle(TableStyle([("ALIGN",(0,0),(-1,-1),"CENTER")]))
    elems.append(gt)
    elems.append(sp(10))

    # key stats row
    key_data = [
        ["Best Strategy", "Buy & Hold"],
        ["Property", "Freehold Serviced Residence"],
        ["Completed", "2015"],
        ["Units", "881 across 4 towers"],
        ["Median Transacted PSF", "RM 866 (Jun 2024–Apr 2025)"],
        ["Entry (1-bed model)", "~RM 580,000"],
        ["Gross Rental Yield", "~4.1%"],
        ["Monthly Top-up (90% MOF)", "~RM 935"],
        ["Hold Target", "7–10 years (exit Yr6+ for 0% RPGT)"],
    ]
    kt = Table(key_data, colWidths=[6*cm, 9*cm])
    kt.setStyle(TableStyle([
        ("FONTNAME",  (0,0), (0,-1), "Helvetica-Bold"),
        ("FONTNAME",  (1,0), (1,-1), "Helvetica"),
        ("FONTSIZE",  (0,0), (-1,-1), 9),
        ("ROWBACKGROUNDS", (0,0), (-1,-1), [LGRAY, WHITE]),
        ("GRID",      (0,0), (-1,-1), 0.3, MGRAY),
        ("LEFTPADDING",(0,0),(-1,-1), 8),
        ("TOPPADDING",(0,0),(-1,-1), 4),
        ("BOTTOMPADDING",(0,0),(-1,-1), 4),
        ("TEXTCOLOR", (0,0), (0,-1), NAVY),
    ]))
    elems.append(kt)
    elems.append(sp(16))

    elems.append(Paragraph(
        "DISCLAIMER: For educational and research purposes only. Not financial, investment, or tax advice. "
        "All estimates are AI-generated approximations. Always verify with a BOVAEP-registered REN/REA, licensed banker, and tax agent.",
        st["disc"]
    ))
    elems.append(PageBreak())
    return elems

# ── Main build ─────────────────────────────────────────────────────────────
def build_pdf():
    path = "PROPERTY-INVEST-Verve-Suites-MontKiara.pdf"
    doc = SimpleDocTemplate(
        path, pagesize=A4,
        leftMargin=1.8*cm, rightMargin=1.8*cm,
        topMargin=2.2*cm, bottomMargin=1.6*cm,
    )
    st = styles()
    elems = []

    # ── Cover ─────────────────────────────────────────────────────────────
    elems += cover_page(st)

    # ── Property Profile ──────────────────────────────────────────────────
    elems += section_header("Property Investment Profile", st)
    profile = [
        ["Field", "Value"],
        ["Project", "Verve Suites, 5 Jalan Kiara 5, Mont Kiara, KL"],
        ["Developer", "Bukit Kiara Properties Sdn Bhd"],
        ["Type", "Freehold Serviced Residence (commercial strata title)"],
        ["Tenure", "Freehold"],
        ["Completed (VP)", "2015"],
        ["Blocks / Units", "4 towers (Viva, Vibe, Vogue, Vox) / 881 units"],
        ["Built-up Range", "462 sq ft (studio) — 1,394 sq ft (3-bed)"],
        ["Median Transacted PSF", "RM 866 (Jun 2024–Apr 2025, brickz, 21 txns)"],
        ["Asking PSF", "~RM 869 (iProperty)"],
        ["Typical Rent", "Studio RM 1,800–2,200 · 1-bed RM 2,300–2,700 · 2-bed RM 3,000–4,000"],
        ["Maintenance Fee", "RM 0.33 psf/mo (commercial utility tariff applies)"],
        ["Appreciation Rate", "2–3%/yr (Mont Kiara 2025 consensus)"],
        ["Mortgage Rate", "~4.4% p.a. (BNM OPR-linked floating)"],
    ]
    elems.append(make_table(profile, [5*cm, 11.5*cm], font_size=8))
    elems.append(sp(6))
    elems.append(Paragraph(
        "⚠ Commercial Title: Verve Suites is a serviced residence on commercial strata title — utilities billed at commercial rates "
        "(~20–30% higher). Confirm bank's MOF policy for commercial-title properties before committing.",
        st["small"]
    ))

    # ── Strategy Dashboard ────────────────────────────────────────────────
    elems += section_header("Strategy Comparison Dashboard", st)
    dash = [
        ["Metric", "Buy & Hold", "BRRRR", "Renovate & Resell"],
        ["Feasibility Score", "65/100", "58/100", "48/100"],
        ["Model Unit", "1-bed 672 sf @ RM 580K", "Studio 462 sf @ RM 480K distressed", "1-bed 672 sf @ RM 560K"],
        ["Total Cash Required", "~RM 86K (90% MOF)", "~RM 105K", "~RM 165K"],
        ["Income / Return Target", "RM 2,400/mo rent", "RM 2,100/mo post-reno", "ARV RM 638K (loss pre-RPGT)"],
        ["Timeline", "7–10 yr hold", "~6 mo to stabilise", "12–18 mo (if viable)"],
        ["Risk Level", "Moderate", "Moderate–High", "High"],
        ["Best For", "Expat landlord; patient", "Tight capital, refi-recycle", "Not recommended"],
    ]
    dash_ts = TableStyle([
        ("BACKGROUND",   (0,0), (-1,0), NAVY),
        ("TEXTCOLOR",    (0,0), (-1,0), WHITE),
        ("FONTNAME",     (0,0), (-1,0), "Helvetica-Bold"),
        ("FONTNAME",     (0,1), (0,-1), "Helvetica-Bold"),
        ("FONTSIZE",     (0,0), (-1,-1), 8),
        ("ALIGN",        (1,0), (-1,-1), "CENTER"),
        ("ALIGN",        (0,0), (0,-1), "LEFT"),
        ("ROWBACKGROUNDS",(0,1),(-1,-1), [WHITE, LGRAY]),
        ("GRID",         (0,0), (-1,-1), 0.3, MGRAY),
        ("LEFTPADDING",  (0,0),(-1,-1), 5),
        ("TOPPADDING",   (0,0),(-1,-1), 3),
        ("BOTTOMPADDING",(0,0),(-1,-1), 3),
        ("TEXTCOLOR",    (1,1),(1,1), GREEN),
        ("TEXTCOLOR",    (3,1),(3,1), RED),
        ("BACKGROUND",   (1,0),(1,0), GREEN),
        ("BACKGROUND",   (3,0),(3,0), RED),
    ])
    dt = Table(dash, colWidths=[4.5*cm, 4*cm, 4*cm, 4*cm])
    dt.setStyle(dash_ts)
    elems.append(dt)

    # ── Score bars ────────────────────────────────────────────────────────
    elems += section_header("Investment Score Breakdown", st)
    bars = [("Buy & Hold", 65), ("BRRRR", 58), ("Renovate & Resell", 48), ("Composite", 59)]
    for lbl, scr in bars:
        elems.append(ScoreBar(lbl, scr, width=380))
        elems.append(sp(3))

    elems.append(sp(6))
    score_detail = [
        ["Strategy", "Score", "Weight", "Weighted"],
        ["Buy & Hold", "65", "45%", "29.3"],
        ["BRRRR", "58", "35%", "20.3"],
        ["Renovate & Resell", "48", "20%", "9.6"],
        ["COMPOSITE", "59", "—", "59.2"],
    ]
    sdt = Table(score_detail, colWidths=[6*cm, 3*cm, 3*cm, 4.5*cm])
    sdt.setStyle(TableStyle([
        ("BACKGROUND",   (0,0), (-1,0), NAVY),
        ("TEXTCOLOR",    (0,0), (-1,0), WHITE),
        ("FONTNAME",     (0,0), (-1,0), "Helvetica-Bold"),
        ("FONTNAME",     (0,-1),(-1,-1), "Helvetica-Bold"),
        ("BACKGROUND",   (0,-1),(-1,-1), TEAL),
        ("TEXTCOLOR",    (0,-1),(-1,-1), WHITE),
        ("FONTSIZE",     (0,0), (-1,-1), 9),
        ("ALIGN",        (1,0), (-1,-1), "CENTER"),
        ("ALIGN",        (0,0), (0,-1), "LEFT"),
        ("ROWBACKGROUNDS",(0,1),(-1,-2), [WHITE, LGRAY]),
        ("GRID",         (0,0), (-1,-1), 0.3, MGRAY),
        ("LEFTPADDING",  (0,0),(-1,-1), 6),
        ("TOPPADDING",   (0,0),(-1,-1), 4),
        ("BOTTOMPADDING",(0,0),(-1,-1), 4),
    ]))
    elems.append(sdt)

    elems.append(PageBreak())

    # ── Strategy 1: Buy & Hold ────────────────────────────────────────────
    elems += section_header("Strategy 1: Buy & Hold — 1-Bed 672 sq ft @ RM 580,000", st)

    elems.append(Paragraph("Acquisition & Financing", st["h3"]))
    acq = [
        ["Parameter", "90% MOF (1st/2nd)", "70% MOF (3rd+)"],
        ["Purchase Price", "RM 580,000", "RM 580,000"],
        ["Loan Amount", "RM 522,000", "RM 406,000"],
        ["Down Payment", "RM 58,000", "RM 174,000"],
        ["MOT Stamp Duty (~2.5%)", "RM 12,400", "RM 12,400"],
        ["Loan Stamp Duty (0.5%)", "RM 2,610", "RM 2,030"],
        ["Legal Fees (est.)", "RM 8,000", "RM 8,000"],
        ["Immediate Repairs", "RM 5,000", "RM 5,000"],
        ["TOTAL CASH INVESTED", "~RM 86,000", "~RM 201,400"],
    ]
    elems.append(make_table(acq, [5.5*cm, 5.5*cm, 5.5*cm], font_size=8))
    elems.append(sp(6))

    elems.append(Paragraph("Annual Cash Flow (90% MOF, 4.4%, 35yr, 7% vacancy)", st["h3"]))
    cf = [
        ["Line Item", "Year 1", "Year 3", "Year 5", "Year 10"],
        ["Gross Monthly Rent", "RM 2,400", "RM 2,520", "RM 2,648", "RM 3,020"],
        ["Gross Annual Rent", "RM 28,800", "RM 30,240", "RM 31,776", "RM 36,240"],
        ["Vacancy (7%)", "–RM 2,016", "–RM 2,117", "–RM 2,224", "–RM 2,537"],
        ["Maintenance Fee", "–RM 2,661", "–RM 2,741", "–RM 2,823", "–RM 3,084"],
        ["CapEx / Repairs (5%)", "–RM 1,440", "–RM 1,512", "–RM 1,589", "–RM 1,812"],
        ["Fire Insurance", "–RM 600", "–RM 600", "–RM 600", "–RM 600"],
        ["Assessment + Quit Rent", "–RM 1,200", "–RM 1,200", "–RM 1,200", "–RM 1,200"],
        ["Agent Fee (renewal, amort.)", "–RM 2,400", "–RM 2,520", "–RM 2,648", "–RM 3,020"],
        ["NOI", "RM 18,483", "RM 19,550", "RM 20,692", "RM 23,987"],
        ["Mortgage Instalment", "–RM 29,712", "–RM 29,712", "–RM 29,712", "–RM 29,712"],
        ["NET CASH FLOW", "–RM 11,229", "–RM 10,162", "–RM 9,020", "–RM 5,725"],
    ]
    cft = Table(cf, colWidths=[5*cm, 3.2*cm, 3.2*cm, 3.2*cm, 3.2*cm])
    cft.setStyle(TableStyle([
        ("BACKGROUND",   (0,0), (-1,0), NAVY),
        ("TEXTCOLOR",    (0,0), (-1,0), WHITE),
        ("FONTNAME",     (0,0), (-1,0), "Helvetica-Bold"),
        ("FONTNAME",     (0,-1),(-1,-1), "Helvetica-Bold"),
        ("FONTNAME",     (0,9), (0,9),  "Helvetica-Bold"),
        ("BACKGROUND",   (0,-1),(-1,-1), colors.HexColor("#F2DEDE")),
        ("BACKGROUND",   (0,9), (-1,9),  colors.HexColor("#DFF0D8")),
        ("FONTSIZE",     (0,0), (-1,-1), 8),
        ("ALIGN",        (1,0), (-1,-1), "RIGHT"),
        ("ALIGN",        (0,0), (0,-1), "LEFT"),
        ("ROWBACKGROUNDS",(0,1),(-1,-2), [WHITE, LGRAY]),
        ("GRID",         (0,0), (-1,-1), 0.3, MGRAY),
        ("LEFTPADDING",  (0,0),(-1,-1), 5),
        ("TOPPADDING",   (0,0),(-1,-1), 3),
        ("BOTTOMPADDING",(0,0),(-1,-1), 3),
    ]))
    elems.append(cft)
    elems.append(sp(4))
    elems.append(Paragraph(
        "Negative leveraged cash flow (~RM 935/mo top-up) is expected and normal for Mont Kiara at 90% MOF. "
        "This is an appreciation + equity play. Gross yield ~4.1%; net yield ~3.2%.",
        st["small"]
    ))

    elems.append(sp(8))
    elems.append(Paragraph("Appreciation & Equity Buildup (2.5%/yr)", st["h3"]))
    eq = [
        ["Year", "Property Value", "Appreciation Gain", "Loan Balance", "Equity"],
        ["0", "RM 580,000", "—", "RM 522,000", "RM 58,000"],
        ["1", "RM 594,500", "RM 14,500", "RM 519,780", "RM 74,720"],
        ["3", "RM 624,300", "RM 44,300", "RM 515,100", "RM 109,200"],
        ["5", "RM 655,600", "RM 75,600", "RM 509,800", "RM 145,800"],
        ["10", "RM 743,000", "RM 163,000", "RM 493,600", "RM 249,400"],
    ]
    elems.append(make_table(eq, [2*cm, 3.8*cm, 3.8*cm, 3.8*cm, 3.8*cm], font_size=8))

    elems.append(sp(8))
    elems.append(Paragraph("Total Return — Buy & Hold", st["h3"]))
    ret = [
        ["Component", "5-Year", "10-Year"],
        ["Cumulative Net Cash Flow", "–RM 50,500", "–RM 83,700"],
        ["Appreciation Gain", "RM 75,600", "RM 163,000"],
        ["Principal Paydown", "RM 12,200", "RM 28,400"],
        ["Less: RPGT (0% if sold Yr6+)", "RM 0", "RM 0"],
        ["Less: Selling Costs (~4%)", "–RM 26,200", "–RM 29,700"],
        ["NET TOTAL RETURN", "~RM 11,100", "~RM 78,000"],
        ["Annualized ROI on Cash (90% MOF)", "~2.6%", "~9.1%"],
    ]
    rt = Table(ret, colWidths=[8*cm, 4*cm, 4*cm])
    rt.setStyle(TableStyle([
        ("BACKGROUND",   (0,0), (-1,0), NAVY),
        ("TEXTCOLOR",    (0,0), (-1,0), WHITE),
        ("FONTNAME",     (0,0), (-1,0), "Helvetica-Bold"),
        ("FONTNAME",     (0,-2),(-1,-1), "Helvetica-Bold"),
        ("BACKGROUND",   (0,-2),(-1,-1), TEAL),
        ("TEXTCOLOR",    (0,-2),(-1,-1), WHITE),
        ("FONTSIZE",     (0,0), (-1,-1), 8.5),
        ("ALIGN",        (1,0), (-1,-1), "RIGHT"),
        ("ALIGN",        (0,0), (0,-1), "LEFT"),
        ("ROWBACKGROUNDS",(0,1),(-1,-3), [WHITE, LGRAY]),
        ("GRID",         (0,0), (-1,-1), 0.3, MGRAY),
        ("LEFTPADDING",  (0,0),(-1,-1), 6),
        ("TOPPADDING",   (0,0),(-1,-1), 4),
        ("BOTTOMPADDING",(0,0),(-1,-1), 4),
    ]))
    elems.append(rt)
    elems.append(sp(4))
    elems.append(Paragraph(
        "⚠ Do NOT sell before Year 6 — RPGT (15% in Yr5) on a RM 76K gain = RM 11,400 avoidable tax. "
        "The 10-year hold is where the return becomes meaningful.",
        st["small"]
    ))

    elems.append(PageBreak())

    # ── Malaysian Tax Treatment ───────────────────────────────────────────
    elems += section_header("Malaysian Tax Treatment — Rental Income", st)
    elems.append(Paragraph(
        "Malaysia does NOT allow residential property depreciation for individuals (unlike US 27.5-yr rule). "
        "Rental income is taxed at scaled personal rates. Only specific cash expenses are deductible.",
        st["body"]
    ))
    tax = [
        ["Deductible Expense", "Notes"],
        ["Loan interest portion", "Interest component of monthly instalment only (~RM 1,900/mo Year 1)"],
        ["Assessment (Cukai Pintu)", "~RM 900/yr"],
        ["Quit Rent (Cukai Tanah)", "~RM 300/yr"],
        ["Fire insurance premium", "~RM 600/yr"],
        ["Maintenance fee + sinking fund", "~RM 2,661/yr"],
        ["Repairs & maintenance", "To maintain (not improve) — keep receipts"],
        ["Renewal agent commission", "For lease renewal only — first-letting fee is capital"],
    ]
    elems.append(make_table(tax, [5.5*cm, 11*cm], font_size=8))
    elems.append(sp(6))
    not_ded = [
        ["NOT Deductible", "Notes"],
        ["Principal repayment", "Capital in nature"],
        ["Depreciation", "NO residential depreciation allowance for individuals in Malaysia"],
        ["Initial renovation / first-fit-out", "Capital — but adds to RPGT cost base on disposal"],
        ["First-letting agent commission", "Capital"],
    ]
    not_t = Table(not_ded, colWidths=[5.5*cm, 11*cm])
    not_t.setStyle(TableStyle([
        ("BACKGROUND",   (0,0), (-1,0), RED),
        ("TEXTCOLOR",    (0,0), (-1,0), WHITE),
        ("FONTNAME",     (0,0), (-1,0), "Helvetica-Bold"),
        ("FONTSIZE",     (0,0), (-1,-1), 8),
        ("ALIGN",        (0,0), (-1,-1), "LEFT"),
        ("ROWBACKGROUNDS",(0,1),(-1,-1), [colors.HexColor("#FDEDEC"), WHITE]),
        ("GRID",         (0,0), (-1,-1), 0.3, MGRAY),
        ("LEFTPADDING",  (0,0),(-1,-1), 6),
        ("TOPPADDING",   (0,0),(-1,-1), 3),
        ("BOTTOMPADDING",(0,0),(-1,-1), 3),
    ]))
    elems.append(not_t)

    elems.append(PageBreak())

    # ── Strategy 2: BRRRR ─────────────────────────────────────────────────
    elems += section_header("Strategy 2: BRRRR — Distressed Studio 462 sq ft @ RM 440K", st)

    brrrr = [
        ["Phase", "Detail", "Amount"],
        ["BUY", "Target Distressed Price", "RM 440,000"],
        ["BUY", "MOT Stamp Duty + Legal", "RM 13,400"],
        ["RENOVATE", "Full Cosmetic Reno Budget", "RM 50,000"],
        ["RENOVATE", "Reno Timeline", "2–3 months"],
        ["RENT", "Post-Reno Monthly Rent", "RM 2,100"],
        ["REFINANCE", "ARV (conservative estimate)", "RM 520,000"],
        ["REFINANCE", "Refi at 80% of ARV", "RM 416,000"],
        ["REFINANCE", "Original Loan (90% on RM440K)", "RM 396,000"],
        ["REPEAT", "Cash Returned from Refi", "RM 20,000"],
        ["REPEAT", "Cash Left in Deal (net)", "~RM 85,000"],
    ]
    elems.append(make_table(brrrr, [3*cm, 7*cm, 6.5*cm], font_size=8))

    elems.append(sp(8))
    elems.append(Paragraph("Renovation Budget — Studio 462 sq ft", st["h3"]))
    reno = [
        ["Category", "Scope", "Cost (RM)"],
        ["Kitchen cabinetry + countertop", "Full replacement", "RM 7,000"],
        ["Bathroom (×1)", "Tile, fittings, vanity", "RM 5,500"],
        ["Flooring (SPC throughout)", "462 sq ft", "RM 6,000"],
        ["Painting + false ceiling", "Throughout", "RM 4,000"],
        ["Wiring / DB upgrade + lighting", "LED + upgrade", "RM 3,500"],
        ["Air-conditioning (1 unit)", "New inverter", "RM 3,000"],
        ["Built-in carpentry", "Wardrobe + TV console", "RM 6,000"],
        ["Waterproofing (bathroom)", "", "RM 1,500"],
        ["Plumbing check", "", "RM 1,000"],
        ["Permits + disposal", "", "RM 1,500"],
        ["Contingency (15%)", "", "RM 6,000"],
        ["TOTAL RENO", "", "RM 45,000–55,000"],
    ]
    elems.append(make_table(reno, [6*cm, 5*cm, 5.5*cm], font_size=8))

    elems.append(sp(8))
    elems.append(Paragraph("BRRRR Financial Analysis", st["h3"]))
    bfin = [
        ["Metric", "Value"],
        ["Total All-In (purchase + stamps + reno)", "RM 503,400"],
        ["ARV (conservative)", "RM 520,000"],
        ["Equity Created", "RM 16,600 (~3% of ARV) — thin"],
        ["70% Rule (Purchase + Reno ≤ 70% of ARV)", "FAIL at asking price"],
        ["Post-Refi Monthly Cash Flow", "~–RM 430/mo"],
        ["Cash Left in Deal", "~RM 85,000"],
        ["Infinite Return?", "No — RM 85K still invested"],
    ]
    elems.append(make_table(bfin, [8*cm, 8.5*cm], font_size=8))
    elems.append(sp(4))
    elems.append(Paragraph(
        "⚠ BRRRR only works if entry price negotiated to RM 370–390K (rare). ARV confidence is LOW — "
        "thin renovated-unit transacted data on brickz for small studios. Get a licensed valuer's opinion before refinancing.",
        st["small"]
    ))

    elems.append(PageBreak())

    # ── Strategy 3: Flip ─────────────────────────────────────────────────
    elems += section_header("Strategy 3: Renovate & Resell (Flip)", st)
    elems.append(Paragraph(
        "Model: 1-bed 672 sq ft @ RM 560,000 entry · ARV RM 638,000 (RM 950 psf renovated)",
        st["body"]
    ))
    pl_data = [
        ["P&L Item", "Amount"],
        ["ARV (RM 950 psf × 672 sq ft)", "RM 638,000"],
        ["Less: Purchase Price", "–RM 560,000"],
        ["Less: Reno Budget (~RM 80 psf)", "–RM 53,800"],
        ["Less: Stamp Duty + Legal (buy)", "–RM 19,400"],
        ["Less: Holding Costs (6 months)", "–RM 12,500"],
        ["Less: Selling Costs (agent + legal)", "–RM 17,200"],
        ["GROSS GAIN (before RPGT)", "–RM 24,900 (LOSS)"],
    ]
    plt = Table(pl_data, colWidths=[9*cm, 7.5*cm])
    plt.setStyle(TableStyle([
        ("BACKGROUND",   (0,0), (-1,0), NAVY),
        ("TEXTCOLOR",    (0,0), (-1,0), WHITE),
        ("FONTNAME",     (0,0), (-1,0), "Helvetica-Bold"),
        ("FONTNAME",     (0,-1),(-1,-1), "Helvetica-Bold"),
        ("BACKGROUND",   (0,-1),(-1,-1), colors.HexColor("#F2DEDE")),
        ("TEXTCOLOR",    (0,-1),(-1,-1), RED),
        ("FONTSIZE",     (0,0), (-1,-1), 9),
        ("ALIGN",        (1,0), (-1,-1), "RIGHT"),
        ("ALIGN",        (0,0), (0,-1), "LEFT"),
        ("ROWBACKGROUNDS",(0,1),(-1,-2), [WHITE, LGRAY]),
        ("GRID",         (0,0), (-1,-1), 0.3, MGRAY),
        ("LEFTPADDING",  (0,0),(-1,-1), 6),
        ("TOPPADDING",   (0,0),(-1,-1), 4),
        ("BOTTOMPADDING",(0,0),(-1,-1), 4),
    ]))
    elems.append(plt)
    elems.append(sp(6))
    elems.append(Paragraph(
        "Renovate & Resell is NOT recommended for Verve Suites at current prices. "
        "The spread between distressed entry and renovated ARV is too thin. "
        "881 units across 4 towers creates significant internal resale competition, suppressing premiums. "
        "RPGT of 30% in Yr1–3 makes any short-hold trade very difficult to profit from.",
        st["body"]
    ))

    elems.append(PageBreak())

    # ── Recommendation ────────────────────────────────────────────────────
    elems += section_header("Recommendation & Buyer Matrix", st)
    rec = [
        ["Buyer Profile", "Recommendation"],
        ["Investor, 1st/2nd property, RM 86K cash", "Buy & Hold 1-bed — top up RM 935/mo, hold 7–10 yr"],
        ["Investor, 3rd+ property", "Pause — 70% MOF requires ~RM 201K cash; stress-test DSR"],
        ["Renovation enthusiast, distressed unit", "BRRRR only if entry ≤ RM 390K — specific deal"],
        ["Short-hold flipper", "Pass — RPGT + thin spread = losing trade"],
        ["Expat own-stay (MM2H)", "Eligible (freehold, >RM 1M threshold applies for foreigners)"],
        ["Foreign buyer (non-MM2H)", "Min. RM 1,000,000 purchase (KL); check foreign stamp duty +4%"],
    ]
    rt2 = Table(rec, colWidths=[6.5*cm, 10*cm])
    rt2.setStyle(TableStyle([
        ("BACKGROUND",   (0,0), (-1,0), NAVY),
        ("TEXTCOLOR",    (0,0), (-1,0), WHITE),
        ("FONTNAME",     (0,0), (-1,0), "Helvetica-Bold"),
        ("FONTNAME",     (0,1), (0,-1), "Helvetica-Bold"),
        ("FONTSIZE",     (0,0), (-1,-1), 8.5),
        ("ALIGN",        (0,0), (-1,-1), "LEFT"),
        ("ROWBACKGROUNDS",(0,1),(-1,-1), [WHITE, LGRAY]),
        ("GRID",         (0,0), (-1,-1), 0.3, MGRAY),
        ("LEFTPADDING",  (0,0),(-1,-1), 6),
        ("TOPPADDING",   (0,0),(-1,-1), 4),
        ("BOTTOMPADDING",(0,0),(-1,-1), 4),
        ("TEXTCOLOR",    (0,1),(0,1), GREEN),
        ("TEXTCOLOR",    (0,3),(0,4), RED),
    ]))
    elems.append(rt2)

    elems.append(sp(12))
    elems += section_header("Risk Factors", st)
    risks = [
        ["Risk", "Severity", "Likelihood", "Mitigation"],
        ["Commercial-title utility tariff", "Medium", "Certain", "Factor into running costs; confirm bank MOF"],
        ["High density (881 units) → resale competition", "Medium", "High", "Price to market; don't over-accumulate"],
        ["Negative cash flow at 90% MOF", "Medium", "High", "Budget RM 935/mo top-up"],
        ["Slow appreciation (2–3%/yr)", "Medium", "Medium", "Hold long-term; accept gradual equity build"],
        ["Short-stay/Airbnb regulation", "Low–Med", "Medium", "Check JMB by-laws before STR thesis"],
        ["Sinking fund adequacy (10yr old)", "Low–Med", "Low", "Request management account from JMB"],
        ["RPGT (30% if sold Yr1–3)", "High", "High if sold early", "Never sell before Yr6"],
        ["MK serviced apt oversupply", "Medium", "Medium", "Focus on tenant demand quality; furnished units let faster"],
    ]
    elems.append(make_table(risks, [5*cm, 2.5*cm, 2.5*cm, 6.5*cm], font_size=7.5))

    elems.append(sp(12))
    elems += section_header("Next Steps", st)
    steps = [
        "1. Inspect 2+ units — compare floor, facing, furnishing condition.",
        "2. Request JMB management account + sinking fund balance.",
        "3. Negotiate 5–10% below asking (125 rental + 105 sale listings = buyer leverage).",
        "4. Confirm bank: commercial title MOF (some cap at 85%).",
        "5. Confirm property count (1st/2nd vs 3rd+) — determines MOF and viability.",
        "6. Run /realestate mortgage 580000 to model full DSR.",
        "7. Run /realestate rental Verve Suites 672 sqft for detailed rental scenarios.",
    ]
    for s in steps:
        elems.append(Paragraph(s, st["body"]))
    elems.append(sp(8))
    elems.append(Paragraph(
        "DISCLAIMER: Educational/research only. Not financial, investment, or tax advice. "
        "RPGT and rental-income tax treatment must be confirmed with a licensed tax agent. "
        "Financing terms must be confirmed with a licensed banker. Always conduct a title search and sinking-fund check before investing.",
        st["disc"]
    ))

    doc.build(elems, onFirstPage=on_page, onLaterPages=on_page)
    print(f"PDF saved: {path}")

if __name__ == "__main__":
    build_pdf()
