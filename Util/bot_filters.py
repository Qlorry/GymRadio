import telebot

from Config.config import conf


class OnlyAdmins(telebot.AdvancedCustomFilter):
    key = 'only_admin_chat'

    def check(self, message, text):
        if not text:
            return True
        return str(message.chat.id) == conf.admins_chat

class TextMatch(telebot.AdvancedCustomFilter):
    key = 'text'

    def check(self, message, text):
        """
        :meta private:
        """
        if isinstance(text, list):
            return message.text in text
        else:
            return text == message.text