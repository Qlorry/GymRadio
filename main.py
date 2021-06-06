import telebot
from telebot import types
import validators

import util
from downloader import Downloader
from player import MyPlayer
from player import Song
from keybord_layouts import *
from convertor import convert
from config import Config
from util import *

conf = Config()
tb = telebot.TeleBot(conf.token)
downloader = Downloader()
player = MyPlayer()
player.switch_to_library()
player.next(False)


def start_download_procedure(message):
    if util.is_youtube_link(message.text):
        return downloader.load(message.text)
    new_link = convert(message.text)
    if new_link == "":
        tb.send_message(message.from_user.id, "Ooops, cant find song from this link")
        return []
    tb.send_message(message.from_user.id, "Found this in youtube " + new_link)
    try:
        res = downloader.load(new_link)
    except Exception as e:
        print("Error while downloading " + str(e))
        return []
    return res


def add_procedure(message, res_dict):
    if '_type' in res_dict:
        cnt = 0
        msg_str = "Adding playlist: \n \n"
        for item in res_dict.get('entries'):
            cnt += 1
            msg_str += "#" + str(cnt) + " " + item.get('title') + "\n"
        tb.send_message(message.from_user.id, msg_str)
        for item in res_dict.get('entries'):
            player.add_song(Song(item.get('title'), res_dict.get('title')))
        tb.send_message(message.from_user.id, "Added " + str(cnt) + " songs in queue")
    else:
        player.add_song(Song(res_dict.get('title')))
        tb.send_message(message.from_user.id, "Song \"" + res_dict.get('title') + "\" added in queue")


@tb.message_handler(commands=['start', 'help'])
def handle_start_help(message):
    # or add KeyboardButton one row at a time:
    markup = get_admin_ui()
    tb.send_message(message.from_user.id, "Choose what to do", reply_markup=markup)


@tb.message_handler(content_types=['text'])
def handle_input(message):
    if message.text == 'Switch to Library':
        player.switch_to_library()
        tb.send_message(message.from_user.id, "Library")
        return
    if message.text == 'Switch to Orders':
        player.switch_to_orders()
        tb.send_message(message.from_user.id, "Orders")
        return
    if (message.text == '⏯') | (message.text == '▶️') | (message.text == '⏹'):
        if player.is_now_playing:
            tb.send_message(message.from_user.id, "Stopping", reply_markup=get_admin_ui_play())
            player.stop()
        else:
            tb.send_message(message.from_user.id, "Lets Rock!", reply_markup=get_admin_ui_stop())
            player.play()
        return
    if message.text == '⏭':
        tb.send_message(message.from_user.id, "Setting \"" + player.get_next_song_name() + "\"")
        player.next()
        return
    if message.text == '⏮':
        prev_song = player.get_prev_song_name()
        if prev_song == "":
            tb.send_message(message.from_user.id, "No more songs")
            return
        tb.send_message(message.from_user.id, "Setting \"" + prev_song +"\"")
        player.prev()
        return
    if message.text == 'Whats playing now?':
        tb.send_message(message.from_user.id, player.current_song.name)
        return
    if message.text == 'Help':
        tb.send_message(message.from_user.id, "Just send me link")
        return
    else:  # https://youtu.be/JD8ZO5P9yzQ
        valid = validators.url(message.text)
        if valid:
            tb.send_message(message.from_user.id, "Url is valid")
            print("Url is valid")
            res_dict = start_download_procedure(message)
            if len(res_dict) == 0:
                tb.send_message(message.from_user.id, "Cant load this link")
                return
            tb.send_message(message.from_user.id, "Link loaded")
            add_procedure(message, res_dict)
        else:
            tb.send_message(message.from_user.id, "Invalid url")

tb.polling(none_stop=True, interval=0)
