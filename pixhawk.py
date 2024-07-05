import sys
from dronekit import connect, VehicleMode
import argparse
import time
import socket

# PC'nin IP adresi ve port numarası
PC_IP = "192.168.172.243"  # Buraya PC'nin IP adresini yazın
PC_PORT = 5005

# UDP soketi oluşturma
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

def connectMyPlane():
    parser = argparse.ArgumentParser(description='commands')
    # parser.add_argument('--connect', default='tcp:127.0.0.1:5762')
    parser.add_argument('--connect', default='/dev/ttyACM0')
    args = parser.parse_args()
    connection_string = args.connect
    baud_rate = 57600
    vehicle = connect(connection_string, baud=baud_rate, wait_ready=True)
    try:
        while True:
            message = "Merhaba, bu bir test mesajıdır."
            sock.sendto(message.encode(), (PC_IP, PC_PORT))
            print(f"Mesaj gönderildi: {message}")
            time.sleep(1)  # Mesaj gönderim aralığı (1 saniye)
    except KeyboardInterrupt:
        print("Gönderim durduruldu.")
    finally:
        sock.close()
    print("worked")
    return vehicle

def function():
    vehicle = connectMyPlane()
    vehicle.mode = VehicleMode("AUTO")
    # vehicle.armed = True
    # wb = Workbook()
    # ws = wb.active
    # ws.delete_rows(1, ws.max_row)
    # ws.title = "DATA"
    # ws["A1"] = "SANİYE"
    # ws["B1"] = "HIZ"
    # ws["C1"] = "ALTİTUDE"
    # ws["D1"] = "PİTCH"
    # ws["E1"] = "ROLL"
    # ws["F1"] = "YAW"
    # ws["G1"] = "BATARYA SEVİYESİ"
    # ws["H1"]= "LATİTUDE"
    # ws["I1"]= "LONGİTUDE"
    saniye = 0
    while True:
        saniye = saniye + 1
        airspeed = vehicle.airspeed
        altitude = vehicle.location.global_relative_frame.alt
        batarya_seviye = vehicle.battery.level
        attitude = vehicle.attitude
        latitude=vehicle.location.global_frame.lat
        longitude=vehicle.location.global_relative_frame.lon
        # ws.append([saniye, airspeed, altitude, attitude.pitch, attitude.roll, attitude.yaw, batarya_seviye,latitude,longitude])
        # wb.save("data.xlsx")
        time.sleep(1)

if __name__ == "__main__":
    print("Started")
    function()
    
