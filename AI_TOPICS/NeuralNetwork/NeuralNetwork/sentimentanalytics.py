# Customer Review Sentiment Analysis

# Concept: Analyzes customer product reviews to detect positive or negative sentiment in real time.
# Business Value: Flags low-rated products quickly, helps improve quality, enhances customer experience.
# Coding Side:

# Preprocessed review text with Tokenizer and padded to equal length.
# Neural net with Embedding + GRU layers for sequential context.
#  Trained with binary crossentropy since output is positive/negative.

import numpy as np
from tensorflow import keras
from tensorflow.keras import layers

# Example reviews
reviews = [
    "The shoes are very comfortable and stylish",
    "Terrible quality, broke in 2 days",
    "Loved the packaging and quick delivery"
]
labels = np.array([1, 0, 1])   # <-- FIX: ensure NumPy array

# Tokenization
tokenizer = keras.preprocessing.text.Tokenizer(num_words=5000)
tokenizer.fit_on_texts(reviews)
X = tokenizer.texts_to_sequences(reviews)
X = keras.preprocessing.sequence.pad_sequences(X, maxlen=30)

# Model (removed input_length)
model = keras.Sequential([
    layers.Embedding(5000, 32),
    layers.GRU(32),
    layers.Dense(1, activation="sigmoid")
])

model.compile(optimizer="adam", loss="binary_crossentropy", metrics=["accuracy"])

# Train
model.fit(X, labels, epochs=5, verbose=1)

# Real-time prediction
new_review = ["The product is overpriced and not worth it"]
X_new = tokenizer.texts_to_sequences(new_review)
X_new = keras.preprocessing.sequence.pad_sequences(X_new, maxlen=30)
print("Sentiment score:", model.predict(X_new)[0][0])


# data - 70 /30.  80/20 - structure and unstructure 
# labelling 
# model -- configuration 
# model parameters -  epochs, batch size, learning rate, optimizer, loss function
# model training
# model evaluation 
# model deployment

# llm model and publish - 

#Nlp + neural network + transformer  == LLM model 

# 1. google ( 2500 crores)
# 2. facebook
# 3. nvidia
# 4. alibaba
# 5. anthropic

