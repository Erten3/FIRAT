import time
import cv2
from gtts import gTTS
import random
import os
import threading
from ultralytics import YOLO
import gi
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

gi.require_version('Gst', '1.0')
from gi.repository import Gst

class firatframe():
    def __init__(self):
        self.kamera = cv2.VideoCapture("/dev/video1")
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

        fig, ax = plt.subplots()
        fig.suptitle('FIRAT')  # Set the window title
        im = ax.imshow(np.zeros((480, 640, 3), dtype=np.uint8))

        def update(frame):
            ret, frame = cap.read()
            if not ret:
                return im,

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
                    self.last_detection_time = int(current_time)
                    threading.Thread(target=self.asistan.seslendirme, args=("Kiþi tespit edildi.",)).start()
            else:
                self.detected = False

            # Convert BGR to RGB
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            im.set_array(frame)
            return im,

        ani = FuncAnimation(fig, update, blit=True)
        plt.show()

        cap.release()

class SesliAsistan():
    def __init__(self):
        Gst.init(None)

    def seslendirme(self, metin):
        xtts = gTTS(text=metin, lang="tr")
        dosya = "dosya" + str(random.randint(0, 123)) + ".mp3"
        xtts.save(dosya)
        
        # Play the audio file using GStreamer
        player = Gst.ElementFactory.make("playbin", "player")
        player.set_property("uri", f"file://{os.path.abspath(dosya)}")
        player.set_state(Gst.State.PLAYING)
        
        # Wait for the audio to finish playing
        bus = player.get_bus()
        msg = bus.timed_pop_filtered(Gst.CLOCK_TIME_NONE, Gst.MessageType.EOS)
        
        # Clean up
        player.set_state(Gst.State.NULL)
        os.remove(dosya)

if __name__ == "__main__":
    kamera_cercevele = firatframe()
    kamera_cercevele.baslat()
