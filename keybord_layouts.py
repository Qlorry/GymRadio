import json

from telebot import types
from music_library import get_radio_library


def get_admin_ui():
    markup = types.ReplyKeyboardMarkup()

    btn_library = types.KeyboardButton('/radio')
    btn_orders = types.KeyboardButton('/orders')
    btn_play = types.KeyboardButton('/p_p ⏯')
    btn_next = types.KeyboardButton('/n ⏭')
    btn_prev = types.KeyboardButton('/p ⏮')
    btn_sound_up = types.KeyboardButton('/upnext')
    btn_stop = types.KeyboardButton('/s ⏹')
    btn_sound_down = types.KeyboardButton('/history')

    markup.row(btn_library, btn_orders)
    markup.row(btn_prev, btn_play, btn_next)
    markup.row(btn_sound_down, btn_stop, btn_sound_up)
    return markup


def get_user_ui():
    markup = types.ReplyKeyboardMarkup()
    btn_sound_up = types.KeyboardButton('Whats playing now?')
    btn_sound_down = types.KeyboardButton('Help')
    markup.row(btn_sound_down, btn_sound_up)
    return markup


def get_radio_list_keyboard():
    lib = get_radio_library()
    markup = types.InlineKeyboardMarkup()
    for station in lib:
        data = json.dumps({"name": station.name,
                           "cmd": "choose_radio"})
        btn = types.InlineKeyboardButton(text=station.name, callback_data=data)
        markup.add(btn)
    return markup


def get_upnext_list_keyboard(songs, last_index):
    markup = types.InlineKeyboardMarkup()
    i = len(songs) - 1
    for song in songs:
        data = json.dumps({"index": last_index - i,
                           "name": song.name[0:20],
                           "cmd": "set_song"})
        i -= 1
        btn = types.InlineKeyboardButton(text=song.name[0:20], callback_data=data)
        markup.add(btn)
    data = json.dumps({"lastIndex": last_index,
                       "cmd": "more_upnext"})
    btn = types.InlineKeyboardButton(text="More", callback_data=data)
    markup.add(btn)
    return markup


def get_history_list_keyboard(songs, first_index):
    markup = types.InlineKeyboardMarkup()
    i = len(songs) - 1
    for song in reversed(songs):
        data = json.dumps({"index": first_index + i,
                           "name": song.name[0:20],
                           "cmd": "set_song"})
        i -= 1
        btn = types.InlineKeyboardButton(text=song.name[0:20], callback_data=data)
        markup.add(btn)
    data = json.dumps({"firstIndex": first_index,
                       "cmd": "more_history"})
    btn = types.InlineKeyboardButton(text="More", callback_data=data)
    markup.add(btn)
    return markup
