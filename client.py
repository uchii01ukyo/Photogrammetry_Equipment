import socket

def main():
    # local client
    Client_IP = "127.0.0.1"
    Client_Port = 10031
    Client_Addr = (Client_IP, Client_Port)
    # UDP-Serial server
    UDP_SERIAL_IP = "127.0.0.1"
    UDP_SERIAL_Port = 10030
    UDP_SERIAL_Addr = (UDP_SERIAL_IP, UDP_SERIAL_Port)
    BUFSIZE = 1024

    udpSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udpSock.bind(UDP_SERIAL_Addr)
    udpSock.settimeout(1)

    while True:                                     
        try:
            data, addr = udpSock.recvfrom(BUFSIZE)
        except:
            pass
        else:
            print("> " + data.decode())
            udpSock.sendto("ok".encode('utf-8'), addr)
            print("-> end")


if __name__ == '__main__':
    main()