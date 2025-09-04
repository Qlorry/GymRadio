import datetime
import logging
import sys

from Util.util import *


date_on_start = datetime.datetime.now()
# logging.basicConfig(filename=log_filename, level=logging.INFO)

class BraceStyleAdapter(logging.Logger):
    def _log(self, level, msg, args, exc_info=None, extra=None, stack_info=False, stacklevel=1):
        if args:
            # do str.format with args instead of %s substitution
            if isinstance(msg, str):
                msg = msg.format(*args)
            else:
                msg = str(msg)
            args = ()  # clear so logging won’t try % formatting
        super()._log(level, msg, args, exc_info, extra, stack_info, stacklevel)

# Patch the logging class globally
logging.setLoggerClass(BraceStyleAdapter)

log_formatter = logging.Formatter('[{asctime}][{levelname}][{thread}][{chat}/{user}][{name}] {message}',
                                  datefmt='%Y-%m-%d %H:%M:%S', 
                                  style='{',
                                  defaults={'chat': '-', 'user': '-'})

sh = logging.StreamHandler(stream=sys.stdout)
sh.setFormatter(log_formatter)
logging.root.addHandler(sh)
log_filename = "Logs/"+date_on_start.strftime("%y-%m-%d %H-%M") + ".log"
fh = logging.FileHandler(log_filename, "a", encoding="utf-8")
fh.setFormatter(log_formatter)
logging.root.addHandler(fh)
logging.root.setLevel(logging.INFO)
rm_old_logs()
