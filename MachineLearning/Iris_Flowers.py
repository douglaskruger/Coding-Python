import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
import seaborn as sns

# Load the Iris dataset
# This dataset contains 150 samples of iris flowers with 4 features and a target label
iris = load_iris()
X = iris.data  # Features: sepal length, sepal width, petal length, petal width
y = iris.target  # Target: species of iris (Setosa, Versicolour, or Virginica)
feature_names = iris.feature_names
target_names = iris.target_names

# Convert to DataFrame for easier manipulation and visualization
df = pd.DataFrame(X, columns=feature_names)
df['species'] = y

# Split the dataset into training and testing sets
# 80% of the data will be used for training and 20% for testing
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train a Logistic Regression model
# Logistic Regression is a simple yet powerful linear model for classification
model = LogisticRegression(max_iter=200)  # max_iter is increased to ensure convergence
model.fit(X_train, y_train)  # Train the model on the training data

# Predict on the test set
y_pred = model.predict(X_test)  # Use the trained model to make predictions on the test set

# Evaluate the model
accuracy = accuracy_score(y_test, y_pred)  # Calculate the accuracy of the model
conf_matrix = confusion_matrix(y_test, y_pred)  # Generate the confusion matrix
class_report = classification_report(y_test, y_pred, target_names=target_names)  # Generate the classification report

# Print evaluation metrics
print(f"Accuracy: {accuracy:.2f}")
print("\nConfusion Matrix:")
print(conf_matrix)
print("\nClassification Report:")
print(class_report)

# Visualize the results
# Confusion Matrix
plt.figure(figsize=(8, 6))
sns.heatmap(conf_matrix, annot=True, fmt='d', cmap='Blues', xticklabels=target_names, yticklabels=target_names)
plt.xlabel('Predicted')
plt.ylabel('Actual')
plt.title('Confusion Matrix')
plt.show()


# Function to plot decision boundaries for the first two features
def plot_decision_boundaries(X, y, model, feature_names):
    x_min, x_max = X[:, 0].min() - 1, X[:, 0].max() + 1
    y_min, y_max = X[:, 1].min() - 1, y[:, 1].max() + 1
    xx, yy = np.meshgrid(np.arange(x_min, x_max, 0.02),
                         np.arange(y_min, y_max, 0.02))

    # Predict the class for each point in the meshgrid
    Z = model.predict(np.c_[xx.ravel(), yy.ravel()])
    Z = Z.reshape(xx.shape)

    # Plot the decision boundaries and the data points
    plt.figure(figsize=(10, 6))
    plt.contourf(xx, yy, Z, alpha=0.3)  # Contour plot for the decision boundaries
    plt.scatter(X[:, 0], X[:, 1], c=y, edgecolors='k', marker='o', s=100)  # Scatter plot for the data points
    plt.xlabel(feature_names[0])
    plt.ylabel(feature_names[1])
    plt.title('Decision Boundaries')
    plt.show()

# Train a new model using only the first two features for visualization
model_2d = LogisticRegression(max_iter=200)
model_2d.fit(X_train[:, :2], y_train)
plot_decision_boundaries(X_test[:, :2], y_test, model_2d, feature_names[:2])
