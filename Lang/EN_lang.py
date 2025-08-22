from Lang.lang_keys import LangKeys


TRANSLATION = {
    LangKeys.instruction : "",
    LangKeys.song_not_found : "Ooops, cant find song from this link",
    LangKeys.found_this : "Found this in youtube ",
    LangKeys.admin_instruction : "Choose what to do",
    LangKeys.stop_msg : "Stopping",
    LangKeys.pause_msg : "Pause",
    LangKeys.play_msg : "Lets Rock!",
    LangKeys.radio_stations_msg : "Radio stations:",
    LangKeys.url_ok : "Processing url",
    LangKeys.url_bad : "Invalid url",
    LangKeys.url_cant_load : "Cant load this link",
    LangKeys.starting_url_load : "Staring url loading",
    LangKeys.already_selected_msg : "Already Selected",
    LangKeys.orders_msg : "Orders",
    LangKeys.found_n_songs: "Added {0} songs to queue",
    LangKeys.song_name_added: "Song \"{0}\" added to queue",
    LangKeys.setting_song: "Setting \"{0}\"",
}



def found_n_songs(n):
    return "Added " + str(n) + " songs in queue"


def song_name_added(name):
    return "Song \"" + name + "\" added in queue"


def setting_song(name):
    return "Setting \"" + name + "\""