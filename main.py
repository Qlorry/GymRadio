import logging
import Util.log
from Logic.logic import Logic
from Player.SuperPlayer import SuperPlayer
from bot import start_bot


player = SuperPlayer()
player.play()

logic = Logic(player)

start_bot(player, logic)
