import vlc
import time
import os


class VLC:
    def __init__(self):
        self.Player = vlc.Instance()

    def addPlaylist(self):
        self.mediaList = self.Player.media_list_new()
        self.mediaList.add_media(self.Player.media_new("music/Radio/RadioROKS.m3u"))
        self.listPlayer = self.Player.media_list_player_new()
        self.listPlayer.set_media_list(self.mediaList)

    def play(self):
        self.listPlayer.play()

    def next(self):
        self.listPlayer.next()

    def pause(self):
        self.listPlayer.pause()

    def previous(self):
        self.listPlayer.previous()

    def stop(self):
        self.listPlayer.pause()


player = VLC()
player.addPlaylist()
player.play()
time.sleep(9)
