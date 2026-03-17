"""FastAPI web dashboard — browser access to Jyotish AI."""
from __future__ import annotations

import json
import logging
from pathlib import Path

logger = logging.getLogger(__name__)


def create_app():
    """Create and configure the FastAPI application."""
    try:
        from fastapi import FastAPI, Request, Form
        from fastapi.responses import HTMLResponse, JSONResponse
    except ImportError:
        raise ImportError("Install with: pip install 'jyotish[web]'")

    app = FastAPI(title="Jyotish AI", version="1.0.0",
                  description="Vedic Astrology Dashboard")

    @app.get("/", response_class=HTMLResponse)
    async def home() -> str:
        """Home page with chart form."""
        return _render_page("Jyotish AI", _HOME_HTML)

    @app.get("/health")
    async def health() -> dict[str, str]:
        """Health check endpoint."""
        return {"status": "ok", "version": "1.0.0"}

    @app.post("/chart", response_class=HTMLResponse)
    async def compute_chart_view(
        name: str = Form(...),
        dob: str = Form(...),
        tob: str = Form(...),
        place: str = Form("Varanasi"),
        gender: str = Form("Male"),
    ) -> str:
        """Compute chart and show results."""
        from jyotish_engine.compute.chart import compute_chart
        from jyotish_engine.compute.yoga import detect_all_yogas
        from jyotish_engine.compute.dosha import detect_all_doshas
        from jyotish_engine.compute.dasha import compute_mahadashas

        chart = compute_chart(name=name, dob=dob, tob=tob, place=place, gender=gender)
        yogas = detect_all_yogas(chart)
        doshas = detect_all_doshas(chart)
        dashas = compute_mahadashas(chart)

        # Build HTML
        planets_html = ""
        for p in chart.planets.values():
            flags = ""
            if p.is_retrograde:
                flags += " <span class='badge'>R</span>"
            if p.is_combust:
                flags += " <span class='badge badge-warn'>C</span>"
            planets_html += (
                f"<tr><td><b>{p.name}</b>{flags}</td><td>{p.sign}</td>"
                f"<td>{p.house}</td><td>{p.degree_in_sign:.1f}°</td>"
                f"<td>{p.nakshatra} P{p.pada}</td><td>{p.dignity}</td></tr>"
            )

        yogas_html = ""
        for y in yogas:
            cls = "good" if y.effect == "benefic" else "warn" if y.effect == "mixed" else "bad"
            yogas_html += f"<div class='yoga {cls}'><b>{y.name}</b> ({y.name_hindi}) — {y.description}</div>"

        doshas_html = ""
        for d in doshas:
            cls = "warn" if d.is_present else "good"
            doshas_html += f"<div class='yoga {cls}'><b>{d.name}</b> — {d.description}</div>"

        from datetime import datetime
        now = datetime.now(tz=dashas[0].start.tzinfo) if dashas else datetime.now()
        dasha_html = ""
        for md in dashas:
            current = " class='current'" if md.start <= now <= md.end else ""
            dasha_html += (
                f"<tr{current}><td><b>{md.lord}</b></td>"
                f"<td>{md.start.strftime('%Y-%m-%d')}</td>"
                f"<td>{md.end.strftime('%Y-%m-%d')}</td></tr>"
            )

        body = f"""
        <h2>कुंडली — {chart.name}</h2>
        <p>DOB: {chart.dob} | TOB: {chart.tob} | Place: {chart.place}</p>
        <p><b>Lagna: {chart.lagna_sign} ({chart.lagna_sign_en} / {chart.lagna_sign_hi}) at {chart.lagna_degree:.1f}°</b></p>

        <h3>Planetary Positions</h3>
        <table>
        <tr><th>Planet</th><th>Sign</th><th>House</th><th>Degree</th><th>Nakshatra</th><th>Dignity</th></tr>
        {planets_html}
        </table>

        <h3>Yogas</h3>
        {yogas_html}

        <h3>Doshas</h3>
        {doshas_html}

        <h3>Vimshottari Mahadasha</h3>
        <table>
        <tr><th>Planet</th><th>Start</th><th>End</th></tr>
        {dasha_html}
        </table>

        <p><a href="/">← Compute another chart</a></p>
        """
        return _render_page(f"Kundali — {chart.name}", body)

    @app.get("/daily", response_class=HTMLResponse)
    async def daily_view() -> str:
        """Show today's daily guidance for saved chart."""
        chart_path = Path("charts/manish.json")
        if not chart_path.exists():
            return _render_page("Daily", "<p>No saved chart. Save one first.</p>")

        from jyotish_engine.models.chart import ChartData
        from jyotish_products.plugins.daily.engine import run_daily, DailyLevel

        chart = ChartData.model_validate_json(chart_path.read_text())
        result = run_daily(chart, DailyLevel.DETAILED)

        body = f"<h2>Daily Guidance — {chart.name}</h2><pre>{result}</pre>"
        return _render_page("Daily Guidance", body)

    @app.get("/api/chart")
    async def api_chart(
        name: str = "Manish", dob: str = "13/03/1989",
        tob: str = "12:17", place: str = "Varanasi", gender: str = "Male",
    ) -> JSONResponse:
        """JSON API for chart computation."""
        from jyotish_engine.compute.chart import compute_chart
        chart = compute_chart(name=name, dob=dob, tob=tob, place=place, gender=gender)
        return JSONResponse(content=json.loads(chart.model_dump_json()))

    return app


