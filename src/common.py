from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_ROOT / "data"
OUTPUT_DIR = PROJECT_ROOT / "outputs"


def resolve_data_file(filename: str) -> Path:
    """Return a project data file from data/ or the repository root."""
    candidates = [DATA_DIR / filename, PROJECT_ROOT / filename]
    for candidate in candidates:
        if candidate.exists():
            return candidate
    searched = ", ".join(str(path) for path in candidates)
    raise FileNotFoundError(
        f"Could not find {filename}. Place it in data/ or the repository root. "
        f"Searched: {searched}"
    )


def load_csv(filename: str, **kwargs) -> pd.DataFrame:
    """Load a CSV while keeping file-location handling consistent."""
    return pd.read_csv(resolve_data_file(filename), **kwargs)


def ensure_output_dir() -> Path:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    return OUTPUT_DIR
