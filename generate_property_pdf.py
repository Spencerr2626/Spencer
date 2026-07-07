#!/usr/bin/env python3
"""
Property Analysis PDF Generator — Mont Kiara Damai Resort Condominium
"""

import math
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, PageBreak, KeepTogether
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.graphics.shapes import Drawing, Rect, String, Line
from reportlab.graphics import renderPDF
from reportlab.graphics.charts.barcharts import HorizontalBarChart
from reportlab.platypus.flowables import Flowable

# ── BRAND COLORS ──────────────────────────────────────────────────────────────
NAVY       = colors.HexColor('#1B2A4A')
DARK_GRAY  = colors.HexColor('#333333')
MED_GRAY   = colors.HexColor('#666666')
LIGHT_GRAY = colors.HexColor('#F5F5F5')
GREEN      = colors.HexColor('#2E7D32')
YELLOW     = colors.HexColor('#F9A825')
RED        = colors.HexColor('#C62828')
ACCENT     = colors.HexColor('#1565C0')
WHITE      = colors.white
BORDER     = colors.HexColor('#CCCCCC')

# ── SCORE COLOR ───────────────────────────────────────────────────────────────
def score_color(score):
    if score >= 70: return GREEN
    if score >= 40: return YELLOW
    return RED

def score_grade(score):
    if score >= 85: return 'A+'
    if score >= 70: return 'A'
    if score >= 55: return 'B'
    if score >= 40: return 'C'
    if score >= 25: return 'D'
    return 'F'

def score_signal(score):
    if score >= 85: return 'Strong Buy'
    if score >= 70: return 'Buy'
    if score >= 55: return 'Watch'
    if score >= 40: return 'Caution'
    if score >= 25: return 'Pass'
    return 'Avoid'

# ── GAUGE FLOWABLE ─────────────────────────────────────────────────────────────
class ScoreGauge(Flowable):
    def __init__(self, score, size=140):
        super().__init__()
        self.score = score
        self.size  = size
        self.width = size
        self.height = size * 0.65

    def draw(self):
        s    = self.score
        sz   = self.size
        cx   = sz / 2
        cy   = sz * 0.35
        r    = sz * 0.38
        lw   = sz * 0.09

        # background arc (180°)
        start_deg = 0
        end_deg   = 180

        # track
        self.canv.setStrokeColor(LIGHT_GRAY)
        self.canv.setLineWidth(lw)
        self.canv.arc(cx - r, cy - r, cx + r, cy + r, startAng=0, extent=180)

        # coloured fill arc
        fill_extent = (s / 100) * 180
        col = score_color(s)
        self.canv.setStrokeColor(col)
        self.canv.arc(cx - r, cy - r, cx + r, cy + r, startAng=0, extent=fill_extent)

        # score number
        self.canv.setFillColor(DARK_GRAY)
        self.canv.setFont('Helvetica-Bold', sz * 0.20)
        self.canv.drawCentredString(cx, cy + sz * 0.02, str(s))

        self.canv.setFont('Helvetica', sz * 0.09)
        self.canv.setFillColor(MED_GRAY)
        self.canv.drawCentredString(cx, cy - sz * 0.11, '/100')

        grade = score_grade(s)
        self.canv.setFont('Helvetica-Bold', sz * 0.12)
        self.canv.setFillColor(col)
        self.canv.drawCentredString(cx, cy - sz * 0.27, grade)


# ── SCORE BAR FLOWABLE ─────────────────────────────────────────────────────────
class ScoreBar(Flowable):
    def __init__(self, label, score, width=300, height=18, weight=None):
        super().__init__()
        self.label  = label
        self.score  = score
        self.bwidth = width
        self.width  = width
        self.height = height + 4
        self.weight = weight

    def draw(self):
        bar_w   = self.bwidth * 0.55
        bar_h   = self.height - 4
        bar_x   = self.bwidth * 0.40
        bar_y   = 2
        fill_w  = (self.score / 100) * bar_w
        col     = score_color(self.score)

        # label
        lbl = self.label
        if self.weight:
            lbl += f'  ({self.weight})'
        self.canv.setFont('Helvetica', 8)
        self.canv.setFillColor(DARK_GRAY)
        self.canv.drawString(0, bar_y + 3, lbl)

        # track
        self.canv.setFillColor(LIGHT_GRAY)
        self.canv.rect(bar_x, bar_y, bar_w, bar_h, fill=1, stroke=0)

        # fill
        if fill_w > 0:
            self.canv.setFillColor(col)
            self.canv.rect(bar_x, bar_y, fill_w, bar_h, fill=1, stroke=0)

        # score label
        self.canv.setFont('Helvetica-Bold', 8)
        self.canv.setFillColor(DARK_GRAY)
        self.canv.drawString(bar_x + bar_w + 6, bar_y + 3, f'{self.score}')


