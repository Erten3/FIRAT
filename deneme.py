from picamera2 import Picamera2
from libcamera import controls
import cv2

# Picamera2 ve libcamera ile kamera örneğini başlatma
picam2 = Picamera2()
picam2.start(show_preview=True)
picam2.set_controls({"AfMode": controls.AfModeEnum.Continuous})

# Kameradan görüntü almak için döngü başlatma
try:
    while True:
        # Kameradan bir kare yakalama
        frame = picam2.capture()

        # OpenCV ile kareyi işleme (örneğin, kareyi gri tonlama)
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # İşlenmiş kareyi ekranda gösterme
        cv2.imshow('Frame', gray_frame)

        # Çıkış için 'q' tuşuna basılmasını bekleyerek döngüden çıkma
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

finally:
    # Döngü sona erdiğinde kamerayı ve OpenCV penceresini kapatma
    picam2.stop()
    cv2.destroyAllWindows()
