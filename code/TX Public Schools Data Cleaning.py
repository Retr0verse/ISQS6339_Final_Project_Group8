import pandas as pd

public = pd.read_csv("Public_Schools.csv")
print(public.head())

# filtereing states to only show TX

public = public[public["STATE"] == "TX"]


# removing columns that mainly have "Not Availiable" values and unnecessary to our project

public_drop = ["X", "Y", "FID","ADDRESS2", "VAL_METHOD", "TELEPHONE", "ZIP4", "LATITUDE", "LONGITUDE", "SOURCE",
               "WEBSITE", "SOURCE_DAT", "SHELTER_ID"]
public = public.drop(columns=public_drop)


# change the VAL_DATE column to only show the year

public["YEAR"] = pd.to_datetime(public["VAL_DATE"]).dt.year
public = public.drop(columns=["VAL_DATE"])
print(public[["YEAR"]].head())


# cleaning up column names and removing possible whitespaces

public = public.rename(columns={"LEVEL_": "LEVEL"})
public.columns = public.columns.str.strip()

public.info()

# changing columns to be appropriate datatypes

string_cols = ["NCESID", "ZIP", "COUNTYFIPS","NAME", "ADDRESS", "CITY", "COUNTY", "COUNTRY","NAICS_DESC", "START_GRAD", "END_GRADE"]
public[string_cols] = public[string_cols].astype("string")

cate_cols = ["TYPE", "STATUS", "NAICS_CODE", "STATE", "LEVEL"]
public[cate_cols] = public[cate_cols].astype("category")

public["YEAR"] = public["YEAR"].astype("int16")

public.info()


# exporting cleaned dataset
public.to_csv("Public_Schools_TX_Cleaned.csv")
