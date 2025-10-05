
import pandas as pd


private = pd.read_csv("Private_Schools.csv", delimiter=";")

private.head()


# filtereing states to only show TX

private = private[private["STATE"] == "TX"]


# removing columns that mainly have "Not Availiable" values and unnecessary to our project

private_drop = ["Geo Point", "Geo Shape", "FID_1", "OBJECTID", "ZIP4", "TELEPHONE","VAL_METHOD", "WEBSITE", "SHELTER_ID", "COUNTRY", "LATITUDE", "LONGITUDE",
               "SOURCE", "SOURCEDATE"]
private = private.drop(columns=private_drop)



# change the VAL_DATE column to only show the year

private["YEAR"] = pd.to_datetime(private["VAL_DATE"]).dt.year
private = private.drop(columns=["VAL_DATE"])
print(private[["YEAR"]].head())


# cleaning up column names and removing possible whitespaces

private = private.rename(columns={"LEVEL_": "LEVEL"})
private.columns = private.columns.str.strip()

private.info()


# changing columns to appropriate data types

string_cols = ["NCESID", "ZIP", "COUNTYFIPS","NAME", "ADDRESS", "CITY", "COUNTY","NAICS_DESC", "START_GRAD", "END_GRADE"]
private[string_cols] = private[string_cols].astype("string")

cate_cols = ["TYPE", "STATUS", "NAICS_CODE", "STATE", "LEVEL"]
private[cate_cols] = private[cate_cols].astype("category")

private["YEAR"] = private["YEAR"].astype("int16")

private.info()


# exporting cleaned dataset
private.to_csv("Private_Schools_TX_Cleaned.csv")
