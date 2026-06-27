#!/usr/bin/env python3
"""
app.py — Labour Market Stress & Social Support Prioritization Dashboard.

A governed decision-SUPPORT dashboard for a social-assistance program owner /
policy lead. It surfaces which areas and groups show elevated *labour-market*
distress (LFS unemployment / employment / participation) so a human can decide
where to focus policy review. It broadens to full economic distress once the
income and housing tables connect (currently NaN, so confidence is medium).
Choosing or delivering any intervention is the owner's downstream call.

GOVERNANCE — READ BEFORE USE
----------------------------
- This dashboard does NOT determine who needs social assistance, eligibility,
  or benefits. It produces a TRIAGE signal for human policy review only.
- Claude-generated briefing text is a CLAIM to verify, not a fact.
- Missing / suppressed data is flagged, never invented.
- Any policy interpretation is reviewed by the AI Council before it is treated
  as decision-ready (see the "AI Council review status" tab).

Run:
    pip install streamlit pandas
    streamlit run dashboard/app.py
Reads: Knowledge/processed/policy_triage_panel.csv (built by the notebooks / src pipeline).
"""
from __future__ import annotations

from pathlib import Path

import pandas as pd
import streamlit as st

ROOT = Path(__file__).resolve().parents[1]
PANEL = ROOT / "Knowledge" / "processed" / "policy_triage_panel.csv"
SYN_PANEL = ROOT / "Knowledge" / "synthetic" / "policy_triage_panel_SYNTHETIC.csv"

st.set_page_config(page_title="Labour Market Stress — Policy Triage", layout="wide")

CAVEAT = (
    "⚠️ **Triage signal only.** This view flags areas for *human policy review*. "
    "It does **not** determine social-assistance need, eligibility, or benefits. "
    "Figures are aggregate public Statistics Canada data; suppressed/missing values "
    "are flagged, not invented."
)

SYN_BANNER = (
    "🧪 **SYNTHETIC DEMONSTRATION DATA — not real Statistics Canada values.** "
    "Labour-market rates derive from the real LFS; **income, low-income, housing and "
    "population are simulated** so every view is fully populated. Scores here are "
    "illustrative — **not a real triage signal and not for any program decision.** "
    "The real governed panel (honest, with income/housing still pending) lives at "
    "`Knowledge/processed/policy_triage_panel.csv` and is checked separately via "
    "`Knowledge/src/verify.py`. Still triage language only — never eligibility, "
    "benefits, or individual claims."
)


@st.cache_data
def load_demo_panel() -> pd.DataFrame:
    """Province × month slice of the SYNTHETIC panel — every column populated, so all
    views render fully. Clearly labelled synthetic; never the governed panel.

    Built from the Total-Gender, 15+ rows; core (25-54) and older (55+) unemployment
    are attached as driver columns to match the real panel's shape.
    """
    if not SYN_PANEL.exists():
        return pd.DataFrame()
    s = pd.read_csv(SYN_PANEL, low_memory=False)
    tot = s[s["gender"] == "Total - Gender"]
    head = tot[tot["age_group"] == "15 years and over"].copy()
    for band, col in [("25 to 54 years", "core_unemployment_rate"),
                      ("55 years and over", "older_unemployment_rate")]:
        b = (tot[tot["age_group"] == band][["geo", "ref_date", "unemployment_rate"]]
             .rename(columns={"unemployment_rate": col}))
        head = head.merge(b, on=["geo", "ref_date"], how="left")
    head["income_indicator"] = "Median employment income (SYNTHETIC, annual)"
    head["date"] = pd.to_datetime(head["ref_date"], errors="coerce")
    return head


def latest_snapshot(df: pd.DataFrame) -> pd.DataFrame:
    return df.sort_values("ref_date").groupby("geo").tail(1)


