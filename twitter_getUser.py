import requests
import os
from flask import Flask, request

# To set your enviornment variables in your terminal run the following line:
# export 'BEARER_TOKEN'='<your_bearer_token>'
bearer_token = os.environ.get("bearer_token")


def create_url():
    # twitter_name = 'BarackObama' # placeholder for testing
    twitter_name = request.form.get("twittname")
    usernames = "usernames=" + twitter_name + ",TwitterAPI"
    # user_fields = "user.fields=description,created_at"
    # tweet_fields = "tweet.fields=attachments"

    url = "https://api.twitter.com/2/users/by?{}".format(usernames)
    return url


def bearer_oauth(r):
    """
    Method required by bearer token authentication.
    """
    r.headers["Authorization"] = f"Bearer {bearer_token}"
    r.headers["User-Agent"] = "v2UserLookupPython"
    return r


def connect_to_endpoint(url):
    response = requests.request("GET", url, auth=bearer_oauth, )
    if response.status_code != 200:
        raise Exception(
            "Request returned an error: {} {}".format(
                response.status_code, response.text
            )
        )
    return response.json()


def twittID():
    url = create_url()
    json_response = connect_to_endpoint(url)
    twitter_id = json_response['data'][0]['id']
    return twitter_id


if __name__ == "__main__":
    twittID()
