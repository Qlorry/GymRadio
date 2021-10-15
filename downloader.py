import logging
import util

from youtube_dl import YoutubeDL
defaultPlaylistId = "NA"


# 'restrictfilenames': True
class Downloader:
    def __init__(self):
        self.audio_downloader = YoutubeDL({'format': 'm4a',
                                           'outtmpl': 'music/%(album)s/%(title)s.m4a',
                                           'nooverwrites': True,
                                           'postprocessors': [{
                                               'key': 'FFmpegMetadata'
                                           }]
                                           })

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
            if not util.is_song_in_os(album, name):
                return None
            return res
        except Exception as e:
            logging.warning("Error downloading song" + str(e))
            return None
