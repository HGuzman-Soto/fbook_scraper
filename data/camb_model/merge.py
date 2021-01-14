import pandas as pd

sentences = pd.read_csv('sentences.csv')
word = pd.read_csv('word_features.csv')

test = pd.merge(word, sentences, on=['ID', 'phrase', 'sentence'], how='left')
test = test.drop_duplicates()
test.to_csv("work.csv", index=False)
