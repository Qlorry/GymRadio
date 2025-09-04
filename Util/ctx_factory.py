import telebot
from Util.ctx import Ctx


class CtxFactory(object):
    def __init__(self, respond_callback, edit_callback):
        self._respond_callback = respond_callback
        self._edit_callback = edit_callback
    
    def new(self, message: telebot.types.Message) -> Ctx:
        return Ctx(message, self._respond_callback, self._edit_callback)
       
    def add_ctx(self, func):
        def wrapper(*args, **kwargs):
            kwargs["ctx"] = self.new(args[0])
            result = func(*args, **kwargs)
            return result
        return wrapper