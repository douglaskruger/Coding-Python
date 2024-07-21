import dask.dataframe as dd
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from dask.distributed import Client, LocalCluster
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from dask_ml.model_selection import train_test_split
from dask_ml.preprocessing import StandardScaler

# Create a sample large dataset (for demonstration purposes)
def create_sample_large_dataset(filename, num_rows=10**4, chunk_size=10**2):
    dates = pd.date_range(start='1/1/2020', periods=num_rows, freq='min')
    df = pd.DataFrame({
        'timestamp': dates,
        'feature1': np.random.rand(num_rows),
        'feature2': np.random.rand(num_rows),
        'feature3': np.random.rand(num_rows),
        'category': np.random.choice(['A', 'B', 'C'], size=num_rows)
    })
    # Write to CSV in chunks
    #ddf = dd.from_pandas(df, npartitions=10)
    #ddf.to_csv(filename, single_file=True)

    for start in range(0, num_rows, chunk_size):
        end = min(start + chunk_size, num_rows)
        chunk = df.iloc[start:end]
        if start == 0:
            chunk.to_csv(filename, index=False, mode='w', header=True)
        else:
            chunk.to_csv(filename, index=False, mode='a', header=False)
        print(f"Wrote rows {start} to {end}")

# Create a large dataset (this step is optional if you already have a dataset)
create_sample_large_dataset('large_dataset.csv')

# Main function to encapsulate the logic
def main():
    # 1. Start a local Dask cluster
    print("*** 1: Setup Local Dask Cluster")
    cluster = LocalCluster(dashboard_address=':0')
    client = Client(cluster)

    # Load the large dataset with Dask
    print("*** 2: Load CSV file")
    numeric_cols = ['feature1', 'feature2', 'feature3']
    ddf = dd.read_csv('large_dataset.csv', parse_dates=['timestamp'])
    #print("*** CSV Data: ***", ddf.head())

    # Recompute ddf after transformation to avoid further issues
    print("*** 3: Recompute transformation")
    ddf = ddf.persist()

    # 4. Visualization
    print("*** 4: Visualization")
    ddf['feature1'].compute().plot(kind='hist', bins=50, alpha=0.5)
    plt.title('Distribution of Feature 1')
    plt.xlabel('Feature 1')
    plt.ylabel('Frequency')
    plt.show()

    # 5. Parallel Processing
    print("*** 5: Parallel Processing")
    def process_partition(df):
        return df['feature1'] * 2

    result = ddf.map_partitions(process_partition).compute(scheduler='processes')
    print("*** Parallel processing result (first 10 rows): ***")
    print(result.head(10))

    # 6. Machine Learning with Dask-ML
    print("*** 6: Machine Learning")
    X = ddf[numeric_cols].compute()
    y = ddf['category'].map({'A': 0, 'B': 1, 'C': 2}).compute()
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

    model = LogisticRegression()
    model.fit(X_train, y_train)
    predictions = model.predict(X_test)
    accuracy = accuracy_score(y_test, predictions)
    print(f"Accuracy: {accuracy}")

    # Clean up Dask client
    print("*** End: Cleanup")
    client.close()
    cluster.close()

# Ensure the script runs only if it's the main module
if __name__ == '__main__':
    main()
