## Remedies & Recommendations

Generate personalized remedies for {{ name }} based on chart analysis.

### Current Dasha Focus
- Mahadasha: {{ current_dasha.mahadasha }}
- Antardasha: {{ current_dasha.antardasha }}
- Lagna: {{ lagna }}

### Doshas to Address
{% for d in doshas %}
- {{ d.name }} ({{ d.name_hindi }}): {{ d.severity }} — {{ d.description }}
{% endfor %}

### Weak Planets Needing Strengthening
{% for s in strengths %}{% if not s.is_strong %}
- {{ s.planet }} (Rank {{ s.rank }}, Strength {{ s.strength }})
{% endif %}{% endfor %}

### Generate These Remedies:

#### 1. Gemstone Recommendations
For the {{ lagna }} lagna:
- Which gemstone to wear (ONLY for functional benefics)
- Weight, finger, metal, wearing day
- CONTRAINDICATIONS: Which stones to NEVER wear together
- Trial period recommendation for Blue Sapphire

#### 2. Weekly Routine
Create a personalized weekly routine:
| Day | Planet | Activity | Why (from chart) |
|-----|--------|----------|------------------|

#### 3. Mantras
- Primary mantra for current Mahadasha lord
- Lagna lord mantra
- Any dosha-specific mantras

#### 4. Daan (Donations)
- What to donate, when, to whom
- Based on weak/afflicted planets

#### 5. Behavioral Remedies
- Most practical actions for the current period
- Direction to face while working (from lagna)
- Colors to wear/avoid

Format: Structured, practical, specific. Include Hindi mantras in Devanagari.
