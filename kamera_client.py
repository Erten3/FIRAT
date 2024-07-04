import socket
import cv2

# Sunucu bilgileri
HOST = '192.168.21.113'  # Sunucu bilgisayarın yerel IP adresi (Örneğin)
PORT = 9999

# Socket oluşturma
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))
print('Sunucuya bağlanıldı.')

# Kamera başlatma
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret: break

    # Görüntüyü JPEG formatına çevirme
    result, frame_encoded = cv2.imencode('.jpg', frame)
    data = frame_encoded.tobytes()
    frame_len = len(data)

    # Çerçeve uzunluğunu ve çerçeveyi gönderme
    client_socket.sendall(frame_len.to_bytes(4, byteorder='big') + data)

    cv2.imshow('Istemci - Gonderilen Goruntu', frame)
    if cv2.waitKey(1) == 27:  # ESC tuşuna basıldığında çık
        break

# Kaynakları serbest bırakma
cap.release()
client_socket.close()
cv2.destroyAllWindows()