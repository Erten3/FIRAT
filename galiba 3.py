from dronekit import connect, VehicleMode, LocationGlobalRelative
import time, math
from pymavlink import mavutil
import cv2
import threading

# Haar Cascade sınıflandırıcısını yükle
face_cascade = cv2.CascadeClassifier('/home/erten/haarcascade_frontalface_default.xml')

# Kamerayı başlat
cap = cv2.VideoCapture(0)

# Merkez konumu belirleyin (örneğin, 640x480 çözünürlük için)
frame_width = 640
frame_height = 480
center_x = frame_width // 2
center_y = frame_height // 2

# Hareket eşiği
move_threshold = 50

# BAĞLANMA KOMMUTU
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

def send_to(latitude, longitude, altitude):
    if vehicle.mode.name == "GUIDED":
        location = LocationGlobalRelative(latitude, longitude, float(altitude))
        vehicle.simple_goto(location)
        time.sleep(1)

def destination_location(homeLatitude, homeLongitude, distance, bearing):
    R = 6371e3
    rlat1 = homeLatitude * (math.pi / 180)
    rlon1 = homeLongitude * (math.pi / 180)
    d = distance
    bearing = bearing * (math.pi / 180)

    rlat2 = math.asin((math.sin(rlat1) * math.cos(d / R)) + (math.cos(rlat1) * math.sin(d / R) * math.cos(bearing)))
    rlon2 = rlon1 + math.atan2((math.sin(bearing) * math.sin(d / R) * math.cos(rlat1)), (math.cos(d / R) - (math.sin(rlat1) * math.sin(rlat2))))

    rlat2 = rlat2 * (180 / math.pi)
    rlon2 = rlon2 * (180 / math.pi)

    return [rlat2, rlon2]

def track_face():
    global vehicle
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Kamera hatası.")
            break
        
        resized_frame = cv2.resize(frame, (640, 480))
        gray = cv2.cvtColor(resized_frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

        if len(faces) > 0:
            (x, y, w, h) = faces[0]
            face_center_x = x + w // 2
            face_center_y = y + h // 2

            angle = int(vehicle.heading)
            loc = (vehicle.location.global_frame.lat, vehicle.location.global_frame.lon, vehicle.location.global_relative_frame.alt)
            default_distance = 5

            if face_center_x > center_x + move_threshold:
                right = angle + 90
                new_loc = destination_location(homeLatitude=loc[0], homeLongitude=loc[1], distance=default_distance, bearing=right)
                send_to(new_loc[0], new_loc[1], loc[2])
            elif face_center_x < center_x - move_threshold:
                left = angle - 90
                new_loc = destination_location(homeLatitude=loc[0], homeLongitude=loc[1], distance=default_distance, bearing=left)
                send_to(new_loc[0], new_loc[1], loc[2])

            if face_center_y > center_y + move_threshold:
                back = angle + 180
                new_loc = destination_location(homeLatitude=loc[0], homeLongitude=loc[1], distance=default_distance, bearing=back)
                send_to(new_loc[0], new_loc[1], loc[2])
            elif face_center_y < center_y - move_threshold:
                front = angle
                new_loc = destination_location(homeLatitude=loc[0], homeLongitude=loc[1], distance=default_distance, bearing=front)
                send_to(new_loc[0], new_loc[1], loc[2])
        
        cv2.imshow('Yüz Takip', resized_frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

def control_drone():
    global vehicle
    try:
        while True:
            if not cap.isOpened():
                print("Kamera kapalı. Drone iniyor...")
                vehicle.mode = VehicleMode("LAND")
                vehicle.armed = False
                vehicle.close()
                break
            time.sleep(1)
    except KeyboardInterrupt:
        print("Kontrol durduruldu.")
    finally:
        if vehicle.armed:
            print("Drone'u güvenli bir şekilde indiriyorum...")
            vehicle.mode = VehicleMode("LAND")
            vehicle.armed = False
            vehicle.close()

try:
    takeoff(5)
    time.sleep(5)

    # Threadler oluştur
    face_tracking_thread = threading.Thread(target=track_face)
    control_thread = threading.Thread(target=control_drone)

    # Threadleri başlat
    face_tracking_thread.start()
    control_thread.start()

    # Threadlerin bitmesini bekle
    face_tracking_thread.join()
    control_thread.join()

except Exception as e:
    print(f"Bir hata oluştu: {e}")
    if vehicle.armed:
        print("Hata nedeniyle drone'u indiriyorum...")
        vehicle.mode = VehicleMode("LAND")
        vehicle.armed = False
        vehicle.close()
finally:
    cap.release()
    cv2.destroyAllWindows()
