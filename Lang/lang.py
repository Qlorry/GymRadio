from Lang.lang_keys import LangKeys

import Lang.UA_lang as ua
import Lang.EN_lang as en

from Config.config import conf

_TRANSLATION = en.TRANSLATION

if conf.lang == "UA":
    for key in ua.TRANSLATION.keys():
        _TRANSLATION[key] = ua.TRANSLATION[key]

def Transl(key: LangKeys, *args):
    return _TRANSLATION[key].format(*args)


