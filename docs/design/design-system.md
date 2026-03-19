# Jyotish Design System — Complete UI Specification

> Paste this into v0.dev, Claude.ai Artifacts, or any AI design tool.
> Each section has a ready-to-paste prompt at the end.

---

## Brand Identity

**Name:** DaivAI — Vedic Astrology Intelligence
**Feel:** Sacred document meets modern mobile app. Like a Pandit Ji's notebook, not a software dashboard.
**Invocation:** "श्री गणेशाय नमः" (not "ॐ" — use the proper invocation before any kundali)
**Closing:** "शुभम् भवतु" (May auspiciousness prevail)
**Language:** Hindi-English mix. Headers in Devanagari, data in English, explanations in Hindi. Like how a modern Pandit speaks.

---

## Color Palette

| Token | Hex | Usage |
|-------|-----|-------|
| `saffron` | `#FF6F00` | Primary brand, headers, top bars, sacred accent |
| `saffron-light` | `#FFF3E0` | Hover states, card highlights |
| `cream` | `#FFFDE7` | Page background, body fill |
| `deep-green` | `#2E7D32` | Benefic planets, positive indicators, recommended |
| `deep-red` | `#C62828` | Malefic planets, prohibited, danger warnings |
| `gold` | `#FF8F00` | Yogakaraka planet, golden period, star ratings |
| `indigo` | `#1A237E` | Section headers, chart borders, text headings |
| `text-primary` | `#212121` | Body text |
| `text-secondary` | `#757575` | Captions, footnotes, metadata |
| `bg-card` | `#FFFFFF` | Card background |
| `border` | `#E0E0E0` | Card borders, dividers |

