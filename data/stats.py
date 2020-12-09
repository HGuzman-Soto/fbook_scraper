import pandas as pd
from preprocess import clean
from preprocess import extract_content_words
from preprocess import find_index_cw
from preprocess import isValuableComment
from os import path
from pathlib import Path

df = pd.read_csv('data.csv')
df = df[0:500]

df['clean_comments'] = df.text.apply(lambda x: clean(x))

df = df[df.clean_comments.apply(lambda x: isValuableComment(x)) == True]


df['content_words'] = df.clean_comments.apply(
    lambda x: extract_content_words(x))

df['index'] = df.apply(lambda x: find_index_cw(
    x.clean_comments, x.content_words), axis=1)


if path.exists('data_clean.csv'):
    df.to_csv('data_clean.csv', mode='a', header=False, index=False)
else:
    df.to_csv('data_clean.csv',  index=False)
