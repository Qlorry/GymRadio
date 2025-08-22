import datetime
import threading

import validators
import logging
import telebot

from Lang.lang import Transl
from Lang.lang_keys import LangKeys
from Logic.logic import Logic
from Player.OrderListPlayer import ChangeSongRes
from Config.keybord_layouts import *
from Config.config import conf
import Util.bot_filters as bot_filters
from Util.ctx_factory import CtxFactory

# Bot setup
tb = telebot.TeleBot(conf.token)
tb.add_custom_filter(bot_filters.OnlyAdmins())
tb.add_custom_filter(bot_filters.TextMatch())

def run_polling():
    tb.polling(none_stop=True, interval=0)

ctx_factory = CtxFactory(lambda chat_id, text: tb.send_message(chat_id, text), 
                         lambda chat_id, message_id, new_text: tb.edit_message_text(chat_id=chat_id, message_id=message_id, text=new_text)
)

# Globals
player = None
logic: Logic = None

def start_bot(player_ref, logic_ref):
    global player
    global logic
    player = player_ref
    logic = logic_ref
    th = threading.Thread(target=run_polling)
    th.start()


@tb.message_handler(commands=['start', 'help'], only_admin_chat=True)
def handle_start_help(message):
    print("Start from admins ", message.chat.id)
    logging.info("admin start/help")
    markup = get_admin_ui()
    tb.send_message(message.chat.id, Transl(LangKeys.admin_instruction), reply_markup=markup)


@tb.message_handler(commands=['start', 'help'], only_admin_chat=False)
def handle_start_help(message):
    print("Start from user ", message.chat.id)
    logging.info("user start/help")
    tb.send_message(message.chat.id, Transl(LangKeys.instruction))

@tb.message_handler(text=['⏯', '⏯️'], only_admin_chat=True)
def handle_p_p(message):
    if player.is_now_playing():
        logging.info("pause")
        tb.send_message(message.chat.id, Transl(LangKeys.pause_msg))
        player.pause()
    else:
        logging.info("play")
        tb.send_message(message.chat.id, Transl(LangKeys.play_msg))
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
    tb.send_message(message.chat.id, Transl(LangKeys.setting_song, name))


@tb.message_handler(text=['⏮'], only_admin_chat=True)
def handle_prev(message):
    res = player.prev()
    if res is None:
        tb.send_message(message.chat.id, "Something went wrong")
        return
    logging.info("prev")
    tb.send_message(message.chat.id, Transl(LangKeys.setting_song, res))


@tb.message_handler(text=['⏹'], only_admin_chat=True)
def handle_stop(message):
    player.stop()
    logging.info("stop")
    tb.send_message(message.chat.id, Transl(LangKeys.stop_msg))


@tb.message_handler(commands=['radio'], only_admin_chat=True)
def handle_radio(message):
    logging.info("radio")
    tb.send_message(message.chat.id, Transl(LangKeys.radio_stations_msg), reply_markup=get_radio_list_keyboard())


@tb.message_handler(commands=['orders'], only_admin_chat=True)
def handle_orders(message):
    if not player.is_from_radio:
        tb.send_message(message.chat.id, Transl(LangKeys.already_selected_msg))
        return
    logging.info("orders")
    player.switch_to_orders()
    tb.send_message(message.chat.id, Transl(LangKeys.orders_msg))


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


@tb.message_handler(commands=['list'], only_admin_chat=False)
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


@tb.message_handler(commands=['now'], only_admin_chat=False)
@tb.message_handler(text=['Whats playing now?'], only_admin_chat=False)
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
    valid = validators.url(message.text)
    ctx = ctx_factory.new(message)
    if valid:
        tb.send_message(message.chat.id, Transl(LangKeys.url_ok))
        print("Url is valid")
        res_dict = logic.fetch_info(message.text, ctx)
        if len(res_dict) == 0:
            logging.warning("No info for link!")
            tb.send_message(message.chat.id, Transl(LangKeys.url_cant_load))
            return
        tb.send_message(message.chat.id, Transl(LangKeys.starting_url_load))
        logic.start_download(res_dict, ctx)
    else:
        logging.info("Invalid Link")
        tb.send_message(message.chat.id, Transl(LangKeys.url_bad))
