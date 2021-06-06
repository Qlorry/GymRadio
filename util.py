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
    return False
