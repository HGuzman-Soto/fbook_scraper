"""
Script takes json objects from chrome extension and organizes the data into a csv files

"""

import json
import pandas as pd
import ast
import csv
import argparse
import os.path
import shutil
import re

from os import path
from pathlib import Path


"""
To add to existing json file, use the argument --a 1
To retrieve json file, use the argument --j 1

"""


def get_jsonfile():
    for files in os.listdir():
        if files.endswith('.json'):
            return files


def find_jsonfile():
    path_to_download_folder = str(os.path.join(Path.home(), "Downloads"))
    RootDir1 = path_to_download_folder
    TargetFolder = os.getcwd()

    for root, dirs, files in os.walk((os.path.normpath(RootDir1)), topdown=False):

        max_num = 0
        max_name = ''
        matches = ['.json', 'threads']
        for name in files:
            # base case
            if all(x in name for x in matches):

                # # copies file to target folder
                current_digit = re.findall(r'\d+', name)
                print(current_digit)

                # check that a digit exists - else turn to int
                if not current_digit:
                    continue
                else:
                    current_digit = int(current_digit[0])

                if (current_digit > max_num):
                    max_num = current_digit
                    max_name = name

    if (max_num == 0):
        max_name = 'threads.json'

    SourceFolder = os.path.join(root, max_name)
    shutil.copy2(SourceFolder, TargetFolder)


def main(add):
    json_file = get_jsonfile()

    df = pd.read_json(json_file, orient='DataFrame')

    df['post'] = ""
    df['comments'] = ""
    for row in range(len(df)):
        dict_comments = df['threads'][row]['comments']
        dict_post = df['threads'][row]['post']

        df['comments'][row] = " ".join(dict_comments)
        df['post'][row] = " ".join(dict_post)

    df.drop(columns=['threads'], axis=1, inplace=True)
    df.drop_duplicates(subset=['post'], keep='last',
                       inplace=True, ignore_index=True)

    if path.exists('data.csv') :
        df.to_csv('data.csv', mode='a', header=False, index=False)
        newdf = pd.read_csv('data.csv')
        newdf.drop_duplicates(subset=['post'], keep='first',inplace=True, ignore_index=True)
        newdf.to_csv('data.csv', index=False)
    else:
        df.to_csv('data.csv', index=False)

    os.remove(json_file)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Organize json data')
    parser.add_argument('--json', '--j', type=int, default=0)
    parser.add_argument('--add', '--a', type=int, default=0,
                        help='add to exisitng data file')

    args = parser.parse_args()
    if (args.json == 1):
        find_jsonfile()

    main(args.add)


