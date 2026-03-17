PLUGIN_NAME = "predictions"
DESCRIPTION = "Prediction tracking, accuracy dashboard, and life event logging"
COMMANDS = {
    "events": {"help": "Life event tracking", "handler": "run_events"},
    "dashboard": {"help": "Prediction accuracy dashboard", "handler": "run_dashboard"},
}
