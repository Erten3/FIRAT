from __future__ import print_function
import cv2
import imutils
import socket
import numpy as np
import time
import base64
import socket
from struct import unpack

HOST = '192.168.1.21'
PORT = 12345########en az 5 dk hiç kapanmadan port ve ip üzerinden dinleme yapıyor
BUFSIZE = 4096

class Receiver:
    ''' Buffer binary data from socket conn '''
    def __init__(self, conn):
        self.conn = conn
        self.buff = bytearray()

    def get(self, size):
        ''' Get size bytes from the buffer, reading
            from conn when necessary
        '''
        while len(self.buff) < size:
            data = self.conn.recv(BUFSIZE)
            if not data:
                break
            self.buff.extend(data)
        # Extract the desired bytes
        result = self.buff[:size]
        # and remove them from the buffer
        del self.buff[:size]
        return bytes(result)

    def save(self, fname):
        ''' Save the remaining bytes to file fname '''
        with open(fname, 'wb') as f:
            if self.buff:
                f.write(bytes(self.buff))
            while True:
                data = self.conn.recv(BUFSIZE)
                if not data:
                    break
                f.write(data)

def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    try:
        sock.bind((HOST, PORT))
    except socket.error as err:
        print('Bind failed', err)
        return

    sock.listen(1)
    print('Socket now listening at', HOST, PORT)
    try:
        while True:
            conn, addr = sock.accept()
            print('Connected with', *addr)
            # Create a buffer for this connection
            receiver = Receiver(conn)
            # Get the length of the file name
            name_size = unpack('B', receiver.get(1))[0]
            # Get the file name itself
            name = receiver.get(name_size).decode()
            print('name', name)
            # Save the file
            receiver.save(name)
            conn.close()
            print('saved\n')
            exit()
    # Hit Break / Ctrl-C to exit
    except KeyboardInterrupt:
        print('\nClosing')

    sock.close()

if __name__ == '__main__':
    main()