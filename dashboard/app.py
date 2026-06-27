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
                          "the first place to look this cycle.",
                "geo": t.geo, "metric": "policy_review_priority_score",
                "metric_label": "Priority score (0–100)",
                "age": "15 years and over", "gender": "Total - Gender"})

    # 2 — Highest low-income rate (the largest scoring factor)
    if prov["low_income_rate"].notna().any():
        t = prov.sort_values("low_income_rate", ascending=False).iloc[0]
        extra = (f", <b>{t.low_income_rate - natl_li:+.1f} pp</b> vs the national {natl_li:.1f}%"
                 if pd.notna(natl_li) else "")
        out.append({"eyebrow": "💲 Highest income hardship",
                    "head": f"{t.geo} has the highest low-income rate",
                    "detail": f"Low-income rate <b>{t.low_income_rate:.1f}%</b>{extra}. "
                              "Low-income is the largest single factor in the score.",
                    "geo": t.geo, "metric": "low_income_rate",
                    "metric_label": "Low-income rate (%)",
                    "age": "15 years and over", "gender": "Total - Gender"})

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
                              f"${med:,.0f} provincial median.",
                    "geo": lo.geo, "metric": "income_value",
                    "metric_label": "Median youth (15–24) income ($)",
                    "age": "15 to 24 years", "gender": "Total - Gender"})

    # 4 — Widest youth disadvantage (youth vs overall unemployment gap)
    if prov["youth_unemployment_rate"].notna().any():
        p = prov.copy()
        p["gap"] = p["youth_unemployment_rate"] - p["unemployment_rate"]
        t = p.sort_values("gap", ascending=False).iloc[0]
        out.append({"eyebrow": "⚠️ Widest youth disadvantage",
                    "head": f"Youth struggle most in {t.geo}",
                    "detail": f"Youth unemployment <b>{t.youth_unemployment_rate:.1f}%</b> vs "
                              f"{t.unemployment_rate:.1f}% overall — a <b>{t.gap:.1f} pp</b> gap.",
                    "geo": t.geo, "metric": "youth_unemployment_rate",
                    "metric_label": "Youth (15–24) unemployment (%)",
                    "age": "15 years and over", "gender": "Total - Gender"})

    # 5 — Fastest-rising unemployment
    if prov["unemp_change"].notna().any():
        t = prov.sort_values("unemp_change", ascending=False).iloc[0]
        if pd.notna(t.unemp_change) and t.unemp_change > 0:
            out.append({"eyebrow": "📈 Rising fastest",
                        "head": f"Unemployment is climbing quickest in {t.geo}",
                        "detail": f"Up <b>{t.unemp_change:+.1f} pp</b> versus its 12-month average.",
                        "geo": t.geo, "metric": "unemp_change",
                        "metric_label": "Unemployment change vs 12-mo avg (pp)",
                        "age": "15 years and over", "gender": "Total - Gender"})

    # 6 — Steepest shelter-cost pressure
    if prov["housing_pressure_proxy"].notna().any():
        t = prov.sort_values("housing_pressure_proxy", ascending=False).iloc[0]
        out.append({"eyebrow": "🏠 Steepest housing pressure",
                    "head": f"{t.geo} faces the highest shelter-cost pressure",
                    "detail": f"Shelter CPI up <b>{t.housing_pressure_proxy:.1f}%</b> year-over-year "
                              "(a proxy, not a measured affordability rate).",
                    "geo": t.geo, "metric": "housing_pressure_proxy",
                    "metric_label": "Shelter CPI, year-over-year (%)",
                    "age": "15 years and over", "gender": "Total - Gender"})
    return out


