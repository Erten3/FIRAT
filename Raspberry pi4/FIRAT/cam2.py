import cv2
import socket
import struct
import pickle

# Socket ayarları
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host_ip = '127.0.0.1'
port = 9999
socket_address = (host_ip, port)

# Server'a bağlanma
client_socket.connect(socket_address)

data = b""
payload_size = struct.calcsize("Q")

# Video kaydedici ayarları
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('output.avi', fourcc, 20.0, (640, 480))

while True:
    while len(data) < payload_size:
        packet = client_socket.recv(4*1024)  # 4KB'lık paketler alınıyor
        if not packet:
            break
        data += packet

    packed_msg_size = data[:payload_size]
    data = data[payload_size:]
    msg_size = struct.unpack("Q", packed_msg_size)[0]

    while len(data) < msg_size:
        data += client_socket.recv(4*1024)
    
    frame_data = data[:msg_size]
    data = data[msg_size:]

    frame = pickle.loads(frame_data)

    # Frame'i gösterme ve kaydetme
    cv2.imshow('Received', frame)
    out.write(frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Temizlik
client_socket.close()
out.release()
cv2.destroyAllWindows()
