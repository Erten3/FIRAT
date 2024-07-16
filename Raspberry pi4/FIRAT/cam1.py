import cv2
import socket
import struct
import pickle

# Socket ayarları
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host_ip = '127.0.0.1'
port = 9999
socket_address = (host_ip, port)

# Socket oluşturuluyor
server_socket.bind(socket_address)
server_socket.listen(5)
print(f"Listening at: {socket_address}")

# Kamera açılıyor
cap = cv2.VideoCapture(0)

# Client ile bağlantı kuruluyor
client_socket, addr = server_socket.accept()
print(f"Connection from: {addr}")

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    
    # Frame'i pickle ile serileştirme ve paketleme
    data = pickle.dumps(frame)
    message_size = struct.pack("Q", len(data))

    # Paketi gönderme
    client_socket.sendall(message_size + data)

# Temizlik
cap.release()
client_socket.close()
server_socket.close()
