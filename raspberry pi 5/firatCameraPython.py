import time
import socket
import cv2

def connectCamera():
    # Kamera bağlantısı
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Kamera bağlanamadı")
        return None, None

    # Sunucu bilgileri
    host = '0.0.0.0'
    port = 9999 

    # Soket oluştur
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(1)

    print("Sunucu başlatıldı, bağlantı bekleniyor...")

    # Bağlantı kabul et
    conn, addr = server_socket.accept()
    print(f"Bağlantı kabul edildi: {addr}")

    return conn, cap


def main():

    # Kamera bağlantısı
    camera, cap = connectCamera()
    
    while True:

        ret, frame = cap.read()
 
        # Görüntüyü JPEG formatına dönüştür
        _, buffer = cv2.imencode('.jpg', frame, [int(cv2.IMWRITE_JPEG_QUALITY), 90])

        # Görüntüyü baytlara çevir
        data = buffer.tobytes()

        # Görüntü boyutunu gönder
        size = len(data)

        # Değişebilir. Görüntü gelmiyorsa "big" yap. !!!!!!!
        camera.sendall(size.to_bytes(4, byteorder='little'))
 
        # Görüntü verisini gönder
        camera.sendall(data) 
        
        # 30 milisaniye bekle (30fps)
        time.sleep(0.03)
    

if __name__ == "__main__":
    main()
