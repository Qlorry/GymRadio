import threading
import vlc
import logging
from config import conf
import os

mutex = threading.Lock()


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

    def go_to(self, index):
        try:
            mutex.acquire()
            # Basic
            if self.current == index:
                mutex.release()
                return False
            if index < 0 or index >= len(self.orders_media_list):
                mutex.release()
                logging.error("Invalid index")
                return False
            self.stop()
            self.current = index
            if not self.load_current_song():
                mutex.release()
                self.next()
                return False
            self.play()
            mutex.release()
            return True
        except Exception as e:
            mutex.release()
            logging.error(str(e))
            return False

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
        if have_songs == 1:
            mutex.release()
            return []
        if self.current + 1 >= len(self.orders_media_list):
            mutex.release()
            return []
        if _from < 0 and _to < 0:
            mutex.release()
            return []
        if _to >= have_songs:
            _to = have_songs - 1
        if _from < 0:
            _from = 0
        res = []
        for i in range(_from, _to + 1):  # end not included
            res.append(self.orders_media_list[i])
        mutex.release()
        return res

    def get_next_songs(self, n):
        _from = self.current + 1
        _to = _from + n - 1

        songs = self.get_n_songs(_from, _to)
        return {
            "lastIndex": _from + len(songs) - 1,  # _from already included in songs
            "list": songs
        }

    def get_prev_songs(self, n):
        _from = self.current - n
        _to = self.current - 1

        songs = self.get_n_songs(_from, _to)
        return {
            "firstIndex": _to - len(songs) + 1,
            "list": songs
        }

    def get_all_next_songs(self):
        _from = self.current + 1
        _to = len(self.orders_media_list) - 1

        songs = self.get_n_songs(_from, _to)
        return {
            "lastIndex": _to,
            "list": songs
        }

    def get_all_prev_songs(self):
        _from = 0
        _to = self.current - 1

        songs = self.get_n_songs(_from, _to)
        return {
            "firstIndex": _to,
            "list": songs
        }

    def get_all_songs(self):
        mutex.acquire()
        songs = self.orders_media_list
        mutex.release()
        return songs
