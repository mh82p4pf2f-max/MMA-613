#!/usr/bin/env python3
"""
app.py — Labour Market Stress & Social Support Prioritization Dashboard.

A governed decision-SUPPORT dashboard for a federal social-assistance program
owner / policy lead. It points the analyst to the area (and group) showing the
most elevated *labour-market* distress (LFS unemployment / employment /
participation) so a human can decide where to focus policy review.

GOVERNANCE — READ BEFORE USE
----------------------------
- This dashboard does NOT determine who needs social assistance, eligibility,
  or benefits. It produces a TRIAGE signal for human policy review only.
- Claude-generated briefing text is a CLAIM to verify, not a fact.
- Missing / suppressed data is flagged, never invented.
- Any policy interpretation is reviewed by the AI Council before it is treated
  as decision-ready (see "Governance & caveats").

Design: "government data room" — calm, official, trustworthy. Four views follow a
federal analyst's path: where to look → why → can I trust it → the rules. The
landing names the area (and group) to review first; the rest is the evidence.

Run:
    pip install streamlit pandas
    streamlit run dashboard/app.py
Reads: Knowledge/synthetic/policy_triage_panel_SYNTHETIC.csv (per-group panel).
"""
from __future__ import annotations

import re
from pathlib import Path

import pandas as pd
import streamlit as st

ROOT = Path(__file__).resolve().parents[1]
SYN_PANEL = ROOT / "Knowledge" / "synthetic" / "policy_triage_panel_SYNTHETIC.csv"

st.set_page_config(
    page_title="Labour Market Stress — Policy Triage",
    page_icon="🍁",
    layout="wide",
)

# ---------------------------------------------------------------------------
# Design tokens — "government data room" (one hue, amber only for confidence)
# ---------------------------------------------------------------------------
NAVY = "#1b2a4a"
CONF_STYLE = {
    "high":   ("#e7f0ea", "#2f6b46", "#3d8a5d"),   # bg, text, dot
    "medium": ("#fbf3e0", "#8a6314", "#c9962b"),
    "low":    ("#f7e7e6", "#9a3b34", "#c0544b"),
}

# Human-readable labels for the demographic dimensions
AGE_LABELS = {
    "15 years and over": "All ages (15+)",
    "15 to 24 years": "Youth (15–24)",
    "25 to 54 years": "Core (25–54)",
    "55 years and over": "Older (55+)",
}
GENDER_LABELS = {"Total - Gender": "all genders", "Men+": "men", "Women+": "women"}


