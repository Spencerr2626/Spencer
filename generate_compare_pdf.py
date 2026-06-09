#!/usr/bin/env python3
"""3-Way Property Comparison PDF — Damai vs Hijauan Kiara vs Mont Kiara Aman."""

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table,
                                TableStyle, HRFlowable, PageBreak)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_RIGHT

NAVY = colors.HexColor('#1B2A4A')
DARK = colors.HexColor('#333333')
MED = colors.HexColor('#666666')
LIGHT = colors.HexColor('#F5F5F5')
GREEN = colors.HexColor('#2E7D32')
AMBER = colors.HexColor('#F9A825')
GOLD = colors.HexColor('#C9A227')
WHITE = colors.white
BORDER = colors.HexColor('#CCCCCC')

base = getSampleStyleSheet()
H1 = ParagraphStyle('H1', parent=base['Heading1'], fontName='Helvetica-Bold',
                    fontSize=14, textColor=WHITE, backColor=NAVY, leading=20,
                    spaceBefore=12, spaceAfter=6, leftIndent=6)
H2 = ParagraphStyle('H2', parent=base['Heading2'], fontName='Helvetica-Bold',
                    fontSize=11, textColor=NAVY, spaceBefore=8, spaceAfter=3)
BODY = ParagraphStyle('B', parent=base['Normal'], fontName='Helvetica',
                      fontSize=8.5, textColor=DARK, leading=12, spaceAfter=3)
BUL = ParagraphStyle('Bul', parent=BODY, leftIndent=10)
CEN = ParagraphStyle('C', parent=base['Normal'], fontName='Helvetica',
                     fontSize=9, textColor=DARK, alignment=TA_CENTER)
DISC = ParagraphStyle('D', parent=base['Normal'], fontName='Helvetica',
                      fontSize=7, textColor=MED, alignment=TA_CENTER, leading=9)
TITLE = ParagraphStyle('T', parent=base['Title'], fontName='Helvetica-Bold',
                       fontSize=20, textColor=NAVY, alignment=TA_CENTER, spaceAfter=4)


def sc_color(v):
    return GREEN if v >= 70 else (AMBER if v >= 55 else colors.HexColor('#C62828'))


