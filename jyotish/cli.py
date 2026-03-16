"""CLI entry point — registers all command groups."""

from __future__ import annotations

import click

from jyotish.cli_core import chart, report, save, export_cmd, ashtakavarga_cmd, kp_cmd
from jyotish.cli_companion import daily, pooja, transit, muhurta, panchang_cmd, match_cmd
from jyotish.cli_learn import correct, learn_audio, rules, events, dashboard


@click.group()
@click.version_option(version="0.1.0", prog_name="jyotish")
def main() -> None:
    """Vedic AI Framework — AI-powered Vedic astrology."""


# Core commands
main.add_command(chart)
main.add_command(report)
main.add_command(save)
main.add_command(export_cmd)
main.add_command(ashtakavarga_cmd)
main.add_command(kp_cmd)

# Companion commands
main.add_command(daily)
main.add_command(pooja)
main.add_command(transit)
main.add_command(muhurta)
main.add_command(panchang_cmd)
main.add_command(match_cmd)

# Learning commands
main.add_command(correct)
main.add_command(learn_audio)
main.add_command(rules)
main.add_command(events)
main.add_command(dashboard)


if __name__ == "__main__":
    main()
