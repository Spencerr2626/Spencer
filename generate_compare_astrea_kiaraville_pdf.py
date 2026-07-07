#!/usr/bin/env python3
"""PDF: Astrea Mont Kiara vs Kiaraville Mont Kiara — Foreign Buyer Comparison."""

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, PageBreak
)
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

A_COL = colors.HexColor("#E8F4F8")   # Astrea — blue tint
K_COL = colors.HexColor("#FEF9E7")   # Kiaraville — gold tint
W, H  = A4

class ScoreBar(Flowable):
    def __init__(self, label, score_a, score_b, width=380, height=20):
        Flowable.__init__(self)
        self.label = label; self.score_a = score_a; self.score_b = score_b
        self.width = width; self.height = height

    def draw(self):
        c = self.canv
        bx, bw, bh = 140, (self.width - 155) // 2 - 4, 10
        by = (self.height - bh) / 2
        # Label
        c.setFont("Helvetica", 8); c.setFillColor(DGRAY)
        c.drawString(0, by + 1, self.label)
        # Astrea bar
        c.setFillColor(LGRAY); c.rect(bx, by, bw, bh, fill=1, stroke=0)
        fc_a = GREEN if self.score_a >= 70 else (AMBER if self.score_a >= 55 else RED)
        c.setFillColor(fc_a); c.rect(bx, by, bw * self.score_a / 100, bh, fill=1, stroke=0)
        c.setFont("Helvetica-Bold", 7); c.setFillColor(NAVY)
        c.drawString(bx + bw + 2, by + 1, f"A:{self.score_a}")
        # Kiaraville bar
        bx2 = bx + bw + 26
        c.setFillColor(LGRAY); c.rect(bx2, by, bw, bh, fill=1, stroke=0)
        fc_b = GREEN if self.score_b >= 70 else (AMBER if self.score_b >= 55 else RED)
        c.setFillColor(fc_b); c.rect(bx2, by, bw * self.score_b / 100, bh, fill=1, stroke=0)
        c.setFont("Helvetica-Bold", 7); c.setFillColor(NAVY)
        c.drawString(bx2 + bw + 2, by + 1, f"K:{self.score_b}")

def on_page(canv, doc):
    canv.saveState()
    canv.setFillColor(NAVY); canv.rect(0, H - 1.8*cm, W, 1.8*cm, fill=1, stroke=0)
    canv.setFont("Helvetica-Bold", 10); canv.setFillColor(WHITE)
    canv.drawString(1.5*cm, H - 1.2*cm, "COMPARISON: ASTREA vs KIARAVILLE — MONT KIARA  |  FOREIGN BUYER")
    canv.setFont("Helvetica", 8); canv.setFillColor(GOLD)
    canv.drawRightString(W - 1.5*cm, H - 1.2*cm, "10 June 2026")
    canv.setFillColor(NAVY); canv.rect(0, 0, W, 1.0*cm, fill=1, stroke=0)
    canv.setFont("Helvetica", 7); canv.setFillColor(MGRAY)
    canv.drawString(1.5*cm, 0.35*cm, "Not financial or investment advice. AI-generated estimates. Verify with BOVAEP REN/REA, solicitor & banker.")
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

def sec(text, st):
    return [sp(8), Paragraph(text, st["h2"]),
            HRFlowable(width="100%", thickness=1.5, color=TEAL, spaceAfter=6)]

def mt(data, cw, hbg=NAVY, stripe=True, fs=8, bold_last=False):
    ts = [
        ("BACKGROUND",(0,0),(-1,0),hbg),("TEXTCOLOR",(0,0),(-1,0),WHITE),
        ("FONTNAME",(0,0),(-1,0),"Helvetica-Bold"),("FONTSIZE",(0,0),(-1,-1),fs),
        ("ALIGN",(1,0),(-1,-1),"RIGHT"),("ALIGN",(0,0),(0,-1),"LEFT"),
        ("ROWBACKGROUNDS",(0,1),(-1,-1),[WHITE,LGRAY] if stripe else [WHITE]),
        ("GRID",(0,0),(-1,-1),0.3,MGRAY),("LEFTPADDING",(0,0),(-1,-1),5),
        ("RIGHTPADDING",(0,0),(-1,-1),5),("TOPPADDING",(0,0),(-1,-1),3),
        ("BOTTOMPADDING",(0,0),(-1,-1),3),
    ]
    if bold_last:
        ts += [("FONTNAME",(0,-1),(-1,-1),"Helvetica-Bold"),
               ("BACKGROUND",(0,-1),(-1,-1),TEAL),("TEXTCOLOR",(0,-1),(-1,-1),WHITE)]
    return Table(data, colWidths=cw, style=TableStyle(ts), repeatRows=1)

