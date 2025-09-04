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
from Util.ctx import Ctx
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
@ctx_factory.add_ctx
def handle_start_help(message, ctx: Ctx):
    ctx.logger.info("admin start/help")
    markup = get_admin_ui()
    tb.send_message(message.chat.id, Transl(LangKeys.admin_instruction), reply_markup=markup)


@tb.message_handler(commands=['start', 'help'], only_admin_chat=False)
@ctx_factory.add_ctx
def handle_start_help(message, ctx: Ctx):
    logging.info("user start/help")
    tb.send_message(message.chat.id, Transl(LangKeys.instruction))

@tb.message_handler(text=['⏯', '⏯️'], only_admin_chat=True)
@ctx_factory.add_ctx
def handle_play_pause(message, ctx: Ctx):
    logic.play_or_pause(ctx)


@tb.message_handler(text=['⏭'], only_admin_chat=True)
@ctx_factory.add_ctx
def handle_next(message, ctx: Ctx):
    logic.next(ctx)


@tb.message_handler(text=['⏮'], only_admin_chat=True)
@ctx_factory.add_ctx
def handle_prev(message, ctx: Ctx):
    logic.prev(ctx)


@tb.message_handler(text=['⏹'], only_admin_chat=True)
@ctx_factory.add_ctx
def handle_stop(message, ctx: Ctx):
    player.stop()
    logging.info("stop")
    tb.send_message(message.chat.id, Transl(LangKeys.stop_msg))


@tb.message_handler(commands=['radio'], only_admin_chat=True)
@ctx_factory.add_ctx
def handle_radio(message, ctx: Ctx):
    logging.info("radio")
    tb.send_message(message.chat.id, Transl(LangKeys.radio_stations_msg), reply_markup=get_radio_list_keyboard())


@tb.message_handler(commands=['orders'], only_admin_chat=True)
@ctx_factory.add_ctx
def handle_orders(message, ctx: Ctx):
    logic.play_orders(ctx)

@tb.message_handler(commands=['live_streams'], only_admin_chat=True)
@ctx_factory.add_ctx
def handle_orders(message, ctx: Ctx):
    logic.play_streams(ctx)


@tb.message_handler(commands=['upnext'], only_admin_chat=True)
@ctx_factory.add_ctx
def handle_upnext(message, ctx: Ctx):
    logging.info("upnext")
    songs = logic.get_upnext_list()
    if len(songs["list"]) == 0:
        logging.warning("No More songs for upnext")
        tb.send_message(message.chat.id, "No more songs in queue")
        return
    tb.send_message(message.chat.id, "Next songs:\n", reply_markup=get_upnext_list_keyboard(songs["list"],
                                                                                            songs["lastIndex"]))


@tb.message_handler(commands=['history'], only_admin_chat=True)
@ctx_factory.add_ctx
def handle_history(message, ctx: Ctx):
    logging.info("history")
    songs = logic.get_history_list()
    if len(songs["list"]) == 0:
        logging.warning("No More songs for history")
        tb.send_message(message.chat.id, "No more songs in history")
        return
    tb.send_message(message.chat.id,
                    "Previous songs:\n",
                    reply_markup=get_history_list_keyboard(songs["list"], songs["firstIndex"]))


@tb.message_handler(commands=['list'], only_admin_chat=False)
@ctx_factory.add_ctx
def handle_list(message, ctx: Ctx):
    logic.handle_list(ctx)


@tb.message_handler(commands=['now'], only_admin_chat=False)
@tb.message_handler(text=['Whats playing now?'], only_admin_chat=False)
@ctx_factory.add_ctx
def handle_now(message, ctx: Ctx):
    logging.info("Want's now")
    tb.send_message(chat_id=message.chat.id, text=player.whats_playing())


@tb.message_handler(commands=['swap'], only_admin_chat=True)
@ctx_factory.add_ctx
def handle_swap(message, ctx: Ctx):
    logging.info("swap")
    command = message.text.split()
    try:
        player.swap(int(command[1]), int(command[2]))
        tb.send_message(chat_id=message.chat.id, text=Transl(LangKeys.ok))
    except():
        return


@tb.callback_query_handler(func=lambda call: True)
@ctx_factory.add_ctx
def callback_inline(call, ctx: Ctx):
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
@ctx_factory.add_ctx
def handle_input(message, ctx: Ctx):
    valid = validators.url(message.text)
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


# TODO: Sound controls