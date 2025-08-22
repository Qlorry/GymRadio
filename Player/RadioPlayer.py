import threading
import vlc
import logging
from Config.config import conf
import os

mutex = threading.Lock()


class RadioPlayer:
    def __init__(self, station_name):
        self.radio_player = vlc.MediaListPlayer()
        self.radio_media_list = None
        self.sub_stations = []
        self.station_index = 0

        self.load_station(station_name)

    def play(self):
        return self.radio_player.play()

    def pause(self):
        return self.radio_player.pause()

    def is_playing(self):
        return self.radio_player.is_playing()

    def stop(self):
        self.station_index = 0
        return self.radio_player.stop()

    def next(self):
        if self.station_index + 1 == len(self.sub_stations):
            self.station_index = 0
        else:
            self.station_index += 1
        self.radio_player.next()
        self.radio_player.next()
        return self.sub_stations[self.station_index]

    def previous(self):
        if self.station_index - 1 < 0:
            self.station_index = len(self.sub_stations) - 1
        else:
            self.station_index -= 1
        self.radio_player.previous()
        self.radio_player.previous()
        return self.sub_stations[self.station_index]

    def get_current(self):
        return self.sub_stations[self.station_index]

    def load_station(self, station_name):
        self.load_sub_stations(station_name)

        self.radio_media_list = vlc.MediaList()
        media = vlc.Media("Radio/" + station_name + ".m3u")
        self.radio_media_list.add_media(media)
        self.radio_media_list.set_media(media)
        self.radio_player.set_media_list(self.radio_media_list)
        return self.sub_stations[self.station_index]

    def load_sub_stations(self, station_name):
        file = open("Radio/" + station_name + ".m3u", "r+")
        filedata = file.readlines()
        file.close()
        index = 1
        self.sub_stations.clear()
        while index < len(filedata):
            url = filedata[index + 2]
            name = url.split("/")[-1]
            name = name.replace("\n", "")
            name = name.replace("_", " ")
            self.sub_stations.append(name)
            index += 5
        self.station_index = 0

