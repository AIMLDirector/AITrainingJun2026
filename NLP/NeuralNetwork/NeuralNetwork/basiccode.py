import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers

# Generate dummy training data
# X: 2D points, y: labels (0 or 1)
X = np.random.rand(1000, 2)
y = (X[:, 0] + X[:, 1] > 1).astype(int)  # Label = 1 if sum > 1, else 0

# Define a simple neural network
model = keras.Sequential([
    layers.Dense(8, activation="relu", input_shape=(2,)),
    layers.Dense(4, activation="relu"),
    layers.Dense(1, activation="sigmoid")  # Output: probability of class 1
])

# Compile model
model.compile(
    optimizer="adam",
    loss="binary_crossentropy",
    metrics=["accuracy"]
)

# Train model
model.fit(X, y, epochs=20, batch_size=16, verbose=1)

# Test prediction
test_point = np.array([[0.9, 0.2]])
prediction = model.predict(test_point)

print(f"Predicted class: {int((prediction > 0.5).item())}, Probability: {prediction[0][0]:.4f}")
# print(f"Predicted class: {int(prediction > 0.5)}, Probability: {prediction[0][0]:.4f}")
