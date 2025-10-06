import pandas as pd
import numpy as np

# Files
houses = r"C:\Users\Deborah Cuellar\Desktop\isqs_6339_project\HouseTS_cleaned.csv"
public_schools = r"C:\Users\Deborah Cuellar\Desktop\isqs_6339_project\Public_Schools_TX_Cleaned.csv"
private_schools = r"C:\Users\Deborah Cuellar\Desktop\isqs_6339_project\Private_Schools_TX_Cleaned.csv"
crime_file = r"C:\Users\Deborah Cuellar\Desktop\isqs_6339_project\crime_data_cleaned.csv"  # .csv or .xlsx


# General Clean Ups
def normalize_zip_state(df: pd.DataFrame) -> pd.DataFrame:
    """Standardize 'zipcode' (5-char string) and ensure 'state' column (upper)."""
    df = df.copy()
    zip_cols = [c for c in df.columns if "zip" in c.lower()]
    if zip_cols:
        df = df.rename(columns={zip_cols[0]: "zipcode"})
        df["zipcode"] = (
            df["zipcode"].astype(str).str.extract(r"(\d+)", expand=False)
            .fillna("").str.zfill(5)
        )
    state_col = next((c for c in ["state", "STATE", "State"] if c in df.columns), None)
    if state_col:
        df["state"] = df[state_col].astype(str).str.strip().str.upper()
        if state_col != "state":
            df = df.drop(columns=[state_col])
    else:
        df["state"] = "TX"
    return df

def _first_col(df: pd.DataFrame, candidates) -> str | None:
    return next((c for c in candidates if c in df.columns), None)

