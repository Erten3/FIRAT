import socket
import cv2
import numpy as np
from pymavlink import mavutil
import struct
import threading
import time

# UDP ayarları
udp_send_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp_send_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_address = ('192.168.1.10', 5005)  # Yer istasyonu PC'nin IP adresi

udp_recv_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp_recv_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
udp_recv_socket.bind(('0.0.0.0', 5006))  # Raspberry Pi'nin dinleyeceği port

# Pixhawk bağlantısı
port = '/dev/ttyACM0'
baud_rate = 115200
master = mavutil.mavlink_connection(port, baud=baud_rate)
master.wait_heartbeat()
print("Heartbeat received")

# OpenCV ile kamera açma
cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

CHUNK_SIZE = 65000
FPS = 10  # Video gönderim hızı (FPS)
FRAME_DELAY = 1 / FPS

def send_telemetry_and_video():
    while True:
        start_time = time.time()
        ret, frame = cap.read()
        if not ret:
            continue
        
        encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]
        result, img_encoded = cv2.imencode('.jpg', frame, encode_param)
        image_data = img_encoded.tobytes()
        
        msg = master.recv_match(type='GLOBAL_POSITION_INT', blocking=True)
        if msg:
            lat = msg.lat / 1e7
            lon = msg.lon / 1e7
            alt = msg.alt / 1e3
            
            telemetry_data = struct.pack('!ddd', lat, lon, alt)
            
            data = telemetry_data + image_data
        
            for i in range(0, len(data), CHUNK_SIZE):
                udp_send_socket.sendto(data[i:i+CHUNK_SIZE], server_address)
        
        cv2.imshow('Sending', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        
        # FPS kontrolü için bekleme süresi
        elapsed_time = time.time() - start_time
        time.sleep(max(0, FRAME_DELAY - elapsed_time))

    cap.release()
    cv2.destroyAllWindows()
    udp_send_socket.close()

def receive_commands():
    while True:
        try:
            data, addr = udp_recv_socket.recvfrom(1024)
            command = data.decode()
            print(f"Received command: {command}")
            
            # Gelen komutu işleyin
            # Bu bölümde gelen komutları işleyebilirsiniz

        except Exception as e:
            print(f"Error: {e}")
            break

# Komut alma işlevini paralel olarak çalıştır
command_thread = threading.Thread(target=receive_commands)
command_thread.start()

# Telemetri ve video gönderim işlevini paralel olarak çalıştır
send_telemetry_and_video()