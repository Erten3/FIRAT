import time
from pymavlink import mavutil

# Pixhawk'a bağlanacak olan seri portu belirleyin
port = '/dev/ttyACM0'  # Bu port, bağlı olan Pixhawk'ın portu olabilir. Bunu 'dmesg | grep tty' komutuyla kontrol edebilirsiniz.
baud_rate = 115200     # Pixhawk'ın standart baud rate değeri

# MAVLink bağlantısını başlatın
master = mavutil.mavlink_connection(port, baud=baud_rate)

# Heartbeat mesajı alana kadar bekleyin
master.wait_heartbeat()
print("Heartbeat received")

# Telemetri verilerini sürekli olarak al ve ekrana yazdır
while True:
    try:
        # Yeni bir MAVLink mesajı bekleyin
        msg = master.recv_match(blocking=True)
        
        if msg:
            # Global konum mesajını işleyin
            if msg.get_type() == 'GLOBAL_POSITION_INT':
                lat = msg.lat / 1e7
                lon = msg.lon / 1e7
                alt = msg.alt / 1e3
                print(f"Latitude: {lat}, Longitude: {lon}, Altitude: {alt} meters")
            
            # Altitude mesajını işleyin
            elif msg.get_type() == 'ALTITUDE':
                alt = msg.alt / 1e3
                print(f"Altitude: {alt} meters")
                
            # Diğer mesaj tiplerini burada ekleyebilirsiniz
            # Örneğin: 'VFR_HUD', 'ATTITUDE', vb.

    except KeyboardInterrupt:
        print("Program terminated")
        break