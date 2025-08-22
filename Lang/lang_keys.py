import enum

@enum.unique
class LangKeys(enum.Enum):
    instruction = enum.auto()
    song_not_found = enum.auto()
    found_this = enum.auto()
    admin_instruction= enum.auto()
    stop_msg= enum.auto()
    pause_msg= enum.auto()
    play_msg = enum.auto()
    radio_stations_msg = enum.auto()
    url_ok = enum.auto()
    url_bad = enum.auto()
    url_cant_load =enum.auto()
    starting_url_load = enum.auto()
    already_selected_msg = enum.auto()
    orders_msg = enum.auto()
    found_n_songs = enum.auto()
    song_name_added = enum.auto()
    setting_song = enum.auto()
