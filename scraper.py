import json
from util import Counter
import newspaper

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

with open('articles.json', 'a') as article_fp:
    articles = []
    for website, siteinfo in websites.items():
        count = 0
        paper = newspaper.build(siteinfo['link'], memoize_articles=False)
        numArticles = siteinfo['count']

        if debug:
            print('Website:', website)
            print('Site info:', siteinfo)

        for content in paper.articles:
            if count >= numArticles:
                break
            
            article_info = {
                "link": siteinfo['link'],
                "label": siteinfo['label'],
            }

            try:
                content.download()
                content.parse()
            except Exception as e:
                print(e)
                print("continuing...")
                continue
            
            article_info['title'] = content.title
            article_info['text'] = content.text
            article_info['url'] = content.url
            count += 1
            print(count, "article(s) downloaded from", website)

            if debug:
                print (article_info)
            articles.append(article_info)

    json.dump(articles, article_fp, indent=4)
    print(file=article_fp)