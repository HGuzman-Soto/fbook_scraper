import pandas as pd
from preprocess import clean
from preprocess import remove_entities
from preprocess import extract_content_words
from os import path
from pathlib import Path

df = pd.read_csv('data.csv')
df['clean_comments'] = df.text.apply(lambda x: clean(x))
# df['clean_comments'] = df.clean_comments.apply(lambda x: remove_entities(x))
df['content_words'] = df.clean_comments.apply(
    lambda x: extract_content_words(x))

if path.exists('data_clean.csv'):
    df.to_csv('data_clean.csv', mode='a', header=False, index=False)
else:
    df.to_csv('data_clean.csv',  index=False)
