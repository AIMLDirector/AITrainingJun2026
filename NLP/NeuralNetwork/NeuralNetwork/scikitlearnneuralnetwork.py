from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neural_network import MLPClassifier

vectorization = TfidfVectorizer()

Data = ["The product is very good", "i feel this product is not upto the mark", "very good", "very bad experience"]
label = [1,0,1,0]

X = vectorization.fit_transform(Data).toarray()
print(X.shape)

model = MLPClassifier(hidden_layer_sizes=(100,),activation="relu",max_iter=1000)
model.fit(X,label)


test = ["I like this product"]

X_test = vectorization.transform(test).toarray()
prediction = model.predict(X_test)
print(prediction)



#hidden_layer_sizes=(100,), activation="relu", *, solver="adam", alpha=0.0001, batch_size="auto", learning_rate="constant", learning_rate_init=0.001, power_t=0.5, , shuffle=True, random_state=None, tol=1e-4, verbose=False, warm_start=False, momentum=0.9, nesterovs_momentum=True, early_stopping=False, validation_fraction=0.1, beta_1=0.9, beta_2=0.999, epsilon=1e-8, n_iter_no_change=10, max_fun=15000)

