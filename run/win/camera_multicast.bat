cd %~dp0
cd ../../capture
python camera_multicast.py 'movie' 1920 1080 30 30
rem :'mode' frame_width frame_height frame_fps frame_brightness 
open ./capture
pause