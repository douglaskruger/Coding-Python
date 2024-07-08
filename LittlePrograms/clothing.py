import pandas as pd

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)

# Read the CSV file into a DataFrame
df = pd.read_csv('Wild_by_Aura_Final.csv')

# Display the first 5 rows
print(df.head().to_markdown(index=False, numalign="left", stralign="left"))

# Print the column names and their data types
print(df.info())

df['Type of Clothing'].fillna('Unknown', inplace=True)
df['Size of Clothing'].fillna('Unknown', inplace=True)

# Combine type and size info into a single column
df['Type/Size of Clothing'] = (
    df['Type of Clothing'] + ' / ' + df['Size of Clothing']
)

# Look at the first 5 rows again
print(df.head().to_markdown(index=False, numalign="left", stralign="left"))