#!/usr/bin/env python3
"""PDF for Verve Suites dual-unit investment analysis: 462 sq ft vs 633 sq ft."""

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, PageBreak
)
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.platypus.flowables import Flowable

NAVY  = colors.HexColor("#1B3A5C")
TEAL  = colors.HexColor("#0A7E8C")
GOLD  = colors.HexColor("#C8A951")
AMBER = colors.HexColor("#E87722")
RED   = colors.HexColor("#C0392B")
GREEN = colors.HexColor("#1E8449")
LGRAY = colors.HexColor("#F5F5F5")
MGRAY = colors.HexColor("#CCCCCC")
DGRAY = colors.HexColor("#555555")
WHITE = colors.white

W, H = A4
STUDIO_COL = colors.HexColor("#E8F4F8")
BED_COL    = colors.HexColor("#FEF9E7")

# ── Score bar ──────────────────────────────────────────────────────────────
class ScoreBar(Flowable):
    def __init__(self, label, score, width=360, height=18):
        Flowable.__init__(self)
        self.label = label; self.score = score
        self.width = width; self.height = height

    def draw(self):
        c = self.canv
        bx, bw, bh = 130, self.width - 170, 10
        by = (self.height - bh) / 2
        c.setFont("Helvetica", 8); c.setFillColor(DGRAY)
        c.drawString(0, by + 1, self.label)
        c.setFillColor(LGRAY); c.rect(bx, by, bw, bh, fill=1, stroke=0)
        fc = GREEN if self.score >= 70 else (AMBER if self.score >= 55 else RED)
        c.setFillColor(fc); c.rect(bx, by, bw * self.score / 100, bh, fill=1, stroke=0)
        c.setFont("Helvetica-Bold", 8); c.setFillColor(NAVY)
        c.drawString(bx + bw + 4, by + 1, f"{self.score}/100")

def on_page(canv, doc):
    canv.saveState()
    canv.setFillColor(NAVY); canv.rect(0, H - 1.8*cm, W, 1.8*cm, fill=1, stroke=0)
    canv.setFont("Helvetica-Bold", 10); canv.setFillColor(WHITE)
    canv.drawString(1.5*cm, H - 1.2*cm, "INVESTMENT ANALYSIS: VERVE SUITES — 462 sq ft vs 633 sq ft")
    canv.setFont("Helvetica", 8); canv.setFillColor(GOLD)
    canv.drawRightString(W - 1.5*cm, H - 1.2*cm, "10 June 2026")
    canv.setFillColor(NAVY); canv.rect(0, 0, W, 1.0*cm, fill=1, stroke=0)
    canv.setFont("Helvetica", 7); canv.setFillColor(MGRAY)
    canv.drawString(1.5*cm, 0.35*cm, "Not financial or investment advice. AI-generated estimates. Verify with BOVAEP REN/REA & tax agent.")
    canv.setFillColor(GOLD); canv.drawRightString(W - 1.5*cm, 0.35*cm, f"Page {doc.page}")
    canv.restoreState()

def styles():
    base = dict(fontName="Helvetica", fontSize=9, leading=13, textColor=colors.black)
    def ps(n, **kw): return ParagraphStyle(n, **{**base, **kw})
    return {
        "h2":   ps("h2",  fontName="Helvetica-Bold", fontSize=13, textColor=NAVY,  spaceAfter=4, leading=16),
        "h3":   ps("h3",  fontName="Helvetica-Bold", fontSize=10, textColor=TEAL,  spaceAfter=3),
        "body": ps("body", spaceAfter=4),
        "small":ps("small", fontSize=7.5, textColor=DGRAY, spaceAfter=3),
        "disc": ps("disc",  fontSize=7,   textColor=DGRAY, fontName="Helvetica-Oblique", spaceAfter=6),
        "warn": ps("warn",  fontSize=8,   textColor=AMBER, fontName="Helvetica-Bold", spaceAfter=4),
    }

def sp(n=6): return Spacer(1, n)
def hr(): return HRFlowable(width="100%", thickness=0.5, color=MGRAY, spaceAfter=6, spaceBefore=4)

def sec(text, st):
    return [sp(8), Paragraph(text, st["h2"]),
            HRFlowable(width="100%", thickness=1.5, color=TEAL, spaceAfter=6)]

