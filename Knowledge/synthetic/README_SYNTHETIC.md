# ⚠️ SYNTHETIC DEMONSTRATION DATA — NOT REAL STATCAN DATA

**Everything in `Knowledge/synthetic/` is a clearly-labelled prototype bridge.** It exists so the
dashboard and the gold-case output can be demonstrated end-to-end *before* the real StatCan context
tables are downloaded. It is **not** a measurement of reality.

> **Hard rules (from `CLAUDE.md`):**
> - **Never** copy these values into `Knowledge/processed/policy_triage_panel.csv` (the real,
>   governed panel). Filling a NaN in the real panel with an invented number is an **automatic fail**.
> - **Never** present any number here as StatCan-sourced or as a real finding.
> - **Never** use these scores for a program decision, demo-as-reliable, or AI Council sign-off.
> - These files are for **pipeline/dashboard prototyping and illustration only.**

The real panel was **left untouched** by this build (verified: still 6,655 rows, `low_income_rate`
and `housing_pressure_proxy` still 100% NaN). Confidence on the real panel correctly stays **medium**.

---

## What is REAL vs SIMULATED

| Column family | Status | Source |
|---|---|---|
| `employment_rate`, `participation_rate`, `unemployment_rate`, `youth_unemployment_rate`, `unemp_change`, `emp_change`, `part_change` | **REAL** | StatCan LFS **14-10-0287-01** (via `labour_force_clean.csv`), just un-filtered to per-group grain |
| `low_income_rate`, `housing_pressure_proxy`, `income_value`, `population` | **SIMULATED** | Deterministic, seeded, anchored to plausible ranges — **not measured** |
| `policy_review_priority_score`, `score_confidence`, `confidence_flag`, `missing_value_flag`, `score_explanation` | **DERIVED** | Computed by the **real** `Knowledge/src/scoring.py` (so synthetic scores match the production formula) |

Because the labour-market spine is real, only **4 of ~17 measurement columns are fabricated** — and
each is flagged. The score is real arithmetic over a partly-simulated input set, so treat the
**score itself as illustrative**, not as a real triage signal.

---

## Files

| File | Grain | Rows | Date range | Purpose |
|---|---|---:|---|---|
| `policy_triage_panel_SYNTHETIC.csv` | geo × age_group × gender × month | **36,517** | 2015-01 → 2026-05 | The analytical deliverable — **per-group scored rows** (e.g. *Youth 15–24, Alberta* as its own row), all 7 score components populated so confidence reaches **high** |
| `synthetic_statcan_long_2015_2026.csv` | geo × age × gender × indicator × data_type × month (tidy/long) | **450,433** (194,814 real LFS rate rows · 255,619 simulated) | 2015-01 → 2026-05 | The volume/raw bridge — a synthetic StatCan-style extract for load- and pipeline-testing |

### On "1,000,000 rows"
The objective does **not** require a million rows — it needs the right *grain*, not raw volume. The
honest ceiling at real StatCan granularity (11 geographies × 9 age groups × 3 genders × indicators ×
137 months, 2015–2026) is a few hundred thousand rows. Going past that would require inventing
**cities/CMAs** or **individual records** — both **automatic fails** in `CLAUDE.md`. So this build
stops at real granularity (**450,433 rows**) rather than pad with prohibited fake geography. If more
volume is genuinely needed for a stress test, extend the *time span* or add more indicators — never
the geography.

---

## Panel schema (`policy_triage_panel_SYNTHETIC.csv`)

Matches the real panel's columns, **plus** the additions needed for per-group scoring and provenance:

- **Added vs real panel:** `age_group`, `gender` (so each demographic intersection is its own row —
  this is the *target build* described under "Next build step" in `CLAUDE.md`), `is_synthetic` (always
  `True`), `dataset_provenance` (a per-row provenance string).
- **Score components & weights** are unchanged from `scoring.py`: unemployment level 0.30 ·
  unemployment change 0.15 · employment decline 0.10 · participation decline 0.10 · youth unemployment
  0.10 · low-income rate 0.15 · housing pressure 0.10.
- **Confidence bands** (unchanged): ≥0.85 high · 0.55–0.85 medium · <0.55 low. Observed values:
  `1.0` (all 7 inputs present), `0.90` (youth rate missing for that small-cell month), `0.65`
  (each series' first 12 months, where the trailing-12-month change can't be computed yet — honest,
  not a defect).
- **`score_explanation`** carries the standard triage disclaimer **plus** a suffix
  `[SYNTHETIC DEMO DATA — illustrative only, not a real measurement.]` on every row.

---

## How the 4 simulated columns are generated

