import requests
import os
import json

# To set your enviornment variables in your terminal run the following line:
# export 'BEARER_TOKEN'='<your_bearer_token>'
bearer_token = os.environ.get("bearer_token")


def create_url():
    # Specify the usernames that you want to lookup below
    # You can enter up to 100 comma-separated values.
    usernames = "usernames=Karl_Lauterbach,TwitterAPI"
    user_fields = "user.fields=description,created_at"
    tweet_fields = "tweet.fields=attachments"
    #expansions = "expansions=pinned_tweet_id"

    #url = "https://api.twitter.com/2/users/by?{}&{}".format(usernames, expansions)
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
    response = requests.request("GET", url, auth=bearer_oauth,)
    print(response.status_code)
    if response.status_code != 200:
        raise Exception(
            "Request returned an error: {} {}".format(
                response.status_code, response.text
            )
        )
    return response.json()


def main():
    url = create_url()
    json_response = connect_to_endpoint(url)
    #print(json.dumps(json_response, indent=4, sort_keys=True))
    print(json_response)


if __name__ == "__main__":
    main()