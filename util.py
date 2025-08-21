import os
from yt_dlp.utils import sanitize_filename, sanitize_path


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
    oldest_file = None
    for root, subdirs, files in os.walk('Logs'):
        for filename in files:
            cnt += 1
            time = os.path.getctime("Logs/"+filename)
            if oldest is None:
                oldest = time
                oldest_file = filename
            if time < oldest:
                oldest = time
                oldest_file = filename
            if cnt > 2:
                try:
                    os.remove("Logs/"+oldest_file)
                except Exception:
                    print()


def is_song_in_os(album, name):
    sanitized_name = sanitize_filename(name, restricted=False)
    sanitized_album = sanitize_filename(album, restricted=False)
    path = sanitize_path("music/" + sanitized_album + "/" + sanitized_name + ".m4a")
    if not os.path.exists(path):
        return False
    return True


def is_song_p_in_os(path):
    if not os.path.exists(path):
        return False
    return True
