import nltk
from nltk.stem import PorterStemmer, LancasterStemmer,SnowballStemmer, WordNetLemmatizer
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
stop_words = set(stopwords.words("english"))

ps = PorterStemmer()
snowball = SnowballStemmer(language='english')
lanc = LancasterStemmer()

example_words = ["python", "pythonic", "pythoner", "pythoning", "pythoned", "pythonly"]

for w in example_words:
    print(ps.stem(w))

for w in example_words:
    print(snowball.stem(w))