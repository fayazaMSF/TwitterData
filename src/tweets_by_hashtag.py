import snscrape.modules.twitter as sntwitter
import pandas as pd
from tqdm import tqdm

config = pd.read_json('src\config.json')

for _hashtag in tqdm(config.hashtags):
    hashtag = _hashtag['hashtag']
    limit = _hashtag['limit']

    # start and end - date format yyyy-mm-dd
    start = _hashtag['start']
    end = _hashtag['end']
    
    if not (start and end):
        query = f'(#{hashtag}) until:{end} since:{start}'
    else:
        query = f'(#{hashtag})'

    tweets = []
    for tweet in tqdm(sntwitter.TwitterSearchScraper(query).get_items()):
        if len(tweets) == limit:
            break
        else:
            tweets.append(
                [
                    tweet.date,
                    tweet.user.username,
                    tweet.url,
                    tweet.content, 
                    tweet.hashtags
                ]
            )

    df = pd.DataFrame(tweets, columns=['Date', 'User', 'Url', 'Tweet', 'HashTags'])
    df.to_csv('data\\hashtag_tweets.csv', encoding='utf-8',
              mode='a', index=False, header=False)
