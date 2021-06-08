import threading
import time
import random

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

        self.radio_player = self.vlc_instance.media_list_player_new()
        self.radio_media_list = self.vlc_instance.media_list_new()
        self.radio_player.set_media_list(self.radio_media_list)

        self.orders_player = self.vlc_instance.media_list_player_new()
        self.orders_media_list = self.vlc_instance.media_list_new()
        self.orders_player.set_media_list(self.orders_media_list)

        self.player = self.radio_player

        media = self.vlc_instance.media_new("music/Radio/KissFM.m3u")
        # LOCK
        self.radio_media_list.lock()
        self.radio_media_list.add_media(media)
        # UNLOCK
        self.radio_media_list.unlock()

    # SONG LISTS
    #     self.history = []
    #     self.up_next = []
        self.library = music_library.get_song_library()
    #     self.order = []
    # DATA NOW
    #     self.current_song = None
        # self.next(False)
        self.th = threading.Thread(target=self.check_thread)
        self.th.start()
    # BOOLS
        self.is_from_radio = True

    def check_thread(self):
        while True:
            time.sleep(0.5)
            if self.is_from_radio:
                time.sleep(1)
            state = self.player.get_state()
            if state == vlc.State(6): #Ended
                self.switch_to_radio()

    def is_now_playing(self):
        return self.player.is_playing()

    def play(self):
        # self.is_now_playing = True
        self.player.play()

    def pause(self):
        # self.is_now_playing = False
        self.player.pause()

    def stop(self):
        # self.is_now_playing = False
        self.player.stop()

    def next(self, play=True):
        # if len(self.up_next) == 0:
        #     if len(self.library) == 0:
        #         self.load_library()
        #     self.up_next = self.library
        # song = self.up_next.pop(0)
        # if len(self.history) > 100:
        #     self.history.pop(0)
        # if self.current_song is not None:
        #     self.history.append(self.current_song)
        # self.load(song)
        if self.is_from_radio:
            return #this is radio dovboiob
        if self.player.next() == -1:
            self.switch_to_radio()
            return "No more songs, going to radio"
        if play:
            self.play()

    def prev(self, play=True):
        # if len(self.history) == 0:
        #     return
        # song = self.history.pop()
        # self.up_next.insert(0, self.current_song)
        # self.load(song)
        if self.is_from_radio:
            return #this is radio dovboiob
        if self.player.previous() == -1:
            self.stop()
            self.play()
        if play:
            self.play()

    def add_song(self, song):
        media = self.vlc_instance.media_new("music/" + song.playlistId + "/" + song.name + ".m4a")
        # LOCK
        self.orders_media_list.lock()
        self.orders_media_list.add_media(media)
        #UNLOCK
        self.orders_media_list.unlock()
        # self.order.append(song)
        if self.is_from_radio:
            self.switch_to_orders()
            self.play()

    def get_next_song_name(self):
        return "11111111"
        # if len(self.up_next) == 0:
        #     return self.history[0].name
        # return self.up_next[0].name

    def get_prev_song_name(self):
        return "11111111"
        # if len(self.history) < 1:
        #     return ""
        # return self.history[len(self.history) - 1].name

    def load_library(self):
        self.library = music_library.get_song_library()

    # def switch_to_library(self):
    #     self.is_from_library = True
    #     self.is_from_radio = False
        # self.up_next = self.library

    def switch_to_orders(self):
        self.is_from_radio = False
        self.stop()
        self.player = self.orders_player

    def switch_to_radio(self):
        self.is_from_radio = True
        self.stop()
        self.player = self.radio_player

    def shuffle_lib(self):
        random.shuffle(self.library)
