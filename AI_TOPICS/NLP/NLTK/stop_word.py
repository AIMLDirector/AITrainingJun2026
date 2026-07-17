import nltk
from nltk.corpus import stopwords
from nltk import word_tokenize
stop_words = stopwords.words('english')
sentence1 = "This is a sample sentence, showing off the stop words filtration."
word_sentence1 = word_tokenize(sentence1)
print(word_sentence1)
filtered_sentence1 = []

for i in word_sentence1:
    if i not in stop_words:
        filtered_sentence1.append(i)

print(filtered_sentence1)
# filtered_sentence2 = [i for i in word_sentence2 if i not in stop_words]


sentence1 = "This process eliminates the need to manually create and populate the .gitignore file. Ensuring that common project-specific files and folders are automatically excluded from Git tracking."