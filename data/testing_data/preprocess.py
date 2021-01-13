"""
Scripts cleans up social media text
"""

from contractions import CONTRACTION_MAP  # from contractions.py
import pandas as pd
import re
import math
import nltk
import spacy
import re
import textstat

from nltk.corpus import stopwords
from nltk import word_tokenize


######################################################################################
"""

Input: String of text
Output: A list of content words from the original cleaned text

Method extracts content words based on if they are a noun, verb, adjective or adverb


Note: I combined the ner step here as 
a) Faster for spacy to do it all at once 
b) Need to remove entity when processing text. We can't remove entities from a list

But, this particular method can only remove entities that are a single token and also performance a bit poor

Look into this for stanford tagger when time permits: https://www.kdnuggets.com/2018/08/named-entity-recognition-practitioners-guide-nlp-4.html
"""


def extract_content_words(text):
    if text != text:
        return text

    nlp = spacy.load("en_core_web_sm", disable=[
                     "parser", "textcat", "tokenizer"])
    doc = nlp(text)
    ents = [e.text for e in doc.ents]

    content_words = []
    for token in doc:
        token_class = token.pos_
        if (token_class == 'NOUN' or token_class == 'VERB' or token_class == 'ADV' or token_class == 'ADJ'):
            # Check if that token is not an entity or function word
            if(token.text not in ents and token.is_stop == False):
                content_words.append(token)
            else:  # this is for testing
                print("Removed word:", token.text, "\n")
    print("content words: ", content_words)
    return content_words

######################################################################################


"""
Input: A string of the cleaned text and a list of a single content word (which are spacy token objects)
Output: The starting and ending indexes of that content word in tuple form
(starting_index, ending_index) ---> mapped to a pd.series

example input: ['I like food'], 'food'
example output: (7, 10) ---> 7, 10

Issues:

1) There are multiple content words, we need to have them be a different column with its own index like in the original data set
   I'm not sure the best approach here. I've not implemented this yet

2) Duplication errors. For instance, if the same word appears multiple time this will always
sget the first occurrence

3) Spacy returns a spacy token. So the list of content words are actually spacy token objects. I need to read up on spacy more

Its been stated that this is not an optimal solution (very memory intensive)


"""


def find_index_cw(clean_text, content_word):
    if (content_word != content_word or clean_text != clean_text):
        return pd.Series([math.nan, math.nan])
    word_tuple = {}
    content_word_str = str(content_word)
    match = re.search(content_word_str, clean_text)

    try:
        indexes = match.span()
    except:
        # change to just get rid of this entry
        return pd.Series([math.nan, math.nan])
    return pd.Series([int(indexes[0]), int(indexes[1])])


######################################################################################
"""
Input: A string of comments that has already been cleaned.
Output: Boolean value that indicates whether to remove(False) or keep(True)

Algorithm - Article inspiration:  https://medium.com/glose-team/how-to-evaluate-text-readability-with-nlp-9c04bd3f46a2
I use text stat package for this: https://pypi.org/project/textstat/

1) Length check (based on characters)
2) Readability score - Flesch-Kincaid
3) Mean number of syllables per word
4) Mean number of words per sentence
5) Number of pollysallables

Additionally: https://towardsdatascience.com/linguistic-complexity-measures-for-text-nlp-e4bf664bd660

Notes:
1) There may be a second filter that we implement that after the content words are extracted, we might say
if theres only 1 content word extracted and its not that signficant, i.e.
    a) The readability score is low
    b) The length is low
    c) etc. etc.

Then just get rid of that entire row

UPDATE: Now that I think about it no. Because we already know that information on the first filter. Like we will know
the number of nouns, verbs, adjectives and adverbs so there is probably no need.

"""


def isValuableComment(clean_text):
    if clean_text != clean_text:
        return False
    print("clean text:", clean_text)
    if (len(clean_text) <= 10):
        return False

    readability_score = textstat.flesch_reading_ease(clean_text)
    syllable_count = textstat.syllable_count(clean_text)

    # Score of 80-90 == easy (from 100 (very easy to hard))
    # if (readability_score > 85):
    #     return False
    # print(readability_score)

    return True


######################################################################################
"""
# Split attached words from https://www.analyticsvidhya.com/blog/2014/11/text-data-cleaning-steps-python/

Potential issues
1) Does see more need a space and a period for a natural break?
2) When removing special characters, sometimes there are special characters
that are needed to convey information such as a guzman-soto or 8.15
This might be a potential issue

3) Skip blank lines?

"""


def clean(text):
    # check if empty (nan) ---> issue??
    if text != text:
        return text

    # remove see more
    text = re.sub(r'[…] ?see more', '', text, flags=re.I)

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

######################################################################################

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

######################################################################################
# from https://towardsdatascience.com/a-practitioners-guide-to-natural-language-processing-part-i-processing-understanding-text-9f4abfd13e72


def remove_special_characters(text, remove_digits=False):
    pattern = r'[^a-zA-z0-9\s]' if not remove_digits else r'[^a-zA-z\s]'
    text = re.sub(pattern, ' ', text)
    return text

######################################################################################
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
######################################################################################
