import requests
import json


def create_request_url(song_url):
    base = 'https://api.song.link/v1-alpha.1/links?url='
    return base + song_url


def get_data_in_json(request_link):
    data = requests.get(request_link)
    print(data.text)
    return data.text


def get_yt_link(data_json):
    temp = []
    youtubeMusic = data_json['linksByPlatform'].get('youtubeMusic')
    if youtubeMusic is not None:
        temp.append(youtubeMusic.get('url'))

    youtube = data_json['linksByPlatform'].get('youtube')
    if youtube is not None:
        temp.append(youtube.get('url'))

    print(temp)
    return temp


def convert(url):
    link = create_request_url(url)
    data = get_data_in_json(link)
    data_dict = json.loads(data)
    if len(data_dict) == 0:
        return ""
    if data_dict.get('statusCode') is not None:
        if data_dict['statusCode'] == 400:
            return ""
    yt_links = get_yt_link(data_dict)
    return yt_links
