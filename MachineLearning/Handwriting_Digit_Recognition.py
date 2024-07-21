import numpy as np
import matplotlib.pyplot as plt
from tensorflow.keras.datasets import mnist
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Conv2D, MaxPooling2D, Flatten
from tensorflow.keras.optimizers import Adam

# Load the MNIST dataset
# X_train and X_test contain the image data
# y_train and y_test contain the labels (digits 0-9)
(X_train, y_train), (X_test, y_test) = mnist.load_data()

# Preprocess the data
# Reshape the data to include the channel dimension (grayscale images have 1 channel)
X_train = X_train.reshape((X_train.shape[0], 28, 28, 1)).astype('float32')
X_test = X_test.reshape((X_test.shape[0], 28, 28, 1)).astype('float32')

# Normalize the pixel values to be between 0 and 1
X_train /= 255
X_test /= 255

# One-hot encode the labels (e.g., 3 -> [0, 0, 0, 1, 0, 0, 0, 0, 0, 0])
y_train = to_categorical(y_train)
y_test = to_categorical(y_test)

# Define the model
model = Sequential()

# Add the first convolutional layer with 32 filters, 3x3 kernel size, and ReLU activation
# The input shape is (28, 28, 1) which corresponds to the dimensions of the images
model.add(Conv2D(32, (3, 3), activation='relu', input_shape=(28, 28, 1)))

# Add a max pooling layer to reduce the spatial dimensions (2x2 pooling)
model.add(MaxPooling2D((2, 2)))

# Add a second convolutional layer with 64 filters, 3x3 kernel size, and ReLU activation
model.add(Conv2D(64, (3, 3), activation='relu'))

# Add another max pooling layer
model.add(MaxPooling2D((2, 2)))

# Flatten the output from the convolutional layers to prepare it for the dense layers
model.add(Flatten())

# Add a dense (fully connected) layer with 128 units and ReLU activation
model.add(Dense(128, activation='relu'))

# Add the output layer with 10 units (one for each digit) and softmax activation
# Softmax activation is used for multi-class classification problems
model.add(Dense(10, activation='softmax'))

# Compile the model
# Use the Adam optimizer, categorical cross-entropy loss, and accuracy as the metric
model.compile(optimizer=Adam(), loss='categorical_crossentropy', metrics=['accuracy'])

# Train the model
# Train on the training data for 5 epochs with a batch size of 200
# Validate the model on the test data after each epoch
model.fit(X_train, y_train, validation_data=(X_test, y_test), epochs=5, batch_size=200, verbose=2)

# Evaluate the model on the test data
# This will print the test accuracy
test_loss, test_acc = model.evaluate(X_test, y_test, verbose=0)
print(f'Test accuracy: {test_acc:.4f}')

# Visualize the first 10 test images and their predicted labels
# Predict the labels for the test data
predictions = model.predict(X_test)

# Loop through the first 10 test images
for i in range(10):
    # Plot the image using matplotlib
    plt.imshow(X_test[i].reshape(28, 28), cmap='gray')

    # Set the title of the plot to show the true and predicted labels
    plt.title(f"True: {np.argmax(y_test[i])}, Predicted: {np.argmax(predictions[i])}")

    # Remove the axis for better visualization
    plt.axis('off')

    # Display the plot
    plt.show()
