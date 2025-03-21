from flask import session
import requests
from loguru import logger

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


def summarize_article(html):
    h3_tags = html.split('<h3>')
    h3_tags[0] = '<h3>' + h3_tags[0]
    content = h3_tags[0] + h3_tags[1]   #Get html elements contained within first 2 h3 tags
    return content


# if __name__ == '__main__':
#     summarize_article(html)