def inject_css() -> None:
    st.markdown(
        """
        <style>
          #MainMenu, footer, [data-testid="stToolbar"], [data-testid="stDecoration"] {
              visibility: hidden; height: 0; }
          html, body, [class*="css"] {
              -webkit-font-smoothing: antialiased;
              font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto,
                           Helvetica, Arial, sans-serif; }
          .block-container { padding-top: 2.2rem; padding-bottom: 4rem; max-width: 1120px; }
          [data-testid="stMetricValue"], .hero-score, .driver-val { font-variant-numeric: tabular-nums; }
          h1, h2, h3 { color: #1b2533; letter-spacing: -0.01em; }
          h1 { font-weight: 680; }

          .stTabs [data-baseweb="tab-list"] { gap: 2px; border-bottom: 1px solid rgba(27,42,74,0.10); }
          .stTabs [data-baseweb="tab"] { font-size: 0.92rem; font-weight: 500; color: #5b6675; padding: 9px 16px; }
          .stTabs [aria-selected="true"] { color: #1b2a4a; font-weight: 650; }

          [data-testid="stMetric"] { background:#fff; border:1px solid rgba(27,42,74,0.10);
              border-radius:12px; padding:14px 16px; }
          [data-testid="stMetricLabel"] { color:#8a94a3; font-weight:500; }
          [data-testid="stDataFrame"] { border:1px solid rgba(27,42,74,0.10); border-radius:12px; }

          .masthead .kicker { display:inline-block; font-size:0.72rem; font-weight:600;
              letter-spacing:0.09em; text-transform:uppercase; color:#1b2a4a; background:#eef1f6;
              padding:4px 10px; border-radius:999px; }
          .masthead h1 { margin:12px 0 2px; font-size:1.9rem; }
          .masthead .sub { color:#5b6675; font-size:0.95rem; }

          .hero-lead { font-size:1.02rem; color:#2b3645; }
          .hero-card { background:#fff; border:1px solid rgba(27,42,74,0.12); border-radius:16px;
              padding:22px 26px; margin:10px 0 8px;
              box-shadow:0 1px 2px -1px rgba(27,42,74,0.10), 0 6px 18px -10px rgba(27,42,74,0.18); }
          .hero-eyebrow { font-size:0.72rem; font-weight:600; letter-spacing:0.09em;
              text-transform:uppercase; color:#8a94a3; margin-bottom:10px; }
          .hero-top { display:flex; align-items:baseline; gap:18px; flex-wrap:wrap; }
          .hero-score { font-size:3.2rem; font-weight:700; color:#1b2a4a; line-height:1; }
          .hero-score .max { font-size:1.1rem; font-weight:500; color:#8a94a3; }
          .hero-geo { font-size:1.35rem; font-weight:650; color:#1b2533; }
          .hero-geo .scope { font-size:0.85rem; font-weight:500; color:#8a94a3; margin-left:6px; }
          .hero-drivers { display:flex; gap:34px; flex-wrap:wrap; margin:20px 0 4px;
              padding-top:16px; border-top:1px solid rgba(27,42,74,0.08); }
          .driver-label { display:block; font-size:0.72rem; font-weight:500; letter-spacing:0.04em;
              text-transform:uppercase; color:#8a94a3; margin-bottom:4px; }
          .driver-val { font-size:1.25rem; font-weight:650; color:#1b2533; }
          .hero-foot { margin-top:16px; font-size:0.8rem; color:#8a94a3; }

          .chip { display:inline-flex; align-items:center; gap:6px; font-size:0.8rem;
              font-weight:600; padding:4px 12px; border-radius:999px; }
          .chip .dot { width:7px; height:7px; border-radius:50%; display:inline-block; }

          .brief-card { background:#fbfcfe; border:1px solid rgba(27,42,74,0.10);
              border-left:4px solid #1b2a4a; border-radius:12px; padding:18px 22px; margin:16px 0 6px; }
          .brief-eyebrow { font-size:0.72rem; font-weight:600; letter-spacing:0.08em;
              text-transform:uppercase; color:#1b2a4a; margin-bottom:8px; }
          .brief-body { color:#2b3645; font-size:0.98rem; line-height:1.6; }
          .brief-body b { color:#1b2533; }
          .brief-foot { margin-top:12px; font-size:0.78rem; color:#8a94a3; font-style:italic; }

          .verdict { background:#fbf3e0; border:1px solid #ecdcb0; border-radius:12px;
              padding:16px 20px; margin:6px 0 14px; color:#6b5417; }
          .verdict b { color:#7a5e12; }
        </style>
        """,
        unsafe_allow_html=True,
    )


def chip(flag) -> str:
    key = str(flag).strip().lower() if pd.notna(flag) else "low"
    bg, fg, dot = CONF_STYLE.get(key, ("#eef1f6", "#5b6675", "#8a94a3"))
    label = key if key in CONF_STYLE else "—"
    return (f'<span class="chip" style="background:{bg};color:{fg};">'
            f'<span class="dot" style="background:{dot};"></span>{label} confidence</span>')


def fmt(value, suffix: str = "", digits: int = 1) -> str:
    if value is None or (isinstance(value, float) and pd.isna(value)) or pd.isna(value):
        return "—"
    return f"{value:.{digits}f}{suffix}"


def clean_expl(text):
    if not isinstance(text, str):
        return text
    return re.sub(r"\s*\[SYNTHETIC DEMO DATA[^\]]*\]", "", text).strip()


@st.cache_data
def load_panel() -> pd.DataFrame:
    """Full per-group panel: geo × age_group × gender × month, every column populated.
    Loaded whole so the dashboard can rank provinces OR demographic groups."""
    if not SYN_PANEL.exists():
        return pd.DataFrame()
    df = pd.read_csv(SYN_PANEL, low_memory=False)
    df["date"] = pd.to_datetime(df["ref_date"], errors="coerce")
    return df


def group_label(age: str, gender: str) -> str:
    """A short human label for the selected demographic slice."""
    age_l = AGE_LABELS.get(age, age)
    if gender == "Total - Gender":
        return age_l
    return f"{age_l}, {GENDER_LABELS.get(gender, gender)}"


