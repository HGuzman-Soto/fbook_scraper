"""
Script takes json objects from chrome extension and organizes the data into a csv files

"""
from pathlib import Path
from os import path
import re
import shutil
import os.path
import argparse
import csv
import ast
import pandas as pd
import json
import nltk
from nltk.tokenize import sent_tokenize
# nltk.download('punkt') run once


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


def main():
    json_file = get_jsonfile()

    df = pd.read_json(json_file, orient='DataFrame')
    df['text'] = ""
    df['id'] = ""

    totalrows = 0
    totalcomments = []  # lists containing all comment threads, all post ids and all posts
    totalids = []
    totalcommid = []
    totalposts = []
    for row in range(len(df)):
        dict_id = df['threads'][row]['id']
        totalids.append(dict_id)
        dict_commentid = df['threads'][row]['commentid']
        totalcommid.append(dict_commentid)
        dict_comments = df['threads'][row]['comments']
        totalcomments.append(dict_comments)
        dict_post = df['threads'][row]['post']
        totalposts.append(dict_post)

    iterator = 0  # variables for adding to the dataframe
    rownum = 0
    # needed this because if post is an image, the array will be empty, which throws an error
    for i in range(0, len(totalposts)):
        if len(totalposts[i]) == 0:
            totalposts[i] = ''

    for comment in totalcomments:  # make each comment its own row in the dataframe and add the necessary information to that row
        addpost = totalposts[iterator]
        postlist = sent_tokenize(str(addpost))
        sentcount = 1
        for item in postlist:
            df2 = pd.DataFrame({'post': 0, 'text': item, 'id': str(
                iterator) + "_" + str(0) + "_" + str(sentcount)}, index=[rownum])
            result2 = df.append(df2)  # append new row to the dataframe
            df = result2.copy()
            rownum = rownum + 1
            sentcount = sentcount + 1
        commentnum = 1
        for comm in comment:
            sentnum = 1
            commlist = sent_tokenize(comm)
            for element in commlist:
                df1 = pd.DataFrame({'post': 0, 'text': element, 'id': str(
                    iterator) + "_" + str(commentnum) + "_" + str(sentnum)}, index=[rownum])
                result = df.append(df1)  # append new row to the dataframe
                df = result.copy()
                rownum = rownum + 1
                sentnum = sentnum + 1
            commentnum = commentnum + 1
        iterator = iterator + 1

    # drop duplicate comments
    df.drop_duplicates(subset=['text'], keep='last',
                       inplace=True, ignore_index=True)
    df.drop(columns=['threads'], axis=1, inplace=True)
    df.drop(columns=['post'], axis=1, inplace=True)
    if path.exists('temp_data.csv'):
        df.to_csv('temp_data.csv', mode='a', header=False, index=False)
        # ensures that duplicate comments are dropped from csv
        newdf = pd.read_csv('temp_data.csv')
        newdf.drop_duplicates(
            subset=['text'], keep='first', inplace=True, ignore_index=True)
        newdf.to_csv('temp_data.csv', index=False)
    else:
        df.to_csv('temp_data.csv', index=False)

    shutil.move(json_file,
                "json_files/")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Organize json data')
    parser.add_argument('--json', '--j', type=int, default=0)

    args = parser.parse_args()
    if (args.json == 1):
        find_jsonfile()
    main()
