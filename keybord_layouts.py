import yaml

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
        data = yaml.dump({"n": station.name,
                          "c": "choose_radio"},
                         Dumper=yaml.Dumper)
        btn = types.InlineKeyboardButton(text=station.name, callback_data=data)
        markup.add(btn)
    return markup


def get_upnext_list_keyboard(songs, last_index):
    markup = types.InlineKeyboardMarkup()
    i = len(songs) - 1
    for song in songs:
        # data = json.dumps({"i": last_index - i,
        #                    "n": song.name[0:20],
        #                    "c": "set"})
        data = yaml.dump({"i": last_index - i,
                          "c": "set"},
                         Dumper=yaml.Dumper)
        i -= 1
        btn = types.InlineKeyboardButton(text=song.name[0:93], callback_data=data)
        markup.add(btn)
    data = yaml.dump({"lastIndex": last_index,
                      "c": "more_upnext"},
                     Dumper=yaml.Dumper)
    btn = types.InlineKeyboardButton(text="More", callback_data=data)
    markup.add(btn)
    return markup


def get_history_list_keyboard(songs, first_index):
    markup = types.InlineKeyboardMarkup()
    i = len(songs) - 1
    for song in reversed(songs):
        # data = json.dumps({"i": first_index + i,
        #                    "n": song.name[0:20],
        #                    "c": "set"})
        data = yaml.dump({"i": first_index + i,
                          "c": "set"},
                         Dumper=yaml.Dumper)
        btn = types.InlineKeyboardButton(text=song.name[0:93], callback_data=data)
        i -= 1
        markup.add(btn)
    data = yaml.dump({"firstIndex": first_index,
                      "c": "more_history"},
                     Dumper=yaml.Dumper)
    btn = types.InlineKeyboardButton(text="More", callback_data=data)
    markup.add(btn)
    return markup
