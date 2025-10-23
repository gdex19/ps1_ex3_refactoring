# %%
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
import polars as pl
import seaborn as sns

plt.style.use("ggplot")
plt.rcParams["figure.figsize"] = (15, 3)
plt.rcParams["font.family"] = "sans-serif"

# %%
# By the end of this chapter, we're going to have downloaded all of Canada's weather data for 2012, and saved it to a CSV. We'll do this by downloading it one month at a time, and then combining all the months together.
# Here's the temperature every hour for 2012!

# Old implementation
# weather_2012_final = pd.read_csv("../data/weather_2012.csv", index_col="date_time")
# weather_2012_final["temperature_c"].plot(figsize=(15, 6))
# plt.show()

# Polars implementation - not exactly the same, no indexes and polars plotting wasn't cooperating
weather_2012_final = pl.read_csv("../data/weather_2012.csv")
x = weather_2012_final.get_column("date_time").to_list()
y = weather_2012_final.get_column("temperature_c").to_list()

fig, ax = plt.subplots(figsize=(15, 6))
ax.plot(x, y)
ax.set_xlabel("date_time")
ax.xaxis.set_major_locator(mdates.AutoDateLocator())

plt.show()

# %%
# Okay, let's start from the beginning.
# We're going to get the data for March 2012, and clean it up
# You can directly download a csv with a URL using Pandas!
# Note, the URL the repo provides is faulty but kindly, someone submitted a PR fixing it. Have a look
# here: https://github.com/jvns/pandas-cookbook/pull/74 and click on "Files changed" and then fix the url.


# This URL is fixed
url_template = "http://climate.weather.gc.ca/climate_data/bulk_data_e.html?format=csv&stationID=5415&Year={year}&Month={month}&timeframe=1&submit=Download+Data"

year = 2012
month = 3
url_march = url_template.format(month=3, year=2012)

# Old implementation
# weather_mar2012 = pd.read_csv(
#     url_march,
#     index_col="Date/Time (LST)",
#     parse_dates=True,
#     encoding="latin1",
#     header=0,
# )
# weather_mar2012.head()

# Polars implementation
weather_mar2012 = pl.read_csv(
    url_march,
    try_parse_dates=True,
    encoding="latin1",
    has_header=True,
)
weather_mar2012.head()


# %%
# Let's clean up the data a bit.
# You'll notice in the summary above that there are a few columns which are are either entirely empty or only have a few values in them. Let's get rid of all of those with `dropna`.
# The argument `axis=1` to `dropna` means "drop columns", not rows", and `how='any'` means "drop the column if any value is null".

# Old implementation
# weather_mar2012 = weather_mar2012.dropna(axis=1, how="any")
# weather_mar2012[:5]

# Polars implementation
weather_mar2012 = weather_mar2012.drop_nans()
weather_mar2012[:5]

# This is much better now -- we only have columns with real data.

# %%
# Let's get rid of columns that we do not need.
# For example, the year, month, day, time columns are redundant (we have Date/Time (LST) column).
# Let's get rid of those. The `axis=1` argument means "Drop columns", like before. The default for operations like `dropna` and `drop` is always to operate on rows.

# Old Implementation
# weather_mar2012 = weather_mar2012.drop(["Year", "Month", "Day", "Time (LST)"], axis=1)
# weather_mar2012[:5]

# Polars Implementation
weather_mar2012 = weather_mar2012.drop(["Year", "Month", "Day", "Time (LST)"])
weather_mar2012[:5]

# %%
# When you look at the data frame, you see that some column names have some weird characters in them.
# Let's clean this up, too.
# Let's print the column names first:
print(weather_mar2012.columns)

# Old implementation
# # And now rename the columns to make it easier to work with
# weather_mar2012.columns = weather_mar2012.columns.str.replace(
#     'ï»¿"', ""
# )  # Remove the weird characters at the beginning
# weather_mar2012.columns = weather_mar2012.columns.str.replace(
#     "Â", ""
# )  # Remove the weird characters at the

# Polars implementation
# And now rename the columns to make it easier to work with
weather_mar2012.columns = [s.replace('ï»¿"', "") for s in weather_mar2012.columns]
# Remove the weird characters at the beginning
weather_mar2012.columns = [s.replace("Â", "") for s in weather_mar2012.columns]
# Remove the weird characters at the end

weather_mar2012.columns


# %%
# Optionally, you can also rename columns more manually for specific cases:

