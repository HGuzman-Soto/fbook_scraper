# Adapted from: https://github.com/siangooding/cwi_2018/blob/master/Populating%20Word%20Features.ipynb
# Populating word Features
import pandas as pd
import numpy
import string
import regex as re


# Load the data set that needs populating
# wikinews done, News_test_complete, Wikipedia_Test_complete, Wikipedia_Train
##########################################################################################################

Wikinews = True

array = ['WikiNews_Train', 'WikiNews_Test']

for x in array:

    location = 'actual-test-sets/'+x+'.tsv'
    data_frame = pd.read_table(location, names=('ID', 'sentence', 'start_index', 'end_index', 'phrase', 'total_native',
                                                'total_non_native', 'native_complex', 'non_native_complex', 'complex_binary', 'complex_probabilistic'))

    data_frame['split'] = data_frame['phrase'].apply(lambda x: x.split())

    data_frame['count'] = data_frame['split'].apply(lambda x: len(x))

    # We create a table that contains only the words
    words = data_frame[data_frame['count'] == 1]

    word_set = words.phrase.str.lower().unique()

    word_set = pd.DataFrame(word_set)
    word_set.columns = ['phrase']


##########################################################################################################
    # Cleaning function for words
    remove = string.punctuation
    remove = remove.replace("-", "")
    remove = remove.replace("'", "")  # don't remove apostraphies
    remove = remove + '“'
    remove = remove + '”'
    pattern = r"[{}]".format(remove)  # create the pattern
    word_set['phrase'] = word_set['phrase'].apply(
        lambda x: x.translate({ord(char): None for char in remove}))

##########################################################################################################
    # function to obtain syablles for words
    from datamuse import datamuse
    api = datamuse.Datamuse()

    def get_syllables(word):
        syllables = 0
        word_results = api.words(sp=word, max=1, md='psf')
        if len(word_results) > 0:
            word = word_results[0]["word"]
            syllables = int(word_results[0]["numSyllables"])
        return syllables

    # Apply function to get syllables
    word_set['syllables'] = word_set['phrase'].apply(
        lambda x: get_syllables(x))

    # Apply function to get word length
    word_set['length'] = word_set['phrase'].apply(lambda x: len(x))

    # take words and merge with values first you will need to clean the phrase column
    words['original phrase'] = words['phrase']
    words['phrase'] = words['phrase'].str.lower()
    words['phrase'] = words['phrase'].apply(
        lambda x: x.translate({ord(char): None for char in remove}))

    word_features = pd.merge(words, word_set)


##########################################################################################################

    # Now parse
    import pycorenlp
    import pandas as pd
    from pycorenlp import StanfordCoreNLP
    nlp = StanfordCoreNLP('http://localhost:9000')

    sentences = data_frame[['sentence', 'ID']].copy()

    sentences = sentences.drop_duplicates()

##########################################################################################################

    def removefirsttoken(x):
        x = x.split(' ', 1)[1]
        return x

    if Wikinews:
        sentences['clean sentence'] = sentences['sentence'].apply(
            lambda x: removefirsttoken(x))

    else:
        sentences['clean sentence'] = sentences['sentence']

##########################################################################################################

    # function to parse sentences
    def parse(string):
        output = nlp.annotate(string, properties={
            'annotators': 'pos,depparse',
            'outputFormat': 'json'
        })
        return output

    # apply parsing to sentences
    sentences['parse'] = sentences['clean sentence'].apply(lambda x: parse(x))

    # Merge
    word_parse_features = pd.merge(sentences, word_features)

##########################################################################################################

    # Work out POS and dep number for words in word_parse_features
    def get_pos(row):
        word = row['phrase']
        parse = row['parse']
        for i in range(len(parse['sentences'][0]['tokens'])):

            comp_word = parse['sentences'][0]['tokens'][i]['word']
            comp_word = comp_word.lower()
            comp_word = comp_word.translate(
                {ord(char): None for char in remove})

            if comp_word == word:
                return parse['sentences'][0]['tokens'][i]['pos']

