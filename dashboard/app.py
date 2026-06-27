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
  as decision-ready (governance docs live under 00_course_artifacts/08_governance/).

Design: "government data room" — calm, official, trustworthy. Four views follow a
federal analyst's path: where to look → why → can I trust it → the rules. The
landing names the area (and group) to review first; the rest is the evidence.

Run:
    pip install streamlit pandas
    streamlit run dashboard/app.py
Reads: Knowledge/synthetic/policy_triage_panel_SYNTHETIC.csv (per-group panel).
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

import pandas as pd
import streamlit as st

ROOT = Path(__file__).resolve().parents[1]
SYN_PANEL = ROOT / "Knowledge" / "synthetic" / "policy_triage_panel_SYNTHETIC.csv"

# Reuse the real scoring engine so the on-screen score breakdown matches the score exactly
sys.path.insert(0, str(ROOT / "Knowledge" / "src"))
import scoring  # noqa: E402

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

# Citations — every indicator traces to a public Statistics Canada table.
STATCAN_URL = "https://www150.statcan.gc.ca/t1/tbl1/en/tv.action?pid="
SOURCES = [
    ("14-10-0287-01", "1410028701", "Labour force characteristics (LFS)",
     "Unemployment, employment, participation & youth rates — the spine"),
    ("11-10-0135-01", "1110013501", "Low income statistics",
     "Low-income rate (LIM-AT) — the largest scoring factor"),
    ("18-10-0004-01", "1810000401", "Consumer Price Index, incl. Shelter",
     "Shelter-cost pressure proxy (year-over-year Shelter CPI)"),
    ("11-10-0239-01", "1110023901", "Income of individuals",
     "Median employment income context"),
    ("17-10-0005-01", "1710000501", "Population estimates (July 1)",
     "Population denominators & context"),
]
LFS_LINK = f"[Statistics Canada LFS 14-10-0287-01]({STATCAN_URL}1410028701)"


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
          .hero-foot a { color:#1b2a4a; text-decoration:underline; }

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

          .find-card { background:#fff; border:1px solid rgba(27,42,74,0.10);
              border-left:4px solid #1b2a4a; border-radius:12px; padding:16px 20px; margin:0 0 14px;
              box-shadow:0 1px 2px -1px rgba(27,42,74,0.08); }
          .find-eyebrow { font-size:0.72rem; font-weight:600; letter-spacing:0.06em;
              text-transform:uppercase; color:#8a94a3; margin-bottom:6px; }
          .find-head { font-size:1.08rem; font-weight:650; color:#1b2533; margin-bottom:5px;
              line-height:1.3; }
          .find-detail { font-size:0.92rem; color:#5b6675; line-height:1.55; }
          .find-detail b { color:#1b2533; }
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


def score_contributions(row: pd.Series) -> pd.DataFrame:
    """How many of the area's score points come from each factor, using the real
    scoring math (normalise vs anchors → weight → renormalise on available weight).
    The points sum to the area's policy_review_priority_score."""
    parts, avail = {}, 0.0
    for comp, col in scoring.COMPONENT_SOURCE.items():
        raw = row.get(col)
        if comp in ("emp_decline", "part_decline") and pd.notna(raw):
            raw = -raw  # a decline is stress
        n = scoring._norm(raw, *scoring.ANCHORS[comp])
        if pd.notna(n):
            parts[scoring.LABELS.get(comp, comp).title()] = scoring.WEIGHTS[comp] * n
            avail += scoring.WEIGHTS[comp]
    if avail == 0:
        return pd.DataFrame(columns=["points"])
    data = {k: 100.0 * v / avail for k, v in parts.items()}
    return pd.DataFrame({"points": data}).sort_values("points", ascending=False)


def key_findings(df: pd.DataFrame, month: str) -> list[dict]:
    """Scan every province and demographic group for the month and surface the most
    specific, notable facts. Each finding is grounded in a real panel value — nothing
    invented. Returns a list of {eyebrow, head, detail}."""
    out: list[dict] = []
    snap = df[df["ref_date"] == month]
    prov = snap[(snap["gender"] == "Total - Gender") &
                (snap["age_group"] == "15 years and over") & (snap["geo"] != "Canada")]
    canada = snap[(snap["gender"] == "Total - Gender") &
                  (snap["age_group"] == "15 years and over") & (snap["geo"] == "Canada")]
    if prov.empty:
        return out
    natl_li = canada["low_income_rate"].mean() if not canada.empty else float("nan")

    # 1 — Top priority area
    t = prov.sort_values("policy_review_priority_score", ascending=False).iloc[0]
    out.append({"eyebrow": "📍 Top area to review",
                "head": f"{t.geo} leads the priority ranking",
                "detail": f"Priority score <b>{t.policy_review_priority_score:.0f}/100</b> — "
                          "the first place to look this cycle."})

    # 2 — Highest low-income rate (the largest scoring factor)
    if prov["low_income_rate"].notna().any():
        t = prov.sort_values("low_income_rate", ascending=False).iloc[0]
        extra = (f", <b>{t.low_income_rate - natl_li:+.1f} pp</b> vs the national {natl_li:.1f}%"
                 if pd.notna(natl_li) else "")
        out.append({"eyebrow": "💲 Highest income hardship",
                    "head": f"{t.geo} has the highest low-income rate",
                    "detail": f"Low-income rate <b>{t.low_income_rate:.1f}%</b>{extra}. "
                              "Low-income is the largest single factor in the score."})

    # 3 — Lowest youth earnings (e.g. "youth in Alberta earn way lower")
    youth = snap[(snap["age_group"] == "15 to 24 years") &
                 (snap["gender"] == "Total - Gender") & (snap["geo"] != "Canada")]
    if not youth.empty and youth["income_value"].notna().any():
        lo = youth.sort_values("income_value").iloc[0]
        med = youth["income_value"].median()
        pct = abs(lo.income_value / med - 1) * 100 if med else 0
        out.append({"eyebrow": "🧑 Lowest youth earnings",
                    "head": f"Young people in {lo.geo} earn the least",
                    "detail": f"Median youth (15–24) employment income <b>${lo.income_value:,.0f}</b> — "
                              f"the lowest of any province, about <b>{pct:.0f}% below</b> the "
                              f"${med:,.0f} provincial median."})

    # 4 — Widest youth disadvantage (youth vs overall unemployment gap)
    if prov["youth_unemployment_rate"].notna().any():
        p = prov.copy()
        p["gap"] = p["youth_unemployment_rate"] - p["unemployment_rate"]
        t = p.sort_values("gap", ascending=False).iloc[0]
        out.append({"eyebrow": "⚠️ Widest youth disadvantage",
                    "head": f"Youth struggle most in {t.geo}",
                    "detail": f"Youth unemployment <b>{t.youth_unemployment_rate:.1f}%</b> vs "
                              f"{t.unemployment_rate:.1f}% overall — a <b>{t.gap:.1f} pp</b> gap."})

    # 5 — Fastest-rising unemployment
    if prov["unemp_change"].notna().any():
        t = prov.sort_values("unemp_change", ascending=False).iloc[0]
        if pd.notna(t.unemp_change) and t.unemp_change > 0:
            out.append({"eyebrow": "📈 Rising fastest",
                        "head": f"Unemployment is climbing quickest in {t.geo}",
                        "detail": f"Up <b>{t.unemp_change:+.1f} pp</b> versus its 12-month average."})

    # 6 — Steepest shelter-cost pressure
    if prov["housing_pressure_proxy"].notna().any():
        t = prov.sort_values("housing_pressure_proxy", ascending=False).iloc[0]
        out.append({"eyebrow": "🏠 Steepest housing pressure",
                    "head": f"{t.geo} faces the highest shelter-cost pressure",
                    "detail": f"Shelter CPI up <b>{t.housing_pressure_proxy:.1f}%</b> year-over-year "
                              "(a proxy, not a measured affordability rate)."})
    return out


@st.cache_data
def load_panel() -> pd.DataFrame:
    """Full per-group panel: geo × age_group × gender × month, every column populated.
    Loaded whole so the dashboard can rank provinces OR demographic groups."""
    if not SYN_PANEL.exists():
        return pd.DataFrame()
    df = pd.read_csv(SYN_PANEL, low_memory=False)
    df["date"] = pd.to_datetime(df["ref_date"], errors="coerce")
    return df


@st.cache_data
def load_geojson():
    """Canada provinces GeoJSON for the priority map (bundled, loaded locally)."""
    p = ROOT / "dashboard" / "canada_provinces.geojson"
    return json.loads(p.read_text()) if p.exists() else None


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
    lowinc = fmt(top.get("low_income_rate"), "%")
    unemp = fmt(top.get("unemployment_rate"), "%")
    youth = fmt(top.get("youth_unemployment_rate"), "%")

    who = f"{slice_label} in {geo}" if slice_label else geo
    body = (
        f"<b>This cycle ({month}), the first area to review is {who}.</b> "
        f"It carries the highest policy-review priority score, <b>{score:.0f}/100</b> — led by its "
        f"<b>low-income rate of {lowinc}</b> (the heaviest-weighted factor), alongside an "
        f"unemployment rate of <b>{unemp}</b> and youth (15–24) unemployment of <b>{youth}</b>. "
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
            <div><span class="driver-label">Low-income rate ★</span>
                 <span class="driver-val">{fmt(top.get("low_income_rate"), "%")}</span></div>
            <div><span class="driver-label">Unemployment</span>
                 <span class="driver-val">{fmt(top.get("unemployment_rate"), "%")}</span></div>
            <div><span class="driver-label">Youth (15–24)</span>
                 <span class="driver-val">{fmt(top.get("youth_unemployment_rate"), "%")}</span></div>
            <div><span class="driver-label">Employment</span>
                 <span class="driver-val">{fmt(top.get("employment_rate"), "%")}</span></div>
          </div>
          <div class="hero-foot">Source: <a href="{STATCAN_URL}1410028701" target="_blank">Statistics
          Canada LFS 14-10-0287-01</a> · Triage signal only — not an eligibility or benefit decision.</div>
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
          source — prototype, not yet ratified for program use.</div>
        </div>''',
        unsafe_allow_html=True,
    )

    # Map: provinces shaded by priority; territories shown in neutral grey
    gj = load_geojson()
    try:
        import plotly.express as px
    except Exception:
        px = None
    if gj is not None and px is not None:
        st.markdown("#### Priority by province")
        mp = ranked[["geo", "policy_review_priority_score"]].copy()
        fig = px.choropleth(
            mp, geojson=gj, locations="geo", featureidkey="properties.name",
            color="policy_review_priority_score", color_continuous_scale="RdYlGn_r",
            labels={"policy_review_priority_score": "Priority"})
        fig.update_geos(
            visible=True, showcountries=False,
            showland=True, landcolor="#dfe3e8",        # neutral land — incl. territories
            showocean=True, oceancolor="#f3f6fa",      # pale ocean
            showlakes=True, lakecolor="#f3f6fa",
            showcoastlines=True, coastlinecolor="rgba(27,42,74,0.18)",
            projection_type="conic conformal", projection_parallels=[49, 77],
            projection_rotation=dict(lon=-95),
            lataxis_range=[41, 84], lonaxis_range=[-141, -52])
        fig.update_layout(margin=dict(l=0, r=0, t=0, b=0), height=470,
                          coloraxis_colorbar=dict(title="Priority<br>score"))
        st.plotly_chart(fig, use_container_width=True, config={"staticPlot": True})
        st.caption("Provinces shaded green (lower priority) → red (higher priority); territories "
                   "are neutral grey (no data). Province-level only — no city/CMA detail.")

    st.markdown("#### Full ranked shortlist")
    st.caption("Every area in this view, highest priority first. The bar shows the 0–100 priority "
               "score; missing inputs lower confidence, never the score. Canada is a national "
               "baseline and is excluded from the focus ranking.")
    shortlist = ranked[["geo", "policy_review_priority_score", "confidence_flag",
                        "low_income_rate", "unemployment_rate"]].copy()
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
            "low_income_rate": st.column_config.NumberColumn("Low-income % ★", format="%.1f",
                help="Largest factor in the score"),
            "unemployment_rate": st.column_config.NumberColumn("Unemployment %", format="%.1f"),
        },
    )
    st.caption("📑 Full data sources with clickable Statistics Canada links are in the "
               "**Sources** tab.")


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

    tabs = st.tabs(["Start here", "Key findings", "Why — the drivers",
                    "Score & evidence", "Sources"])

    # 1 — Start here
    with tabs[0]:
        render_decision(snap_focus, sel_month, slice_label)

    # 2 — Key findings (auto-generated, scans all groups for the selected month)
    with tabs[1]:
        st.subheader(f"Key findings — {sel_month}")
        st.caption("Auto-generated from the full panel — every province, age band and gender — for "
                   "the selected month. Each finding is a claim to verify against the Statistics "
                   "Canada source, not a program decision.")
        findings = key_findings(df, sel_month)
        if not findings:
            st.info("No findings for this month.")
        else:
            cols = st.columns(2)
            for i, f in enumerate(findings):
                with cols[i % 2]:
                    st.markdown(
                        f'<div class="find-card">'
                        f'<div class="find-eyebrow">{f["eyebrow"]}</div>'
                        f'<div class="find-head">{f["head"]}</div>'
                        f'<div class="find-detail">{f["detail"]}</div>'
                        f'</div>', unsafe_allow_html=True)

    # 3 — Why: the drivers (income lead, then labour, demographic, housing — all open)
    with tabs[2]:
        st.subheader("Why these areas — the drivers")

        st.markdown("**Low-income rate by area ★** — the largest factor in the score")
        inc_rank = snap_focus.sort_values("low_income_rate", ascending=False)
        st.bar_chart(inc_rank.set_index("geo")["low_income_rate"], color=NAVY)

        st.markdown("**Unemployment rate over time**")
        st.line_chart(view.pivot_table(index="date", columns="geo", values="unemployment_rate"))

        st.markdown("**Housing / affordability pressure over time (proxy)**")
        st.caption("Proxy = year-over-year growth in the Shelter CPI (18-10-0004-01). Not a measured "
                   "affordability or core-housing-need rate. Feeds 0.10 of the score.")
        st.line_chart(view.pivot_table(index="date", columns="geo", values="housing_pressure_proxy"))

        st.markdown("#### Demographic breakdown")
        st.caption("Unemployment by age band for the selected month — overall (15+), youth (15–24), "
                   "core (25–54), older (55+). 65+ is not published in the LFS source, so 'older' is 55+.")
        latest = df[(df["ref_date"] == sel_month) & (df["gender"] == sel_gender) & (df["geo"] != "Canada")]
        demo = (latest.pivot_table(index="geo", columns="age_group", values="unemployment_rate")
                .reindex(columns=[a for a in AGE_LABELS if a in latest["age_group"].unique()])
                .rename(columns=AGE_LABELS))
        st.dataframe(demo.sort_values(demo.columns[0], ascending=False) if len(demo.columns) else demo,
                     use_container_width=True)

        st.markdown("#### Income detail (annual)")
        cols = [c for c in ("geo", "income_value", "low_income_rate") if c in snap_focus]
        st.dataframe(
            snap_focus[cols].sort_values("low_income_rate", ascending=False)
            if "low_income_rate" in snap_focus else snap_focus[cols],
            use_container_width=True, hide_index=True,
            column_config={
                "geo": st.column_config.TextColumn("Geography", width="medium"),
                "income_value": st.column_config.NumberColumn("Median income $", format="%.0f"),
                "low_income_rate": st.column_config.NumberColumn("Low-income % ★", format="%.1f"),
            })
        st.caption("Median employment income & low-income rate (LIM-AT) — annual values, repeated "
                   "across the year by join design. Low-income feeds 0.25 of the score (the largest factor).")

    # 4 — Score & evidence
    with tabs[3]:
        st.subheader("The score & the evidence behind it")
        st.caption("A 0–100 triage score. **Low-income rate is the largest factor (0.25)**, then "
                   "unemployment level (0.22) & 12-mo change (0.13), employment & participation "
                   "decline (0.10 each), youth unemployment (0.10), housing-cost pressure (0.10). "
                   "Missing inputs lower confidence — they are never filled in.")

        # ---- Break one area down: the chart that explains the score ----
        st.markdown("#### What builds an area's score")
        g = st.selectbox("Area to break down", sorted(snap_focus["geo"].unique()))
        row = snap_focus[snap_focus["geo"] == g]
        if not row.empty:
            r = row.iloc[0]
            c1, c2, c3, c4 = st.columns(4)
            c1.metric("Priority score", f"{r['policy_review_priority_score']:.0f}/100")
            c2.metric("Low-income rate ★", fmt(r.get("low_income_rate"), "%"))
            c3.metric("Unemployment", fmt(r.get("unemployment_rate"), "%"))
            c4.metric("Youth unemp.", fmt(r.get("youth_unemployment_rate"), "%"))

            contrib = score_contributions(r)
            if not contrib.empty:
                st.markdown(f"**Where {g}'s {r['policy_review_priority_score']:.0f} points come from** "
                            "— each factor's contribution to the score:")
                st.bar_chart(contrib, y="points", horizontal=True, color=NAVY)
            conf = r.get("score_confidence")
            conf_pct = f"{conf:.0%}" if pd.notna(conf) else "—"
            st.caption(
                f"Confidence: **{str(r.get('confidence_flag', '—')).capitalize()}** "
                f"({conf_pct} of the score's weight backed by data). "
                f"Source: {LFS_LINK} (province-level). "
                f"Triage signal only — not an eligibility or benefit decision.")

        # ---- Compare every area (with in-cell bars, not a bland grid) ----
        st.divider()
        st.markdown("#### Compare every area")
        tbl = snap_focus.sort_values("policy_review_priority_score", ascending=False)[
            ["geo", "policy_review_priority_score", "confidence_flag",
             "low_income_rate", "unemployment_rate", "youth_unemployment_rate"]].copy()
        tbl["confidence_flag"] = tbl["confidence_flag"].astype(str).str.capitalize()
        li_max = float(tbl["low_income_rate"].max()) if tbl["low_income_rate"].notna().any() else 25.0
        un_max = float(tbl["unemployment_rate"].max()) if tbl["unemployment_rate"].notna().any() else 20.0
        st.dataframe(tbl, use_container_width=True, hide_index=True,
            column_config={
                "geo": st.column_config.TextColumn("Geography", width="medium"),
                "policy_review_priority_score": st.column_config.ProgressColumn(
                    "Priority score", format="%.0f", min_value=0, max_value=100),
                "confidence_flag": st.column_config.TextColumn("Confidence", width="small"),
                "low_income_rate": st.column_config.ProgressColumn(
                    "Low-income % ★", format="%.1f", min_value=0, max_value=li_max),
                "unemployment_rate": st.column_config.ProgressColumn(
                    "Unemployment %", format="%.1f", min_value=0, max_value=un_max),
                "youth_unemployment_rate": st.column_config.NumberColumn("Youth unemp. %", format="%.1f"),
            })

    # 5 — Sources (citations + key caveats)
    with tabs[4]:
        st.subheader("Data sources & citations")
        st.caption("Every indicator traces to an aggregate, public Statistics Canada table. "
                   "Click a product ID to open the source table on statcan.gc.ca.")
        src_lines = ["| Statistics Canada table | What it provides in this dashboard |", "|---|---|"]
        for pid_disp, pid, title, role in SOURCES:
            src_lines.append(f"| [**{pid_disp}** · {title}]({STATCAN_URL}{pid}) | {role} |")
        st.markdown("\n".join(src_lines))
        st.caption("Aggregate public data only — no individual records, no city/CMA detail. "
                   "Triage signal for human review — not an eligibility or benefit decision. "
                   "Full source notes: `Knowledge/metadata/data_sources.md`.")


if __name__ == "__main__":
    main()
