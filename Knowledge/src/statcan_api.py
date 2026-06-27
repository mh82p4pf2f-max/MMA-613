#!/usr/bin/env python3
"""
statcan_api.py — Pull Statistics Canada source tables for the Labour Market
Stress & Social Support Prioritization Dashboard via the Web Data Service (WDS)
REST API. Standard library only — runs with `python3 statcan_api.py ...` and no
`pip install`.

WDS docs: https://www.statcan.gc.ca/en/developers/wds/user-guide   (no API key)

Each table is saved as a full CSV + the StatCan metadata CSV + a provenance
JSON under Knowledge/raw/<domain>/. The table TITLE, dimensions, geography, and time
range printed by `--metadata` are authoritative — confirm them on first pull and
update Knowledge/metadata/data_sources.md if a label changed.

GOVERNANCE
----------
- Aggregate, public data only. No individual records.
- Suppressed / blank / "F" / ".." cells are MISSING — never invented or imputed.
- Every output is a CLAIM to check, not a fact. Policy interpretation routes to
  the AI Council before it is treated as decision-ready.

Usage
-----
    python3 statcan_api.py --list                 # show configured tables
    python3 statcan_api.py --check                # which tables changed today?
    python3 statcan_api.py --metadata 9810059701  # print a table's dimensions
    python3 statcan_api.py --table census_income   # pull one table by key
    python3 statcan_api.py --all                   # pull every configured table
"""
from __future__ import annotations

import argparse
import io
import json
import sys
import urllib.request
import zipfile
from datetime import date, datetime, timezone
from pathlib import Path

WDS = "https://www150.statcan.gc.ca/t1/wds/rest"
UA = {"User-Agent": "MMA616-GovernedTriage/1.0 (educational project)"}

# Write raw data into the project's Knowledge/raw/ tree regardless of CWD.
ROOT = Path(__file__).resolve().parents[1]   # = Knowledge/
RAW = ROOT / "raw"

# --------------------------------------------------------------------------- #
# Configured source tables.
#   domain ∈ {labour_force, income, demographics, affordability}
#   "added": tables newly requested for this iteration (June 2026).
# Titles confirmed from statcan.gc.ca search June 2026; `--metadata <pid>`
# prints the authoritative cubeTitleEn at pull time.
# --------------------------------------------------------------------------- #
TABLES = {
    # ---- Labour force (the dashboard spine) --------------------------------
    "labour_force": {
        "pid": 14100287, "domain": "labour_force", "frequency": "monthly",
        "category": "labour force",
        "title": "Labour force characteristics, monthly, seasonally adjusted and "
                 "trend-cycle (LFS), 14-10-0287-01",
    },
    # ---- NEW tables requested this iteration -------------------------------
    "census_income": {
        "pid": 9810059701, "domain": "income", "frequency": "one-time (2021 Census)",
        "category": "income", "added": True,
        "title": "Employment income statistics by industry sectors, highest level "
                 "of education, immigrant status and period of immigration, work "
                 "activity, age and gender — Canada, provinces, territories, CMAs/CAs "
                 "(2021 Census, income year 2020), 98-10-0597-01",
    },
    "wages_occupation_annual": {
        "pid": 1410041701, "domain": "income", "frequency": "annual",
        "category": "income / wages", "added": True,
        "title": "Employee wages by occupation, annual, 14-10-0417-01",
    },
    "wages_occupation_monthly": {
        "pid": 1410042601, "domain": "income", "frequency": "monthly",
        "category": "income / wages", "added": True,
        "title": "Employee wages by occupation, monthly (confirm title via "
                 "--metadata), 14-10-0426-01",
    },
    # ---- Previously verified context tables (kept; pull as needed) ----------
    "income_individuals": {
        "pid": 11100239, "domain": "income", "frequency": "annual",
        "category": "income",
        "title": "Income of individuals by age group, sex and income source, "
                 "11-10-0239-01",
    },
    "low_income": {
        "pid": 11100135, "domain": "income", "frequency": "annual",
        "category": "income",
        "title": "Low income statistics by age, gender and economic family type, "
                 "11-10-0135-01",
    },
    "population": {
        "pid": 17100005, "domain": "demographics", "frequency": "annual",
        "category": "demographics",
        "title": "Population estimates on July 1, by age and gender, 17-10-0005-01",
    },
    "cpi_shelter": {
        "pid": 18100004, "domain": "affordability", "frequency": "monthly",
        "category": "affordability (proxy)",
        "title": "Consumer Price Index, monthly, not seasonally adjusted "
                 "(incl. Shelter), 18-10-0004-01",
    },
}


# --------------------------------------------------------------------------- #
# HTTP helpers (stdlib only)
# --------------------------------------------------------------------------- #
def _get(url: str, binary: bool = False):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=120) as r:
        data = r.read()
    return data if binary else data.decode("utf-8")


