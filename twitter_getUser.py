import requests
import os
from flask import Flask, request

# To set your enviornment variables in your terminal run the following line:
# export 'BEARER_TOKEN'='<your_bearer_token>'
bearer_token = os.environ.get("bearer_token")


def create_url():
    twitter_name = 'realDonaldTrump' # placeholder for testing
    #twitter_name = request.form.get("twittname")
    usernames = "usernames=" + twitter_name + ",TwitterAPI"
    user_fields = "user.fields=created_at,name"

    url = "https://api.twitter.com/2/users/by?{}&{}".format(usernames, user_fields)
    return url


def bearer_oauth(r):
    """
    Method required by bearer token authentication.
    """
    r.headers["Authorization"] = f"Bearer {bearer_token}"
    r.headers["User-Agent"] = "v2UserLookupPython"
    return r


def connect_to_endpoint(url):
    response = requests.request("GET", url, auth=bearer_oauth)
    if response.status_code != 200:
        raise Exception(
            "Request returned an error: {} {}".format(
                response.status_code, response.text
            )
        )
    return response.json()

def errorCheck():
    url = create_url()
    json_response = connect_to_endpoint(url)
    error = False
    if "errors" in json_response:
        error = True
    return error

def error_reason():
    url = create_url()
    json_response = connect_to_endpoint(url)
    error_reason = json_response['errors'][0]['detail']
    #error_reason = ''.join(str(e) for e in error_reason)
    #print(error_reason)
    return error_reason

def realName():
    url = create_url()
    json_response = connect_to_endpoint(url)
    real_name = json_response['data'][0]['name']
    return real_name

def createDate():
    url = create_url()
    json_response = connect_to_endpoint(url)
    created_at = json_response['data'][0]['created_at']
    return created_at

def twittID():
    url = create_url()
    json_response = connect_to_endpoint(url)
    twitter_id = json_response['data'][0]['id'] #813286
    return twitter_id

def testResponse():
    url = create_url()
    json_response = connect_to_endpoint(url)
    return json_response

if __name__ == "__main__":
    error_reason()
