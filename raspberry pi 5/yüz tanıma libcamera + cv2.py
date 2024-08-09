import cv2
from picamera2 import Picamera2
from libcamera import controls

# Picamera2 ile kamera başlatma
picam2 = Picamera2()
picam2.start(show_preview=True)
picam2.set_controls({"AfMode": controls.AfModeEnum.Manual, "LensPosition": 0.5})

# Haarcascades yüz algılama modelinin XML dosyasının yolu
haarcascade_path = '/home/FIRAT/Downloads/haarcascade_frontalface_default.xml'

# OpenCV'nin Haarcascades yüz algılama modelini yükleme
face_cascade = cv2.CascadeClassifier(haarcascade_path)

try:
    while True:
        # Kameradan görüntüyü alma
        frame = picam2.capture_array()

        # RGB'den BGR'ye dönüşüm
        bgr_frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

        # Gri tonlama dönüşümü
        gray = cv2.cvtColor(bgr_frame, cv2.COLOR_BGR2GRAY)

        # Yüz algılama
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

        # Algılanan yüzleri çerçeve içine alma
        for (x, y, w, h) in faces:
            cv2.rectangle(bgr_frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

        # Görüntüyü gösterme
        cv2.imshow('Face Detection', bgr_frame)

        # 'q' tuşuna basarak çıkma
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

finally:
    # İş bittiğinde kamerayı durdurma ve pencereleri kapatma
    picam2.stop()
    cv2.destroyAllWindows()
