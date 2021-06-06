import requests
import json


def create_request_url(song_url):
    base = 'https://api.song.link/v1-alpha.1/links?url='
    return base + song_url


def get_data_in_json(request_link):
    data = requests.get(request_link)
    print(data.text)
    #check status code
    return data.text


def get_yt_link(data_json):
    data_py = json.loads(data_json)
    print(data_py['linksByPlatform'].get('youtubeMusic').get('url'))
    return data_py['linksByPlatform'].get('youtubeMusic').get('url')


def convert(url):
    link = create_request_url(url)
    data = get_data_in_json(link)
    yt_link = get_yt_link(data)
    return yt_link
