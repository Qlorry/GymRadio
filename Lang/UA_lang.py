from Lang.lang_keys import LangKeys

TRANSLATION = {
    LangKeys.instruction : "    Привіт!\n" \
                "Я домовий цього залу!\n" \
                "Щоб замовити пісню просто відправ мені посилання з улюбленого стрімінгу і я спробую її знайти\n" \
                "\n" \
                "    Деталі\n" \
                "1. Ти відправляєш посилання сюди\n" \
                "2. Я шукаю у себе за пічкою\n" \
                "3. Добавляю в чергу\n" \
                "4. Твоя пісня грає!!!\n" \
                "\n" \
                "    Які посилання підійдуть?\n" \
                "З будь-якого стрімінгового сервіса(з ймовірністю 99,9% включу з youtube music)\n" \
                "Кидай сюди посилання на альбом чи плейліст з youtube music, добавлю в чергу все.",
    LangKeys.song_not_found : "Ой, не можу знайти пісню за цим посиланням",
    LangKeys.found_this : "От що я знайшов в ютубі {0}",
    LangKeys.admin_instruction : "Вибери що потрібно зробити",
    LangKeys.stop_msg : "Стоп",
    LangKeys.pause_msg : "Пауза",
    LangKeys.play_msg : "Включаю!",
    LangKeys.radio_stations_msg : "Вибери радіостанцію:",
    LangKeys.url_ok : "Працюю над посиланням",
    LangKeys.url_bad : "Щось не так з посиланням((",
    LangKeys.url_cant_load : "Не можу завантажити цю пісню",
    LangKeys.starting_url_load : "Починаю завантаження",
    LangKeys.already_selected_msg : "Вже вибрано",
    LangKeys.orders_msg : "Замовлення",
    LangKeys.found_n_songs: "Добавив {0} пісень в чергу",
    LangKeys.song_name_added: "Пісня \"{0}\" додана до черги",
    LangKeys.setting_song: "Вмикаю \"{0}\"",
}
