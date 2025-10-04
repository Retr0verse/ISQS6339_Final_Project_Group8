import pandas as pd

# files
houses = "HouseTS_cleaned.csv"
public_schools = "Public_Schools_TX_Cleaned.csv"
private_schools = "Private_Schools_TX_Cleaned.csv"
crime = "crime_data_cleaned.csv"

# load
house = pd.read_csv(houses, on_bad_lines="skip", low_memory=False)
public = pd.read_csv(public_schools, on_bad_lines="skip", low_memory=False)
private = pd.read_csv(private_schools, on_bad_lines="skip", low_memory=False)
crime = pd.read_csv(crime, on_bad_lines="skip", low_memory=False)

print("house:", house.shape)
print("public:", public.shape)
print("private:", private.shape)
print("crime:", crime.shape)

# fix zip columns
def fix_zip(df):
    zip_cols = [c for c in df.columns if "zip" in c.lower()]
    if len(zip_cols) > 0:
        df = df.rename(columns={zip_cols[0]: "zipcode"})
        df["zipcode"] = df["zipcode"].astype(str).str.zfill(5)
    return df

house = fix_zip(house)
public = fix_zip(public)
private = fix_zip(private)

# Texas filter
if "STATE" in public.columns:
    public = public[public["STATE"] == "TX"]
if "STATE" in private.columns:
    private = private[private["STATE"] == "TX"]
if "State" in crime.columns:
    crime = crime[crime["State"] == "TX"]

print("public TX:", public.shape)
print("private TX:", private.shape)
print("crime TX:", crime.shape)

# merge by zipcode only (house and schools)
merged = pd.merge(house, public, on="zipcode", how="inner")
merged = pd.merge(merged, private, on="zipcode", how="inner")

# final dataset
final = pd.DataFrame()
final["zipcode"] = merged["zipcode"]

# add state
final["STATE"] = "TX"

# add city
if "city" in merged.columns:
    final["city"] = merged["city"]

# keep one column from each dataset
if "NAME_x" in merged.columns:
    final["Public_School_Name"] = merged["NAME_x"]
if "NAME_y" in merged.columns:
    final["Private_School_Name"] = merged["NAME_y"]

# add crime averages (state level)
if "Offense_Type_Violent_Crime_Record_Count" in crime.columns:
    violentTX = crime["Offense_Type_Violent_Crime_Record_Count"].mean()
else:
    violentTX = 0
if "Offense_Type_Property_Crime_Record_Count" in crime.columns:
    propertyTX = crime["Offense_Type_Property_Crime_Record_Count"].mean()
else:
    propertyTX = 0

final["Violent_Crimes_Avg_TX"] = violentTX
final["Property_Crimes_Avg_TX"] = propertyTX

# bin income
if "Per Capita Income" in merged.columns:
    final["Income_Bin"] = pd.cut(merged["Per Capita Income"],
        bins=[0, 30000, 60000, 1000000],
        labels=["Low Income", "Medium Income", "High Income"])

# bin rent
if "Median Rent" in merged.columns:
    final["Rent_Bin"] = pd.cut(merged["Median Rent"],
        bins=[0, 1000, 2000, 10000],
        labels=["Low Rent", "Medium Rent", "High Rent"])

print("final dataset:", final.shape)
final.to_csv("Merged_Dataset.csv", index=False)
print("saved Merged_Dataset.csv")
