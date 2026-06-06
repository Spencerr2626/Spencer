---
name: listing-proposal
description: >-
  Generate a branded Kommons Realty "Property Showing Route" proposal deck (PDF)
  from property details + photos. Use when Spencer says "make a listing
  proposal", "build a showing route", "create a proposal deck", or sends a
  property's specs + photos to turn into a client-facing PDF. Reproduces the
  exact house style: cover → [detail page + photos page] per property → back
  cover.
---

# Listing Proposal Deck

Builds Spencer's signature **Property Showing Route** proposal — a polished 16:9
landscape PDF in Kommons Realty house style. One deck can hold any number of
properties (e.g. a multi-stop viewing route).

## When to use

Spencer sends a property (or several) — name, unit, specs, asking price, photos,
optionally a floor plan — and wants the client-facing proposal PDF.

## Deck structure (auto-generated)

1. **Cover** — Spencer's photo + "PROPOSAL / Property Showing Route" + name block + logo.
2. **Per property** (repeats):
   - **Detail page** — spec table, icon strip, gold asking-price bar, floor plan.
   - **Photos page** — 2×3 grid (up to 6), each with a captioned dark strip.
3. **Back cover** — full contact card, QR codes (WhatsApp + WeChat), registration seal, logo.

## How to run

The generator needs `fpdf2` + `Pillow`. The system Python has a broken `cffi`,
so **use a venv**:

```bash
python3 -m venv /tmp/lpvenv
/tmp/lpvenv/bin/pip install -q fpdf2 Pillow
/tmp/lpvenv/bin/python .claude/skills/listing-proposal/generate.py <spec.json> <output.pdf>
```

Render to images to eyeball it before sending:
`pdftoppm -png -r 90 output.pdf /tmp/preview/p` (needs `poppler-utils`).

## Workflow

1. **Collect** per property: name, unit, location, listing type (For Sale / For
   Rent), the 8 spec rows, the 5 icon-strip items, asking price, and the photos
   (+ captions). Floor plan is optional.
2. **Photos must be real files** — if Spencer pastes images inline, ask him to
   send them as **file attachments** so they can be embedded. Save them under a
   working folder and reference by path in the spec.
3. **Write a `spec.json`** (copy `example/spec.json` and edit). Paths resolve
   relative to the spec file.
4. **Generate**, render a preview, sanity-check, then deliver the PDF with
   `SendUserFile`.
5. **Don't invent specs.** Missing built-up / floor plan / photo caption → ask,
   per CRM rules. Mont Kiara in Chinese = **满家乐** (for Chinese-language decks).

## spec.json schema

```jsonc
{
  "deck": { "title": "PROPOSAL", "subtitle": "Property Showing Route" },
  "agent": { /* optional overrides; defaults = Spencer in brand.py */ },
  "properties": [{
    "name": "Residensi Astrea",
    "unit": "Unit 12-07",
    "location": "Mont Kiara, Kuala Lumpur",
    "area": "Mont Kiara",
    "listing_type": "For Rent",                 // For Rent | For Sale
    "specs": { "Built-Up": "1,656 Sq Ft", "Bedrooms": "3 + 1 Bedrooms", "...": "..." },
    "icons": ["3+1", "3", "2", "1,656sf", "Furnished"],
    "price_label": "ASKING RENTAL",             // or ASKING PRICE
    "price": "RM 7,500 / month",
    "price_summary": "RM 7,500/mo  |  1,656 sqft  |  3+1 Bed  |  Fully Furnished",
    "floor_plan_caption": "Floor Plan — Type B (1,656 sqft)",
    "floor_plan": "floorplans/astrea.png",      // optional
    "photos": [ { "caption": "Living & Dining Room", "file": "photos/astrea/living.jpg" } ]
  }]
}
```

## Files

- `generate.py` — the builder (`python generate.py spec.json out.pdf`).
- `brand.py` — colours, fonts, asset paths, default agent block.
- `assets/` — logo, Spencer's cover/back photos, QR codes, seal, bundled fonts.
- `example/` — a working `spec.json` reproducing the original 2-property deck.

## Notes

- Canvas is `1440×810 pt` (16:9). Fonts: Liberation Sans/Serif (bundled,
  Arial/Times-compatible) with a system CJK fallback for Chinese text.
- Brand palette: black `#2D2D2D`, gold `#F5C518`, row gray `#F2F2F2`,
  icon strip `#FFF9D6`.
