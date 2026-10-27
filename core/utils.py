# Copyright (©) 2025, Alexander Suvorov. All rights reserved.
import json
import os


def ensure_directory(path: str):
    os.makedirs(os.path.dirname(path), exist_ok=True)


def load_json(filepath: str) -> dict:
    if os.path.exists(filepath):
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return {}
    return {}


def save_json(filepath: str, data: dict):
    ensure_directory(filepath)
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False, sort_keys=True)
