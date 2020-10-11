from socket import *
import struct

PORT = 8080
ip = "127.0.0.1"
recv_size = 2020

def main():
    s = socket(AF_INET,SOCK_STREAM)
    s.connect((ip,PORT))
    while True:
        data = struct.pack('>if', 1, 0.1)
        s.sendall(data)
        recv_data = s.recv(recv_size)
        print(recv_data)


if __name__ == '__main__':
    main()

