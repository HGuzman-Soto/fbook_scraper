import os
import time
import glob
import shutil
import multiprocessing
import pandas as pd
from dask import dataframe as dd
from dask.multiprocessing import get
from preprocess import clean
from preprocess import extract_content_words
from preprocess import find_index_cw
from preprocess import isValuableComment
from os import path
from pathlib import Path

start_time = time.time()
df = pd.read_csv('temp_data.csv')
df = df[1000:1500]

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

df['clean_text'] = df.text.apply(lambda x: clean(x))

df = df[df.clean_text.apply(lambda x: isValuableComment(x)) == True]
meta = ('content_word', 'object')
# convert to dask dataframe and call extract_content_words()
df = dd.from_pandas(df, npartitions=16)
df['content_word'] = df.map_partitions(lambda df: df.clean_text.apply(
    lambda x: extract_content_words(x)), meta=meta).compute(num_workers=4)

print("\n")
print("Expanding content word lists \n")
df = df.explode('content_word')


print("Attaching indexes to each content words \n")
df[['starting_index', 'ending_index']] = df.apply(lambda x: find_index_cw(
    x.clean_text, x.content_word), axis=1)

df.to_csv('dask_data.csv', index=False)
print("Finished")
print("--- %s seconds ---" % (time.time() - start_time))

# get path to directory with part files
script_path = os.path.abspath(__file__)
script_dir = os.path.split(script_path)[0]
rel_path = "dask_data.csv"
rel_path2 = "main.csv"
abs_file_path = os.path.join(script_dir, rel_path)
rem_file_path = os.path.join(script_dir, rel_path2)
# convert part files to csv files
os.chdir(abs_file_path)
extension = 'part'
all_filenames1 = [i for i in glob.glob('*.{}'.format(extension))]
count = 0
for f in all_filenames1:
    read_file = pd.read_csv(f)
    read_file.to_csv('file' + str(count) + '.csv', index=None)
    count = count + 1
# concat all csv files into one
extension = 'csv'
all_filenames = [i for i in glob.glob('*.{}'.format(extension))]
combined_csv = pd.concat([pd.read_csv(f) for f in all_filenames])
combined_csv.to_csv("new.csv", index=False, encoding='utf-8-sig')
# move main.csv up a directory and delete data.csv directory
script_path = os.path.abspath(__file__)
script_dir = os.path.split(script_path)[0]
rel_path = "new.csv"
filePath = os.path.join(script_dir, rel_path)
os.chdir("..")
folderPath = os.getcwd()
shutil.copy(filePath, folderPath)
shutil.rmtree(abs_file_path)
shutil.rmtree(rem_file_path)
# convert combined csv file to dataframe
df = pd.read_csv("new.csv")
# create or combine data.csv
if path.exists('dask_data.csv'):
    df.to_csv('dask_data.csv', mode='a', header=False, index=False)
    # os.remove('temp_data.csv')

else:
    df.to_csv('dask_data.csv', index=False)
    # os.remove('temp_data.csv')
os.remove('new.csv')
