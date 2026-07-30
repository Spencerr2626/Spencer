#!/usr/bin/env python3
"""Generate Spencer's one-page business progress report (PDF) from the live CRM.

Reads references/crm/Spencer_Kommons_CRM_v3.xlsx (Dashboard + Pipeline sheets),
classifies pipeline deals, computes the projection, and renders a branded
one-page A4 PDF into reports/.

Usage:  python generate.py [YYYY-MM-DD]   (defaults to today)
Deps:   openpyxl, reportlab   (system CJK font wqy-zenhei used if present)
"""
import sys, os, datetime, re
import openpyxl
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (BaseDocTemplate, PageTemplate, Frame, Paragraph,
                                Spacer, Table, TableStyle)
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_RIGHT, TA_CENTER

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
CRM  = os.path.join(ROOT, "references", "crm", "Spencer_Kommons_CRM_v3.xlsx")
OUTDIR = os.path.join(ROOT, "reports")

# ---- date ----
if len(sys.argv) > 1:
    run = datetime.date.fromisoformat(sys.argv[1])
else:
    # date passed in avoids sandbox clock issues; fall back to file mtime day
    run = datetime.date.today()

# ---- CJK font (graceful fallback) ----
CJK = "Helvetica"
for p in ("/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc",
          "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"):
    if os.path.exists(p):
        try:
            pdfmetrics.registerFont(TTFont("CJK", p, subfontIndex=0)); CJK = "CJK"; break
        except Exception:
            pass

def cjk(s):
    """Wrap any CJK runs in the CJK font so they render."""
    if CJK == "Helvetica":
        return s
    return re.sub(r"([　-鿿＀-￯]+)", r'<font name="CJK">\1</font>', s)

# ---- read CRM ----
wb = openpyxl.load_workbook(CRM, data_only=True)
dash = wb["\U0001F4CA Dashboard"]
def dcell(ref):
    v = dash[ref].value
    return "" if v is None else str(v)
gci   = dcell("J5")           # GCI YTD (realized)
active= dcell("D5")
done  = dcell("G5")
pval  = dcell("D9")
ecomm = dcell("G9")

pl = wb["\U0001F4B0 Pipeline & Deals"]
deals = []
for r in pl.iter_rows(min_row=2):
    did = r[0].value
    if not (isinstance(did, str) and re.match(r"D\d+", did)):
        continue
    client = r[1].value or ""
    prop   = r[3].value or ""
    price  = r[7].value
    commp  = r[8].value
    est    = r[9].value
    stage  = str(r[6].value or "")
    if isinstance(est, str) or est is None:
        est = (price or 0) * (commp or 0) if price and commp else 0
    deals.append(dict(client=str(client), prop=str(prop), price=price or 0,
                      est=est or 0, stage=stage))

def classify(s):
    u = s.upper()
    if any(k in u for k in ("DONE", "SOLD", "✅")):
        return "done"
    if any(k in u for k in ("SPA", "ATP", "STAMPED", "SIGNED", "EARNEST", "OFFER LETTER")):
        return "signed"
    return "early"

signed = [d for d in deals if classify(d["stage"]) == "signed" and d["est"]]
early  = [d for d in deals if classify(d["stage"]) == "early"]
signed_total = sum(d["est"] for d in signed)

def money(n):
    return "RM " + f"{int(round(n)):,}"
def mn(price):
    try: return f"RM {price/1e6:.2f}m"
    except Exception: return str(price)

# projected = realized GCI + signed pipeline
gci_num = int(re.sub(r"[^\d]", "", gci) or 0)
projected = gci_num + signed_total

# ---- render ----
NAVY=colors.HexColor('#12263A'); GOLD=colors.HexColor('#B8912F')
GREEN=colors.HexColor('#1E7A4D'); INK=colors.HexColor('#22303C')
GREY=colors.HexColor('#6A7683'); LGREY=colors.HexColor('#EEF1F4'); LINE=colors.HexColor('#D8DEE4')
W,H=A4
os.makedirs(OUTDIR, exist_ok=True)
out=os.path.join(OUTDIR, f"Spencer_Progress_Report_{run:%Y-%m-%d}.pdf")

def hdr(c,doc):
    c.saveState()
    c.setFillColor(NAVY); c.rect(0,H-34*mm,W,34*mm,fill=1,stroke=0)
    c.setFillColor(GOLD); c.rect(0,H-34*mm,W,1.6*mm,fill=1,stroke=0)
    c.setFillColor(colors.white); c.setFont('Helvetica-Bold',18)
    c.drawString(18*mm,H-16*mm,"SPENCER LEONG")
    c.setFillColor(GOLD); c.setFont('Helvetica',9.5)
    c.drawString(18*mm,H-21.5*mm,"Kommons Realty Sdn Bhd  ·  REN 72821")
    c.setFillColor(colors.white); c.setFont('Helvetica-Bold',11)
    c.drawRightString(W-18*mm,H-15*mm,"BUSINESS PROGRESS REPORT")
    c.setFillColor(colors.HexColor('#AEB9C4')); c.setFont('Helvetica',9)
    c.drawRightString(W-18*mm,H-20.5*mm,f"As of {run:%d %B %Y}")
    c.setFillColor(GREY); c.setFont('Helvetica-Oblique',7.5)
    c.drawCentredString(W/2,10*mm,"Confidential  ·  Generated for Spencer Leong  ·  Kommons Realty Sdn Bhd")
    c.restoreState()

def P(t,f='Helvetica',s=9,c=INK,lead=None,align=TA_LEFT,sa=0):
    return Paragraph(t,ParagraphStyle('x',fontName=f,fontSize=s,textColor=c,
        leading=lead or s*1.25,alignment=align,spaceAfter=sa))
