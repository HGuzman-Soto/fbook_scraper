import pandas as pd
from preprocess import clean
from preprocess import extract_content_words
from preprocess import find_index_cw
from preprocess import isValuableComment
from os import path
from pathlib import Path

df = pd.read_csv('data.csv')


"""todo
1) rename this file
2) Use spacy.pipe() for all these processes/maybe the preprocess.py file to make things faster


Steps
1) We clean our social media data --> clean_comments
2) We apply a small heuristic to remove rows with less than 10 characters
3) As an intermediate step, we generate a list of all content words for each text
4) Then, using this list, we attach each word as a seperate row --> content_word
5) Finally, we attach the indexes, which are represented as a tuple --> index

"""


df['clean_comments'] = df.text.apply(lambda x: clean(x))

df = df[df.clean_comments.apply(lambda x: isValuableComment(x)) == True]


df['content_word'] = df.clean_comments.apply(
    lambda x: extract_content_words(x))

df = df.explode('content_word')

df['index'] = df.apply(lambda x: find_index_cw(
    x.clean_comments, x.content_word), axis=1)


if path.exists('data_clean.csv'):
    df.to_csv('data_clean.csv', mode='a', header=False, index=False)
else:
    df.to_csv('data_clean.csv',  index=False)
