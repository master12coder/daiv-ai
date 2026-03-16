## Financial Analysis

Analyze the wealth and financial prospects for {{ name }} based on:

### Key Financial Houses
- **2nd House (Dhana Bhava):** Accumulated wealth, family money, speech
- **11th House (Labha Bhava):** Income, gains, fulfillment of desires
- **5th House:** Speculative gains, past life merit
- **9th House (Bhagya Bhava):** Fortune, luck

### Dhan Yogas Present
{% for y in yogas %}
{% if 'Dhan' in y.name or 'Lakshmi' in y.name %}
- {{ y.name }}: {{ y.description }}
{% endif %}
{% endfor %}

### Jupiter's Role
Jupiter is the natural significator of wealth. Its placement:
{% for p in planets %}{% if p.name == 'Jupiter' %}
- Jupiter in {{ p.sign }}, House {{ p.house }}, Dignity: {{ p.dignity }}
{% endif %}{% endfor %}

### Financial Timeline by Dasha
{% for md in mahadashas %}
- {{ md.lord }} period ({{ md.start }} - {{ md.end }}): Financial implications
{% endfor %}

### Wealth-Building Advice
Based on strong houses and planets, suggest optimal financial strategies.

Format: Include specific dasha periods for financial highs and lows. Hindi + English.
