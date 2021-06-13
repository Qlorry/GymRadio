# importing vlc module
import vlc

# importing time module
import time


def next_song_callback(event):
    print("listPlayerCallback:", event.type, event.u)


# creating a media player object
media_player = vlc.MediaListPlayer()

list_player_events = media_player.event_manager()
list_player_events.event_attach(vlc.EventType.MediaListPlayerNextItemSet, next_song_callback)

# creating Instance class object
player = vlc.Instance()

# creating a media list object
media_list = vlc.MediaList()

# creating a new media
media = player.media_new("music/NA/LITTLE BIG - EVERYBODY (Little Big Are Back) (Official Music Video).m4a")

# setting media object to the media list
media_list.lock()
media_list.add_media(media)
media_list.unlock()
media_list.set_media(media)


# setting media list to the media player
media_player.set_media_list(media_list)

# start playing video
media_player.play()

# wait so the video can be played for 5 seconds
# irrespective for length of video
time.sleep(5)

# getting media object from the media list
value = media_list.media().get_mrl()

# printing val
print(value)
