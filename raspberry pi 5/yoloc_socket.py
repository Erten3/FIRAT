import cv2
import socket
import struct
import pickle
import threading
import time
import random
from gtts import gTTS
from playsound import playsound
import os
from ultralytics import YOLO

class firatframe():
    def __init__(self):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect(('localhost', 8000))
        self.payload_size = struct.calcsize("Q")
        self.thread = threading.Thread(target=self.modelkamera)
#         self.asistan = SesliAsistan()
        self.detected = False
        self.last_detection_time = 0
        self.cooldown_period = 5  # seconds

    def baslat(self):
        self.thread.start()

    def modelkamera(self):
        model = YOLO("yolov8n.pt")
        class_names = model.names

        while True:
            data = b""
            while len(data) < self.payload_size:
                packet = self.client_socket.recv(4*1024)
                if not packet:
                    break
                data += packet

            packed_msg_size = data[:self.payload_size]
            data = data[self.payload_size:]
            msg_size = struct.unpack("Q", packed_msg_size)[0]

            while len(data) < msg_size:
                packet = self.client_socket.recv(4*1024)
                if not packet:
                    break
                data += packet

            frame_data = data[:msg_size]
            data = data[msg_size:]

            frame = pickle.loads(frame_data)

            results = model.predict(frame)
            person_detected = False

            for result in results:
                boxes = result.boxes.xyxy
                scores = result.boxes.conf
                classes = result.boxes.cls

                for box, score, cls in zip(boxes, scores, classes):
                    label = class_names[int(cls)]
                    x1, y1, x2, y2 = map(int, box)

                    if label == "person" and score >= 0.5:
                        person_detected = True
                        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                        cv2.putText(frame, f'{label} {score:.2f}', (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

            current_time = float(time.time())
            if person_detected:
                if not self.detected or (current_time - self.last_detection_time) > self.cooldown_period:
                    self.detected = True
                    self.last_detection_time = current_time
                    threading.Thread(target=self.asistan.seslendirme, args=("Kişi tespit edildi.",)).start()
            else:
                self.detected = False

            cv2.imshow('FIRAT', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        self.client_socket.close()
        cv2.destroyAllWindows()

class SesliAsistan():
    def __init__(self):
        pass

    def seslendirme(self, metin):
        xtts = gTTS(text=metin, lang="tr")
        dosya = "dosya" + str(random.randint(0, 123)) + ".mp3"
        xtts.save(dosya)
        playsound(dosya)
        os.remove(dosya)

if __name__ == "__main__":
    kamera_cercevele = firatframe()
    kamera_cercevele.baslat()
