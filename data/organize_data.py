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
    df['post id'] = ""
    totalrows = 0
    totalcomments = []         #lists containing all comment threads, all post ids and all posts
    totalids = []
    totalposts = []
    for row in range(len(df)):
        dict_id = df['threads'][row]['id']
        totalids.append(dict_id)
        dict_comments = df['threads'][row]['comments']
        totalcomments.append(dict_comments)
        dict_post = df['threads'][row]['post']
        totalposts.append(dict_post)
    
    iterator = 0                             #variables for adding to the dataframe 
    rownum = 0
    for i in range (0, len(totalposts)) :    #needed this because if post is an image, the array will be empty, which throws an error
        if len(totalposts[i]) == 0 :
            totalposts[i] = ''
            
    for comment in totalcomments :           #make each comment its own row in the dataframe and add the necessary information to that row
        commentnum = 0
        for comm in comment :
            if commentnum == 0 :             #gets rid of duplicating the text of the posts
                addpost = totalposts[iterator]
            else :
                addpost = ''
            df1 = pd.DataFrame({'post': addpost, 'comments': comm, 'post id': totalids[iterator]} , index= [rownum])
            result = df.append(df1)           #append new row to the dataframe
            df = result.copy()
            rownum = rownum + 1
            commentnum = commentnum + 1
        iterator = iterator + 1
    df.drop_duplicates(subset=['comments'], keep='last', inplace=True, ignore_index=True) #drop duplicate comments
    df.drop(columns=['threads'], axis=1, inplace=True)
    if path.exists('data.csv') :
        df.to_csv('data.csv', mode='a', header=False, index=False)
        newdf = pd.read_csv('data.csv')                                   #ensures that duplicate comments are dropped from csv
        newdf.drop_duplicates(subset=['comments'], keep='first',inplace=True, ignore_index=True)   
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


