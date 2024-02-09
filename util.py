import json

def read_settings() -> dict:
    with open("settings.json", "r", encoding="utf-8") as settings:
        settings = json.load(settings)
    return settings
