import telebot
from telebot import types
from music_library import get_radio_library


def get_admin_ui():
    markup = types.ReplyKeyboardMarkup()

    btn_library = types.KeyboardButton('/radio')
    btn_orders = types.KeyboardButton('/orders')
    btn_play = types.KeyboardButton('/p_p ⏯')
    btn_next = types.KeyboardButton('/n ⏭')
    btn_prev = types.KeyboardButton('/p ⏮')
    btn_sound_up = types.KeyboardButton('Whats playing now?')
    btn_stop = types.KeyboardButton('/s ⏹')
    btn_sound_down = types.KeyboardButton('/help')

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
        btn = types.InlineKeyboardButton(text=station.name, callback_data=station.name)
        markup.add(btn)
    return markup
