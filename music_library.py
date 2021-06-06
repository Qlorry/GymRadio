import os
import sys
import player


def get_song_library():
    res = []
    for root, subdirs, files in os.walk('music'):
        for filename in files:
            file_path = os.path.join(root, filename)
            name, extension = os.path.splitext(filename)
            if extension != '.m4a':
                continue
            album = os.path.basename(os.path.dirname(file_path))
            res.append(player.Song(name, album))
    return res