##########################################################################################################

    def get_dep(row):
        number = 0
        word = row['phrase']
        parse = row['parse']
        for i in range(len(parse['sentences'][0]['basicDependencies'])):
            comp_word = parse['sentences'][0]['basicDependencies'][i]['governorGloss']
            comp_word = comp_word.lower()
            comp_word = comp_word.translate(
                {ord(char): None for char in remove})

            if comp_word == word:
                number += 1

        return number

##########################################################################################################

    # Function to get the proper lemma

    from nltk.corpus import wordnet

    def get_wordnet_pos(treebank_tag):

        if treebank_tag.startswith('J'):
            return wordnet.ADJ
        elif treebank_tag.startswith('V'):
            return wordnet.VERB
        elif treebank_tag.startswith('N'):
            return wordnet.NOUN
        elif treebank_tag.startswith('R'):
            return wordnet.ADV
        else:
            return None

##########################################################################################################

    from nltk.stem import WordNetLemmatizer
    wordnet_lemmatizer = WordNetLemmatizer()

##########################################################################################################

    def lemmatiser(row):

        word = row['phrase']
        pos = row['pos']

        try:
            lemma = wordnet_lemmatizer.lemmatize(word, get_wordnet_pos(pos))
            return lemma
        except:
            try:
                lemma = wordnet_lemmatizer.lemmatize(word)
                return lemma
            except:
                print(word)
##########################################################################################################

    # return MRC scores
    mrc_features = pd.read_table('corpus/MRC.tsv', names=('word', 'AOA', 'BFRQ', 'CNC',
                                                          'KFCAT', 'FAM', 'KFSMP', 'IMG', 'KFFRQ', 'NLET', 'CMEAN', 'PMEAN', 'NPHN', 'T-LFRQ'))

##########################################################################################################

    def aoa(word):
        word = ''.join(word.split()).lower()
        try:
            df = mrc_features.loc[mrc_features['word'] == word]
            fvalue = df.iloc[0]['AOA']
            return fvalue
        except:
            return 0
##########################################################################################################

    def cnc(word):
        word = ''.join(word.split()).lower()
        try:
            df = mrc_features.loc[mrc_features['word'] == word]
            fvalue = df.iloc[0]['CNC']
            return fvalue
        except:
            return 0

##########################################################################################################

    def fam(word):
        word = ''.join(word.split()).lower()
        try:
            df = mrc_features.loc[mrc_features['word'] == word]
            fvalue = df.iloc[0]['FAM']
            return fvalue
        except:
            return 0

##########################################################################################################

    def img(word):
        word = ''.join(word.split()).lower()
        try:
            df = mrc_features.loc[mrc_features['word'] == word]
            fvalue = df.iloc[0]['IMG']
            return fvalue
        except:
            return 0

##########################################################################################################

    def phon(word):
        word = ''.join(word.split()).lower()
        try:
            df = mrc_features.loc[mrc_features['word'] == word]
            fvalue = df.iloc[0]['NPHN']
            return fvalue
        except:
            return 0

##########################################################################################################

    # functions using wordnet
    from nltk.corpus import wordnet

    def synonyms(word):
        synonyms = 0
        try:
            results = wordnet.synsets(word)
            synonyms = len(results)
            return synonyms
        except:
            return synonyms

##########################################################################################################

    def hypernyms(word):
        hypernyms = 0
        try:
            results = wordnet.synsets(word)
            hypernyms = len(results[0].hypernyms())
            return hypernyms
        except:
            return hypernyms

##########################################################################################################

    def hyponyms(word):
        hyponyms = 0
        try:
            results = wordnet.synsets(word)
        except:
            return hyponyms
        try:
            hyponyms = len(results[0].hyponyms())
            return hyponyms
        except:
            return hyponyms

##########################################################################################################

    # return CEFR levels
    all_levels = pd.read_table(
        'corpus/CEFR_levels.tsv', names=('word', 'level'))

    def levels(word):
        word = ''.join(word.split()).lower()
        try:
            df = all_levels.loc[all_levels['word'] == word]
            level = df.iloc[0]['level']
            return level

        except:
            try:
                df = all_levels.loc[all_levels['word'] == word]
                level = df.iloc[0]['level']
                return level
            except:
                return 0

