import dask.dataframe as dd
import pandas as pd
import matplotlib.pyplot as plt

# Create a sample large dataset (for demonstration purposes)
# You can skip this part if you already have a large dataset
def create_sample_large_dataset(filename, num_rows=10**6):
    df = pd.DataFrame({
        'A': range(num_rows),
        'B': range(num_rows, 2*num_rows),
        'C': range(2*num_rows, 3*num_rows),
        'D': [i % 10 for i in range(num_rows)]  # Adding a categorical column
    })
    df.to_csv(filename, index=False)

# Create a large dataset (this step is optional if you already have a dataset)
create_sample_large_dataset('large_dataset.csv')

# Load the large dataset with Dask
ddf = dd.read_csv('large_dataset.csv')

# 1. Grouping and Aggregation
# Group by column 'D' and compute the mean of columns 'A', 'B', and 'C'
grouped = ddf.groupby('D').mean().compute()
print("Grouped by 'D' and computed means:")
print(grouped)

# 2. Joining DataFrames
# Create another large dataset for joining
create_sample_large_dataset('large_dataset2.csv')
ddf2 = dd.read_csv('large_dataset2.csv')

# Perform an inner join on the 'A' column
joined = dd.merge(ddf, ddf2, on='A', suffixes=('_left', '_right'))
joined_computed = joined.compute()
print("Joined DataFrames on column 'A':")
print(joined_computed.head())

# 3. Handling Missing Data
# Introduce some missing values
ddf_with_nans = ddf.mask(ddf % 100000 < 5, other=None)

# Count missing values
missing_counts = ddf_with_nans.isnull().sum().compute()
print("Missing values count:")
print(missing_counts)

# Fill missing values with a specified value
ddf_filled = ddf_with_nans.fillna(-1)

# 4. Visualization
# Visualize the distribution of column 'A'
ddf['A'].compute().plot(kind='hist', bins=50, alpha=0.5)
plt.title('Distribution of Column A')
plt.xlabel('A')
plt.ylabel('Frequency')
plt.show()

# 5. Parallel Processing
def process_partition(df):
    return df['A'] * 2

if __name__ == '__main__':
    result = ddf.map_partitions(process_partition).compute(scheduler='processes')
    print("Parallel processing result (first 10 rows):")
    print(result.head(10))

    # Note: For better performance with large datasets, consider using a Dask cluster.
