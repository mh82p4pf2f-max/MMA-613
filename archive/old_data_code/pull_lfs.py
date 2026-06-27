#!/usr/bin/env python3
"""
pull_lfs.py — Pull Statistics Canada Labour Force Survey (LFS) data via the
Web Data Service (WDS) REST API.

Primary source
--------------
Table 14-10-0287-01, "Labour force characteristics, monthly, seasonally
adjusted and trend-cycle" — StatCan product ID (PID) 14100287.
Indicators: unemployment rate, participation rate, employment rate, labour
force counts, by geography (Canada / province / territory), gender, and age
group, monthly back to 1976.

WDS API docs: https://www.statcan.gc.ca/en/developers/wds/user-guide
No API key is required. Responses are JSON / CSV.

This script intentionally uses ONLY the Python standard library, so it runs
with `python3 pull_lfs.py ...` and no `pip install` step.

Usage
-----
    python3 pull_lfs.py --check          # did the table change today? (freshness gate)
    python3 pull_lfs.py --metadata       # list the table's dimensions + member codes
    python3 pull_lfs.py --full           # download the whole table -> data/lfs_14100287_raw.csv
    python3 pull_lfs.py --full --tidy    # also write a tidy slice -> data/lfs_14100287_tidy.csv

Governance note (read the project CLAUDE.md): the LFS measures labour-market
STRESS only. It cannot establish individual eligibility, poverty, household
need, disability, food insecurity, or housing insecurity. Treat every output
as a claim to check, flag small/suppressed cells, and route anything that
could affect a real funding decision to a human reviewer.
"""

from __future__ import annotations

import argparse
import csv
import io
import json
import sys
import urllib.request
import zipfile
from datetime import date
from pathlib import Path

WDS = "https://www150.statcan.gc.ca/t1/wds/rest"
PID = 14100287                      # Table 14-10-0287-01
OUT_DIR = Path(__file__).resolve().parent   # write outputs next to this file (data/)
USER_AGENT = "MMA616-GovernedClaude/1.0 (educational project)"

# Indicators we usually want for a labour-market-stress dashboard. Matched by
# case-insensitive substring against the table's characteristic column.
TARGET_INDICATORS = ("unemployment rate", "participation rate", "employment rate")


# --------------------------------------------------------------------------- #
# Low-level HTTP helpers (stdlib only)
# --------------------------------------------------------------------------- #
def _get(url: str, binary: bool = False):
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=60) as resp:
        data = resp.read()
    return data if binary else data.decode("utf-8")