**Rule:** Never use pure black (#000). Never use blue links. Saffron is the only accent color for interactive elements.

---

## Typography

| Style | Font | Size (mobile) | Size (desktop) | Weight | Usage |
|-------|------|---------------|----------------|--------|-------|
| `display` | Noto Sans Devanagari | 28px | 36px | 700 | Page titles (श्री गणेशाय नमः) |
| `h1` | Noto Sans Devanagari | 22px | 28px | 600 | Section headers |
| `h2` | Noto Sans Devanagari | 18px | 22px | 600 | Sub-section headers |
| `h3` | Noto Sans Devanagari | 16px | 18px | 500 | Card titles |
| `body` | Noto Sans Devanagari | 14px | 16px | 400 | Body text |
| `body-hi` | Noto Sans Devanagari | 15px | 17px | 400 | Hindi body text (slightly larger for readability) |
| `caption` | Noto Sans | 12px | 13px | 400 | Footnotes, metadata |
| `data` | JetBrains Mono / monospace | 13px | 14px | 400 | Degrees, numbers, coordinates |

---

## Spacing System

| Token | Value | Usage |
|-------|-------|-------|
| `xs` | 4px | Inside badges |
| `sm` | 8px | Between related items |
| `md` | 16px | Card padding, section gaps |
| `lg` | 24px | Between sections |
| `xl` | 32px | Page margins (mobile) |
| `2xl` | 48px | Page margins (desktop) |

**Mobile-first:** All designs start at 390px width (iPhone 14). Scale up to 768px (tablet) and 1024px (desktop).

---

## Reusable Components

### 1. Sacred Header Bar
- Full-width saffron (#FF6F00) bar, 56px height
- White text, centered: "श्री गणेशाय नमः"
- Appears on EVERY page/screen as the first element
- On PDF: saffron band across top of every page

### 2. Page Title Card
- Cream background, indigo text
- Person's name (large, Devanagari + English)
- Birth details: DOB | TOB | Place
- Lagna badge: rounded pill, saffron background, white text "मिथुन लग्न"
- Moon badge: "चन्द्र: रोहिणी पाद 2"
- Current dasha badge: "गुरु > बुध दशा"

### 3. Diamond Chart (North Indian)
- Traditional diamond shape inside a rounded card
- Thick indigo borders (3px)
- 12 triangular houses, each showing:
  - Sign name in Hindi (small, gray, top of triangle)
  - Planet abbreviations in Devanagari (large, colored by role)
  - Degree value (small, below planet name)
- Planet colors: green = benefic for THIS lagna, red = malefic, gold = yogakaraka
- "लग्न" label in the center
- Card has: title bar ("D1 राशि चक्र"), rounded corners, subtle shadow

### 4. Planet Row (reusable for tables)
- Left: Planet icon/emoji + Hindi name + English name
- Middle: Sign, House, Degree, Nakshatra
- Right: Status badges (वक्री = blue pill, अस्त = orange pill, उच्च = green pill, नीच = red pill)
- Alternating row colors: white / cream

### 5. Dasha Badge
- Pill-shaped, color based on planet's functional role
- Shows: Hindi planet name + date range
- Current dasha has pulsing border or "अभी" badge

### 6. Gemstone Card
- Card with colored left border (green = recommended, red = prohibited, gold = test)
- Stone image placeholder (circle with stone color)
- Stone name (Hindi + English)
- Weight: "3.08 रत्ती (Recommended)" in large text
- Key factors as small pills: "अवस्था: कुमार", "गरिमा: नीच"
- vs Website: "GemPundit: 6.5 | Ours: 3.08"

### 7. Status Badge
- Small rounded pill
- Green + "शुभ" for benefic
- Red + "अशुभ" for malefic
- Gold + "मिश्र" for mixed
- Red + "मारक" for maraka
- Gold + "योगकारक" for yogakaraka

### 8. Info Card
- White card with rounded corners (12px)
- Subtle border (#E0E0E0)
- Optional saffron left border (4px) for emphasis
- Title in indigo h3
- Body in text-primary
- Footer caption in text-secondary

### 9. Warning Card
- Red left border (4px)
- Red icon (shield/warning)
- Used for prohibited stones, maraka warnings

### 10. Sacred Footer
- "शुभम् भवतु" centered
- "daivai" small caption
- Page number (for PDF)

---

## Pages to Design (14 total)

### PAGE 1: Title Page (श्री गणेशाय नमः)
**Used in:** PDF cover, Web landing after chart computation
**Components:** Sacred Header, Page Title Card
**Layout:**
```
┌─────────────────────────┐
│  ███ SAFFRON BAR ███    │
│  श्री गणेशाय नमः         │
├─────────────────────────┤
│                         │
│     [Name in large]     │
│  मनीष चौरसिया            │
│  Manish Chaurasia       │
│                         │
│  13/03/1989 | 12:17     │
│  वाराणसी                 │
│                         │
│  ┌─────┐ ┌─────┐       │
│  │मिथुन │ │रोहिणी│       │
│  │लग्न  │ │पाद 2│       │
│  └─────┘ └─────┘       │
│                         │
│  वर्तमान दशा: गुरु > बुध │
│                         │
│     शुभम् भवतु           │
└─────────────────────────┘
```

---

### PAGE 2: D1 Birth Chart (राशि चक्र)
**Used in:** PDF page 2, Web chart result, Telegram image
**Components:** Sacred Header, Diamond Chart, Legend
**Data:**
- 9 planets placed in 12 houses
- Each planet: Hindi abbreviation + degree + functional role badge
- House numbers with sign names
- Legend at bottom: green = शुभ, red = अशुभ, gold = योगकारक

---

### PAGE 3: D9 Navamsha Chart (नवमांश)
**Used in:** PDF page 3 (detailed/pandit)
**Components:** Same Diamond Chart component, different data
**Extra:** Vargottam planets marked with ★ star

---

### PAGE 4: Planet Positions Table (ग्रह स्थिति)
**Used in:** PDF, Web chart result
**Components:** Planet Row (x9), Status Badges
**Columns:**
| ग्रह | राशि | भाव | अंश | नक्षत्र | पाद | गति | अवस्था | बल | लग्न-फल |
**Mobile:** Horizontal scroll or stacked card view (one card per planet)

---

### PAGE 5: Dasha Timeline (दशा चक्र)
**Used in:** PDF, Web, Telegram
**Layout:** Vertical timeline (mobile-friendly, not horizontal Gantt)
```
  ● चन्द्र MD (1989-1999) ─── gray
  ● मंगल MD (1999-2006) ──── red (malefic)
  ● राहु MD (2006-2024) ──── gray
  ◉ गुरु MD (2024-2040) ──── red (CURRENT, expanded)
    ├ गुरु AD (2024-2026)
    ├ शनि AD (2026-2029) ← अभी
    ├ बुध AD (2029-2031) ← green (benefic)
    └ ...
  ● शनि MD (2040-2059) ──── green (benefic)
  ● बुध MD (2059-2076) ──── green (lagnesh!)
```
**Mobile:** Vertical is better than horizontal. Each MD is a row. Current expanded.

---

### PAGE 6: Ashtakavarga Grid (अष्टकवर्ग)
**Used in:** PDF, Web (pandit view)
**Layout:** 7 rows × 12 columns heatmap
- Green cells (5-8 bindus), Gold (3-4), Red (0-2)
- SAV total row at bottom
- Sign names in Hindi as column headers
- Planet names in Hindi as row headers
- Total: 337 shown prominently

---

### PAGE 7: Active Yogas (सक्रिय योग)
**Used in:** PDF, Web
**Layout:** Card stack (max 5-7 cards)
Each card:
```
┌──────────────────────────┐
│ 🟢 हंस योग (Hamsa Yoga)  │
│ शुभ — गुरु in कर्म भाव    │
│ Forming: Jupiter in 10th  │
│ "Bestows wisdom..."       │
└──────────────────────────┘
```

---

### PAGE 8: Shadbala Strength (षड्बल)
**Used in:** PDF, Web (pandit view)
**Layout:** Horizontal bars or radial chart
- 7 planets, each with strength bar
- Green if ratio > 1.0, Red if < 1.0
- Strongest/Weakest highlighted
- "सबसे बलवान: शुक्र (1.8)" at top

---

### PAGE 9: Golden Period (स्वर्ण काल)
**Used in:** PDF, Web
**Layout:** Single highlight card with gold border
```
┌──── GOLD BORDER ──────────┐
│  आपका स्वर्ण काल:          │
│  बुध महादशा               │
│  2059 — 2076              │
│                           │
│  लग्नेश की दशा — career,  │
│  intellect, communication │
│  at peak                  │
└───────────────────────────┘
```

---

### PAGE 10: Gemstone Recommendation (रत्न सुझाव)
**Used in:** PDF, Web, Telegram
**Layout:** 3 sections — Recommended / Test / Prohibited
```
RECOMMENDED ✅
┌──────────────────────────┐
│ 💚 पन्ना (Emerald)       │
│ Planet: बुध (Mercury)     │
│ Weight: 3.08 रत्ती        │
│ Factors: अवस्था कुमार,    │
│   नीच राशि, शुभ भाव      │
│ vs GemPundit: 6.5 रत्ती   │
│ Free alt: ओम् बुधाय नमः   │
└──────────────────────────┘

PROHIBITED ❌
┌──────────────────────────┐
│ 🔴 पुखराज (Yellow Sapphire)│
│ गुरु = 7th मारक lord     │
│ Free: ओम् गुरुवे नमः      │
└──────────────────────────┘
```

---

### PAGE 11: Daily Guidance (दैनिक मार्गदर्शन)
**Used in:** Web, Telegram, WhatsApp image
**Layout:** Single card, 3 levels
**Simple (1 card for WhatsApp):**
```
┌──────────────────────────┐
│ 18 मार्च 2026 | मंगलवार   │
│ ⭐⭐⭐⭐⭐⭐⭐ 7/10        │
│ Color: Red 🔴             │
│ Mantra: हनुमान चालीसा      │
│ Rahu Kaal: 3:00-4:30 PM  │
│ Good: नई शुरुआत, व्यायाम   │
│ Avoid: बड़ा निवेश           │
└──────────────────────────┘
```

---

### PAGE 12: Compatibility Report (गुण मिलान)
**Used in:** Web, PDF
**Layout:**
- Two name badges side by side
- 8 koota scores as progress bars
- Total score as large number with color indicator
- "36 में से 28 गुण = अति उत्तम"

---

### PAGE 13: Muhurta Results (शुभ मुहूर्त)
**Used in:** Web, PDF
**Layout:** Card list (top 5 dates)
Each card:
```
┌──────────────────────────┐
│ #1 — 25 मार्च 2026       │
│ बुधवार | रोहिणी नक्षत्र    │
│ Score: 8.5/10 ⭐          │
│ ✅ Favorable tithi        │
│ ✅ No Rahu Kaal           │
│ ⚠️ Moon in 8th transit    │
└──────────────────────────┘
```

---

### PAGE 14: Accuracy Certificate (प्रमाणपत्र)
**Used in:** PDF last page
**Layout:** Formal certificate card
- Computation metadata table
- Cross-verification note
- Disclaimer in Hindi: "यह computational tool है, Pandit Ji का विकल्प नहीं"
- QR code placeholder for verification link

---

## Design for Each Platform

### Mobile Web (Primary)
- 390px width, full height scroll
- Bottom tab bar: Home | Chart | Daily | Remedies | More
- Pull-to-refresh on daily page
- Share button → generates WhatsApp image

### WhatsApp Image Card
- 1080×1080 or 1080×1920 PNG
- One card = one insight (daily, gemstone, yoga)
- Large text, readable without zooming
- Brand watermark at bottom

### PDF (A4)
- Same components, laid out for print
- Saffron header band on every page
- Page numbers in footer
- "श्री गणेशाय नमः" on page 1 only

### Telegram
- Markdown formatted text
- Send chart as image attachment
- Inline keyboard buttons for navigation

---

## AI Prompt to Generate All Pages

Copy-paste this into v0.dev or Claude.ai:

```
Design a complete mobile-first Vedic astrology app called "DaivAI".

Color scheme: saffron (#FF6F00), cream (#FFFDE7), deep green (#2E7D32),
deep red (#C62828), gold (#FF8F00), indigo (#1A237E).

Font: Noto Sans Devanagari for all text. Hindi-English bilingual.

Header: Every page starts with a saffron bar containing "श्री गणेशाय नमः" in white.
Footer: "शुभम् भवतु | daivai"

Design these pages (390px mobile width):

1. TITLE PAGE: Person's name large in Devanagari, birth details, lagna badge
   (saffron pill), moon nakshatra badge, current dasha display.

2. BIRTH CHART: North Indian diamond layout inside a card. 12 houses with
   Hindi sign names. Planets colored: green=benefic, red=malefic, gold=yogakaraka.
   Show degree next to planet name.

3. PLANET TABLE: 9 rows, one per planet. Columns: planet (Hindi+EN), sign, house,
   degree, nakshatra, motion badges (retrograde=blue pill, combust=orange pill),
   strength ratio, functional role (शुभ/अशुभ/मारक badge).

4. DASHA TIMELINE: Vertical timeline with 9 mahadasha periods. Current period
   expanded to show antardashas. Color-coded by benefic/malefic. "अभी" badge
   on current period.

5. GEMSTONE CARD: Recommended stone with green left border, weight in ratti,
   key factors as pills, website comparison line. Prohibited stone with red
   left border and warning icon. Free alternatives section.

6. DAILY GUIDANCE: Single card with day rating (stars), color recommendation,
   mantra, rahu kaal time, good/avoid lists. Optimized for WhatsApp sharing.

7. YOGA CARDS: Stack of 3-5 cards, each showing yoga name (Hindi), effect badge
   (शुभ/अशुभ), forming planets, one-line description.

8. GOLDEN PERIOD: Single highlight card with gold border showing best upcoming
   dasha period and preparation advice.

Use shadcn/ui components. Tailwind CSS. All text must be readable at mobile size.
No tiny text. Generous padding. Sacred document feel, not corporate dashboard.
```

---

## Quick Start for Each Tool

### v0.dev
1. Go to v0.dev
2. Paste the prompt above
3. Click generate
4. Say "show me page 1 and page 2" to iterate
5. Share the v0 link back

### Claude.ai (Artifacts)
1. Go to claude.ai
2. Start new chat
3. Say: "Create an interactive HTML prototype" + paste the prompt
4. Iterate in Artifacts (renders live in browser)

### Adobe Express
1. Search templates: "spiritual" or "astrology"
2. Pick a warm, traditional template
3. Customize colors to saffron/cream palette
4. Design the title page and daily card as templates
5. Export as PNG → share with me for reference

### Gemini
1. Ask: "Design layout mockup for Vedic astrology mobile app"
2. Describe the saffron/cream theme
3. Ask for specific pages one by one
4. It will describe layouts you can then create in any tool
