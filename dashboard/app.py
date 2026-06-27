#!/usr/bin/env python3
"""
app.py — Labour Market Stress & Social Support Prioritization Dashboard (Streamlit).

A governed decision-SUPPORT dashboard for a social-assistance program owner / policy
lead. It surfaces which areas and groups show elevated labour-market, income and
housing distress, so a human can decide where to focus policy review. Choosing or
delivering any intervention is the owner's downstream call.

GOVERNANCE — READ BEFORE USE
----------------------------
- This dashboard does NOT determine who needs social assistance, eligibility, or
  benefits. It produces a TRIAGE signal for human policy review only.
- Claude-generated briefing text is a CLAIM to verify, not a fact.
- Any policy interpretation is reviewed by the AI Council before it is treated as
  decision-ready (see the "AI Council review" tab).

Run:
    pip install streamlit pandas altair
    streamlit run dashboard/app.py
Reads: Knowledge/processed/policy_triage_panel_full.csv
"""
from __future__ import annotations

from pathlib import Path

import altair as alt
import pandas as pd
import streamlit as st

ROOT = Path(__file__).resolve().parents[1]
PANEL = ROOT / "Knowledge" / "processed" / "policy_triage_panel_full.csv"

ACCENT = "#1f6feb"
CONF_COLOR = {"high": "#1f7a4d", "medium": "#9a6700", "low": "#b42323"}
CONF_LABEL = {"high": "🟢 High", "medium": "🟡 Medium", "low": "🔴 Low"}

st.set_page_config(page_title="Labour Market Stress — Policy Triage",
                   page_icon="📊", layout="wide")

# --------------------------------------------------------------------------- #
# Styling
# --------------------------------------------------------------------------- #
CSS = """
<style>
.block-container {padding-top: 1.6rem; padding-bottom: 2rem; max-width: 1380px;}
header[data-testid="stHeader"] {display: none;}
[data-testid="stToolbar"] {display: none;}
#MainMenu, footer {visibility: hidden;}
.app-header {display:flex; justify-content:space-between; align-items:flex-start;
  border-bottom:1px solid #e6e9ef; padding-bottom:14px; margin-bottom:14px;}
.app-title {font-size:25px; font-weight:700; color:#16202b; margin:0; line-height:1.2;}
.app-sub {color:#5b6b7b; font-size:13.5px; margin-top:4px; max-width:760px;}
.badges {display:flex; gap:8px; flex-wrap:wrap; justify-content:flex-end;}
.badge {font-size:11px; font-weight:700; letter-spacing:.03em; padding:6px 11px;
  border-radius:7px; white-space:nowrap;}
.badge.cycle {background:#fdf2d6; color:#9a6700; border:1px solid #f0d79a;}
.badge.proto {background:#eef1f5; color:#5b6b7b; border:1px solid #d8dee6;}
.kpi {background:#fff; border:1px solid #e6e9ef; border-radius:12px; padding:15px 17px;
  height:100%; box-shadow:0 1px 2px rgba(16,24,40,.04);}
.kpi-label {font-size:10.5px; font-weight:700; letter-spacing:.05em; color:#8a97a6;
  text-transform:uppercase;}
.kpi-value {font-size:23px; font-weight:700; margin-top:6px; line-height:1.15;}
.kpi-sub {font-size:12.5px; color:#5b6b7b; margin-top:3px;}
.caveat {background:#fff8e6; border:1px solid #f0d79a; border-radius:10px;
  padding:11px 14px; font-size:12.8px; color:#5b4a1f; margin-bottom:6px;}
.briefing {background:#f4f8ff; border:1px solid #cfe0fb; border-left:4px solid #1f6feb;
  border-radius:10px; padding:14px 16px; font-size:14px; color:#1c2b3a; line-height:1.55;}
.evidence {background:#f8fafc; border:1px solid #e6e9ef; border-radius:12px; padding:6px 20px 16px;}
.ev-row {display:flex; justify-content:space-between; gap:14px; padding:9px 0;
  border-bottom:1px solid #eef1f5; font-size:13.5px;}
.ev-row:last-child {border-bottom:none;}
.ev-k {color:#5b6b7b;} .ev-v {font-weight:600; color:#16202b; text-align:right;}
.pill {display:inline-block; font-size:11px; font-weight:700; padding:2px 10px; border-radius:999px;}
.section-note {color:#7a8794; font-size:12.5px; margin-top:8px;}
</style>
"""
st.markdown(CSS, unsafe_allow_html=True)

