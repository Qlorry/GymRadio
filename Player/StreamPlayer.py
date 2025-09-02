import threading
import vlc
import logging

import yt_dlp
from Config.config import conf
import os

mutex = threading.Lock()

ydl_opts = {
    'format': 'bestaudio/best',  # pick best available
    'quiet': True,
}

class StreamPlayer:
    def __init__(self):
        self.stream_player: vlc.MediaListPlayer = vlc.MediaListPlayer()

        self.stream_names = []
        self.stream_links = []
        self.real_stream_links = {}
        self.current_stream_index = 0

        self.media_list = vlc.MediaList()

        index = 0
        for stream_name in conf.streams.keys():
            self.stream_links.append(conf.streams[stream_name])
            self.stream_names.append(stream_name)
        
            if stream_name == conf.default_stream:
                self.current_stream_index = index
            index += 1

        self.stream_player.set_media_list(self.media_list)


    def _add_to_media_list(self, index):
        if self.stream_names[index] in self.real_stream_links.keys():
            return
        link = self._get_real_stream_link(index)
        self.real_stream_links[self.stream_names[index]] = link
        media = vlc.Media(link, "no-video")
        self.media_list.add_media(media)

    def _get_real_stream_link(self, index):
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(self.stream_links[index], download=False)
            return info['url']

    def play(self):
        self._add_to_media_list(self.current_stream_index)
        return self.stream_player.play()

    def pause(self):
        return self.stream_player.pause()

    def is_playing(self):
        return self.stream_player.is_playing()

    def stop(self):
        return self.stream_player.stop()
    
    def set_callback(self, callback_func):
        self._end_callback = callback_func

    def next(self):
        if self.current_stream_index + 1 == len(self.stream_names):
            self.current_stream_index = 0
        else:
            self.current_stream_index += 1
        self._add_to_media_list(self.current_stream_index)
        self.stream_player.next()
        return self.stream_names[self.current_stream_index]

    def previous(self):
        if self.current_stream_index - 1 < 0:
            self.current_stream_index = len(self.stream_names) - 1
        else:
            self.current_stream_index -= 1
        self._add_to_media_list(self.current_stream_index)
        self.stream_player.next()
        return self.stream_names[self.current_stream_index]
    
    def get_current(self):
        return self.stream_names[self.current_stream_index]



