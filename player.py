import threading
import time
import vlc
import music_library
from config import conf
import os

defaultPlaylistId = "NA"
vlc_instance = vlc.Instance()


class Song:
    def __init__(self, name, playlistId=defaultPlaylistId):
        self.name = name
        self.playlistId = playlistId


class MyPlayer:
    def __init__(self):
    # RADIO
        self.radio_player = vlc.MediaListPlayer()

        self.radio_media_list = vlc.MediaList()
        media = vlc_instance.media_new("music/Radio/KissFM.m3u")
        self.radio_media_list.add_media(media)
        self.radio_media_list.set_media(media)
        self.radio_player.set_media_list(self.radio_media_list)

        self.player = self.radio_player
    # ORDERS
        self.orders_player = vlc.MediaListPlayer()
        self.orders_player.set_playback_mode(0)

        self.orders_media_list = vlc.MediaList()
        print(self.orders_media_list.count())
        self.orders_player.set_media_list(self.orders_media_list)

        list_player_events = self.orders_player.event_manager()
        list_player_events.event_attach(vlc.EventType.MediaListPlayerNextItemSet, self.next_song_callback)
    # THREAD
        self.th = threading.Thread(target=self.check_thread)
        self.th.start()
    # BOOLS
        self.is_from_radio = True

    def next_song_callback(self, event):
        print("listPlayerCallback:", event.u.media)

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
            media = self.radio_media_list.media()
            if not media.is_parsed():
                media.parse()
            name = media.get_meta(vlc.Meta.Title)
            return os.path.splitext(name)[0]
        else:
            media = self.orders_media_list.media()
            if not media.is_parsed():
                media.parse()
            return media.get_meta(vlc.Meta.Title)

    def play(self):
        self.player.play()

    def pause(self):
        self.player.pause()

    def stop(self):
        self.player.stop()

    def next(self):
        if self.is_from_radio:
            return "Radio"
        if self.player.next() == -1:
            self.switch_to_radio()
            self.play()
            return "No more songs, going to radio"

    def prev(self):
        if self.is_from_radio:
            return "Radio"
        if self.player.previous() == -1:
            self.stop()
            self.play()

    def add_song(self, song):
        media = vlc_instance.media_new("music/" + song.playlistId + "/" + song.name + ".m4a")
        media.parse()
        # LOCK
        self.orders_media_list.lock()
        self.orders_media_list.add_media(media)
        if self.orders_media_list.count() > conf.max_history_size:
            self.orders_media_list.remove_index(0)
        #UNLOCK
        self.orders_media_list.unlock()
        self.orders_media_list.set_media(media)
        if self.is_from_radio:
            self.switch_to_orders()
            self.play()

    def switch_to_orders(self):
        self.is_from_radio = False
        self.stop()
        self.player = self.orders_player

    def switch_to_radio(self):
        self.is_from_radio = True
        self.stop()
        self.player = self.radio_player

    def load_station(self, station_name):
        self.radio_media_list = vlc_instance.media_list_new()
        media = vlc_instance.media_new("music/Radio/" + station_name + ".m3u")
        self.radio_media_list.add_media(media)
        self.radio_media_list.set_media(media)
        self.radio_player.set_media_list(self.radio_media_list)
