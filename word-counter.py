import json
import string
import util

'''
Takes article text in 'articles.json' and converts it into word counts for each
article and stores results in 'data.json'.
'''

with open('articles.json', 'r') as article_fp, open('data.json', 'w') as data_fp:
    articles = json.load(article_fp)

    wordCounts = []

    for article in articles:
        article_text = article['text']
        this_counter = util.Counter()
        translation = str.maketrans("", "", string.punctuation)
        article_words = article_text.translate(translation).lower().split()
        for word in article_words:
            this_counter[word] += 1
        word_count_info = {
            'link': article['link'],
            'label': article['label'],
            'url': article['url'],
            'counts': this_counter
        }
        wordCounts.append(word_count_info)

    
    json.dump(wordCounts, data_fp, indent=4)
