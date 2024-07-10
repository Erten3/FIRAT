import time
import cv2
import numpy as np
from gtts import gTTS
import random
from playsound import playsound
import os
import threading
from ultralytics import YOLO

class firatframe():
    def __init__(self):
        self.kamera = cv2.VideoCapture(0)
        self.asistan = SesliAsistan()
        self.thread = threading.Thread(target=self.modelkamera)
        self.detected = False
        self.last_detection_time = 0
        self.cooldown_period = 5  # seconds

    def baslat(self):
        self.thread.start()

    def modelkamera(self):
        model = YOLO("yolov8n.pt")
        cap = cv2.VideoCapture(0)
        class_names = model.names

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

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
                        cv2.putText(frame, f'{label} {score:.2f}', (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9,
                                    (0, 255, 0), 2)

            current_time = time.time()
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

        cap.release()
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
