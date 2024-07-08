import json

# Function to request the JSON file name to process
def get_json_file_name():
    """
    Request the JSON file name to process from the user.
    If no file name is entered, default to "sample.json".
    """
    file_name = input("Please enter the name of the JSON file to process (default: sample.json): ")
    if not file_name:
        file_name = "sample.json"
    return file_name

# Function to print out the key-value pairs
def print_items(data, indent=0):
    """
    Recursively print out the key-value pairs in the JSON data.
    """
    for key, value in data.items():
        if isinstance(value, dict):
            print(f"{'  ' * indent}{key}:")
            print_items(value, indent + 1)
        elif isinstance(value, list):
            print(f"{'  ' * indent}{key}:")
            for item in value:
                if isinstance(item, dict):
                    print_items(item, indent + 1)
                else:
                    print(f"{'  ' * (indent + 1)}- {item}")
        else:
            print(f"{'  ' * indent}{key}: {value}")

# Main function
def main():
    """
    Get the JSON file name, open the file, load the JSON data, and print out the key-value pairs.
    """
    try:
        # Get the JSON file name to process
        file_name = get_json_file_name()

        # Open the JSON file
        with open(file_name) as f:
            # Load the JSON data into a Python dictionary
            data = json.load(f)

        # Print out the key-value pairs
        print_items(data)

    except FileNotFoundError:
        print("Error: File not found.")
    except json.JSONDecodeError:
        print("Error: Invalid JSON file.")
    except Exception as e:
        print(f"Error: {str(e)}")

# Call the main function
if __name__ == "__main__":
    main()