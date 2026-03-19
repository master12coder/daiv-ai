PLUGIN_NAME = "pandit"
DESCRIPTION = "Professional tools — corrections, trust scoring, comparison reports"
COMMANDS = {
    "correct": {"help": "Add a Pandit Ji correction", "handler": "run_correct"},
    "rules": {"help": "Show learned rules", "handler": "run_rules"},
}
