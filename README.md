# news-classification

Fake news data: https://www.kaggle.com/mrisdal/fake-news

Real news data: https://www.kaggle.com/asad1m9a9h6mood/news-articles or filtering https://www.kaggle.com/snapcrack/all-the-news

__PLAN:__

## Scrape news datasets (4/28)

Fake: __Breitbart, InfoWars, NewsPunch__ (extreme-right fake news), Occupy Democrats (extreme-left fake news)

Real: __AP, Reuters__, BBC (generally unbiased), __NPR__ (left-center bias), Chicago Tribune (right-center bias)

_Amount of news to collect from each news site: TBD_

Split datasets into 70-15-15 for training, validation, testing.

NOTES:
* 'articles.json' contains the text of the scraped articles
* 'data.json' contains the word counts of the scraped articles
* 'scraper.py' scrapes the news articles and updates them into 'articles.json'
* 'word-counts.py' takes article text from 'articles.json', calculates the word counts, and stores them into 'data.json'

## Naive Bayes classifier (May 2nd)
-parse each article, create word counts
-naive bayes stuff
-laplace smoothing

## Neural network (may 5th)
-more steps tbd


## testing and report (may 10th)
