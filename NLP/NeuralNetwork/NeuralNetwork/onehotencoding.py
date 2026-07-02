from sklearn.preprocessing import OneHotEncoder, LabelEncoder, OrdinalEncoder

le = LabelEncoder()
labels = ['cat', 'dog', 'fish', 'cat', 'dog']
integer_encoded = le.fit_transform(labels)
print("Label Encoded:", integer_encoded)


ohe = OneHotEncoder(sparse_output=False)
integer_encoded = integer_encoded.reshape(-1, 1)
onehot_encoded = ohe.fit_transform(integer_encoded)
print("One-Hot Encoded:\n", onehot_encoded)

import pandas as pd
data = ['Low', 'Medium', 'High', 'Medium', 'Low']
df = pd.DataFrame({"colour": data})
ohe1 = pd.get_dummies(df['colour'])
print("One-Hot Encoded using pandas:\n", ohe1)

oe = OrdinalEncoder()
size = [['Small'], ['Medium'], ['Large'], ['Medium'], ['Small']]
ordinal_encoded = oe.fit_transform(size)
print("Ordinal Encoded:\n", ordinal_encoded)

from transformers import AutoTokenizer
tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")
sentences = ["I love programming.", "Transformers are powerful."]
encoded_inputs = tokenizer(sentences, padding=True, truncation=True, return_tensors="pt")
print("Tokenized Inputs:\n", encoded_inputs)
