from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import pymorphy2


morph = pymorphy2.MorphAnalyzer()
stop_words = stopwords.words('russian')
stop_words.extend(stopwords.words('english'))
stop_words.extend(['россияхорватия', 'ruscro', 'worldcup',
                   'rusiavscroacia', 'https', 'чм', 'youtube'
                   'голубаяпапка', 'http'])


def preparing(file):

    with open(file, encoding='utf-8') as corpus:

        tweets_corpus = []

        for line in corpus:

            if line == '\n':
                continue

            tweet = word_tokenize(line.lower(), 'russian')

            tweet = [s for s in tweet if s.isalpha()]
            tweet = [morph.parse(i)[0].normal_form for i in tweet if i not in stop_words]

            tweets_corpus.append(tweet)

        return tweets_corpus


def frequency_analyze(tweets_corpus):

    frequency_dict = dict()
    frequency_list = list()

    for tweet in tweets_corpus:
        for word in tweet:

            if not frequency_dict.get(word):
                frequency_dict[word] = 1

            elif frequency_dict.get(word) and tweet.count(word) >= 1:
                frequency_dict[word] += 1

    for key, value in frequency_dict.items():

        freq_data = []

        percentage = str(round(value / len(tweets_corpus) * 100, 1)) + '%'
        freq_data.append(key)
        freq_data.append(value)
        freq_data.append(percentage)

        frequency_list.append(freq_data)

    frequency_list.sort(key=lambda x: (-x[1], x[0]))

    with open('frequency.txt', 'w', encoding='utf-8') as frequency_file:

        for line in frequency_list:
            frequency_file.write(' – '.join(map(str, line)) + '\n')

    return frequency_list


def length_analyze(tweets_corpus):

    length_dict = dict()
    length_list = list()

    for tweet in tweets_corpus:

        length_key = str(len(tweet))

        if not length_dict.get(length_key):
            length_dict[length_key] = 1
        else:
            length_dict[length_key] += 1

    for key, value in length_dict.items():

        len_data = []

        percentage = str(round(value / len(tweets_corpus) * 100, 1)) + '%'
        len_data.append(key)
        len_data.append(value)
        len_data.append(percentage)

        length_list.append(len_data)

    length_list.sort(key=lambda x: (-x[1], x[0]))

    with open('tweets_length.txt', 'w', encoding='utf-8') as length_file:

        for line in length_list:
            length_file.write(' – '.join(map(str, line)) + '\n')


def write_to_estimations(frequency_list):

    with open('estimations.txt', 'w', encoding='utf-8') as estimations:

        for line in frequency_list:
            if line[1] is 1:
                data_for_estimations = frequency_list[:frequency_list.index(line)]
                break

        for string in data_for_estimations:
            estimations.write(string[0] + ' \n')


def filling_tonality_dict(file):

    tonality_dict = dict()
    with open(file, encoding='utf-8') as tonality_file:

        for i, line in enumerate(tonality_file):
            line = line.split()
            tonality_dict[line[0]] = line[1]

    return tonality_dict


def classification(tweets_corpus, tonality_dict):

    negative_1, neutral_1, positive_1 = 0, 0, 0
    negative_2, neutral_2, positive_2 = 0, 0, 0

    for tweet in tweets_corpus:

        # rule_1
        tweet_tonality = 0
        # rule_2
        neg_words, neut_words, pos_words = 0, 0, 0

        for word in tweet:
            if word not in tonality_dict:
                continue

            # rule_1 tonality
            tweet_tonality += int(tonality_dict[word])

            # rule_2 tonality
            if tonality_dict[word] == '-1':
                neg_words += 1
            elif tonality_dict[word] == '0':
                neut_words += 1
            elif tonality_dict[word] == '1':
                pos_words += 1

        words_tonality = (neg_words, neut_words, pos_words)

        # rule_1 classification
        if tweet_tonality < 0:
            negative_1 += 1
        elif tweet_tonality == 0:
            neutral_1 += 1
        elif tweet_tonality > 0:
            positive_1 += 1

        # rule_2 classification
        if max(words_tonality) == neg_words:
            negative_2 += 1
        elif max(words_tonality) == neut_words:
            neutral_2 += 1
        elif max(words_tonality) == pos_words:
            positive_2 += 1

    rule_1_categories = (negative_1, neutral_1, positive_1,)
    rule_2_categories = (negative_2, neutral_2, positive_2,)

    with open('classifications.txt', 'w', encoding='utf-8') as classifile:

        rules_categories = (rule_1_categories, rule_2_categories,)
        category_data = []

        for i, rule in enumerate(rules_categories):

            if i is 0:
                classifile.write('rule_1\n')
            elif i is 1:
                classifile.write('\nrule_2\n')

            for index, category in enumerate(rule):

                if index is 0:
                    category_data.append('negative')
                elif index is 1:
                    category_data.append('neutral')
                elif index is 2:
                    category_data.append('positive')

                category_data.append(category)

                percentage = str(round((category / len(tweets_corpus)) * 100, 2)) + '%'
                category_data.append(percentage)

                classifile.write(' – '.join(map(str, category_data)) + '\n')
                category_data.clear()


def adjectives(tonality_dict, frequency_list, tweets_corpus):

    positive_adj, negative_adj = {}, {}

    for word in tonality_dict:

        morph_data = morph.parse(word)[0]
        if morph_data.tag.POS == 'ADJF':

            if tonality_dict[word] == '-1':
                negative_adj[word] = 1
            elif tonality_dict[word] == '1':
                positive_adj[word] = 1

    for data in frequency_list:

        if data[0] in positive_adj:
            positive_adj[data[0]] = data[1]
        elif data[0] in negative_adj:
            negative_adj[data[0]] = data[1]
        else:
            continue

    positive_adj_list = [(pkey, pvalue,) for pkey, pvalue in positive_adj.items()]
    negative_adj_list = [(nkey, nvalue,) for nkey, nvalue in negative_adj.items()]

    positive_adj_list.sort(key=lambda x: x[1], reverse=True)
    negative_adj_list.sort(key=lambda x: x[1], reverse=True)

    top_5_pos = positive_adj_list[:5]
    top_5_neg = negative_adj_list[:5]

    top_tuple = (top_5_pos, top_5_neg,)

    with open('adjectives.txt', 'w', encoding='utf-8') as adj_file:

        adj_data = []

        for i, top in enumerate(top_tuple):

            if i is 0:
                adj_file.write('top-5 positive adjectives\n')
            elif i is 1:
                adj_file.write('\ntop-5 negative adjectives\n')

            for pair in top:
                percentage = str(round((int(pair[1]) / len(tweets_corpus)) * 100, 2)) + '%'
                adj_data.append(pair[0])
                adj_data.append(pair[1])
                adj_data.append(percentage)

                adj_file.write(' – '.join(map(str, adj_data)) + '\n')
                adj_data.clear()


y = preparing('data.txt')
adjectives(filling_tonality_dict('done_estimations.txt'), frequency_analyze(y), y)

# classification(preparing('data.txt'), filling_tonality_dict('done_estimations.txt'))
# write_to_estimations(frequency_analyze(preparing('data.txt')))
# length_analyze(preparing('data.txt'))
