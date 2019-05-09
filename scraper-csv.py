import json
from util import Counter
import newspaper
import re
import csv
import itertools
from collections import namedtuple

'''
TODO:
- Make sure articles scraped are legit articles and are not duplicates.
  Can accomplish this by checking the URL field
- Make sure that the article text contains no extraneous content
  (e.g.: "Follow <author name> on Twitter at <Twitter handle>!")
'''

debug = True

fp = open('articles3.csv', newline='')
csv_reader = csv.reader(fp)

article_headers = next(csv_reader)
print(article_headers)

ContentClass = namedtuple('ContentClass', ['url', 'title', 'text'])

articles = {}

while True:
    next_row = next(csv_reader, 0)
    if next_row == 0:
        break
    
    print (next_row[0], next_row[3])
    
    if next_row[3] == 'Reuters':
        article_info = {
            'link': 'http://www.reuters.com', 
            'label': 'real', 
            'title': next_row[2]
        }
        content = ContentClass(url=next_row[8].strip(), title=next_row[2], text=next_row[9])

        while True:
            article_info['text'] = content.text
            print("Title:", content.title)
            print('----------------------')
            print("Text:", content.text)
            print('----------------------')
            print("Article obtained from", content.url)
            if content.url in articles:
                print("NOTE: Article already stored")

            if 'The views expressed in this article are not those of Reuters News.' in content.text:
                print("Discarding: This article contains the text: 'The views expressed in this article are not those of Reuters News.'")
                char1 = 'd'
            elif 'Breakingviews' in content.text:
                print("Discarding since this article is from Reuters Breakingviews")
                char1 = 'd'
            else:
                char1 = 'p'
                # char1 = input("Keep [k]? Trim [t]? Trim & Keep [p]? Discard [d]? ")
                # while char1 not in ('k', 't', 'd', 'p'):
                #     print("Error: Invalid response")
                #     char1 = input("Keep [k]? Trim [t]? Trim & Keep [p]? Discard [d]? ")

            if char1 == 'k' or char1 == 'd':
                break
            
            article_info['text'] = article_info['text'].replace("FILE PHOTO:", "")
            article_info['text'] = article_info['text'].replace("FILE PHOTO", "")
            article_info['text'] = article_info['text'].replace("File Photo", "")
            article_info['text'] = article_info['text'].replace("REUTERS", "")
            article_info['text'] = article_info['text'].replace("Reuters", "")
            article_info['text'] = article_info['text'].replace("[.N]", "")
            article_info['text'] = re.sub("Slideshow \([0-9]+ Images\)", "", article_info['text'])
            article_info['text'] = article_info['text'].replace("U. S.", "U.S.")
            
            

            # Remove everything before the first "(Reuters)"
            idx = article_info['text'].find("(Reuters)")
            if idx != -1:
                idx += len("(Reuters) - ")
                article_info['text'] = article_info['text'][idx:]
            print('----------------------')
            print("New text:", article_info['text'])
            print('----------------------')
                
            if char1 == 'p':
                char2 = 'y'
            else:
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
            
with open('articles_reuters2.json', 'a') as article_fp:
    json.dump(articles, article_fp, indent=4)
    print(file=article_fp)


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
# website = 'reuters'
# paper = newspaper.build('http://www.reuters.com', memoize_articles=False)
# url_list = [i.url for i in paper.articles if ('www.reuters.com/article' in i.url)]

# for url in url_list:
#     print(url)
# print('Total: {} articles'.format(len(url_list)))

# for i in range(20, len(url_list)):
#     url = url_list[i]
#     content = newspaper.Article(url)

#     article_info = {
#         "link": 'http://www.reuters.com',
#         "label": 'real',
#     }

#     try:
#         content.download()
#         content.parse()
#     except Exception as e:
#         print(e)
#         print("continuing...")
#         continue
    
#     article_info['title'] = content.title
#     print("Article {} downloaded from".format(i + 1), website)
#     print()

#     while True:
#         article_info['text'] = content.text
#         print("Title:", content.title)
#         print('----------------------')
#         print("Text:", content.text)
#         print('----------------------')
#         print("Article downloaded from", content.url)
#         if content.url in articles:
#             print("NOTE: Article already stored")
        
#         char1 = input("Keep [k]? Trim [t]? Discard [d]? ")
#         while char1 not in ('k', 't', 'd'):
#             print("Error: Invalid response")
#             char1 = input("Keep [k]? Trim [t]? Discard [d]? ")

#         if char1 == 'k' or char1 == 'd':
#             break
        
#         article_info['text'] = article_info['text'].replace("FILE PHOTO:", "")
#         article_info['text'] = article_info['text'].replace("FILE PHOTO", "")
#         article_info['text'] = article_info['text'].replace("File Photo", "")
#         article_info['text'] = article_info['text'].replace("REUTERS", "")
#         article_info['text'] = article_info['text'].replace("[.N]", "")
#         article_info['text'] = re.sub("Slideshow \([0-9]+ Images\)", "", article_info['text'])
        

#         # Remove everything before the first "(Reuters)"
#         idx = article_info['text'].find("(Reuters)")
#         if idx != -1:
#             idx += len("(Reuters) - ")
#             article_info['text'] = article_info['text'][idx:]
#         print('----------------------')
#         print("New text:", article_info['text'])
#         print('----------------------')
            
#         char2 = input("OK [y]? Trim manually [t]? Start over [s]? ")
#         while char2 not in ('s', 'y', 't'):
#             print("Error: Invalid response")
#             char2 = input("OK [y]? Trim manually [t]? Start over [s]? ")
        
#         if char2 == 's':
#             continue
#         elif char2 == 'y':
#             break
#         else:
#             while input("Remove last line of article [y]? Continue [c]? ") == 'y':
#                 s = article_info['text']
#                 index_newline = s.rfind('\n')
#                 article_info['text'] = s[:index_newline]
#                 print('----------------------')
#                 print("New text:", article_info['text'])
#                 print('----------------------')
                
#             while True:
#                 s = article_info['text']
#                 index_newline = s.find('\n')
#                 if input("Remove first line of article: \"{}\" [y]? Continue [c]? ".format(s[0:index_newline])) != 'y':
#                     break
#                 article_info['text'] = s[index_newline + 1:]
#                 print('----------------------')
#                 print("New text:", article_info['text'])
#                 print('----------------------')

#             while True:
#                 s = article_info['text']
#                 index_newline = s.find(' ')
#                 if input("Remove first word of article: \"{}\" [y]? Continue [c]? ".format(s[0:index_newline])) != 'y':
#                     break
#                 article_info['text'] = s[index_newline + 1:]
#                 print('----------------------')
#                 print("New text:", article_info['text'])
#                 print('----------------------')
            
#             char2 = input("OK [y]? Start over [s]?")
#             while char2 not in ('s', 'y'):
#                 print("Error: Invalid response")
#                 char2 = input("OK [y]? Start over [s]?")
#             if char2 == 'y':
#                 break
        
#     if char1 != 'd':   
#         print("Storing article downloaded from", content.url)
#         if debug:
#             print (article_info)
#         articles[content.url] = article_info
#     else:
#         print("Discarding article downloaded from", content.url)

#     print()
#     print()
#     print()
            
# with open('articles_reuters.json', 'a') as article_fp:
#     json.dump(articles, article_fp, indent=4)
#     print(file=article_fp)
