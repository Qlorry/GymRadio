import logging
import os
import Util.util as util

from yt_dlp import YoutubeDL

defaultPlaylistId = "NA"

def my_hook(d):
    if d['status'] == 'finished':
        print('Done downloading, now converting ...')

class Downloader:
    def __init__(self):
        ydl_opts = {
            'format': 'm4a',
            'outtmpl': 'music/%(album)s/%(title)s.m4a',
            'nooverwrites': True,
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredquality': '192',
            }],     
            'progress_hooks': [my_hook],
        }
        self.audio_downloader = YoutubeDL(ydl_opts)

    def load_info(self, url):
        try:
            return self.audio_downloader.extract_info(url, download=False)
        except Exception as e:
            logging.warning("Error loading song info" + str(e))
            return []

    def load(self, url):
        try:
            res = self.audio_downloader.extract_info(url)

            name = res.get('title') if res.get('title') is not None else ""
            album = res.get('album') if res.get('album') is not None else "NA"
            if util.is_song_in_os(album, name):
                return res
            return None
        except Exception as e:
            logging.warning("Error downloading song" + str(e))
            return None
