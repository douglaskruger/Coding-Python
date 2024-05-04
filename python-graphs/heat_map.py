import pandas as pd

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)

# Read the CSV file into a DataFrame
df_drug_abuse = pd.read_csv('Hospital_Survey_Data_Alcohol_Drug_Abuse.csv', skiprows=1)

# Display the first 5 rows
print(df_drug_abuse.head().to_markdown(index=False, numalign="left", stralign="left"))

# Print the column names and their data types
print(df_drug_abuse.info())

import altair as alt
import numpy as np

# Create new columns by dividing the respective payment columns into 10 equal-width bins
df_drug_abuse['Total Payments Bin'] = pd.cut(df_drug_abuse['Average Total Payments ($)'], 10)
df_drug_abuse['Covered Charges Bin'] = pd.cut(df_drug_abuse['Average Covered Charges ($)'], 10)
df_drug_abuse['Medicare Payments Bin'] = pd.cut(df_drug_abuse['Average Medicare Payments ($)'], 10)

# Aggregate by `Hospital Rating` and payment bins, calculate mean `Hospital Rating`
df_agg = df_drug_abuse.groupby(['Hospital Rating', 'Total Payments Bin', 'Covered Charges Bin', 'Medicare Payments Bin']).agg(Mean_Hospital_Rating=('Hospital Rating', 'mean')).reset_index()

# Create pivot tables for each payment type
pivot_total_payments = df_agg.pivot_table(index='Hospital Rating', columns='Total Payments Bin', values='Mean_Hospital_Rating', fill_value=0)
pivot_covered_charges = df_agg.pivot_table(index='Hospital Rating', columns='Covered Charges Bin', values='Mean_Hospital_Rating', fill_value=0)
pivot_medicare_payments = df_agg.pivot_table(index='Hospital Rating', columns='Medicare Payments Bin', values='Mean_Hospital_Rating', fill_value=0)

# Create heatmaps for each pivot table
heatmap_total_payments = alt.Chart(pivot_total_payments.reset_index().melt('Hospital Rating'), title='Mean Hospital Rating by Total Payments and Hospital Rating').mark_rect().encode(
    x=alt.X('Total Payments Bin:N', axis=alt.Axis(title='Total Payments Bin', labelAngle=-45)),
    y=alt.Y('Hospital Rating:N', axis=alt.Axis(title='Hospital Rating')),
    color=alt.Color('value:Q', scale=alt.Scale(scheme='greenblue'), legend=alt.Legend(title='Mean Hospital Rating')),
    tooltip=['Total Payments Bin', 'Hospital Rating', 'value']
).interactive()

heatmap_covered_charges = alt.Chart(pivot_covered_charges.reset_index().melt('Hospital Rating'), title='Mean Hospital Rating by Covered Charges and Hospital Rating').mark_rect().encode(
    x=alt.X('Covered Charges Bin:N', axis=alt.Axis(title='Covered Charges Bin', labelAngle=-45)),
    y=alt.Y('Hospital Rating:N', axis=alt.Axis(title='Hospital Rating')),
    color=alt.Color('value:Q', scale=alt.Scale(scheme='greenblue'), legend=alt.Legend(title='Mean Hospital Rating')),
    tooltip=['Covered Charges Bin', 'Hospital Rating', 'value']
).interactive()

heatmap_medicare_payments = alt.Chart(pivot_medicare_payments.reset_index().melt('Hospital Rating'), title='Mean Hospital Rating by Medicare Payments and Hospital Rating').mark_rect().encode(
    x=alt.X('Medicare Payments Bin:N', axis=alt.Axis(title='Medicare Payments Bin', labelAngle=-45)),
    y=alt.Y('Hospital Rating:N', axis=alt.Axis(title='Hospital Rating')),
    color=alt.Color('value:Q', scale=alt.Scale(scheme='greenblue'), legend=alt.Legend(title='Mean Hospital Rating')),
    tooltip=['Medicare Payments Bin', 'Hospital Rating', 'value']
).interactive()

# Save the plot
heatmap_total_payments.save('hospital_rating_by_total_payments_heatmap.json')
heatmap_covered_charges.save('hospital_rating_by_covered_charges_heatmap.json')
heatmap_medicare_payments.save('hospital_rating_by_medicare_payments_heatmap.json')
