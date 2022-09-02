import pandas as pd

import spacy
from multi_rake import Rake
rake = Rake(language_code='ru')
nlp = spacy.load("ru_core_news_md")
def get_inspiration(text):
    keywords = rake.apply(text)
    if len(keywords) == 0:
        return ''
    keyword = keywords[0][0]
    lem_keywords = [token.lemma_ for token in nlp(keyword)]
    return ' '.join(lem_keywords)

df = pd.read_csv('data/agg-setup-punch-dataset/agg-setup-punch-dataset-test.csv')
for _ in range(10):
    text = df.punch.sample().values[0]
    print('Input: ', text)
    inspiration = get_inspiration(text)
    print('Inspiration: ', inspiration)