##########################################################################################################

    # CNC, KFCAT, FAM, KFSMP, KFFRQ, NLET, NPHN, T-LFRQ

    def CNC_fun(word):

        table = mrc_features[mrc_features['word'] == word]

        if len(table) > 0:

            CNC = table['CNC'].values[0]
            CNC = int(CNC)

            return CNC
        else:
            y = 0
            return y

##########################################################################################################

    def KFCAT_fun(word):

        table = mrc_features[mrc_features['word'] == word]

        if len(table) > 0:

            KFCAT = table['KFCAT'].values[0]
            KFCAT = int(KFCAT)

            return KFCAT
        else:
            y = 0
            return y

##########################################################################################################

    def FAM_fun(word):

        table = mrc_features[mrc_features['word'] == word]

        if len(table) > 0:

            FAM = table['FAM'].values[0]
            FAM = int(FAM)

            return FAM
        else:
            y = 0
            return y

##########################################################################################################

    def KFSMP_fun(word):

        table = mrc_features[mrc_features['word'] == word]

        if len(table) > 0:

            KFSMP = table['KFSMP'].values[0]
            KFSMP = int(KFSMP)

            return KFSMP
        else:
            y = 0
            return y

##########################################################################################################

    def KFFRQ_fun(word):

        table = mrc_features[mrc_features['word'] == word]

        if len(table) > 0:

            KFFRQ = table['KFFRQ'].values[0]
            KFFRQ = int(KFFRQ)

            return KFFRQ
        else:
            y = 0
            return y

##########################################################################################################

    def NLET_fun(word):

        table = mrc_features[mrc_features['word'] == word]
        if len(table) > 0:

            NLET = table['NLET'].values[0]
            NLET = int(NLET)

            return NLET
        else:
            y = 0
            return y

##########################################################################################################

    def NPHN_fun(word):

        table = mrc_features[mrc_features['word'] == word]
        if len(table) > 0:

            NPHN = table['NPHN'].values[0]
            NPHN = int(NPHN)

            return NPHN
        else:
            y = 0
            return y

##########################################################################################################

    def TLFRQ_fun(word):

        table = mrc_features[mrc_features['word'] == word]
        if len(table) > 0:

            TLFRQ = table['T-LFRQ'].values[0]
            TLFRQ = int(TLFRQ)

            return TLFRQ
        else:
            y = 0
            return y


##########################################################################################################

    # Convert tree bank tags to ones that are compatible w google

    def is_noun(tag):
        return tag in ['NN', 'NNS', 'NNP', 'NNPS']

    def is_verb(tag):
        return tag in ['VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ']

    def is_adverb(tag):
        return tag in ['RB', 'RBR', 'RBS']

    def is_adjective(tag):
        return tag in ['JJ', 'JJR', 'JJS']

    def penn_to_wn(tag):
        if is_adjective(tag):
            return wordnet.ADJ
        elif is_noun(tag):
            return wordnet.NOUN
        elif is_adverb(tag):
            return wordnet.ADV
        elif is_verb(tag):
            return wordnet.VERB
        return None

    def penn_to_google(tag):
        if is_adjective(tag):
            return 'adj'
        elif is_noun(tag):
            return 'n'
        elif is_adverb(tag):
            return 'adv'
        elif is_verb(tag):
            return 'v'
        return None

##########################################################################################################

    def get_frequency(row):
        nofreq = float(0.000000)
        word = row["phrase"]
        word = str(word)
        tag = row["pos"]
        tag = penn_to_google(tag)

        try:
            word_results = api.words(sp=word, max=1, md='pf')
            tag_list = (word_results[0]['tags'][:-1])

            frequency = word_results[0]['tags'][-1][2:]

            frequency = float(frequency)

            if tag in tag_list:
                return frequency
            else:
                lemma = row['lemma']
                try:
                    word_results = api.words(sp=lemma, max=1, md='pf')
                    tag_list = (word_results[0]['tags'][:-1])

                    frequency = word_results[0]['tags'][-1][2:]

                    frequency = float(frequency)

                    if tag in tag_list:
                        return frequency
                    else:
                        return nofreq
                except:
                    return nofreq

        except:

            return nofreq

