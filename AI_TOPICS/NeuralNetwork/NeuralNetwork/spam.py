# Spam Email Detection

# Concept: Classifies emails into spam vs. not spam. Helps block phishing and junk before 
# reaching inboxes.Business Value: Improves security, reduces employee distraction, prevents 
# financial risk.

#  Coding Side:

# Used Tokenizer + pad_sequences to convert text into numeric form.
# Neural net with Embedding + LSTM layers for sequence understanding.
# Labels ([1,0,1]) stored as NumPy arrays for compatibility with Keras.

import numpy as np
from tensorflow import keras
from tensorflow.keras import layers

# Example email dataset
emails = [
    "Win a free iPhone now!!!",  # win, free, now - spam indicators
    "Meeting at 10am in conference room",
    "Claim your lottery prize" # claim , prize - spam indicators
]
labels = np.array([1, 0, 1])  # <-- Convert to NumPy array

# Tokenize & pad
tokenizer = keras.preprocessing.text.Tokenizer(num_words=5000)
tokenizer.fit_on_texts(emails)
X = tokenizer.texts_to_sequences(emails)
X = keras.preprocessing.sequence.pad_sequences(X, maxlen=50)

# Model
model = keras.Sequential([
    layers.Embedding(5000, 32),   # removed input_length
    layers.LSTM(32),
    layers.Dense(1, activation="sigmoid")
])

model.compile(optimizer="adam", loss="binary_crossentropy", metrics=["accuracy"])

#QA test engineer: 

#ADAM - Text data( NLP, RNN, LLM)  - Fast  - Weight and bias 
#SGD  - CNN, simple machine learning models  - Slow    

# Train
model.fit(X, labels, epochs=2, verbose=1)

# Real-time test
new_email = ["Urgent: you win a prize please register with your mobile number "]
X_new = tokenizer.texts_to_sequences(new_email)
X_new = keras.preprocessing.sequence.pad_sequences(X_new, maxlen=50)
print("Spam probability:", model.predict(X_new)[0][0])
