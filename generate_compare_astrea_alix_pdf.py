#!/usr/bin/env python3
"""PDF: Astrea Mont Kiara vs Alix Residences Segambut — Comparison."""

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
X_COL = colors.HexColor("#FEF9E7")   # Alix — gold tint
W, HT = A4

class ScoreBar(Flowable):
    def __init__(self, label, score_a, score_b, width=430, height=20):
        Flowable.__init__(self)
        self.label = label; self.score_a = score_a; self.score_b = score_b
        self.width = width; self.height = height

    def draw(self):
        c = self.canv
        bx, bw, bh = 155, (self.width - 170) // 2 - 4, 10
        by = (self.height - bh) / 2
        c.setFont("Helvetica", 8); c.setFillColor(DGRAY)
        c.drawString(0, by + 1, self.label)
        c.setFillColor(LGRAY); c.rect(bx, by, bw, bh, fill=1, stroke=0)
        fc_a = GREEN if self.score_a >= 70 else (AMBER if self.score_a >= 55 else RED)
        c.setFillColor(fc_a); c.rect(bx, by, bw * self.score_a / 100, bh, fill=1, stroke=0)
        c.setFont("Helvetica-Bold", 7); c.setFillColor(NAVY)
        c.drawString(bx + bw + 2, by + 1, f"Ast:{self.score_a}")
        bx2 = bx + bw + 30
        c.setFillColor(LGRAY); c.rect(bx2, by, bw, bh, fill=1, stroke=0)
        fc_b = GREEN if self.score_b >= 70 else (AMBER if self.score_b >= 55 else RED)
        c.setFillColor(fc_b); c.rect(bx2, by, bw * self.score_b / 100, bh, fill=1, stroke=0)
        c.setFont("Helvetica-Bold", 7); c.setFillColor(NAVY)
        c.drawString(bx2 + bw + 2, by + 1, f"Alix:{self.score_b}")

def on_page(canv, doc):
    canv.saveState()
    canv.setFillColor(NAVY); canv.rect(0, HT - 1.8*cm, W, 1.8*cm, fill=1, stroke=0)
    canv.setFont("Helvetica-Bold", 10); canv.setFillColor(WHITE)
    canv.drawString(1.5*cm, HT - 1.2*cm, "COMPARISON: ASTREA (MONT KIARA) vs ALIX (SEGAMBUT)")
    canv.setFont("Helvetica", 8); canv.setFillColor(GOLD)
    canv.drawRightString(W - 1.5*cm, HT - 1.2*cm, "3 July 2026")
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
        "disc": ps("disc",  fontSize=7,   textColor=DGRAY, fontName="Helvetica-Oblique", spaceAfter=6),
        "warn": ps("warn",  fontSize=8,   textColor=AMBER, fontName="Helvetica-Bold", spaceAfter=4),
    }

def sp(n=6): return Spacer(1, n)

def sec(text, st):
    return [sp(8), Paragraph(text, st["h2"]),
            HRFlowable(width="100%", thickness=1.5, color=TEAL, spaceAfter=6)]

