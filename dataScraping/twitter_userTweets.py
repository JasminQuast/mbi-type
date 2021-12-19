import requests
import os
import json
import Twitter_getUser

# To set your environment variables in your terminal run the following line:
# export 'BEARER_TOKEN'='<your_bearer_token>'
bearer_token = os.environ.get("bearer_token")


def create_url():
    return "https://api.twitter.com/2/users/{}/tweets".format(Twitter_getUser.twittID())


def get_params():
    # Tweet fields are adjustable.
    # Options include:
    # attachments, author_id, context_annotations,
    # conversation_id, created_at, entities, geo, id,
    # in_reply_to_user_id, lang, non_public_metrics, organic_metrics,
    # possibly_sensitive, promoted_metrics, public_metrics, referenced_tweets,
    # source, text, and withheld
    return {"tweet.fields": "created_at"}


def bearer_oauth(r):
    """
    Method required by bearer token authentication.
    """
    r.headers["Authorization"] = f"Bearer {bearer_token}"
    r.headers["User-Agent"] = "v2UserTweetsPython"
    return r


def connect_to_endpoint(url, params):
    response = requests.request("GET", url, auth=bearer_oauth, params=params)
    #print(response.status_code)
    if response.status_code != 200:
        raise Exception(
            "Request returned an error: {} {}".format(
                response.status_code, response.text
            )
        )
    return response.json()


def main():
    url = create_url()
    params = get_params()
    json_response = connect_to_endpoint(url, params)

    json_data = json.dumps(json_response, indent=4, sort_keys=True)
    item_dict = json.loads(json_data)
    json_lenght = len(item_dict['data'])

    text_list = []
    for x in range(1, json_lenght):
        text_list.append(json_response['data'][x]['text'])
    print(text_list)


if __name__ == "__main__":
    main()