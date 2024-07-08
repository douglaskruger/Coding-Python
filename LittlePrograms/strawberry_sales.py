import pandas as pd

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)

# Read the CSV file into a DataFrame
df = pd.read_csv('STRAWBERRY SALES 2023 - Sheet1.tsv', sep='\t', skiprows=2)

# Display the first 5 rows
print(df.head().to_markdown(index=False, numalign="left", stralign="left"))

# Print the column names and their data types
print(df.info())

# Convert `DATE` column to datetime
df['DATE'] = pd.to_datetime(df['DATE'], format='%d-%b-%y')

# Extract month name from `DATE` and create new column `MONTH`
df['MONTH'] = df['DATE'].dt.strftime('%B')

# Print descriptive statistics of `#BOXES` and `TOTAL`
print("Statistics of #BOXES:")
print(df['#BOXES'].describe().to_markdown(numalign="left", stralign="left"))
print("\nStatistics of TOTAL:")
print(df['TOTAL'].describe().to_markdown(numalign="left", stralign="left"))

# Calculate the first quartile (Q1), third quartile (Q3), and interquartile range (IQR) for `#BOXES`.
Q1 = df['#BOXES'].quantile(0.25)
Q3 = df['#BOXES'].quantile(0.75)
IQR = Q3 - Q1

# Define the lower and upper bounds for outliers using the formula:
# Lower Bound = Q1 - 1.5 * IQR
# Upper Bound = Q3 + 1.5 * IQR
lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR

# Identify outliers in `#BOXES` by filtering values that fall outside the lower and upper bounds.
outliers = df[(df['#BOXES'] < lower_bound) | (df['#BOXES'] > upper_bound)]

# Print the outliers.
if not outliers.empty:
  print("Outliers in #BOXES:")
  print(outliers[['DATE', '#BOXES', 'TOTAL']].to_markdown(index=False, numalign="left", stralign="left"))
else:
  print("No outliers found in #BOXES.")

# Remove '$', ',' and empty spaces from `TOTAL`.
df['TOTAL'] = df['TOTAL'].astype(str).str.replace('[$, ]', '', regex=True)

# Convert `TOTAL` column to numeric.
df['TOTAL'] = pd.to_numeric(df['TOTAL'])

# Calculate the first quartile (Q1), third quartile (Q3), and interquartile range (IQR) for `TOTAL`.
Q1 = df['TOTAL'].quantile(0.25)
Q3 = df['TOTAL'].quantile(0.75)
IQR = Q3 - Q1

# Define the lower and upper bounds for outliers using the formula:
# Lower Bound = Q1 - 1.5 * IQR
# Upper Bound = Q3 + 1.5 * IQR
lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR

# Identify outliers in `TOTAL` by filtering values that fall outside the lower and upper bounds.
outliers = df[(df['TOTAL'] < lower_bound) | (df['TOTAL'] > upper_bound)]

# Print the outliers.
if not outliers.empty:
  print("Outliers in TOTAL:")
  print(outliers[['DATE', '#BOXES', 'TOTAL']].to_markdown(index=False, numalign="left", stralign="left"))
else:
  print("No outliers found in TOTAL.")

import matplotlib.pyplot as plt

# Create two subplots
fig, ax = plt.subplots(2, 1, figsize=(12, 8))

# Plot for `#BOXES` over time
ax[0].plot(df['DATE'], df['#BOXES'], marker='o', linestyle='-', color='b')
ax[0].set_xlabel('Date')
ax[0].set_ylabel('#BOXES')
ax[0].set_title('#BOXES Over Time')

# Plot for `TOTAL` over time
ax[1].plot(df['DATE'], df['TOTAL'], marker='o', linestyle='-', color='r')
ax[1].set_xlabel('Date')
ax[1].set_ylabel('TOTAL')
ax[1].set_title('TOTAL Over Time')

# Adjust layout for better readability
plt.tight_layout()

# Display the plots
plt.show()