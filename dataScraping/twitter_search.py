import os
import tweepy


def getClient():
    client = tweepy.Client(bearer_token=os.environ.get('bearer_token'),
                           consumer_key=os.environ.get('consumer_key'),
                           consumer_secret=os.environ.get('consumer_secret'),
                           access_token=os.environ.get('access_token'),
                           access_token_secret=os.environ.get('access_token_secret'))
    return client

def searchTweets(query):
    client = getClient()
    tweets = client.search_recent_tweets(query=query, max_results=10)
    tweet_data = tweets.data
    results = []

    if not tweet_data is None and len(tweet_data) > 0:
        for tweet in tweet_data:
            obj = {}
            obj['id'] = tweet.id
            obj['text'] = tweet.text
            results.append(obj)
    else:
        return []

    return results

tweets = searchTweets('crm software')

if len(tweets) > 0:
    for x in tweets:
        print(x)
else:
    print('No matching tweets found')