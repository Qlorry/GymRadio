import datetime

import telebot
from telebot import types
import validators
import logging

import util
from downloader import Downloader
from player import SuperPlayer
from player import Song
from keybord_layouts import *
from convertor import convert
from config import conf
from util import *
from Lang.lang import *

date_on_start = datetime.datetime.now()
logfilename = "Logs/"+date_on_start.strftime("%y-%m-%d %H-%M") + ".log"
logging.basicConfig(filename=logfilename, level=logging.INFO)
rm_old_logs()
tb = telebot.TeleBot(conf.token)
downloader = Downloader()
player = SuperPlayer()
player.play()


def start_download_procedure(message):
    if util.is_youtube_link(message.text):
        logging.info("Loading YT link")
        return downloader.load_info(message.text)
    new_link = convert(message.text)
    if new_link == "":
        tb.send_message(message.chat.id, song_not_found)
        return []
    tb.send_message(message.chat.id, found_this + new_link)
    return downloader.load_info(new_link)


def add_procedure(message, res_dict):
    if '_type' in res_dict:
        logging.info("Adding playlist")
        cnt = 0
        fails = 0
        msg_str = "Adding playlist: \n \n"
        list_msg = tb.send_message(message.chat.id, msg_str)
        for item in res_dict.get('entries'):
            if downloader.load(item['webpage_url']) is None:
                cnt += 1
                msg_str += "#" + str(cnt) + " " + item.get('title') + " -- Failed\n"
                fails += 1
                continue
            player.add_song(Song(item.get('title'), item.get('album')))
            cnt += 1
            msg_str += "#" + str(cnt) + " " + item.get('title') + "\n"
            # list_msg = tb.send_message(message.chat.id, msg_str)
            tb.edit_message_text(chat_id=message.chat.id, message_id=list_msg.message_id, text=msg_str)
        msg_str += "\nДобавил " + str(cnt - fails) + " песен"
        tb.edit_message_text(chat_id=message.chat.id, message_id=list_msg.message_id, text=msg_str)
    else:
        logging.info("Adding single song " + res_dict.get('title'))
        downloader.load(res_dict['webpage_url'])
        player.add_song(Song(res_dict.get('title'), res_dict.get('album')))
        tb.send_message(message.chat.id, song_name_added(res_dict.get('title')))


@tb.message_handler(commands=['start', 'help'])
def handle_start_help(message):
    print("Start from ", message.chat.id)
    logging.info("start/help")
    if is_not_admins_chat(message.chat.id, conf):
        tb.send_message(message.chat.id, instruction)
        return
    markup = get_admin_ui()
    tb.send_message(message.chat.id, admin_instruction, reply_markup=markup)


@tb.message_handler(commands=['p_p'])
def handle_p_p(message):
    if is_not_admins_chat(message.chat.id, conf):
        return

    if player.is_now_playing():
        tb.send_message(message.chat.id, pause_msg)
        player.pause()
        logging.info("pause")
    else:
        logging.info("play")
        tb.send_message(message.chat.id, play_msg)
        player.play()


@tb.message_handler(commands=['n'])
def handle_next(message):
    if is_not_admins_chat(message.chat.id, conf):
        return
    if player.next() == "Radio":
        return
    logging.info("next")
    tb.send_message(message.chat.id, setting_song(player.whats_playing()))


@tb.message_handler(commands=['p'])
def handle_prev(message):
    if is_not_admins_chat(message.chat.id, conf):
        return
    if player.prev() == "Radio":
        return
    logging.info("prev")
    tb.send_message(message.chat.id, setting_song(player.whats_playing()))


@tb.message_handler(commands=['s'])
def handle_stop(message):
    if is_not_admins_chat(message.chat.id, conf):
        return
    player.stop()
    logging.info("stop")
    tb.send_message(message.chat.id, stop_msg)


@tb.message_handler(commands=['radio'])
def handle_radio(message):
    if is_not_admins_chat(message.chat.id, conf):
        return
    logging.info("radio")
    tb.send_message(message.chat.id, radio_stations_msg, reply_markup=get_radio_list_keyboard())


@tb.message_handler(commands=['orders'])
def handle_orders(message):
    if is_not_admins_chat(message.chat.id, conf):
        return
    if not player.is_from_radio:
        tb.send_message(message.chat.id, "Already playing")
        return
    logging.info("orders")
    player.switch_to_orders()
    player.next()
    tb.send_message(message.chat.id, "Orders")


@tb.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    # Если сообщение из чата с ботом
    if call.message:
        if player.is_from_radio:
            player.stop()
        player.load_station(call.data)
        player.switch_to_radio()
        player.play()
        tb.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="OK")


@tb.message_handler(content_types=['text'])
def handle_input(message):
    if message.text == "Whats playing now?":
        tb.send_message(message.chat.id, player.whats_playing())
        return
    valid = validators.url(message.text)
    if valid:
        tb.send_message(message.chat.id, url_ok)
        print("Url is valid")
        res_dict = start_download_procedure(message)
        if len(res_dict) == 0:
            logging.warning("No info for link!")
            tb.send_message(message.chat.id, url_cant_load)
            return
        tb.send_message(message.chat.id, url_loaded)
        add_procedure(message, res_dict)
    else:
        logging.info("Invalid Link")
        tb.send_message(message.chat.id, url_bad)


tb.polling(none_stop=True, interval=0)
