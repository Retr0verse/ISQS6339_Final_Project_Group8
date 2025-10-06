import pandas as pd

# Files
src = r"C:\Users\Deborah Cuellar\Desktop\isqs_6339_project\House_TS_Raw\archive\HouseTS.csv"
dst_csv = r"C:\Users\Deborah Cuellar\Desktop\isqs_6339_project\House_TS_Raw\archive\HouseTS_cleaned.csv"

# Load Raw Data
df = pd.read_csv(src)

# Quick checks
print("Shape of dataset:", df.shape)
print("\nFirst 5 rows:")
print(df.head())

print("\nColumn names:")
print(df.columns.tolist())

print("\nMissing values per column:")
print(df.isnull().sum())

print("\nData types:")
print(df.dtypes)

value_counts_series = df['city'].value_counts()
print(value_counts_series)

value_counts_series = df['city_full'].value_counts()
print(value_counts_series)

# Clean Up by City by removing cities not being analyzed
df['city'] = df['city'].astype(str).str.strip().str.upper()

cities_to_drop = [
    'NY','CHI','LA','PHL','DC','PGH','BOS','MSP','DET','STL',
    'ATL','MIA','SF','SEA','PHX','CIN','BWI','RIV','TPA','DEN',
    'PDX','SAC','CLT','SD','ORL','LV'
]
df = df[~df['city'].isin(cities_to_drop)]

# Add Texas explicitly into dataset
if 'city' in df.columns:
    city_index = df.columns.get_loc('city')
    df.insert(city_index + 1, 'state', 'TX')

# Clean Up by Extra Info not needed for this analysis
cols_to_drop = ['bank', 'bus', 'hospital', 'mall', 'park', 'restaurant','school','station',
                'supermarket','Total Population','Median Age','Per Capita Income',
                'Total Families Below Poverty','Total Labor Force','Unemployed Population',
                'Total School Age Population','Total School Enrollment','Median Commute Time']
df = df.drop(columns=cols_to_drop)

# Clean Up Data Types
df["date"] = pd.to_datetime(df["date"], errors="coerce")  # convert to datetime
df["zipcode"] = df["zipcode"].astype(str)                 # keep ZIP as string
df["city"] = df["city"].astype("category")                # categorical
df["city_full"] = df["city_full"].astype("category")      # categorical


# Save Cleaned Up File
df.to_csv(dst_csv, index=False)

print(f" Cleaned CSV saved to: {dst_csv}")

# Check that rows and columns were deleted from update file
print("\nShape:", df.shape)
print("\nDtypes:\n", df.dtypes.head(20))

value_counts_series = df['city'].value_counts()
print(value_counts_series)