def build_time_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Create 'year' (Int64), optional 'month', and 'period' (monthly if month else yearly)."""
    df = df.copy()
    year_col  = _first_col(df, ["year","Year","YEAR","report_year","Report Year"])
    month_col = _first_col(df, ["month","Month","MONTH"])
    date_col  = _first_col(df, ["date","Date","DATE"])

    if date_col is not None:
        d = pd.to_datetime(df[date_col], errors="coerce")
        df["year"]  = d.dt.year.astype("Int64")
        df["month"] = d.dt.month.astype("Int64")
    else:
        if year_col is not None:
            df["year"] = pd.to_numeric(df[year_col], errors="coerce").astype("Int64")
        if month_col is not None:
            df["month"] = pd.to_numeric(df[month_col], errors="coerce").astype("Int64")

    has_year  = ("year" in df.columns) and df["year"].notna().any()
    has_month = ("month" in df.columns) and df["month"].notna().any()

    if has_year and has_month:
        y = (df["year"].astype("float").fillna(0)).astype(int).astype(str)
        m = (df["month"].astype("float").fillna(1)).astype(int).astype(str).str.zfill(2)
        df["period"] = pd.PeriodIndex(y + "-" + m, freq="M")
    elif has_year:
        df["period"] = pd.PeriodIndex(df["year"].astype("float").fillna(0).astype(int), freq="Y")
    else:
        df["year"]   = pd.Series([pd.NA]*len(df), dtype="Int64")
        df["period"] = pd.PeriodIndex([pd.NaT]*len(df), freq="Y")
    return df

def detect_enrollment_col(df: pd.DataFrame) -> str | None:
    return _first_col(df, ["ENROLLMENT","Enrollment","enrollment","TOTAL_ENROLLMENT","Total Enrollment"])

def detect_teacher_col(df: pd.DataFrame) -> str | None:
    """
    Robustly find a teacher-count column.
    Prefers explicit FT_* names, else any column containing 'teach', else something like 'full_time'.
    """
    # 1) direct candidates
    candidates = [
        "FT_TEACHER","FT TEACHER","FT-TEACHER","FTTEACHER",
        "FULL_TIME_TEACHER","FULL TIME TEACHER","FTE_TEACHER","FTE TEACHERS",
        "Teachers_FT","Teachers FT","TEACHERS_FT"
    ]
    hit = _first_col(df, candidates)
    if hit: return hit

    # 2) any column containing 'teach'
    for c in df.columns:
        if "teach" in c.lower():
            return c

    # 3) last resort: something that looks like 'full_time'
    for c in df.columns:
        cl = c.lower()
        if "full" in cl and "time" in cl:
            return c

    return None

def to_numeric_inplace(df: pd.DataFrame, cols: list[str]):
    for c in cols:
        if c in df.columns:
            df[c] = pd.to_numeric(df[c], errors="coerce")

# Load data
read_csv_opts = dict(on_bad_lines="skip", low_memory=False)
house  = pd.read_csv(houses, **read_csv_opts)
public = pd.read_csv(public_schools, **read_csv_opts)
private = pd.read_csv(private_schools, **read_csv_opts)
crime  = pd.read_excel(crime_file) if crime_file.lower().endswith(".xlsx") else pd.read_csv(crime_file, **read_csv_opts)

print("Loaded shapes ->",
      "house:", house.shape,
      "public:", public.shape,
      "private:", private.shape,
      "crime:", crime.shape)

# Normalize year and TX filter
house  = build_time_columns(normalize_zip_state(house))
public = build_time_columns(normalize_zip_state(public))
private = build_time_columns(normalize_zip_state(private))
crime  = build_time_columns(normalize_zip_state(crime))

house  = house.query("state == 'TX'").copy()
public = public.query("state == 'TX'").copy()
private = private.query("state == 'TX'").copy()
crime  = crime.query("state == 'TX'").copy()

# Price column
price_col_candidates = [
    "price","Price","Median Home Value","median_home_value",
    "median_price","Median Home Price","Home Value Index","value"
]
price_col = next((c for c in price_col_candidates if c in house.columns), None)
if price_col is None:
    raise ValueError("Price column not found in HouseTS_cleaned.csv. "
                     "Add your true column name to price_col_candidates.")

# Schools (public vs private) Clean Up
pub_enroll = detect_enrollment_col(public)
pub_ft     = detect_teacher_col(public)
if pub_enroll is None or pub_ft is None:
    raise ValueError(f"Public schools file missing ENROLLMENT/FT_TEACHER-like column. Found: {list(public.columns)}")

pri_enroll = detect_enrollment_col(private)
pri_ft     = detect_teacher_col(private)
if pri_enroll is None or pri_ft is None:
    raise ValueError(f"Private schools file missing ENROLLMENT/FT_TEACHER-like column. Found: {list(private.columns)}")

to_numeric_inplace(public, [pub_enroll, pub_ft])
to_numeric_inplace(private, [pri_enroll, pri_ft])

public_slim  = public[["state","year", pub_enroll, pub_ft]].copy()
private_slim = private[["state","year", pri_enroll, pri_ft]].copy()

public_state_year = (
    public_slim.groupby(["state","year"], dropna=False)
    .agg(public_enrollment=(pub_enroll, "sum"),
         public_ft_teacher=(pub_ft, "sum"))
    .reset_index()
)

private_state_year = (
    private_slim.groupby(["state","year"], dropna=False)
    .agg(private_enrollment=(pri_enroll, "sum"),
         private_ft_teacher=(pri_ft, "sum"))
    .reset_index()
)

# Ratios (students per FT teacher), guard div by zero
public_state_year["public_student_teacher_ratio"] = np.where(
    public_state_year["public_ft_teacher"] > 0,
    public_state_year["public_enrollment"] / public_state_year["public_ft_teacher"],
    np.nan
)
private_state_year["private_student_teacher_ratio"] = np.where(
    private_state_year["private_ft_teacher"] > 0,
    private_state_year["private_enrollment"] / private_state_year["private_ft_teacher"],
    np.nan
)

# Crime Merge
violent_cols  = [c for c in crime.columns if "Violent" in c and "Record" in c]
property_cols = [c for c in crime.columns if "Property" in c and "Record" in c]
vcol = violent_cols[0] if violent_cols else None
pcol = property_cols[0] if property_cols else None

crime_has_year = ("year" in crime.columns and crime["year"].notna().any())
crime_keys = ["state"] + (["year"] if crime_has_year else [])

if vcol or pcol:
    keep = crime_keys + ([vcol] if vcol else []) + ([pcol] if pcol else [])
    crime_state = crime[keep].drop_duplicates().rename(
        columns={vcol: "violent_crime_cnt", pcol: "property_crime_cnt"}
    )
else:
    crime_state = None

# Save Cleaned Up File
final = house.copy()
if "city" in final.columns:
    final["city"] = final["city"].astype(str).str.strip()

# Merge state–year school totals
final = final.merge(public_state_year,  on=["state","year"], how="left")
final = final.merge(private_state_year, on=["state","year"], how="left")

# Merge state–year crime
if crime_state is not None:
    final = final.merge(crime_state, on=crime_keys, how="left")
else:
    final["violent_crime_cnt"]  = np.nan
    final["property_crime_cnt"] = np.nan

# Yearly housing trends by ZIP
is_monthly = final["period"].dtype == "period[M]"
final = final.sort_values(["zipcode","period"])

if is_monthly:
    final["price_roll12"] = final.groupby("zipcode")[price_col].transform(
        lambda s: s.rolling(12, min_periods=3).mean()
    )
    final["price_yoy_pct"] = final.groupby("zipcode")[price_col].transform(
        lambda s: s.pct_change(12)
    )
else:
    final["price_roll3y"] = final.groupby("zipcode")[price_col].transform(
        lambda s: s.rolling(3, min_periods=2).mean()
    )
    final["price_yoy_pct"] = final.groupby("zipcode")[price_col].transform(
        lambda s: s.pct_change(1)
    )


# Texas Summary
state_year = (
    final.groupby("year", observed=True).agg(
        tx_median_price=(price_col, "median"),
        public_enrollment=("public_enrollment","first"),
        private_enrollment=("private_enrollment","first"),
        public_ft_teacher=("public_ft_teacher","first"),
        private_ft_teacher=("private_ft_teacher","first"),
        public_student_teacher_ratio=("public_student_teacher_ratio","first"),
        private_student_teacher_ratio=("private_student_teacher_ratio","first"),
        violent_crime_cnt=("violent_crime_cnt","first"),
        property_crime_cnt=("property_crime_cnt","first")
    ).reset_index()
)

# Save Merged Datasets
base = r"C:\Users\Deborah Cuellar\Desktop\isqs_6339_project"
final.to_csv(fr"{base}\final_full_panel_TX.csv", index=False)
state_year.to_csv(fr"{base}\summary_state_year_schools_crime.csv", index=False)

print("Saved:")
print(" - final_full_panel_TX.csv")
print(" - summary_state_year_schools_crime.csv")

print("\nDetected school columns:")
print("  Public -> ENROLLMENT:", pub_enroll, "| FT_TEACHER-like:", pub_ft)
print("  Private -> ENROLLMENT:", pri_enroll, "| FT_TEACHER-like:", pri_ft)

print("\nPreview:")
cols_to_show = ["state","year","zipcode", price_col,
                "public_enrollment","private_enrollment",
                "public_ft_teacher","private_ft_teacher",
                "public_student_teacher_ratio","private_student_teacher_ratio",
                "violent_crime_cnt","property_crime_cnt"]
print(final[[c for c in cols_to_show if c in final.columns]].head())
