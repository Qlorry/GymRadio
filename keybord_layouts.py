import telebot
from telebot import types


def get_admin_ui():
    markup = types.ReplyKeyboardMarkup()
    btn_library = types.KeyboardButton('Switch to Radio')
    btn_orders = types.KeyboardButton('Switch to Orders')
    btn_play = types.KeyboardButton('⏯')
    btn_next = types.KeyboardButton('⏭')
    btn_prev = types.KeyboardButton('⏮')
    btn_sound_up = types.KeyboardButton('Whats playing now?')
    btn_sound_down = types.KeyboardButton('Help')
    markup.row(btn_library, btn_orders)
    markup.row(btn_prev, btn_play, btn_next)
    markup.row(btn_sound_down, btn_sound_up)
    return markup


def get_user_ui():
    markup = types.ReplyKeyboardMarkup()
    btn_library = types.KeyboardButton('Switch to Radio')
    btn_orders = types.KeyboardButton('Switch to Orders')
    btn_sound_up = types.KeyboardButton('Whats playing now?')
    btn_sound_down = types.KeyboardButton('Help')
    markup.row(btn_library, btn_orders)
    markup.row(btn_sound_down, btn_sound_up)
    return markup


def get_admin_ui_play():
    markup = types.ReplyKeyboardMarkup()
    btn_library = types.KeyboardButton('Switch to Radio')
    btn_orders = types.KeyboardButton('Switch to Orders')
    btn_play = types.KeyboardButton('▶️')
    btn_next = types.KeyboardButton('⏭')
    btn_prev = types.KeyboardButton('⏮')
    btn_sound_up = types.KeyboardButton('Whats playing now?')
    btn_sound_down = types.KeyboardButton('Help')
    markup.row(btn_library, btn_orders)
    markup.row(btn_prev, btn_play, btn_next)
    markup.row(btn_sound_down, btn_sound_up)
    return markup


def get_admin_ui_stop():
    markup = types.ReplyKeyboardMarkup()
    btn_library = types.KeyboardButton('Switch to Radio')
    btn_orders = types.KeyboardButton('Switch to Orders')
    btn_play = types.KeyboardButton('⏹')
    btn_next = types.KeyboardButton('⏭')
    btn_prev = types.KeyboardButton('⏮')
    btn_sound_up = types.KeyboardButton('Whats playing now?')
    btn_sound_down = types.KeyboardButton('Help')
    markup.row(btn_library, btn_orders)
    markup.row(btn_prev, btn_play, btn_next)
    markup.row(btn_sound_down, btn_sound_up)
    return markup
