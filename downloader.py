from youtube_dl import YoutubeDL


class Downloader:
    def __init__(self):
        self.audio_downloader = YoutubeDL({'format': 'm4a',
                                           'outtmpl': 'music/%(playlist_title)s/%(title)s.m4a',
                                           'postprocessors': [{
                                               'key': 'FFmpegMetadata'
                                           }]
                                           })

    def load(self, url):
        return self.audio_downloader.extract_info(url)
