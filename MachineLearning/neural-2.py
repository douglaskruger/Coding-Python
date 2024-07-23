import numpy as np

# Sigmoid function
def sigmoid(x):
    return 1 / (1 + np.exp(-x))

# Derivative of sigmoid function
def sigmoid_derivative(x):
    return x * (1 - x)

# Input datasets
X = np.array([[0, 0], [0, 1], [1, 0], [1, 1]])

# Output datasets
y = np.array([[0], [1], [1], [0]])

# Seed random numbers to make calculation deterministic
np.random.seed(1)

# Weights initialization
weights0 = 2 * np.random.random((2, 2)) - 1
weights1 = 2 * np.random.random((2, 1)) - 1

# Training loop
for i in range(20000):
    # Feedforward
    layer0 = X
    layer1 = sigmoid(np.dot(layer0, weights0))
    layer2 = sigmoid(np.dot(layer1, weights1))

    # Backpropagation
    layer2_error = y - layer2
    layer2_delta = layer2_error * sigmoid_derivative(layer2)
    layer1_error = layer2_delta.dot(weights1.T)
    layer1_delta = layer1_error * sigmoid_derivative(layer1)

    # Update weights
    weights1 += layer1.T.dot(layer2_delta)
    weights0 += layer0.T.dot(layer1_delta)

print("Final Hidden Weights: ")
print(weights0)
print("Final Hidden Bias: ")
print(weights1)

print("[0, 0] = ", end='')
print(round(sigmoid(np.dot(sigmoid(np.dot([0, 0], weights0)), weights1))[0]))
print("[0, 1] = ", end='')
print(round(sigmoid(np.dot(sigmoid(np.dot([0, 1], weights0)), weights1))[0]))
print("[1, 0] = ", end='')
print(round(sigmoid(np.dot(sigmoid(np.dot([1, 0], weights0)), weights1))[0]))
print("[1, 1] = ", end='')
print(round(sigmoid(np.dot(sigmoid(np.dot([1, 1], weights0)), weights1))[0]))
