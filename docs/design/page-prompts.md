# Page-by-Page AI Prompts

> Open v0.dev or Claude.ai. Paste ONE prompt at a time.
> When you like a page, say "next" and paste the next prompt.
> Each prompt builds on the same design system.

---

## PROMPT 1: Design System + Title Page

```
Create a mobile-first (390px) Vedic astrology app page.

DESIGN SYSTEM:
- Colors: saffron #FF6F00, cream #FFFDE7, green #2E7D32, red #C62828, gold #FF8F00, indigo #1A237E
- Font: Noto Sans Devanagari (use Google Fonts import)
- Every page: saffron top bar with "श्री गणेशाय नमः" in white
- Bottom: "शुभम् भवतु" centered in gray
- Card radius: 12px, shadow: subtle

PAGE: Title / Cover Page
Show this data:
- Name: मनीष चौरसिया (Manish Chaurasia)
- DOB: 13/03/1989 | TOB: 12:17 PM
- Place: वाराणसी (Varanasi)
- Lagna: मिथुन (Gemini) — show as saffron badge/pill
- Moon: रोहिणी नक्षत्र पाद 2 — show as indigo badge
- Current Dasha: गुरु > बुध — show as badge with icon
- Feel: Sacred document. Warm. Traditional. NOT corporate.
```

---

## PROMPT 2: Birth Chart (Diamond)

```
Using the same design system (saffron/cream/indigo), create:

PAGE: North Indian Diamond Birth Chart (राशि चक्र)
- Traditional diamond shape (rotated square) with 12 triangular houses
- Thick indigo borders
- Each house shows:
  - Sign name in Hindi (small, gray): मिथुन, कर्क, सिंह...
  - Planets as colored text: green=benefic, red=malefic, gold=yogakaraka
  - Planet format: "गु 15°" (Hindi abbreviation + degree)
- Houses are numbered 1-12
- Center shows: "लग्न" with the lagna sign
- Below chart: Legend showing color meaning
  - 🟢 शुभ (Benefic) 🔴 अशुभ (Malefic) 🟡 योगकारक

Sample data for House 1 (Mithuna/Gemini):
  - No planets (empty)
House 7: गु 15° (Jupiter, red=malefic/maraka)
House 5: सू 28° (Sun), बु 10° (Mercury, green=lagnesh)

Card with rounded corners, subtle shadow, cream background.
Title bar: "D1 राशि चक्र — Birth Chart"
```

---

## PROMPT 3: Planet Positions Table

```
Same design system. Create:

PAGE: Planet Positions Table (ग्रह स्थिति)
Mobile-friendly card layout (not a wide table).

Show 9 planet cards stacked vertically. Each card:
┌─────────────────────────────┐
│ सूर्य (Sun)          House 5 │
│ Pisces (मीन) • 28.1°        │
│ Uttarabhadra • Pada 1        │
│ [अस्त] [neutral]            │
│ Shadbala: 1.2 ████████░░     │
│ Role: 3rd lord (अशुभ)       │
└─────────────────────────────┘

Badges:
- वक्री (Retrograde) = blue pill
- अस्त (Combust) = orange pill
- उच्च (Exalted) = green pill
- नीच (Debilitated) = red pill

Shadbala: progress bar, green if > 1.0, red if < 1.0
Role badge: शुभ=green, अशुभ=red, मारक=dark red, योगकारक=gold
```

---

## PROMPT 4: Dasha Timeline

```
Same design system. Create:

PAGE: Dasha Timeline (विंशोत्तरी दशा)
Vertical timeline layout for mobile.

9 Mahadasha periods, each as a row:
- Left: colored dot (green=benefic, red=malefic, gray=neutral)
- Middle: Planet name (Hindi + English), date range
- Right: duration years

Current period (Jupiter 2024-2040) is EXPANDED:
- Shows all 9 Antardasha sub-periods indented
- Current AD has "अभी" (NOW) badge pulsing
- Highlight the next benefic AD with gold border

Example:
  ● चन्द्र (Moon) — 1989-1999 — 10 years     [gray]
  ● मंगल (Mars) — 1999-2006 — 7 years         [red, अशुभ]
  ● राहु (Rahu) — 2006-2024 — 18 years        [gray]
  ◉ गुरु (Jupiter) — 2024-2040 — 16 years     [red, मारक, EXPANDED]
    ├─ गुरु-गुरु (2024-2026)
    ├─ गुरु-शनि (2026-2029)  ← अभी
    ├─ गुरु-बुध (2029-2031)  ← शुभ next
    └─ ...
  ○ शनि (Saturn) — 2040-2059                   [green, शुभ]
  ○ बुध (Mercury) — 2059-2076                   [green, लग्नेश ★]
```

---

## PROMPT 5: Gemstone Recommendation

