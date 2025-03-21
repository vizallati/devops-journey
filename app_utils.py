from flask import session
import requests


json_converter_endpoint = "https://api.rss2json.com/v1/api.json"
medium_username = "iekwoge"

def check_user_auth():
    try:
        return session['loggedin']
    except KeyError:
        return False



def convert_rrs_to_json():
     response = requests.get(f'{json_converter_endpoint}?rss_url=https:%2F%2Fmedium.com%2F@{medium_username}5%2Ffeed')
     return response.json()["items"]