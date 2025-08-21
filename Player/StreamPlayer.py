import threading
import vlc
import logging
from Config.config import conf
import os

mutex = threading.Lock()


class StreamPlayer:
    def __init__(self, station_name):
        self.stream_player = vlc.MediaListPlayer()

    def play(self):
        return self.stream_player.play()

    def pause(self):
        return self.stream_player.pause()

    def is_playing(self):
        return self.stream_player.is_playing()

    def stop(self):
        return self.stream_player.stop()
    
    def set_callback(self, callback_func):
        self._end_callback = callback_func



