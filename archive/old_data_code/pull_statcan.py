#!/usr/bin/env python3
"""
pull_statcan.py — Pull all Statistics Canada source tables for the
"Labour Market Stress & Social Support Prioritization Dashboard" via the
Web Data Service (WDS) REST API. Stdlib only (no `pip install`).

Verified source tables (titles/dimensions/geography/frequency confirmed on
statcan.gc.ca, June 2026):

  key            PID        freq     title
  -------------  ---------  -------  --------------------------------------------------
  labour_force   14100287   monthly  Labour force characteristics (LFS)
  income         11100239   annual   Income of individuals by age group, sex & source
  low_income     11100135   annual   Low income statistics by age, gender & family type
  population     17100005   annual   Population estimates on July 1, by age and gender
  cpi_shelter    18100004   monthly  Consumer Price Index (incl. Shelter components)

Each table is saved as a full CSV plus a provenance JSON under
data/raw/<domain>/. Re-run only when --check says a table changed.

GOVERNANCE: aggregate public data only. Treat suppressed/blank cells as
missing — never invent or impute. See data/metadata/integration_notes.md.

Usage
-----
  python3 pull_statcan.py --list                 # show configured tables
  python3 pull_statcan.py --check                # which tables changed today?
  python3 pull_statcan.py --table income         # pull one table by key
  python3 pull_statcan.py --all                  # pull every table
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
UA = {"User-Agent": "MMA616-GovernedClaude/1.0 (educational project)"}
DATA = Path(__file__).resolve().parent          # the data/ folder

TABLES = {
    "labour_force": {"pid": 14100287, "domain": "labour_force",         "frequency": "monthly",
                     "title": "Labour force characteristics, monthly (LFS), 14-10-0287-01"},
    "income":       {"pid": 11100239, "domain": "income",               "frequency": "annual",
                     "title": "Income of individuals by age group, sex and income source, 11-10-0239-01"},
    "low_income":   {"pid": 11100135, "domain": "income",               "frequency": "annual",
                     "title": "Low income statistics by age, gender and economic family type, 11-10-0135-01"},
    "population":   {"pid": 17100005, "domain": "demographics",         "frequency": "annual",
                     "title": "Population estimates on July 1, by age and gender, 17-10-0005-01"},
    "cpi_shelter":  {"pid": 18100004, "domain": "housing_affordability", "frequency": "monthly",
                     "title": "Consumer Price Index, monthly, not seasonally adjusted, 18-10-0004-01"},
}


def _get(url: str, binary: bool = False):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=120) as r:
        data = r.read()
    return data if binary else data.decode("utf-8")


def list_tables() -> None:
    print(f"{'key':<14}{'PID':<11}{'freq':<9}title")
    for k, t in TABLES.items():
        print(f"{k:<14}{t['pid']:<11}{t['frequency']:<9}{t['title']}")


def check(on: str | None = None) -> None:
    on = on or date.today().isoformat()
    changed = json.loads(_get(f"{WDS}/getChangedCubeList/{on}")).get("object", [])
    changed_pids = {int(i["productId"]) for i in changed}
    print(f"{len(changed_pids)} StatCan tables changed on {on}.\n")
    for k, t in TABLES.items():
        flag = "UPDATED -> re-pull" if t["pid"] in changed_pids else "no change"
        print(f"  {k:<14} ({t['pid']}): {flag}")


def pull_one(key: str) -> None:
    t = TABLES[key]
    pid = t["pid"]
    out_dir = DATA / "raw" / t["domain"]
    out_dir.mkdir(parents=True, exist_ok=True)

    info = json.loads(_get(f"{WDS}/getFullTableDownloadCSV/{pid}/en"))
    if info.get("status") != "SUCCESS":
        sys.exit(f"[{key}] WDS did not return a link: {info}")
    zip_url = info["object"]
    print(f"[{key}] downloading {zip_url} ...")
    blob = _get(zip_url, binary=True)

    with zipfile.ZipFile(io.BytesIO(blob)) as zf:
        data_name = next(n for n in zf.namelist()
                         if n.lower().endswith(".csv") and "metadata" not in n.lower())
        meta_name = next((n for n in zf.namelist() if "metadata" in n.lower()), None)
        data_csv = out_dir / f"{pid}.csv"
        data_csv.write_bytes(zf.read(data_name))
        if meta_name:
            (out_dir / f"{pid}_metadata.csv").write_bytes(zf.read(meta_name))

    # provenance record next to the data
    prov = {
        "key": key, "product_id": pid, "title": t["title"], "frequency": t["frequency"],
        "domain": t["domain"], "source_zip": zip_url,
        "table_page": f"https://www150.statcan.gc.ca/t1/tbl1/en/tv.action?pid={pid}01",
        "pulled_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
    }
    (out_dir / f"{pid}.source.json").write_text(json.dumps(prov, indent=2))
    print(f"[{key}] saved -> {data_csv}  (+ provenance JSON)")


def main() -> None:
    ap = argparse.ArgumentParser(description="Pull StatCan source tables via the WDS API.")
    ap.add_argument("--list", action="store_true", help="show configured tables")
    ap.add_argument("--check", action="store_true", help="report which tables changed")
    ap.add_argument("--on", metavar="YYYY-MM-DD", help="date for --check (default: today)")
    ap.add_argument("--table", metavar="KEY", choices=list(TABLES), help="pull a single table by key")
    ap.add_argument("--all", action="store_true", help="pull every configured table")
    args = ap.parse_args()

    if not any((args.list, args.check, args.table, args.all)):
        ap.print_help(); return
    if args.list:
        list_tables()
    if args.check:
        check(args.on)
    if args.table:
        pull_one(args.table)
    if args.all:
        for key in TABLES:
            pull_one(key)


if __name__ == "__main__":
    main()
