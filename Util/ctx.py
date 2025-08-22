from typing import Union

import telebot


class Ctx:
    def __init__(self, message: telebot.types.Message, respond_callback, edit_callback):
        self.chat_id = message.chat.id
        self._respond_callback = respond_callback
        self._edit_callback = edit_callback

    def respond(self, text) -> telebot.types.Message:
        self._respond_callback(self.chat_id, text)

    def edit_respond(self, message: telebot.types.Message, new_text) -> Union[telebot.types.Message, bool]:
        self._edit_callback(self.chat_id, message.message_id, new_text)