# ── STYLES ─────────────────────────────────────────────────────────────────────
def make_styles():
    base = getSampleStyleSheet()
    styles = {}

    styles['title'] = ParagraphStyle('title',
        parent=base['Title'],
        fontName='Helvetica-Bold',
        fontSize=22,
        textColor=NAVY,
        spaceAfter=6,
        alignment=TA_CENTER,
    )
    styles['subtitle'] = ParagraphStyle('subtitle',
        parent=base['Normal'],
        fontName='Helvetica',
        fontSize=12,
        textColor=MED_GRAY,
        spaceAfter=4,
        alignment=TA_CENTER,
    )
    styles['h1'] = ParagraphStyle('h1',
        parent=base['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=14,
        textColor=WHITE,
        backColor=NAVY,
        spaceBefore=14,
        spaceAfter=6,
        leftIndent=-10,
        rightIndent=-10,
        leading=20,
    )
    styles['h2'] = ParagraphStyle('h2',
        parent=base['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=11,
        textColor=NAVY,
        spaceBefore=10,
        spaceAfter=4,
    )
    styles['body'] = ParagraphStyle('body',
        parent=base['Normal'],
        fontName='Helvetica',
        fontSize=9,
        textColor=DARK_GRAY,
        spaceAfter=4,
        leading=13,
    )
    styles['body_small'] = ParagraphStyle('body_small',
        parent=base['Normal'],
        fontName='Helvetica',
        fontSize=8,
        textColor=DARK_GRAY,
        spaceAfter=3,
        leading=11,
    )
    styles['bullet'] = ParagraphStyle('bullet',
        parent=base['Normal'],
        fontName='Helvetica',
        fontSize=9,
        textColor=DARK_GRAY,
        spaceAfter=3,
        leading=13,
        leftIndent=12,
        bulletIndent=2,
    )
    styles['center'] = ParagraphStyle('center',
        parent=base['Normal'],
        fontName='Helvetica',
        fontSize=9,
        textColor=DARK_GRAY,
        alignment=TA_CENTER,
    )
    styles['disclaimer'] = ParagraphStyle('disclaimer',
        parent=base['Normal'],
        fontName='Helvetica',
        fontSize=7,
        textColor=MED_GRAY,
        alignment=TA_CENTER,
        leading=10,
    )
    styles['signal_green'] = ParagraphStyle('signal_green',
        parent=base['Normal'],
        fontName='Helvetica-Bold',
        fontSize=16,
        textColor=GREEN,
        alignment=TA_CENTER,
        spaceAfter=4,
    )
    styles['signal_yellow'] = ParagraphStyle('signal_yellow',
        parent=base['Normal'],
        fontName='Helvetica-Bold',
        fontSize=16,
        textColor=YELLOW,
        alignment=TA_CENTER,
        spaceAfter=4,
    )
    return styles


# ── TABLE HELPER ───────────────────────────────────────────────────────────────
def make_table(data, col_widths, header=True, compact=False):
    fs = 8 if compact else 9
    tbl = Table(data, colWidths=col_widths)
    style = [
        ('FONTNAME',  (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE',  (0, 0), (-1, -1), fs),
        ('TEXTCOLOR', (0, 0), (-1, -1), DARK_GRAY),
        ('ROWBACKGROUNDS', (0, 0), (-1, -1), [WHITE, LIGHT_GRAY]),
        ('GRID',      (0, 0), (-1, -1), 0.4, BORDER),
        ('LEFTPADDING',  (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
        ('TOPPADDING',   (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING',(0, 0), (-1, -1), 4),
        ('VALIGN',    (0, 0), (-1, -1), 'MIDDLE'),
    ]
    if header:
        style += [
            ('BACKGROUND', (0, 0), (-1, 0), NAVY),
            ('TEXTCOLOR',  (0, 0), (-1, 0), WHITE),
            ('FONTNAME',   (0, 0), (-1, 0), 'Helvetica-Bold'),
        ]
    tbl.setStyle(TableStyle(style))
    return tbl


def section_header(text, styles):
    p = Paragraph(f'&nbsp;&nbsp;{text}', styles['h1'])
    return p


# ── PAGE TEMPLATE (footer) ─────────────────────────────────────────────────────
def add_footer(canvas, doc):
    canvas.saveState()
    canvas.setFont('Helvetica', 7)
    canvas.setFillColor(MED_GRAY)
    canvas.drawString(inch * 0.6, 0.45 * inch,
        'For educational/research purposes only. Not financial or investment advice.')
    canvas.drawRightString(letter[0] - inch * 0.6, 0.45 * inch,
        f'Page {doc.page}')
    canvas.restoreState()


# ── MAIN ───────────────────────────────────────────────────────────────────────
def build_pdf(output='PROPERTY-REPORT-Mont-Kiara-Damai.pdf'):
    doc = SimpleDocTemplate(
        output,
        pagesize=letter,
        leftMargin=0.6*inch, rightMargin=0.6*inch,
        topMargin=0.6*inch,  bottomMargin=0.7*inch,
    )
    styles = make_styles()
    story  = []
    W = letter[0] - 1.2*inch   # usable width

    DISCLAIMER = ('DISCLAIMER: For educational/research purposes only. '
                  'Not financial or investment advice. '
                  'All estimates are AI-generated approximations based on publicly available data. '
                  'Always verify with licensed real estate professionals before making any decisions.')

    # ── PAGE 1: COVER ──────────────────────────────────────────────────────────
    story.append(Spacer(1, 0.3*inch))
    story.append(Paragraph('PROPERTY ANALYSIS REPORT', styles['title']))
    story.append(Paragraph('Mont Kiara Damai Resort Condominium', ParagraphStyle(
        'addr', parent=styles['subtitle'], fontSize=14, textColor=NAVY,
        fontName='Helvetica-Bold', spaceAfter=2)))
    story.append(Paragraph('Jalan Kiara 2, Mont Kiara, Kuala Lumpur', styles['subtitle']))
    story.append(Paragraph('8 June 2026', styles['subtitle']))
    story.append(Spacer(1, 0.15*inch))
    story.append(HRFlowable(width=W, thickness=2, color=NAVY))
    story.append(Spacer(1, 0.2*inch))

    # Gauge centred
    gauge = ScoreGauge(68, size=160)
    gauge_table = Table([[gauge]], colWidths=[W])
    gauge_table.setStyle(TableStyle([('ALIGN', (0,0), (-1,-1), 'CENTER')]))
    story.append(gauge_table)
    story.append(Spacer(1, 0.1*inch))

    story.append(Paragraph('Property Score: 68/100', ParagraphStyle(
        'sc', parent=styles['center'], fontName='Helvetica-Bold', fontSize=13, textColor=NAVY)))
    story.append(Paragraph('Grade: B  ·  Signal: WATCH / SELECTIVE BUY', ParagraphStyle(
        'gr', parent=styles['center'], fontName='Helvetica-Bold', fontSize=11,
        textColor=YELLOW, spaceAfter=8)))

    story.append(Spacer(1, 0.15*inch))
    cover_data = [
        ['Asking Range', 'RM 707–1,020 psf', 'Tenure', 'Freehold'],
        ['Base Case Price', 'RM 2,500,000', 'Completed', '2004'],
        ['Unit Size', '2,272–3,325 sq ft', 'Developer', 'Sunrise Berhad'],
        ['Floors / Units', '40 floors / 230 units', 'Density', '6 units/floor'],
    ]
    col = W / 4
    tbl = make_table(cover_data, [col]*4, header=False)
    story.append(tbl)
    story.append(Spacer(1, 0.3*inch))
    story.append(Paragraph(DISCLAIMER, styles['disclaimer']))
    story.append(PageBreak())

    # ── PAGE 2: EXECUTIVE SUMMARY ──────────────────────────────────────────────
    story.append(section_header('EXECUTIVE SUMMARY & PROPERTY PROFILE', styles))
    story.append(Spacer(1, 0.08*inch))

    story.append(Paragraph(
        'Mont Kiara Damai Resort Condominium is a freehold luxury high-rise at Jalan Kiara 2 — '
        "KL's premier expat enclave. Developed by Sunrise Berhad and completed in 2004, "
        'the 40-storey, 230-unit tower offers unusually large units (2,272–11,000 sq ft) at '
        'just 6 units per floor, giving it a boutique density rare in the corridor.',
        styles['body']))
    story.append(Paragraph(
        'The property scores <b>68/100 (Grade B — Watch / Selective Buy)</b>. Its strongest '
        'dimensions are Neighborhood Quality (85/100) and Comparable Value (71/100), underpinned '
        'by the best international school cluster in KL and a robust Japanese/Korean/European expat '
        'tenant pool. The drag: thin net yields (1.6–2.9%) and negative leveraged cash flow across '
        'all scenarios. This is a capital-appreciation play, not a yield investment.',
        styles['body']))
    story.append(Spacer(1, 0.1*inch))

    story.append(Paragraph('Property Profile', styles['h2']))
    prop_data = [
        ['Detail', 'Value', 'Detail', 'Value'],
        ['Address', 'Jalan Kiara 2, Mont Kiara, KL', 'Tenure', 'Freehold'],
        ['Developer', 'Sunrise Berhad', 'Completed', '2004'],
        ['Floors', '40', 'Total Units', '230 (6/floor)'],
        ['Standard Unit', '2,272–3,325 sq ft', 'Super Deluxe', '5,733–5,934 sq ft'],
        ['Base Case Price', 'RM 2,500,000', 'Price PSF', 'RM 893'],
        ['Asking PSF Range', 'RM 707–1,020', 'Median Transacted PSF', 'RM 677'],
        ['Facilities', 'Pool, Gym, Tennis, Squash, Sauna, BBQ, 24hr Security, Mini Market, Nursery, Business Centre', '', ''],
    ]
    col2 = [W*0.22, W*0.28, W*0.22, W*0.28]
    story.append(make_table(prop_data, col2))
    story.append(Spacer(1, 0.12*inch))

    story.append(Paragraph('Key Findings', styles['h2']))
    findings = [
        'Low end of asking (RM 707 psf) represents genuine value — 25% below luxury comp benchmark (RM 941 psf weighted avg)',
        'Negative leveraged cash flow across all scenarios; breakeven rent ~RM 10,600/month vs market RM 7,000–9,000',
        'Exceptional neighborhood: KL\'s densest international school cluster, 50%+ expat residents, SPRINT Expressway km0',
        'No MRT — structural weakness; 37 new launch pipeline adds rental competition for older stock',
        'Best strategy: Negotiate to RM 2.0–2.2M, renovate (RM 150–170k), hold 7–10 years RPGT-free',
    ]
    for f in findings:
        story.append(Paragraph(f'• {f}', styles['bullet']))

    story.append(PageBreak())

    # ── PAGE 3: SCORE DASHBOARD ────────────────────────────────────────────────
    story.append(section_header('SCORE DASHBOARD', styles))
    story.append(Spacer(1, 0.08*inch))

    scores = [
        ('Value & Comps',        71, '25%'),
        ('Income Potential',     58, '20%'),
        ('Neighborhood Quality', 85, '20%'),
        ('Investment Upside',    56, '20%'),
        ('Market Conditions',    67, '15%'),
    ]

    bar_items = []
    for label, score, weight in scores:
        bar_items.append(ScoreBar(label, score, width=W*0.95, weight=weight))
        bar_items.append(Spacer(1, 4))

    composite_score = 68
    composite_row = [
        [Paragraph('<b>COMPOSITE PROPERTY SCORE</b>', ParagraphStyle(
            'cps', parent=styles['body'], fontName='Helvetica-Bold', fontSize=10)),
         Paragraph(f'<b>{composite_score}/100</b>', ParagraphStyle(
             'cpv', parent=styles['body'], fontName='Helvetica-Bold', fontSize=10,
             textColor=score_color(composite_score), alignment=TA_RIGHT))],
    ]
    comp_tbl = Table(composite_row, colWidths=[W*0.75, W*0.25])
    comp_tbl.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), LIGHT_GRAY),
        ('GRID', (0,0), (-1,-1), 0.4, BORDER),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
    ]))

    score_table_data = [
        ['Category', 'Score', 'Weight', 'Weighted'],
        ['Value & Comps',        '71/100', '25%', '17.75'],
        ['Income Potential',     '58/100', '20%', '11.60'],
        ['Neighborhood Quality', '85/100', '20%', '17.00'],
        ['Investment Upside',    '56/100', '20%', '11.20'],
        ['Market Conditions',    '67/100', '15%', '10.05'],
        ['COMPOSITE SCORE',      '',       '',     '67.6 / 100'],
    ]
    score_tbl = make_table(score_table_data, [W*0.40, W*0.18, W*0.18, W*0.24])
    score_tbl.setStyle(TableStyle([
        ('FONTNAME',  (0, 6), (-1, 6), 'Helvetica-Bold'),
        ('BACKGROUND',(0, 6), (-1, 6), LIGHT_GRAY),
        ('TEXTCOLOR', (3, 6), (3, 6), score_color(68)),
    ]))

    # Two-column: bars left, table right
    left_col = bar_items
    right_col = [score_tbl, Spacer(1, 10), comp_tbl]

    two_col = Table([[left_col, right_col]], colWidths=[W*0.48, W*0.50])
    two_col.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('LEFTPADDING', (0,0), (-1,-1), 0),
        ('RIGHTPADDING', (0,0), (-1,-1), 0),
    ]))
    story.append(two_col)
    story.append(PageBreak())

    # ── PAGE 4: COMPARABLE SALES ───────────────────────────────────────────────
    story.append(section_header('COMPARABLE SALES ANALYSIS', styles))
    story.append(Spacer(1, 0.08*inch))

    comp_data = [
        ['Property', 'Tenure', 'Built', 'Median PSF', 'Median Price', 'Relevance'],
        ['Mont Kiara Damai (subject)', 'Freehold', '2004', 'RM 677', 'RM 2,050,000', '—'],
        ['10 Mont Kiara (MK10)',       'Freehold', '2006', 'RM 985', 'RM 3,660,000', 'High'],
        ['11 Mont Kiara (MK11)',       'Freehold', '2009', 'RM 953', 'RM 3,270,000', 'High'],
        ['Seni Mont Kiara',           'Freehold', '2010', 'RM 878', 'RM 2,650,000', 'High'],
        ['Arcoris Residences',        'Freehold', '2015', 'RM 1,071','RM 789,400',  'Medium'],
        ['Kiaramas Sutera',           'Freehold', '2003', 'RM 470', 'RM 865,000',   'Medium'],
        ['Mont Kiara suburb-wide',    'Mixed',    'Mixed','RM 808',  'RM 1,550,000', 'Benchmark'],
    ]
    story.append(make_table(comp_data,
        [W*0.28, W*0.12, W*0.09, W*0.14, W*0.18, W*0.14], compact=True))

    story.append(Spacer(1, 0.1*inch))
    story.append(Paragraph('Weighted Benchmark (High-Relevance Comps)', styles['h2']))
    bench_data = [
        ['Comp', 'Weight', 'PSF'],
        ['10 Mont Kiara', '35%', 'RM 985'],
        ['11 Mont Kiara', '35%', 'RM 953'],
        ['Seni Mont Kiara', '30%', 'RM 878'],
        ['Weighted Average', '', 'RM 941'],
    ]
    bench_tbl = make_table(bench_data, [W*0.45, W*0.20, W*0.20])
    bench_tbl.setStyle(TableStyle([
        ('FONTNAME',  (0, 4), (-1, 4), 'Helvetica-Bold'),
        ('BACKGROUND',(0, 4), (-1, 4), LIGHT_GRAY),
    ]))
    story.append(bench_tbl)

    story.append(Spacer(1, 0.1*inch))
    story.append(Paragraph('Price Alignment Assessment', styles['h2']))
    align_data = [
        ['Asking Range', 'vs Weighted Benchmark (RM 941)', 'Assessment'],
        ['RM 707 psf (low)',  '–25% discount', '✓ Good value for decent-condition units'],
        ['RM 850–870 psf',   '–8% to –7%',   '✓ Fair — in line with suburb median'],
        ['RM 1,020 psf (top)','+ 8%',         '⚠ Only for renovated, high-floor, premium view'],
        ['Own median: RM 677','–28%',          '↓ Age/liquidity discount built in'],
    ]
    story.append(make_table(align_data, [W*0.22, W*0.25, W*0.48], compact=True))

    story.append(Spacer(1, 0.1*inch))
    story.append(Paragraph('Comps Score Breakdown: 71/100', styles['h2']))
    comps_score_data = [
        ['Dimension', 'Score /20', 'Notes'],
        ['Data Quality',      '14', 'Real transaction data; thin subject volume (7 deals)'],
        ['Price Alignment',   '15', 'Low/mid asking straddles market; no wild overpricing'],
        ['Comp Relevance',    '13', 'MK10/MK11/Seni highly comparable; others for context'],
        ['Market Trend',      '14', 'Gentle upward trend; expat demand supports price floor'],
        ['Value Assessment',  '15', 'Age discount appropriately priced at RM 677–750 psf'],
        ['TOTAL',             '71', ''],
    ]
    story.append(make_table(comps_score_data, [W*0.28, W*0.16, W*0.52], compact=True))
    story.append(PageBreak())

    # ── PAGE 5: RENTAL ANALYSIS ────────────────────────────────────────────────
    story.append(section_header('RENTAL INCOME & CASH FLOW ANALYSIS', styles))
    story.append(Paragraph(
        'Base case: ~2,800 sq ft, 4+1 bed / 4 bath unit | Purchase price: RM 2,500,000 | '
        'Loan: 70% LTV @ 4.5% p.a., 30 years = RM 8,866/month',
        styles['body_small']))
    story.append(Spacer(1, 0.08*inch))

    story.append(Paragraph('Three-Scenario Cash Flow Projection', styles['h2']))
    cf_data = [
        ['Metric', 'Conservative', 'Moderate', 'Optimistic'],
        ['Monthly Rent',              'RM 5,500',    'RM 7,000',    'RM 9,000'],
        ['Vacancy (7%)',              '– RM 385',    '– RM 490',    '– RM 630'],
        ['Effective Gross Income/mo', 'RM 5,115',    'RM 6,510',    'RM 8,370'],
        ['Total Expenses/mo',         '– RM 1,800',  '– RM 2,050',  '– RM 2,383'],
        ['NOI / month',               'RM 3,315',    'RM 4,460',    'RM 5,987'],
        ['Mortgage / month',          '– RM 8,866',  '– RM 8,866',  '– RM 8,866'],
        ['Leveraged Cash Flow/mo',    '– RM 5,551',  '– RM 4,406',  '– RM 2,879'],
        ['Gross Yield',               '2.64%',       '3.36%',       '4.32%'],
        ['Net Yield (NOI / Price)',   '1.59%',       '2.14%',       '2.87%'],
        ['Gross Rent Multiplier',     '37.9×',       '29.8×',       '23.1×'],
    ]
    cf_tbl = make_table(cf_data, [W*0.35, W*0.21, W*0.21, W*0.21])
    # highlight negative rows
    neg_rows = [7]  # leveraged cf row
    cf_tbl.setStyle(TableStyle([
        ('TEXTCOLOR', (1, 8), (3, 8), RED),
        ('TEXTCOLOR', (1, 9), (3, 9), MED_GRAY),
        ('FONTNAME', (0, 7), (-1, 7), 'Helvetica-Bold'),
        ('TEXTCOLOR', (1, 7), (3, 7), RED),
    ]))
    story.append(cf_tbl)

    story.append(Spacer(1, 0.1*inch))
    story.append(Paragraph('Expense Breakdown (Moderate Scenario)', styles['h2']))
    exp_data = [
        ['Expense Item', 'Monthly (RM)', 'Annual (RM)'],
        ['Property Management (9%)',     '630',    '7,560'],
        ['Maintenance / Sinking Fund',   '650',    '7,800'],
        ['Insurance (fire + liability)', '200',    '2,400'],
        ['Cukai Pintu + Cukai Tanah',    '264',    '3,172'],
        ['CapEx Reserve (5% gross)',      '350',    '4,200'],
        ['TOTAL',                        '2,094', '25,132'],
    ]
    story.append(make_table(exp_data, [W*0.52, W*0.23, W*0.23], compact=True))

    story.append(Spacer(1, 0.08*inch))
    story.append(Paragraph(
        '⚠ Breakeven rent for leveraged purchase = ~RM 10,600/month — well above current market (RM 7,000–9,000). '
        'This is fundamentally an equity/capital-appreciation investment, not a cashflow investment. '
        'Unleveraged investors earn RM 3,315–5,987/month net income.',
        ParagraphStyle('warn', parent=styles['body'], textColor=RED, fontName='Helvetica-Bold')))

    story.append(Spacer(1, 0.06*inch))
    story.append(Paragraph('Rental Score: 58/100', styles['h2']))
    rs_data = [
        ['Factor', 'Score /20', 'Notes'],
        ['Location & Expat Demand', '18', 'KL\'s #1 expat enclave; JP/KR/EU corporate tenants'],
        ['Net Yield (1.6–2.9%)',    '10', 'Below 4–5% investor threshold'],
        ['Vacancy Risk',            '14', 'Low structural vacancy near international schools'],
        ['Building Age/Condition',  '7',  '2004 vintage; renovation recommended for top rents'],
        ['Leveraged Cash Flow',     '5',  'Negative in all scenarios at 70% LTV'],
        ['Liquidity / Exit',        '4',  'Reasonable resale; freehold positive'],
        ['TOTAL',                   '58', ''],
    ]
    story.append(make_table(rs_data, [W*0.30, W*0.16, W*0.50], compact=True))
    story.append(PageBreak())

    # ── PAGE 6: NEIGHBORHOOD ───────────────────────────────────────────────────
    story.append(section_header('NEIGHBORHOOD REPORT', styles))
    story.append(Spacer(1, 0.08*inch))

    story.append(Paragraph('Neighborhood Scorecard: 85/100', styles['h2']))
    nb_bars = []
    nb_scores = [
        ('School Quality', 18, 20),
        ('Safety & Security', 16, 20),
        ('Amenities & Walkability', 17, 20),
        ('Expat Demand & Demographics', 19, 20),
        ('Connectivity & Growth', 15, 20),
    ]
    nb_score_data = [['Dimension', 'Score /20', 'Notes']]
    nb_notes = [
        'GIS, MKIS, Lycée Français, Sayfol on doorstep',
        'Low crime vs KL average; gated; some opportunistic theft on strips',
        '1MK, Plaza MK, Solaris, Publika, Taman Lembah Kiara nearby',
        '50%+ foreign residents; JP/KR/EU/Chinese community; corporate demand',
        'SPRINT km0; KLCC 15–20 min; no MRT; 37 new launches = supply pressure',
    ]
    for i, (lbl, sc, mx) in enumerate(nb_scores):
        nb_score_data.append([lbl, f'{sc}/{mx}', nb_notes[i]])
    nb_score_data.append(['TOTAL', '85/100', ''])
    story.append(make_table(nb_score_data, [W*0.30, W*0.14, W*0.52], compact=True))

    story.append(Spacer(1, 0.12*inch))
    str_con = Table([
        [
            [Paragraph('Top 3 Strengths', styles['h2'])] +
            [Paragraph(f'✓ {s}', styles['bullet']) for s in [
                'Expat ecosystem density — 50%+ foreign residents; self-reinforcing corporate/embassy demand',
                'International school cluster — GIS + MKIS + French School; hard-floors rental demand',
                'Highway superconnectivity — SPRINT km0; KLCC in 15–20 min by car',
            ]],
            [Paragraph('Top 3 Concerns', styles['h2'])] +
            [Paragraph(f'⚠ {s}', styles['bullet']) for s in [
                'No MRT/LRT — car-dependent; limits future buyer/tenant pool (younger demographic)',
                'Condo supply overhang — 37+ new launches; Damai competes as 2004-vintage stock',
                'Opportunistic snatch theft on Jalan Kiara/Jalan Solaris commercial strips',
            ]],
        ]
    ], colWidths=[W*0.50, W*0.50])
    str_con.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('LEFTPADDING', (0,0), (-1,-1), 0),
        ('RIGHTPADDING', (1,0), (1,0), 0),
    ]))
    story.append(str_con)

    story.append(Spacer(1, 0.1*inch))
    story.append(Paragraph('Key Amenities & Connectivity', styles['h2']))
    am_data = [
        ['Category', 'Details', 'Distance'],
        ['Shopping', '1 Mont Kiara, Plaza Mont Kiara, Solaris MK, Publika, Kiara 163', '2–5 min drive'],
        ['Parks', 'Taman Lembah Kiara (jogging, green space)', '5 min drive'],
        ['Medical', 'KPJ Damansara Hospital, Pantai Hospital', '10 min drive'],
        ['City Centre', 'KLCC / Bukit Bintang', '15–20 min via SPRINT'],
        ['Public Transit', 'Semantan MRT (Kajang Line)', '10 min drive'],
        ['Airport', 'KLIA', '~50 min via LDP/MEX'],
    ]
    story.append(make_table(am_data, [W*0.20, W*0.55, W*0.22], compact=True))
    story.append(PageBreak())

    # ── PAGE 7: INVESTMENT ANALYSIS ────────────────────────────────────────────
    story.append(section_header('INVESTMENT ANALYSIS', styles))
    story.append(Spacer(1, 0.08*inch))

    story.append(Paragraph('Acquisition Costs (Citizen Buyer)', styles['h2']))
    acq_data = [
        ['Item', 'Amount (RM)'],
        ['Purchase Price',                'RM 2,500,000'],
        ['Stamp Duty (MOT)',              'RM 84,000'],
        ['Loan Stamp Duty (0.5% of loan)','RM 8,750'],
        ['Legal Fees',                   'RM 12,500'],
        ['TOTAL ALL-IN',                 'RM 2,605,250'],
    ]
    acq_tbl = make_table(acq_data, [W*0.60, W*0.35])
    acq_tbl.setStyle(TableStyle([
        ('FONTNAME', (0, 5), (-1, 5), 'Helvetica-Bold'),
        ('BACKGROUND', (0, 5), (-1, 5), LIGHT_GRAY),
    ]))
    story.append(acq_tbl)

    story.append(Spacer(1, 0.1*inch))
    story.append(Paragraph('Strategy Comparison', styles['h2']))
    strat_data = [
        ['Metric',              'Buy & Hold', 'Renovate & Hold', 'Flip'],
        ['Feasibility Score',  '62/100',     '71/100',          '12/100'],
        ['Extra Investment',   '—',          'RM 150–170k',     'RM 150–170k'],
        ['Monthly Cash Flow',  '–RM 3,967',  '–RM 1,700',       'Not viable'],
        ['Hold Period',        '7–10 years', '7–10 years',      'N/A (loss)'],
        ['RPGT (citizen)',     '0% after 5yr','0% after 5yr',   '10–20% if <5yr'],
        ['Verdict',            'Viable',     'Recommended',     'Avoid'],
    ]
    strat_tbl = make_table(strat_data, [W*0.28, W*0.22, W*0.25, W*0.22])
    strat_tbl.setStyle(TableStyle([
        ('TEXTCOLOR', (3, 7), (3, 7), RED),
        ('TEXTCOLOR', (2, 7), (2, 7), GREEN),
        ('FONTNAME', (0, 7), (-1, 7), 'Helvetica-Bold'),
    ]))
    story.append(strat_tbl)

    story.append(Spacer(1, 0.1*inch))
    story.append(Paragraph('5-Year Capital Appreciation Projections', styles['h2']))
    proj_data = [
        ['Year', 'Value @ 3% p.a.', 'Value @ 5% p.a.', 'Equity Buildup (5yr loan)'],
        ['2026 (Now)', 'RM 2,500,000', 'RM 2,500,000', '—'],
        ['2027',       'RM 2,575,000', 'RM 2,625,000', 'RM 21,000'],
        ['2028',       'RM 2,652,000', 'RM 2,756,000', 'RM 43,000'],
        ['2029',       'RM 2,732,000', 'RM 2,894,000', 'RM 67,000'],
        ['2030',       'RM 2,814,000', 'RM 3,039,000', 'RM 93,000'],
        ['2031',       'RM 2,898,000', 'RM 3,191,000', 'RM 115,000'],
    ]
    story.append(make_table(proj_data, [W*0.18, W*0.24, W*0.24, W*0.30], compact=True))

    story.append(Spacer(1, 0.1*inch))
    story.append(Paragraph(
        'Total Net Profit (Buy & Hold, 5yr, 5% appreciation, RM 7k/mo rent): <b>~RM 438,000</b> '
        'after selling costs (3% agent + 1% legal). RPGT = 0% for citizens after Year 5.',
        styles['body']))

    story.append(Spacer(1, 0.08*inch))
    story.append(Paragraph('Renovation ROI (Renovate & Hold)', styles['h2']))
    reno_data = [
        ['Item', 'Amount'],
        ['Renovation Cost (mid-estimate)', 'RM 170,000'],
        ['Pre-reno Monthly Rent',          'RM 6,500'],
        ['Post-reno Monthly Rent',         'RM 8,500–9,000'],
        ['Annual Rent Uplift',             'RM 24,000+'],
        ['Reno Payback Period',            '7.1 years'],
        ['Monthly Shortfall Reduction',    'RM 4,000 → RM 1,700'],
    ]
    story.append(make_table(reno_data, [W*0.60, W*0.35], compact=True))
    story.append(PageBreak())

    # ── PAGE 8: MARKET CONDITIONS ──────────────────────────────────────────────
    story.append(section_header('MARKET CONDITIONS — MONT KIARA LUXURY CONDO MARKET', styles))
    story.append(Spacer(1, 0.08*inch))

    story.append(Paragraph('Market Classification: BALANCED — TILTING SELLER (sales side) / BUYERS\' MARKET (rentals)', styles['h2']))
    story.append(Spacer(1, 0.04*inch))

    mk_data = [
        ['Indicator', 'Data', 'Indicator', 'Data'],
        ['Active Listings (MK)', '3,700+',     'New Launch Pipeline', '37 projects'],
        ['Median PSF (2023)',    'RM 680–720',  'Median PSF (2026)',   'RM 808'],
        ['Annual PSF Growth',   '5–7%',        'Gross Rental Yield',  '4.0–5.5%'],
        ['DOM (well-priced)',    '~25 days',    'DOM (overpriced)',    '60+ days'],
        ['Malaysia GDP 2025',   '5.2%',        'BNM OPR',            '2.75%'],
        ['MYR (2025 change)',    '+10.2%',      'Foreign Buyer Min',  'RM 1,000,000'],
        ['Foreign Stamp Duty',  '4–8% (2026)', 'MM2H Buyers (pipeline)', '2,637'],
    ]
    story.append(make_table(mk_data, [W*0.25, W*0.23, W*0.27, W*0.23], compact=True))

    story.append(Spacer(1, 0.1*inch))
    story.append(Paragraph('Market Score Breakdown: 67/100', styles['h2']))
    mkt_score_data = [
        ['Dimension', 'Score /20', 'Notes'],
        ['Supply & Demand Balance',      '11', 'High inventory; 37 new launches = supply pressure'],
        ['Price Trend Strength',         '15', 'Clear +5–7% p.a. upward trajectory'],
        ['Economic Fundamentals',        '16', 'GDP 5.2%, OPR 2.75%, MYR strengthening'],
        ['Market Momentum',              '13', 'MM2H pipeline adds demand; capped by oversupply'],
        ['Investor/Buyer Favourability', '12', 'Good yields; new 8% foreign stamp duty a headwind'],
        ['TOTAL',                        '67', ''],
    ]
    story.append(make_table(mkt_score_data, [W*0.30, W*0.14, W*0.52], compact=True))

    story.append(Spacer(1, 0.1*inch))
    story.append(Paragraph('Market Outlook', styles['h2']))
    out_data = [
        ['Horizon', 'Outlook'],
        ['6-Month\n(Jun–Dec 2026)',
         'Prices hold/tick up 2–4%. Rental market stays competitive. '
         'MM2H pipeline (2,637 buyers in process) adds pulse of demand in H2. '
         'New foreign stamp duty (8%) already baking in buyer hesitation.'],
        ['12-Month\n(to Jun 2027)',
         '5–8% annual appreciation realistic for premium units. '
         'MM2H-driven demand + expat inflows + limited land supply support price floor. '
         'Rental recovery depends on absorption of new completions — expect 12–18 months '
         'of competition before market tightens. '
         'Best-positioned: branded, well-managed, school-proximate, large built-up, furnished, good views.'],
    ]
    story.append(make_table(out_data, [W*0.18, W*0.78]))
    story.append(PageBreak())

    # ── PAGE 9: RISK MATRIX + RECOMMENDATION ──────────────────────────────────
    story.append(section_header('RISK ASSESSMENT & RECOMMENDATION', styles))
    story.append(Spacer(1, 0.08*inch))

    story.append(Paragraph('Risk Matrix', styles['h2']))
    risk_data = [
        ['#', 'Risk', 'Severity', 'Likelihood', 'Mitigation'],
        ['1', 'Entry price above median (RM 893 vs RM 677 psf)', 'High', 'High',
         'Negotiate to RM 750–800 psf; walk at >RM 900 for standard units'],
        ['2', 'Negative leveraged cash flow (–RM 3k–5.5k/mo)', 'High', 'Certain',
         'Only proceed if cash-rich; or buy smaller/cheaper unit'],
        ['3', 'Building age (2004) — rising CapEx/maintenance', 'Medium', 'Medium',
         'Budget RM 170k reno; inspect M&E systems pre-purchase'],
        ['4', 'Supply overhang (37 new launches)', 'Medium', 'High',
         'Renovate + furnish; use expat relocation channels'],
        ['5', 'No MRT — car dependent', 'Low', 'Certain',
         'Currently not a dealbreaker for target expat tenant'],
        ['6', 'MYR appreciation reducing China buyer interest', 'Medium', 'Medium',
         'Broad expat base (JP/KR/EU) less MYR-sensitive'],
        ['7', 'New foreign stamp duty (8%)', 'Low', 'Certain',
         'Affects resale to foreigners; freehold partially mitigates'],
    ]
    risk_tbl = make_table(risk_data, [W*0.04, W*0.30, W*0.11, W*0.13, W*0.38], compact=True)
    risk_tbl.setStyle(TableStyle([
        ('TEXTCOLOR', (2, 1), (2, 2), RED),
        ('TEXTCOLOR', (2, 3), (2, 4), YELLOW),
        ('TEXTCOLOR', (2, 5), (2, 7), MED_GRAY),
        ('FONTNAME', (2, 1), (2, 2), 'Helvetica-Bold'),
    ]))
    story.append(risk_tbl)

    story.append(Spacer(1, 0.15*inch))
    story.append(HRFlowable(width=W, thickness=1.5, color=NAVY))
    story.append(Spacer(1, 0.1*inch))

    # Signal box
    signal_box = Table([[
        Paragraph('SIGNAL: WATCH / SELECTIVE BUY', ParagraphStyle(
            'sig', parent=styles['center'],
            fontName='Helvetica-Bold', fontSize=14, textColor=WHITE))
    ]], colWidths=[W])
    signal_box.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), YELLOW),
        ('TOPPADDING', (0,0), (-1,-1), 10),
        ('BOTTOMPADDING', (0,0), (-1,-1), 10),
    ]))
    story.append(signal_box)
    story.append(Spacer(1, 0.1*inch))

    story.append(Paragraph('<b>Proceed IF all of these are true:</b>', styles['body']))
    proceed = [
        'Entry price negotiated to RM 750–850 psf (RM 2.1M–2.4M for ~2,800 sqft)',
        'You can carry RM 2,000–4,000/month negative cash flow for 5–7 years without financial strain',
        'Plan to renovate (RM 150–170k budget) for full expat-grade rental potential',
        'Holding horizon is 7–10 years minimum (RPGT-free after Year 5 for citizens)',
    ]
    for p in proceed:
        story.append(Paragraph(f'✓ {p}', styles['bullet']))

    story.append(Spacer(1, 0.08*inch))
    story.append(Paragraph('<b>Pass IF:</b>', styles['body']))
    pass_cond = [
        'Seller won\'t move below RM 900 psf on a standard unit',
        'You need positive monthly cash flow from Day 1',
        'Your investment horizon is under 5 years',
        'You\'re considering this as a flip (net loss under any scenario)',
    ]
    for p in pass_cond:
        story.append(Paragraph(f'✗ {p}', ParagraphStyle('pass', parent=styles['bullet'], textColor=RED)))

    story.append(Spacer(1, 0.1*inch))
    story.append(Paragraph('<b>Suggested Offer Price: RM 2.0M–2.2M</b> (RM 714–786 psf for a standard ~2,800 sqft unit)', styles['body']))
    story.append(Paragraph(
        'This range sits between the subject\'s own historical median (RM 677 psf) and the suburb-wide median '
        '(RM 808 psf). At this entry, net yield improves to ~2.4–2.7% and monthly shortfall drops to ~RM 2,500–3,500.',
        styles['body']))

    story.append(Spacer(1, 0.08*inch))
    story.append(Paragraph('<b>Key Contingencies:</b>', styles['body']))
    contingencies = [
        'Full building inspection — structural + M&E systems (lift, plumbing, electrical)',
        'Sinking fund balance check — confirm no underfunded reserves or outstanding special levies',
        'Confirm no outstanding maintenance arrears on the specific unit',
        'Engage a licensed valuer for formal valuation before committing',
    ]
    for c in contingencies:
        story.append(Paragraph(f'• {c}', styles['bullet']))

    story.append(Spacer(1, 0.08*inch))
    story.append(Paragraph('<b>Next Steps:</b>', styles['body']))
    nexts = [
        'Visit the unit — check floor level, view, and renovation scope in person',
        'Get 3 rental agent opinions on realistic effective rent (not just advertised)',
        'Request management company sinking fund and account statements',
        'Negotiate to RM 2.0M–2.2M — or walk',
        'If proceeding: appoint contractor to scope reno cost before signing SPA',
    ]
    for n in nexts:
        story.append(Paragraph(f'→ {n}', styles['bullet']))

    story.append(Spacer(1, 0.15*inch))
    story.append(HRFlowable(width=W, thickness=0.5, color=BORDER))
    story.append(Spacer(1, 0.08*inch))
    story.append(Paragraph(DISCLAIMER, styles['disclaimer']))
    story.append(Paragraph(
        'Report generated by AI Real Estate Analyst · 8 June 2026 · '
        'Data sourced from brickz.my, iProperty.com.my, PropertyGuru, EdgeProp.my, '
        'Global Property Guide, BNM, World Bank, MM2H Programme records.',
        styles['disclaimer']))

    # ── BUILD ──────────────────────────────────────────────────────────────────
    doc.build(story, onFirstPage=add_footer, onLaterPages=add_footer)
    print(f'PDF saved: {output}')


if __name__ == '__main__':
    build_pdf()
