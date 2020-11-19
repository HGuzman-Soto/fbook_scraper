"""
Scripts cleans up social media text
"""

from contractions import CONTRACTION_MAP  # from contractions.py
import pandas as pd
import re
import nltk
from nltk.corpus import stopwords


# Split attached words from https://www.analyticsvidhya.com/blog/2014/11/text-data-cleaning-steps-python/
"""
Potential issues
1) Does see more need a space and a period for a natural break?
2) When removing special characters, sometimes there are special characters
that are needed to convey information such as a guzman-soto or 8.15
This might be a potential issue

"""


def clean(text):

    # remove see more
    text = re.sub(r' ?\w*?[…]see more.', '', text, flags=re.I)

    # remove urls
    text = re.sub(r'http:?\S+|www.\S+', '', text)

    # remove emojis
    text = remove_emoji(text)

    # swap single right quotes for aposrophes
    text = re.sub(r'’', "'", text)

    # all lower case
    text = "".join([w.lower() for w in text])

    # expand contractions
    text = expand_contractions(text)

    # remove special characters
    text = remove_special_characters(text)

    # remove extra newlines
    text = re.sub(r'[\r|\n|\r\n]+', ' ', text)

    # remove extra whitespace
    text = re.sub(' +', ' ', text)

    return text

# From https://gist.github.com/slowkow/7a7f61f495e3dbb7e3d767f97bd7304b below


def remove_emoji(string):
    emoji_pattern = re.compile("["
                               u"\U0001F600-\U0001F64F"  # emoticons
                               u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                               u"\U0001F680-\U0001F6FF"  # transport & map symbols
                               u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                               u"\U00002500-\U00002BEF"  # chinese char
                               u"\U00002702-\U000027B0"
                               u"\U00002702-\U000027B0"
                               u"\U000024C2-\U0001F251"
                               u"\U0001f926-\U0001f937"
                               u"\U00010000-\U0010ffff"
                               u"\u2640-\u2642"
                               u"\u2600-\u2B55"
                               u"\u200d"
                               u"\u23cf"
                               u"\u23e9"
                               u"\u231a"
                               u"\ufe0f"  # dingbats
                               u"\u3030"
                               "]+", flags=re.UNICODE)
    return emoji_pattern.sub(r'', string)


# from https://towardsdatascience.com/a-practitioners-guide-to-natural-language-processing-part-i-processing-understanding-text-9f4abfd13e72
def remove_special_characters(text, remove_digits=False):
    pattern = r'[^a-zA-z0-9\s]' if not remove_digits else r'[^a-zA-z\s]'
    text = re.sub(pattern, ' ', text)
    return text


# from https://towardsdatascience.com/nlp-building-text-cleanup-and-preprocessing-pipeline-eba4095245a0


def expand_contractions(text, map=CONTRACTION_MAP):
    pattern = re.compile('({})'.format('|'.join(map.keys())),
                         flags=re.IGNORECASE | re.DOTALL)

    def get_match(contraction):
        match = contraction.group(0)
        first_char = match[0]
        expanded = map.get(match) if map.get(match) else map.get(match.lower())
        expanded = first_char+expanded[1:]
        return expanded
    new_text = pattern.sub(get_match, text)
    new_text = re.sub("'", "", new_text)
    return new_text
