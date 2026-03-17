PLUGIN_NAME = "remedies"
DESCRIPTION = "Gemstone recommendations, weekly pooja plan, Lal Kitab remedies"
COMMANDS = {
    "remedies": {"help": "Get personalized remedy recommendations", "handler": "run_remedies"},
    "pooja": {"help": "Generate weekly pooja plan", "handler": "run_pooja"},
}