def winner_table(data, cw):
    """Table with GOLD highlight on winner column per row."""
    ts = [
        ("BACKGROUND",(0,0),(-1,0),NAVY),("TEXTCOLOR",(0,0),(-1,0),WHITE),
        ("FONTNAME",(0,0),(-1,0),"Helvetica-Bold"),("FONTSIZE",(0,0),(-1,-1),8.5),
        ("ALIGN",(1,0),(-1,-1),"CENTER"),("ALIGN",(0,0),(0,-1),"LEFT"),
        ("BACKGROUND",(1,1),(1,-1),A_COL),("BACKGROUND",(2,1),(2,-1),K_COL),
        ("GRID",(0,0),(-1,-1),0.3,MGRAY),("LEFTPADDING",(0,0),(-1,-1),5),
        ("TOPPADDING",(0,0),(-1,-1),3),("BOTTOMPADDING",(0,0),(-1,-1),3),
    ]
    # Bold the composite row
    ts += [("FONTNAME",(0,-1),(-1,-1),"Helvetica-Bold"),
           ("BACKGROUND",(0,-1),(-1,-1),TEAL),("TEXTCOLOR",(0,-1),(-1,-1),WHITE)]
    return Table(data, colWidths=cw, style=TableStyle(ts), repeatRows=1)