CAVEAT = (
    "⚠️ <b>Triage signal only.</b> This dashboard flags areas for <b>human policy "
    "review</b>. It does <b>not</b> determine social-assistance need, eligibility, or "
    "benefits, and never operates on individuals. Figures are aggregate public Statistics "
    "Canada data; Claude-drafted text is a claim to verify, not a fact."
)


# --------------------------------------------------------------------------- #
# Data
# --------------------------------------------------------------------------- #
@st.cache_data
def load_panel() -> pd.DataFrame:
    """Province × month slice (Total-Gender, 15+) with core/older unemployment merged
    in as driver columns, matching the scored panel's shape."""
    s = pd.read_csv(PANEL, low_memory=False)
    tot = s[s["gender"] == "Total - Gender"]
    head = tot[tot["age_group"] == "15 years and over"].copy()
    for band, col in [("25 to 54 years", "core_unemployment_rate"),
                      ("55 years and over", "older_unemployment_rate")]:
        b = (tot[tot["age_group"] == band][["geo", "ref_date", "unemployment_rate"]]
             .rename(columns={"unemployment_rate": col}))
        head = head.merge(b, on=["geo", "ref_date"], how="left")
    head["date"] = pd.to_datetime(head["ref_date"], errors="coerce")
    return head


def kpi_card(label: str, value: str, sub: str, color: str = "#16202b") -> None:
    st.markdown(
        f'<div class="kpi"><div class="kpi-label">{label}</div>'
        f'<div class="kpi-value" style="color:{color}">{value}</div>'
        f'<div class="kpi-sub">{sub}</div></div>',
        unsafe_allow_html=True,
    )


def fmt(v, spec="{:.1f}", dash="—"):
    return dash if pd.isna(v) else spec.format(v)


