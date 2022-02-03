### Windows installation:

1. Download ffmpeg 
        
        https://www.gyan.dev/ffmpeg/builds/
        
2. Download VLC

        https://www.videolan.org/vlc/index.ru.html

3. Install requirements


4. Build

### Windows Build

      pyinstaller -F --distpath _BuildGymBot --specpath build -i ..\BuildRelated\icon.ico -n GymBot main.py
      mkdir _BuildGymBot\Radio _BuildGymBot\Logs
      xcopy Radio _BuildGymBot\Radio /e /s /y
      copy ffmpeg.exe _BuildGymBot\ffmpeg.exe /y

### Clear
      
      rmdir GymBot build /S /Q

### Linux Build

      pyinstaller -F --distpath _BuildGymBot --specpath build -i ../BuildRelated/icon.ico -n GymBot main.py
      mkdir _BuildGymBot/Radio _BuildGymBot/Logs
      cp -avR Radio _BuildGymBot
      cp /usr/local/opt/ffmpeg/bin/ffmpeg _BuildGymBot/ffmpeg

### Clear
      
      rm -r build _BuildGymBot


### Run instruction

1. Get your bot API token from FatherBot
2. Run bot app to get default config
3. Set _token_ to your API token
4. Restart bot app
5. Create admins chat(can be your own chat with bot)
      1. Restart bot app
      2. Add bot to chat
      3. Use /start command
      4. From message in console copy chat id
6. Set _admins_chat_ to id from 5.4.
7. Restart bot app
