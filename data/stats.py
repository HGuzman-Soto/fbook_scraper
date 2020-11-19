import pandas as pd
from preprocess import clean
from preprocess import remove_entities

from preprocess import extract_content_words


df = pd.read_csv('data.csv')
df['clean_comments'] = df.comments.apply(lambda x: clean(x))
df['clean_comments'] = df.clean_comments.apply(lambda x: remove_entities(x))
df['content_words'] = df.clean_comments.apply(
    lambda x: extract_content_words(x))
