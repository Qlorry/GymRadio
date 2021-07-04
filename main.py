import datetime
import validators
import logging


import util
from downloader import Downloader
from Player.SuperPlayer import SuperPlayer
from Player.Song import Song
from keybord_layouts import *
from convertor import convert
from util import *
from Lang.lang import *

date_on_start = datetime.datetime.now()
log_filename = "Logs/"+date_on_start.strftime("%y-%m-%d %H-%M") + ".log"
logging.basicConfig(filename=log_filename, level=logging.INFO)
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
            loaded_song = downloader.load(item['webpage_url'])
            if loaded_song is None:
                cnt += 1
                msg_str += "#" + str(cnt) + " " + item.get('title') + " -- Failed\n"
                fails += 1
                continue
            player.add_song(Song(loaded_song.get('title'), loaded_song.get('album')))
            cnt += 1
            msg_str += "#" + str(cnt) + " " + loaded_song.get('title') + "\n"
            # list_msg = tb.send_message(message.chat.id, msg_str)
            tb.edit_message_text(chat_id=message.chat.id, message_id=list_msg.message_id, text=msg_str)
        msg_str += "\nДобавил " + str(cnt - fails) + " песен"
        tb.edit_message_text(chat_id=message.chat.id, message_id=list_msg.message_id, text=msg_str)
    else:
        logging.info("Adding single song " + res_dict.get('title'))
        loaded_song = downloader.load(res_dict['webpage_url'])
        player.add_song(Song(loaded_song.get('title'), loaded_song.get('album')))
        tb.send_message(message.chat.id, song_name_added(loaded_song.get('title')))


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
        logging.info("pause")
        tb.send_message(message.chat.id, pause_msg)
        player.pause()
    else:
        logging.info("play")
        tb.send_message(message.chat.id, play_msg)
        player.play()


@tb.message_handler(commands=['n'])
def handle_next(message):
    if is_not_admins_chat(message.chat.id, conf):
        return
    song_name = player.next()
    if song_name is None:
        tb.send_message(message.chat.id, "Something went wrong")
        return
    logging.info("next")
    tb.send_message(message.chat.id, setting_song(song_name))


@tb.message_handler(commands=['p'])
def handle_prev(message):
    if is_not_admins_chat(message.chat.id, conf):
        return
    res = player.prev()
    if res is None:
        tb.send_message(message.chat.id, "Something went wrong")
        return
    logging.info("prev")
    tb.send_message(message.chat.id, setting_song(res))


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
    tb.send_message(message.chat.id, "Orders")


@tb.message_handler(commands=['upnext'])
def handle_orders(message):
    if is_not_admins_chat(message.chat.id, conf):
        return
    logging.info("upnext")
    songs = player.get_next_songs(5)
    if len(songs["list"]) == 0:
        logging.warning("No More songs for upnext")
        tb.send_message(message.chat.id, "No more songs in queue")
        return
    tb.send_message(message.chat.id, "Next songs:\n", reply_markup=get_upnext_list_keyboard(songs["list"],
                                                                                            songs["lastIndex"]))


@tb.message_handler(commands=['history'])
def handle_orders(message):
    if is_not_admins_chat(message.chat.id, conf):
        return
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
            msg += "-> # " + str(cnt) + s.name + "\n"
        else:
            msg += "# " + str(cnt) + s.name + "\n"
        cnt += 1
    tb.send_message(message.chat.id, msg)


@tb.message_handler(commands=['now'])
def handle_orders(message):
    logging.info("Want's now")
    tb.send_message(chat_id=message.chat.id, text=player.whats_playing())


@tb.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    # Если сообщение из чата с ботом
    if call.message:
        data = json.loads(call.data)
        if data["cmd"] == "choose_radio":
            player.stop()
            name = player.load_station(data["name"])
            player.switch_to_radio()
            player.play()
            tb.edit_message_text(chat_id=call.message.chat.id,
                                 message_id=call.message.message_id,
                                 text="Setting " + name)
        if data["cmd"] == "set_song":
            logging.info("Want to play song " + data["name"] + " at " + str(data["index"]))
            player.stop()
            player.go_to(data["index"])
            player.play()
            tb.edit_message_text(chat_id=call.message.chat.id,
                                 message_id=call.message.message_id,
                                 text="Setting " + data["name"])
        if data["cmd"] == "more_upnext":
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
        if data["cmd"] == "more_history":
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
        tb.send_message(message.chat.id, url_loaded)
        add_procedure(message, res_dict)
    else:
        logging.info("Invalid Link")
        tb.send_message(message.chat.id, url_bad)


tb.polling(none_stop=True, interval=0)
