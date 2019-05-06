import json
import util
import re

'''
Takes article text in 'articles.json' and converts it into word counts for each
article and stores results in 'data.json'.
'''

with open('articles.json', 'r') as article_fp:
    articles = json.load(article_fp)

wordCounts = []

for article_url, article_data in articles.items():
    article_text = article_data['text']
    this_counter = util.Counter()

    # Punctuation counts
    this_counter['?'] = article_text.count('?')
    this_counter['!'] = article_text.count('!')

    # Word counts
    translation = str.maketrans("", "", u"!\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~\u2013\u2014\u2018\u2019\u201c\u201d\u2026")
    article_words = article_text.translate(translation).lower().split()
    for word in article_words:
        this_counter[word] += 1
    
    word_count_info = {
        'link': article_data['link'],
        'label': article_data['label'],
        'url': article_url,
        'counts': this_counter
    }
    wordCounts.append(word_count_info)

with open('data.json', 'w') as data_fp:
    json.dump(wordCounts, data_fp, indent=4)
