from typing import Union

import telebot
import logging


class ContextLogger(logging.LoggerAdapter):
    def __init__(self, chat, user):
        super(ContextLogger, self).__init__(logging.getLogger("context"), {'chat': chat, 'user': user})


class Ctx:
    def __init__(self, message: telebot.types.Message | telebot.types.CallbackQuery, respond_callback, edit_callback):
        if isinstance(message, telebot.types.CallbackQuery):
            message = message.message
        
        self.chat_id = message.chat.id
        self._respond_callback = respond_callback
        self._edit_callback = edit_callback
        self.logger = ContextLogger(self.chat_id, message.from_user.id)
        

    def respond(self, text) -> telebot.types.Message:
        return self._respond_callback(self.chat_id, text)

    def edit_respond(self, message: telebot.types.Message, new_text) -> Union[telebot.types.Message, bool]:
        return self._edit_callback(self.chat_id, message.message_id, new_text)