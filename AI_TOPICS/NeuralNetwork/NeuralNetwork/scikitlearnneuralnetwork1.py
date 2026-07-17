from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neural_network import MLPClassifier
from sklearn.pipeline import Pipeline
import joblib

vectorization = TfidfVectorizer()

Data = ["win money now", "Limited offer click here", "hello friend how are you", "congratulations you won a prize", "important update about you account", "Let us meet tomorrow"]
label = [1,1,0,1,0,0]
label1 = ["external", "internal" ]

X = vectorization.fit_transform(Data).toarray()
print(X.shape)

model = MLPClassifier(hidden_layer_sizes=(10,),max_iter=1000)
model.fit(X,label)

joblib.dump(model, "model.pkl")

test_sample = ["win a free phone now", "meeting schedule tomorrow"]

X_test = vectorization.transform(test_sample).toarray()
prediction = model.predict(X_test)
print(prediction)
for email , pred in zip(test_sample, prediction):
    print(email, '->', "Spam" if pred == 1 else "Not Spam")


model1 = joblib.load("model.pkl")

# print(model1.predict(["won a prize"]))

from cryptography.fernet import Fernet
key = Fernet.generate_key()
print(key)
