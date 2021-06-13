from config import conf
import Lang.RU_lang as ru

instruction = ""
song_not_found = "Ooops, cant find song from this link"
found_this = "Found this in youtube "
admin_instruction = "Choose what to do"

stop_msg = "Stopping"
pause_msg = "Pause"
play_msg = "Lets Rock!"
next_msg = "Setting next"
prev_msg = "Setting previous"

radio_stations_msg = "Radio stations:"

url_ok = "Url is valid"
url_bad = "Invalid url"
url_cant_load = "Cant load this link"
url_loaded = "Link loaded"


def found_n_songs(n):
    if conf.lang == "RU":
        return ru.found_n_songs(n)
    else:
        return "Added " + str(n) + " songs in queue"


def song_name_added(name):
    if conf.lang == "RU":
        return ru.song_name_added(name)
    else:
        return "Song \"" + name + "\" added in queue"


if conf.lang == "RU":
    instruction = ru.instruction
    song_not_found = ru.song_not_found
    found_this = ru.found_this
    admin_instruction = ru.admin_instruction
    stop_msg = ru.stop_msg
    pause_msg = ru.pause_msg
    play_msg = ru.play_msg
    next_msg = ru.next_msg
    prev_msg = ru.prev_msg
    radio_stations_msg = ru.radio_stations_msg
    url_ok = ru.url_ok
    url_bad = ru.url_bad
    url_cant_load = ru.url_cant_load
    url_loaded = ru.url_loaded