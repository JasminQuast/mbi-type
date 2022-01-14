# import requests
# import os
# import json
# import twitter_getUser
# import pandas as pd
# from sklearn.feature_extraction.text import CountVectorizer
# from sklearn.ensemble import RandomForestClassifier
# import type_classificator
# import datetime
#
# bearer_token = os.environ.get("bearer_token")
#
#
# def past_url():
#     return "https://api.twitter.com/2/users/{}/tweets?max_results=100&start_time={}-01-01T00:00:00Z&end_time={}-01-01T00:00:00Z".format(twitter_getUser.twittID(), start_time(), end_time())
#
#
# def get_params():
#     return {"tweet.fields": "created_at"}
#
#
# def bearer_oauth(r):
#     """
#     Method required by bearer token authentication.
#     """
#     r.headers["Authorization"] = f"Bearer {bearer_token}"
#     r.headers["User-Agent"] = "v2UserTweetsPython"
#     return r
#
#
# def connect_to_endpoint(url, params):
#     response = requests.request("GET", url, auth=bearer_oauth, params=params)
#     if response.status_code != 200:
#         raise Exception(
#             "Request returned an error: {} {}".format(
#                 response.status_code, response.text
#             )
#         )
#     return response.json()
#
# start_time_var = 0
#
# def start_time():
#     current_year = datetime.datetime.today().year
#     tree_years_ago_from_current = current_year - 3
#     min_allowable_year = 2011 #2010-11-06T00:00:01
#     registration_year = twitter_getUser.registrationYear()
#     print(registration_year)
#
#     global start_time_var
#     if registration_year <= min_allowable_year:
#         start_time_var = min_allowable_year
#         test = "vor 2011 angemendet"
#     elif min_allowable_year < registration_year < tree_years_ago_from_current:
#         start_time_var = registration_year
#         test = "zwischen 2011 und 2019 angemendet"
#     else:
#         start_time_var = 0
#         test = "nach 2019 angemendet"
#     #print(test)
#     return start_time_var
#
# end_time_var = 0
#
# def end_time():
#     global end_time_var
#     if start_time_var != 0:
#         end_time_var = start_time_var + 1
#     return end_time_var
#
# def past_ped():
#     if start_time_var == 0:
#         past_pred = "Sorry, the user hasn't been on Twitter long enough."
#     else:
#         json_response = connect_to_endpoint(past_url(), get_params())
#         json_data = json.dumps(json_response, indent=4, sort_keys=True)
#         item_dict = json.loads(json_data)
#         json_lenght = len(item_dict['data'])
#
#         text_list = []
#         for x in range(1, json_lenght):
#             if (json_response['data'][x]['lang']) == 'en':
#                 text_list.append(json_response['data'][x]['text'])
#
#         big_text_list = ' '.join(text_list)
#         df = pd.DataFrame([big_text_list])
#         df.columns = ["posts"]
#
#         tokenlist_training_dataset = list(type_classificator.training.iloc[:, 2:])
#         count_vect_twitt = CountVectorizer(input=[big_text_list], vocabulary=tokenlist_training_dataset)
#         count_vect_twitt.get_feature_names()
#
#         x_twitt = count_vect_twitt.fit_transform([big_text_list])
#
#         forest = RandomForestClassifier()
#         forest.fit(type_classificator.X_train, type_classificator.training["target_variable"])
#         pred_forest = forest.predict(x_twitt)
#         past_pred = ''.join(str(e) for e in pred_forest)
#         return past_pred
#
#
# if __name__ == "__main__":
#    start_time()
#    past_ped()
#
