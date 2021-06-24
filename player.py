import threading
import time
import vlc
import logging
from config import conf
import os
from downloader import defaultPlaylistId
from youtube_dl.utils import sanitize_filename, sanitize_path

mutex = threading.Lock()
vlc_instance = vlc.Instance()


class Song:
    def __init__(self, name, album=defaultPlaylistId):
        if album is None:
            album = defaultPlaylistId
        self.name = name
        self.playlistId = album

        sanitized_name = sanitize_filename(name, restricted=True)
        sanitized_album = sanitize_filename(album, restricted=True)
        self.path = sanitize_path("music/" + sanitized_album + "/" + sanitized_name + ".m4a")


class OrdersListPlayer:
    def __init__(self):
        self.orders_player = vlc.MediaPlayer()
        self.orders_media_list = []
        self.current = -1
        self.end_callback = None

        player_events = self.orders_player.event_manager()
        print(player_events.event_attach(vlc.EventType.MediaPlayerEndReached, self.next_callback))

    def add_song(self, song):
        mutex.acquire()
        self.orders_media_list.append(song)
        if len(self.orders_media_list) > conf.max_history_size:
            self.orders_media_list.pop(0)
        mutex.release()

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
        th = threading.Thread(target=self.next)
        th.start()

    def next(self):
        while True:
            try:
                mutex.acquire()
                # Basic
                if self.current == -1 and len(self.orders_media_list) == 0:
                    mutex.release()
                    return None
                if self.current + 1 >= len(self.orders_media_list):
                    try:
                        self.end_callback()
                        mutex.release()
                    except Exception as e:
                        mutex.release()
                        return e
                    return None
                self.stop()
                self.current += 1
                if not self.load_current_song():
                    mutex.release()
                    continue
                self.play()
                mutex.release()
                return self.get_current_song()
            except Exception:
                mutex.release()
                continue

    def previous(self):
        while True:
            try:
                mutex.acquire()
                # Basic
                if self.current == -1:
                    mutex.release()
                    return None
                if self.current - 1 < 0:
                    self.stop()
                    self.play()
                    mutex.release()
                    return self.get_current_song()
                self.stop()
                self.current -= 1
                if not self.load_current_song():
                    mutex.release()
                    continue
                self.play()
                mutex.release()
                return self.get_current_song()
            except Exception:
                mutex.release()
                continue

    def get_current_song(self):
        mutex.acquire()
        if self.current == -1:
            mutex.release()
            return None
        res = self.orders_media_list[self.current]
        mutex.release()
        return res

    def get_current_song_mrl(self):
        if self.current == -1:
            return None
        song = self.orders_media_list[self.current]
        return song.path

    def load_current_song(self):
        mrl = self.get_current_song_mrl()
        if not os.path.exists(mrl):
            return
        media = vlc.Media(mrl)
        if media.get_state() == vlc.State.Error:
            media.release()
            return False
        self.orders_player.set_media(media)
        media.release()
        if media.get_state() == vlc.State.Error:
            return False
        if self.orders_player.get_state() == vlc.State.Error:
            return False
        return True

    def get_n_songs(self, _from, _to):
        mutex.acquire()
        if _from is None:
            _from = self.current
        have_songs = len(self.orders_media_list)
        if self.current + 1 >= len(self.orders_media_list):
            mutex.release()
            return []
        if _to >= have_songs:
            _to = have_songs - 1
        res = []
        for i in range(_from, self.current + _to):
            res.append(self.orders_media_list[i])
        if _from == _to:
            res.append(self.orders_media_list[_to])
        mutex.release()
        return res

    def get_next_songs(self, n):
        _from = self.current + 1
        _to = _from + n

        songs = self.get_n_songs(_from, _to)
        return {
            "lastIndex": _from + len(songs),
            "list": songs
        }


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
