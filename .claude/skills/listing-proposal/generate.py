#!/usr/bin/env python3
"""
Listing Proposal deck generator — Kommons Realty / Spencer Leong house style.

Reproduces the 6-page (and scalable) "Property Showing Route" proposal:
  cover  →  [detail page + photos page] per property  →  back cover

Usage:
    python generate.py spec.json [output.pdf]

`spec.json` schema — see example/spec.json. Paths inside the spec
(floor_plan, photo files) are resolved relative to the spec file's folder
unless absolute. Requires: fpdf2, Pillow.
"""
import json
import os
import sys
import tempfile

from fpdf import FPDF
from PIL import Image

import brand

# 16:9 landscape canvas, in points (matches the source deck 1440 x 810).
PW, PH = 1440.0, 810.0


def _f(parent, path):
    """Resolve a spec-relative path."""
    if not path:
        return None
    return path if os.path.isabs(path) else os.path.normpath(os.path.join(parent, path))


def cover_fit(src, w_pt, h_pt, tmpdir, dpi=2.0):
    """Crop+scale an image to exactly fill a w_pt x h_pt box (object-fit:cover)."""
    im = Image.open(src).convert("RGB")
    tw, th = max(1, int(w_pt * dpi)), max(1, int(h_pt * dpi))
    sw, sh = im.size
    scale = max(tw / sw, th / sh)
    nw, nh = int(sw * scale), int(sh * scale)
    im = im.resize((nw, nh), Image.LANCZOS)
    left, top = (nw - tw) // 2, (nh - th) // 2
    im = im.crop((left, top, left + tw, top + th))
    fd, out = tempfile.mkstemp(suffix=".jpg", dir=tmpdir)
    os.close(fd)
    im.save(out, quality=90)
    return out


def contain_box(src, max_w, max_h):
    """Return (w,h) that fits src inside max box preserving aspect ratio."""
    im = Image.open(src)
    sw, sh = im.size
    scale = min(max_w / sw, max_h / sh)
    return sw * scale, sh * scale


