{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 1,
   "id": "6cebf078-516a-4dc3-99b0-18798a14ae48",
   "metadata": {},
   "outputs": [],
   "source": [
    "import pandas as pd"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 2,
   "id": "73c302fc-d63e-4e00-80da-a714f5268f70",
   "metadata": {},
   "outputs": [
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "/var/folders/6h/0xwz27g56m3d0bx7zm77q6wr0000gn/T/ipykernel_31609/1366813514.py:1: DtypeWarning: Columns (16) have mixed types. Specify dtype option on import or set low_memory=False.\n",
      "  public = pd.read_csv(\"Public_Schools.csv\")\n"
     ]
    }
   ],
   "source": [
    "public = pd.read_csv(\"Public_Schools.csv\")"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 3,
   "id": "327d9a81-f4d6-4e87-8f9a-dbcec83e8c2a",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "           X          Y  FID       NCESID                        NAME  \\\n",
      "0 -88.028074  32.791868    1  10168000578       PARAMOUNT JR HIGH SCH   \n",
      "1 -87.918717  32.846392    2  10168000864  PETER J KIRKSEY CAREER CTR   \n",
      "2 -87.893147  32.838000    3  10168001452           EUTAW PRIMARY SCH   \n",
      "3 -87.877214  32.833911    4  10168001520           CARVER MIDDLE SCH   \n",
      "4 -87.620561  32.998976    5  10171000588            HALE CO HIGH SCH   \n",
      "\n",
      "               ADDRESS       ADDRESS2        CITY STATE    ZIP  ...  \\\n",
      "0               HWY 20  NOT AVAILABLE     BOLIGEE    AL  35443  ...   \n",
      "1    836 COUNTY RD 131  NOT AVAILABLE       EUTAW    AL  35462  ...   \n",
      "2  212 EUTAW AVE SOUTH  NOT AVAILABLE       EUTAW    AL  35462  ...   \n",
      "3   527 GREENSBORO AVE  NOT AVAILABLE       EUTAW    AL  35462  ...   \n",
      "4       50 WILDCAT WAY  NOT AVAILABLE  MOUNDVILLE    AL  35474  ...   \n",
      "\n",
      "      VAL_METHOD                  VAL_DATE  \\\n",
      "0  Imagery/Other  2010-06-25T00:00:00.000Z   \n",
      "1  Imagery/Other  2010-06-25T00:00:00.000Z   \n",
      "2  Imagery/Other  2010-06-25T00:00:00.000Z   \n",
      "3  Imagery/Other  2010-06-25T00:00:00.000Z   \n",
      "4  Imagery/Other  2010-06-22T00:00:00.000Z   \n",
      "\n",
      "                                             WEBSITE   LEVEL_  ENROLLMENT  \\\n",
      "0  http://nces.ed.gov/GLOBALLOCATOR/sch_info_popu...    Other         312   \n",
      "1  http://nces.ed.gov/GLOBALLOCATOR/sch_info_popu...     High           0   \n",
      "2  http://nces.ed.gov/GLOBALLOCATOR/sch_info_popu...  Primary         272   \n",
      "3  http://nces.ed.gov/GLOBALLOCATOR/sch_info_popu...   Middle         346   \n",
      "4  http://nces.ed.gov/GLOBALLOCATOR/sch_info_popu...     High         489   \n",
      "\n",
      "  START_GRAD END_GRADE DISTRICT_I  FULL_TIME_     SHELTER_ID  \n",
      "0         KG        09     101680          28  NOT AVAILABLE  \n",
      "1         08        12     101680           0  NOT AVAILABLE  \n",
      "2         KG        03     101680          20  NOT AVAILABLE  \n",
      "3         04        09     101680          24  NOT AVAILABLE  \n",
      "4         07        12     101710          25       10774856  \n",
      "\n",
      "[5 rows x 34 columns]\n"
     ]
    }
   ],
   "source": [
    "print(public.head())"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 4,
   "id": "d43648c6-4e6f-41af-81ff-17322baa2160",
   "metadata": {},
   "outputs": [],
   "source": [
    "# filtereing states to only show TX\n",
    "\n",
    "public = public[public[\"STATE\"] == \"TX\"]"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 5,
   "id": "eabb499d-ee92-4463-ba37-21bfa28994bb",
   "metadata": {},
   "outputs": [],
   "source": [
    "# removing columns that mainly have \"Not Availiable\" values and unnecessary to our project\n",
    "\n",
    "public_drop = [\"X\", \"Y\", \"FID\",\"ADDRESS2\", \"VAL_METHOD\", \"TELEPHONE\", \"ZIP4\", \"LATITUDE\", \"LONGITUDE\", \"SOURCE\",\n",
    "               \"WEBSITE\", \"SOURCE_DAT\", \"SHELTER_ID\"]\n",
    "public = public.drop(columns=public_drop)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 6,
   "id": "8ce7291c-f3bc-442a-87d9-9b21cbe5e2af",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "       YEAR\n",
      "74000  2010\n",
      "74001  2010\n",
      "74002  2013\n",
      "74003  2013\n",
      "74004  2010\n"
     ]
    }
   ],
   "source": [
    "# change the VAL_DATE column to only show the year\n",
    "\n",
    "public[\"YEAR\"] = pd.to_datetime(public[\"VAL_DATE\"]).dt.year\n",
    "public = public.drop(columns=[\"VAL_DATE\"])\n",
    "print(public[[\"YEAR\"]].head())"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 8,
   "id": "97ed6ffb-053c-42be-8454-4196daa763d6",
   "metadata": {},
   "outputs": [],
   "source": [
    "# cleaning up column names and removing possible whitespaces\n",
    "\n",
    "public = public.rename(columns={\"LEVEL_\": \"LEVEL\"})\n",
    "public.columns = public.columns.str.strip()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 9,
   "id": "b13d9097-c726-4d84-82ae-92f54b67414d",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "<class 'pandas.core.frame.DataFrame'>\n",
      "Index: 9340 entries, 74000 to 103459\n",
      "Data columns (total 21 columns):\n",
      " #   Column      Non-Null Count  Dtype \n",
      "---  ------      --------------  ----- \n",
      " 0   NCESID      9340 non-null   int64 \n",
      " 1   NAME        9340 non-null   object\n",
      " 2   ADDRESS     9340 non-null   object\n",
      " 3   CITY        9340 non-null   object\n",
      " 4   STATE       9340 non-null   object\n",
      " 5   ZIP         9340 non-null   int64 \n",
      " 6   TYPE        9340 non-null   int64 \n",
      " 7   STATUS      9340 non-null   int64 \n",
      " 8   POPULATION  9340 non-null   int64 \n",
      " 9   COUNTY      9340 non-null   object\n",
      " 10  COUNTYFIPS  9340 non-null   object\n",
      " 11  COUNTRY     9340 non-null   object\n",
      " 12  NAICS_CODE  9340 non-null   int64 \n",
      " 13  NAICS_DESC  9340 non-null   object\n",
      " 14  LEVEL       9340 non-null   object\n",
      " 15  ENROLLMENT  9340 non-null   int64 \n",
      " 16  START_GRAD  9340 non-null   object\n",
      " 17  END_GRADE   9340 non-null   object\n",
      " 18  DISTRICT_I  9340 non-null   int64 \n",
      " 19  FULL_TIME_  9340 non-null   int64 \n",
      " 20  YEAR        9340 non-null   int32 \n",
      "dtypes: int32(1), int64(9), object(11)\n",
      "memory usage: 1.5+ MB\n"
     ]
    }
   ],
   "source": [
    "public.info()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 13,
   "id": "a684963b-ab8d-4fff-958f-2e7e152f6d92",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "<class 'pandas.core.frame.DataFrame'>\n",
      "Index: 9340 entries, 74000 to 103459\n",
      "Data columns (total 21 columns):\n",
      " #   Column      Non-Null Count  Dtype   \n",
      "---  ------      --------------  -----   \n",
      " 0   NCESID      9340 non-null   string  \n",
      " 1   NAME        9340 non-null   string  \n",
      " 2   ADDRESS     9340 non-null   string  \n",
      " 3   CITY        9340 non-null   string  \n",
      " 4   STATE       9340 non-null   category\n",
      " 5   ZIP         9340 non-null   string  \n",
      " 6   TYPE        9340 non-null   category\n",
      " 7   STATUS      9340 non-null   category\n",
      " 8   POPULATION  9340 non-null   int64   \n",
      " 9   COUNTY      9340 non-null   string  \n",
      " 10  COUNTYFIPS  9340 non-null   string  \n",
      " 11  COUNTRY     9340 non-null   string  \n",
      " 12  NAICS_CODE  9340 non-null   category\n",
      " 13  NAICS_DESC  9340 non-null   string  \n",
      " 14  LEVEL       9340 non-null   category\n",
      " 15  ENROLLMENT  9340 non-null   int64   \n",
      " 16  START_GRAD  9340 non-null   string  \n",
      " 17  END_GRADE   9340 non-null   string  \n",
      " 18  DISTRICT_I  9340 non-null   int64   \n",
      " 19  FULL_TIME_  9340 non-null   int64   \n",
      " 20  YEAR        9340 non-null   int16   \n",
      "dtypes: category(5), int16(1), int64(4), string(11)\n",
      "memory usage: 1.2 MB\n"
     ]
    }
   ],
   "source": [
    "# changing columns to be appropriate datatypes\n",
    "\n",
    "string_cols = [\"NCESID\", \"ZIP\", \"COUNTYFIPS\",\"NAME\", \"ADDRESS\", \"CITY\", \"COUNTY\", \"COUNTRY\",\"NAICS_DESC\", \"START_GRAD\", \"END_GRADE\"]\n",
    "public[string_cols] = public[string_cols].astype(\"string\")\n",
    "\n",
    "cate_cols = [\"TYPE\", \"STATUS\", \"NAICS_CODE\", \"STATE\", \"LEVEL\"]\n",
    "public[cate_cols] = public[cate_cols].astype(\"category\")\n",
    "\n",
    "public[\"YEAR\"] = public[\"YEAR\"].astype(\"int16\")\n",
    "\n",
    "public.info()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 16,
   "id": "b1a157a4-a2fd-4154-ac79-72b19a98682e",
   "metadata": {},
   "outputs": [],
   "source": [
    "# exporting cleaned dataset\n",
    "public.to_csv(\"Public_Schools_TX_Cleaned.csv\")"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "ebcfb0e7-0882-4675-bb54-c2da84ff209a",
   "metadata": {},
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python [conda env:base] *",
   "language": "python",
   "name": "conda-base-py"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.13.5"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