##########################################################################################################

    # GET DEP AND POS NUMBER
    word_parse_features['pos'] = word_parse_features.apply(get_pos, axis=1)
    word_parse_features['dep num'] = word_parse_features.apply(get_dep, axis=1)


##########################################################################################################

    # To obtain word lemmas
    # Get Lemma
    word_parse_features['lemma'] = word_parse_features.apply(
        lemmatiser, axis=1)


##########################################################################################################

    # Apply function to get number of synonyms and hypernyms/hyponyms
    word_parse_features['synonyms'] = word_parse_features['lemma'].apply(
        lambda x: synonyms(x))
    word_parse_features['hypernyms'] = word_parse_features['lemma'].apply(
        lambda x: hypernyms(x))
    word_parse_features['hyponyms'] = word_parse_features['lemma'].apply(
        lambda x: hyponyms(x))

##########################################################################################################
    # FINISHED
    # Apply function to check if contained in Ogden word set
    ogden = pd.read_table('binary-features/ogden.txt')
    word_parse_features['ogden'] = word_parse_features['lemma'].apply(
        lambda x: 1 if any(ogden.words == x) else 0)  # clean words

##########################################################################################################
    # TODO - Have dataset, need to do some processing

    # Apply function to check if contained in simple wiki word set
    simple_wiki = pd.read_csv('binary-features/Most_Frequent.csv')
    word_parse_features['simple_wiki'] = word_parse_features['lemma'].apply(
        lambda x: 1 if any(simple_wiki.a == x) else 0)  # clean words

##########################################################################################################
    # TODO - Need to get CALD feature text

    # Apply function to get the level from Cambridge Advanced Learner Dictionary
    cald = pd.read_csv('binary-features/CALD.txt')
    word_parse_features['cald'] = word_parse_features['phrase'].apply(
        lambda x: 1 if any(cald.a == x) else 0)

##########################################################################################################
    # TODO - Trying to track down a complete version of this database
    # Get some MRC features
    mrc_features = pd.read_table('corpus/MRC.tsv', names=('word', 'AOA', 'BFRQ', 'CNC',
                                                          'KFCAT', 'FAM', 'KFSMP', 'IMG', 'KFFRQ', 'NLET', 'CMEAN', 'PMEAN', 'NPHN', 'T-LFRQ'))

    word_parse_features['cnc'] = word_parse_features['lemma'].apply(
        lambda x: cnc(x))
    word_parse_features['img'] = word_parse_features['lemma'].apply(
        lambda x: img(x))

##########################################################################################################
    # TODO - Need to take subtitles.txt and extract most frequent x words as defined in the paper
    # Apply function to check if contained  subimdb word set
    subimdb_500 = pd.read_pickle('binary-features/subimdb_500')
    word_parse_features['sub_imdb'] = word_parse_features['lemma'].apply(
        lambda x: 1 if any(subimdb_500.words == x) else 0)

##########################################################################################################

    # Apply function for google freq
    word_parse_features['google frequency'] = word_parse_features.apply(
        get_frequency, axis=1)

##########################################################################################################

    word_parse_features['phrase'] = word_parse_features.phrase.astype(str)
    word_parse_features['pos'] = word_parse_features.pos.astype(str)

##########################################################################################################

    word_parse_features['KFCAT'] = word_parse_features['lemma'].apply(
        lambda x: KFCAT_fun(x))
    word_parse_features['FAM'] = word_parse_features['lemma'].apply(
        lambda x: FAM_fun(x))
    word_parse_features['KFSMP'] = word_parse_features['lemma'].apply(
        lambda x: KFSMP_fun(x))
    word_parse_features['KFFRQ'] = word_parse_features['lemma'].apply(
        lambda x: KFFRQ_fun(x))
    word_parse_features['NLET'] = word_parse_features['lemma'].apply(
        lambda x: NLET_fun(x))
    word_parse_features['NPHN'] = word_parse_features['lemma'].apply(
        lambda x: NPHN_fun(x))
    word_parse_features['TLFRQ'] = word_parse_features['lemma'].apply(
        lambda x: TLFRQ_fun(x))

##########################################################################################################

    word_parse_features.to_pickle('final_run/'+x+'_actual')

    print(x)
