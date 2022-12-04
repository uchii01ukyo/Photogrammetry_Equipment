import requests
import socket

def get_gip_addr():
    res = requests.get('https://ifconfig.me')
    print(res.text)

def get():
    ip = socket.gethostbyname_ex(socket.gethostname())
    a=ip[2]
    print(a[0])

if __name__ == '__main__':
   get()