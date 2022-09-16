from Config.config import conf
import Lang.UA_lang as ua

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

already_selected_msg = "Already Selected"
orders_msg = "Orders"

def found_n_songs(n):
    if conf.lang == "UA":
        return ua.found_n_songs(n)
    else:
        return "Added " + str(n) + " songs in queue"


def song_name_added(name):
    if conf.lang == "UA":
        return ua.song_name_added(name)
    else:
        return "Song \"" + name + "\" added in queue"


def setting_song(name):
    if conf.lang == "UA":
        return ua.setting_song(name)
    else:
        return "Setting \"" + name + "\""


if conf.lang == "UA":
    instruction = ua.instruction
    song_not_found = ua.song_not_found
    found_this = ua.found_this
    admin_instruction = ua.admin_instruction
    stop_msg = ua.stop_msg
    pause_msg = ua.pause_msg
    play_msg = ua.play_msg
    radio_stations_msg = ua.radio_stations_msg
    url_ok = ua.url_ok
    url_bad = ua.url_bad
    url_cant_load = ua.url_cant_load
    starting_url_load = ua.starting_url_load
    already_selected_msg = ua.already_selected_msg
    orders_msg = ua.orders_msg
