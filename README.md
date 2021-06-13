### Windows installation:

1. Download ffmpeg 
        
        https://www.gyan.dev/ffmpeg/builds/
        
2. Download VLC

        https://www.videolan.org/vlc/index.ru.html

3. Install requirements

### Build

      pyinstaller -F -n GymBot main.py
      mkdir dist\music
      xcopy music dist\music /e /s
      copy ffmpeg.exe dist\ffmpeg.exe /y

### Clear
      
      rmdir dist build /S /Q

   