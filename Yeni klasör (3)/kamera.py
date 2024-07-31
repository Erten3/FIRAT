import cv2

# Kamera nesnesini oluştur
# 0, bilgisayara bağlı olan varsayılan kamerayı temsil eder
cap = cv2.VideoCapture("http://192.168.21.159:8080/video")

if not cap.isOpened():
    print("Kamera açılamadı")
    exit()

while True:
    # Kameradan bir kare oku
    ret, frame = cap.read()

    if not ret:
        print("Kare alınamadı")
        break

    # Görüntüyü ekranda göster
    cv2.imshow('Kamera', frame)

    # 'q' tuşuna basıldığında döngüden çık
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Kaynakları serbest bırak
cap.release()
cv2.destroyAllWindows()
