import socket
import cv2
import numpy as np

# OpenCV kullanarak harici kamerayı aç
cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

# UDP soketi oluştur ve hedef adresi ayarla
udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_address = ('192.168.1.10', 5005)

CHUNK_SIZE = 65000  # UDP paket boyut limiti

while True:
    ret, frame = cap.read()
    if not ret:
        continue
    
    # Görüntüyü JPEG formatında sıkıştır
    encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]
    result, img_encoded = cv2.imencode('.jpg', frame, encode_param)
    image_data = img_encoded.tobytes()
    
    # Görüntü verisini parçalara bölerek gönder
    for i in range(0, len(image_data), CHUNK_SIZE):
        udp_socket.sendto(image_data[i:i+CHUNK_SIZE], server_address)
    
    # Gönderilen görüntüyü yerel ekranda göster
    cv2.imshow('Sending', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Kaynakları serbest bırak
cap.release()
cv2.destroyAllWindows()
udp_socket.close()
