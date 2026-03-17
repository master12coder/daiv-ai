## 10-Year Forecast & Timeline

Provide a timeline forecast for {{ name }} based on upcoming dasha periods.

### Dasha Timeline
{% for md in mahadashas %}
- **{{ md.lord }} Mahadasha:** {{ md.start }} to {{ md.end }}
{% endfor %}

### Current Period
- Running: {{ current_dasha.mahadasha }}-{{ current_dasha.antardasha }}

### Forecast Requirements

#### Year-by-Year Summary (Next 10 Years)
For each year, provide:
- Dominant dasha influence
- Key themes (career, health, relationships, finances)
- Best months and challenging months
- One actionable recommendation

#### Golden Periods
Identify the most favorable upcoming periods based on:
- Benefic planet dashas
- Yogakaraka dasha
- Trikona lord periods

#### Challenging Periods
Identify periods needing caution:
- Dusthana lord dashas
- Maraka periods
- Saturn/Rahu transits

#### Key Decision Windows
Best times for: property purchase, career change, marriage, health investments.

Format: Year-by-year breakdown with specific months where possible.