def sect(t):
    return Paragraph(t,ParagraphStyle('s',fontName='Helvetica-Bold',fontSize=10,
        textColor=NAVY,spaceBefore=6,spaceAfter=3,leading=12))

story=[Spacer(1,6*mm)]
hero=Table([[P("GCI REALIZED (YTD)",'Helvetica-Bold',8.5,colors.HexColor('#CBB26A')),
  P("SIGNED &amp; ADVANCED",'Helvetica-Bold',8.5,colors.HexColor('#CBB26A')),
  P("PROJECTED IF CLOSED",'Helvetica-Bold',8.5,colors.HexColor('#CBB26A'))],
 [P(gci or money(gci_num),'Helvetica-Bold',20,colors.white),
  P("+ "+money(signed_total),'Helvetica-Bold',20,colors.white),
  P("~ "+money(projected),'Helvetica-Bold',20,colors.HexColor('#7FE3AD'))]],
  colWidths=[58*mm,58*mm,58*mm])
hero.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1),NAVY),('TOPPADDING',(0,0),(-1,0),8),
  ('BOTTOMPADDING',(0,1),(-1,1),9),('TOPPADDING',(0,1),(-1,1),0),('LEFTPADDING',(0,0),(-1,-1),10),
  ('LINEAFTER',(0,0),(1,-1),0.6,colors.HexColor('#2E4258'))]))
story+=[hero,Spacer(1,3*mm),sect("UNDER CONTRACT / NEAR-CLOSE")]

def c_(t,f='Helvetica',s=8.5,col=INK,al=TA_LEFT): return P(cjk(t),f,s,col,align=al)
rows=[[c_("Client",'Helvetica-Bold',8,colors.white),c_("Property",'Helvetica-Bold',8,colors.white),
  c_("Value",'Helvetica-Bold',8,colors.white,TA_RIGHT),c_("Your Comm.",'Helvetica-Bold',8,colors.white,TA_RIGHT),
  c_("Status",'Helvetica-Bold',8,colors.white)]]
for d in sorted(signed,key=lambda x:-x["est"]):
    rows.append([c_(d["client"]),c_(d["prop"]),c_(mn(d["price"]),al=TA_RIGHT),
        c_(money(d["est"]),'Helvetica-Bold',8.5,GREEN,TA_RIGHT),c_(d["stage"][:46])])
rows.append([c_(""),c_("TOTAL SIGNED / ADVANCED",'Helvetica-Bold',8.5,NAVY),c_(""),
    c_(money(signed_total),'Helvetica-Bold',9.5,NAVY,TA_RIGHT),c_("")])
t=Table(rows,colWidths=[26*mm,42*mm,20*mm,26*mm,60*mm])
n=len(rows)
t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),NAVY),('ROWBACKGROUNDS',(0,1),(-1,n-2),[colors.white,LGREY]),
  ('BACKGROUND',(0,n-1),(-1,n-1),colors.HexColor('#E7ECF1')),('LINEBELOW',(0,0),(-1,0),0.4,NAVY),
  ('VALIGN',(0,0),(-1,-1),'MIDDLE'),('TOPPADDING',(0,0),(-1,-1),4.5),('BOTTOMPADDING',(0,0),(-1,-1),4.5),
  ('LEFTPADDING',(0,0),(-1,-1),6),('RIGHTPADDING',(0,0),(-1,-1),6),('LINEABOVE',(0,n-1),(-1,n-1),0.5,NAVY)]))
story+=[t,Spacer(1,3.5*mm)]

def bl(items): return [P(cjk("• "+i),'Helvetica',8.5,INK,lead=12,sa=1.5) for i in items]
early_items=[f'{d["client"]}, {mn(d["price"])}, {d["stage"][:34]}' for d in early] or ["(none in early stage)"]
left=[sect("EARLY PIPELINE")]+bl(early_items)
right=[sect("SNAPSHOT")]+bl([
  f'Active leads: {active}', f'Done deals: {done}',
  f'Pipeline value: {pval}', f'Est. commission (all live): {ecomm}',
  f'Signed / advanced deals: {len(signed)}'])
cols=Table([[left,right]],colWidths=[100*mm,74*mm])
cols.setStyle(TableStyle([('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(0,0),0),
  ('LEFTPADDING',(1,0),(1,0),8),('RIGHTPADDING',(0,0),(-1,-1),4)]))
story+=[cols,Spacer(1,3*mm)]

mom=Table([[P(f"<b>MOMENTUM:</b>  {money(gci_num)} realized, plus {money(signed_total)} in signed / advanced deals "
   f"now working through loans and paperwork. Land those and you reach ~{money(projected)}. "
   "Focus: RM500k GCI &amp; build the team.",'Helvetica',8.7,INK,lead=12)]],colWidths=[174*mm])
mom.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1),colors.HexColor('#FBF6E9')),('BOX',(0,0),(-1,-1),0.6,GOLD),
  ('LEFTPADDING',(0,0),(-1,-1),8),('RIGHTPADDING',(0,0),(-1,-1),8),('TOPPADDING',(0,0),(-1,-1),6),('BOTTOMPADDING',(0,0),(-1,-1),6)]))
story+=[mom]

doc=BaseDocTemplate(out,pagesize=A4,leftMargin=18*mm,rightMargin=18*mm,topMargin=40*mm,bottomMargin=14*mm)
doc.addPageTemplates([PageTemplate(id='p',frames=[Frame(18*mm,14*mm,W-36*mm,H-54*mm,id='f',
                     leftPadding=0,rightPadding=0,topPadding=0,bottomPadding=0)],onPage=hdr)])
doc.build(story)
print(out)
