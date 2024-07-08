import matplotlib.pyplot as plt

def get_user_numbers():
    """Gets a list of numbers from the user."""
    numbers_input = input("Enter a list of numbers separated by commas: ")
    try:
        numbers = [float(num) for num in numbers_input.split(',')]
        return numbers
    except ValueError:
        print("Invalid input. Please enter numbers separated by commas.")
        return get_user_numbers()  # Ask for input again

def create_pie_chart(numbers):
    """Creates a pie chart from the given list of numbers."""
    labels = [f"Slice {i + 1}" for i in range(len(numbers))]
    title = input("Enter a title for your pie chart: ")

    background_color = input("Enter a background color for the chart (e.g., white, lightblue): ")
    plt.figure(facecolor=background_color)  # Set background color

    plt.pie(numbers, labels=labels, autopct="%1.1f%%")
    plt.title(title)
    plt.show()

if __name__ == "__main__":
    numbers = get_user_numbers()
    create_pie_chart(numbers)