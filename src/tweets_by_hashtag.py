import snscrape.modules.twitter as sntwitter
import pandas as pd
from tqdm import tqdm

config = pd.read_json('src\config.json')

for _hashtag in tqdm(config.hashtags):
    hashtag = _hashtag['hashtag']
    limit = _hashtag['limit']
    
    tweets = []
    for tweet in tqdm(sntwitter.TwitterHashtagScraper(hashtag).get_items()):
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
