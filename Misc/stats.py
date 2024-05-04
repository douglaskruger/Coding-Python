import statistics
import numpy as np
from scipy.stats import t

def calculate_stats(numbers, confidence_level=0.95):
    try:
        mean = statistics.mean(numbers)
        mode = statistics.mode(numbers)
        std_dev = statistics.stdev(numbers)
        variance = statistics.variance(numbers)
        correlation_coefficient = np.corrcoef(numbers, numbers)[0, 1]

        # Calculate confidence interval
        n = len(numbers)
        t_value = t.ppf((1 + confidence_level) / 2, n - 1)
        margin_of_error = t_value * std_dev / np.sqrt(n)
        confidence_interval = (mean - margin_of_error, mean + margin_of_error)

        # Calculate percentiles
        percentiles = np.percentile(numbers, [25, 50, 75])

        return mean, mode, std_dev, variance, correlation_coefficient, confidence_interval, percentiles
    except statistics.StatisticsError as e:
        print(f"Error: {e}")
        return None

numbers = [1, 2, 3, 4, 5, 5, 5]
results = calculate_stats(numbers)

if results is not None:
    mean, mode, std_dev, variance, correlation_coefficient, confidence_interval, percentiles = results
    print("Mean: ", mean)
    print("Mode: ", mode)
    print("Standard Deviation: ", std_dev)
    print("Variance: ", variance)
    print("Correlation Coefficient: ", correlation_coefficient)
    print("Confidence Interval: ", confidence_interval)
    print("25th Percentile: ", percentiles[0])
    print("50th Percentile (Median): ", percentiles[1])
    print("75th Percentile: ", percentiles[2])