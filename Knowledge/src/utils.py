"""
utils.py — Shared paths and small helpers for the Labour Market Stress &
Social Support Prioritization Dashboard.

Governance: this project produces a TRIAGE signal for human policy review only.
It never establishes eligibility, need, or benefit decisions. See CLAUDE.md and
Knowledge/metadata/integration_notes.md.
"""
from __future__ import annotations

from pathlib import Path

# --------------------------------------------------------------------------- #
# Project paths. `src/` lives one level under the pipeline root `Knowledge/`,
# and raw/processed/metadata/outputs live directly under it (no `data/` wrapper).
# --------------------------------------------------------------------------- #
ROOT = Path(__file__).resolve().parents[1]   # = Knowledge/
DATA = ROOT                                   # raw/processed/metadata are direct children
RAW = DATA / "raw"
PROCESSED = DATA / "processed"
METADATA = DATA / "metadata"
OUTPUTS = ROOT / "outputs"
FIGURES = OUTPUTS / "figures"
TABLES = OUTPUTS / "tables"
BRIEFINGS = OUTPUTS / "briefing_outputs"

# Raw domain sub-folders (match the documented Knowledge/raw/ tree).
RAW_LABOUR = RAW / "labour_force"
RAW_INCOME = RAW / "income"
RAW_DEMOGRAPHICS = RAW / "demographics"
RAW_AFFORDABILITY = RAW / "affordability"


def ensure_dirs() -> None:
    """Create the output folders if they do not exist (raw/processed are tracked)."""
    for d in (PROCESSED, OUTPUTS, FIGURES, TABLES, BRIEFINGS,
              RAW_LABOUR, RAW_INCOME, RAW_DEMOGRAPHICS, RAW_AFFORDABILITY):
        d.mkdir(parents=True, exist_ok=True)


# Strings StatCan uses for suppressed / unavailable / not-applicable values.
# Treat all of these as MISSING — never invent or impute. (Ch. governance rule.)
SUPPRESSION = {"", "..", "...", "F", "x", "X", "E", "..E", "n/a", "NA", None}


def find_col(df, *needles):
    """Return the first column whose name contains any needle (case-insensitive)."""
    for n in needles:
        for c in df.columns:
            if n.lower() in str(c).lower():
                return c
    return None


def snake(name: str) -> str:
    """Lowercase snake_case a column label."""
    out = []
    for ch in str(name).strip():
        if ch.isalnum():
            out.append(ch.lower())
        elif out and out[-1] != "_":
            out.append("_")
    return "".join(out).strip("_")
