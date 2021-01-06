import pandas as pd


df = pd.read_csv('data.csv')

column_names = ['id', 'sentence', 'start', 'end', 'word']
df = df.reindex(columns=column_names)
print(df.head())

df.to_csv('test_data.tsv', header=False, sep='\t')
