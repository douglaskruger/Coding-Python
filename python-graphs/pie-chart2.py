import matplotlib.pyplot as plt

# Get the numbers from the user
data_str = input("Enter a list of numbers separated by commas: ")
data = [float(x) for x in data_str.split(',')]

# Create labels (optional)
labels = ["Slice " + str(i + 1) for i in range(len(data))]

# Create the pie chart
plt.pie(data, labels=labels, autopct="%1.1f%%")
plt.title("Pie Chart of User Input")
plt.show()