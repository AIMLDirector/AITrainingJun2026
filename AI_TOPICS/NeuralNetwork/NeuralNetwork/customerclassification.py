# Customer Support Chat Intent Detection
# Concept: Detects customer query intent (billing, tech support, cancellation) to auto-route tickets.
# Business Value: Reduces manual triage, speeds up support, lowers costs, improves satisfaction.
# Coding Side:

# Encoded intents into sequences with Tokenizer.
# Used Embedding + Dense layers (multi-class classification).
# Trained with sparse_categorical_crossentropy since labels are integers (0,1,2).
# Predictions return a class index (argmax) which maps back to intent.

import numpy as np
from tensorflow import keras
from tensorflow.keras import layers

# # Example training data
# intents = [
#     "I want to cancel my subscription",
#     "My internet is not working properly",
#     "How can I update my billing address?"
# ]
# labels = np.array([0, 1, 2])  # 0=cancel, 1=tech support, 2=billing


intents = [
    "cancel sub", "stop my service", "end subscription", # Label 0
    "internet down", "wifi slow", "router broken",      # Label 1
    "change card", "new billing address", "update pay"   # Label 2
]
labels = np.array([0, 0, 0, 1, 1, 1, 2, 2, 2])
# Tokenization
tokenizer = keras.preprocessing.text.Tokenizer(num_words=5000)
tokenizer.fit_on_texts(intents)
X = tokenizer.texts_to_sequences(intents)
X = keras.preprocessing.sequence.pad_sequences(X, maxlen=20)

# Model (no input_length)
model = keras.Sequential([
    layers.Embedding(5000, 32),
    layers.Flatten(),
    layers.Dense(32, activation="relu"),
    layers.Dense(3, activation="softmax")  # 3 classes
])

model.compile(optimizer="adam",
              loss="sparse_categorical_crossentropy",
              metrics=["accuracy"])

# Train
model.fit(X, labels, epochs=15, verbose=1)

# --- Real-time test ---
new_query = ["payment gateway"]
X_new = tokenizer.texts_to_sequences(new_query)
X_new = keras.preprocessing.sequence.pad_sequences(X_new, maxlen=20)
pred = model.predict(X_new)

print("Predicted intent:", pred.argmax())  # 0=cancel, 1=tech, 2=billing