def mt(data, cw, hbg=NAVY, stripe=True, fs=8):
    ts = [
        ("BACKGROUND",  (0,0), (-1,0), hbg),
        ("TEXTCOLOR",   (0,0), (-1,0), WHITE),
        ("FONTNAME",    (0,0), (-1,0), "Helvetica-Bold"),
        ("FONTSIZE",    (0,0), (-1,-1), fs),
        ("ALIGN",       (1,0), (-1,-1), "RIGHT"),
        ("ALIGN",       (0,0), (0,-1), "LEFT"),
        ("ROWBACKGROUNDS", (0,1), (-1,-1), [WHITE, LGRAY] if stripe else [WHITE]),
        ("GRID",        (0,0), (-1,-1), 0.3, MGRAY),
        ("LEFTPADDING", (0,0), (-1,-1), 5),
        ("RIGHTPADDING",(0,0), (-1,-1), 5),
        ("TOPPADDING",  (0,0), (-1,-1), 3),
        ("BOTTOMPADDING",(0,0),(-1,-1), 3),
    ]
    return Table(data, colWidths=cw, style=TableStyle(ts), repeatRows=1)

def build():
    path = "PROPERTY-INVEST-Verve-Suites-462-633.pdf"
    doc = SimpleDocTemplate(path, pagesize=A4,
        leftMargin=1.8*cm, rightMargin=1.8*cm,
        topMargin=2.2*cm, bottomMargin=1.6*cm)
    st = styles()
    e = []

    # ── COVER ──────────────────────────────────────────────────────────────
    e.append(sp(1.5*cm))
    title = Table([["INVESTMENT ANALYSIS"]], colWidths=[W - 3.6*cm])
    title.setStyle(TableStyle([
        ("BACKGROUND",(0,0),(-1,-1),NAVY),("TEXTCOLOR",(0,0),(-1,-1),WHITE),
        ("FONTNAME",(0,0),(-1,-1),"Helvetica-Bold"),("FONTSIZE",(0,0),(-1,-1),22),
        ("ALIGN",(0,0),(-1,-1),"CENTER"),("TOPPADDING",(0,0),(-1,-1),14),("BOTTOMPADDING",(0,0),(-1,-1),14),
    ]))
    e.append(title); e.append(sp(4))
    sub = Table([["Verve Suites Mont Kiara · Studio 462 sq ft  vs  1-Bed 633 sq ft"]], colWidths=[W - 3.6*cm])
    sub.setStyle(TableStyle([
        ("BACKGROUND",(0,0),(-1,-1),TEAL),("TEXTCOLOR",(0,0),(-1,-1),WHITE),
        ("FONTNAME",(0,0),(-1,-1),"Helvetica-Bold"),("FONTSIZE",(0,0),(-1,-1),12),
        ("ALIGN",(0,0),(-1,-1),"CENTER"),("TOPPADDING",(0,0),(-1,-1),10),("BOTTOMPADDING",(0,0),(-1,-1),10),
    ]))
    e.append(sub); e.append(sp(20))

    # score bars on cover
    for lbl, sc in [("Studio 462 sq ft — Buy & Hold", 67), ("Studio 462 sq ft — BRRRR", 55),
                    ("Studio 462 sq ft — Composite", 62), ("1-Bed 633 sq ft — Buy & Hold", 62),
                    ("1-Bed 633 sq ft — BRRRR (@RM450K)", 63), ("1-Bed 633 sq ft — Composite", 60)]:
        e.append(ScoreBar(lbl, sc, width=400))
        e.append(sp(4))

    e.append(sp(16))
    e.append(Paragraph(
        "⚠ KEY OPPORTUNITY: 1-bed 633 sq ft listing found at RM 450,000 — RM 711 psf vs transacted median RM 866 psf. "
        "If genuine, this is RM 98,000 below market before renovation. Verify urgently.",
        st["warn"]
    ))
    e.append(sp(10))
    e.append(Paragraph(
        "DISCLAIMER: Educational/research purposes only. Not financial, investment, or tax advice. "
        "All estimates are AI-generated approximations. Consult BOVAEP-registered REN/REA, licensed banker, and tax agent.",
        st["disc"]
    ))
    e.append(PageBreak())

    # ── UNIT PROFILES ──────────────────────────────────────────────────────
    e += sec("Unit Profiles", st)
    profiles = [
        ["Field", "Studio — 462 sq ft", "1-Bed — 633 sq ft"],
        ["Layout", "City Flux / Centro Jazz", "Urban Glam"],
        ["Tenure", "Freehold", "Freehold"],
        ["Property Type", "Serviced Residence (commercial title)", "Serviced Residence (commercial title)"],
        ["Completed (VP)", "2015", "2015"],
        ["Distressed / Low Ask", "RM 365,000 (RM 790 psf)", "RM 450,000 (RM 711 psf) ← below median"],
        ["High Ask", "RM 480,000 (RM 1,039 psf)", "RM 680,000 (RM 1,074 psf)"],
        ["Target Entry (median)", "~RM 400,000 (RM 866 psf)", "~RM 548,000 (RM 866 psf)"],
        ["Maintenance Fee", "RM 152/mo (RM 0.33 psf)", "RM 209/mo (RM 0.33 psf)"],
        ["Typical Rent (as-is)", "RM 1,800–2,000/mo", "RM 2,300–2,500/mo"],
        ["Typical Rent (furnished)", "RM 2,000–2,200/mo", "RM 2,400–2,700/mo"],
    ]
    pt = Table(profiles, colWidths=[4.5*cm, 7*cm, 7*cm])
    pt.setStyle(TableStyle([
        ("BACKGROUND",(0,0),(-1,0),NAVY),("TEXTCOLOR",(0,0),(-1,0),WHITE),
        ("FONTNAME",(0,0),(-1,0),"Helvetica-Bold"),
        ("BACKGROUND",(1,1),(1,-1),STUDIO_COL),
        ("BACKGROUND",(2,1),(2,-1),BED_COL),
        ("FONTSIZE",(0,0),(-1,-1),8),("ALIGN",(0,0),(-1,-1),"LEFT"),
        ("GRID",(0,0),(-1,-1),0.3,MGRAY),("LEFTPADDING",(0,0),(-1,-1),5),
        ("TOPPADDING",(0,0),(-1,-1),3),("BOTTOMPADDING",(0,0),(-1,-1),3),
        ("FONTNAME",(0,7),(0,7),"Helvetica-Bold"),("TEXTCOLOR",(0,7),(0,7),TEAL),
        ("FONTNAME",(1,7),(-1,7),"Helvetica-Bold"),("TEXTCOLOR",(1,7),(-1,7),GREEN),
    ]))
    e.append(pt)

    # ── HEAD-TO-HEAD DASHBOARD ─────────────────────────────────────────────
    e += sec("Head-to-Head Strategy Dashboard", st)
    dash = [
        ["Metric", "Studio 462 sq ft", "1-Bed 633 sq ft"],
        ["Buy & Hold Score", "67/100", "62/100"],
        ["BRRRR Score", "55/100", "63/100 (@ RM 450K)"],
        ["Flip Score", "38/100", "42/100"],
        ["Composite Investment Score", "62/100", "60/100"],
        ["Target Entry", "RM 400,000", "RM 548,000"],
        ["Cash Required (90% MOF, 1st/2nd)", "~RM 57,000", "~RM 78,000"],
        ["Cash Required (70% MOF, 3rd+)", "~RM 130,000", "~RM 178,000"],
        ["Monthly Instalment (4.4%, 35yr)", "RM 1,680", "RM 2,303"],
        ["Gross Rental Yield", "5.7%", "5.3%"],
        ["Net Rental Yield", "3.8%", "3.4%"],
        ["Monthly Top-up (90% MOF, Yr1)", "RM 419", "RM 737"],
        ["10-yr Appreciation Gain", "RM 112,000", "RM 153,500"],
        ["Winner on:", "Yield% & cash efficiency", "Absolute return & tenant pool"],
    ]
    dt = Table(dash, colWidths=[6*cm, 5.5*cm, 5.5*cm])
    dt.setStyle(TableStyle([
        ("BACKGROUND",(0,0),(-1,0),NAVY),("TEXTCOLOR",(0,0),(-1,0),WHITE),
        ("FONTNAME",(0,0),(-1,0),"Helvetica-Bold"),
        ("BACKGROUND",(1,1),(1,-1),STUDIO_COL),("BACKGROUND",(2,1),(2,-1),BED_COL),
        ("FONTNAME",(0,-1),(0,-1),"Helvetica-Bold"),("FONTSIZE",(0,0),(-1,-1),8.5),
        ("ALIGN",(1,0),(-1,-1),"CENTER"),("ALIGN",(0,0),(0,-1),"LEFT"),
        ("GRID",(0,0),(-1,-1),0.3,MGRAY),("LEFTPADDING",(0,0),(-1,-1),5),
        ("TOPPADDING",(0,0),(-1,-1),3),("BOTTOMPADDING",(0,0),(-1,-1),3),
        ("FONTNAME",(0,1),(-1,4),"Helvetica-Bold"),
        ("TEXTCOLOR",(1,1),(1,4),GREEN),("TEXTCOLOR",(2,1),(2,4),AMBER),
    ]))
    e.append(dt)
    e.append(PageBreak())

    # ── STRATEGY 1: BUY & HOLD ─────────────────────────────────────────────
    e += sec("Strategy 1: Buy & Hold", st)
    e.append(Paragraph("Acquisition & Financing", st["h3"]))
    acq = [
        ["Parameter", "Studio 462 (90% MOF)", "1-Bed 633 (90% MOF)"],
        ["Purchase Price (target)", "RM 400,000", "RM 548,000"],
        ["Loan Amount (90%)", "RM 360,000", "RM 493,200"],
        ["Down Payment (10%)", "RM 40,000", "RM 54,800"],
        ["MOT Stamp Duty", "RM 7,000", "RM 10,440"],
        ["Loan Stamp Duty (0.5%)", "RM 1,800", "RM 2,466"],
        ["Legal Fees", "RM 6,000", "RM 7,500"],
        ["Repairs / Furnishing", "RM 2,000", "RM 3,000"],
        ["TOTAL CASH INVESTED", "~RM 57,000", "~RM 78,000"],
        ["Monthly Instalment (4.4%, 35yr)", "RM 1,680/mo", "RM 2,303/mo"],
        ["Cash if 3rd+ property (70% MOF)", "~RM 130,000", "~RM 178,000"],
    ]
    aq = Table(acq, colWidths=[5.5*cm, 5.5*cm, 5.5*cm])
    aq.setStyle(TableStyle([
        ("BACKGROUND",(0,0),(-1,0),NAVY),("TEXTCOLOR",(0,0),(-1,0),WHITE),
        ("FONTNAME",(0,0),(-1,0),"Helvetica-Bold"),
        ("BACKGROUND",(1,1),(1,-1),STUDIO_COL),("BACKGROUND",(2,1),(2,-1),BED_COL),
        ("FONTNAME",(0,-3),(0,-1),"Helvetica-Bold"),("FONTNAME",(0,8),(0,8),"Helvetica-Bold"),
        ("BACKGROUND",(0,8),(-1,8),colors.HexColor("#DFF0D8")),
        ("FONTSIZE",(0,0),(-1,-1),8.5),("ALIGN",(1,0),(-1,-1),"RIGHT"),("ALIGN",(0,0),(0,-1),"LEFT"),
        ("GRID",(0,0),(-1,-1),0.3,MGRAY),("LEFTPADDING",(0,0),(-1,-1),5),
        ("TOPPADDING",(0,0),(-1,-1),3),("BOTTOMPADDING",(0,0),(-1,-1),3),
    ]))
    e.append(aq)

    e.append(sp(8))
    e.append(Paragraph("Annual Cash Flow (90% MOF · 7% vacancy · 2.5%/yr rent growth)", st["h3"]))
    cf = [
        ["Line Item", "Studio Yr1", "Studio Yr5", "1-Bed Yr1", "1-Bed Yr5"],
        ["Gross Monthly Rent", "RM 1,900", "RM 2,100", "RM 2,400", "RM 2,650"],
        ["Gross Annual Rent", "RM 22,800", "RM 25,200", "RM 28,800", "RM 31,800"],
        ["Vacancy (7%)", "–RM 1,596", "–RM 1,764", "–RM 2,016", "–RM 2,226"],
        ["Maintenance Fee", "–RM 1,827", "–RM 2,000", "–RM 2,507", "–RM 2,740"],
        ["CapEx / Repairs (5%)", "–RM 1,140", "–RM 1,260", "–RM 1,440", "–RM 1,590"],
        ["Insurance + Assessment + QR", "–RM 1,200", "–RM 1,200", "–RM 1,650", "–RM 1,650"],
        ["Agent Fee (renewal)", "–RM 1,900", "–RM 2,100", "–RM 2,400", "–RM 2,650"],
        ["NOI", "RM 15,137", "RM 16,876", "RM 18,787", "RM 20,944"],
        ["Mortgage Instalment", "–RM 20,160", "–RM 20,160", "–RM 27,636", "–RM 27,636"],
        ["NET CASH FLOW", "–RM 5,023", "–RM 3,284", "–RM 8,849", "–RM 6,692"],
        ["Monthly Top-up", "RM 419/mo", "RM 274/mo", "RM 737/mo", "RM 558/mo"],
    ]
    cft = Table(cf, colWidths=[4.5*cm, 2.8*cm, 2.8*cm, 2.8*cm, 2.8*cm])
    cft.setStyle(TableStyle([
        ("BACKGROUND",(0,0),(-1,0),NAVY),("TEXTCOLOR",(0,0),(-1,0),WHITE),
        ("FONTNAME",(0,0),(-1,0),"Helvetica-Bold"),
        ("BACKGROUND",(1,1),(2,-1),STUDIO_COL),("BACKGROUND",(3,1),(4,-1),BED_COL),
        ("FONTNAME",(0,8),(0,8),"Helvetica-Bold"),("FONTNAME",(0,-2),(0,-1),"Helvetica-Bold"),
        ("BACKGROUND",(0,8),(-1,8),colors.HexColor("#DFF0D8")),
        ("BACKGROUND",(0,-2),(-1,-2),colors.HexColor("#F2DEDE")),
        ("BACKGROUND",(0,-1),(-1,-1),colors.HexColor("#FDEBD0")),
        ("FONTSIZE",(0,0),(-1,-1),8),("ALIGN",(1,0),(-1,-1),"RIGHT"),("ALIGN",(0,0),(0,-1),"LEFT"),
        ("GRID",(0,0),(-1,-1),0.3,MGRAY),("LEFTPADDING",(0,0),(-1,-1),5),
        ("TOPPADDING",(0,0),(-1,-1),3),("BOTTOMPADDING",(0,0),(-1,-1),3),
    ]))
    e.append(cft)
    e.append(sp(4))
    e.append(Paragraph(
        "Studio gross yield 5.7% / net 3.8% — 1-bed gross 5.3% / net 3.4%. "
        "Both run negative leveraged CF at 90% MOF — normal for Mont Kiara. Studio top-up is half the 1-bed's.",
        st["small"]
    ))

    e.append(sp(8))
    e.append(Paragraph("10-Year Total Return (90% MOF, exit Yr7+ — 0% RPGT)", st["h3"]))
    ret = [
        ["Component", "Studio 7-Yr", "1-Bed 7-Yr"],
        ["Cumulative Net Cash Flow", "–RM 38,000", "–RM 67,000"],
        ["Appreciation Gain (2.5%/yr)", "RM 74,600", "RM 102,200"],
        ["Principal Paydown", "RM 14,500", "RM 19,800"],
        ["RPGT (0% — Yr7 exit)", "RM 0", "RM 0"],
        ["Selling Costs (~4%)", "–RM 19,400", "–RM 25,900"],
        ["NET TOTAL RETURN", "~RM 31,700", "~RM 29,100"],
        ["Annualized ROI on Cash", "~7.9%", "~5.3%"],
    ]
    rt = Table(ret, colWidths=[6.5*cm, 4.5*cm, 4.5*cm])
    rt.setStyle(TableStyle([
        ("BACKGROUND",(0,0),(-1,0),NAVY),("TEXTCOLOR",(0,0),(-1,0),WHITE),
        ("FONTNAME",(0,0),(-1,0),"Helvetica-Bold"),
        ("BACKGROUND",(1,1),(1,-1),STUDIO_COL),("BACKGROUND",(2,1),(2,-1),BED_COL),
        ("FONTNAME",(0,-2),(0,-1),"Helvetica-Bold"),
        ("BACKGROUND",(0,-2),(-1,-1),TEAL),("TEXTCOLOR",(0,-2),(-1,-1),WHITE),
        ("FONTSIZE",(0,0),(-1,-1),9),("ALIGN",(1,0),(-1,-1),"RIGHT"),("ALIGN",(0,0),(0,-1),"LEFT"),
        ("ROWBACKGROUNDS",(0,1),(-1,-3),[WHITE,LGRAY]),
        ("GRID",(0,0),(-1,-1),0.3,MGRAY),("LEFTPADDING",(0,0),(-1,-1),6),
        ("TOPPADDING",(0,0),(-1,-1),4),("BOTTOMPADDING",(0,0),(-1,-1),4),
    ]))
    e.append(rt)
    e.append(sp(4))
    e.append(Paragraph(
        "Studio delivers better annualised ROI on cash (7.9% vs 5.3%) due to lower capital base. "
        "1-bed delivers higher absolute gain. NEVER sell before Yr6 — 30% RPGT in Yr1-3 wipes the return.",
        st["small"]
    ))
    e.append(PageBreak())

    # ── STRATEGY 2: BRRRR ─────────────────────────────────────────────────
    e += sec("Strategy 2: BRRRR", st)
    e.append(Paragraph("Studio 462 sq ft — Entry RM 365K (distressed listing)", st["h3"]))
    b1 = [
        ["Phase", "Detail", "Amount"],
        ["BUY", "Distressed price", "RM 365,000"],
        ["BUY", "Stamps + Legal", "RM 10,450"],
        ["RENOVATE", "Full cosmetic reno (RM 100 psf × 462)", "RM 46,200"],
        ["RENT", "Post-reno monthly rent", "RM 2,100"],
        ["REFINANCE", "ARV (RM 910 psf × 462 = RM 420,420)", "RM 420,420"],
        ["REFINANCE", "Refi 80% of ARV", "RM 336,336"],
        ["REFINANCE", "Original loan (90% × RM 365K)", "RM 328,500"],
        ["REPEAT", "Cash returned from refi", "RM 7,836"],
        ["REPEAT", "Cash left in deal", "~RM 87,000"],
    ]
    e.append(mt(b1, [2.5*cm, 7*cm, 5*cm], hbg=TEAL, fs=8))
    e.append(sp(4))
    e.append(Paragraph(
        "70% Rule: RM 411K ≤ 70% × RM 420K = RM 294K → FAIL. ARV confidence is LOW. Post-refi CF ≈ –RM 200/mo (manageable).",
        st["small"]
    ))

    e.append(sp(10))
    e.append(Paragraph("★ 1-Bed 633 sq ft — Entry RM 450K (below-median listing) ← Key Opportunity", st["h3"]))
    b2 = [
        ["Phase", "Detail", "Amount"],
        ["BUY", "Below-median price (RM 711 psf — RM 155K below median!)", "RM 450,000"],
        ["BUY", "Stamps + Legal", "RM 12,150"],
        ["RENOVATE", "Full cosmetic reno (RM 100 psf × 633)", "RM 63,300"],
        ["RENT", "Post-reno monthly rent", "RM 2,600"],
        ["REFINANCE", "ARV (RM 920 psf × 633 = RM 582,360)", "RM 582,360"],
        ["REFINANCE", "Refi 80% of ARV", "RM 465,888"],
        ["REFINANCE", "Original loan (90% × RM 450K)", "RM 405,000"],
        ["REPEAT", "Cash returned from refi", "RM 60,888"],
        ["REPEAT", "Cash left in deal", "~RM 64,562"],
        ["EQUITY", "Instant equity (ARV vs all-in RM 525.5K)", "RM 56,800 (10% of ARV)"],
    ]
    b2t = Table(b2, colWidths=[2.5*cm, 8.5*cm, 4*cm])
    b2t.setStyle(TableStyle([
        ("BACKGROUND",(0,0),(-1,0),GREEN),("TEXTCOLOR",(0,0),(-1,0),WHITE),
        ("FONTNAME",(0,0),(-1,0),"Helvetica-Bold"),
        ("BACKGROUND",(0,-1),(-1,-1),colors.HexColor("#DFF0D8")),
        ("FONTNAME",(0,-1),(-1,-1),"Helvetica-Bold"),
        ("FONTSIZE",(0,0),(-1,-1),8),("ALIGN",(2,0),(2,-1),"RIGHT"),("ALIGN",(0,0),(1,-1),"LEFT"),
        ("ROWBACKGROUNDS",(0,1),(-1,-2),[WHITE,LGRAY]),
        ("GRID",(0,0),(-1,-1),0.3,MGRAY),("LEFTPADDING",(0,0),(-1,-1),5),
        ("TOPPADDING",(0,0),(-1,-1),3),("BOTTOMPADDING",(0,0),(-1,-1),3),
    ]))
    e.append(b2t)
    e.append(sp(4))
    e.append(Paragraph(
        "This is the most compelling deal in the analysis. Buying RM 98K below transacted median before renovation — "
        "real equity at purchase. 70% rule still fails but the structure is meaningfully better. "
        "Verify the RM 450K listing with the agent immediately — confirm reason of sale, floor, facing, condition.",
        st["warn"]
    ))

    e.append(sp(8))
    e.append(Paragraph("BRRRR Scores", st["h3"]))
    bscores = [
        ["Criterion", "Max", "Studio 462\n(@ RM 365K)", "1-Bed 633\n(@ RM 450K)"],
        ["Equity Created", "25", "8", "15"],
        ["Cash Left in Deal", "20", "8", "12"],
        ["Post-Refi Cash Flow", "20", "12", "10"],
        ["ARV Confidence", "15", "5", "8"],
        ["Reno Feasibility", "10", "10", "10"],
        ["70% Rule Compliance", "10", "1", "3"],
        ["TOTAL", "100", "44 → 55", "58 → 63"],
    ]
    e.append(mt(bscores, [6*cm, 2*cm, 3.5*cm, 3.5*cm], fs=8))
    e.append(PageBreak())

    # ── STRATEGY 3: FLIP ─────────────────────────────────────────────────
    e += sec("Strategy 3: Renovate & Resell (Flip)", st)
    e.append(Paragraph("Both units: NOT recommended at current prices.", st["h3"]))
    flip = [
        ["P&L Item", "Studio 462 @ RM 365K", "1-Bed 633 @ RM 450K"],
        ["ARV (renovated)", "RM 420,000", "RM 582,000"],
        ["Less: Purchase Price", "–RM 365,000", "–RM 450,000"],
        ["Less: Reno", "–RM 46,200", "–RM 63,300"],
        ["Less: Stamps + Legal", "–RM 10,450", "–RM 12,150"],
        ["Less: Holding Costs (5 mo)", "–RM 5,500", "–RM 7,000"],
        ["Less: Selling Costs (~4%)", "–RM 16,800", "–RM 23,280"],
        ["GROSS GAIN (pre-RPGT)", "–RM 23,950 (LOSS)", "RM 26,270"],
        ["RPGT @ 30% (sold Yr1-3)", "RM 0 (loss)", "–RM 7,881"],
        ["NET PROFIT", "–RM 23,950 ❌", "~RM 18,389 ⚠"],
        ["Profit Margin on ARV", "Negative", "3.2% — target is >10%"],
        ["Flip Score", "38/100", "42/100"],
    ]
    flt = Table(flip, colWidths=[5.5*cm, 5.5*cm, 5.5*cm])
    flt.setStyle(TableStyle([
        ("BACKGROUND",(0,0),(-1,0),RED),("TEXTCOLOR",(0,0),(-1,0),WHITE),
        ("FONTNAME",(0,0),(-1,0),"Helvetica-Bold"),
        ("BACKGROUND",(1,1),(1,-1),STUDIO_COL),("BACKGROUND",(2,1),(2,-1),BED_COL),
        ("FONTNAME",(0,-5),(0,-1),"Helvetica-Bold"),
        ("BACKGROUND",(0,-5),(-1,-5),colors.HexColor("#F2DEDE")),
        ("FONTSIZE",(0,0),(-1,-1),8.5),("ALIGN",(1,0),(-1,-1),"RIGHT"),("ALIGN",(0,0),(0,-1),"LEFT"),
        ("ROWBACKGROUNDS",(0,1),(-1,-6),[WHITE,LGRAY]),
        ("GRID",(0,0),(-1,-1),0.3,MGRAY),("LEFTPADDING",(0,0),(-1,-1),5),
        ("TOPPADDING",(0,0),(-1,-1),3),("BOTTOMPADDING",(0,0),(-1,-1),3),
        ("TEXTCOLOR",(1,-5),(1,-5),RED),
    ]))
    e.append(flt)
    e.append(sp(4))
    e.append(Paragraph(
        "Flip doesn't work for either unit. 881-unit project limits resale premium; RPGT 30% in Yr1-3 is fatal. "
        "If you buy the RM 450K 1-bed, HOLD it — don't flip.",
        st["small"]
    ))

    # ── PROJECTIONS ────────────────────────────────────────────────────────
    e += sec("10-Year Projections — Buy & Hold", st)
    e.append(Paragraph("Studio 462 sq ft @ RM 400,000 (90% MOF)", st["h3"]))
    proj_s = [
        ["Year", "Value", "Rent/mo", "NOI/yr", "Net CF/yr", "Equity"],
        ["1", "RM 410K", "RM 1,900", "RM 15,137", "–RM 5,023", "RM 51,500"],
        ["3", "RM 431K", "RM 2,000", "RM 15,900", "–RM 4,260", "RM 73,200"],
        ["5", "RM 453K", "RM 2,100", "RM 16,876", "–RM 3,284", "RM 96,700"],
        ["7", "RM 475K", "RM 2,200", "RM 17,700", "–RM 2,460", "RM 121,000"],
        ["10", "RM 512K", "RM 2,400", "RM 19,200", "–RM 960", "RM 153,000"],
    ]
    e.append(mt(proj_s, [2*cm, 3*cm, 3*cm, 3*cm, 3.5*cm, 3*cm], hbg=TEAL, fs=8))

    e.append(sp(8))
    e.append(Paragraph("1-Bed 633 sq ft @ RM 548,000 (90% MOF)", st["h3"]))
    proj_b = [
        ["Year", "Value", "Rent/mo", "NOI/yr", "Net CF/yr", "Equity"],
        ["1", "RM 561.7K", "RM 2,400", "RM 18,787", "–RM 8,849", "RM 70,400"],
        ["3", "RM 590.2K", "RM 2,520", "RM 19,700", "–RM 7,936", "RM 98,500"],
        ["5", "RM 620K", "RM 2,650", "RM 20,944", "–RM 6,692", "RM 128,400"],
        ["7", "RM 651.2K", "RM 2,800", "RM 22,050", "–RM 5,586", "RM 160,000"],
        ["10", "RM 701.5K", "RM 3,020", "RM 23,900", "–RM 3,736", "RM 218,000"],
    ]
    e.append(mt(proj_b, [2*cm, 3*cm, 3*cm, 3*cm, 3.5*cm, 3*cm], hbg=NAVY, fs=8))

    # ── RECOMMENDATION ─────────────────────────────────────────────────────
    e += sec("Recommendation", st)
    rec = [
        ["Buyer Profile", "Best Pick", "Why"],
        ["Lower budget / 1st property", "Studio 462 @ RM 400K", "RM 57K cash-in, RM 419/mo top-up"],
        ["Distressed hunter / BRRRR", "1-Bed 633 @ RM 450K ★", "RM 98K below median = rare equity"],
        ["Widest tenant demand", "1-Bed 633 @ RM 548K", "More expat family / couple demand"],
        ["Max yield%", "Studio 462", "5.7% gross vs 5.3% for 1-bed"],
        ["3rd+ property (70% MOF)", "Pause — stress-test DSR first", "Cash-in RM 130K–178K"],
        ["Short-hold / flip", "Pass — both units", "Negative or sub-3% margin"],
    ]
    rt2 = Table(rec, colWidths=[4.5*cm, 5*cm, 7*cm])
    rt2.setStyle(TableStyle([
        ("BACKGROUND",(0,0),(-1,0),NAVY),("TEXTCOLOR",(0,0),(-1,0),WHITE),
        ("FONTNAME",(0,0),(-1,0),"Helvetica-Bold"),
        ("FONTNAME",(0,1),(0,-1),"Helvetica-Bold"),
        ("BACKGROUND",(0,2),(-1,2),colors.HexColor("#D5F5E3")),
        ("FONTSIZE",(0,0),(-1,-1),8.5),("ALIGN",(0,0),(-1,-1),"LEFT"),
        ("ROWBACKGROUNDS",(0,1),(-1,-1),[WHITE,LGRAY]),
        ("GRID",(0,0),(-1,-1),0.3,MGRAY),("LEFTPADDING",(0,0),(-1,-1),6),
        ("TOPPADDING",(0,0),(-1,-1),4),("BOTTOMPADDING",(0,0),(-1,-1),4),
    ]))
    e.append(rt2)

    e.append(sp(12))
    e += sec("Next Steps", st)
    steps = [
        "1. Studio 462: Inspect RM 365K distressed listing. If decent condition (mid floor+, reasonable facing), target RM 365–385K.",
        "2. 1-Bed 633: Verify the RM 450,000 listing URGENTLY — ask agent for floor, facing, condition, reason for sale. If genuine, this is the best deal.",
        "3. Confirm property count (1st/2nd vs 3rd+) with your banker before signing anything.",
        "4. Request JMB management account + sinking fund balance. Building is 10 years old — check maintenance spend.",
        "5. Get a licensed panel valuer's pre-approval for ARV before committing to any BRRRR refi.",
        "6. Negotiate 5–10% below asking — 105 sale listings + 125 rental = strong buyer leverage.",
        "7. Run /realestate mortgage on chosen unit + price for full DSR + Islamic vs conventional breakdown.",
    ]
    for s in steps:
        e.append(Paragraph(s, st["body"]))
    e.append(sp(8))
    e.append(Paragraph(
        "DISCLAIMER: Educational/research only. Not financial, investment, or tax advice. "
        "RPGT and rental income tax deductibility must be confirmed with a licensed tax agent. "
        "Financing must be confirmed with a licensed banker. Conduct title search and sinking-fund check before investing.",
        st["disc"]
    ))

    doc.build(e, onFirstPage=on_page, onLaterPages=on_page)
    print(f"PDF saved: {path}")

if __name__ == "__main__":
    build()