```
Same design system. Create:

PAGE: Gemstone Recommendations (रत्न सुझाव)

Three sections:

SECTION 1 — RECOMMENDED (green header):
Card with green left border:
  Stone: पन्ना (Emerald) 💚
  Planet: बुध (Mercury) — लग्नेश
  Recommended Weight: 3.08 रत्ती
  Key Factors:
    [अवस्था: कुमार] [गरिमा: नीच] [भाव: 1+4 शुभ]
  vs Websites: GemPundit 6.5 | BrahmaGems 5.9 | Ours 3.08
  Free Alternative: ओम् बुधाय नमः (9000x) | हरा रंग पहनें

SECTION 2 — PROHIBITED (red header):
Card with red left border, red X icon:
  पुखराज (Yellow Sapphire) ❌
  गुरु = 7th + 10th lord, मारक, Kendradhipati dosha

  मूंगा (Red Coral) ❌
  मंगल = 6th + 11th lord, chief अशुभ

  मोती (Pearl) ❌
  चन्द्र = 2nd lord, मारक

SECTION 3 — Honesty Note:
Gray italic text:
"कोई भी शास्त्र सटीक रत्न भार नहीं बताता।
body_weight/10 formula gemstone industry की convention है, शास्त्र नहीं।"

SECTION 4 — Discuss with Pandit Ji:
Numbered list of 5 questions in Hindi
```

---

## PROMPT 6: Daily Guidance Card

```
Same design system. Create:

PAGE: Daily Guidance (दैनिक मार्गदर्शन)
Designed for WhatsApp sharing (1080px wide, single card).

Layout:
┌──────────────────────────────┐
│  श्री गणेशाय नमः              │ (saffron bar)
├──────────────────────────────┤
│  18 मार्च 2026 | मंगलवार       │
│  ⭐⭐⭐⭐⭐⭐⭐☆☆☆  7/10    │
│                              │
│  🔴 रंग: लाल (Red)            │
│  📿 मंत्र: हनुमान चालीसा        │
│  ⏰ राहु काल: 3:00-4:30 PM   │
│  🏥 स्वास्थ्य: पाचन पर ध्यान दें │
│                              │
│  ✅ शुभ कार्य:                 │
│  • नई शुरुआत                  │
│  • व्यायाम, खेल               │
│  • मंगल पूजा                  │
│                              │
│  ❌ अशुभ कार्य:               │
│  • बड़ा निवेश                  │
│  • यात्रा शुरू करना             │
│                              │
│  शुभम् भवतु | Jyotish AI     │
└──────────────────────────────┘

Make it look like a premium daily horoscope card.
Background: warm cream with subtle mandala watermark.
```

---

## PROMPT 7: Compatibility Report

```
Same design system. Create:

PAGE: Compatibility / Guna Milan (गुण मिलान)

Top: Two name cards side by side
  [मनीष] ←→ [प्रिया]
  Mithuna Lagna    Karka Lagna

Score: Large circle showing "28/36"
  Green if > 24, Gold if 18-24, Red if < 18
  "अति उत्तम (Excellent Match)"

8 Koota bars (vertical stack):
  वर्ण (Varna)     ████░  1/1
  वश्य (Vashya)    ████░  2/2
  तारा (Tara)      ████░  3/3
  योनि (Yoni)      ███░░  3/4
  ग्रह मैत्री       █████  5/5
  गण (Gana)        █████░ 5/6
  भकूट (Bhakoot)   █████░░ 5/7
  नाडी (Nadi)      ████░░░░ 4/8

Each bar: green if max score, gold if partial, red if 0
```

---

## PROMPT 8: Muhurta Results

```
Same design system. Create:

PAGE: Auspicious Dates (शुभ मुहूर्त)
Purpose shown at top: "विवाह मुहूर्त (Marriage)"

5 date cards stacked:
Each card:
  #1 | 25 मार्च 2026 | बुधवार
  नक्षत्र: रोहिणी | तिथि: शुक्ल पंचमी
  Score: ⭐⭐⭐⭐⭐⭐⭐⭐½ (8.5/10)
  ✅ शुभ नक्षत्र for marriage
  ✅ No राहु काल conflict
  ⚠️ Moon transiting 8th house

Cards ranked by score, best first.
Gold border on #1 card.
```

---

## PROMPT 9: Mobile Navigation + Home

```
Same design system. Create:

PAGE: App Home with Bottom Navigation

Bottom tab bar (5 tabs):
  🏠 Home | 📊 Chart | 🌅 Daily | 💎 Remedies | ⋮ More

HOME screen shows:
  - Sacred header (श्री गणेशाय नमः)
  - Today's quick card (day rating + color + mantra)
  - Current dasha badge
  - Quick actions: "View Chart" | "Today's Guidance" | "Gemstone Report"
  - Family members list (if any)

Clean, minimal, sacred feel. Not cluttered.
Warm cream background. Saffron accents only on interactive elements.
```

---

## After Designing

When you're happy with the designs from v0.dev or Claude Artifacts:
1. Share the v0 link or screenshots with me
2. I'll implement each page as:
   - **Web (HTML/CSS/JS)** — for the mobile dashboard
   - **Image cards (PIL)** — for WhatsApp/Telegram sharing
   - **PDF (WeasyPrint)** — using the same HTML templates
3. All components are reusable across all platforms
4. Single design system, clean code, no duplication
