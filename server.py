# coding: UTF-8
import socket
#from socket import *

def main():

    # $ipconfig/all or $ifconfig
    Client_IP = "192.168.11.6"
    Client_Port = 50000
    Client_Addr = (Client_IP, Client_Port)
    UDP_SERIAL_IP = "192.168.11.8"
    UDP_SERIAL_Port = 50000
    UDP_SERIAL_Addr = (UDP_SERIAL_IP, UDP_SERIAL_Port)
    UDP_BUFSIZE = 1024

    udpSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udpSock.bind(Client_Addr)
    udpSock.settimeout(1)

    command = "Hello"
    print(command)
    udpSock.sendto(command.encode('utf-8'), UDP_SERIAL_Addr)

    while True:
        try:
            data, addr = udpSock.recvfrom(UDP_BUFSIZE)
        except:
            pass
        else:
            if data.decode() == "ok":
                print("-> OK")
                break
    print("end")


if __name__ == '__main__':
    main()