def build():
    path = "PROPERTY-COMPARE-Astrea-vs-Kiaraville.pdf"
    doc = SimpleDocTemplate(path, pagesize=A4,
        leftMargin=1.8*cm, rightMargin=1.8*cm,
        topMargin=2.2*cm, bottomMargin=1.6*cm)
    st = styles()
    e = []

    # ── COVER ──────────────────────────────────────────────────────────────
    e.append(sp(1.5*cm))
    t = Table([["PROPERTY COMPARISON"]], colWidths=[W - 3.6*cm])
    t.setStyle(TableStyle([
        ("BACKGROUND",(0,0),(-1,-1),NAVY),("TEXTCOLOR",(0,0),(-1,-1),WHITE),
        ("FONTNAME",(0,0),(-1,-1),"Helvetica-Bold"),("FONTSIZE",(0,0),(-1,-1),22),
        ("ALIGN",(0,0),(-1,-1),"CENTER"),("TOPPADDING",(0,0),(-1,-1),14),("BOTTOMPADDING",(0,0),(-1,-1),14),
    ]))
    e.append(t); e.append(sp(4))

    sub = Table([["Residensi Astrea  vs  Kiaraville · Mont Kiara · Foreign Buyer Profile"]], colWidths=[W - 3.6*cm])
    sub.setStyle(TableStyle([
        ("BACKGROUND",(0,0),(-1,-1),TEAL),("TEXTCOLOR",(0,0),(-1,-1),WHITE),
        ("FONTNAME",(0,0),(-1,-1),"Helvetica-Bold"),("FONTSIZE",(0,0),(-1,-1),11),
        ("ALIGN",(0,0),(-1,-1),"CENTER"),("TOPPADDING",(0,0),(-1,-1),10),("BOTTOMPADDING",(0,0),(-1,-1),10),
    ]))
    e.append(sub); e.append(sp(16))

    # Score bars
    cats = [
        ("Price & Value (20%)", 70, 72),
        ("Property Specs (10%)", 82, 72),
        ("Rental Income (20%)", 72, 68),
        ("Neighbourhood (15%)", 84, 84),
        ("Investment Potential (20%)", 72, 66),
        ("Cost of Ownership (5%)", 74, 68),
        ("Market Position (5%)", 66, 62),
        ("Risk Factors (5%)", 74, 66),
    ]
    for lbl, a, k in cats:
        e.append(ScoreBar(lbl, a, k, width=430))
        e.append(sp(3))

    e.append(sp(12))
    # composite highlight
    comp = Table([["COMPOSITE SCORE", "Astrea: 74.0 / 100", "Kiaraville: 69.5 / 100", "Winner: ASTREA"]], colWidths=[4.5*cm, 4.5*cm, 4.5*cm, 3.5*cm])
    comp.setStyle(TableStyle([
        ("BACKGROUND",(0,0),(0,0),NAVY),("BACKGROUND",(1,0),(1,0),A_COL),
        ("BACKGROUND",(2,0),(2,0),K_COL),("BACKGROUND",(3,0),(3,0),GREEN),
        ("TEXTCOLOR",(0,0),(0,0),WHITE),("TEXTCOLOR",(3,0),(3,0),WHITE),
        ("FONTNAME",(0,0),(-1,-1),"Helvetica-Bold"),("FONTSIZE",(0,0),(-1,-1),9),
        ("ALIGN",(0,0),(-1,-1),"CENTER"),
        ("TOPPADDING",(0,0),(-1,-1),10),("BOTTOMPADDING",(0,0),(-1,-1),10),
    ]))
    e.append(comp); e.append(sp(12))

    e.append(Paragraph(
        "⚠ FOREIGN BUYER: RM 1,000,000 minimum (KL). Foreign stamp duty surcharge 4–8% applies on top of standard MOT. "
        "RPGT for foreigners: 30% Yr1–5, 10% from Yr6 (never 0%). MOF typically capped at 70%. "
        "Confirm all with your solicitor and banker.",
        st["warn"]
    ))
    e.append(sp(8))
    e.append(Paragraph(
        "DISCLAIMER: Educational/research purposes only. Not financial, investment, or legal advice. "
        "AI-generated approximations only. Verify with BOVAEP-registered REN/REA, licensed solicitor, and banker.",
        st["disc"]
    ))
    e.append(PageBreak())

    # ── PROFILES ───────────────────────────────────────────────────────────
    e += sec("Property Profiles", st)
    prof = [
        ["Detail", "Residensi Astrea", "Kiaraville"],
        ["Address", "Jalan Kiara 5, Mont Kiara", "Jalan Changkat Duta Kiara, MK"],
        ["Tenure", "Freehold", "Freehold"],
        ["Completed (VP)", "2023 (newest)", "2008 (18 yrs old)"],
        ["Developer", "UEM Sunrise Berhad", "Binaderas Sdn Bhd"],
        ["Blocks / Units", "1 block / 240 units", "6 blocks / 404 units"],
        ["Land Area", "2.4 acres", "6.74 acres"],
        ["Density", "100 units/acre", "60 units/acre"],
        ["Built-up Range", "1,364–1,859 sq ft", "1,593–3,935 sq ft"],
        ["Median Transacted PSF", "RM 874 psf", "RM 660 psf (–2.4% YoY)"],
        ["Foreign-Eligible Entry", "from RM 1.16M ✓", "from ~RM 1.05M ✓ (check unit)"],
        ["Maintenance Fee", "RM 0.35 psf/mo", "RM 0.40 psf/mo"],
        ["Typical Monthly Rent", "RM 5,000–9,000", "RM 4,500–7,500"],
        ["Rental Yield (est.)", "~4.5–5.5% gross", "~4.71% gross"],
    ]
    pt = Table(prof, colWidths=[4.5*cm, 6.5*cm, 6.5*cm])
    pt.setStyle(TableStyle([
        ("BACKGROUND",(0,0),(-1,0),NAVY),("TEXTCOLOR",(0,0),(-1,0),WHITE),
        ("FONTNAME",(0,0),(-1,0),"Helvetica-Bold"),
        ("BACKGROUND",(1,1),(1,-1),A_COL),("BACKGROUND",(2,1),(2,-1),K_COL),
        ("FONTSIZE",(0,0),(-1,-1),8),("ALIGN",(0,0),(-1,-1),"LEFT"),
        ("GRID",(0,0),(-1,-1),0.3,MGRAY),("LEFTPADDING",(0,0),(-1,-1),5),
        ("TOPPADDING",(0,0),(-1,-1),3),("BOTTOMPADDING",(0,0),(-1,-1),3),
        ("ROWBACKGROUNDS",(0,1),(-1,-1),[WHITE,LGRAY]),
        ("FONTNAME",(0,9),(0,9),"Helvetica-Bold"),("TEXTCOLOR",(0,9),(0,9),TEAL),
    ]))
    e.append(pt)

    # ── SCORECARD ──────────────────────────────────────────────────────────
    e += sec("Head-to-Head Scorecard", st)
    scores = [
        ["Category (Weight)", "Astrea", "Kiaraville", "Winner"],
        ["Price & Value (20%)", "70", "72", "Kiaraville"],
        ["Property Specs (10%)", "82", "72", "Astrea ✓"],
        ["Rental Income (20%)", "72", "68", "Astrea ✓"],
        ["Neighbourhood (15%)", "84", "84", "Tie"],
        ["Investment Potential (20%)", "72", "66", "Astrea ✓"],
        ["Cost of Ownership (5%)", "74", "68", "Astrea ✓"],
        ["Market Position (5%)", "66", "62", "Astrea ✓"],
        ["Risk Factors (5%)", "74", "66", "Astrea ✓"],
        ["COMPOSITE SCORE", "74.0 / 100", "69.5 / 100", "ASTREA"],
    ]
    st2 = Table(scores, colWidths=[5.5*cm, 3*cm, 3*cm, 5*cm])
    st2.setStyle(TableStyle([
        ("BACKGROUND",(0,0),(-1,0),NAVY),("TEXTCOLOR",(0,0),(-1,0),WHITE),
        ("FONTNAME",(0,0),(-1,0),"Helvetica-Bold"),
        ("BACKGROUND",(1,1),(1,-1),A_COL),("BACKGROUND",(2,1),(2,-1),K_COL),
        ("FONTNAME",(0,-1),(-1,-1),"Helvetica-Bold"),
        ("BACKGROUND",(0,-1),(-1,-1),TEAL),("TEXTCOLOR",(0,-1),(-1,-1),WHITE),
        ("BACKGROUND",(3,2),(3,2),GREEN),("TEXTCOLOR",(3,2),(3,2),WHITE),
        ("BACKGROUND",(3,3),(3,3),GREEN),("TEXTCOLOR",(3,3),(3,3),WHITE),
        ("BACKGROUND",(3,5),(3,5),GREEN),("TEXTCOLOR",(3,5),(3,5),WHITE),
        ("BACKGROUND",(3,6),(3,6),GREEN),("TEXTCOLOR",(3,6),(3,6),WHITE),
        ("BACKGROUND",(3,7),(3,7),GREEN),("TEXTCOLOR",(3,7),(3,7),WHITE),
        ("BACKGROUND",(3,8),(3,8),GREEN),("TEXTCOLOR",(3,8),(3,8),WHITE),
        ("BACKGROUND",(3,1),(3,1),K_COL),
        ("BACKGROUND",(2,9),(2,9),A_COL),
        ("FONTSIZE",(0,0),(-1,-1),9),("ALIGN",(1,0),(3,-1),"CENTER"),("ALIGN",(0,0),(0,-1),"LEFT"),
        ("ROWBACKGROUNDS",(0,1),(-1,-2),[WHITE,LGRAY]),
        ("GRID",(0,0),(-1,-1),0.3,MGRAY),("LEFTPADDING",(0,0),(-1,-1),5),
        ("TOPPADDING",(0,0),(-1,-1),4),("BOTTOMPADDING",(0,0),(-1,-1),4),
    ]))
    e.append(st2)
    e.append(PageBreak())

    # ── FOREIGN BUYER COST ─────────────────────────────────────────────────
    e += sec("Foreign Buyer Cost Breakdown", st)
    e.append(Paragraph(
        "Both properties clear the RM 1,000,000 foreign buyer minimum for KL. "
        "Foreign buyers are typically limited to 70% MOF. RPGT: 30% Yr1–5, then 10% (never 0%). "
        "Confirm stamp duty surcharge % with your solicitor.",
        st["body"]
    ))
    e.append(sp(6))

    e.append(Paragraph("Astrea — 1,364 sq ft @ RM 1,160,000", st["h3"]))
    a_cost = [
        ["Cost Item", "Calculation", "Amount"],
        ["Purchase Price", "—", "RM 1,160,000"],
        ["MOT Stamp Duty (local progressive)", "1%×RM100K + 2%×RM400K + 3%×RM500K + 4%×RM160K", "RM 33,400"],
        ["Foreign Surcharge (~6% est.)", "6% × RM 1,160,000", "RM 69,600"],
        ["Down Payment (30% — 70% MOF)", "30% × RM 1,160,000", "RM 348,000"],
        ["Loan Amount (70%)", "—", "RM 812,000"],
        ["Loan Stamp Duty (0.5%)", "0.5% × RM 812,000", "RM 4,060"],
        ["Legal Fees (SPA + loan, est.)", "—", "RM 12,000"],
        ["TOTAL UPFRONT CASH", "Down + all fees", "~RM 467,000"],
        ["Monthly Instalment (4.4%, 35yr)", "RM 812,000", "RM 3,854/mo"],
    ]
    e.append(mt(a_cost, [4.5*cm, 7*cm, 4.5*cm], hbg=TEAL, fs=8, bold_last=False))

    e.append(sp(10))
    e.append(Paragraph("Kiaraville — 1,593 sq ft @ RM 1,052,000 (RM 660 psf × 1,593 sq ft)", st["h3"]))
    k_cost = [
        ["Cost Item", "Calculation", "Amount"],
        ["Purchase Price", "—", "RM 1,052,000"],
        ["MOT Stamp Duty (local progressive)", "1%×RM100K + 2%×RM400K + 3%×RM500K + 4%×RM52K", "RM 26,080"],
        ["Foreign Surcharge (~6% est.)", "6% × RM 1,052,000", "RM 63,120"],
        ["Down Payment (30%)", "30% × RM 1,052,000", "RM 315,600"],
        ["Loan Amount (70%)", "—", "RM 736,400"],
        ["Loan Stamp Duty (0.5%)", "0.5% × RM 736,400", "RM 3,682"],
        ["Legal Fees (est.)", "—", "RM 11,000"],
        ["TOTAL UPFRONT CASH", "Down + all fees", "~RM 419,000"],
        ["Monthly Instalment (4.4%, 35yr)", "RM 736,400", "RM 3,496/mo"],
    ]
    e.append(mt(k_cost, [4.5*cm, 7*cm, 4.5*cm], hbg=NAVY, fs=8, bold_last=False))

    e.append(sp(8))
    e.append(Paragraph("Foreign Buyer RPGT Profile", st["h3"]))
    rpgt = [
        ["Hold Period", "RPGT Rate (Foreigner)", "On RM 100K gain", "vs Malaysian Citizen"],
        ["Year 1–5", "30%", "RM 30,000", "Same (30%)"],
        ["Year 6+", "10%", "RM 10,000", "0% for citizen"],
        ["Note", "Foreigners NEVER get 0% RPGT", "Always factor 10%+", "Plan exit accordingly"],
    ]
    e.append(mt(rpgt, [3*cm, 4*cm, 3.5*cm, 6*cm], hbg=RED, fs=8))
    e.append(PageBreak())

    # ── CATEGORY DETAIL ───────────────────────────────────────────────────
    e += sec("Category Analysis", st)

    cats_detail = [
        ("1. Price & Value — Winner: Kiaraville",
         "Kiaraville at RM 660 psf transacted is RM 214 psf cheaper than Astrea (RM 874 psf). "
         "On a 1,593 sq ft unit, that's RM 341K less for more space. However Kiaraville shows –2.4% YoY psf — mild depreciation signal. "
         "Astrea asking aligns closely to transacted = fair pricing with no premium overhang."),
        ("2. Property Specs — Winner: Astrea",
         "Astrea (2023): brand-new UEM Sunrise quality, dual facility decks (Stella Deck 8F + Astrea Deck 36F with sky lounge, sky gym, yoga, sunken pods), smart home features. "
         "Kiaraville (2008): 18 years old, larger unit sizes (up to 3,935 sq ft = big win for families), "
         "low-rise boutique feel, but dated facilities."),
        ("3. Rental Income — Winner: Astrea",
         "Astrea: RM 5,000–9,000/mo, ~4.5–5.5% gross yield at RM 1.16M entry. New product commands rent premium. "
         "Kiaraville: ~4.71% yield (slipped from 5.22% in 2022). Both benefit from MK's deep expat tenant pool (GIS, MKIS nearby)."),
        ("4. Neighbourhood — Tie (84/84)",
         "Both in Mont Kiara core: GIS, MKIS, 1 Mont Kiara, Plaza Mont Kiara, Solaris Dutamas, SPRINT access. Neither has walkable MRT. Genuinely tied."),
        ("5. Investment Potential — Winner: Astrea",
         "Astrea: new stock, brand recognition, stable-to-rising psf. Foreign buyer RPGT: 30% Yr1–5, 10% from Yr6. "
         "Kiaraville: value-add reno potential on older larger units; –2.4% YoY psf is a yellow flag; 404 units = more resale competition."),
        ("6. Cost of Ownership — Winner: Astrea",
         "Astrea: RM 0.35 psf/mo = RM 477/mo on 1,364 sq ft. New build = minimal CapEx risk near-term. "
         "Kiaraville: RM 0.40 psf/mo = RM 637/mo on 1,593 sq ft + 18-year-old M&E risk (lifts, HVAC, water tanks). "
         "Request sinking fund account balance before committing to Kiaraville."),
        ("7. Market Position — Winner: Astrea",
         "Astrea: 132 for sale / 139 for rent — active but manageable. Stable pricing. "
         "Kiaraville: 252+ listings for sale, rental yield trending down. Buyer has strong negotiating leverage — but signals softer demand."),
        ("8. Risk Factors — Winner: Astrea",
         "Astrea: minimal M&E risk (new); UEM Sunrise track record strong. Main risk: single tower on 2.4 acres = all 240 units competing internally on resale. "
         "Kiaraville: 18-year M&E risk (commission professional inspection); –2.4% YoY psf; 404 units = more competition. Both: foreign RPGT 10%+ from Yr6."),
    ]
    for title, body in cats_detail:
        e.append(Paragraph(title, st["h3"]))
        e.append(Paragraph(body, st["body"]))
        e.append(sp(4))

    e.append(PageBreak())

    # ── PROS & CONS ───────────────────────────────────────────────────────
    e += sec("Pros & Cons", st)
    pc = [
        ["", "Residensi Astrea", "Kiaraville"],
        ["PROS", "• Newest (2023) — UEM Sunrise quality\n• Dual facility decks (sky lounge, sky gym)\n• Low maint fee (RM 0.35 psf)\n• Stable-to-rising psf trend\n• Clears RM 1M foreign threshold cleanly", "• Lowest psf in MK (RM 660 transacted)\n• Largest land (6.74 acres)\n• Big unit sizes (up to 3,935 sq ft)\n• Rental track record (since 2008)\n• Strong buyer negotiation leverage"],
        ["CONS", "• Highest psf (RM 874)\n• Small land (2.4 acres, 1 tower)\n• Foreign RPGT 10%+ from Yr6 (never 0%)\n• 70% MOF cap = large upfront cash\n• Serviced residence title — confirm", "• Oldest (18 years) — M&E/CapEx risk\n• YoY psf –2.4% (depreciating)\n• Higher maint fee (RM 0.40 psf)\n• 404 units = more resale competition\n• Sinking fund check essential"],
    ]
    pct = Table(pc, colWidths=[2*cm, 8.5*cm, 7*cm])
    pct.setStyle(TableStyle([
        ("BACKGROUND",(0,0),(-1,0),NAVY),("TEXTCOLOR",(0,0),(-1,0),WHITE),
        ("FONTNAME",(0,0),(-1,0),"Helvetica-Bold"),
        ("BACKGROUND",(1,1),(1,-1),A_COL),("BACKGROUND",(2,1),(2,-1),K_COL),
        ("FONTNAME",(0,1),(0,-1),"Helvetica-Bold"),("TEXTCOLOR",(0,1),(0,1),GREEN),("TEXTCOLOR",(0,2),(0,2),RED),
        ("FONTSIZE",(0,0),(-1,-1),8),("ALIGN",(0,0),(-1,-1),"LEFT"),
        ("GRID",(0,0),(-1,-1),0.3,MGRAY),("VALIGN",(0,0),(-1,-1),"TOP"),
        ("LEFTPADDING",(0,0),(-1,-1),6),("TOPPADDING",(0,0),(-1,-1),6),("BOTTOMPADDING",(0,0),(-1,-1),6),
    ]))
    e.append(pct)

    # ── RECOMMENDATION ────────────────────────────────────────────────────
    e += sec("Recommendation", st)
    rec = [
        ["Goal", "Best Pick", "Why"],
        ["Foreign investor — yield & appreciation", "Astrea ★", "New stock, stable psf, stronger tenant confidence"],
        ["Foreign buyer — max space / family stay", "Kiaraville", "RM 660 psf buys 3,000 sq ft vs 1,800 sq ft at Astrea price"],
        ["Renovation value-add", "Kiaraville", "Older stock, deep psf discount, reno uplift potential"],
        ["Lowest upfront cash", "Kiaraville", "~RM 419K vs ~RM 467K for comparable budget"],
        ["Best facilities / lifestyle", "Astrea", "Sky lounge, sky gym, yoga deck, smart home"],
        ["Lowest ongoing carry", "Astrea", "RM 0.35 psf vs 0.40 psf + Astrea newer (less CapEx)"],
        ["Lowest RPGT exposure", "Both equal (foreign)", "Both: 30% Yr1–5, 10% Yr6+ — no difference"],
    ]
    rt = Table(rec, colWidths=[5.5*cm, 4.5*cm, 7*cm])
    rt.setStyle(TableStyle([
        ("BACKGROUND",(0,0),(-1,0),NAVY),("TEXTCOLOR",(0,0),(-1,0),WHITE),
        ("FONTNAME",(0,0),(-1,0),"Helvetica-Bold"),
        ("FONTNAME",(0,1),(0,-1),"Helvetica-Bold"),
        ("BACKGROUND",(0,1),(-1,1),colors.HexColor("#D5F5E3")),
        ("FONTSIZE",(0,0),(-1,-1),8.5),("ALIGN",(0,0),(-1,-1),"LEFT"),
        ("ROWBACKGROUNDS",(0,2),(-1,-1),[WHITE,LGRAY]),
        ("GRID",(0,0),(-1,-1),0.3,MGRAY),("LEFTPADDING",(0,0),(-1,-1),6),
        ("TOPPADDING",(0,0),(-1,-1),4),("BOTTOMPADDING",(0,0),(-1,-1),4),
    ]))
    e.append(rt)

    e.append(sp(12))
    e += sec("Next Steps", st)
    steps = [
        "1. Verify Astrea title type — confirm residential condominium vs serviced residence (affects MOF and utility tariff).",
        "2. Kiaraville: request MC management account + sinking fund balance before making any offer.",
        "3. Confirm foreign stamp duty surcharge % (4–8%) with a licensed solicitor — exact rate matters at this price point.",
        "4. Get loan pre-approval from bank: confirm 70% MOF available for your client's nationality.",
        "5. Engage BOVAEP-registered valuer for both before SPA signing.",
        "6. Run /realestate analyze Residensi Astrea Mont Kiara for full sub-scored deep-dive.",
        "7. Run /realestate analyze Kiaraville Mont Kiara for full sub-scored deep-dive.",
    ]
    for s in steps:
        e.append(Paragraph(s, st["body"]))
    e.append(sp(10))
    e.append(Paragraph(
        "DISCLAIMER: Educational/research only. Not financial, investment, or legal advice. "
        "Foreign buyer stamp duty, RPGT, and MOF caps must be confirmed with a licensed solicitor and banker. "
        "All figures are AI-generated estimates based on publicly available portal data.",
        st["disc"]
    ))

    doc.build(e, onFirstPage=on_page, onLaterPages=on_page)
    print(f"PDF saved: {path}")

if __name__ == "__main__":
    build()
