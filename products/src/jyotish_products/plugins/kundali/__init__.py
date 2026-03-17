PLUGIN_NAME = "kundali"
DESCRIPTION = "Full birth chart report with 18 sections, North Indian diamond chart, and PDF export"
COMMANDS = {
    "chart": {"help": "Compute and display birth chart", "handler": "show_chart"},
    "report": {"help": "Generate full interpretation report", "handler": "generate_report"},
    "save": {"help": "Save chart for later reuse", "handler": "save_chart"},
}
