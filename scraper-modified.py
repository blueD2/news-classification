import json
from util import Counter
import newspaper
import re

'''
TODO:
- Make sure articles scraped are legit articles and are not duplicates.
  Can accomplish this by checking the URL field
- Make sure that the article text contains no extraneous content
  (e.g.: "Follow <author name> on Twitter at <Twitter handle>!")
'''

debug = True

with open('websites.json') as data_file:
    websites = json.load(data_file)

articles = {}


    # for website, siteinfo in websites.items():
    #     count = 0
    #     numArticles = siteinfo['count']
    #     if debug:
    #         print('Website:', website)
    #         print('Site info:', siteinfo)
    #     if numArticles == 0:
    #         continue
        
    #     paper = newspaper.build(siteinfo['link'], memoize_articles=False)
        
    #     for content in paper.articles:
    #         if count >= numArticles:
    #             break
            
    #         article_info = {
    #             "link": siteinfo['link'],
    #             "label": siteinfo['label'],
    #         }
website = 'reuters'
paper = newspaper.build('http://www.reuters.com', memoize_articles=False)
url_list = [i.url for i in paper.articles if ('www.reuters.com/article' in i.url)]

for url in url_list:
    print(url)
print('Total: {} articles'.format(len(url_list)))

for i in range(20, len(url_list)):
    url = url_list[i]
    content = newspaper.Article(url)

    article_info = {
        "link": 'http://www.reuters.com',
        "label": 'real',
    }

    try:
        content.download()
        content.parse()
    except Exception as e:
        print(e)
        print("continuing...")
        continue
    
    article_info['title'] = content.title
    print("Article {} downloaded from".format(i + 1), website)
    print()

    while True:
        article_info['text'] = content.text
        print("Title:", content.title)
        print('----------------------')
        print("Text:", content.text)
        print('----------------------')
        print("Article downloaded from", content.url)
        if content.url in articles:
            print("NOTE: Article already stored")
        
        char1 = input("Keep [k]? Trim [t]? Discard [d]? ")
        while char1 not in ('k', 't', 'd'):
            print("Error: Invalid response")
            char1 = input("Keep [k]? Trim [t]? Discard [d]? ")

        if char1 == 'k' or char1 == 'd':
            break
        
        article_info['text'] = article_info['text'].replace("FILE PHOTO:", "")
        article_info['text'] = article_info['text'].replace("FILE PHOTO", "")
        article_info['text'] = article_info['text'].replace("File Photo", "")
        article_info['text'] = article_info['text'].replace("REUTERS", "")
        article_info['text'] = article_info['text'].replace("[.N]", "")
        article_info['text'] = re.sub("Slideshow \([0-9]+ Images\)", "", article_info['text'])
        

        # Remove everything before the first "(Reuters)"
        idx = article_info['text'].find("(Reuters)")
        if idx != -1:
            idx += len("(Reuters) - ")
            article_info['text'] = article_info['text'][idx:]
        print('----------------------')
        print("New text:", article_info['text'])
        print('----------------------')
            
        char2 = input("OK [y]? Trim manually [t]? Start over [s]? ")
        while char2 not in ('s', 'y', 't'):
            print("Error: Invalid response")
            char2 = input("OK [y]? Trim manually [t]? Start over [s]? ")
        
        if char2 == 's':
            continue
        elif char2 == 'y':
            break
        else:
            while input("Remove last line of article [y]? Continue [c]? ") == 'y':
                s = article_info['text']
                index_newline = s.rfind('\n')
                article_info['text'] = s[:index_newline]
                print('----------------------')
                print("New text:", article_info['text'])
                print('----------------------')
                
            while True:
                s = article_info['text']
                index_newline = s.find('\n')
                if input("Remove first line of article: \"{}\" [y]? Continue [c]? ".format(s[0:index_newline])) != 'y':
                    break
                article_info['text'] = s[index_newline + 1:]
                print('----------------------')
                print("New text:", article_info['text'])
                print('----------------------')

            while True:
                s = article_info['text']
                index_newline = s.find(' ')
                if input("Remove first word of article: \"{}\" [y]? Continue [c]? ".format(s[0:index_newline])) != 'y':
                    break
                article_info['text'] = s[index_newline + 1:]
                print('----------------------')
                print("New text:", article_info['text'])
                print('----------------------')
            
            char2 = input("OK [y]? Start over [s]?")
            while char2 not in ('s', 'y'):
                print("Error: Invalid response")
                char2 = input("OK [y]? Start over [s]?")
            if char2 == 'y':
                break
        
    if char1 != 'd':   
        print("Storing article downloaded from", content.url)
        if debug:
            print (article_info)
        articles[content.url] = article_info
    else:
        print("Discarding article downloaded from", content.url)

    print()
    print()
    print()
            
with open('articles_reuters.json', 'a') as article_fp:
    json.dump(articles, article_fp, indent=4)
    print(file=article_fp)