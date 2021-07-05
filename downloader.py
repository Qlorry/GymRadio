import logging

from youtube_dl import YoutubeDL
defaultPlaylistId = "NA"


# 'restrictfilenames': True
class Downloader:
    def __init__(self):
        self.audio_downloader = YoutubeDL({'format': 'm4a',
                                           'outtmpl': 'music/%(album)s/%(title)s.m4a',
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
            return self.audio_downloader.extract_info(url)
        except Exception as e:
            logging.warning("Error downloading song" + str(e))
            return None