def render_finding_detail(df: pd.DataFrame, month: str, f: dict) -> None:
    """Drill-down for a clicked finding: a purpose-built chart that reveals an
    insight for this specific topic, plus a placeholder for related articles."""
    try:
        import plotly.express as px
    except Exception:
        px = None

    st.subheader(f"🔎 {f['head']}")
    st.markdown(f'<div class="find-detail">{f["detail"]}</div>', unsafe_allow_html=True)

    metric, geo = f.get("metric"), f.get("geo")
    snap = df[(df["ref_date"] == month) & (df["geo"] != "Canada")]
    prov = snap[(snap["gender"] == "Total - Gender") & (snap["age_group"] == "15 years and over")]
    recent = df[df["date"] >= (df["date"].max() - pd.DateOffset(months=36))]
    HI, OTHER = "#c0544b", "#9aa6b5"

    # ---- Tailored insight per finding ----
    if metric == "policy_review_priority_score":
        row = prov[prov["geo"] == geo]
        if not row.empty:
            contrib = score_contributions(row.iloc[0])
            st.markdown(f"**What builds {geo}'s score** — each factor's point contribution")
            st.bar_chart(contrib, y="points", horizontal=True, color=NAVY)
        hist = recent[(recent["gender"] == "Total - Gender") &
                      (recent["age_group"] == "15 years and over") &
                      (recent["geo"].isin([geo, "Canada"]))]
        piv = hist.pivot_table(index="date", columns="geo", values="policy_review_priority_score")
        st.markdown(f"**{geo} vs Canada — priority score over the last 3 years**")
        st.line_chart(piv)
        st.caption("How this area's overall stress compares to the national baseline, and where it's heading.")

    elif metric == "low_income_rate" and px is not None:
        d = prov.dropna(subset=["low_income_rate", "unemployment_rate"]).copy()
        d["Province"] = d["geo"].where(d["geo"] == geo, "Other provinces")
        st.markdown("**Does income hardship track joblessness?** Low-income rate vs unemployment, by province")
        fig = px.scatter(d, x="low_income_rate", y="unemployment_rate", text="geo", color="Province",
                         color_discrete_map={geo: HI, "Other provinces": OTHER},
                         labels={"low_income_rate": "Low-income rate (%)",
                                 "unemployment_rate": "Unemployment rate (%)"})
        fig.update_traces(textposition="top center", marker=dict(size=12))
        fig.update_layout(showlegend=False, height=460, margin=dict(l=0, r=0, t=10, b=0))
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
        st.caption(f"Each dot is a province; {geo} is highlighted. Top-right = both high unemployment "
                   "and high income hardship — the areas under the most combined pressure.")

    elif metric == "income_value":
        youth = snap[(snap["age_group"] == "15 to 24 years") & (snap["gender"] == "Total - Gender")]
        core = snap[(snap["age_group"] == "25 to 54 years") & (snap["gender"] == "Total - Gender")]
        m = (youth[["geo", "income_value"]].rename(columns={"income_value": "Youth (15–24)"})
             .merge(core[["geo", "income_value"]].rename(columns={"income_value": "Prime-age (25–54)"}), on="geo")
             .set_index("geo").sort_values("Youth (15–24)"))
        st.markdown("**The youth earnings penalty** — youth vs prime-age median income, by province")
        st.bar_chart(m, stack=False)
        if geo in m.index:
            ratio = m.loc[geo, "Youth (15–24)"] / m.loc[geo, "Prime-age (25–54)"] * 100
            st.caption(f"In {geo}, youth earn about **{ratio:.0f}%** of prime-age (25–54) median income — "
                       "the gap between the bars is the earnings penalty young workers face.")

    elif metric == "youth_unemployment_rate":
        d = (prov[["geo", "youth_unemployment_rate", "unemployment_rate"]].dropna()
             .rename(columns={"youth_unemployment_rate": "Youth (15–24)", "unemployment_rate": "Overall (15+)"})
             .set_index("geo").sort_values("Youth (15–24)", ascending=False))
        st.markdown("**Youth vs overall unemployment, by province** — the gap is the youth disadvantage")
        st.bar_chart(d, stack=False)
        st.caption(f"Where the youth bar towers over the overall bar, young people are hit hardest. "
                   f"{geo} shows the widest gap this month.")

    elif metric in ("unemp_change", "housing_pressure_proxy"):
        col = "unemployment_rate" if metric == "unemp_change" else "housing_pressure_proxy"
        what = "Unemployment rate" if metric == "unemp_change" else "Shelter-cost pressure (YoY %)"
        hist = recent[(recent["gender"] == "Total - Gender") &
                      (recent["age_group"] == "15 years and over") &
                      (recent["geo"].isin([geo, "Canada"]))]
        piv = hist.pivot_table(index="date", columns="geo", values=col)
        st.markdown(f"**{what}: {geo} vs Canada — last 3 years**")
        st.line_chart(piv)
        st.caption(f"The trajectory matters as much as the level — watch whether {geo} is pulling "
                   "away from the national line.")

    else:
        series = prov.set_index("geo")[metric].dropna().sort_values(ascending=False)
        if not series.empty:
            st.bar_chart(series, color=NAVY, horizontal=True)

    st.markdown("#### 📰 Related public articles")
    st.info("Placeholder — public articles, news coverage and reports about this topic will be "
            "linked here. (Coming soon.)")


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

    # 2 — Key findings (auto-generated; Explore opens a detail view)
    with tabs[1]:
        findings = key_findings(df, sel_month)
        sel = st.session_state.get("sel_finding")

        if sel is not None and sel < len(findings):
            # ---- Detail "page" for the selected finding ----
            if st.button("← Back to all findings"):
                st.session_state["sel_finding"] = None
                st.rerun()
            render_finding_detail(df, sel_month, findings[sel])
        else:
            # ---- The findings list ----
            st.subheader(f"Key findings — {sel_month}")
            st.caption("Auto-generated from the full panel — every province, age band and gender — for "
                       "the selected month. Click **Explore** on a finding to open its data, charts "
                       "and related articles. Each finding is a claim to verify against the source.")
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
                        if st.button("Explore →", key=f"explore_{i}", use_container_width=True):
                            st.session_state["sel_finding"] = i
                            st.rerun()

    # 3 — Why: the drivers (income lead, then labour, demographic, housing — all open)
    with tabs[2]:
        st.subheader("Why these areas — the drivers")
        st.caption("Pick a driver to see which provinces are worse than the national average, and how "
                   "the worst are trending. For the overall ranking see **Start here**.")
        try:
            import plotly.express as px
        except Exception:
            px = None

        DRIVERS = {"Unemployment rate": "unemployment_rate",
                   "Low-income rate ★ (largest factor)": "low_income_rate",
                   "Youth unemployment": "youth_unemployment_rate",
                   "Housing-cost pressure (proxy)": "housing_pressure_proxy"}
        dlabel = st.selectbox("Driver to explore", list(DRIVERS))
        col = DRIVERS[dlabel]
        short = dlabel.split(" (")[0].replace(" ★", "")

        natl_row = snap[snap["geo"] == "Canada"]
        natl = float(natl_row[col].iloc[0]) if (not natl_row.empty and natl_row[col].notna().any()) else None
        pcur = snap[snap["geo"] != "Canada"].dropna(subset=[col]).copy()

        # 1) Gap vs national — who's worse than average, ranked and colour-coded
        if px is not None and not pcur.empty and natl is not None:
            pcur["gap"] = pcur[col] - natl
            pcur = pcur.sort_values("gap")
            pcur["Status"] = pcur["gap"].apply(lambda g: "Worse than national" if g > 0 else "Better than national")
            st.markdown(f"**{short}: gap vs the national average of {natl:.1f}** — {sel_month}")
            fig = px.bar(pcur, x="gap", y="geo", orientation="h", color="Status",
                         color_discrete_map={"Worse than national": "#c0544b",
                                             "Better than national": "#3d8a5d"},
                         labels={"gap": f"Difference from national {short.lower()}", "geo": ""})
            fig.update_layout(height=430, margin=dict(l=0, r=0, t=10, b=0), legend_title_text="")
            st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
            st.caption("Why it matters: provinces above the national line are where the same federal "
                       "program reaches people facing tougher conditions than the country overall — the "
                       "natural first call on limited review capacity.")
        elif not pcur.empty:
            st.bar_chart(pcur.set_index("geo")[col], horizontal=True, color=NAVY)

        # 2) Recent trend — only the worst provinces + Canada, so it's readable
        top_geos = pcur.sort_values(col, ascending=False)["geo"].head(4).tolist()
        rec = view[(view["date"] >= (view["date"].max() - pd.DateOffset(months=24))) &
                   (view["geo"].isin(top_geos + ["Canada"]))]
        if px is not None and not rec.empty:
            st.markdown(f"**{short}: last 24 months — the four highest provinces vs Canada**")
            fig2 = px.line(rec, x="date", y=col, color="geo",
                           labels={col: short, "date": "", "geo": ""})
            fig2.update_layout(height=380, margin=dict(l=0, r=0, t=10, b=0))
            st.plotly_chart(fig2, use_container_width=True, config={"displayModeBar": False})
            st.caption("Why it matters: a province climbing toward the leaders deserves attention "
                       "before it tops the table — acting on the trend is cheaper than reacting after "
                       "the peak. (Top few provinces plus Canada, to stay readable.)")
        if col == "housing_pressure_proxy":
            st.caption("Housing pressure = YoY growth in the Shelter CPI (18-10-0004-01) — a proxy, "
                       "not a measured affordability rate.")

        st.markdown("#### Unemployment by age band")
        st.caption("Overall (15+), youth (15–24), core (25–54), older (55+) for the selected month — "
                   "the one place to compare age groups. 65+ is not published in the LFS source, so "
                   "'older' is 55+.")
        latest = df[(df["ref_date"] == sel_month) & (df["gender"] == sel_gender) & (df["geo"] != "Canada")]
        demo = (latest.pivot_table(index="geo", columns="age_group", values="unemployment_rate")
                .reindex(columns=[a for a in AGE_LABELS if a in latest["age_group"].unique()])
                .rename(columns=AGE_LABELS))
        st.dataframe(demo.sort_values(demo.columns[0], ascending=False) if len(demo.columns) else demo,
                     use_container_width=True)
        st.caption("Why it matters: when one band towers over the others, a province-wide response "
                   "misses the mark — the pressure sits in a group, not the whole population.")

        # --- Where distress is rising vs easing (trajectory) ---
        st.markdown("#### Where distress is rising vs easing")
        ch = snap[snap["geo"] != "Canada"].dropna(subset=["unemp_change"]).copy()
        if px is not None and not ch.empty:
            ch["Trend"] = ch["unemp_change"].apply(lambda g: "Rising" if g > 0 else "Easing")
            ch = ch.sort_values("unemp_change")
            figr = px.bar(ch, x="unemp_change", y="geo", orientation="h", color="Trend",
                          color_discrete_map={"Rising": "#c0544b", "Easing": "#3d8a5d"},
                          labels={"unemp_change": "Unemployment change vs 12-mo avg (pp)", "geo": ""})
            figr.update_layout(height=420, margin=dict(l=0, r=0, t=10, b=0), legend_title_text="")
            st.plotly_chart(figr, use_container_width=True, config={"displayModeBar": False})
            st.caption("Why it matters: today's worst area isn't always next cycle's. The red provinces "
                       "are deteriorating fastest, so they're most likely to overtake the current "
                       "ranking — and cheaper to address now than after they peak.")

        # --- What's driving each province's score (the mix) ---
        st.markdown("#### What's driving each province's score")
        rows = []
        for _, r in snap_focus.iterrows():
            c = score_contributions(r)
            if not c.empty:
                d = c["points"].to_dict()
                d["geo"] = r["geo"]
                rows.append(d)
        if rows:
            comp = pd.DataFrame(rows).set_index("geo").fillna(0)
            comp["__t"] = comp.sum(axis=1)
            comp = comp.sort_values("__t").drop(columns="__t")
            st.bar_chart(comp, horizontal=True, stack=True)
            st.caption("Why it matters: two provinces can reach the same score for opposite reasons — "
                       "one income-led, one jobs-led. The mix points to which lever (income supports vs "
                       "employment programs) is most likely to help.")

        # --- Gender gap within areas ---
        st.markdown("#### The gender gap (unemployment, 15+)")
        gcur = df[(df["ref_date"] == sel_month) & (df["age_group"] == "15 years and over") &
                  (df["geo"] != "Canada")]
        women = (gcur[gcur["gender"] == "Women+"][["geo", "unemployment_rate"]]
                 .rename(columns={"unemployment_rate": "Women+"}))
        men = (gcur[gcur["gender"] == "Men+"][["geo", "unemployment_rate"]]
               .rename(columns={"unemployment_rate": "Men+"}))
        gg = women.merge(men, on="geo").set_index("geo")
        if not gg.empty:
            gg["__g"] = (gg["Women+"] - gg["Men+"]).abs()
            gg = gg.sort_values("__g", ascending=False).drop(columns="__g")
            st.bar_chart(gg, horizontal=True, stack=False)
            st.caption("Why it matters: a province's headline rate can hide that men or women carry most "
                       "of the burden. Where the two bars diverge, who you reach inside the area matters "
                       "more than the average.")

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

        st.caption("Looking for the full province ranking? It's on the **Start here** tab — this page "
                   "explains how any one area's score is built.")

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
