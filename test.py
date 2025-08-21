import yt_dlp
import vlc

# YouTube URL
url = "https://www.youtube.com/watch?v=jfKfPfyJRdk&ab_channel=LofiGirl"

# Step 1: Use yt-dlp to get the direct stream URL
ydl_opts = {
    'format': 'bestaudio/best',  # pick best available
    'quiet': True,
}
with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    info = ydl.extract_info(url, download=False)
    stream_url = info['url']

print("Resolved stream:", stream_url)

# Step 2: Play with VLC
instance = vlc.Instance()
player = instance.media_player_new()
media = instance.media_new(stream_url)
player.set_media(media)
player.play()

# Keep the script running so playback continues
while True:
    pass