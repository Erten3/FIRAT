import cv2

# Kamera bağlantısını başlatma
cap = cv2.VideoCapture(0)  # 0, varsayılan kamerayı temsil eder (bilgisayarınızda birden fazla kamera varsa 0, 1, 2, ... şeklinde değiştirerek diğer kameraları seçebilirsiniz)

# Kamera bağlantısını kontrol etme
if not cap.isOpened():
    print("Kamera açılamadı. Lütfen bağlantıyı kontrol edin.")
    exit()

# Kamera görüntüsünü yakalama ve gösterme
while True:
    ret, frame = cap.read()  # frame, kameradan alınan her kareyi temsil eder
    if not ret:
        print("Kare alınamadı. Çıkış yapılıyor...")
        break
    
    # Alınan kareyi ekranda gösterme
    cv2.imshow('Kamera', frame)

    # Kullanıcı 'q' tuşuna basarsa çık
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# İşlem sonunda, kamera bağlantısını serbest bırak
cap.release()

# Tüm pencereleri kapat
cv2.destroyAllWindows()