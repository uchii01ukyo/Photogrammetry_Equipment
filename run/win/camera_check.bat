cd %~dp0
cd ../../capture
python -c "import camera_capture; camera_capture.check_camera()"
pause