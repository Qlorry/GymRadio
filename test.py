# importing vlc module
import vlc

# importing time module
import time

# creating a media player object
media_player = vlc.MediaListPlayer()

# creating Instance class object
player = vlc.Instance()

# creating a media list object
media_list = vlc.MediaList()

# creating a new media
media = player.media_new("music/NA/Nyanpasu (Rynti M Remix).m4a")

# setting media object to the media list
media_list.set_media(media)

# setting media list to the media player
media_player.set_media_list(media_list)

# start playing video
media_player.play()

# wait so the video can be played for 5 seconds
# irrespective for length of video
time.sleep(5)

# getting media object from the media list
value = media_list.media()

# printing val
print(value)