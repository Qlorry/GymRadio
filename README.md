### Windows installation:

1. Download ffmpeg 
        
        https://www.gyan.dev/ffmpeg/builds/
        
2. Download VLC

        https://www.videolan.org/vlc/index.ru.html

3. Install requirements

### Windows Build

      pyinstaller -F -n GymBot main.py
      mkdir dist\music\Radio
      xcopy music\Radio dist\music\Radio /e /s
      copy ffmpeg.exe dist\ffmpeg.exe /y

### Clear
      
      rmdir dist build /S /Q

### Linux Build

      pyinstaller -F -n GymBot main.py
      mkdir dist
      cp -avR music dist
      cp /usr/local/opt/ffmpeg/bin/ffmpeg dist/ffmpeg

### Clear
      
      rm -r dist build
