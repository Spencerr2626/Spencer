#!/usr/bin/env python3
"""PDF: Hijauan Kiara vs Trinity Pentamont — Mont Kiara Comparison."""

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

H_COL = colors.HexColor("#E8F4F8")   # Hijauan — blue tint
P_COL = colors.HexColor("#FEF9E7")   # Pentamont — gold tint
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
        # Hijauan bar
        c.setFillColor(LGRAY); c.rect(bx, by, bw, bh, fill=1, stroke=0)
        fc_a = GREEN if self.score_a >= 70 else (AMBER if self.score_a >= 55 else RED)
        c.setFillColor(fc_a); c.rect(bx, by, bw * self.score_a / 100, bh, fill=1, stroke=0)
        c.setFont("Helvetica-Bold", 7); c.setFillColor(NAVY)
        c.drawString(bx + bw + 2, by + 1, f"H:{self.score_a}")
        # Pentamont bar
        bx2 = bx + bw + 26
        c.setFillColor(LGRAY); c.rect(bx2, by, bw, bh, fill=1, stroke=0)
        fc_b = GREEN if self.score_b >= 70 else (AMBER if self.score_b >= 55 else RED)
        c.setFillColor(fc_b); c.rect(bx2, by, bw * self.score_b / 100, bh, fill=1, stroke=0)
        c.setFont("Helvetica-Bold", 7); c.setFillColor(NAVY)
        c.drawString(bx2 + bw + 2, by + 1, f"P:{self.score_b}")

def on_page(canv, doc):
    canv.saveState()
    canv.setFillColor(NAVY); canv.rect(0, HT - 1.8*cm, W, 1.8*cm, fill=1, stroke=0)
    canv.setFont("Helvetica-Bold", 10); canv.setFillColor(WHITE)
    canv.drawString(1.5*cm, HT - 1.2*cm, "COMPARISON: HIJAUAN KIARA vs TRINITY PENTAMONT  |  MONT KIARA")
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

def mt(data, cw, hbg=NAVY, fs=8):
    ts = [
        ("BACKGROUND",(0,0),(-1,0),hbg),("TEXTCOLOR",(0,0),(-1,0),WHITE),
        ("FONTNAME",(0,0),(-1,0),"Helvetica-Bold"),("FONTSIZE",(0,0),(-1,-1),fs),
        ("ALIGN",(1,0),(-1,-1),"RIGHT"),("ALIGN",(0,0),(0,-1),"LEFT"),
        ("ROWBACKGROUNDS",(0,1),(-1,-1),[WHITE,LGRAY]),
        ("GRID",(0,0),(-1,-1),0.3,MGRAY),("LEFTPADDING",(0,0),(-1,-1),5),
        ("RIGHTPADDING",(0,0),(-1,-1),5),("TOPPADDING",(0,0),(-1,-1),3),
        ("BOTTOMPADDING",(0,0),(-1,-1),3),
    ]
    return Table(data, colWidths=cw, style=TableStyle(ts), repeatRows=1)

