from detoxify import Detoxify
import pandas as pd

# Define input texts
input_text = [
    'i hate south indian people',
    'example text 1',
    'example text 2',
    'example text',
    'exemple de texte',
    'texto de ejemplo',
    'testo di esempio',
    'texto de exemplo',
    'örnek metin',
    'пример текста'
]

default_score = {
    'toxicity': 0.5,
    'severe_toxicity': 0.5,
    'obscene': 0.5,
    'threat': 0.5,
    'insult': 0.5,
    'identity_attack': 0.5
}
model = Detoxify('multilingual')

for i in input_text:
    results = model.predict(i)
    print(results)
    if results['toxicity'] > default_score['toxicity']:
        print(f"Flagged as toxic: {i}")
        # exit()
    elif results['severe_toxicity'] > default_score['severe_toxicity']:
        print(f"Flagged as severely toxic: {i}")
        # exit()
    elif results['obscene'] > default_score['obscene']:
        print(f"Flagged as obscene: {i}")
    elif results['threat'] > default_score['threat']:
        print(f"Flagged as threat: {i}")
    else:
        print(f"Safe: {i}")

# df = pd.DataFrame(results, index=input_text)
# print(df.round(5))