## Spiritual & Psychological Profile

Analyze the spiritual and psychological nature of {{ name }}:

### Moon Nakshatra Analysis
{% for p in planets %}{% if p.name == 'Moon' %}
- Moon in {{ p.nakshatra }}, Pada {{ p.pada }}
- Moon sign: {{ p.sign }} ({{ p.sign_en }})
- Moon house: {{ p.house }}
{% endif %}{% endfor %}

This nakshatra reveals the core psychological nature, emotional patterns, and spiritual inclinations.

### Lagna & Moon Combination
- Lagna: {{ lagna }} — external personality
- Moon: The emotional self and subconscious patterns

### 9th House (Dharma Bhava)
- 9th lord placement and its spiritual implications
- Jupiter (guru planet) analysis

### 12th House (Moksha Bhava)
- 12th house connections to spirituality and liberation
- Ketu's placement (natural moksha karaka)

### Psychological Strengths
Based on strong planets:
{% for s in strengths %}{% if s.is_strong %}
- {{ s.planet }} (Rank {{ s.rank }}): Psychological strength this brings
{% endif %}{% endfor %}

### Spiritual Practices Suited
Based on the Moon nakshatra and dominant planets, recommend spiritual practices.

Format: Deep, introspective tone. Use both Hindi spiritual terms and English explanations.
