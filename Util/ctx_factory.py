import telebot
from Util.ctx import Ctx


class CtxFactory(object):
    def __init__(self, respond_callback, edit_callback):
        self._respond_callback = respond_callback
        self._edit_callback = edit_callback
    
    def new(self, message: telebot.types.Message) -> Ctx:
        return Ctx(message, self._respond_callback, self._edit_callback)