# import stanza
# #stanza.download('en') # download English model

# nlp = stanza.Pipeline(lang='en', processors='tokenize,mwt,pos')
# doc = nlp('Barack Obama was born in Hawaii.')
# print(*[f'word: {word.text}\tupos: {word.upos}\txpos: {word.xpos}\tfeats: {word.feats if word.feats else "_"}' for sent in doc.sentences for word in sent.words], sep='\n')


import nltk
from nltk import word_tokenize
from nltk import StanfordTagger

text_tok = nltk.word_tokenize("Just a small snippet of text.")


# TODO -
# 1) Make it run in O(n) instead of O(n^2)
# 2) Edge cases --> VBP for instances and so on
# 3) Maybe add its index?
def extract_content_words(text):
    content_words = []

    text_tokenize = nltk.word_tokenize(text)
    text_tagged = nltk.pos_tag(text_tokenize)
    for word, word_class in text_tagged:
        if (word_class == 'NN' or word_class == 'JJ' or word_class == 'RB' or word_class == 'VB'):
            content_words.append(word)
    return content_words
