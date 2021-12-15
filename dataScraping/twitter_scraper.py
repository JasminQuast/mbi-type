import os
import tweepy


def getClient():
    client = tweepy.Client(bearer_token=os.environ.get('bearer_token'),
                           consumer_key=os.environ.get('consumer_key'),
                           consumer_secret=os.environ.get('consumer_secret'),
                           access_token=os.environ.get('access_token'),
                           access_token_secret=os.environ.get('access_token_secret'))
    return client

def searchTweets(client, query):
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

def getTweet(client, id):
    tweet = client.get_tweet(id, expansions=['author_id'], user_fields=['username'])
    return tweet


client = getClient()
tweets = searchTweets(client, 'crm software')

objs = []
if len(tweets) > 0:
    for tweet in tweets:
        twt = getTweet(client, tweet['id'])
        obj = {}
        obj['id'] = tweet['id']
        obj['text'] = tweet['text']
        obj['username'] = twt.includes['users'][0].username
        objs.append(obj)

for x in objs:
    url = 'https://twitter.com/{}/status/{}'.format(x['username'], x['id'])
    print('\n')
    print(url)