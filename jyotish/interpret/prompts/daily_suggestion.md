## Daily Suggestion

Generate a concise daily suggestion for {{ name }} for {{ transit_date }}.

### Today's Transits
{% for t in transits %}
- {{ t.name }} in {{ t.sign }} (natal house {{ t.house }}){% if t.retrograde %} [R]{% endif %}
{% endfor %}

### Major Transit Alerts
{% for mt in major_transits %}
- {{ mt }}
{% endfor %}

### Current Dasha
- {{ current_dasha.mahadasha }}-{{ current_dasha.antardasha }}

### Generate
Provide a SHORT daily suggestion in this format (both Hindi and English):

**Today's Suggestion:**
1. Day and ruling planet
2. Color to wear
3. Mantra recommendation (if applicable)
4. Good for: (2-3 activities)
5. Avoid: (1-2 things to avoid based on transit)
6. One-line transit insight

Keep it to 5-6 lines maximum. Practical and actionable.
