from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

def asset(path: str):
    return str(BASE_DIR / "assets" / path)