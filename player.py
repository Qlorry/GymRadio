import threading
import time
import vlc
import music_library
from config import conf

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
        self.orders_player.set_playback_mode(0)
        self.orders_player.set_media_list(self.orders_media_list)

        self.player = self.radio_player

        media = self.vlc_instance.media_new("music/Radio/KissFM.m3u")
        # LOCK
        self.radio_media_list.lock()
        self.radio_media_list.add_media(media)
        # UNLOCK
        self.radio_media_list.unlock()

        list_player_events = self.orders_player.event_manager()
        list_player_events.event_attach(vlc.EventType.MediaListPlayerNextItemSet, self.next_song_callback)
    # THREAD
        self.th = threading.Thread(target=self.check_thread)
        self.th.start()
    # BOOLS
        self.is_from_radio = True

    def next_song_callback(event):
        print
        "listPlayerCallback:", event.type, event.u

    def check_thread(self):
        while True:
            time.sleep(0.5)
            if self.is_from_radio:
                time.sleep(1)
            state = self.player.get_state()
            if state == vlc.State(6): #Ended
                self.switch_to_radio()
                self.play()

    def is_now_playing(self):
        return self.player.is_playing()

    def whats_playing(self):
        if self.is_from_radio:
            return "Radio"
        return self.get_song_name()

    def play(self):
        self.player.play()

    def pause(self):
        self.player.pause()

    def stop(self):
        self.player.stop()

    def next(self):
        if self.is_from_radio:
            return #this is radio dovboiob
        if self.player.next() == -1:
            self.switch_to_radio()
            self.play()
            return "No more songs, going to radio"

    def prev(self):

        if self.is_from_radio:
            return #this is radio dovboiob
        if self.player.previous() == -1:
            self.stop()
            self.play()

    def add_song(self, song):
        media = self.vlc_instance.media_new("music/" + song.playlistId + "/" + song.name + ".m4a")
        # LOCK
        self.orders_media_list.lock()
        self.orders_media_list.add_media(media)
        if self.orders_media_list.count() > conf.max_history_size:
            self.orders_media_list.remove_index(0)
        #UNLOCK
        self.orders_media_list.unlock()
        # self.order.append(song)
        if self.is_from_radio:
            self.switch_to_orders()
            self.play()

    def get_song_name(self):
        return "111"
        # if len(self.up_next) == 0:
        #     return self.history[0].name
        # return self.up_next[0].name

    def switch_to_orders(self):
        self.is_from_radio = False
        self.stop()
        self.player = self.orders_player

    def switch_to_radio(self):
        self.is_from_radio = True
        self.stop()
        self.player = self.radio_player

    def load_station(self, station_name):
        self.radio_media_list = self.vlc_instance.media_list_new()
        media = self.vlc_instance.media_new("music/Radio/" + station_name + ".m3u")
        self.radio_media_list.add_media(media)
        self.radio_player.set_media_list(self.radio_media_list)
    # def shuffle_lib(self):
    #     random.shuffle(self.library)
    #
    # def load_library(self):
    #     self.library = music_library.get_song_library()
    #
    # def switch_to_library(self):
    #     self.is_from_library = True
    #     self.is_from_radio = False
        # self.up_next = self.library