def main() -> None:
    st.title("Labour Market Stress & Social Support Prioritization")
    st.caption("Governed decision-support for policy review & triage · MMA 616 · "
               "labour-market distress signal (broadens to economic distress when "
               "income/housing connect)")

    active_caveat = SYN_BANNER
    st.error(SYN_BANNER)
    df = load_demo_panel()

    if df.empty:
        st.error("No demo data found. Run "
                 "`python3 Knowledge/src/generate_synthetic_demo.py` to build "
                 "`Knowledge/synthetic/policy_triage_panel_SYNTHETIC.csv`.")
        return

    # Sidebar filters
    geos = sorted(df["geo"].unique())
    sel_geos = st.sidebar.multiselect("Geographies", geos, default=geos)
    months = sorted(df["ref_date"].dropna().unique())
    sel_month = st.sidebar.select_slider("Reference month", options=months,
                                         value=months[-1])
    view = df[df["geo"].isin(sel_geos)]
    snap = view[view["ref_date"] == sel_month]

    tabs = st.tabs([
        "1 · Executive summary", "2 · Regional stress", "3 · Demographic vulnerability",
        "4 · Income context", "5 · Affordability pressure", "6 · Priority score",
        "7 · Evidence panel", "8 · AI Council review", "9 · Caveats & limitations",
    ])

    # 1 — Executive summary
    with tabs[0]:
        st.subheader(f"Executive summary — {sel_month}")
        st.markdown(active_caveat)
        ranked = snap.sort_values("policy_review_priority_score", ascending=False)
        if not ranked.empty:
            top = ranked.iloc[0]
            c1, c2, c3 = st.columns(3)
            c1.metric("Highest triage score", f"{top['policy_review_priority_score']:.0f}",
                      help="0-100, higher = review sooner")
            c1.write(f"**{top['geo']}**")
            c2.metric("Unemployment rate", f"{top.get('unemployment_rate', float('nan')):.1f}%")
            c3.metric("Score confidence", str(top.get("confidence_flag", "—")))
            st.dataframe(ranked[["geo", "policy_review_priority_score", "confidence_flag",
                                 "unemployment_rate", "youth_unemployment_rate"]],
                         use_container_width=True, hide_index=True)
        st.caption("Claude can draft a briefing paragraph from this table — but the draft "
                   "is a claim for an analyst to verify, and the AI Council reviews any "
                   "policy interpretation before it is used.")

    # 2 — Regional stress
    with tabs[1]:
        st.subheader("Regional labour-market stress")
        rank = snap.sort_values("policy_review_priority_score", ascending=False)
        st.bar_chart(rank.set_index("geo")["policy_review_priority_score"])
        st.markdown("**Unemployment rate over time**")
        wide = view.pivot_table(index="date", columns="geo", values="unemployment_rate")
        st.line_chart(wide)

    # 3 — Demographic vulnerability
    with tabs[2]:
        st.subheader("Demographic vulnerability")
        st.markdown("Unemployment by age band — overall (15+), youth (15-24), core (25-54), "
                    "older (55+). Seasonally adjusted, Total-Gender. Youth feeds the score; "
                    "core/older are drivers. **Seniors 65+ is not published in the LFS source**, "
                    "so 'older' is 55+.")
        cols = [c for c in ("geo", "unemployment_rate", "youth_unemployment_rate",
                            "core_unemployment_rate", "older_unemployment_rate") if c in snap]
        d = snap[cols].copy()
        if "youth_unemployment_rate" in d and "unemployment_rate" in d:
            d["youth_gap_pp"] = (d["youth_unemployment_rate"] - d["unemployment_rate"]).round(1)
        st.dataframe(d.sort_values("youth_unemployment_rate", ascending=False),
                     use_container_width=True, hide_index=True)
        st.caption("Gender (Men+/Women+) and age bands scored as their own rows are pending "
                   "(the latter needs an AI-Council-ratified scoring redesign). Unscored age "
                   "view: Knowledge/processed/policy_triage_panel_age_exploratory.csv. "
                   "Missing slices are flagged, not inferred.")

    # 4 — Income context
    with tabs[3]:
        st.subheader("Income context (annual · synthetic)")
        income_cols = [c for c in ("geo", "income_indicator", "income_value",
                                   "low_income_rate") if c in snap]
        st.dataframe(snap[income_cols].sort_values("income_value", ascending=False)
                     if "income_value" in snap else snap[income_cols],
                     use_container_width=True, hide_index=True)
        st.caption("Median employment income & low-income rate (LIM-AT) — 🧪 SYNTHETIC demo "
                   "values (annual; repeat across the year by join design). Not measured StatCan data.")

    # 5 — Affordability pressure
    with tabs[4]:
        st.subheader("Housing / affordability pressure (PROXY · synthetic)")
        st.caption("Proxy = year-over-year growth in the Shelter CPI (18-10-0004-01). "
                   "Not a measured affordability or core-housing-need rate. 🧪 SYNTHETIC demo values.")
        st.line_chart(view.pivot_table(index="date", columns="geo",
                                       values="housing_pressure_proxy"))

    # 6 — Priority score
    with tabs[5]:
        st.subheader("Policy review priority score")
        st.markdown(
            "A transparent 0-100 triage score combining unemployment level & 12-mo change, "
            "employment & participation decline (vs **3-mo** average), youth unemployment, "
            "low-income rate, and shelter-cost pressure — each normalised against fixed, "
            "documented anchors. **Missing inputs lower confidence; they are never filled in** "
            "(low-income & housing are pending, so confidence is currently medium).")
        st.dataframe(snap.sort_values("policy_review_priority_score", ascending=False)[
            ["geo", "policy_review_priority_score", "score_confidence",
             "confidence_flag", "score_explanation"]],
            use_container_width=True, hide_index=True)

    # 7 — Evidence panel
    with tabs[6]:
        st.subheader("Evidence panel")
        g = st.selectbox("Geography", sorted(snap["geo"].unique()))
        row = snap[snap["geo"] == g]
        if not row.empty:
            st.json({k: (None if pd.isna(v) else v) for k, v in row.iloc[0].to_dict().items()
                     if k in ("geo", "ref_date", "unemployment_rate", "employment_rate",
                              "participation_rate", "youth_unemployment_rate",
                              "core_unemployment_rate", "older_unemployment_rate",
                              "unemp_change", "emp_change", "part_change",
                              "policy_review_priority_score", "score_confidence",
                              "confidence_flag", "missing_value_flag", "score_explanation",
                              "source_product_id")})
        st.caption("Source: Statistics Canada LFS 14-10-0287-01 (+ context tables when "
                   "downloaded). See Knowledge/metadata/data_sources.md.")

    # 8 — AI Council review status
    with tabs[7]:
        st.subheader("AI Council review status")
        st.markdown(
            "- **Status:** 🟡 *Reviewed 2026-06-27 — recommended **Approve with revisions**; "
            "awaiting human Council ratification.* Remains a prototype until signed.\n"
            "- **Required revisions:** ✅ 3-mo employment/participation windows · ✅ core/older "
            "age-band drivers (65+ absent from source) · ✅ reframe to labour-market distress · "
            "⬜ download low-income + CPI-Shelter · ⬜ re-run the 5 known-answer cases — **3 of 5 done.**\n"
            "- The AI Council reviews accuracy, usefulness, clarity, appropriateness, "
            "governance, safety, scope, and evidence before any deployment-ready claim.\n"
            "- Decisions recorded in `00_course_artifacts/08_governance/ai_council_decision_log.md` "
            "and `ai_council_review_2026-06-27.md`.")
        st.warning("Recommended decision is **Approve with revisions** and is **not yet ratified "
                   "by a human Council member** — treat every output here as a draft for human review.")

    # 9 — Caveats & limitations
    with tabs[8]:
        st.subheader("Caveats & limitations")
        st.markdown(
            "- **Triage, not need.** Flags areas for human review; never determines "
            "eligibility or benefits.\n"
            "- **Proxy housing field.** Shelter-CPI growth ≠ measured affordability.\n"
            "- **Frequency mismatch.** Monthly LFS spine; income/wages/population are annual "
            "context joined by year.\n"
            "- **Missing data flagged.** Suppressed/blank values lower score confidence and "
            "are never imputed.\n"
            "- **Claims, not facts.** Claude-drafted summaries require analyst + AI Council "
            "review.\n\n"
            "Full detail: `Knowledge/metadata/integration_notes.md`.")


if __name__ == "__main__":
    main()