# Old implementation
# weather_mar2012 = weather_mar2012.rename(
#     columns={
#         'Longitude (x)"': "Longitude",
#         "Latitude (y)": "Latitude",
#         "Station Name": "Station_Name",
#         "Climate ID": "Climate_ID",
#         "Temp (°C)": "Temperature_C",
#         "Dew Point Temp (Â°C)": "Dew_Point_Temp_C",
#         "Rel Hum (%)": "Relative_Humidity",
#         "Wind Spd (km/h)": "Wind_Speed_kmh",
#         "Visibility (km)": "Visibility_km",
#         "Stn Press (kPa)": "Station_Pressure_kPa",
#         "Weather": "Weather",
#     }
# )
# weather_mar2012.index.name = "date_time"

# # Check the new column names
# print(weather_mar2012.columns)

# # Some people also prefer lower case column names.
# weather_mar2012.columns = weather_mar2012.columns.str.lower()
# print(weather_mar2012.columns)

# Polars implementation 
weather_mar2012 = weather_mar2012.rename(
    {
        'Longitude (x)"': "Longitude",
        "Latitude (y)": "Latitude",
        "Station Name": "Station_Name",
        "Climate ID": "Climate_ID",
        "Temp (°C)": "Temperature_C",
        "Dew Point Temp (°C)": "Dew_Point_Temp_C",
        "Rel Hum (%)": "Relative_Humidity",
        "Wind Spd (km/h)": "Wind_Speed_kmh",
        "Visibility (km)": "Visibility_km",
        "Stn Press (kPa)": "Station_Pressure_kPa",
        "Weather": "Weather",
    }
)

# Check the new column names
print(weather_mar2012.columns)

# Some people also prefer lower case column names.
weather_mar2012.columns = [s.lower() for s in weather_mar2012.columns]
print(weather_mar2012.columns)


# %%
# Notice how it goes up to 25° C in the middle there? That was a big deal. It was March, and people were wearing shorts outside.

# Old implementation
# weather_mar2012["temperature_c"].plot(figsize=(15, 5))
# plt.show()

# Polars implementation
x = weather_mar2012.get_column("date/time (lst)").to_list()
y = weather_mar2012.get_column("temperature_c").to_list()

fig, ax = plt.subplots(figsize=(15, 5))
ax.plot(x, y)
ax.set_xlabel("date_time")
ax.xaxis.set_major_locator(mdates.AutoDateLocator())

plt.show()

# %%
# This one's just for fun -- we've already done this before, using groupby and aggregate! We will learn whether or not it gets colder at night. Well, obviously. But let's do it anyway.

# Old implementation
# temperatures = weather_mar2012[["temperature_c"]].copy()
# print(temperatures.head)
# temperatures.loc[:, "Hour"] = weather_mar2012.index.hour
# temperatures.groupby("Hour").aggregate(np.median).plot()
# plt.show()

# Polars implementation
temperatures = weather_mar2012[["temperature_c"]].clone()
print(temperatures.head)
temperatures.insert_column(0, weather_mar2012["date/time (lst)"].dt.hour().rename("hour"))
print(temperatures.head())
medians = temperatures.group_by("hour").median()
sns.lineplot(data=medians, x="hour", y="temperature_c")
plt.show()

# So it looks like the time with the highest median temperature is 2pm. Neat.

# %%
# Okay, so what if we want the data for the whole year? Ideally the API would just let us download that, but I couldn't figure out a way to do that.
# First, let's put our work from above into a function that gets the weather for a given month.

# Old implementation
# def clean_data(data):
#     data = data.dropna(axis=1, how="any")
#     data = data.drop(["Year", "Month", "Day", "Time (LST)"], axis=1)
#     data.columns = data.columns.str.replace('ï»¿"', "")
#     data.columns = data.columns.str.replace("Â", "")
#     data = data.rename(
#         columns={
#             "Longitude (x)": "Longitude",
#             "Latitude (y)": "Latitude",
#             "Station Name": "Station_Name",
#             "Climate ID": "Climate_ID",
#             "Temp (°C)": "Temperature_C",
#             "Dew Point Temp (°C)": "Dew_Point_Temp_C",
#             "Rel Hum (%)": "Relative_Humidity",
#             "Wind Spd (km/h)": "Wind_Speed_kmh",
#             "Visibility (km)": "Visibility_km",
#             "Stn Press (kPa)": "Station_Pressure_kPa",
#             "Weather": "Weather",
#         }
#     )
#     data.columns = data.columns.str.lower()
#     data.index.name = "date_time"
#     return data


