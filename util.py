import os


def compare(str1, str2):
    i = 0
    l = len(str2)
    while i < l:
        if str1[i] != str2[i]:
            return False
        i += 1
    return True


def is_youtube_link(url):
    if compare(url, 'https://music.youtube.com'):
        return True
    if compare(url, 'https://www.youtube.com'):
        return True
    if compare(url, 'https://youtube.com'):
        return True
    if compare(url, 'https://youtu.be'):
        return True
    return False


def is_not_admins_chat(chat_id, conf):
    if str(chat_id) == conf.admins_chat:
        return False
    return True


def rm_old_logs():
    cnt = 0
    oldest = None
    oldestfile = None
    for root, subdirs, files in os.walk('Logs'):
        for filename in files:
            cnt += 1
            time = os.path.getctime("Logs/"+filename)
            if oldest is None:
                oldest = time
                oldestfile = filename
            if time < oldest:
                oldest = time
                oldestfile = filename
            if cnt > 2:
                try:
                    os.remove("Logs/"+oldestfile)
                except Exception:
                    print()
