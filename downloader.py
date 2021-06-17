from youtube_dl import YoutubeDL


class Downloader:
    def __init__(self):
        self.audio_downloader = YoutubeDL({'format': 'm4a',
                                           'outtmpl': 'music/%(album)s/%(title)s.m4a',
                                           'postprocessors': [{
                                               'key': 'FFmpegMetadata'
                                           }]
                                           })

    def load_info(self, url):
        return self.audio_downloader.extract_info(url, download=False)

    def load(self, url):
        try:
            return self.audio_downloader.extract_info(url)
        except Exception:
            return None