def tbl(data, widths, header=True, compact=False, align_center_from=1):
    fs = 8 if compact else 8.5
    t = Table(data, colWidths=widths)
    style = [('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
             ('FONTSIZE', (0, 0), (-1, -1), fs),
             ('TEXTCOLOR', (0, 0), (-1, -1), DARK),
             ('ROWBACKGROUNDS', (0, 0), (-1, -1), [WHITE, LIGHT]),
             ('GRID', (0, 0), (-1, -1), 0.4, BORDER),
             ('LEFTPADDING', (0, 0), (-1, -1), 5),
             ('RIGHTPADDING', (0, 0), (-1, -1), 5),
             ('TOPPADDING', (0, 0), (-1, -1), 3.5),
             ('BOTTOMPADDING', (0, 0), (-1, -1), 3.5),
             ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
             ('ALIGN', (align_center_from, 0), (-1, -1), 'CENTER')]
    if header:
        style += [('BACKGROUND', (0, 0), (-1, 0), NAVY),
                  ('TEXTCOLOR', (0, 0), (-1, 0), WHITE),
                  ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                  ('ALIGN', (0, 0), (-1, 0), 'CENTER')]
    t.setStyle(TableStyle(style))
    return t


def build():
    doc = SimpleDocTemplate('PROPERTY-COMPARE-MontKiara-3way.pdf', pagesize=A4,
                            leftMargin=0.55 * inch, rightMargin=0.55 * inch,
                            topMargin=0.55 * inch, bottomMargin=0.6 * inch)
    W = A4[0] - 1.1 * inch
    s = []
    DISCLAIMER = ('For educational/research purposes only. Not financial or investment advice. '
                  'AI-generated estimates; Hijauan median psf partly estimated (thin volume). '
                  'Verify on PropertyGuru/iProperty/EdgeProp/brickz before acting.')

    # ---- Cover ----
    s.append(Spacer(1, 0.2 * inch))
    s.append(Paragraph('PROPERTY COMPARISON', TITLE))
    s.append(Paragraph('Three-Way Head-to-Head &mdash; Mont Kiara Luxury Condos', CEN))
    s.append(Paragraph('8 June 2026', CEN))
    s.append(Spacer(1, 0.12 * inch))
    s.append(HRFlowable(width=W, thickness=2, color=NAVY))
    s.append(Spacer(1, 0.18 * inch))

    contenders = [
        ['', 'Mont Kiara Damai', 'Hijauan Kiara', 'Mont Kiara Aman'],
        ['Composite', '65.0', '72.2', '72.7'],
        ['Tenure', 'Freehold', 'Freehold', 'Freehold'],
        ['Completed', '2004', '2008', '2005'],
        ['Density', '6/floor', 'Lowest (<=2/fl)', 'High (2 towers)'],
        ['Entry', '~RM 2.0m+', 'RM 1.55-2.8m', 'from RM 1.48m'],
        ['Median psf', 'RM 677', '~RM 690-750', 'RM 674'],
    ]
    ct = tbl(contenders, [W * 0.22, W * 0.26, W * 0.26, W * 0.26])
    ct.setStyle(TableStyle([
        ('FONTNAME', (0, 1), (0, -1), 'Helvetica-Bold'),
        ('FONTNAME', (1, 1), (-1, 1), 'Helvetica-Bold'),
        ('FONTSIZE', (1, 1), (-1, 1), 12),
        ('TEXTCOLOR', (1, 1), (1, 1), sc_color(65.0)),
        ('TEXTCOLOR', (2, 1), (2, 1), sc_color(72.2)),
        ('TEXTCOLOR', (3, 1), (3, 1), sc_color(72.7)),
        ('BACKGROUND', (3, 0), (3, 0), GOLD),
    ]))
    s.append(ct)
    s.append(Spacer(1, 0.1 * inch))
    s.append(Paragraph('<b>WINNER: Mont Kiara Aman (72.7)</b> &mdash; narrowly, on yield, liquidity '
                       'and lowest carry. <b>Hijauan Kiara (72.2)</b> is effectively tied and wins on '
                       'exclusivity &amp; risk. <b>Damai (65.0)</b> trails but offers the deepest '
                       'renovate-and-resell value-add.', BODY))
    s.append(Spacer(1, 0.1 * inch))
    s.append(Paragraph('All three are <b>freehold, Sunrise-built condos in the Mont Kiara core</b> '
                       '&mdash; so neighbourhood is a tie and the contest is decided on price/value, '
                       'density, unit size, yield and liquidity.', BODY))
    s.append(Spacer(1, 0.15 * inch))
    s.append(Paragraph(DISCLAIMER, DISC))
    s.append(PageBreak())

    # ---- Scorecard ----
    s.append(Paragraph('&nbsp;Head-to-Head Scorecard', H1))
    s.append(Spacer(1, 0.06 * inch))
    rows = [['Category (weight)', 'Damai', 'Hijauan', 'Aman', 'Winner'],
            ['Price & Value (20%)', '68', '76', '74', 'Hijauan'],
            ['Property Specs (10%)', '72', '80', '68', 'Hijauan'],
            ['Rental Income (20%)', '56', '64', '70', 'Aman'],
            ['Neighbourhood (15%)', '84', '84', '84', 'Tie'],
            ['Investment Potential (20%)', '58', '67', '70', 'Aman'],
            ['Cost of Ownership (5%)', '60', '68', '76', 'Aman'],
            ['Market Position (5%)', '56', '60', '68', 'Aman'],
            ['Risk Factors (5%)', '60', '76', '66', 'Hijauan'],
            ['COMPOSITE SCORE', '65.0', '72.2', '72.7', 'Aman']]
    st = tbl(rows, [W * 0.34, W * 0.14, W * 0.15, W * 0.14, W * 0.23])
    st.setStyle(TableStyle([
        ('FONTNAME', (0, 9), (-1, 9), 'Helvetica-Bold'),
        ('BACKGROUND', (0, 9), (-1, 9), LIGHT),
        ('TEXTCOLOR', (1, 9), (1, 9), sc_color(65)),
        ('TEXTCOLOR', (2, 9), (2, 9), sc_color(72.2)),
        ('TEXTCOLOR', (3, 9), (3, 9), sc_color(72.7)),
        ('FONTNAME', (3, 9), (3, 9), 'Helvetica-Bold'),
    ]))
    s.append(st)

    s.append(Spacer(1, 0.14 * inch))
    s.append(Paragraph('&nbsp;Property Profiles', H1))
    s.append(Spacer(1, 0.06 * inch))
    prof = [
        ['Detail', 'Damai', 'Hijauan', 'Aman'],
        ['Address', 'Jln Kiara 2', 'Jln Kiara 5', 'Jln Kiara 2'],
        ['Developer', 'Sunrise', 'Sunrise', 'UEM Sunrise'],
        ['Units / Land', '230 / 8.7 ac', '188 / 5.4 ac', '345 / 5.8 ac'],
        ['Built-up (std)', '2,272-3,325', '2,090-3,732', '1,600-2,648'],
        ['Larger units', 'to 11,000 sf', 'PH to 5,045', 'PH 4,300'],
        ['Asking psf', 'RM 707-1,020', 'RM 603-786', '~RM 600-750'],
        ['Maint. fee', 'RM 0.33 psf', 'RM 0.35 psf', '~RM 0.34 psf'],
        ['Typical rent', 'RM 5.5-9k', 'RM 6-7k', 'RM 5-7k'],
    ]
    s.append(tbl(prof, [W * 0.20, W * 0.27, W * 0.27, W * 0.26], compact=True))
    s.append(Spacer(1, 0.1 * inch))
    s.append(Paragraph('<b>Read:</b> Hijauan = newest + most exclusive (lowest density). '
                       'Aman = cheapest entry + best yield/liquidity (smallest units). '
                       'Damai = biggest units + deepest psf discount, but oldest and least liquid.', BODY))
    s.append(PageBreak())

    # ---- Category detail ----
    s.append(Paragraph('&nbsp;Category Detail', H1))
    cats = [
        ('1. Price & Value &mdash; Hijauan', 'Hijauan has the lowest psf band (RM 603-786) AND the lowest '
         'density &mdash; most value-for-product. Aman is the cheapest absolute entry (from RM 1.48m). '
         'Damai transacts at RM 677 psf but huge units inflate absolute price; weak at the top of its asking.'),
        ('2. Specs &mdash; Hijauan', 'Hijauan: newest (2008), garden low-rise, <=2 units/floor (best privacy). '
         'Damai: biggest units in MK (to 11,000 sf) but oldest (2004). Aman: smallest units in denser towers.'),
        ('3. Rental Income &mdash; Aman', 'Aman: smaller units + low entry = best gross yield (~4-5%) and '
         'deepest tenant pool. Hijauan ~4-4.5% on a low-psf entry. Damai weakest (~2.6-4.3%) &mdash; large '
         'built-ups depress rent-per-psf; appreciation-led.'),
        ('4. Neighbourhood &mdash; Tie (84)', 'All in the MK core: GIS/MKIS international schools, 1MK / '
         'Plaza MK / Solaris, SPRINT access. No walkable MRT/LRT for any (car-dependent). Genuinely tied.'),
        ('5. Investment Potential &mdash; Aman', 'Aman: best yield + liquidity, freehold, RPGT-free after Yr5. '
         'Hijauan: strongest capital-preservation (scarcity, 188 low-density units). Damai: best value-add '
         '(oldest, biggest discount) but thin large-unit resale.'),
        ('6. Cost of Ownership &mdash; Aman', 'Maintenance psf is similar, so absolute carry tracks unit size. '
         'Aman (smallest) = lowest carry; Damai (largest) = highest.'),
        ('7. Market Position &mdash; Aman', 'Aman\'s smaller, cheaper units transact most often = best '
         'liquidity. Damai (big units) and Hijauan (only 188 units) are thinner. All freehold; broad KL '
         'high-rise overhang applies.'),
        ('8. Risk &mdash; Hijauan', 'Hijauan: newest + lowest density + freehold = lowest risk (small resale '
         'pool the only knock). Aman: denser = internal resale competition. Damai: oldest = higher CapEx/'
         'sinking-fund and liquidity risk.'),
    ]
    for h, b in cats:
        s.append(Paragraph(h, H2))
        s.append(Paragraph(b, BODY))
    s.append(PageBreak())

    # ---- Pros/Cons + Recommendation ----
    s.append(Paragraph('&nbsp;Pros & Cons', H1))
    pc = [
        ('Mont Kiara Damai',
         'Biggest units in MK; lowest transacted psf (RM 677); Sunrise pedigree; strong renovate-and-resell value-add.',
         'Oldest (2004) = CapEx/sinking-fund risk; large units = poor liquidity & thin yield; negative leveraged cash flow.'),
        ('Hijauan Kiara',
         'Newest (2008); lowest density in MK (188 units); lowest psf band; freehold; lowest risk; superb own-stay.',
         'Small project = thin resale/rental volume; modest yield; larger layouts cost more in absolute RM.'),
        ('Mont Kiara Aman',
         'Lowest entry (from RM 1.48m); best yield + liquidity; lowest carry; deep expat tenant pool for 2-3 bed.',
         'Densest of the three (345 units) = less exclusivity + internal resale competition; 2005 stock may need refresh.'),
    ]
    for name, pros, cons in pc:
        s.append(Paragraph(name, H2))
        s.append(Paragraph('<b>Pros:</b> ' + pros, BODY))
        s.append(Paragraph('<b>Cons:</b> ' + cons, BODY))
    s.append(Spacer(1, 0.1 * inch))

    s.append(Paragraph('&nbsp;Recommendation', H1))
    s.append(Spacer(1, 0.05 * inch))
    box = Table([[Paragraph('OVERALL WINNER: MONT KIARA AMAN (72.7) &mdash; '
                            'narrowly over Hijauan Kiara (72.2)',
                            ParagraphStyle('w', parent=CEN, fontName='Helvetica-Bold',
                                           fontSize=11, textColor=WHITE))]], colWidths=[W])
    box.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, -1), GOLD),
                             ('TOPPADDING', (0, 0), (-1, -1), 8),
                             ('BOTTOMPADDING', (0, 0), (-1, -1), 8)]))
    s.append(box)
    s.append(Spacer(1, 0.08 * inch))
    recs = [
        ('Best for Cash Flow / Yield', 'Mont Kiara Aman &mdash; smaller units + low entry = best gross yield, easiest to let.'),
        ('Best for Capital Appreciation', 'Hijauan Kiara &mdash; scarcity & ultra-low density preserve value.'),
        ('Best for Own-Stay / First Luxury Home', 'Hijauan (lifestyle) or Aman (budget entry from RM 1.48m).'),
        ('Best for Renovate-and-Resell', 'Mont Kiara Damai &mdash; oldest, deepest psf discount, large units (mind RPGT before Yr6).'),
        ('The Catch (winner Aman)', 'Densest of the three &mdash; trades exclusivity for liquidity; you compete with other owners on resale. If prestige > yield, buy Hijauan.'),
    ]
    rtab = [[Paragraph('<b>' + k + '</b>', BODY), Paragraph(v, BODY)] for k, v in recs]
    rt = Table(rtab, colWidths=[W * 0.32, W * 0.68])
    rt.setStyle(TableStyle([('ROWBACKGROUNDS', (0, 0), (-1, -1), [WHITE, LIGHT]),
                            ('GRID', (0, 0), (-1, -1), 0.4, BORDER),
                            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                            ('LEFTPADDING', (0, 0), (-1, -1), 6),
                            ('TOPPADDING', (0, 0), (-1, -1), 4),
                            ('BOTTOMPADDING', (0, 0), (-1, -1), 4)]))
    s.append(rt)
    s.append(Spacer(1, 0.14 * inch))
    s.append(HRFlowable(width=W, thickness=0.5, color=BORDER))
    s.append(Spacer(1, 0.06 * inch))
    s.append(Paragraph(DISCLAIMER, DISC))
    s.append(Paragraph('Generated by AI Real Estate Analyst &middot; 8 June 2026 &middot; '
                       'Sources: PropertyGuru, iProperty, EdgeProp, brickz, Property Genie, montkiara.properties.', DISC))

    def footer(c, d):
        c.saveState()
        c.setFont('Helvetica', 7)
        c.setFillColor(MED)
        c.drawString(0.55 * inch, 0.4 * inch, 'Mont Kiara 3-Way Comparison')
        c.drawRightString(A4[0] - 0.55 * inch, 0.4 * inch, f'Page {d.page}')
        c.restoreState()

    doc.build(s, onFirstPage=footer, onLaterPages=footer)
    print('PDF saved: PROPERTY-COMPARE-MontKiara-3way.pdf')


if __name__ == '__main__':
    build()
