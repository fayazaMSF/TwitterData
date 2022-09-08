import snscrape.modules.twitter as sntwitter
import pandas as pd
from tqdm import tqdm

config = pd.read_json('src\config.json')

for _user in tqdm(config.users):
    user = _user['user']
    limit = _user['limit']

    # start and end - date format yyyy-mm-dd
    start = _user['start']
    end = _user['end']

    if not (start and end):
        query = f'from:{user} until:{end} since:{start}'
    else:
        query = f'from:{user}'
    
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

    df = pd.DataFrame(
        tweets, columns=['Date', 'User', 'Url', 'Tweet', 'HashTags'])
    df.to_csv('data\\user_tweets.csv', encoding='utf-8',
              mode='a', index=False, header=False)
