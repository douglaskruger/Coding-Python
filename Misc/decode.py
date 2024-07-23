import sys

def decode(file_name):
    # Define an array to store the decoded values
    decoded_data = []
    # Variable to count the number of lines
    line_count = 0

    # Open the file
    with open(file_name, 'r') as file:
        # Read each line
        for line in file:
            # Increment line count
            line_count += 1
            # Split the line into number and word
            number, word = line.strip().split()
            # Add the tuple (number, word) to the array
            decoded_data.append((int(number), word))
            
    pyramid = 1
    counter = 1
    result = []  # Initialize result as an empty list
    while pyramid <= line_count:
        # Print the decoded_data where the first tuple value is the pyramid value
        for tuple_value, word in decoded_data:
            if tuple_value == pyramid:
                result.append(word)
                print(tuple_value,counter)
        counter += 1
        pyramid += counter
    return " ".join(result)  # Join the strings with a space between them

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <file_name>")
        sys.exit(1)

    file_name = sys.argv[1]
    decoded_string = decode(file_name)
    print(decoded_string)
