#!/bin/sh
cd `dirname $0`
cd ../../capture
python -c "import camera_capture; camera_capture.check_camera()"