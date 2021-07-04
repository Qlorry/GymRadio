### Windows installation:

1. Download ffmpeg 
        
        https://www.gyan.dev/ffmpeg/builds/
        
2. Download VLC

        https://www.videolan.org/vlc/index.ru.html

3. Install requirements


4. Build

### Windows Build

      pyinstaller -F --distpath GymBot --specpath build -i ..\icon.ico -n GymBot main.py
      mkdir GymBot\Radio GymBot\Logs
      xcopy Radio GymBot\Radio /e /s
      copy ffmpeg.exe GymBot\ffmpeg.exe /y

### Clear
      
      rmdir GymBot build /S /Q

### Linux Build

      pyinstaller -F --distpath GymBot --specpath build -i ../icon.ico -n GymBot main.py
      mkdir GymBot/Radio GymBot/Logs
      cp -avR Radio GymBot
      cp /usr/local/opt/ffmpeg/bin/ffmpeg GymBot/ffmpeg

### Clear
      
      rm -r dist build


### Run instruction

1. Get your bot API token from FatherBot
2. Run app to get default config
3. Set _token_ to your API token
4. Start bot
5. Create admins chat
      1. Start bot
      2. Add bot in chat
      3. Write start
      4. From message in console copy chat id
6. Set _admins_chat_ to id from 5.IV.
7. Restart bot
