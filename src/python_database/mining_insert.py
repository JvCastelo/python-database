import pandas as pd
import psycopg2
from dotenv import load_dotenv
import os

load_dotenv()

df = pd.read_csv("src/python_database/raw_data/data.csv")

dict_columns = {
    "Date/Time": "sample_time",
    "LV ActivePower (kW)": "active_power",
    "Wind Speed (m/s)": "wind_speed",
    "Theoretical_Power_Curve (KWh)": "expected_power",
    "Wind Direction (°)": "wind_direction",
}

df.rename(columns=dict_columns, inplace=True)

df["sample_time"] = pd.to_datetime(
    df["sample_time"], format="%d %m %Y %H:%M"
).dt.tz_localize("America/Fortaleza")


connection = psycopg2.connect(
    database=os.getenv("DATABASE"),
    user=os.getenv("USER"),
    host=os.getenv("HOST"),
    password=os.getenv("PASSWORD"),
    port=os.getenv("PORT"),
)

schema = "public"
table = "raw"

cursor = connection.cursor()

for index, row in df.iterrows():
    print(index, end="\n")
    print(row["sample_time"], end="\n")
    print(row["active_power"], end="\n")
    print(row["wind_speed"], end="\n")
    print(row["expected_power"], end="\n")
    print(row["wind_direction"], end="\n")

    print(f"### INSERTION {index} ###", end="\n")

    query = f"""
        INSERT INTO {schema}.{table} (sample_time, active_power, wind_speed, expected_power, wind_direction)
        VALUES ('{row["sample_time"]}', {row["active_power"]}, {row["wind_speed"]}, {row["expected_power"]}, {row["wind_direction"]})
    """
    print(query, end="\n")

    cursor.execute(query)

# rows = cursor.fetchall()

connection.commit()
cursor.close()
connection.close()

# for row in rows:
#     print(row)