def build():
    path = "PROPERTY-COMPARE-Astrea-vs-Alix.pdf"
    doc = SimpleDocTemplate(path, pagesize=A4,
        leftMargin=1.8*cm, rightMargin=1.8*cm,
        topMargin=2.2*cm, bottomMargin=1.6*cm)
    st = styles()
    e = []

    # ── COVER ──
    e.append(sp(1.5*cm))
    t = Table([["PROPERTY COMPARISON"]], colWidths=[W - 3.6*cm])
    t.setStyle(TableStyle([
        ("BACKGROUND",(0,0),(-1,-1),NAVY),("TEXTCOLOR",(0,0),(-1,-1),WHITE),
        ("FONTNAME",(0,0),(-1,-1),"Helvetica-Bold"),("FONTSIZE",(0,0),(-1,-1),22),
        ("ALIGN",(0,0),(-1,-1),"CENTER"),("TOPPADDING",(0,0),(-1,-1),14),("BOTTOMPADDING",(0,0),(-1,-1),14),
    ]))
    e.append(t); e.append(sp(4))

    sub = Table([["Astrea (Mont Kiara core)  vs  Alix Residences (Segambut / North Kiara)"]], colWidths=[W - 3.6*cm])
    sub.setStyle(TableStyle([
        ("BACKGROUND",(0,0),(-1,-1),TEAL),("TEXTCOLOR",(0,0),(-1,-1),WHITE),
        ("FONTNAME",(0,0),(-1,-1),"Helvetica-Bold"),("FONTSIZE",(0,0),(-1,-1),10.5),
        ("ALIGN",(0,0),(-1,-1),"CENTER"),("TOPPADDING",(0,0),(-1,-1),10),("BOTTOMPADDING",(0,0),(-1,-1),10),
    ]))
    e.append(sub); e.append(sp(16))

    cats = [
        ("Price & Value (20%)", 69, 72),
        ("Property Specs (10%)", 76, 80),
        ("Rental Income (20%)", 76, 60),
        ("Neighbourhood (15%)", 82, 64),
        ("Investment Potential (20%)", 74, 60),
        ("Cost of Ownership (5%)", 74, 70),
        ("Market Position (5%)", 68, 62),
        ("Risk Factors (5%)", 72, 58),
    ]
    for lbl, a, k in cats:
        e.append(ScoreBar(lbl, a, k, width=430))
        e.append(sp(3))

    e.append(sp(12))
    comp = Table([["COMPOSITE", "Astrea: 74.4 / 100", "Alix: 65.5 / 100", "Winner: ASTREA"]],
                 colWidths=[3.5*cm, 4.7*cm, 4.4*cm, 4.4*cm])
    comp.setStyle(TableStyle([
        ("BACKGROUND",(0,0),(0,0),NAVY),("BACKGROUND",(1,0),(1,0),A_COL),
        ("BACKGROUND",(2,0),(2,0),X_COL),("BACKGROUND",(3,0),(3,0),GREEN),
        ("TEXTCOLOR",(0,0),(0,0),WHITE),("TEXTCOLOR",(3,0),(3,0),WHITE),
        ("FONTNAME",(0,0),(-1,-1),"Helvetica-Bold"),("FONTSIZE",(0,0),(-1,-1),9),
        ("ALIGN",(0,0),(-1,-1),"CENTER"),
        ("TOPPADDING",(0,0),(-1,-1),10),("BOTTOMPADDING",(0,0),(-1,-1),10),
    ]))
    e.append(comp); e.append(sp(12))

    e.append(Paragraph(
        "CROSS-SUBMARKET: Astrea is Mont Kiara core; Alix is the Segambut / North Kiara fringe (~RM 700 psf belt). "
        "The psf gap is largely a LOCATION gap, not a bargain. Alix transacted data is very thin (new project) - pricing is indicative only.",
        st["warn"]
    ))
    e.append(sp(8))
    e.append(Paragraph(
        "DISCLAIMER: Educational/research purposes only. Not financial, investment, or legal advice. "
        "AI-generated approximations only. Verify with BOVAEP-registered REN/REA, licensed solicitor, and banker.",
        st["disc"]
    ))
    e.append(PageBreak())

    # ── PROFILES ──
    e += sec("Property Profiles", st)
    prof = [
        ["Detail", "Astrea (Mont Kiara)", "Alix (Segambut)"],
        ["Location", "Jln Kiara 5, MK core", "Jln Dutamas Raya, Segambut fringe"],
        ["Tenure", "Freehold", "Freehold"],
        ["Completed (VP)", "2023", "~2024 (newly completed)"],
        ["Developer", "UEM Sunrise", "TA Global"],
        ["Blocks / Units", "1 blk / 240 / 37 st", "2 twr / 364 / 22 & 35 st"],
        ["Land / Density", "2.4 ac · ~100/ac", "4.55 ac · ~80/ac"],
        ["Built-up Range", "1,364-1,859 sq ft (3BR)", "1,485-2,476 sq ft (4BR/4+1)"],
        ["Parking", "~2 bays (verify)", "2-4 bays *"],
        ["Median Transacted PSF", "RM 874 (13 deals)", "~RM 700-760 (thin/new)"],
        ["Median / Indic. Price", "RM 1,228,000", "~RM 1.25M+ (ask 631-939 psf)"],
        ["Maintenance Fee", "RM 0.35 psf/mo", "RM 0.38 psf/mo"],
        ["Typical Monthly Rent", "RM 6,500-8,000", "RM 3,700-4,000 (1,744 sf)"],
        ["Gross Yield (est.)", "~5.5-6.0% *", "~3.8%"],
        ["Title (verify on SPA)", "Condo (some tag SR)", "Condo"],
    ]
    pt = Table(prof, colWidths=[4.2*cm, 6.6*cm, 6.7*cm])
    pt.setStyle(TableStyle([
        ("BACKGROUND",(0,0),(-1,0),NAVY),("TEXTCOLOR",(0,0),(-1,0),WHITE),
        ("FONTNAME",(0,0),(-1,0),"Helvetica-Bold"),
        ("BACKGROUND",(1,1),(1,-1),A_COL),("BACKGROUND",(2,1),(2,-1),X_COL),
        ("FONTSIZE",(0,0),(-1,-1),8),("ALIGN",(0,0),(-1,-1),"LEFT"),
        ("GRID",(0,0),(-1,-1),0.3,MGRAY),("LEFTPADDING",(0,0),(-1,-1),5),
        ("TOPPADDING",(0,0),(-1,-1),3),("BOTTOMPADDING",(0,0),(-1,-1),3),
        ("ROWBACKGROUNDS",(0,1),(-1,-1),[WHITE,LGRAY]),
    ]))
    e.append(pt)

    # ── SCORECARD ──
    e += sec("Head-to-Head Scorecard", st)
    scores = [
        ["Category (Weight)", "Astrea", "Alix", "Winner"],
        ["Price & Value (20%)", "69", "72", "Alix"],
        ["Property Specs (10%)", "76", "80", "Alix"],
        ["Rental Income (20%)", "76", "60", "Astrea"],
        ["Neighbourhood (15%)", "82", "64", "Astrea"],
        ["Investment Potential (20%)", "74", "60", "Astrea"],
        ["Cost of Ownership (5%)", "74", "70", "Astrea"],
        ["Market Position (5%)", "68", "62", "Astrea"],
        ["Risk Factors (5%)", "72", "58", "Astrea"],
        ["COMPOSITE SCORE", "74.4 / 100", "65.5 / 100", "ASTREA"],
    ]
    st2ts = [
        ("BACKGROUND",(0,0),(-1,0),NAVY),("TEXTCOLOR",(0,0),(-1,0),WHITE),
        ("FONTNAME",(0,0),(-1,0),"Helvetica-Bold"),
        ("BACKGROUND",(1,1),(1,-1),A_COL),("BACKGROUND",(2,1),(2,-1),X_COL),
        ("FONTNAME",(0,-1),(-1,-1),"Helvetica-Bold"),
        ("BACKGROUND",(0,-1),(-1,-1),TEAL),("TEXTCOLOR",(0,-1),(-1,-1),WHITE),
        ("FONTSIZE",(0,0),(-1,-1),9),("ALIGN",(1,0),(3,-1),"CENTER"),("ALIGN",(0,0),(0,-1),"LEFT"),
        ("ROWBACKGROUNDS",(0,1),(-1,-2),[WHITE,LGRAY]),
        ("GRID",(0,0),(-1,-1),0.3,MGRAY),("LEFTPADDING",(0,0),(-1,-1),5),
        ("TOPPADDING",(0,0),(-1,-1),4),("BOTTOMPADDING",(0,0),(-1,-1),4),
    ]
    for r in [3,4,5,6,7,8]:  # Astrea wins
        st2ts += [("BACKGROUND",(3,r),(3,r),GREEN),("TEXTCOLOR",(3,r),(3,r),WHITE)]
    for r in [1,2]:          # Alix wins
        st2ts += [("BACKGROUND",(3,r),(3,r),GOLD),("TEXTCOLOR",(3,r),(3,r),WHITE)]
    st2ts += [("BACKGROUND",(1,9),(1,9),GREEN),("TEXTCOLOR",(1,9),(1,9),WHITE)]
    st2 = Table(scores, colWidths=[5.5*cm, 3*cm, 3*cm, 5*cm])
    st2.setStyle(TableStyle(st2ts))
    e.append(st2)
    e.append(PageBreak())

    # ── CATEGORY DETAIL ──
    e += sec("Category Analysis", st)
    cats_detail = [
        ("1. Price & Value - Winner: Alix (slight)",
         "Alix's ~RM 700 psf vs Astrea's RM 874 buys more space (up to 2,476 sq ft, 4+1) for the money, both freehold. "
         "But the ~20% discount reflects Segambut's fringe status, not underpricing - within its own belt (~RM 650-750) Alix is FAIR, not cheap. "
         "Astrea's transacted RM 874 sits just below its asking cluster = mild buyer leverage in MK core."),
        ("2. Property Specs - Winner: Alix",
         "Alix has bigger family layouts (4BR standard, up to 2,476 sq ft), more parking (2-4 bays), rich facilities (sky futsal, tennis, sky pool, theatre). "
         "Astrea is newer-feeling UEM Sunrise quality with dual sky decks (8F + 36F) but smaller 3BR units and ~2 bays."),
        ("3. Rental Income - Winner: Astrea",
         "Decisive. Astrea yields ~5.5-6.0% gross (RM 6,500-8,000/mo) - above the MK average - vs Alix's ~3.8% (big units + fringe location drag rent). "
         "Astrea's MK-core expat tenant demand (GIS/MKIS families) is far deeper than Segambut's."),
        ("4. Neighbourhood - Winner: Astrea",
         "Mont Kiara core (international schools, 1MK/Publika/Plaza MK, hospitals, established expat hub) clearly outranks the Segambut/North Kiara fringe, "
         "which carries flood-exposure history near the river, chronic traffic, and transit years out (MRT3 ~2032). Neither has walkable rail today."),
        ("5. Investment Potential - Winner: Astrea",
         "Higher yield, better resale liquidity (13 transactions vs ~1), stronger appreciation support from a prime address. "
         "Alix's angle is a cheaper freehold entry with big units, but thin price discovery, area oversupply and flood/transit risk weaken the case."),
        ("6. Cost of Ownership - Winner: Astrea (slight)",
         "Maintenance is close (RM 0.35 vs 0.38 psf/mo); both new = low near-term CapEx. Astrea's smaller units mean a lower absolute monthly carry."),
        ("7. Market Position - Winner: Astrea",
         "Both buyer's markets. Astrea has real liquidity and demand; Alix offers more negotiation room (wide RM 631-939 psf asking spread = motivated sellers) "
         "but signals softer absorption and harder exit."),
        ("8. Risk Factors - Winner: Astrea",
         "Alix carries more: Segambut flood exposure, thin transaction history (exit-liquidity risk), area oversupply, transit years away, condo-vs-SR title to verify. "
         "Astrea's main risks are MK high-rise oversupply and its own thin resale sample. Lower overall risk on Astrea."),
    ]
    for title, body in cats_detail:
        e.append(Paragraph(title, st["h3"]))
        e.append(Paragraph(body, st["body"]))
        e.append(sp(4))
    e.append(PageBreak())

    # ── PROS & CONS ──
    e += sec("Pros & Cons", st)
    pc = [
        ["", "Astrea (Mont Kiara)", "Alix (Segambut)"],
        ["PROS", "- Freehold in MK core\n- Above-market yield (~5.5-6%)\n- New (2023), UEM Sunrise quality\n- Low density (240 units)\n- Deep expat tenant pool",
                 "- Cheapest entry (~RM 700 psf)\n- Freehold\n- Big 4BR family layouts + parking\n- Rich facilities\n- TA Global pedigree"],
        ["CONS", "- Higher psf (RM 874)\n- Smaller 3BR units\n- Thin resale liquidity (13 deals)\n- MK oversupply caps appreciation\n- Title condo-vs-SR to confirm",
                 "- Fringe Segambut address\n- Low yield (~3.8%)\n- Flood-prone area history\n- Very thin transaction data\n- Transit years out; oversupply belt"],
    ]
    pct = Table(pc, colWidths=[2*cm, 8*cm, 7.5*cm])
    pct.setStyle(TableStyle([
        ("BACKGROUND",(0,0),(-1,0),NAVY),("TEXTCOLOR",(0,0),(-1,0),WHITE),
        ("FONTNAME",(0,0),(-1,0),"Helvetica-Bold"),
        ("BACKGROUND",(1,1),(1,-1),A_COL),("BACKGROUND",(2,1),(2,-1),X_COL),
        ("FONTNAME",(0,1),(0,-1),"Helvetica-Bold"),("TEXTCOLOR",(0,1),(0,1),GREEN),("TEXTCOLOR",(0,2),(0,2),RED),
        ("FONTSIZE",(0,0),(-1,-1),8),("ALIGN",(0,0),(-1,-1),"LEFT"),
        ("GRID",(0,0),(-1,-1),0.3,MGRAY),("VALIGN",(0,0),(-1,-1),"TOP"),
        ("LEFTPADDING",(0,0),(-1,-1),6),("TOPPADDING",(0,0),(-1,-1),6),("BOTTOMPADDING",(0,0),(-1,-1),6),
    ]))
    e.append(pct)

    # ── RECOMMENDATION ──
    e += sec("Recommendation", st)
    rec = [
        ["Goal", "Best Pick", "Why"],
        ["Overall winner", "Astrea *", "74.4 vs 65.5 - wins 6 of 8 categories"],
        ["Cash flow / yield", "Astrea", "~5.5-6% vs ~3.8%"],
        ["Capital appreciation", "Astrea", "Prime address, resale liquidity"],
        ["Own-stay / big family space", "Alix", "4+1, up to 2,476 sq ft, more parking, for less"],
        ["Value-entry / lowest ticket", "Alix", "~RM 700 psf freehold near MK"],
        ["Lowest risk / easiest exit", "Astrea", "Liquid, prime, no flood/transit drag"],
    ]
    rt = Table(rec, colWidths=[5.5*cm, 4*cm, 7.5*cm])
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
    e.append(sp(8))
    e.append(Paragraph(
        "The Catch (Astrea): you pay a MK-core premium (RM 874 psf) into an oversupplied high-rise market that caps appreciation - "
        "the return case leans on yield + rentability, not price growth. Confirm title type (condo vs serviced residence) before committing.",
        st["warn"]
    ))

    e.append(sp(10))
    e += sec("Next Steps", st)
    steps = [
        "1. Verify title type on both (condo vs serviced residence) - affects utility tariff, quit rent, and MOF.",
        "2. Alix: check exact block flood elevation (Segambut river proximity) and pull agency co-broke transacted data - brickz is too thin.",
        "3. Astrea: request MC sinking-fund balance; confirm current maintenance rate + parking bays.",
        "4. Foreign buyer: both clear the RM 1M KL minimum; model 70% MOF, 4-8% stamp-duty surcharge, RPGT 30% Yr1-5 / 10% Yr6+.",
        "5. Run /realestate analyze Residensi Astrea Mont Kiara for a full sub-scored deep-dive.",
    ]
    for s in steps:
        e.append(Paragraph(s, st["body"]))
    e.append(sp(10))
    e.append(Paragraph(
        "DISCLAIMER: Educational/research only. Not financial, investment, or legal advice. Cross-submarket comparison (MK core vs Segambut fringe) - "
        "the psf gap is largely locational. Alix transacted data is very thin (new project); treat pricing as indicative. AI-generated estimates.",
        st["disc"]
    ))

    doc.build(e, onFirstPage=on_page, onLaterPages=on_page)
    print(f"PDF saved: {path}")

if __name__ == "__main__":
    build()
