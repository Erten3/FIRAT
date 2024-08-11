from dronekit import connect, VehicleMode
import time
from pymavlink import mavutil
import cv2
import threading

# Haar Cascade sınıflandırıcısını yükle
face_cascade = cv2.CascadeClassifier('/home/erten/haarcascade_frontalface_default.xml')

# Kamerayı başlat
cap = cv2.VideoCapture(0)

# Merkez konumu belirleyin (örneğin, 320x240 çözünürlük için)
frame_width = 320
frame_height = 240
center_x = frame_width // 2
center_y = frame_height // 2

# 9 eşit kareye bölme
grid_size = 3
cell_width = frame_width // grid_size
cell_height = frame_height // grid_size

# BAĞLANMA KOMUTU
vehicle = connect('127.0.0.1:14550', wait_ready=True)

# KALKIŞ FONKSİYONU
def takeoff(irtifa):
    while not vehicle.is_armable:
        print("İHA arm edilebilir durumda değil.")
        time.sleep(1)

    print("İHA arm edilebilir.")

    vehicle.mode = VehicleMode("GUIDED")
    vehicle.armed = True

    while not vehicle.armed:
        print("İHA arm ediliyor...")
        time.sleep(0.5)
    print("İHA arm edildi.")

    vehicle.simple_takeoff(irtifa)
    
    while vehicle.location.global_relative_frame.alt < irtifa * 0.9:
        print("İHA hedefe yükseliyor.")
        time.sleep(1)


def set_velocity_body(vx, vy, vz):
    """
    Dronu vücut çerçevesinde (ön, sağ, yukarı) hareket ettirir.
    vx: İleri/geri hız (metre/saniye)
    vy: Sağ/sol hız (metre/saniye)
    vz: Yukarı/aşağı hız (metre/saniye)
    """
    msg = vehicle.message_factory.set_position_target_local_ned_encode(
        0,       # Zaman damgası (geçerli kullanılmaz)
        0, 0,    # Hedef sistemi ve bileşeni
        mavutil.mavlink.MAV_FRAME_BODY_NED,  # Hedef çerçeve
        0b0000111111000111,  # Sadece hızları kontrol et
        0, 0, 0,  # Konum (kullanılmıyor)
        vx, vy, vz,  # Hızlar
        0, 0, 0,  # Hızlanma (kullanılmıyor)
        0, 0)    # Yaw ve yaw oranı (kullanılmıyor)
    vehicle.send_mavlink(msg)
    vehicle.flush()


def process_frame(stop_event):
    global face_center_x, face_center_y
    while not stop_event.is_set():
        ret, frame = cap.read()
        if not ret:
            print("Kamera bağlantısı kesildi.")
            stop_event.set()
            break

        resized_frame = cv2.resize(frame, (frame_width, frame_height))
        gray = cv2.cvtColor(resized_frame, cv2.COLOR_BGR2GRAY)
        
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
        if len(faces) > 0:
            (x, y, w, h) = faces[0]
            face_center_x = x + w // 2
            face_center_y = y + h // 2
        
        # 9 eşit kareye bölme
        for i in range(1, grid_size):
            cv2.line(resized_frame, (i * cell_width, 0), (i * cell_width, frame_height), (0, 255, 0), 1)
            cv2.line(resized_frame, (0, i * cell_height), (frame_width, i * cell_height), (0, 255, 0), 1)

        cv2.imshow('Yüz Takip', resized_frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            stop_event.set()
            break


def control_drone(stop_event):
    global face_center_x, face_center_y
    while not stop_event.is_set():
        if 'face_center_x' in globals() and 'face_center_y' in globals():
            if face_center_x > center_x + 20:
                set_velocity_body(0, -1, 0)
                time.sleep(0.3)
                set_velocity_body(0, 0, 0)   
            elif face_center_x < center_x - 20:
                set_velocity_body(0, 1, 0)
                time.sleep(0.3)
                set_velocity_body(0, 0, 0)

            if face_center_y > center_y + 20:
                set_velocity_body(-1, 0, 0)
                time.sleep(0.3)
                set_velocity_body(0, 0, 0)
            elif face_center_y < center_y - 20:
                set_velocity_body(1, 0, 0)
                time.sleep(0.3)
                set_velocity_body(0, 0, 0)


takeoff(5)
time.sleep(5)

stop_event = threading.Event()

try:
    face_center_x = center_x
    face_center_y = center_y

    frame_thread = threading.Thread(target=process_frame, args=(stop_event,))
    control_thread = threading.Thread(target=control_drone, args=(stop_event,))

    frame_thread.start()
    control_thread.start()

    frame_thread.join()
    control_thread.join()

finally:
    cap.release()
    cv2.destroyAllWindows()
    if vehicle:
        vehicle.mode = VehicleMode("LOITER")  # Hareketi durdurur ve yerde kalır
        time.sleep(2)
        print("Hareket durduruldu. İniş yapılıyor...")
        vehicle.mode = VehicleMode("LAND")
        vehicle.close()
