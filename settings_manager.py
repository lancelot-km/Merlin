import yaml
import os

SETTINGS_FILE = "settings.yml"

DEFAULT_SETTINGS = {
    "download_path": "",
    "audio_only": False,
    "download_playlist": False
}

def load_settings():
    if not os.path.exists(SETTINGS_FILE):
        save_settings(DEFAULT_SETTINGS)
    with open(SETTINGS_FILE, 'r') as f:
        return yaml.safe_load(f)

def save_settings(settings: dict):
    with open(SETTINGS_FILE, 'w') as f:
        yaml.dump(settings, f)
