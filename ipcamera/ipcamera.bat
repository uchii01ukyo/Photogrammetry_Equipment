http://192.168.11.16
curl http://192.168.11.16/control?var=framesize&val=10
curl http://192.168.11.16/control?var=framesize&val=FRAMESIZE_UXGA
curl http://192.168.11.16/capture -o capture.jpg
curl http://192.168.11.16/status
gcc send_bcast.c -o send_bcast