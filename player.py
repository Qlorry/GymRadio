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


class OrdersListPlayer:
    def __init__(self):
        self.orders_player = vlc.MediaPlayer()
        self.orders_media_list = []
        self.current = -1
        self.end_callback = None

        player_events = self.orders_player.event_manager()
        print(player_events.event_attach(vlc.EventType.MediaPlayerEndReached, self.next_callback))

    def add_song(self, song):
        self.orders_media_list.append(song)
        if len(self.orders_media_list) > conf.max_history_size:
            self.orders_media_list.pop(0)

    def play(self):
        if self.current == -1:
            return
        return self.orders_player.play()

    def pause(self):
        return self.orders_player.pause()

    def is_playing(self):
        return self.orders_player.is_playing()

    def set_callback(self, callback_func):
        self.end_callback = callback_func

    def stop(self):
        return self.orders_player.stop()

    def next_callback(self, e):
        print(e)
        th = threading.Thread(target=self.next, args=[True])
        th.start()

    def next(self, play=False):
        if self.current == -1 and len(self.orders_media_list) == 0:
            return None
        if self.current + 1 >= len(self.orders_media_list):
            try:
                self.end_callback()
            except Exception as e:
                return e
            return None
        played = self.is_playing()
        self.orders_player.stop()
        self.current += 1
        self.load_current_song()
        if played or play:
            self.play()
        return self.get_current_song()

    def previous(self):
        if self.current == -1:
            return None
        if self.current - 1 < 0:
            self.stop()
            self.play()
            return self.get_current_song()
        played = self.is_playing()
        self.orders_player.stop()
        self.current -= 1
        self.load_current_song()
        if played:
            self.play()
        return self.get_current_song()

    def get_current_song(self):
        if self.current == -1:
            return None
        return self.orders_media_list[self.current]

    def get_current_song_mrl(self):
        song = self.get_current_song()
        return "music/" + song.playlistId + "/" + song.name + ".m4a"

    def load_current_song(self):
        media = vlc.Media(self.get_current_song_mrl())
        self.orders_player.set_media(media)


class SuperPlayer:
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
        self.orders_player = OrdersListPlayer()
        self.orders_player.set_callback(self.switch_to_radio)
        # list_player_events = self.orders_player.event_manager()
        # list_player_events.event_attach(vlc.EventType.MediaListPlayerNextItemSet, self.next_song_callback)
        # THREAD
        #     self.th = threading.Thread(target=self.check_thread)
        # self.th.start()
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
            if state == vlc.State(6):  # Ended
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
            res = self.player.get_current_song()
            if res is None:
                return "None"
            return res.name

    def play(self):
        self.player.play()

    def pause(self):
        self.player.pause()

    def stop(self):
        self.player.stop()

    def next(self):
        if self.is_from_radio:
            return "Radio"
        return self.player.next()

    def prev(self):
        if self.is_from_radio:
            return "Radio"
        return self.player.previous()

    def add_song(self, song):
        self.orders_player.add_song(song)
        if self.is_from_radio:
            self.switch_to_orders()
            self.next()
            self.play()

    def switch_to_orders(self):
        self.is_from_radio = False
        self.stop()
        self.player = self.orders_player

    def switch_to_radio(self):
        self.is_from_radio = True
        self.stop()
        self.player = self.radio_player
        self.play()

    def load_station(self, station_name):
        self.radio_media_list = vlc_instance.media_list_new()
        media = vlc_instance.media_new("music/Radio/" + station_name + ".m3u")
        self.radio_media_list.add_media(media)
        self.radio_media_list.set_media(media)
        self.radio_player.set_media_list(self.radio_media_list)
