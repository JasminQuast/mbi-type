import requests
import os
import json
import twitter_getUser
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.ensemble import RandomForestClassifier
import type_classificator

bearer_token = os.environ.get("bearer_token")


def create_url():
    return "https://api.twitter.com/2/users/{}/tweets?max_results=100".format(twitter_getUser.twittID())


def get_params():
    # Tweet fields are adjustable.
    # Options include:
    # attachments, author_id, context_annotations,
    # conversation_id, created_at, entities, geo, id,
    # in_reply_to_user_id, lang, non_public_metrics, organic_metrics,
    # possibly_sensitive, promoted_metrics, public_metrics, referenced_tweets,
    # source, text, and withheld
    return {"tweet.fields": "created_at,lang"}


def bearer_oauth(r):
    """
    Method required by bearer token authentication.
    """
    r.headers["Authorization"] = f"Bearer {bearer_token}"
    r.headers["User-Agent"] = "v2UserTweetsPython"
    return r


def connect_to_endpoint(url, params):
    response = requests.request("GET", url, auth=bearer_oauth, params=params)
    if response.status_code != 200:
        raise Exception(
            "Request returned an error: {} {}".format(
                response.status_code, response.text
            )
        )
    return response.json()


def pred():
    json_response = connect_to_endpoint(create_url(), get_params())

    json_data = json.dumps(json_response, indent=4, sort_keys=True)
    item_dict = json.loads(json_data)
    json_lenght = len(item_dict['data'])

    text_list = []
    for x in range(1, json_lenght):
        if (json_response['data'][x]['lang']) == 'en':
            text_list.append(json_response['data'][x]['text'])

    big_text_list = ' '.join(text_list)
    df = pd.DataFrame([big_text_list])
    df.columns = ["posts"]

    tokenlist_training_dataset = list(type_classificator.training.iloc[:, 2:])
    count_vect_twitt = CountVectorizer(input=[big_text_list], vocabulary=tokenlist_training_dataset)
    count_vect_twitt.get_feature_names()

    x_twitt = count_vect_twitt.fit_transform([big_text_list])

    forest = RandomForestClassifier()
    forest.fit(type_classificator.X_train, type_classificator.training["target_variable"])
    pred_forest = forest.predict(x_twitt)
    pred = ''.join(str(e) for e in pred_forest)
    return pred

