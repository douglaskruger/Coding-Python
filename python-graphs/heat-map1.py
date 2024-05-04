import pandas as pd

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)

# Read the CSV files into Pandas Dataframes.
df_february = pd.read_csv("SOLDFOOD2023 - Winter.xlsx - FEBRUARY.csv")
df_january = pd.read_csv("SOLDFOOD2023 - Winter.xlsx - JANUARY.csv")

# Display the first 5 rows of each DataFrame.
print("First 5 rows of February data:")
print(df_february.head().to_markdown(index=False, numalign="left", stralign="left"))

print("\nFirst 5 rows of January data:")
print(df_january.head().to_markdown(index=False, numalign="left", stralign="left"))

# Print the column names and their data types of each DataFrame.
print("\nColumn names and data types of February data:")
print(df_february.info())

print("\nColumn names and data types of January data:")
print(df_january.info())

import seaborn as sns
import matplotlib.pyplot as plt

# Remove the first two rows and promote the third row as the header for both DataFrames.
df_february = df_february.iloc[2:].copy()
df_february.columns = df_february.iloc[0]
df_february = df_february.iloc[1:].copy()

df_january = df_january.iloc[2:].copy()
df_january.columns = df_january.iloc[0]
df_january = df_january.iloc[1:].copy()

# Filter columns to keep only `QUANTITY` and `GROUP` columns.
df_february = df_february[['QUANTITY', 'GROUP']]
df_january = df_january[['QUANTITY', 'GROUP']]

# Convert `QUANTITY` to numeric, coercing errors to NaN.
df_february['QUANTITY'] = pd.to_numeric(df_february['QUANTITY'], errors='coerce')
df_january['QUANTITY'] = pd.to_numeric(df_january['QUANTITY'], errors='coerce')

# Create a `Month` column by extracting the month name from the file name and add it to each DataFrame.
df_february['Month'] = 'February'
df_january['Month'] = 'January'

# Combine both DataFrames into one.
df_combined = pd.concat([df_january, df_february], ignore_index=True)

# Aggregate by `GROUP` and `Month` to get the total `QUANTITY` sold.
df_agg = df_combined.groupby(['GROUP', 'Month'])['QUANTITY'].sum().reset_index()

# Create a pivot table to restructure the data for the heatmap with `Month` as the index, `GROUP` as the columns, and `QUANTITY` as the values.
pivot_table = df_agg.pivot(index='Month', columns='GROUP', values='QUANTITY')

# Fill any missing values in the pivot table with 0.
pivot_table = pivot_table.fillna(0)

# Create and display a heatmap.
plt.figure(figsize=(10, 6))
sns.heatmap(pivot_table, annot=True, fmt='g', cmap="YlGnBu")

# Add labels and title to the heatmap and display it.
plt.xlabel('Group', fontsize=12)
plt.ylabel('Month', fontsize=12)
plt.title('Quantity Sold by Group and Month', fontsize=14)
plt.show()