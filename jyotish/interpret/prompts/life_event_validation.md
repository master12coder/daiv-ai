## Life Event Validation

Match each life event against the dasha period running at that time.

### Dasha Timeline
{% for md in mahadashas %}
- {{ md.lord }} Mahadasha: {{ md.start }} to {{ md.end }}
{% endfor %}

### Life Events to Validate
{% if life_events %}
{% for event in life_events %}
- **{{ event.date }}**: {{ event.event }}
{% endfor %}
{% else %}
No life events provided.
{% endif %}

### Analysis Required
For each event, create a table:
| Date | Event | Mahadasha | Antardasha | Relevant House/Planet | Match Rating |
|------|-------|-----------|------------|----------------------|--------------|

Match Rating: STRONG (clear planetary connection), MODERATE (indirect connection), WEAK (no clear connection)

### Interpretation
- Explain why each event matches or doesn't match the running dasha
- Reference specific house lords and their significations
- Identify patterns (e.g., all career events during 10th lord dashas)
- Overall chart accuracy assessment based on how many events match

Format: Table format with detailed explanations below.
