"""
Quick EDA + visuals for our merged housing dataset.
Goal: produce a few clean, presentation-ready charts in ~minutes.

Outputs:
    outputs/chart_1_trend.png
    outputs/chart_2_top_zips.png
    outputs/chart_3_income_vs_homevalue.png
    outputs/chart_4_enrollment_box.png
    outputs/chart_5_unemp_vs_price.png  (optional if columns exist)

Notes:
- Keeps everything base-Anaconda friendly (pandas + matplotlib).
- Samples large frames a bit so it runs quickly on my machine.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

# --- basic setup ---
INFILE = "outputs/Merged_Dataset.csv.xz"   # merged file from /outputs in the repo
OUTDIR = Path("outputs")               # save charts here
OUTDIR.mkdir(exist_ok=True)

# --- load data ---
# low_memory=True is fine; we only touch a handful of columns for plots
df = pd.read_csv(INFILE, low_memory=True)

# tiny helper: find a column by case-insensitive match
def col(name: str):
    for c in df.columns:
        if c.lower() == name.lower():
            return c
    return None  # if it's truly not there

# map likely column names (handles minor casing differences)
sale   = col("median_sale_price")
homev  = col("Median Home Value")
income = col("Per Capita Income")
zipc   = col("zipcode") or col("ZIP")
city   = col("city_full") or col("city")
datec  = col("date")
enroll = col("ENROLLMENT_x")
unemp  = col("Unemployed Population")

# parse date if present; if not, the trend chart simply won't run
if datec is not None:
    df[datec] = pd.to_datetime(df[datec], errors="coerce")

# -----------------------------------------------------------------
# 1) Trend by city: median sale price over time (top 5 cities only)
# -----------------------------------------------------------------
if sale and datec and city:
    # pick cities with enough rows so the lines look stable
    top_cities = df[city].value_counts().head(5).index.tolist()
    sub = df.loc[df[city].isin(top_cities), [city, datec, sale]].dropna()

    # sample to keep things snappy on large data
    if len(sub) > 250_000:
        sub = sub.sample(250_000, random_state=42)

    sub["month"] = sub[datec].dt.to_period("M").dt.to_timestamp()
    trend = sub.groupby([city, "month"])[sale].median().reset_index()

    plt.figure()
    for ct in top_cities:
        s = trend[trend[city] == ct]
        plt.plot(s["month"], s[sale], label=ct)
    plt.title("Median Sale Price Over Time (Top Cities)")
    plt.xlabel("Date")
    plt.ylabel("Median Sale Price")
    plt.legend()
    plt.tight_layout()
    plt.savefig(OUTDIR / "chart_1_trend.png", dpi=160)
    plt.close()

# ---------------------------------------------------------
# 2) Top 10 ZIP codes by average median sale price (bar)
# ---------------------------------------------------------
if sale and zipc:
    sub = df[[zipc, sale]].dropna()
    if len(sub) > 400_000:
        sub = sub.sample(400_000, random_state=42)

    topz = sub.groupby(zipc)[sale].mean().sort_values(ascending=False).head(10)

    plt.figure()
    topz.plot(kind="bar")
    plt.title("Top 10 ZIP Codes by Avg Median Sale Price")
    plt.xlabel("ZIP Code")
    plt.ylabel("Avg Median Sale Price")
    plt.tight_layout()
    plt.savefig(OUTDIR / "chart_2_top_zips.png", dpi=160)
    plt.close()

# -------------------------------------------------------------------
# 3) Income vs. Home Value (scatter) + Pearson correlation annotation
# -------------------------------------------------------------------
if income and homev:
    sub = df[[income, homev]].replace([np.inf, -np.inf], np.nan).dropna()
    sub = sub[(sub[income] > 0) & (sub[homev] > 0)]
    if len(sub) > 120_000:
        sub = sub.sample(120_000, random_state=42)

    r = sub[income].corr(sub[homev])

    plt.figure()
    plt.scatter(sub[income], sub[homev], s=5, alpha=0.35)
    plt.title("Per Capita Income vs Median Home Value")
    plt.xlabel("Per Capita Income")
    plt.ylabel("Median Home Value")
    plt.text(0.02, 0.96, f"Pearson r = {r:.2f}", transform=plt.gca().transAxes)
    plt.tight_layout()
    plt.savefig(OUTDIR / "chart_3_income_vs_homevalue.png", dpi=160)
    plt.close()

# -------------------------------------------------------------
# 4) Prices by school enrollment tier (simple proxy for quality)
# -------------------------------------------------------------
if sale and enroll:
    sub = df[[sale, enroll]].dropna()
    if len(sub) > 300_000:
        sub = sub.sample(300_000, random_state=42)

    # small/medium/large bins—quick and understandable
    bins   = [-np.inf, 300, 800, np.inf]
    labels = ["Small (≤300)", "Medium (301–800)", "Large (800+)"]
    sub["tier"] = pd.cut(sub[enroll], bins=bins, labels=labels)

    # clip extreme prices so the boxplot is readable
    q99 = sub[sale].quantile(0.99)
    sub = sub[(sub[sale] > 10_000) & (sub[sale] < q99)]

    data = [sub.loc[sub["tier"] == lab, sale] for lab in labels]

    plt.figure()
    plt.boxplot(data, labels=labels, showfliers=False)
    plt.title("Median Sale Price by School Enrollment Tier")
    plt.xlabel("School Enrollment Tier")
    plt.ylabel("Median Sale Price")
    plt.tight_layout()
    plt.savefig(OUTDIR / "chart_4_enrollment_box.png", dpi=160)
    plt.close()

# -----------------------------------------------------------
# 5) Optional: Unemployed population vs sale price (scatter)
# -----------------------------------------------------------
if sale and unemp:
    sub = df[[sale, unemp]].dropna()
    if len(sub) > 120_000:
        sub = sub.sample(120_000, random_state=42)

    r2 = sub[unemp].corr(sub[sale])

    plt.figure()
    plt.scatter(sub[unemp], sub[sale], s=5, alpha=0.35)
    plt.title("Unemployed Population vs Median Sale Price")
    plt.xlabel("Unemployed Population")
    plt.ylabel("Median Sale Price")
    plt.text(0.02, 0.96, f"Pearson r = {r2:.2f}", transform=plt.gca().transAxes)
    plt.tight_layout()
    plt.savefig(OUTDIR / "chart_5_unemp_vs_price.png", dpi=160)
    plt.close()

print("Charts saved to:", OUTDIR.resolve())
