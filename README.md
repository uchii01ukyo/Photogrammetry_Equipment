# Photogrammetry
Proposal for 3D recording of physical experiments using photogrammetry.
(ex: physical experiments = experiments of soil fracture behavior) 
  
### What Photogrammetry?
A method of photographing a subject from various angles and integrating the digital images to create a three-dimensional 3DCG model.
  
## Contents
### basic
+ **camera.py**  
  ... How to use a usb-camera simply  
+ **multi_test.py**  
  ... How to use some usb-cameras simply  
  
### capture
+ **camera_capture_single.py**  
  ... Control a usb-camera  
+ **camera_capture_multi.py**  
  ... Control some usb-camera using multi_thread  
+ **camera_capture_multi_fps.py**  
  ... Control some usb-camera using multi_thread + continuous shooting  
+ **camera_capture_multi_sametiming.py**  
  ... Control some usb-camera using multi_thread + shoot same timing of all  
+ **camera_capture_multi_server.py**  
  ... Control some usb-camera using multi_thread + Linkage of two PCs via UDP (server)  
+ **camera_capture_multi_client.py**  
  ... Control some usb-camera using multi_thread + Linkage of two PCs via UDP (client)  
  
### movie
+ **camera_movie_single.py**  
  ... Recording using a usb-camera  
+ **camera_movie_multi.py**  
  ... Recording using some usb-cameras + record same start-timing of all  
  
## System
In progress...
  
## Author  
Uchii Ukyo (https://github.com/uchii01ukyo)
