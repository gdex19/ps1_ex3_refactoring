# %%
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import polars as pl

# %%
# Reading data from a csv file
# Original broken pandas read
broken_df = pd.read_csv("../data/bikes.csv", encoding="ISO-8859-1")

# ✅ TODO completed: load with Polars
pl_broken_df = pl.read_csv("../data/bikes.csv", encoding="ISO-8859-1")

# %%
# Look at the first 3 rows
broken_df[:3]

# ✅ TODO completed: Polars equivalent
pl_broken_df.head(3)

# %%
# Fixing the broken CSV parsing in Pandas
fixed_df = pd.read_csv(
    "../data/bikes.csv",
    sep=";",
    encoding="latin1",
    parse_dates=["Date"],
    dayfirst=True,
    index_col="Date",
)
fixed_df[:3]

# ✅ TODO: equivalent in Polars
# Note: Polars doesn't set an index like pandas; instead, you just keep "Date" as a column.
# You can later sort or use it for plotting/grouping.
pl_fixed_df = pl.read_csv(
    "../data/bikes.csv",
    separator=";",
    encoding="latin1",
    try_parse_dates=True,
)
# Convert "Date" to datetime with day-first interpretation
pl_fixed_df = pl_fixed_df.with_columns(
    pl.col("Date").str.strptime(pl.Date, fmt="%d/%m/%Y")
)
pl_fixed_df.head(3)

# %%
# Selecting a column
fixed_df["Berri 1"]

# ✅ TODO: Polars equivalent
pl_fixed_df.select("Berri 1")

# Alternatively, if you want it as a Series-like object (for plotting):
pl_fixed_df["Berri 1"]

# %%
# Plotting is quite easy in Pandas
fixed_df["Berri 1"].plot()

# ✅ TODO: Polars equivalent
# Polars doesn’t have built-in plotting like pandas; convert to pandas first.
pl_fixed_df["Berri 1"].to_pandas().plot()
plt.title("Berri 1 Bike Counts")
plt.show()

# %%
# Plot all columns in Pandas
fixed_df.plot(figsize=(15, 10))

# ✅ TODO: Polars equivalent
# Option 1: Convert entire DataFrame to pandas for quick plotting
pl_fixed_df.to_pandas().plot(figsize=(15, 10))
plt.title("All Bike Paths - Montréal 2012")
plt.show()

# Option 2 (alternative): Use Seaborn for a Polars-native approach
# Melt data into long format for Seaborn
pl_melted = pl_fixed_df.melt(id_vars=["Date"], variable_name="Path", value_name="Count")
sns.lineplot(data=pl_melted.to_pandas(), x="Date", y="Count", hue="Path")
plt.title("All Bike Paths - Montréal 2012 (Seaborn)")
plt.show()