def _post_json(path: str, payload) -> object:
    body = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        f"{WDS}/{path}",
        data=body,
        headers={"User-Agent": USER_AGENT, "Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=60) as resp:
        return json.loads(resp.read().decode("utf-8"))


# --------------------------------------------------------------------------- #
# WDS operations
# --------------------------------------------------------------------------- #
def check_changed(on: str | None = None) -> None:
    """Freshness gate: report whether our table changed on a given date.

    LFS updates ~monthly, so most days return nothing — that is the point.
    Pull fresh data only when the table actually changed.
    """
    on = on or date.today().isoformat()
    raw = _get(f"{WDS}/getChangedCubeList/{on}")
    changed = json.loads(raw).get("object", [])
    pids = {int(item["productId"]) for item in changed}
    if PID in pids:
        when = next(i.get("releaseTime") for i in changed if int(i["productId"]) == PID)
        print(f"UPDATED: table {PID} changed on {on} (released {when}). Pull fresh data.")
    else:
        print(f"no change for table {PID} on {on} ({len(pids)} tables changed that day).")


def show_metadata() -> None:
    """Print the table's dimensions and member codes.

    Use these member IDs to build a `coordinate` (dot-separated member IDs, one
    per dimension) for targeted pulls via getDataFromCubePidCoordAndLatestNPeriods.
    """
    meta = _post_json("getCubeMetadata", [{"productId": PID}])
    obj = meta[0]["object"]
    print(f"Table {PID}: {obj.get('cubeTitleEn')}")
    print(f"Frequency code: {obj.get('frequencyCode')}  "
          f"Range: {obj.get('cubeStartDate')} -> {obj.get('cubeEndDate')}\n")
    for dim in obj.get("dimension", []):
        print(f"Dimension {dim['dimensionPositionId']}: {dim['dimensionNameEn']}")
        for m in dim.get("member", [])[:25]:
            print(f"    [{m['memberId']:>4}] {m['memberNameEn']}")
        if len(dim.get("member", [])) > 25:
            print(f"    ... ({len(dim['member'])} members total)")
        print()


def download_full_table(tidy: bool) -> None:
    """Download the entire table as CSV and (optionally) write a tidy slice."""
    info = json.loads(_get(f"{WDS}/getFullTableDownloadCSV/{PID}/en"))
    if info.get("status") != "SUCCESS":
        sys.exit(f"WDS did not return a download link: {info}")
    zip_url = info["object"]
    print(f"Downloading {zip_url} ...")
    blob = _get(zip_url, binary=True)

    with zipfile.ZipFile(io.BytesIO(blob)) as zf:
        # The data CSV is the one that is NOT the *_MetaData.csv
        name = next(n for n in zf.namelist()
                    if n.lower().endswith(".csv") and "metadata" not in n.lower())
        rows = list(csv.DictReader(io.TextIOWrapper(zf.open(name), encoding="utf-8-sig")))

    raw_path = OUT_DIR / "lfs_14100287_raw.csv"
    with raw_path.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)
    print(f"wrote {len(rows):,} rows -> {raw_path}")

    if tidy:
        write_tidy(rows)


def write_tidy(rows: list[dict]) -> None:
    """Keep the headline rate indicators and the columns a dashboard needs."""
    headers = rows[0].keys()
    char_col = _find(headers, "labour force characteristics") or _find(headers, "characteristic")
    value_col = _find(headers, "value") or "VALUE"
    geo_col = _find(headers, "geo") or "GEO"
    date_col = _find(headers, "ref_date") or "REF_DATE"
    gender_col = _find(headers, "gender") or _find(headers, "sex")
    age_col = _find(headers, "age group")
    dtype_col = _find(headers, "data type")

    keep_cols = [c for c in (date_col, geo_col, char_col, gender_col, age_col,
                             dtype_col, value_col) if c]

    tidy_rows = []
    for r in rows:
        characteristic = (r.get(char_col) or "").lower()
        if any(ind in characteristic for ind in TARGET_INDICATORS):
            tidy_rows.append({c: r.get(c, "") for c in keep_cols})

    tidy_path = OUT_DIR / "lfs_14100287_tidy.csv"
    with tidy_path.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=keep_cols)
        writer.writeheader()
        writer.writerows(tidy_rows)
    print(f"wrote {len(tidy_rows):,} tidy rows ({', '.join(TARGET_INDICATORS)}) -> {tidy_path}")


def _find(headers, needle: str):
    """Find a column whose name contains `needle` (case-insensitive)."""
    needle = needle.lower()
    for h in headers:
        if needle in h.lower():
            return h
    return None


# --------------------------------------------------------------------------- #
# CLI
# --------------------------------------------------------------------------- #
def main() -> None:
    ap = argparse.ArgumentParser(description="Pull StatCan LFS table 14-10-0287-01 via the WDS API.")
    ap.add_argument("--check", action="store_true", help="report whether the table changed (freshness gate)")
    ap.add_argument("--on", metavar="YYYY-MM-DD", help="date to check with --check (default: today)")
    ap.add_argument("--metadata", action="store_true", help="print dimensions and member codes")
    ap.add_argument("--full", action="store_true", help="download the entire table to CSV")
    ap.add_argument("--tidy", action="store_true", help="with --full, also write a tidy rate-only CSV")
    args = ap.parse_args()

    if not any((args.check, args.metadata, args.full)):
        ap.print_help()
        return
    if args.check:
        check_changed(args.on)
    if args.metadata:
        show_metadata()
    if args.full:
        download_full_table(tidy=args.tidy)


if __name__ == "__main__":
    main()