# def download_weather_month(year, month):
#     url_template = "http://climate.weather.gc.ca/climate_data/bulk_data_e.html?format=csv&stationID=5415&Year={year}&Month={month}&timeframe=1&submit=Download+Data"
#     url = url_template.format(year=year, month=month)
#     weather_data = pd.read_csv(
#         url, index_col="Date/Time (LST)", parse_dates=True, header=0
#     )
#     weather_data_clean = clean_data(weather_data)
#     return weather_data_clean

# Polars implementation
def clean_data(data):
    data = data.drop_nans()
    data = data.drop(["Year", "Month", "Day", "Time (LST)"])
    data.columns = [s.replace('ï»¿"', "") for s in data.columns]
    data.columns = [s.replace("Â", "") for s in data.columns]
    data = data.rename(
        {
            "Longitude (x)": "Longitude",
            "Latitude (y)": "Latitude",
            "Station Name": "Station_Name",
            "Climate ID": "Climate_ID",
            "Temp (°C)": "Temperature_C",
            "Dew Point Temp (°C)": "Dew_Point_Temp_C",
            "Rel Hum (%)": "Relative_Humidity",
            "Wind Spd (km/h)": "Wind_Speed_kmh",
            "Visibility (km)": "Visibility_km",
            "Stn Press (kPa)": "Station_Pressure_kPa",
            "Weather": "Weather",
        }
    )
    data.columns = [s.lower() for s in data.columns]
    if data["hmdx flag"].dtype.is_integer():
        data["hdmx flag"] = data["hmdx flag"].cast(pl.String)
    return data

schema = {
    'Longitude (x)': pl.Float64(), 'Latitude (y)': pl.Float64(), 'Station Name': pl.String(), 'Climate ID': pl.Int64(), 
    'Date/Time (LST)': pl.Datetime(time_unit='us', time_zone=None), 'Year': pl.Int64(), 'Month': pl.Int64(), 
    'Day': pl.Int64(), 'Time (LST)': pl.Time(), 'Flag': pl.String(), 'Temp (°C)': pl.Float64(), 'Temp Flag': pl.String(), 
    'Dew Point Temp (°C)': pl.Float64(), 'Dew Point Temp Flag': pl.String(), 'Rel Hum (%)': pl.Int64(), 
    'Rel Hum Flag': pl.String(), 'Precip. Amount (mm)': pl.String(), 'Precip. Amount Flag': pl.String(), 
    'Wind Dir (10s deg)': pl.String(), 'Wind Dir Flag': pl.String(), 'Wind Spd (km/h)': pl.Int64(), 'Wind Spd Flag': pl.String(), 
    'Visibility (km)': pl.Float64(), 'Visibility Flag': pl.String(), 'Stn Press (kPa)': pl.Float64(), 'Stn Press Flag': pl.String(), 
    'Hmdx': pl.String(), 'Hmdx Flag': pl.String(), 'Wind Chill': pl.String(), 'Wind Chill Flag': pl.String(), 'Weather': pl.String()
}

def download_weather_month(year, month):
    url_template = "http://climate.weather.gc.ca/climate_data/bulk_data_e.html?format=csv&stationID=5415&Year={year}&Month={month}&timeframe=1&submit=Download+Data"
    url = url_template.format(year=year, month=month)
    weather_data = pl.read_csv(
        url, try_parse_dates=True, has_header=True,
        schema_overrides=schema
    )
    weather_data_clean = clean_data(weather_data)
    return weather_data_clean


# %%
download_weather_month(2012, 1)[:5]
# %%
# Now, let's use a list comprehension to download all our data and then just concatenate these data frames
# This might take a while

# Old implementation
# data_by_month = [download_weather_month(2012, i) for i in range(1, 13)]
# weather_2012 = pd.concat(data_by_month)
# weather_2012.head()

# Polars implementation
data_by_month = [download_weather_month(2012, i) for i in range(1, 13)]

weather_2012 = pl.concat(data_by_month)
weather_2012.head()

# %%
# Now, let's save the data.

# Old implementation
# weather_2012.to_csv("../data/weather_2012.csv")

# Polars implementation
weather_2012.write_csv("../data/weather_2012.csv")

# %%
