"""
Brand constants and asset paths for Spencer Leong's Kommons Realty
listing-proposal deck. Single source of truth for colours, fonts and
the default agent / company details.
"""
import os

SKILL_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(SKILL_DIR, "assets")

# --- Brand palette (sampled from the original deck) ---
BLACK = (45, 45, 45)        # #2D2D2D  header / footer bars
GOLD = (245, 197, 24)       # #F5C518  asking-price bar, accent text
LIGHT_YELLOW = (255, 249, 214)  # #FFF9D6  icon strip background
ROW_GRAY = (242, 242, 242)  # #F2F2F2  alternating table row
WHITE = (255, 255, 255)
DARK_TEXT = (38, 38, 38)
GRAY_TEXT = (110, 110, 110)
MAROON = (138, 30, 30)      # Kommons mark colour (for accents if needed)

# --- Brand assets ---
FONTS = os.path.join(ASSETS, "fonts")
# Liberation Sans/Serif are metric-compatible with Arial/Times — bundled so
# decks render identically in any session. SANS ≈ the deck's body font.
FONT_SANS = os.path.join(FONTS, "LiberationSans-Regular.ttf")
FONT_SANS_B = os.path.join(FONTS, "LiberationSans-Bold.ttf")
FONT_SERIF = os.path.join(FONTS, "LiberationSerif-Regular.ttf")
FONT_SERIF_B = os.path.join(FONTS, "LiberationSerif-Bold.ttf")

# Best-effort CJK fallback for Chinese captions/names. Bundled if present,
# otherwise discovered from common system locations at runtime.
CJK_CANDIDATES = [
    os.path.join(FONTS, "wqy-zenhei.ttc"),
    "/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc",
    "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
    "/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc",
    "/System/Library/Fonts/PingFang.ttc",
]


def find_cjk():
    for p in CJK_CANDIDATES:
        if os.path.exists(p):
            return p
    return None


LOGO = os.path.join(ASSETS, "kommons-logo.png")
SEAL = os.path.join(ASSETS, "ejen-hartanah-seal.png")
COVER_PHOTO = os.path.join(ASSETS, "spencer-cover.jpg")
BACKCOVER_PHOTO = os.path.join(ASSETS, "spencer-backcover.jpg")
QR_WECHAT = os.path.join(ASSETS, "qr-wechat.png")
QR_WHATSAPP = os.path.join(ASSETS, "qr-whatsapp.png")

# --- Default agent / company block ---
DEFAULT_AGENT = {
    "name": "Spencer Leong",
    "title": "Senior Property Consultant",
    "ren": "REN 72821",
    "phone": "+6016 814 2626",
    "email": "spencer@kommonsrealty.com",
    "company": "Kommons Realty Sdn Bhd",
    "company_reg": "201801027637",
    "address": [
        "J-2-7, No 2 Jalan Solaris",
        "Solaris Mont Kiara, 50480",
        "Kuala Lumpur, Malaysia",
    ],
    "tel": "+603 6413 0178",
    "fax": "+603 6413 0188",
}