def build_briefing(top: pd.Series, month: str, slice_label: str | None) -> str:
    """Governed cycle briefing (cycle-briefing-writer format). Every figure comes
    from the panel row — nothing invented. Works for a province or a group."""
    geo = top["geo"]
    score = top["policy_review_priority_score"]
    flag = str(top.get("confidence_flag", "—")).lower()
    unemp = fmt(top.get("unemployment_rate"), "%")
    youth = fmt(top.get("youth_unemployment_rate"), "%")

    who = f"{slice_label} in {geo}" if slice_label else geo
    body = (
        f"<b>This cycle ({month}), the first area to review is {who}.</b> "
        f"It carries the highest policy-review priority score, <b>{score:.0f}/100</b> — "
        f"the steepest labour-market stress in this view, driven by an unemployment rate of "
        f"<b>{unemp}</b> and youth (15–24) unemployment of <b>{youth}</b>. "
        f"Confidence is <b>{flag}</b>. "
        f"Source: Statistics Canada Labour Force Survey 14-10-0287-01 (province-level — no city detail). "
        f"This is a triage signal — an area for closer human policy review, "
        f"<b>not</b> an eligibility, benefit, or program decision."
    )
    if pd.notna(score) and score >= 70:
        body += " <b>This output warrants direct human review before any program action.</b>"
    return body


def render_decision(snap_focus: pd.DataFrame, month: str, slice_label: str | None) -> None:
    """Shared 'where to look first' block: lead line + hero card + brief + shortlist."""
    ranked = snap_focus.sort_values("policy_review_priority_score", ascending=False)
    if ranked.empty:
        st.info("No rows for this selection.")
        return
    top = ranked.iloc[0]
    geo, score = top["geo"], top["policy_review_priority_score"]
    who = f"{slice_label} in {geo}" if slice_label else geo

    st.markdown(
        f'<p class="hero-lead"><b>Start here.</b> For {month}, <b>{who}</b> shows the most '
        f'elevated labour-market stress and warrants the first look.</p>',
        unsafe_allow_html=True,
    )
    scope = (slice_label + " · province-level") if slice_label else "province-level"
    st.markdown(
        f'''<div class="hero-card">
          <div class="hero-eyebrow">Highest priority to review · {month}</div>
          <div class="hero-top">
            <div class="hero-score">{score:.0f}<span class="max">/100</span></div>
            <div>
              <div class="hero-geo">{geo}<span class="scope">{scope}</span></div>
              <div style="margin-top:8px;">{chip(top.get("confidence_flag"))}</div>
            </div>
          </div>
          <div class="hero-drivers">
            <div><span class="driver-label">Unemployment</span>
                 <span class="driver-val">{fmt(top.get("unemployment_rate"), "%")}</span></div>
            <div><span class="driver-label">Youth (15–24)</span>
                 <span class="driver-val">{fmt(top.get("youth_unemployment_rate"), "%")}</span></div>
            <div><span class="driver-label">Employment</span>
                 <span class="driver-val">{fmt(top.get("employment_rate"), "%")}</span></div>
            <div><span class="driver-label">Participation</span>
                 <span class="driver-val">{fmt(top.get("participation_rate"), "%")}</span></div>
          </div>
          <div class="hero-foot">Source: Statistics Canada LFS 14-10-0287-01 ·
          Triage signal only — not an eligibility or benefit decision.</div>
        </div>''',
        unsafe_allow_html=True,
    )
    if pd.notna(score) and score >= 70:
        st.warning("This output warrants direct human review before any program action (top score ≥ 70).")

    st.markdown(
        f'''<div class="brief-card">
          <div class="brief-eyebrow">Cycle briefing · drafted by Claude</div>
          <div class="brief-body">{build_briefing(top, month, slice_label)}</div>
          <div class="brief-foot">A claim for an analyst to verify against the Statistics Canada
          source, reviewed by the AI Council (see Governance) — prototype.</div>
        </div>''',
        unsafe_allow_html=True,
    )

    st.markdown("#### Full ranked shortlist")
    st.caption("Every area in this view, highest priority first. The bar shows the 0–100 priority "
               "score; missing inputs lower confidence, never the score. Canada is a national "
               "baseline and is excluded from the focus ranking.")
    shortlist = ranked[["geo", "policy_review_priority_score", "confidence_flag",
                        "unemployment_rate", "youth_unemployment_rate"]].copy()
    shortlist.insert(0, "rank", range(1, len(shortlist) + 1))
    shortlist["confidence_flag"] = shortlist["confidence_flag"].astype(str).str.capitalize()
    st.dataframe(
        shortlist, use_container_width=True, hide_index=True,
        column_config={
            "rank": st.column_config.NumberColumn("#", width="small"),
            "geo": st.column_config.TextColumn("Geography", width="medium"),
            "policy_review_priority_score": st.column_config.ProgressColumn(
                "Priority score", format="%.0f", min_value=0, max_value=100,
                help="0–100, higher = review sooner"),
            "confidence_flag": st.column_config.TextColumn("Confidence", width="small"),
            "unemployment_rate": st.column_config.NumberColumn("Unemployment %", format="%.1f"),
            "youth_unemployment_rate": st.column_config.NumberColumn("Youth unemp. %", format="%.1f"),
        },
    )


