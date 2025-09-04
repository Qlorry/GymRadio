from DataDownloader.downloader import Downloader
from DataDownloader.convertor import convert
from Player.OrderListPlayer import ChangeSongRes
from Player.Song import Song
from Player.SuperPlayer import Source, SuperPlayer
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
            ctx.logger.info("Loading YT link {0}".format(url))
            return self._downloader.load_info(url)
        new_links = convert(url)
        if len(new_links) == 0:
            ctx.respond(Transl(LangKeys.song_not_found))
            return []
        ctx.logger.info("Loading multiple YT links {0}".format(str(new_links)))
        for link in new_links:
            result = self._downloader.load_info(link)
            if len(result) != 0:
                ctx.respond(Transl(LangKeys.found_this, link))
                return result
        return []


    def add_list(self, res_dict, ctx: Ctx):
        ctx.logger.info("Adding playlist")
        cnt = 0
        fails = 0
        msg_str = Transl(LangKeys.adding_playlist)

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
        ctx.logger.info("Adding single song " + res_dict.get('title'))

        name = res_dict.get('title') if res_dict.get('title') is not None else ""
        album = res_dict.get('album') if res_dict.get('album') is not None else "NA"
        if util.is_song_in_os(album, name):
            loaded_song = res_dict
        else:
            loaded_song = self._downloader.load(res_dict['webpage_url'])
        if loaded_song is None:
            ctx.respond(Transl(LangKeys.song_load_failed, res_dict.get('title')))
            return
        self._player.add_song(Song(loaded_song.get('title'), loaded_song.get('album')))
        ctx.respond(Transl(LangKeys.song_name_added, loaded_song.get('title')))


    def start_download(self, res_dict, ctx: Ctx):
        if '_type' in res_dict:
            self.add_list(res_dict, ctx)
        else:
            self.add_single(res_dict, ctx)


    def play_or_pause(self, ctx: Ctx):
        if self._player.is_now_playing():
            ctx.logger.info("pause")
            ctx.respond(Transl(LangKeys.pause_msg))
            self._player.pause()
        else:
            ctx.logger.info("play")
            ctx.respond(Transl(LangKeys.play_msg))
            self._player.play()

    def next(self, ctx: Ctx):
        ctx.logger.info("next")
        song_name = self._player.next()
        if song_name is None:
            ctx.respond(Transl(LangKeys.something_went_wrong))
            return
        elif song_name is ChangeSongRes.empty_list:
            ctx.respond(Transl(LangKeys.list_of_songs_is_empty))
            return
        elif song_name is ChangeSongRes.end:
            ctx.respond(Transl(LangKeys.end_of_song_list))
            return

        ctx.respond(Transl(LangKeys.setting_song, song_name))

    def prev(self, ctx: Ctx):
        ctx.logger.info("prev")
        res = self._player.prev()
        if res is None:
            ctx.respond(Transl(LangKeys.something_went_wrong))
            return
        ctx.respond(Transl(LangKeys.setting_song, res))

    def play_orders(self, ctx: Ctx):
        if self._player.is_playing(Source.ORDERS):
            ctx.respond(Transl(LangKeys.already_selected_msg))
            return
        ctx.logger.info("orders")
        self._player.switch_to_orders()
        ctx.respond(Transl(LangKeys.orders_msg))

    def play_streams(self, ctx: Ctx):
        if self._player.is_playing(Source.STREAM):
            ctx.respond(Transl(LangKeys.already_selected_msg))
            return
        ctx.logger.info("streams")
        self._player.switch_to_streams()
        ctx.respond(Transl(LangKeys.streams_msg, self._player.whats_playing()))


    def get_upnext_list(self, ctx: Ctx):
        ctx.logger.info("upnext")
        return self._player.get_next_songs(5)

    def get_history_list(self, ctx: Ctx):
        ctx.logger.info("history")
        return self._player.get_prev_songs(5)

    def handle_list(self, ctx: Ctx):
        ctx.logger.info("list")
        songs = self._player.get_all_songs()
        if len(songs) == 0:
            ctx.logger.warning("No songs in media player")
            ctx.respond(Transl(LangKeys.list_is_empty))
            return
        current = self._player.get_current_index()
        msg = Transl(LangKeys.request_list) + "\n"
        cnt = 1
        for s in songs:
            if cnt - 1 == current:
                msg += "-> " + str(cnt) + " " + s.name + "\n"
            else:
                msg += "  #" + str(cnt) + " " + s.name + "\n"
            cnt += 1
        ctx.respond(msg)