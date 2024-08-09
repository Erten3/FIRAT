import socket
import struct
import pickle
import time
from picamera2 import Picamera2
from libcamera import controls

# Kamera akışını başlat
picam2 = Picamera2()
picam2.start(show_preview=True)
picam2.set_controls({"AfMode": controls.AfModeEnum.Continuous})

# Socket oluştur
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('0.0.0.0', 8000))
server_socket.listen(1)
print("Waiting for a connection...")

conn, addr = server_socket.accept()
print(f"Connection from: {addr}")

while True:
    frame = picam2.capture_array()

    data = pickle.dumps(frame)
    message_size = struct.pack("L", len(data))
    conn.sendall(message_size + data)

    time.sleep(0.1)  # Biraz bekleme süresi ekleyerek akışı düzenleyin

conn.close()
server_socket.close()