def _render_page(title: str, body: str) -> str:
    """Wrap body content in HTML page template."""
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title} — Jyotish AI</title>
<style>
body {{ font-family: 'Segoe UI', system-ui, sans-serif; max-width: 900px; margin: 0 auto; padding: 20px; background: #fefefe; color: #333; }}
h1, h2, h3 {{ color: #8B4513; }}
table {{ border-collapse: collapse; width: 100%; margin: 10px 0; }}
th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
th {{ background: #FFF8DC; color: #8B4513; }}
tr.current {{ background: #FFF3CD; font-weight: bold; }}
.yoga {{ padding: 8px; margin: 4px 0; border-radius: 4px; }}
.good {{ background: #d4edda; }}
.warn {{ background: #fff3cd; }}
.bad {{ background: #f8d7da; }}
.badge {{ background: #6c757d; color: white; padding: 2px 6px; border-radius: 3px; font-size: 0.8em; }}
.badge-warn {{ background: #ffc107; color: black; }}
form {{ background: #f8f9fa; padding: 20px; border-radius: 8px; }}
input, select {{ padding: 8px; margin: 4px; border: 1px solid #ddd; border-radius: 4px; }}
button {{ padding: 10px 20px; background: #8B4513; color: white; border: none; border-radius: 4px; cursor: pointer; }}
button:hover {{ background: #A0522D; }}
nav {{ margin-bottom: 20px; }}
nav a {{ margin-right: 15px; color: #8B4513; text-decoration: none; }}
nav a:hover {{ text-decoration: underline; }}
pre {{ background: #f8f9fa; padding: 15px; border-radius: 8px; white-space: pre-wrap; }}
</style>
</head>
<body>
<h1>🙏 Jyotish AI</h1>
<nav><a href="/">Home</a> <a href="/daily">Daily</a> <a href="/api/chart">API</a></nav>
{body}
</body>
</html>"""


_HOME_HTML = """
<h2>Compute Birth Chart</h2>
<form method="post" action="/chart">
  <div>
    <label>Name: <input name="name" value="Manish Chaurasia" required></label>
  </div>
  <div>
    <label>DOB: <input name="dob" value="13/03/1989" placeholder="DD/MM/YYYY" required></label>
  </div>
  <div>
    <label>TOB: <input name="tob" value="12:17" placeholder="HH:MM" required></label>
  </div>
  <div>
    <label>Place: <input name="place" value="Varanasi"></label>
  </div>
  <div>
    <label>Gender:
      <select name="gender"><option>Male</option><option>Female</option></select>
    </label>
  </div>
  <div style="margin-top:10px">
    <button type="submit">🔮 Compute Chart</button>
  </div>
</form>
"""
