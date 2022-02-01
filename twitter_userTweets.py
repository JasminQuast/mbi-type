import requests
import os
import json
import twitter_getUser
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.ensemble import RandomForestClassifier
import type_predictor
import datetime

bearer_token = os.environ.get("bearer_token")


def bearer_oauth(r):
    """
    Method required by bearer token authentication.
    """
    r.headers["Authorization"] = f"Bearer {bearer_token}"
    r.headers["User-Agent"] = "v2UserTweetsPython"
    return r


def current_url():
    return "https://api.twitter.com/2/users/{}/tweets?max_results=100".format(twitter_getUser.twitt_id())


def past_url():
    return "https://api.twitter.com/2/users/{}/tweets?max_results=100&start_time={}-01-01T00:00:00Z&end_time={}-12-01T00:00:00Z".format(twitter_getUser.twitt_id(), start_time(), start_time())


def connect_to_endpoint(url):
    params = {"tweet.fields": "created_at,lang"}
    response = requests.request("GET", url, auth=bearer_oauth, params=params)
    if response.status_code != 200:
        raise Exception(
            "Request returned an error: {} {}".format(
                response.status_code, response.text
            )
        )
    return response.json()


def connect_to_past_endpoint(url):
    response = requests.request("GET", url, auth=bearer_oauth)
    if response.status_code != 200:
        raise Exception(
            "Request returned an error: {} {}".format(
                response.status_code, response.text
            )
        )
    return response.json()


def current_posts():
    """ Connect to endpoint and get the text (posts) of the json data object, but only those that are english

    :parameter
        text_list (list): list of the latest posts marked as english
    :return:
        main_pred(text_list) (function): Executes the function main_pred() which passes the parameter text_list
    """
    json_response = connect_to_endpoint(current_url())
    json_data = json.dumps(json_response, indent=4, sort_keys=True)  # takes in a json object and returns a string
    item_dict = json.loads(json_data)  # takes in a string and returns a json object
    json_length = len(item_dict['data'])
    text_list = []
    for x in range(1, json_length):
        if (json_response['data'][x]['lang']) == 'en':
            text_list.append(json_response['data'][x]['text'])

    return main_pred(text_list)


def past_posts():
    """ Connect to endpoint in the past and get the text (posts) of the json data object.

    :parameter
        text_list (list): list of the posts in the past. If there are no or not enough results,
        set placeholder (0 or 1) to list

    :return:
        main_pred(text_list) (function): Executes the function main_pred(), which passes the parameter text_list
    """
    json_response = connect_to_past_endpoint(past_url())
    json_data = json.dumps(json_response, indent=4, sort_keys=True)
    item_dict = json.loads(json_data)

    text_list = []
    if start_time() == 0 or item_dict['meta']['result_count'] == 0:
        text_list.append(0)  # User hasn't been on Twitter long enough OR not enough posts this time
    else:
        json_lenght = len(item_dict['data'])
        for x in range(1, json_lenght):
            text_list.append(json_response['data'][x]['text'])

    return main_pred(text_list)


def start_time():
    """ Get current year and registration year of the user. Check that the year is not too far back and not too close
    either. Minimum allowable time according to Twitter is 2010-11-06T00:00:01Z.

    :return:
        tweet_year (int): Year in which the Twitter data should be retrieved
    """
    current_year = datetime.datetime.today().year
    tree_years_ago_from_current = current_year - 2
    min_allowable_year = current_year - 6
    registration_year = twitter_getUser.registration_year()

    if registration_year <= min_allowable_year:
        tweet_year = min_allowable_year
    elif min_allowable_year < registration_year < tree_years_ago_from_current:
        tweet_year = registration_year
    else:
        tweet_year = 0
    return tweet_year


def main_pred(text_list):
    """ Real data prediction of the type based on training data set in the type_predictor class

    :param
        text_list (list): List of posts (0 and 1 are just placeholders)
    :return:
        pred (str): Type Prediction
    """
    if text_list[0] == 0:
        pred = ""
    else:
        big_text_list = ' '.join(text_list)
        df = pd.DataFrame([big_text_list])
        df.columns = ["posts"]

        tokenlist_training_dataset = list(type_predictor.training.iloc[:, 2:])
        count_vect_twitt = CountVectorizer(input=[big_text_list], vocabulary=tokenlist_training_dataset)
        count_vect_twitt.get_feature_names()
        x_twitt = count_vect_twitt.fit_transform([big_text_list])

        forest = RandomForestClassifier()
        forest.fit(type_predictor.X_train, type_predictor.training["target_variable"])
        pred_forest = forest.predict(x_twitt)
        pred = ''.join(str(e) for e in pred_forest)
        print(pred)
    return pred


def description(prediction):
    """ One-word description for each letter the type consists of

    :param
        prediction (str): Type which was predicted before, e.g. INFP
    :return:
        descr (str): Description consisting of 4 words (separated with -) depending on the type
    """
    letter_list = list(prediction)
    print(letter_list)
    descr_list = []
    if "I" in letter_list:
        descr = "Introversion"
        descr_list.append(descr)
    if "E" in letter_list:
        descr = "Extroversion"
        descr_list.append(descr)
    if "N" in letter_list:
        descr = "Intuition"
        descr_list.append(descr)
    if "S" in letter_list:
        descr = "Sensing"
        descr_list.append(descr)
    if "T" in letter_list:
        descr = "Thinking"
        descr_list.append(descr)
    if "F" in letter_list:
        descr = "Feeling"
        descr_list.append(descr)
    if "J" in letter_list:
        descr = "Judging"
        descr_list.append(descr)
    if "P" in letter_list:
        descr = "Perceiving"
        descr_list.append(descr)
    descr = ' - '.join(str(e) for e in descr_list)

    print(descr)
    return descr

if __name__ == '__main__':
    start_time()