import datetime
import logging

from Logic.logic import Logic
from Player.SuperPlayer import SuperPlayer
from Util.util import *
from bot import start_bot

date_on_start = datetime.datetime.now()
log_filename = "Logs/"+date_on_start.strftime("%y-%m-%d %H-%M") + ".log"
logging.basicConfig(filename=log_filename, level=logging.INFO)
rm_old_logs()

player = SuperPlayer()
player.play()

logic = Logic(player)

start_bot(player, logic)
