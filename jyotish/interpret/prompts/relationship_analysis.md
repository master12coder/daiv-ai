## Relationship Analysis

Analyze relationships and marriage for {{ name }}:

### 7th House (Kalatra Bhava — Marriage House)
- 7th house sign from {{ lagna }} lagna
- 7th lord placement, dignity, and aspects
- Venus's role (natural significator of marriage)

### Marriage Timing
- Which dasha periods favor marriage
- Current period: {{ current_dasha.mahadasha }}-{{ current_dasha.antardasha }}

### Mangal Dosha Check
{% for d in doshas %}{% if d.name == 'Mangal Dosha' %}
- {{ d.name }}: {{ d.severity }} — {{ d.description }}
{% endif %}{% endfor %}

### 5th House (Children)
- 5th lord and Jupiter (putrakaraka) analysis
- Favorable periods for children

### Key Relationship Planets
{% for p in planets %}{% if p.name in ['Venus', 'Jupiter', 'Moon'] %}
- {{ p.name }} in {{ p.sign }}, House {{ p.house }}, {{ p.dignity }}
{% endif %}{% endfor %}

### Navamsha (D9) Insights
Navamsha is the chart of dharma and marriage. Vargottam planets: {{ vargottam_planets | join(', ') if vargottam_planets else 'None' }}

Format: Be sensitive and positive. Reference specific dasha periods for timing.