def _post_json(path: str, payload):
    body = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        f"{WDS}/{path}", data=body, method="POST",
        headers={**UA, "Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=120) as r:
        return json.loads(r.read().decode("utf-8"))


# --------------------------------------------------------------------------- #
# Operations
# --------------------------------------------------------------------------- #
def list_tables() -> None:
    print(f"{'key':<26}{'PID':<12}{'freq':<26}{'new?':<6}title")
    for k, t in TABLES.items():
        new = "NEW" if t.get("added") else ""
        print(f"{k:<26}{t['pid']:<12}{t['frequency']:<26}{new:<6}{t['title']}")


def check(on: str | None = None) -> None:
    on = on or date.today().isoformat()
    changed = json.loads(_get(f"{WDS}/getChangedCubeList/{on}")).get("object", [])
    changed_pids = {int(i["productId"]) for i in changed}
    print(f"{len(changed_pids)} StatCan tables changed on {on}.\n")
    for k, t in TABLES.items():
        flag = "UPDATED -> re-pull" if t["pid"] in changed_pids else "no change"
        print(f"  {k:<26} ({t['pid']}): {flag}")


def show_metadata(pid: int) -> None:
    """Print a table's title, frequency, date range, and dimensions/members."""
    meta = _post_json("getCubeMetadata", [{"productId": int(pid)}])
    obj = meta[0]["object"]
    print(f"Table {pid}: {obj.get('cubeTitleEn')}")
    print(f"Frequency code: {obj.get('frequencyCode')}  "
          f"Range: {obj.get('cubeStartDate')} -> {obj.get('cubeEndDate')}\n")
    for dim in obj.get("dimension", []):
        members = dim.get("member", [])
        print(f"Dimension {dim['dimensionPositionId']}: {dim['dimensionNameEn']} "
              f"({len(members)} members)")
        for m in members[:20]:
            print(f"    [{m['memberId']:>5}] {m['memberNameEn']}")
        if len(members) > 20:
            print(f"    ... ({len(members)} total)")
        print()


def pull_one(key: str) -> None:
    t = TABLES[key]
    pid = t["pid"]
    out_dir = RAW / t["domain"]
    out_dir.mkdir(parents=True, exist_ok=True)

    info = json.loads(_get(f"{WDS}/getFullTableDownloadCSV/{pid}/en"))
    if info.get("status") != "SUCCESS":
        sys.exit(f"[{key}] WDS did not return a download link: {info}")
    zip_url = info["object"]
    print(f"[{key}] downloading {zip_url} ...")
    blob = _get(zip_url, binary=True)

    with zipfile.ZipFile(io.BytesIO(blob)) as zf:
        data_name = next(n for n in zf.namelist()
                         if n.lower().endswith(".csv") and "metadata" not in n.lower())
        meta_name = next((n for n in zf.namelist() if "metadata" in n.lower()), None)
        (out_dir / f"{pid}.csv").write_bytes(zf.read(data_name))
        if meta_name:
            (out_dir / f"{pid}_metadata.csv").write_bytes(zf.read(meta_name))

    prov = {
        "key": key, "product_id": pid, "title": t["title"],
        "frequency": t["frequency"], "category": t["category"], "domain": t["domain"],
        "source_zip": zip_url,
        "table_page": f"https://www150.statcan.gc.ca/t1/tbl1/en/tv.action?pid={pid}",
        "wds_csv_endpoint": f"{WDS}/getFullTableDownloadCSV/{pid}/en",
        "retrieval_date": date.today().isoformat(),
        "pulled_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
    }
    (out_dir / f"{pid}.source.json").write_text(json.dumps(prov, indent=2))
    print(f"[{key}] saved -> {out_dir / f'{pid}.csv'}  (+ metadata CSV + provenance JSON)")


def main() -> None:
    ap = argparse.ArgumentParser(description="Pull StatCan source tables via the WDS API.")
    ap.add_argument("--list", action="store_true", help="show configured tables")
    ap.add_argument("--check", action="store_true", help="report which tables changed")
    ap.add_argument("--on", metavar="YYYY-MM-DD", help="date for --check (default: today)")
    ap.add_argument("--metadata", metavar="PID", help="print one table's dimensions by product id")
    ap.add_argument("--table", metavar="KEY", choices=list(TABLES), help="pull a single table by key")
    ap.add_argument("--all", action="store_true", help="pull every configured table")
    args = ap.parse_args()

    if not any((args.list, args.check, args.metadata, args.table, args.all)):
        ap.print_help(); return
    if args.list:
        list_tables()
    if args.check:
        check(args.on)
    if args.metadata:
        show_metadata(args.metadata)
    if args.table:
        pull_one(args.table)
    if args.all:
        for key in TABLES:
            pull_one(key)


if __name__ == "__main__":
    main()
