import json
from util import Counter
import newspaper
#from newspaper import Article

numArticles = 4 #max number of articles scraped from each website

data = {} #dictionary of website names to dictionaries containing their
            # link, label (real/fake), and list of article word counts

with open('websites.json') as data_file:
    websites = json.load(data_file)

for website, siteinfo in websites.items():
    count = 0
    paper = newspaper.build(siteinfo['link'], memoize_articles=False)
    websiteInfo = {
        "link": siteinfo['link'],
        "label": siteinfo['label'],
        "articles": [],
    }
    #noneTypeCount = 0
    for content in paper.articles:
        if count >= numArticles:
            break
        try:
            content.download()
            content.parse()
        except Exception as e:
            print(e)
            print("continuing...")
            continue
        """
        if content.publish_date is None:
            print(count, " Article has date of type None...")
            noneTypeCount = noneTypeCount + 1
            if noneTypeCount > 10:
                print("Too many noneType dates, aborting...")
                noneTypeCount = 0
                break
            count = count + 1
            continue
        """
        articletext = content.text
        wordCounts = Counter()
        for word in articletext.split():
            wordCounts[word] += 1
        websiteInfo['articles'].append(wordCounts)
        print(count, "articles downloaded from", website)
        count += 1
        #noneTypeCount = 0
    
    data[website] = websiteInfo