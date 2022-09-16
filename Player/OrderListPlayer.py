import threading
import vlc
import logging
from Config.config import conf
import util
import os
from enum import Enum


class ChangeSongRes(Enum):
    begin = 1
    end = 2
    empty_list = 3


class OrdersListPlayer:
    def __init__(self):
        self._mutex = threading.Lock()
        self._orders_player = vlc.MediaPlayer()
        self._orders_media_list = []
        self._current = -1
        self._end_callback = None
        player_events = self._orders_player.event_manager()
        print(player_events.event_attach(vlc.EventType.MediaPlayerEndReached, self.next_callback))

    def current(self):
        self._mutex.acquire()
        curr = self._current
        self._mutex.release()
        return curr

    def add_song(self, song):
        self._mutex.acquire()
        self._orders_media_list.append(song)
        if len(self._orders_media_list) > conf.max_history_size:
            self._orders_media_list.pop(0)
        self._mutex.release()

    def play(self):
        if self._current == -1:
            return
        return self._orders_player.play()

    def pause(self):
        return self._orders_player.pause()

    def is_playing(self):
        return self._orders_player.is_playing()

    def set_callback(self, callback_func):
        self._end_callback = callback_func

    def stop(self):
        return self._orders_player.stop()

    def next_callback(self, e):
        print(e)
        th = threading.Thread(target=self.next)
        th.start()

    def next(self):
        while True:
            try:
                self._mutex.acquire()
                # Basic
                if self._current == -1 and len(self._orders_media_list) == 0:
                    self._mutex.release()
                    self._end_callback()
                    return ChangeSongRes.empty_list
                if self._current + 1 >= len(self._orders_media_list):
                    try:
                        self._end_callback()
                        self.stop()
                        self._mutex.release()
                    except Exception as e:
                        self._mutex.release()
                        return e
                    return ChangeSongRes.end
                self.stop()
                self._current += 1
                if not self.load_current_song():
                    self._mutex.release()
                    continue
                self.play()
                self._mutex.release()
                return self.get_current()
            except Exception:
                self._mutex.release()
                continue

    def previous(self):
        while True:
            try:
                self._mutex.acquire()
                # Basic
                if self._current == -1:
                    self._mutex.release()
                    return None
                if self._current - 1 < 0:
                    self.stop()
                    self.play()
                    self._mutex.release()
                    return self.get_current()
                self.stop()
                self._current -= 1
                if not self.load_current_song():
                    self._mutex.release()
                    continue
                self.play()
                self._mutex.release()

                return self.get_current()
            except Exception:
                self._mutex.release()
                continue

    def go_to(self, index):
        try:
            self._mutex.acquire()
            # Basic
            if self._current == index:
                self._mutex.release()
                return False
            if index < 0 or index >= len(self._orders_media_list):
                self._mutex.release()
                logging.error("Invalid index")
                return False
            self.stop()
            self._current = index
            if not self.load_current_song():
                self._mutex.release()
                self.next()
                return False
            self.play()
            self._mutex.release()
            return True
        except Exception as e:
            self._mutex.release()
            logging.error(str(e))
            return False

    def get_current(self):
        self._mutex.acquire()
        if self._current == -1:
            self._mutex.release()
            return None
        res = self._orders_media_list[self._current]
        self._mutex.release()
        return res

    def get_current_song_mrl(self):
        if self._current == -1:
            return None
        song = self._orders_media_list[self._current]
        return song.path

    def load_current_song(self):
        mrl = self.get_current_song_mrl()
        if not util.is_song_p_in_os(mrl):
            return
        media = vlc.Media(mrl)
        if media.get_state() == vlc.State.Error:
            media.release()
            return False
        self._orders_player.set_media(media)
        media.release()
        if media.get_state() == vlc.State.Error:
            return False
        if self._orders_player.get_state() == vlc.State.Error:
            return False
        return True

    def get_n_songs(self, _from, _to):
        self._mutex.acquire()
        if _from is None:
            _from = self._current
        have_songs = len(self._orders_media_list)
        if have_songs == 1:
            self._mutex.release()
            return []
        # if self._current + 1 >= len(self._orders_media_list):
        #     self._mutex.release()
        #     return []
        if _from < 0 and _to < 0:
            self._mutex.release()
            return []
        if _to >= have_songs:
            _to = have_songs - 1
        if _from < 0:
            _from = 0
        res = []
        for i in range(_from, _to + 1):  # end not included
            res.append(self._orders_media_list[i])
        self._mutex.release()
        return res

    def get_next_songs(self, n):
        _from = self._current + 1
        _to = _from + n - 1

        songs = self.get_n_songs(_from, _to)
        return {
            "lastIndex": _from + len(songs) - 1,  # _from already included in songs
            "list": songs
        }

    def get_prev_songs(self, n):
        _from = self._current - n
        _to = self._current - 1

        songs = self.get_n_songs(_from, _to)
        return {
            "firstIndex": _to - len(songs) + 1,
            "list": songs
        }

    def get_all_next_songs(self):
        _from = self._current + 1
        _to = len(self._orders_media_list) - 1

        songs = self.get_n_songs(_from, _to)
        return {
            "lastIndex": _to,
            "list": songs
        }

    def get_all_prev_songs(self):
        _from = 0
        _to = self._current - 1

        songs = self.get_n_songs(_from, _to)
        return {
            "firstIndex": _to,
            "list": songs
        }

    def get_all_songs(self):
        self._mutex.acquire()
        songs = self._orders_media_list
        self._mutex.release()
        return songs

    def swap(self, first_index, second_index):
        self._mutex.acquire()
        if first_index == self._current or second_index == self._current :
            return
        if first_index == second_index:
            return

        if first_index > second_index:
            t = first_index
            first_index = second_index
            second_index = t

        f_song = self._orders_media_list.pop(first_index - 1)
        s_song = self._orders_media_list.pop(second_index - 2)

        self._orders_media_list.insert(first_index - 1, s_song)
        self._orders_media_list.insert(second_index - 1, f_song)

        self._mutex.release()
