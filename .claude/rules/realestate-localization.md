# Real Estate Skill Localization (Malaysia)

**Standing instruction:** Every real-estate skill Spencer pastes — and every existing one — must default to the **Malaysian market**. When saving or editing any skill, localize it before committing. No need to ask.

## Localize these automatically

| Dimension | Default to |
|-----------|-----------|
| Currency | **RM** (never `$`); thousands separators |
| Area / pricing | **sq ft**, **RM psf** (built-up + land area for landed) |
| Tenure | **Freehold / Leasehold** (state years remaining) — first-class field |
| Data sources | **PropertyGuru, iProperty, EdgeProp, brickz.my (transacted), StarProperty, NAPIC/JPPH, Bank Negara Malaysia (BNM)** — prefer transacted over asking |
| Markets | Klang Valley / KL default: **Mont Kiara, KLCC, Damansara Heights, Desa ParkCity, Sri Hartamas, Bangsar**; adapt to other MY locations as given |
| Taxes | **RPGT** (citizens: 30/20/30/20% Yr1-3, 15% Yr4, 10% Yr5, **0% from Yr6**; higher for foreigners/companies), **MOT stamp duty** (1/2/3/4% progressive, +4-8% foreign surcharge 2026), **loan stamp duty 0.5%**, **Cukai Pintu** (assessment) + **Cukai Tanah** (quit rent), **6% SST on commercial rent** |
| Foreign buyers | **RM 1,000,000 minimum** purchase (KL), **MM2H** tiers/eligibility, foreign stamp-duty surcharge |
| Yields | **Gross & Net rental yield** for residential (cap rate OK for commercial) |
| Financing | **BNM OPR-linked**, ~4.3-4.5% p.a., **70-90% margin of finance**, 30-35 yr |
| Connectivity | **MRT/LRT/monorail** distance + highways (SPRINT, LDP, DUKE, NKVE, MEX, Penchala Link) |
| Schools | **International schools** (GIS, MKIS, Alice Smith, ISKL, etc.), private/national |
| Risk factors | Leasehold decay, **NAPIC overhang/oversupply**, sinking-fund/maintenance adequacy, **Bumi-lot** resale restriction, short-stay/Airbnb regulation, flood-prone areas, strata Act 757, BOMBA/CCC/OC |
| Professionals | **BOVAEP-registered REN/REA**, registered valuers |

## Strip / replace US-isms

Remove or convert: `$`, Zillow/Redfin/Realtor, county assessor, GreatSchools, Walk/Transit/Bike Score (replace with MY connectivity), flood-zone (→ flood-prone areas), 27.5-yr depreciation, MLS, ZIP code (→ postcode), acres (→ sq ft, or note acres for land). Keep universal concepts (BRRRR, GRM, DSCR, cap rate for commercial).

## Workflow for any pasted skill

1. Save under `.claude/skills/<skill-name>/SKILL.md`.
2. Localize per the table above before committing.
3. Keep the skill's structure/scoring intact — only swap the market context.
4. Commit + push to the working branch. Don't open a PR unless asked.
