import time
import vlc
import logging
import os

from Player.OrderListPlayer import OrdersListPlayer
from config import conf


vlc_instance = vlc.Instance()


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
        # BOOLS
        self.is_from_radio = True

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
            self.player.next()
            self.player.next()
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
        self.play()

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

    def get_n_songs(self, _from, _to):
        if self.is_from_radio:
            return []
        return self.player.get_n_songs(_from, _to)

    def get_next_songs(self, n):
        if self.is_from_radio:
            return {
                "lastIndex": -1,
                "list": []
            }
        return self.player.get_next_songs(n)

    def get_prev_songs(self, n):
        if self.is_from_radio:
            return {
                "firstIndex": -1,
                "list": []
            }
        return self.player.get_prev_songs(n)

    def go_to(self, index):
        self.orders_player.go_to(index)
        if self.is_from_radio:
            self.switch_to_orders()

    def get_all_songs(self):
        return self.orders_player.get_all_songs()

    def get_current_index(self):
        if self.is_from_radio:
            return None
        return self.orders_player.current
