import datetime
import threading

import validators
import logging
import telebot

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


def start():
    tb.polling(none_stop=True, interval=0)


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


class Bot:
    def __init__(self, player):
        self.player = player
        th = threading.Thread(target=start)
        th.start()

    def add_list(self, message, res_dict):
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
            self.player.add_song(Song(loaded_song.get('title'), loaded_song.get('album')))
            cnt += 1
            msg_str += "#" + str(cnt) + " " + loaded_song.get('title') + "\n"
            tb.edit_message_text(chat_id=message.chat.id, message_id=list_msg.message_id, text=msg_str)

        msg_str += found_n_songs(cnt - fails)
        tb.edit_message_text(chat_id=message.chat.id, message_id=list_msg.message_id, text=msg_str)

    def add_single(self, message, res_dict):
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
        self.player.add_song(Song(loaded_song.get('title'), loaded_song.get('album')))
        tb.send_message(message.chat.id, song_name_added(loaded_song.get('title')))

    def add_procedure(self, message, res_dict):
        if '_type' in res_dict:
            self.add_list(message, res_dict)
        else:
            self.add_single(message, res_dict)

    @tb.message_handler(commands=['start', 'help'])
    def handle_start_help(self, message):
        print("Start from ", message.chat.id)
        logging.info("start/help")
        if is_not_admins_chat(message.chat.id, conf):
            tb.send_message(message.chat.id, instruction)
            return
        markup = get_admin_ui()
        tb.send_message(message.chat.id, admin_instruction, reply_markup=markup)

    @tb.message_handler(commands=['p_p'])
    def handle_p_p(self, message):
        if is_not_admins_chat(message.chat.id, conf):
            return
        if self.player.is_now_playing():
            logging.info("pause")
            tb.send_message(message.chat.id, pause_msg)
            self.player.pause()
        else:
            logging.info("play")
            tb.send_message(message.chat.id, play_msg)
            self.player.play()

    @tb.message_handler(commands=['n'])
    def handle_next(self, message):
        if is_not_admins_chat(message.chat.id, conf):
            return
        logging.info("next")
        song_name = self.player.next()
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
        if self.player.is_from_radio:
            name = song_name
        else:
            name = song_name.name
        tb.send_message(message.chat.id, setting_song(name))

    @tb.message_handler(commands=['p'])
    def handle_prev(self, message):
        if is_not_admins_chat(message.chat.id, conf):
            return
        res = self.player.prev()
        if res is None:
            tb.send_message(message.chat.id, "Something went wrong")
            return
        logging.info("prev")
        tb.send_message(message.chat.id, setting_song(res))

    @tb.message_handler(commands=['s'])
    def handle_stop(self, message):
        if is_not_admins_chat(message.chat.id, conf):
            return
        self.player.stop()
        logging.info("stop")
        tb.send_message(message.chat.id, stop_msg)

    @tb.message_handler(commands=['radio'])
    def handle_radio(self, message):
        if is_not_admins_chat(message.chat.id, conf):
            return
        logging.info("radio")
        tb.send_message(message.chat.id, radio_stations_msg, reply_markup=get_radio_list_keyboard())

    @tb.message_handler(commands=['orders'])
    def handle_orders(self, message):
        if is_not_admins_chat(message.chat.id, conf):
            return
        if not self.player.is_from_radio:
            tb.send_message(message.chat.id, already_selected_msg)
            return
        logging.info("orders")
        self.player.switch_to_orders()
        tb.send_message(message.chat.id, orders_msg)

    @tb.message_handler(commands=['upnext'])
    def handle_orders(self, message):
        if is_not_admins_chat(message.chat.id, conf):
            return
        logging.info("upnext")
        songs = self.player.get_next_songs(5)
        if len(songs["list"]) == 0:
            logging.warning("No More songs for upnext")
            tb.send_message(message.chat.id, "No more songs in queue")
            return
        tb.send_message(message.chat.id, "Next songs:\n", reply_markup=get_upnext_list_keyboard(songs["list"],
                                                                                                songs["lastIndex"]))

    @tb.message_handler(commands=['history'])
    def handle_orders(self, message):
        if is_not_admins_chat(message.chat.id, conf):
            return
        logging.info("history")
        songs = self.player.get_prev_songs(5)
        if len(songs["list"]) == 0:
            logging.warning("No More songs for history")
            tb.send_message(message.chat.id, "No more songs in history")
            return
        tb.send_message(message.chat.id,
                        "Previous songs:\n",
                        reply_markup=get_history_list_keyboard(songs["list"], songs["firstIndex"]))

    @tb.message_handler(commands=['list'])
    def handle_orders(self, message):
        logging.info("list")
        songs = self.player.get_all_songs()
        if len(songs) == 0:
            logging.warning("No songs in media player")
            tb.send_message(message.chat.id, "List is empty")
            return
        current = self.player.get_current_index()
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
    def handle_orders(self, message):
        logging.info("Want's now")
        tb.send_message(chat_id=message.chat.id, text=self.player.whats_playing())

    @tb.message_handler(commands=['swap'])
    def handle_orders(self, message):
        if is_not_admins_chat(message.chat.id, conf):
            return
        logging.info("swap")
        command = message.text.split()
        try:
            self.player.swap(int(command[1]), int(command[2]))
        except():
            return

    @tb.callback_query_handler(func=lambda call: True)
    def callback_inline(self, call):
        # Если сообщение из чата с ботом
        if call.message:
            data = yaml.load(call.data, Loader=yaml.Loader)
            if data["c"] == "choose_radio":
                self.player.stop()
                name = self.player.load_station(data["n"])
                self.player.switch_to_radio()
                self.player.play()
                tb.edit_message_text(chat_id=call.message.chat.id,
                                     message_id=call.message.message_id,
                                     text="Setting " + name)
            if data["c"] == "set":
                logging.info("Want to play song " + " at " + str(data["i"]))
                self.player.stop()
                self.player.go_to(data["i"])
                self.player.play()
                tb.edit_message_text(chat_id=call.message.chat.id,
                                     message_id=call.message.message_id,
                                     text="Setting " + self.player.whats_playing())
            if data["c"] == "more_upnext":
                last_index = data["lastIndex"] + 5  # 1 + 5 not to get last song in that list
                songs = self.player.get_n_songs(data["lastIndex"] + 1, last_index)
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
                songs = self.player.get_n_songs(first_index, data["firstIndex"] - 1)
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
    def handle_input(self, message):
        if message.text == "Whats playing now?":
            tb.send_message(message.chat.id, self.player.whats_playing())
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
            self.add_procedure(message, res_dict)
        else:
            logging.info("Invalid Link")
            tb.send_message(message.chat.id, url_bad)
