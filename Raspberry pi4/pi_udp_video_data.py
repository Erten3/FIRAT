import socket
import cv2
import numpy as np
from pymavlink import mavutil
import struct

# OpenCV kullanarak harici kamerayı aç
cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

# UDP soketi oluştur ve hedef adresi ayarla
udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_address = ('192.168.1.10', 5005)

# Pixhawk'a bağlan
port = '/dev/ttyACM0'  # Bu port, bağlı olan Pixhawk'ın portu olabilir.
baud_rate = 115200     # Pixhawk'ın standart baud rate değeri
master = mavutil.mavlink_connection(port, baud=baud_rate)

# Heartbeat mesajı alana kadar bekleyin
master.wait_heartbeat()
print("Heartbeat received")

CHUNK_SIZE = 65000  # UDP paket boyut limiti

while True:
    ret, frame = cap.read()
    if not ret:
        continue
    
    # Görüntüyü JPEG formatında sıkıştır
    encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]
    result, img_encoded = cv2.imencode('.jpg', frame, encode_param)
    image_data = img_encoded.tobytes()
    
    # Telemetri verilerini al
    msg = master.recv_match(type='GLOBAL_POSITION_INT', blocking=True)
    if msg:
        lat = msg.lat / 1e7
        lon = msg.lon / 1e7
        alt = msg.alt / 1e3
        
        # Konum verilerini paketle
        telemetry_data = struct.pack('!ddd', lat, lon, alt)
        
        # Görüntü ve telemetri verilerini birleştir
        data = telemetry_data + image_data
    
        # Veriyi parçalara bölerek gönder
        for i in range(0, len(data), CHUNK_SIZE):
            udp_socket.sendto(data[i:i+CHUNK_SIZE], server_address)
    
    # Gönderilen görüntüyü yerel ekranda göster
    cv2.imshow('Sending', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Kaynakları serbest bırak
cap.release()
cv2.destroyAllWindows()
udp_socket.close()