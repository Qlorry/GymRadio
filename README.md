### Windows installation:

1. Download ffmpeg 
        
        https://www.gyan.dev/ffmpeg/builds/
        
2. Download VLC

        https://www.videolan.org/vlc/index.ru.html

3. Install requirements

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
