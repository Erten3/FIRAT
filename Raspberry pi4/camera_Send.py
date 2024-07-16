import socket
import time
import io
import cv2
import numpy as np
import picamera

# UDP soketi oluştur ve hedef adresi ayarla
udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_address = ('192.168.1.10', 5005)

# Kamera ayarları
camera = picamera.PiCamera()
camera.resolution = (640, 480)
camera.framerate = 24
camera.vflip = True  # Gerekirse kamerayı dikey olarak çevir

# Video akışını yakalamak için bir ByteIO nesnesi kullan
stream = io.BytesIO()

while True:
    # Stream içeriğini temizle
    stream.seek(0)
    stream.truncate()
    
    # Kamera görüntüsünü yakala
    camera.capture(stream, format='jpeg')
    image_data = stream.getvalue()
    
    # Görüntüyü UDP ile gönder
    udp_socket.sendto(image_data, server_address)
    
    # Gönderilen görüntüyü yerel ekranda göster
    data = np.frombuffer(image_data, dtype=np.uint8)
    frame = cv2.imdecode(data, cv2.IMREAD_COLOR)
    cv2.imshow('Sending', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Kaynakları serbest bırak
camera.close()
cv2.destroyAllWindows()
udp_socket.close()
