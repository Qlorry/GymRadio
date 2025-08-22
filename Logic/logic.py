import logging

from DataDownloader.downloader import Downloader
from DataDownloader.convertor import convert
from Player.Song import Song
from Player.SuperPlayer import SuperPlayer
from Util.ctx import Ctx
import Util.util as util
from Lang.lang import Transl
from Lang.lang_keys import LangKeys


class Logic:
    def __init__(self, player: SuperPlayer):
        self._downloader = Downloader()
        self._player = player

    def fetch_info(self, url, ctx: Ctx):
        if util.is_youtube_link(url):
            logging.info("Loading YT link")
            return self._downloader.load_info(url)
        new_links = convert(url)
        if len(new_links) == 0:
            ctx.respond(Transl(LangKeys.song_not_found))
            return []
        for link in new_links:
            result = self._downloader.load_info(link)
            if len(result) != 0:
                ctx.respond(Transl(LangKeys.found_this, link))
                return result
        return []


    def add_list(self, res_dict, ctx: Ctx):
        logging.info("Adding playlist")
        cnt = 0
        fails = 0
        msg_str = "Adding playlist: \n \n"

        list_msg = ctx.respond(msg_str)

        for item in res_dict.get('entries'):
            name = item.get('title') if item.get('title') is not None else ""
            album = item.get('album') if item.get('album') is not None else "NA"
            if util.is_song_in_os(album, name):
                loaded_song = item
            else:
                loaded_song = self._downloader.load(item['webpage_url'])
            if loaded_song is None:
                cnt += 1
                msg_str += "#" + str(cnt) + " " + item.get('title') + " -- Failed\n"
                fails += 1
                continue
            self._player.add_song(Song(loaded_song.get('title'), loaded_song.get('album')))
            cnt += 1
            msg_str += "#" + str(cnt) + " " + loaded_song.get('title') + "\n"
            ctx.edit_respond(list_msg, msg_str)

        msg_str += Transl(LangKeys.found_n_songs, (cnt - fails))
        ctx.edit_respond(list_msg, msg_str)


    def add_single(self, res_dict, ctx: Ctx):
        logging.info("Adding single song " + res_dict.get('title'))

        name = res_dict.get('title') if res_dict.get('title') is not None else ""
        album = res_dict.get('album') if res_dict.get('album') is not None else "NA"
        if util.is_song_in_os(album, name):
            loaded_song = res_dict
        else:
            loaded_song = self._downloader.load(res_dict['webpage_url'])
        if loaded_song is None:
            ctx.respond(res_dict.get('title') + " -- Failed\n")
            return
        self._player.add_song(Song(loaded_song.get('title'), loaded_song.get('album')))
        ctx.respond(Transl(LangKeys.song_name_added, loaded_song.get('title')))


    def start_download(self, res_dict, ctx: Ctx):
        if '_type' in res_dict:
            self.add_list(res_dict, ctx)
        else:
            self.add_single(res_dict, ctx)