def build():
    path = "PROPERTY-COMPARE-Hijauan-vs-Pentamont.pdf"
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

    sub = Table([["Hijauan Kiara  vs  Trinity Pentamont · Mont Kiara"]], colWidths=[W - 3.6*cm])
    sub.setStyle(TableStyle([
        ("BACKGROUND",(0,0),(-1,-1),TEAL),("TEXTCOLOR",(0,0),(-1,-1),WHITE),
        ("FONTNAME",(0,0),(-1,-1),"Helvetica-Bold"),("FONTSIZE",(0,0),(-1,-1),11),
        ("ALIGN",(0,0),(-1,-1),"CENTER"),("TOPPADDING",(0,0),(-1,-1),10),("BOTTOMPADDING",(0,0),(-1,-1),10),
    ]))
    e.append(sub); e.append(sp(16))

    cats = [
        ("Price & Value (20%)", 72, 68),
        ("Property Specs (10%)", 74, 80),
        ("Rental Income (20%)", 68, 78),
        ("Neighbourhood (15%)", 78, 80),
        ("Investment Potential (20%)", 66, 74),
        ("Cost of Ownership (5%)", 68, 72),
        ("Market Position (5%)", 64, 70),
        ("Risk Factors (5%)", 62, 72),
    ]
    for lbl, a, k in cats:
        e.append(ScoreBar(lbl, a, k, width=430))
        e.append(sp(3))

    e.append(sp(12))
    comp = Table([["COMPOSITE", "Hijauan: 70.0 / 100", "Pentamont: 74.7 / 100", "Winner: PENTAMONT"]],
                 colWidths=[3.5*cm, 4.7*cm, 4.9*cm, 3.9*cm])
    comp.setStyle(TableStyle([
        ("BACKGROUND",(0,0),(0,0),NAVY),("BACKGROUND",(1,0),(1,0),H_COL),
        ("BACKGROUND",(2,0),(2,0),P_COL),("BACKGROUND",(3,0),(3,0),GREEN),
        ("TEXTCOLOR",(0,0),(0,0),WHITE),("TEXTCOLOR",(3,0),(3,0),WHITE),
        ("FONTNAME",(0,0),(-1,-1),"Helvetica-Bold"),("FONTSIZE",(0,0),(-1,-1),9),
        ("ALIGN",(0,0),(-1,-1),"CENTER"),
        ("TOPPADDING",(0,0),(-1,-1),10),("BOTTOMPADDING",(0,0),(-1,-1),10),
    ]))
    e.append(comp); e.append(sp(12))

    e.append(Paragraph(
        "Both freehold, large-format Mont Kiara. Pentamont wins on yield, newness, liquidity and parking; "
        "Hijauan wins on price-per-sq-ft and low-density exclusivity. Hijauan transacted data is THIN (2 deals) — treat its value case as indicative.",
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
        ["Detail", "Hijauan Kiara", "Trinity Pentamont"],
        ["Address", "Jln Bukit Kiara 5, Mont Kiara", "Mont Kiara (off Jln Kiara)"],
        ["Tenure", "Freehold", "Freehold"],
        ["Completed (VP)", "2008 (~18 yrs)", "~2021-22 (~4-5 yrs)"],
        ["Developer", "Bukit Kiara Properties", "Trinity Group"],
        ["Blocks / Units", "7 blocks / 188 units", "41-storey / 330 units"],
        ["Land / Density", "5.4 acres · 35/acre (v.low)", "Higher density, 1 tower"],
        ["Built-up Range", "2,090-3,732 sq ft (PH 4,068+)", "1,379-4,115 sq ft"],
        ["Layouts", "3+1, 4+1", "3+1 to 5+1 (mostly 4-5 bed)"],
        ["Parking", "Full (undisclosed)", "~4 bays/unit (1,034) *"],
        ["Median Transacted PSF", "RM 732 (2 deals-thin)", "RM 831 (32 deals-healthy)"],
        ["Median Transacted Price", "RM 1,635,000", "RM 1,689,000"],
        ["Maintenance Fee", "RM 0.45 psf/mo", "RM 0.41 psf/mo"],
        ["Typical Monthly Rent", "RM 6,000-7,000", "RM 8,000-10,000"],
        ["Gross Yield (est.)", "~4.9-5.2%", "~6.0-6.4% *"],
        ["Signature", "Spa Island + private lift lobby", "Adventure-themed resort"],
    ]
    pt = Table(prof, colWidths=[4.2*cm, 6.6*cm, 6.7*cm])
    pt.setStyle(TableStyle([
        ("BACKGROUND",(0,0),(-1,0),NAVY),("TEXTCOLOR",(0,0),(-1,0),WHITE),
        ("FONTNAME",(0,0),(-1,0),"Helvetica-Bold"),
        ("BACKGROUND",(1,1),(1,-1),H_COL),("BACKGROUND",(2,1),(2,-1),P_COL),
        ("FONTSIZE",(0,0),(-1,-1),8),("ALIGN",(0,0),(-1,-1),"LEFT"),
        ("GRID",(0,0),(-1,-1),0.3,MGRAY),("LEFTPADDING",(0,0),(-1,-1),5),
        ("TOPPADDING",(0,0),(-1,-1),3),("BOTTOMPADDING",(0,0),(-1,-1),3),
        ("ROWBACKGROUNDS",(0,1),(-1,-1),[WHITE,LGRAY]),
    ]))
    e.append(pt)

    # ── SCORECARD ──
    e += sec("Head-to-Head Scorecard", st)
    scores = [
        ["Category (Weight)", "Hijauan", "Pentamont", "Winner"],
        ["Price & Value (20%)", "72", "68", "Hijauan"],
        ["Property Specs (10%)", "74", "80", "Pentamont"],
        ["Rental Income (20%)", "68", "78", "Pentamont"],
        ["Neighbourhood (15%)", "78", "80", "Pentamont"],
        ["Investment Potential (20%)", "66", "74", "Pentamont"],
        ["Cost of Ownership (5%)", "68", "72", "Pentamont"],
        ["Market Position (5%)", "64", "70", "Pentamont"],
        ["Risk Factors (5%)", "62", "72", "Pentamont"],
        ["COMPOSITE SCORE", "70.0 / 100", "74.7 / 100", "PENTAMONT"],
    ]
    # winner-highlight rows (Pentamont wins rows 2,3,4,5,6,7,8; Hijauan wins row 1)
    winrows = []
    st2ts = [
        ("BACKGROUND",(0,0),(-1,0),NAVY),("TEXTCOLOR",(0,0),(-1,0),WHITE),
        ("FONTNAME",(0,0),(-1,0),"Helvetica-Bold"),
        ("BACKGROUND",(1,1),(1,-1),H_COL),("BACKGROUND",(2,1),(2,-1),P_COL),
        ("FONTNAME",(0,-1),(-1,-1),"Helvetica-Bold"),
        ("BACKGROUND",(0,-1),(-1,-1),TEAL),("TEXTCOLOR",(0,-1),(-1,-1),WHITE),
        ("FONTSIZE",(0,0),(-1,-1),9),("ALIGN",(1,0),(3,-1),"CENTER"),("ALIGN",(0,0),(0,-1),"LEFT"),
        ("ROWBACKGROUNDS",(0,1),(-1,-2),[WHITE,LGRAY]),
        ("GRID",(0,0),(-1,-1),0.3,MGRAY),("LEFTPADDING",(0,0),(-1,-1),5),
        ("TOPPADDING",(0,0),(-1,-1),4),("BOTTOMPADDING",(0,0),(-1,-1),4),
    ]
    # green winner cells
    for r in [2,3,4,5,6,7,8]:
        st2ts += [("BACKGROUND",(3,r),(3,r),GREEN),("TEXTCOLOR",(3,r),(3,r),WHITE)]
    st2ts += [("BACKGROUND",(3,1),(3,1),GOLD),("TEXTCOLOR",(3,1),(3,1),WHITE)]  # Hijauan win
    st2ts += [("BACKGROUND",(2,9),(2,9),GREEN),("TEXTCOLOR",(2,9),(2,9),WHITE)]
    st2 = Table(scores, colWidths=[5.5*cm, 3*cm, 3*cm, 5*cm])
    st2.setStyle(TableStyle(st2ts))
    e.append(st2)
    e.append(PageBreak())

    # ── CATEGORY DETAIL ──
    e += sec("Category Analysis", st)
    cats_detail = [
        ("1. Price & Value - Winner: Hijauan Kiara",
         "Hijauan transacts at RM 732 psf vs Pentamont's RM 831 (~12% cheaper) with larger minimum built-ups (2,090 sq ft floor). "
         "Caveat: Hijauan's median rests on ONLY 2 transactions (May-Oct 2025) - directional, not robust. Pentamont's 32-deal median is far more reliable."),
        ("2. Property Specs - Winner: Trinity Pentamont",
         "Pentamont is ~13-14 years newer (2021 vs 2008), with a standout ~4-bay/unit parking ratio and a wider layout range. "
         "Hijauan counters with real exclusivity - private lift lobby per unit, max 2 units/floor, and one of Mont Kiara's lowest densities (35 units/acre)."),
        ("3. Rental Income - Winner: Trinity Pentamont",
         "Pentamont's ~6.0-6.4% gross yield is strong for MK luxury; Hijauan sits ~5%. Newer fit-out and resort facilities command RM 8-10k/mo on 2,000+ sq ft "
         "vs RM 6-7k at Hijauan. Both draw the same deep expat pool (GIS/MKIS families, Japanese/Korean/European, China mainland)."),
        ("4. Neighbourhood - Winner: Trinity Pentamont (slight)",
         "Both core Mont Kiara: international schools, malls (1MK, Publika, Plaza MK), hospitals, SPRINT/NKVE/Penchala Link. Neither has walkable rail. "
         "Hijauan's adjacency to the SPRINT elevated highway (noise) and TNB high-tension lines (a perception turn-off) tips it slightly to Pentamont."),
        ("5. Investment Potential - Winner: Trinity Pentamont",
         "Higher yield, newer asset (lower near-term CapEx), and critically - liquidity: 32 transactions/yr vs 2. Easier to exit at a defensible price. "
         "Hijauan's renovate value-add angle exists but is offset by thin transaction depth and an 18-year-old building."),
        ("6. Cost of Ownership - Winner: Trinity Pentamont",
         "Maintenance is close (RM 0.41 vs 0.45 psf/mo), but Pentamont's newer M&E means lower repair/sinking-fund risk. "
         "Hijauan's 18-year-old lifts, HVAC and water systems warrant a sinking-fund balance check before any offer."),
        ("7. Market Position - Winner: Trinity Pentamont",
         "Both buyer's markets. Pentamont's ~140 active for-sale listings signal liquidity and negotiation room; Hijauan's near-zero transaction volume "
         "signals thin demand - harder to price and to exit."),
        ("8. Risk Factors - Winner: Trinity Pentamont",
         "Hijauan carries: SPRINT noise, TNB high-tension-wire perception, thin liquidity, older building. Pentamont's main risks are a higher absolute "
         "entry (RM 1.7M+) and large-unit oversupply competition - but it's newer, liquid, and 95% taken up."),
    ]
    for title, body in cats_detail:
        e.append(Paragraph(title, st["h3"]))
        e.append(Paragraph(body, st["body"]))
        e.append(sp(4))
    e.append(PageBreak())

    # ── PROS & CONS ──
    e += sec("Pros & Cons", st)
    pc = [
        ["", "Hijauan Kiara", "Trinity Pentamont"],
        ["PROS", "- Cheapest psf (RM 732 transacted)\n- Very low density / exclusivity\n- Private lift lobby per unit\n- Large family layouts (2,090 sq ft floor)\n- Spa Island facilities",
                 "- Strong ~6% gross yield\n- Newer (2021-22)\n- Exceptional parking (~4 bays/unit)\n- Liquid (32 deals/yr)\n- Resort facilities, 95% taken up"],
        ["CONS", "- 18 years old (M&E/CapEx risk)\n- SPRINT highway noise\n- TNB high-tension lines nearby\n- Very thin transaction volume\n- Higher maintenance psf",
                 "- Higher psf (RM 831)\n- High absolute entry (RM 1.7M+)\n- Large units = shallower buyer pool\n- Oversupply competition\n- Polarising theme facilities"],
    ]
    pct = Table(pc, colWidths=[2*cm, 8*cm, 7.5*cm])
    pct.setStyle(TableStyle([
        ("BACKGROUND",(0,0),(-1,0),NAVY),("TEXTCOLOR",(0,0),(-1,0),WHITE),
        ("FONTNAME",(0,0),(-1,0),"Helvetica-Bold"),
        ("BACKGROUND",(1,1),(1,-1),H_COL),("BACKGROUND",(2,1),(2,-1),P_COL),
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
        ["Yield / rental investor", "Pentamont *", "~6% gross vs ~5%, newer, liquid"],
        ["Capital appreciation", "Pentamont", "Newer stock, defensible resale, 32-deal liquidity"],
        ["Cheapest entry per sq ft", "Hijauan", "RM 732 vs 831 psf transacted"],
        ["Low-density / privacy / own-stay", "Hijauan", "35 units/acre, private lift lobby, big layouts"],
        ["Renovate value-add", "Hijauan", "Older stock, deeper psf discount"],
        ["Lowest risk / easiest exit", "Pentamont", "Liquid, newer, no highway/TNB drag"],
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
        "The Catch (winner): Pentamont's large units mean a high absolute ticket (RM 1.7M+) and a shallower buyer/tenant pool - "
        "factor longer letting-up time and price on transacted RM 831 psf, not asking. Verify the sinking-fund split within the maintenance rate.",
        st["warn"]
    ))

    e.append(sp(10))
    e += sec("Next Steps", st)
    steps = [
        "1. Confirm Hijauan Kiara transacted comps beyond the 2 recent deals - the value case hinges on real liquidity.",
        "2. Pentamont: verify current live listing count + latest transacted psf on-portal before quoting a client.",
        "3. For either - request MC management + sinking-fund account balance (essential for the 18-yr-old Hijauan).",
        "4. Run /realestate analyze Trinity Pentamont Mont Kiara for a full sub-scored deep-dive.",
        "5. Foreign buyer: both clear the RM 1M KL minimum; model 70% MOF, 4-8% stamp-duty surcharge, RPGT 30% Yr1-5 / 10% Yr6+.",
    ]
    for s in steps:
        e.append(Paragraph(s, st["body"]))
    e.append(sp(10))
    e.append(Paragraph(
        "DISCLAIMER: Educational/research only. Not financial, investment, or legal advice. "
        "Hijauan Kiara transacted data is thin (2 deals) - treat as indicative. All figures are AI-generated estimates from public portal data.",
        st["disc"]
    ))

    doc.build(e, onFirstPage=on_page, onLaterPages=on_page)
    print(f"PDF saved: {path}")

if __name__ == "__main__":
    build()
