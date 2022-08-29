from multi_rake import Rake
import pandas as pd

df = pd.read_csv('data/agg-setup-punch-dataset/agg-setup-punch-dataset-test.csv')

rake = Rake(language_code='ru')

for _ in range(10):

    text = df.punch.sample().values[0]
    print('Input: ', text)

    keywords = rake.apply(text)
    print('Keywords: ', keywords[0])