class Deck(FPDF):
    def __init__(self, agent, tmpdir):
        # format=(1440,810) with orientation "P" yields the 16:9 landscape
        # canvas; fpdf2's "L" would swap W/H and give portrait here.
        super().__init__(orientation="P", unit="pt", format=(PW, PH))
        self.agent = agent
        self.tmpdir = tmpdir
        self.set_auto_page_break(False)
        self.set_margins(0, 0, 0)
        self._register_fonts()

    def _register_fonts(self):
        # "sans" (Arial-like) and "serif" (Times-like), both Unicode-capable.
        self.add_font("sans", "", brand.FONT_SANS)
        self.add_font("sans", "B", brand.FONT_SANS_B)
        self.add_font("serif", "", brand.FONT_SERIF)
        self.add_font("serif", "B", brand.FONT_SERIF_B)
        cjk = brand.find_cjk()
        self.has_cjk = bool(cjk)
        if cjk:
            # .ttc collections: index 0 is the main face.
            for style in ("", "B"):
                self.add_font("cjk", style, cjk)
            # Auto-fallback to CJK when a glyph is missing in sans/serif.
            self.set_fallback_fonts(["cjk"])

    # ---- low-level helpers ----
    def box(self, x, y, w, h, color):
        self.set_fill_color(*color)
        super().rect(x, y, w, h, style="F")

    def txt(self, x, y, s, size, color, style="", align="L", font="sans", w=None):
        self.set_font(font, style, size)
        self.set_text_color(*color)
        if align == "L":
            self.set_xy(x, y)
            self.cell(self.get_string_width(s) + 2, size * 1.2, s)
        else:
            cw = w if w is not None else (PW - x)
            self.set_xy(x, y)
            self.cell(cw, size * 1.2, s, align=align)

    # ---- shared chrome ----
    def header_bar(self, left_text, right_text):
        self.box(0, 0, PW, 46, brand.BLACK)
        # yellow square bullet
        self.box(28, 17, 13, 13, brand.GOLD)
        self.txt(50, 14, left_text, 15, brand.GOLD, style="B")
        self.txt(0, 15, right_text, 12, brand.WHITE, align="R", w=PW - 30)

    def footer_bar(self):
        a = self.agent
        self.box(0, PH - 40, PW, 40, brand.BLACK)
        left = f"{a['name']}  |  {a['title']} ({a['ren']})"
        right = f"{a['phone']}  |  {a['email']}  |  {a['company']}"
        self.txt(30, PH - 28, left, 12, brand.GOLD, style="B")
        self.txt(0, PH - 27, right, 11, brand.WHITE, align="R", w=PW - 30)

    def place_logo(self, x, y, w):
        ar = Image.open(brand.LOGO)
        h = w * ar.size[1] / ar.size[0]
        self.image(brand.LOGO, x, y, w, h)
        return h

    # ===================== PAGES =====================
    def cover(self, deck):
        self.add_page()
        # left photo panel (full bleed ~40%)
        pw = PW * 0.40
        img = cover_fit(brand.COVER_PHOTO, pw, PH, self.tmpdir)
        self.image(img, 0, 0, pw, PH)
        # right content
        cx = pw + 70
        self.set_draw_color(*brand.DARK_TEXT)
        # "PROPOSAL" outline
        title = deck.get("title", "PROPOSAL")
        self.set_font("sans", "B", 70)
        try:
            with self.local_context(text_mode="STROKE", line_width=1.4):
                self.set_draw_color(70, 70, 70)
                self.set_xy(cx, 120)
                self.cell(self.get_string_width(title) + 4, 80, title)
        except Exception:
            self.txt(cx, 120, title, 70, (120, 120, 120), style="B")
        self.txt(cx + 4, 215, deck.get("subtitle", "Property Showing Route"),
                 20, brand.DARK_TEXT, style="B")
        # agent block
        self.txt(cx + 4, 300, self.agent["name"], 34, brand.DARK_TEXT,
                 style="B", font="serif")
        self.txt(cx + 4, 350, self.agent["title"], 19, (80, 80, 80))
        self.txt(cx + 4, 382, f"({self.agent['ren']})", 13, brand.GRAY_TEXT)
        self.place_logo(cx + 4, 450, 230)

    def detail_page(self, p):
        self.add_page()
        ltype = p.get("listing_type", "For Sale")
        area = p.get("area", "Mont Kiara")
        self.header_bar(f"{p['name']}, {area}  —  {ltype}",
                        f"{self.agent['company'].replace(' Sdn Bhd','')} | "
                        f"{self.agent['name']}  {self.agent['phone']}")
        # title + subtitle
        self.txt(40, 70, p["name"], 38, brand.DARK_TEXT, style="B")
        parts = [s for s in (p.get("unit", "").strip(), p.get("location", "").strip()) if s]
        self.txt(42, 128, "  •  ".join(parts), 15, brand.GRAY_TEXT)
        self.box(42, 152, 150, 3, brand.GOLD)  # yellow underline accent

        # ---- spec table (left half) ----
        tx, tw = 40, 600
        ty, rh = 175, 38
        specs = list(p.get("specs", {}).items())
        for i, (k, v) in enumerate(specs):
            if i % 2 == 0:
                self.box(tx, ty + i * rh, tw, rh, brand.ROW_GRAY)
            self.txt(tx + 14, ty + i * rh + 11, k, 13, brand.DARK_TEXT, style="B")
            self.txt(tx + 175, ty + i * rh + 11, str(v), 13, (70, 70, 70))
        tbot = ty + len(specs) * rh

        # ---- icon strip ----
        icons = p.get("icons", [])
        iy = tbot + 10
        self.box(tx, iy, tw, 34, brand.LIGHT_YELLOW)
        ix = tx + 14
        for ic in icons:
            self.box(ix, iy + 12, 10, 10, brand.BLACK)
            self.txt(ix + 16, iy + 9, str(ic), 12, brand.DARK_TEXT, style="B")
            ix += 24 + self.get_string_width(str(ic)) + 40

        # ---- asking price bar ----
        ay = iy + 50
        self.box(tx, ay, tw, 50, brand.GOLD)
        self.txt(tx + 16, ay + 8, p.get("price_label", "ASKING PRICE"),
                 12, brand.DARK_TEXT, style="B")
        self.txt(tx + 175, ay + 9, p.get("price", ""), 26, brand.DARK_TEXT, style="B")

        # ---- floor plan (right half) ----
        fp = p.get("_floor_plan_abs")
        rx, rtop, rw, rh2 = 720, 175, 660, 420
        if fp and os.path.exists(fp):
            cap = p.get("floor_plan_caption", "Floor Plan")
            self.txt(rx, 138, cap, 14, brand.DARK_TEXT, style="B", align="C", w=rw)
            w, h = contain_box(fp, rw - 40, rh2)
            self.image(fp, rx + (rw - w) / 2, rtop + (rh2 - h) / 2, w, h)
        self.footer_bar()

    def photos_page(self, p):
        self.add_page()
        area = p.get("area", "Mont Kiara")
        summary = p.get("photo_summary") or p.get("price_summary", "")
        self.header_bar(f"{p['name']}, {area}  —  Property Photos", summary)
        photos = p.get("_photos_abs", [])[:6]
        # 2 x 3 grid in the body
        gx, gy = 18, 56
        gw, gh = PW - 36, PH - 56 - 44
        gutter = 10
        cols, rows = 3, 2
        cw = (gw - gutter * (cols - 1)) / cols
        ch = (gh - gutter * (rows - 1)) / rows
        cap_h = 22
        for idx in range(6):
            r, c = divmod(idx, cols)
            x = gx + c * (cw + gutter)
            y = gy + r * (ch + gutter)
            if idx < len(photos):
                ph = photos[idx]
                abs_p = ph.get("_abs")
                if abs_p and os.path.exists(abs_p):
                    img = cover_fit(abs_p, cw, ch - cap_h, self.tmpdir)
                    self.image(img, x, y, cw, ch - cap_h)
                else:
                    # missing file → labelled placeholder (preview / await photo)
                    self.box(x, y, cw, ch - cap_h, (224, 224, 224))
                    self.txt(x, y + (ch - cap_h) / 2 - 8, "[ photo ]", 13,
                             (150, 150, 150), align="C", w=cw)
                # caption strip
                self.box(x, y + ch - cap_h, cw, cap_h, brand.BLACK)
                self.txt(x, y + ch - cap_h + 5, ph.get("caption", ""),
                         11, brand.GOLD, style="B", align="C", w=cw)
            else:
                self.box(x, y, cw, ch, brand.ROW_GRAY)
        self.footer_bar()

    def back_cover(self):
        self.add_page()
        a = self.agent
        pw = PW * 0.38
        img = cover_fit(brand.BACKCOVER_PHOTO, pw, PH, self.tmpdir)
        self.image(img, 0, 0, pw, PH)
        cx = pw + 60
        self.txt(cx, 70, a["name"], 32, brand.DARK_TEXT, style="B", font="serif")
        self.txt(cx + 2, 118, a["title"], 17, brand.DARK_TEXT, style="B")
        self.txt(cx + 2, 144, f"({a['ren']})", 12, brand.GRAY_TEXT)
        self.txt(cx + 2, 185, a["phone"], 21, brand.DARK_TEXT, style="B")
        self.txt(cx + 2, 218, a["email"], 14, (70, 70, 70))
        # company block
        by = 270
        self.txt(cx + 2, by, a["company"], 14, brand.DARK_TEXT, style="B")
        self.txt(cx + 2, by + 22, a["company_reg"], 11, brand.GRAY_TEXT)
        yy = by + 44
        for line in a["address"]:
            self.txt(cx + 2, yy, line, 12, (70, 70, 70))
            yy += 19
        self.txt(cx + 2, yy + 2, f"T {a['tel']}", 12, (70, 70, 70))
        self.txt(cx + 2, yy + 21, f"F {a['fax']}", 12, (70, 70, 70))
        # seal + registered text
        seal_w = 80
        sar = Image.open(brand.SEAL)
        sh = seal_w * sar.size[1] / sar.size[0]
        self.image(brand.SEAL, cx + 2, yy + 50, seal_w, sh)
        self.txt(cx + 2, yy + 52 + sh, "Registered Real Estate Agent",
                 11, brand.DARK_TEXT, style="B")
        # QR codes (right column)
        qx = PW - 250
        self.image(brand.QR_WHATSAPP, qx, 70, 110, 110)
        self.image(brand.QR_WECHAT, qx, 200, 110, 110)
        # logo bottom-right
        self.place_logo(PW - 230, PH - 110, 180)


def build(spec_path, out_path):
    base = os.path.dirname(os.path.abspath(spec_path))
    with open(spec_path, encoding="utf-8") as fh:
        spec = json.load(fh)

    agent = {**brand.DEFAULT_AGENT, **spec.get("agent", {})}
    deck_meta = spec.get("deck", {})

    with tempfile.TemporaryDirectory() as tmpdir:
        # resolve asset paths
        for p in spec.get("properties", []):
            p["_floor_plan_abs"] = _f(base, p.get("floor_plan"))
            abs_photos = []
            for ph in p.get("photos", []):
                ph = dict(ph)
                ph["_abs"] = _f(base, ph.get("file"))
                abs_photos.append(ph)
            p["_photos_abs"] = abs_photos

        pdf = Deck(agent, tmpdir)
        pdf.cover(deck_meta)
        for p in spec.get("properties", []):
            pdf.detail_page(p)
            pdf.photos_page(p)
        pdf.back_cover()
        pdf.output(out_path)
    print(f"✓ Wrote {out_path}  ({len(spec.get('properties', []))} properties)")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    spec = sys.argv[1]
    out = sys.argv[2] if len(sys.argv) > 2 else "Listing_Proposal.pdf"
    build(spec, out)
