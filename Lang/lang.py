from Config.config import conf
import Lang.RU_lang as ru

instruction = ""
song_not_found = "Ooops, cant find song from this link"
found_this = "Found this in youtube "
admin_instruction = "Choose what to do"

stop_msg = "Stopping"
pause_msg = "Pause"
play_msg = "Lets Rock!"

radio_stations_msg = "Radio stations:"

url_ok = "Processing url"
url_bad = "Invalid url"
url_cant_load = "Cant load this link"
starting_url_load = "Staring url loading"


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


def setting_song(name):
    if conf.lang == "RU":
        return ru.setting_song(name)
    else:
        return "Setting \"" + name + "\""


if conf.lang == "RU":
    instruction = ru.instruction
    song_not_found = ru.song_not_found
    found_this = ru.found_this
    admin_instruction = ru.admin_instruction
    stop_msg = ru.stop_msg
    pause_msg = ru.pause_msg
    play_msg = ru.play_msg
    radio_stations_msg = ru.radio_stations_msg
    url_ok = ru.url_ok
    url_bad = ru.url_bad
    url_cant_load = ru.url_cant_load
    starting_url_load = ru.starting_url_load
