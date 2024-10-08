import os
import matplotlib.pyplot as plt

def generate_file_count_data(directory_path):
    """
    Collects data on the number of files in each subdirectory.

    Args:
        directory_path (str): The path to the directory to process.

    Returns:
        dict: A dictionary where keys are subdirectory names and values are file counts.
    """

    file_counts = {}
    for root, subdirs, files in os.walk(directory_path):
        for subdir in subdirs:
            file_counts[subdir] = len(files)

    return file_counts

def graph_file_counts(file_counts):
    """
    Creates a bar graph of the number of files in each subdirectory.

    Args:
        file_counts (dict): A dictionary where keys are subdirectory names and values are file counts.
    """

    subdirectories = list(file_counts.keys())
    counts = list(file_counts.values())

    plt.bar(subdirectories, counts)
    plt.xlabel("Subdirectory")
    plt.ylabel("Number of Files")
    plt.title("File Counts in Subdirectories")
    plt.xticks(rotation=45, ha='right')  # Rotate x-axis labels for readability
    plt.tight_layout()  # Adjust layout to prevent labels from overlapping
    plt.show()

if __name__ == '__main__':
    root_directory = input("Enter the root directory path: ")
    data = generate_file_count_data(root_directory)
    graph_file_counts(data)
