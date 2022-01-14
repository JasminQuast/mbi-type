import requests
import os
import json
import twitter_getUser
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.ensemble import RandomForestClassifier
import type_classificator
import datetime


bearer_token = os.environ.get("bearer_token")


def create_url():
    return "https://api.twitter.com/2/users/{}/tweets?max_results=100".format(twitter_getUser.twittID())

def get_params():
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

    letter_list = list(pred)
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

    pred = pred + ": \n" + descr
    return pred


# -------------------------------------- Prediction of past type -------------------------------------------

def past_url():
    return "https://api.twitter.com/2/users/{}/tweets?max_results=100&start_time={}-01-01T00:00:00Z&end_time={}-12-01T00:00:00Z".format(twitter_getUser.twittID(), start_time(), start_time())

def connect_to_past_endpoint(url):
    response = requests.request("GET", url, auth=bearer_oauth)
    if response.status_code != 200:
        raise Exception(
            "Request returned an error: {} {}".format(
                response.status_code, response.text
            )
        )
    return response.json()

start_time_var = 0

def start_time():
    current_year = datetime.datetime.today().year
    tree_years_ago_from_current = current_year - 3
    min_allowable_year = current_year - 7 #2010-11-06T00:00:01
    registration_year = twitter_getUser.registrationYear()
    print("Registration: " + str(registration_year))

    global start_time_var
    if registration_year <= min_allowable_year:
        start_time_var = min_allowable_year
    elif min_allowable_year < registration_year < tree_years_ago_from_current:
        start_time_var = registration_year
    else:
        start_time_var = 0
    return start_time_var


def past_ped():
    json_response = connect_to_past_endpoint(past_url())
    json_data = json.dumps(json_response, indent=4, sort_keys=True)
    item_dict = json.loads(json_data)
    print(item_dict)

    if start_time() == 0:
        past_pred = "Sorry, user hasn't been on Twitter long enough."
    elif item_dict['meta']['result_count'] == 0:
        past_pred = "Sorry, there were too few posts this year."
    else:
        json_lenght = len(item_dict['data'])
        text_list = []
        for x in range(1, json_lenght):
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
        past_pred = ''.join(str(e) for e in pred_forest)

        letter_list = list(past_pred)
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

        past_pred = past_pred + ": " + descr
    return past_pred
