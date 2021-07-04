import os
import sys
from Player.Song import Song


def get_radio_library():
    res = []
    for root, subdirs, files in os.walk('Radio'):
        for filename in files:
            file_path = os.path.join(root, filename)
            name, extension = os.path.splitext(filename)
            if extension != '.m3u':
                continue
            res.append(Song(name, "Radio"))
    return res