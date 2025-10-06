import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter, MaxNLocator
from pathlib import Path

# Files
STATE_FILE = r"C:\Users\Deborah Cuellar\Desktop\isqs_6339_project\summary_state_year_schools_crime.csv"
OUTDIR = Path("outputs"); OUTDIR.mkdir(exist_ok=True)

# Sizing
plt.rcParams.update({
    "figure.figsize": (16, 9),
    "figure.dpi": 220,             
    "axes.titlesize": 18,
    "axes.labelsize": 14,
    "xtick.labelsize": 12,
    "ytick.labelsize": 12,
    "legend.fontsize": 12,
    "lines.linewidth": 2.5,
    "lines.markersize": 7,
})

# Housekeeping
def find_col(df, *cands):
    for c in cands:
        if c in df.columns:
            return c
    low = {c.lower(): c for c in df.columns}
    for c in cands:
        if c.lower() in low:
            return low[c.lower()]
    return None

def fmt_dollars(x, pos): return f"${x:,.0f}"
def fmt_thousands(x, pos): return f"{x:,.0f}"

def dual_axis_chart(df, year_col, price_col, crime_col, crime_label, outname):
    """
    Plot price (left y-axis) vs crime (right y-axis) with a FIGURE-LEVEL legend
    placed to the RIGHT. Enlarged canvas + fonts for presentation.
    """
    sub = df[[year_col, price_col, crime_col]].dropna().sort_values(year_col)
    if len(sub) < 2:
        print(f"Not enough data for {crime_label}. Skipping.")
        return

    # Big figure; reserve space on right for legend area
    fig, ax1 = plt.subplots()            )
    plt.subplots_adjust(right=0.78)      

    color1, color2 = "tab:blue", "tab:red"

    # Left axis: price
    ax1.plot(sub[year_col], sub[price_col], color=color1, marker="o", label="Median Price")
    ax1.set_xlabel("Year")
    ax1.set_ylabel("Median Price", color=color1)
    ax1.yaxis.set_major_formatter(FuncFormatter(fmt_dollars))
    ax1.xaxis.set_major_locator(MaxNLocator(integer=True))

    # Right axis: crime
    ax2 = ax1.twinx()
    ax2.plot(sub[year_col], sub[crime_col], color=color2, marker="s", label=crime_label)
    ax2.set_ylabel(f"{crime_label} Count", color=color2)
    ax2.yaxis.set_major_formatter(FuncFormatter(fmt_thousands))

    # Fix Legend
    h1, l1 = ax1.get_legend_handles_labels()
    h2, l2 = ax2.get_legend_handles_labels()
    fig.legend(
        h1 + h2, l1 + l2,
        loc="center left",
        bbox_to_anchor=(0.81, 0.5),   
        frameon=True
    )
    fig.subplots_adjust(right=0.72)
    
    plt.title(f"TX Median Price vs {crime_label}")

    # Save tight
    outpath = OUTDIR / outname
    plt.savefig(outpath, bbox_inches="tight")
    plt.close()
    print("Saved:", outpath)

# Load
state = pd.read_csv(STATE_FILE, low_memory=True)

yr_col    = find_col(state, "year", "Year", "YEAR")
price_col = find_col(state, "tx_median_price", "TX_Median_Price", "txMedianPrice")
vio_col   = find_col(state, "violent_crime_cnt", "Violent_Crime_Count", "violent_crime")
prop_col  = find_col(state, "property_crime_cnt", "Property_Crime_Count", "property_crime")

if not yr_col or not price_col:
    raise ValueError("Missing 'year' and/or 'tx_median_price' columns in the state file.")

# Final Plots
if vio_col:
    dual_axis_chart(state, yr_col, price_col, vio_col,
                    "Violent Crime", "chart_dualaxis_price_vs_violent_big.png")
else:
    print("Violent crime column not found; skipping.")

if prop_col:
    dual_axis_chart(state, yr_col, price_col, prop_col,
                    "Property Crime", "chart_dualaxis_price_vs_property_big.png")
else:
    print("Property crime column not found; skipping.")
