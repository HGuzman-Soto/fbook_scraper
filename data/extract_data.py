import pandas as pd

import re
import collections

"""For simple wikipedia

1) Convert text file to csv, set columns to [word,frequency,sentence]
2) Read that csv file to pandas again
3) Get the top 6,386 words 


"""


def simple_wiki():
    colnames = ['word', 'frequency', 'sentence']
    df_wiki = pd.read_table('camb_model/corpus/simple.txt',
                            names=colnames, header=None)

    df_top_words = df_wiki.groupby(
        ['word']).sum().sort_values('frequency').nlargest(6386, 'frequency')
    print(df_top_words)

    # make csv file


"""
For subtitles

1) Use collection dictionaries to map each word to a frequency
2) Turn this into a pandas dataframe
3) Keep the top 1000 word frequencies


"""


def subtitles():

    words = re.findall(
        '\w+', open('camb_model/binary-features/subtitles.txt').read().lower())

    word_dict = collections.Counter(words)
    df = pd.DataFrame.from_dict(
        word_dict, orient='index', columns=['frequency'])

    # filter and keep top 1000 word frequency

    df.to_csv("test.csv", index=True)
    # make csv file
    # print(df)


# simple_wiki()
subtitles()
