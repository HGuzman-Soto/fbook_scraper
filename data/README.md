# Instructions

## 1. Run unpack_json.py to unpack json object into proper data format (text, id)

Note: you can either 
        a) manually place the json file in the directory or
        b) run unpack_json.py with --j command to automatically retrieve the last
        downloaded json file from the scraper


## 2. Next, run.py

This will run preprocessing on the text and extract content words using POS tagging and NER. 
It will also attach the starting and ending indexes of each content word



## Columns are identified as such:

text - corresponds to the raw text (string)
id - corresponds to postID_commentID_sentenceID (string)
clean_text - corresponds to the preprocess text (string)
content_word - corresponds to extracted content words (list)
starting_index - corresponds the beginning index of the content word, from the cleaned text
ending_index - corresponds to the ending index of the content word, from the cleaned text


![GitHub Logo](fbook_scraper/diagrams/pipeline_high.png)
