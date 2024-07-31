import socket
import threading
from ultralytics import YOLO
import cv2

# YOLOv8 modelini yükle
model = YOLO("yolov8n.pt")

def send_message_to_rpi(message):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    rpi_ip = '192.168.212.105'  # Raspberry Pi'nin IP adresi
    rpi_port = 9999  # Raspberry Pi üzerinde sunucu kodunda belirtilen port numarası
    
    client_socket.connect((rpi_ip, rpi_port))
    client_socket.sendall(message.encode('utf-8'))
    client_socket.close()

def detect_person():
    cap = cv2.VideoCapture("http://192.168.212.177:8080/video")  # IP kamera kullanarak görüntü yakalama

    person_detected = False  # İlk insan tespit edilene kadar False olarak başlat

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to capture frame")
            break
        frame = cv2.resize(frame, (640, 480))
        results = model(frame)
        
        current_person_detected = False

        for result in results:
            boxes = result.boxes.xyxy
            classes = result.boxes.cls

            for box, cls in zip(boxes, classes):
                if cls == 0:  # '0' sınıfı, insan sınıfıdır
                    x1, y1, x2, y2 = map(int, box)
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)  # Kare içine alma
                    current_person_detected = True

        # Eğer insan tespit edilirse ve daha önce tespit edilmemişse, mesaj gönder
        if current_person_detected and not person_detected:
            threading.Thread(target=send_message_to_rpi, args=('15',)).start()
            print('Person detected and message sent to Raspberry Pi')
            person_detected = True  # Bir kez tespit edildikten sonra bayrağı güncelle

        # Eğer insan tespit edilmezse, bayrağı sıfırla
        if not current_person_detected:
            person_detected = False

        cv2.imshow('Frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    detect_person()
