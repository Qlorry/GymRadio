import datetime
import threading

import validators
import logging
import telebot

from telebot.custom_filters import TextMatchFilter

from Player.OrderListPlayer import ChangeSongRes
from DataDownloader.downloader import Downloader
from Player.SuperPlayer import SuperPlayer
from Player.Song import Song
from Config.keybord_layouts import *
from DataDownloader.convertor import convert
from Config.config import conf
from util import *
from Lang.lang import *

tb = telebot.TeleBot(conf.token)
downloader = Downloader()
player = None


class OnlyAdmins(telebot.AdvancedCustomFilter):
    key = 'only_admin_chat'

    def check(self, message, text):
        if not text:
            return True
        return str(message.chat.id) == conf.admins_chat

class TextMatch(telebot.AdvancedCustomFilter):
    """
    Filter to check Text message.

    .. code-block:: python3
        :caption: Example on using this filter:

        @bot.message_handler(text=['account'])
        # your function
    """

    key = 'text'

    def check(self, message, text):
        """
        :meta private:
        """
        if isinstance(text, list):
            return message.text in text
        else:
            return text == message.text
        
tb.add_custom_filter(OnlyAdmins())
tb.add_custom_filter(TextMatch())

def start():
    tb.polling(none_stop=True, interval=0)


def start_bot(player_ref):
    global player
    player = player_ref
    th = threading.Thread(target=start)
    th.start()


def start_download_procedure(message):
    if is_youtube_link(message.text):
        logging.info("Loading YT link")
        return downloader.load_info(message.text)
    new_links = convert(message.text)
    if len(new_links) == 0:
        tb.send_message(message.chat.id, song_not_found)
        return []
    for link in new_links:
        result = downloader.load_info(link)
        if len(result) != 0:
            tb.send_message(message.chat.id, found_this + link)
            return result
    return []


def add_list(message, res_dict):
    logging.info("Adding playlist")
    cnt = 0
    fails = 0
    msg_str = "Adding playlist: \n \n"

    list_msg = tb.send_message(message.chat.id, msg_str)

    for item in res_dict.get('entries'):
        name = item.get('title') if item.get('title') is not None else ""
        album = item.get('album') if item.get('album') is not None else "NA"
        if is_song_in_os(album, name):
            loaded_song = item
        else:
            loaded_song = downloader.load(item['webpage_url'])
        if loaded_song is None:
            cnt += 1
            msg_str += "#" + str(cnt) + " " + item.get('title') + " -- Failed\n"
            fails += 1
            continue
        player.add_song(Song(loaded_song.get('title'), loaded_song.get('album')))
        cnt += 1
        msg_str += "#" + str(cnt) + " " + loaded_song.get('title') + "\n"
        tb.edit_message_text(chat_id=message.chat.id, message_id=list_msg.message_id, text=msg_str)

    msg_str += found_n_songs(cnt - fails)
    tb.edit_message_text(chat_id=message.chat.id, message_id=list_msg.message_id, text=msg_str)


def add_single(message, res_dict):
    logging.info("Adding single song " + res_dict.get('title'))

    name = res_dict.get('title') if res_dict.get('title') is not None else ""
    album = res_dict.get('album') if res_dict.get('album') is not None else "NA"
    if is_song_in_os(album, name):
        loaded_song = res_dict
    else:
        loaded_song = downloader.load(res_dict['webpage_url'])
    if loaded_song is None:
        tb.send_message(message.chat.id, res_dict.get('title') + " -- Failed\n")
        return
    player.add_song(Song(loaded_song.get('title'), loaded_song.get('album')))
    tb.send_message(message.chat.id, song_name_added(loaded_song.get('title')))


def add_procedure(message, res_dict):
    if '_type' in res_dict:
        add_list(message, res_dict)
    else:
        add_single(message, res_dict)


@tb.message_handler(commands=['start', 'help'], only_admin_chat=True)
def handle_start_help(message):
    print("Start from admins ", message.chat.id)
    logging.info("admin start/help")
    markup = get_admin_ui()
    tb.send_message(message.chat.id, admin_instruction, reply_markup=markup)


@tb.message_handler(commands=['start', 'help'], only_admin_chat=False)
def handle_start_help(message):
    print("Start from user ", message.chat.id)
    logging.info("user start/help")
    tb.send_message(message.chat.id, instruction)

@tb.message_handler(text=['⏯', '⏯️'], only_admin_chat=True)
def handle_p_p(message):
    if player.is_now_playing():
        logging.info("pause")
        tb.send_message(message.chat.id, pause_msg)
        player.pause()
    else:
        logging.info("play")
        tb.send_message(message.chat.id, play_msg)
        player.play()


@tb.message_handler(text=['⏭'], only_admin_chat=True)
def handle_next(message):
    logging.info("next")
    song_name = player.next()
    if song_name is None:
        tb.send_message(message.chat.id, "Something went wrong")
        return
    elif song_name is ChangeSongRes.empty_list:
        tb.send_message(message.chat.id, "List of songs is empty")
        return
    elif song_name is ChangeSongRes.end:
        tb.send_message(message.chat.id, "End of Song list")
        return

    name = ""
    if player.is_from_radio:
        name = song_name
    else:
        name = song_name.name
    tb.send_message(message.chat.id, setting_song(name))


