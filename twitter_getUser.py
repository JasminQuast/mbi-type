import requests
import os
from flask import Flask, request


# bearer_token = os.environ.get("bearer_token")  # Encoded Token for GitHub
bearer_token = "AAAAAAAAAAAAAAAAAAAAACoHWgEAAAAAsJqMO1RYRqlQviQA%2BLTX%2BHw12BM%3DHWNW4RGiwP9YzYxfwnwgamb9SzFZmZhDsJgHPLVCLWf0DM18QK"


def create_url():
    #twitter_name = 'BarackObama' # placeholder for testing
    twitter_name = request.form.get("twittname")
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


def error_check():
    """
    Check if any errors in response, e.g. the user has been suspended
    """
    url = create_url()
    json_response = connect_to_endpoint(url)
    error = False
    if "errors" in json_response:
        error = True
    return error


def error_reason():
    """
    Reason of the error
    """
    json_response = connect_to_endpoint(create_url())
    error_reason = str(json_response['errors'][0]['detail'])
    return error_reason


def real_name():
    """
    Name of the Twitter user
     """
    url = create_url()
    json_response = connect_to_endpoint(url)
    real_name = json_response['data'][0]['name']
    return real_name


def registration_year():
    """
    Year of the registration by taking the first 4 characters of the date of registration
     """
    json_response = connect_to_endpoint(create_url())
    created_at = str(json_response['data'][0]['created_at'])
    registration_year = int(created_at[0:4])
    return registration_year


def twitt_id():
    """
    ID of the Twitter user
    """
    json_response = connect_to_endpoint(create_url())
    twitter_id = json_response['data'][0]['id']
    return twitter_id
