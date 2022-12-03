#!/bin/sh
send_bcast
sleep 1
curl http://192.168.179.10/capture2 -o a.jpg
curl http://192.168.179.11/capture2 -o b.jpg
curl http://192.168.179.12/capture2 -o c.jpg