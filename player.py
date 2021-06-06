import threading
import time
import vlc
import music_library

defaultPlaylistId = "NA"


class Song:
    def __init__(self, name, playlistId=defaultPlaylistId):
        self.name = name
        self.playlistId = playlistId


class MyPlayer:
    def __init__(self):
    # VLC
        self.vlc_instance = vlc.Instance()
        self.vlc_player = self.vlc_instance.media_player_new()
    # SONG LISTS
        self.history = []
        self.up_next = []
        self.library = music_library.get_song_library()
        self.order = []
    # DATA NOW
        self.current_song = None
        self.media = None
        # self.next(False)
        self.th = threading.Thread(target=self.check_thread)
        self.th.start()
    # BOOLS
        self.is_from_library = True
        self.is_now_playing = False

    def check_thread(self):
        while True:
            time.sleep(0.5)
            songTime = self.vlc_player.get_position()
            if songTime == -1:
                time.sleep(0.5)
                continue
            if songTime > 0.998:
                self.next()

    def play(self):
        self.is_now_playing = True
        self.vlc_player.play()

    def stop(self):
        self.is_now_playing = False
        self.vlc_player.stop()

    def next(self, play=True):
        if len(self.up_next) == 0:
            self.load_library()
            self.up_next = self.library
        song = self.up_next.pop(0)
        if len(self.history) > 100:
            self.history.pop(0)
        if self.current_song is not None:
            self.history.append(self.current_song)
        self.load(song)
        if play:
            self.play()

    def prev(self, play=True):
        if len(self.history) == 0:
            return
        song = self.history.pop()
        self.up_next.insert(0, self.current_song)
        self.load(song)
        if play:
            self.play()

    def load(self, song):
        self.current_song = song
        self.media = self.vlc_instance.media_new("music/" + song.playlistId + "/" + song.name + ".m4a")
        self.vlc_player.set_media(self.media)

    def add_song(self, song):
        self.order.append(song)

    def get_next_song_name(self):
        if len(self.up_next) == 0:
            return self.history[0].name
        return self.up_next[0].name

    def get_prev_song_name(self):
        if len(self.history) < 1:
            return ""
        return self.history[len(self.history) - 1].name

    def load_library(self):
        self.library = music_library.get_song_library()

    def switch_to_library(self):
        self.up_next = self.library
        self.next()

    def switch_to_orders(self):
        self.up_next = self.order
        self.next()
