import cv2

# OpenCV kullanarak kamera modülünü aç
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Kamera açılamadı")
else:
    print("Kamera başarıyla açıldı")

while True:
    ret, frame = cap.read()
    if ret:
        cv2.imshow('Test', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()