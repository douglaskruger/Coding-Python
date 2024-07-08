import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Read the CSV file into a DataFrame
data = pd.read_csv('Hospital_Survey_Data_Alcohol_Drug_Abuse.csv', skiprows=1)

# Display the first 5 rows
#print(data.head().to_markdown(index=False, numalign="left", stralign="left"))

# Print the column names and their data types
#print(data.info())

# Extract relevant columns
hospital_data = data[['Hospital Rating', 'Average Total Payments ($)', 'Average Covered Charges ($)', 'Average Medicare Payments ($)']]

# Compute the correlation matrix
correlation_matrix = hospital_data.corr()

# Create heatmap
plt.figure(figsize=(10, 8))
heatmap = sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt=".2f", linewidths=.5)
plt.title('Correlation Heatmap of Hospital Data')
plt.show()