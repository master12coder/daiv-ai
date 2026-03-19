"""Full chart analysis — compute ALL engine calculations in one call.

Single entry point that runs every engine computation and returns
a FullChartAnalysis model. Deterministic: same input = same output.

NOTE: lordship_context must be passed in from the products layer,
since engine/ cannot import products/ (CLAUDE.md boundary rule).
"""

from __future__ import annotations

import logging
from collections.abc import Callable
from typing import Any

from daivai_engine.compute.argala import compute_argala
from daivai_engine.compute.ashtakavarga import compute_ashtakavarga
from daivai_engine.compute.avasthas import (
    compute_deeptadi_avasthas,
    compute_lajjitadi_avasthas,
)
from daivai_engine.compute.dasha import (
    compute_mahadashas,
    find_current_dasha,
)
from daivai_engine.compute.dosha import detect_all_doshas
from daivai_engine.compute.double_transit import (
    check_double_transit,
    check_double_transit_from_moon,
)
from daivai_engine.compute.gandanta import check_gandanta
from daivai_engine.compute.graha_yuddha import detect_planetary_war
from daivai_engine.compute.house_comparison import compare_whole_sign_vs_chalit
from daivai_engine.compute.ishta_kashta import compute_ishta_kashta
from daivai_engine.compute.narayana_dasha import compute_narayana_dasha
from daivai_engine.compute.saham import compute_sahams
from daivai_engine.compute.special_lagnas import compute_special_lagnas
from daivai_engine.compute.strength import compute_shadbala
from daivai_engine.compute.sudarshan import compute_sudarshan
from daivai_engine.compute.upapada import compute_upapada_lagna
from daivai_engine.compute.verify import verify_chart_accuracy
from daivai_engine.compute.vimshopaka import compute_vimshopaka_bala
from daivai_engine.compute.yoga import detect_all_yogas
from daivai_engine.models.analysis import FullChartAnalysis
from daivai_engine.models.chart import ChartData


logger = logging.getLogger(__name__)


def compute_full_analysis(
    chart: ChartData,
    lordship_context: dict[str, Any] | None = None,
) -> FullChartAnalysis:
    """Run ALL engine computations and return a single typed result.

    Each module is wrapped in safe_compute() — individual failures
    don't crash the pipeline, they log a warning and return empty.

    Args:
        chart: Computed birth chart.
        lordship_context: Pre-built lordship context from products layer.

    Returns:
        FullChartAnalysis containing every computation result.
    """
    if lordship_context is None:
        lordship_context = {}

    # Core
    mahadashas = compute_mahadashas(chart)
    md, ad, _pd = find_current_dasha(chart)
    yogas = detect_all_yogas(chart)
    doshas = detect_all_doshas(chart)
    shadbala = compute_shadbala(chart)
    avk = compute_ashtakavarga(chart)

    # Advanced strength
    vimshopaka = safe_compute(compute_vimshopaka_bala, chart)
    ishta_kashta = safe_compute(compute_ishta_kashta, chart, shadbala)

    # Avasthas
    deeptadi = safe_compute(compute_deeptadi_avasthas, chart)
    lajjitadi = safe_compute(compute_lajjitadi_avasthas, chart)

    # Special checks
    gandanta = safe_compute(check_gandanta, chart)
    yuddha = safe_compute(detect_planetary_war, chart)

    # Transit
    dt_lagna = safe_compute(check_double_transit, chart)
    dt_moon = safe_compute(check_double_transit_from_moon, chart)

    # Jaimini
    upapada = compute_upapada_lagna(chart)
    argala = safe_compute(compute_argala, chart)

    # Dashas (additional)
    narayana = safe_compute(compute_narayana_dasha, chart)

    # Special lagnas
    special_lagnas = safe_compute(compute_special_lagnas, chart)
    if not isinstance(special_lagnas, dict):
        special_lagnas = {}

    # Sudarshan Chakra
    sudarshan = safe_compute(compute_sudarshan, chart)

    # House comparison
    house_shifts = safe_compute(compare_whole_sign_vs_chalit, chart)

    # Saham points
    sahams = safe_compute(compute_sahams, chart)

    # Verification
    verification = verify_chart_accuracy(chart)

    return FullChartAnalysis(
        chart=chart,
        mahadashas=mahadashas,
        current_md=md,
        current_ad=ad,
        narayana_dasha=narayana,
        yogas=yogas,
        doshas=doshas,
        shadbala=shadbala,
        ashtakavarga=avk,
        vimshopaka=vimshopaka,
        ishta_kashta=ishta_kashta,
        deeptadi_avasthas=deeptadi,
        lajjitadi_avasthas=lajjitadi,
        gandanta=gandanta,
        graha_yuddha=yuddha,
        double_transit=dt_lagna,
        double_transit_moon=dt_moon,
        upapada=upapada,
        argala=argala,
        special_lagnas=special_lagnas,
        sudarshan=sudarshan,
        house_shifts=house_shifts,
        sahams=sahams,
        lordship_context=lordship_context,
        verification_warnings=verification,
    )


def safe_compute(fn: Callable, *args: Any, **kwargs: Any) -> Any:
    """Call a computation function. On crash, log error and return empty list."""
    try:
        return fn(*args, **kwargs)
    except Exception as e:
        logger.warning("Computation %s failed: %s", fn.__name__, e)
        return []