Deterministic (`numpy` seed **616** — identical output every run), anchored to plausible orders of
magnitude, with mild noise. **None are measurements.**

| Column | Frequency | Method (anchored, seeded) | Observed range |
|---|---|---|---|
| `low_income_rate` (LIM-AT %) | **annual** — one value per geo×age×gender×year, repeated across the 12 months | provincial base × age × gender × mild year path, gently correlated with that group-year's *annual-mean* unemployment | 6.0 → 19.7 |
| `housing_pressure_proxy` (shelter-CPI YoY %) | monthly | national curve (low pre-2021 → ~7.8% 2022 peak → easing) + provincial offset + noise | 0.5 → 9.4 |
| `income_value` (median employment income $) | **annual** — one value per group-year, repeated across the months | provincial prime-age base × age × gender × ~2.5%/yr growth | 7,000 → 74,500 |
| `population` (persons, July-1 estimate) | **annual** — one value per group-year, repeated across the months | provincial 15+ base × age-share × gender × provincial growth | 4,500 → 33,864,300 |

> The three annual columns are now **genuinely constant within each group-year** (verified: max 1
> distinct value per geo×age×gender×year), so the "repeats across the year" label is exact. Only
> `housing_pressure_proxy` varies month-to-month (it is a monthly proxy by design).

These are **proxies/illustrations**. `housing_pressure_proxy` in particular is a *proxy for cost
pressure, not true affordability* — the same caveat as the real spec.

---

## Known design choices & caveats

- **Unadjusted, not seasonally adjusted.** The per-group panel uses **Unadjusted** LFS rates because
  they give the most complete demographic coverage (36,517 vs 28,359 complete intersection-months).
  The real headline panel uses seasonally-adjusted 15+ totals. Unadjusted detailed series for small
  provinces × narrow age bands are **volatile** (e.g. a PEI 15–19 monthly rate can spike very high) —
  this is real StatCan behaviour, but it makes some small-cell scores swing month-to-month. Read
  small-province youth cells with that volatility in mind.
- **High confidence ≠ trustworthy finding.** `confidence_flag = high` here means *the score inputs are
  complete*, but the income/housing/population inputs are **simulated** — so a "high" row is a
  demonstration of the target end-state, not a real high-confidence result.
- **Province-level only.** Same geography limit as the real project: Canada + 10 provinces, no
  cities/CMAs, no territories.
- **Youth as cross-cutting driver.** `youth_unemployment_rate` on a non-youth row is the geo×gender
  15–24 rate for that month (mirroring the real panel's design); on a youth row it is the row's own
  rate.
- **High-score escalation is embedded.** The 3,635 rows scoring ≥ 70 carry the mandatory caveat
  *"This output warrants direct human review before any program action."* in `score_explanation`
  (per `CLAUDE.md`). A dashboard/briefing layer should still surface it prominently.
- **Simulated counts are Unadjusted-only.** In the long extract, the four simulated count indicators
  (Population, Labour force, Employment, Unemployment) are derived from the **Unadjusted** rate basis
  and labelled Unadjusted, so the accounting identities (Labour force ≈ Employment + Unemployment;
  Employment ≈ Population × employment-rate) hold within the Unadjusted slice (~1% jitter). The
  *real* rate rows still carry both the genuine seasonally-adjusted and unadjusted StatCan series.
- **"eligibility / benefit" wording.** Those words appear **only** inside the mandated refusal
  disclaimer *"…not an eligibility or benefit decision."* — there is zero affirmative eligibility or
  benefit language. A blunt keyword scanner will hit them there; that is correct, required behaviour.

---

## Regenerate

```bash
python3 Knowledge/src/generate_synthetic_demo.py
```

Writes **only** to `Knowledge/synthetic/`. Reads the real `labour_force_clean.csv` and the real
`scoring.py`. Deterministic — same files every run.

---

## How this maps to the known-answer cases

- **Case 1 (Gold):** `policy_triage_panel_SYNTHETIC.csv` now contains *Youth (15–24), Alberta* (and
  every other geo × group) as its **own ranked row** with drivers, confidence, source, and the triage
  disclaimer — the gold target becomes live output **on synthetic data**. (On the *real* panel, youth
  is still only a province-row driver until the real rebuild.)
- **Case 2 (NaN ask):** still answered from the **real** panel — low-income for Manitoba is NaN there
  and must be flagged, never filled. Do not quote the synthetic value as if it were real.
- **Case 4 (Demographic breakdown):** demonstrable here (gender/age are real rows), but label outputs
  as synthetic demo until the real per-group rebuild + context downloads are done.
- **Case 5 (Out-of-scope):** unchanged — no eligibility/benefit language anywhere.