# --------------------------------------------------------------------------- #
# App
# --------------------------------------------------------------------------- #
def main() -> None:
    df = load_panel()
    if df.empty:
        st.error("No panel found. Run `python3 Knowledge/src/build_demo_panel.py` to "
                 "build `Knowledge/processed/policy_triage_panel_full.csv`.")
        return

    months = sorted(df["ref_date"].dropna().unique())
    provinces = [g for g in sorted(df["geo"].unique()) if g != "Canada"]

    # ---- Sidebar ----
    st.sidebar.header("Filters")
    sel_month = st.sidebar.select_slider("Reference month", options=months,
                                         value=months[-1])
    sel_geos = st.sidebar.multiselect("Provinces", provinces, default=provinces)
    st.sidebar.caption("Geography: Canada + 10 provinces only — no city / CMA "
                       "granularity in the source table.")
    st.sidebar.divider()
    st.sidebar.caption("Source: Statistics Canada LFS 14-10-0287-01 (+ income, "
                       "low-income, CPI-Shelter and population context). "
                       "Reference month above drives every view.")

    # ---- Slices ----
    view = df[df["geo"].isin(sel_geos)]               # selected provinces, all months
    snap = view[view["ref_date"] == sel_month].copy()  # selected provinces, this month
    ranked = snap.sort_values("policy_review_priority_score", ascending=False)
    nat = df[(df["geo"] == "Canada") & (df["ref_date"] == sel_month)]
    nat_unemp = nat["unemployment_rate"].iloc[0] if not nat.empty else float("nan")

    # ---- Header ----
    st.markdown(
        f'<div class="app-header"><div>'
        f'<p class="app-title">Labour Market Stress &amp; Social Support Prioritization</p>'
        f'<p class="app-sub">Governed decision-support — a ranked shortlist of where to '
        f'focus policy review this cycle, with drivers, confidence and evidence.</p></div>'
        f'<div class="badges"><span class="badge cycle">CYCLE · {sel_month}</span>'
        f'<span class="badge proto">PROTOTYPE — NOT REVIEWED</span></div></div>',
        unsafe_allow_html=True,
    )
    st.markdown(f'<div class="caveat">{CAVEAT}</div>', unsafe_allow_html=True)

    if ranked.empty:
        st.warning("Select at least one province in the sidebar.")
        return

    # ---- KPI row ----
    top = ranked.iloc[0]
    fastest = ranked.sort_values("unemp_change", ascending=False).iloc[0]
    conf = str(top["confidence_flag"]).lower()
    backed = top.get("score_confidence", float("nan"))
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        kpi_card("Top area to focus", top["geo"],
                 f"Priority score {top['policy_review_priority_score']:.0f} · "
                 f"{conf} confidence", ACCENT)
    with c2:
        kpi_card("Fastest-rising unemployment", fastest["geo"],
                 f"{fmt(fastest['unemp_change'], '{:+.1f}')} pp vs 12-mo avg", "#b4540f")
    with c3:
        kpi_card("System confidence", conf.capitalize(),
                 f"{fmt(backed * 100, '{:.0f}')}% of score weight backed",
                 CONF_COLOR.get(conf, "#16202b"))
    with c4:
        kpi_card("National unemployment", f"{fmt(nat_unemp)}%",
                 f"Canada reference · {sel_month}", "#5b6b7b")

    if top["policy_review_priority_score"] >= 70:
        st.warning("⚠️ The top-ranked area scores ≥ 70 — **this output warrants direct "
                   "human review before any program action.**")

    st.write("")
    tabs = st.tabs([
        "① Executive summary", "② Regional stress", "③ Demographic", "④ Income context",
        "⑤ Affordability", "⑥ Priority score", "⑦ Evidence panel",
        "⑧ AI Council review", "⑨ Caveats",
    ])

    # ① Executive summary -------------------------------------------------- #
    with tabs[0]:
        st.subheader(f"Areas to focus on — {sel_month}")
        disp = ranked.copy()
        disp["conf"] = disp["confidence_flag"].astype(str).str.lower().map(CONF_LABEL)
        disp = disp[["geo", "policy_review_priority_score", "conf", "unemployment_rate",
                     "youth_unemployment_rate", "unemp_change"]]
        st.dataframe(
            disp, hide_index=True, use_container_width=True,
            column_config={
                "geo": "Area to focus on",
                "policy_review_priority_score": st.column_config.ProgressColumn(
                    "Priority score", min_value=0, max_value=100, format="%.0f"),
                "conf": "Confidence",
                "unemployment_rate": st.column_config.NumberColumn("Unemp %", format="%.1f"),
                "youth_unemployment_rate": st.column_config.NumberColumn(
                    "Youth unemp %", format="%.1f"),
                "unemp_change": st.column_config.NumberColumn("12-mo Δ pp", format="%+.1f"),
            },
        )
        st.markdown(
            f'<div class="briefing"><b>Briefing — {top["geo"]}.</b> '
            f'{top["score_explanation"]}</div>', unsafe_allow_html=True)
        st.markdown('<div class="section-note">Claude can draft this briefing from the '
                    'panel — the draft is a claim for an analyst to verify, and the AI '
                    'Council reviews any policy interpretation before it is used.</div>',
                    unsafe_allow_html=True)

    # ② Regional stress ---------------------------------------------------- #
    with tabs[1]:
        st.subheader("Regional labour-market stress")
        bar = (alt.Chart(ranked).mark_bar(cornerRadiusEnd=3).encode(
            x=alt.X("policy_review_priority_score:Q", title="Priority score (0–100)",
                    scale=alt.Scale(domain=[0, 100])),
            y=alt.Y("geo:N", sort="-x", title=None),
            color=alt.condition(alt.datum.policy_review_priority_score >= 70,
                                alt.value("#b42323"), alt.value(ACCENT)),
            tooltip=[alt.Tooltip("geo:N", title="Province"),
                     alt.Tooltip("policy_review_priority_score:Q", title="Score", format=".0f"),
                     alt.Tooltip("confidence_flag:N", title="Confidence")],
        ).properties(height=max(220, 34 * len(ranked))))
        st.altair_chart(bar, use_container_width=True)

        st.markdown("**Unemployment rate over time** (15+, seasonally adjusted)")
        line = (alt.Chart(view).mark_line().encode(
            x=alt.X("date:T", title=None),
            y=alt.Y("unemployment_rate:Q", title="Unemployment rate (%)"),
            color=alt.Color("geo:N", title="Province"),
            tooltip=["geo:N", "ref_date:N",
                     alt.Tooltip("unemployment_rate:Q", format=".1f")],
        ).properties(height=320).interactive())
        st.altair_chart(line, use_container_width=True)

    # ③ Demographic -------------------------------------------------------- #
    with tabs[2]:
        st.subheader("Demographic vulnerability")
        st.caption("Unemployment by age band — overall (15+), youth (15–24), core "
                   "(25–54), older (55+). Youth feeds the score; core/older are drivers. "
                   "**Seniors 65+ is not published in the LFS source**, so 'older' is 55+.")
        names = {"unemployment_rate": "Overall 15+", "youth_unemployment_rate": "Youth 15–24",
                 "core_unemployment_rate": "Core 25–54", "older_unemployment_rate": "Older 55+"}
        cols = [c for c in names if c in snap]
        melt = snap.melt("geo", value_vars=cols, var_name="band", value_name="rate")
        melt["band"] = melt["band"].map(names)
        order = ["Overall 15+", "Youth 15–24", "Core 25–54", "Older 55+"]
        grouped = (alt.Chart(melt).mark_bar().encode(
            x=alt.X("geo:N", title=None, axis=alt.Axis(labelAngle=-35)),
            xOffset=alt.XOffset("band:N", sort=order),
            y=alt.Y("rate:Q", title="Unemployment %"),
            color=alt.Color("band:N", sort=order, title="Age band",
                            scale=alt.Scale(range=["#9aa6b2", "#1f6feb", "#3aa76d", "#b4540f"])),
            tooltip=["geo:N", "band:N", alt.Tooltip("rate:Q", format=".1f")],
        ).properties(height=340))
        st.altair_chart(grouped, use_container_width=True)
        d = snap[["geo"] + cols].copy()
        if "youth_unemployment_rate" in d:
            d["youth_gap_pp"] = (d["youth_unemployment_rate"] - d["unemployment_rate"]).round(1)
        st.dataframe(d.sort_values("youth_unemployment_rate", ascending=False),
                     hide_index=True, use_container_width=True)
        st.markdown('<div class="section-note">Age bands are scored as drivers on the '
                    'province row. Gender (Men+/Women+) breakdowns exist in the source and '
                    'are a planned next view.</div>', unsafe_allow_html=True)

    # ④ Income context ----------------------------------------------------- #
    with tabs[3]:
        st.subheader("Income context (annual)")
        inc = snap[["geo", "income_value", "low_income_rate"]].sort_values(
            "income_value", ascending=False)
        col_a, col_b = st.columns([3, 4])
        with col_a:
            st.dataframe(
                inc, hide_index=True, use_container_width=True,
                column_config={
                    "geo": "Province",
                    "income_value": st.column_config.NumberColumn(
                        "Median employment income", format="$%d"),
                    "low_income_rate": st.column_config.NumberColumn(
                        "Low-income rate (LIM-AT) %", format="%.1f"),
                })
        with col_b:
            li = (alt.Chart(snap).mark_bar(cornerRadiusEnd=3).encode(
                x=alt.X("low_income_rate:Q", title="Low-income rate (LIM-AT) %"),
                y=alt.Y("geo:N", sort="-x", title=None),
                color=alt.value("#7a5cc0"),
                tooltip=["geo:N", alt.Tooltip("low_income_rate:Q", format=".1f")],
            ).properties(height=max(200, 30 * len(snap))))
            st.altair_chart(li, use_container_width=True)
        st.caption("Median employment income & low-income rate are annual — they repeat "
                   "across the year by join design; never compared as monthly figures.")

    # ⑤ Affordability ------------------------------------------------------ #
    with tabs[4]:
        st.subheader("Housing / affordability pressure (PROXY)")
        st.caption("Proxy = year-over-year growth in the Shelter CPI (18-10-0004-01). "
                   "**Not** a measured affordability or core-housing-need rate.")
        area = (alt.Chart(view).mark_line().encode(
            x=alt.X("date:T", title=None),
            y=alt.Y("housing_pressure_proxy:Q", title="Shelter-CPI YoY %"),
            color=alt.Color("geo:N", title="Province"),
            tooltip=["geo:N", "ref_date:N",
                     alt.Tooltip("housing_pressure_proxy:Q", format=".1f")],
        ).properties(height=340).interactive())
        st.altair_chart(area, use_container_width=True)
        st.markdown('<div class="section-note">Labelled a <b>proxy</b> everywhere; never '
                    'presented as measured affordability.</div>', unsafe_allow_html=True)

    # ⑥ Priority score ----------------------------------------------------- #
    with tabs[5]:
        st.subheader("Policy review priority score")
        st.markdown(
            "A transparent 0–100 triage score combining unemployment level & 12-mo change, "
            "employment & participation decline (vs 3-mo average), youth unemployment, "
            "low-income rate, and shelter-cost pressure — each normalised against fixed, "
            "documented anchors. **Missing inputs lower confidence; they are never filled in.**")
        weights = pd.DataFrame([
            ("Unemployment level", 0.30, "4% → 14%"),
            ("Unemployment rise vs 12-mo avg", 0.15, "0 → +3 pp"),
            ("Employment decline vs 3-mo avg", 0.10, "0 → 3 pp"),
            ("Participation decline vs 3-mo avg", 0.10, "0 → 3 pp"),
            ("Youth unemployment", 0.10, "8% → 25%"),
            ("Low-income rate", 0.15, "5% → 20%"),
            ("Housing pressure (proxy)", 0.10, "0 → 10% YoY"),
        ], columns=["Component", "Weight", "Anchors (0→1)"])
        col_w, col_s = st.columns([2, 3])
        with col_w:
            st.dataframe(weights, hide_index=True, use_container_width=True,
                         column_config={"Weight": st.column_config.NumberColumn(format="%.2f")})
        with col_s:
            st.dataframe(
                ranked[["geo", "policy_review_priority_score", "score_confidence",
                        "confidence_flag"]],
                hide_index=True, use_container_width=True,
                column_config={
                    "geo": "Province",
                    "policy_review_priority_score": st.column_config.ProgressColumn(
                        "Score", min_value=0, max_value=100, format="%.0f"),
                    "score_confidence": st.column_config.NumberColumn(
                        "Backed weight", format="%.2f"),
                    "confidence_flag": "Band",
                })
        st.caption("Confidence band: <0.55 low · 0.55–0.85 medium · ≥0.85 high. Weights "
                   "and anchors are explicit and editable so the AI Council can review them.")

    # ⑦ Evidence panel ----------------------------------------------------- #
    with tabs[6]:
        st.subheader("Evidence panel")
        g = st.selectbox("Geography", list(ranked["geo"]))
        r = snap[snap["geo"] == g].iloc[0]
        cflag = str(r["confidence_flag"]).lower()
        rows = [
            ("Reference month", str(r["ref_date"])),
            ("Priority score", f"{r['policy_review_priority_score']:.1f} / 100"),
            ("Confidence", f"{cflag} · {fmt(r['score_confidence'] * 100, '{:.0f}')}% backed"),
            ("Unemployment rate", f"{fmt(r['unemployment_rate'])}%"),
            ("Youth / Core / Older unemp.",
             f"{fmt(r['youth_unemployment_rate'])}% · {fmt(r.get('core_unemployment_rate'))}% · "
             f"{fmt(r.get('older_unemployment_rate'))}%"),
            ("Unemployment 12-mo change", f"{fmt(r['unemp_change'], '{:+.1f}')} pp"),
            ("Employment / participation Δ (3-mo)",
             f"{fmt(r['emp_change'], '{:+.1f}')} / {fmt(r['part_change'], '{:+.1f}')} pp"),
            ("Low-income rate (LIM-AT)", f"{fmt(r['low_income_rate'])}%"),
            ("Median employment income", f"${fmt(r['income_value'], '{:,.0f}')}"),
            ("Housing pressure (Shelter-CPI proxy)", f"{fmt(r['housing_pressure_proxy'])}% YoY"),
            ("Source", "Statistics Canada LFS 14-10-0287-01 (+ context tables)"),
        ]
        body = "".join(
            f'<div class="ev-row"><span class="ev-k">{k}</span>'
            f'<span class="ev-v">{v}</span></div>' for k, v in rows)
        st.markdown(f'<div class="evidence">{body}</div>', unsafe_allow_html=True)
        st.markdown(
            f'<div class="briefing" style="margin-top:12px">{r["score_explanation"]}</div>',
            unsafe_allow_html=True)

    # ⑧ AI Council review -------------------------------------------------- #
    with tabs[7]:
        st.subheader("AI Council review status")
        st.markdown(
            "- **Status:** 🟡 *Reviewed 2026-06-27 — recommended **Approve with revisions**; "
            "awaiting human Council ratification.* Remains a prototype until signed.\n"
            "- **Required revisions:** ✅ 3-mo employment/participation windows · ✅ core/older "
            "age-band drivers (65+ absent from source) · ✅ reframe to labour-market distress · "
            "✅ income, low-income & CPI-Shelter connected · ⬜ re-run the 5 known-answer cases "
            "— **4 of 5 done.**\n"
            "- The AI Council reviews accuracy, usefulness, clarity, appropriateness, "
            "governance, safety, scope, and evidence before any deployment-ready claim.")
        st.warning("The recommended decision is **Approve with revisions** and is **not yet "
                   "ratified by a human Council member** — treat every output here as a draft "
                   "for human review.")

    # ⑨ Caveats ------------------------------------------------------------ #
    with tabs[8]:
        st.subheader("Caveats & limitations")
        st.markdown(
            "- **Triage, not need.** Flags areas for human review; never determines "
            "eligibility or benefits.\n"
            "- **Proxy housing field.** Shelter-CPI growth ≠ measured affordability.\n"
            "- **Frequency mismatch.** Monthly LFS spine; income/population are annual "
            "context joined by year — never compared as monthly equivalents.\n"
            "- **Province-level geography.** Canada + 10 provinces only; no city/CMA "
            "claims, and within-province variation is masked.\n"
            "- **Age as drivers.** 65+ not published (older = 55+); age bands not yet "
            "scored as their own rows.\n"
            "- **Claims, not facts.** Claude-drafted summaries require analyst + AI Council "
            "review before any program action.")


if __name__ == "__main__":
    main()