@tb.message_handler(text=['⏮'], only_admin_chat=True)
def handle_prev(message):
    res = player.prev()
    if res is None:
        tb.send_message(message.chat.id, "Something went wrong")
        return
    logging.info("prev")
    tb.send_message(message.chat.id, setting_song(res))


@tb.message_handler(text=['⏹'], only_admin_chat=True)
def handle_stop(message):
    player.stop()
    logging.info("stop")
    tb.send_message(message.chat.id, stop_msg)


@tb.message_handler(commands=['radio'], only_admin_chat=True)
def handle_radio(message):
    logging.info("radio")
    tb.send_message(message.chat.id, radio_stations_msg, reply_markup=get_radio_list_keyboard())


@tb.message_handler(commands=['orders'], only_admin_chat=True)
def handle_orders(message):
    if not player.is_from_radio:
        tb.send_message(message.chat.id, already_selected_msg)
        return
    logging.info("orders")
    player.switch_to_orders()
    tb.send_message(message.chat.id, orders_msg)


@tb.message_handler(commands=['upnext'], only_admin_chat=True)
def handle_orders(message):
    logging.info("upnext")
    songs = player.get_next_songs(5)
    if len(songs["list"]) == 0:
        logging.warning("No More songs for upnext")
        tb.send_message(message.chat.id, "No more songs in queue")
        return
    tb.send_message(message.chat.id, "Next songs:\n", reply_markup=get_upnext_list_keyboard(songs["list"],
                                                                                            songs["lastIndex"]))


@tb.message_handler(commands=['history'], only_admin_chat=True)
def handle_orders(message):
    logging.info("history")
    songs = player.get_prev_songs(5)
    if len(songs["list"]) == 0:
        logging.warning("No More songs for history")
        tb.send_message(message.chat.id, "No more songs in history")
        return
    tb.send_message(message.chat.id,
                    "Previous songs:\n",
                    reply_markup=get_history_list_keyboard(songs["list"], songs["firstIndex"]))


@tb.message_handler(commands=['list'])
def handle_orders(message):
    logging.info("list")
    songs = player.get_all_songs()
    if len(songs) == 0:
        logging.warning("No songs in media player")
        tb.send_message(message.chat.id, "List is empty")
        return
    current = player.get_current_index()
    msg = ""
    cnt = 1
    for s in songs:
        if cnt - 1 == current:
            msg += "-> " + str(cnt) + " " + s.name + "\n"
        else:
            msg += "# " + str(cnt) + " " + s.name + "\n"
        cnt += 1
    tb.send_message(message.chat.id, msg)


@tb.message_handler(commands=['now'])
def handle_orders(message):
    logging.info("Want's now")
    tb.send_message(chat_id=message.chat.id, text=player.whats_playing())


@tb.message_handler(commands=['swap'], only_admin_chat=True)
def handle_orders(message):
    logging.info("swap")
    command = message.text.split()
    try:
        player.swap(int(command[1]), int(command[2]))
    except():
        return


@tb.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    # Если сообщение из чата с ботом
    if call.message:
        data = yaml.load(call.data, Loader=yaml.Loader)
        if data["c"] == "choose_radio":
            player.stop()
            name = player.load_station(data["n"])
            player.switch_to_radio()
            player.play()
            tb.edit_message_text(chat_id=call.message.chat.id,
                                 message_id=call.message.message_id,
                                 text="Setting " + name)
        if data["c"] == "set":
            logging.info("Want to play song " + " at " + str(data["i"]))
            player.stop()
            player.go_to(data["i"])
            player.play()
            tb.edit_message_text(chat_id=call.message.chat.id,
                                 message_id=call.message.message_id,
                                 text="Setting " + player.whats_playing())
        if data["c"] == "more_upnext":
            last_index = data["lastIndex"] + 5  # 1 + 5 not to get last song in that list
            songs = player.get_n_songs(data["lastIndex"] + 1, last_index)
            logging.info("Want to see more songs")
            if len(songs) == 0:
                tb.edit_message_text(chat_id=call.message.chat.id,
                                     message_id=call.message.message_id,
                                     text="No more songs")
                return
            last_index = data["lastIndex"] + len(songs)
            tb.edit_message_text(chat_id=call.message.chat.id,
                                 message_id=call.message.message_id,
                                 reply_markup=get_upnext_list_keyboard(songs, last_index),
                                 text="Next songs:\n")
        if data["c"] == "more_history":
            first_index = data["firstIndex"] - 5
            songs = player.get_n_songs(first_index, data["firstIndex"] - 1)
            if first_index < 0:
                first_index = 0
            logging.info("Want to see more songs")
            if len(songs) == 0:
                tb.edit_message_text(chat_id=call.message.chat.id,
                                     message_id=call.message.message_id,
                                     text="No more songs")
                return
            tb.edit_message_text(chat_id=call.message.chat.id,
                                 message_id=call.message.message_id,
                                 reply_markup=get_history_list_keyboard(songs, first_index),
                                 text="Previous songs:\n")


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
        tb.send_message(message.chat.id, starting_url_load)
        add_procedure(message, res_dict)
    else:
        logging.info("Invalid Link")
        tb.send_message(message.chat.id, url_bad)
