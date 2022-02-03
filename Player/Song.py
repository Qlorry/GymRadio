from DataDownloader.downloader import defaultPlaylistId
from youtube_dl.utils import sanitize_filename, sanitize_path


class Song:
    def __init__(self, name, album=defaultPlaylistId):
        if album is None:
            album = defaultPlaylistId
        self.name = name
        self.playlistId = album

        sanitized_name = sanitize_filename(name, restricted=False)
        sanitized_album = sanitize_filename(album, restricted=False)
        self.path = sanitize_path("music/" + sanitized_album + "/" + sanitized_name + ".m4a")
