## Career Analysis

Analyze the career prospects for {{ name }} based on:

### 10th House (Karma Bhava)
- 10th house sign from {{ lagna }} lagna
- 10th lord placement, dignity, and aspects
- Any planets in the 10th house

### Key Career Indicators
- Dasamsha (D10) implications
- 10th lord's nakshatra and its career significations
- Mercury's strength (communication/business)
- Saturn's role (discipline/service)

### Current Career Dasha
- Current Mahadasha: {{ current_dasha.mahadasha }} ({{ current_dasha.md_start }} to {{ current_dasha.md_end }})
- Current Antardasha: {{ current_dasha.antardasha }}
- How this dasha period affects career

### Career Timeline
Map the dasha periods to career phases:
{% for md in mahadashas %}
- {{ md.lord }} Mahadasha ({{ md.start }} to {{ md.end }}): Career implications
{% endfor %}

### Recommended Career Fields
Based on the chart's dominant planets and houses, suggest suitable career fields.

Format: Be specific with timing using dasha periods. Use both English and Hindi terms.
