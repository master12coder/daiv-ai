## Health Analysis

Analyze the health profile for {{ name }} based on:

### 6th House (Roga Bhava — Disease House)
- 6th house lord placement and dignity
- Any planets in the 6th house
- Malefic influences on the 6th house

### Planet-Body Mapping
- Sun → Heart, bones, eyes, vitality
- Moon → Mind, blood, fluids, lungs
- Mars → Blood, muscles, head, accidents
- Mercury → Nervous system, skin, speech
- Jupiter → Liver, fat, diabetes, growth
- Venus → Reproductive system, kidneys, throat
- Saturn → Joints, teeth, chronic disease, aging

### Vulnerable Periods
Based on dasha of 6th/8th lord or afflicted planets:
{% for md in mahadashas %}
- {{ md.lord }} period: Health implications
{% endfor %}

### Current Health Focus
- Current Mahadasha: {{ current_dasha.mahadasha }}
- Which body systems need attention now

### Doshas Affecting Health
{% for d in doshas %}
- {{ d.name }}: {{ d.description }}
{% endfor %}

### Preventive Recommendations
Based on weak planets and vulnerable periods, suggest preventive health measures.

Format: Be specific but sensitive. Reference specific planets and periods.
