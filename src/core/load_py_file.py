import os
from pathlib import Path


def load(file_path):
    path = Path(file_path)

    if path.suffix.lower() != ".py":
        return None

    if not path.is_file():
        raise FileNotFoundError(file_path)

    with open(path, "r", encoding="utf-8") as f:
        return f.read()