def main() -> None:
    inject_css()
    st.markdown(
        '<div class="masthead">'
        '<span class="kicker">🍁 MMA 616 · Governed decision-support</span>'
        '<h1>Labour Market Stress &amp; Social Support Prioritization</h1>'
        '<div class="sub">Where labour-market distress is most elevated this cycle — '
        'a starting point for human policy review, not a program decision.</div>'
        '</div>',
        unsafe_allow_html=True,
    )

    df = load_panel()
    if df.empty:
        st.error("No data found. Run `python3 Knowledge/src/generate_synthetic_demo.py` to build "
                 "`Knowledge/synthetic/policy_triage_panel_SYNTHETIC.csv`.")
        return

    # ---- Sidebar: view mode + group + month ----
    st.sidebar.markdown("### View")
    mode = st.sidebar.radio("Rank by", ["Provinces (all ages)", "Demographic groups"])

    if mode == "Demographic groups":
        ages = [a for a in AGE_LABELS if a in df["age_group"].unique()]
        sel_age = st.sidebar.selectbox("Age group", ages,
                                       index=ages.index("15 to 24 years") if "15 to 24 years" in ages else 0,
                                       format_func=lambda a: AGE_LABELS.get(a, a))
        genders = [g for g in ("Total - Gender", "Women+", "Men+") if g in df["gender"].unique()]
        sel_gender = st.sidebar.selectbox("Gender", genders,
                                          format_func=lambda g: GENDER_LABELS.get(g, g).title())
        slice_label = group_label(sel_age, sel_gender)
    else:
        sel_age, sel_gender, slice_label = "15 years and over", "Total - Gender", None

    base = df[(df["age_group"] == sel_age) & (df["gender"] == sel_gender)].copy()
    months = sorted(base["ref_date"].dropna().unique())
    sel_month = st.sidebar.select_slider("Reference month", options=months, value=months[-1])
    st.sidebar.caption("Province-level only — the connected data has no city/CMA granularity. "
                       "Triage signal for human review.")

    snap = base[base["ref_date"] == sel_month]
    snap_focus = snap[snap["geo"] != "Canada"]          # Canada = baseline, not a focus area
    view = base                                          # full history for the chosen slice

    tabs = st.tabs(["Start here", "Why — the drivers", "Score & evidence", "Governance & caveats"])

    # 1 — Start here
    with tabs[0]:
        render_decision(snap_focus, sel_month, slice_label)

    # 2 — Why: the drivers (regional + demographic + income/housing folded in)
    with tabs[1]:
        st.subheader("Why these areas — the drivers")
        st.markdown("**Priority score by area**")
        rank = snap_focus.sort_values("policy_review_priority_score", ascending=False)
        st.bar_chart(rank.set_index("geo")["policy_review_priority_score"], color=NAVY)

        st.markdown("**Unemployment rate over time**")
        st.line_chart(view.pivot_table(index="date", columns="geo", values="unemployment_rate"))

        st.markdown("#### Demographic breakdown")
        st.caption("Unemployment by age band for the selected month — overall (15+), youth (15–24), "
                   "core (25–54), older (55+). 65+ is not published in the LFS source, so 'older' is 55+.")
        latest = df[(df["ref_date"] == sel_month) & (df["gender"] == sel_gender) & (df["geo"] != "Canada")]
        demo = (latest.pivot_table(index="geo", columns="age_group", values="unemployment_rate")
                .reindex(columns=[a for a in AGE_LABELS if a in latest["age_group"].unique()])
                .rename(columns=AGE_LABELS))
        st.dataframe(demo.sort_values(demo.columns[0], ascending=False) if len(demo.columns) else demo,
                     use_container_width=True)

        with st.expander("Income context (annual)"):
            cols = [c for c in ("geo", "income_value", "low_income_rate") if c in snap_focus]
            st.dataframe(snap_focus[cols].sort_values("income_value", ascending=False)
                         if "income_value" in snap_focus else snap_focus[cols],
                         use_container_width=True, hide_index=True)
            st.caption("Median employment income & low-income rate (LIM-AT) — annual values, "
                       "repeated across the year by join design. Low-income feeds **0.25** of the "
                       "score — the largest single factor.")
        with st.expander("Housing / affordability pressure (proxy)"):
            st.caption("Proxy = year-over-year growth in the Shelter CPI (18-10-0004-01). Not a "
                       "measured affordability or core-housing-need rate. Feeds 0.10 of the score.")
            st.line_chart(view.pivot_table(index="date", columns="geo", values="housing_pressure_proxy"))

    # 3 — Score & evidence
    with tabs[2]:
        st.subheader("How the priority score is built")
        st.markdown(
            "A transparent **0–100** triage score, each input normalised against fixed, documented "
            "anchors and weighted:\n"
            "- **Low-income rate 0.25** — the largest single factor\n"
            "- Unemployment level **0.22**, 12-mo change **0.13**\n"
            "- Employment decline vs 3-mo avg **0.10**, participation decline vs 3-mo avg **0.10**\n"
            "- Youth unemployment **0.10**, shelter-cost pressure **0.10**\n\n"
            "**Missing inputs lower confidence; they are never filled in.** Confidence = the share of "
            "weight backed by real data (≥0.85 high · 0.55–0.85 medium · <0.55 low).")
        disp = snap_focus.sort_values("policy_review_priority_score", ascending=False)[
            ["geo", "policy_review_priority_score", "score_confidence",
             "confidence_flag", "score_explanation"]].copy()
        disp["score_explanation"] = disp["score_explanation"].map(clean_expl)
        st.dataframe(disp, use_container_width=True, hide_index=True,
                     column_config={"geo": "Geography",
                                    "policy_review_priority_score": st.column_config.NumberColumn("Score", format="%.0f"),
                                    "score_confidence": st.column_config.NumberColumn("Confidence (0–1)", format="%.2f"),
                                    "confidence_flag": "Flag",
                                    "score_explanation": "Explanation"})

        st.markdown("#### Evidence panel")
        g = st.selectbox("Geography", sorted(snap_focus["geo"].unique()))
        row = snap_focus[snap_focus["geo"] == g]
        if not row.empty:
            keep = ("geo", "ref_date", "unemployment_rate", "employment_rate", "participation_rate",
                    "youth_unemployment_rate", "unemp_change", "emp_change", "part_change",
                    "low_income_rate", "housing_pressure_proxy",
                    "policy_review_priority_score", "score_confidence", "confidence_flag",
                    "missing_value_flag", "score_explanation", "source_product_id_lfs")
            ev = {k: (None if pd.isna(v) else v) for k, v in row.iloc[0].to_dict().items() if k in keep}
            if "score_explanation" in ev:
                ev["score_explanation"] = clean_expl(ev["score_explanation"])
            st.json(ev)
        st.caption("Source: Statistics Canada LFS 14-10-0287-01. See Knowledge/metadata/data_sources.md.")

    # 4 — Governance & caveats
    with tabs[3]:
        st.subheader("AI Council review")
        st.markdown(
            '<div class="verdict"><b>Verdict: 🟡 Approve with revisions</b> — reviewed 2026-06-27, '
            'awaiting human Council ratification. Until signed, every output is a <b>prototype</b> '
            'and must not inform a real program decision.</div>', unsafe_allow_html=True)
        st.markdown(
            "**The Council checked** accuracy, usefulness, trustworthiness, appropriateness, governance, "
            "scope, and evidence. **Findings & required revisions:**\n"
            "- ✅ Reframed to labour-market distress (not broad 'economic distress')\n"
            "- ✅ Employment/participation change on a 3-mo window; core (25–54) & older (55+) age drivers added\n"
            "- ✅ Confidence flags match the backed-weight share; missing inputs lower confidence, never imputed\n"
            "- ⬜ Download real low-income (11-10-0135-01) + CPI-Shelter (18-10-0004-01) tables\n"
            "- ⬜ Re-run the 5 known-answer evaluation cases\n\n"
            "Decisions logged in `00_course_artifacts/08_governance/`.")
        st.warning("Recommended decision is **Approve with revisions** and is **not yet ratified by a "
                   "human Council member** — treat every output as a draft for human review.")

        st.subheader("Caveats & limitations")
        st.markdown(
            "- **Triage, not need.** Flags areas for human review; never determines eligibility or benefits.\n"
            "- **Province-level only.** No city/CMA claims — the data has no sub-provincial granularity.\n"
            "- **Housing is a proxy.** Shelter-CPI growth ≠ measured affordability.\n"
            "- **Frequency mismatch.** Monthly LFS spine; income/population are annual context joined by year.\n"
            "- **Missing data flagged**, never imputed; it lowers confidence.\n"
            "- **Claims, not facts.** Claude-drafted summaries require analyst + AI Council review.\n\n"
            "Full detail: `Knowledge/metadata/integration_notes.md`.")


if __name__ == "__main__":
    main()
