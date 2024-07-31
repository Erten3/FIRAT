import socket
import dronekit
from dronekit import connect, VehicleMode, LocationGlobalRelative
import time
import argparse
from gtts import gTTS
import random
import os

gi.require_version('Gst', '1.0')
from gi.repository import Gst

class SesliAsistan:
    def __init__(self):
        Gst.init(None)

    def seslendirme(self, metin):
        xtts = gTTS(text=metin, lang="tr")
        dosya = "dosya" + str(random.randint(0, 123)) + ".mp3"
        xtts.save(dosya)

        # Play the audio file using GStreamer
        player = Gst.ElementFactory.make("playbin", "player")
        player.set_property("uri", f"file://{os.path.abspath(dosya)}")
        player.set_state(Gst.State.PLAYING)

        # Wait for the audio to finish playing
        bus = player.get_bus()
        msg = bus.timed_pop_filtered(Gst.CLOCK_TIME_NONE, Gst.MessageType.EOS)

        # Clean up
        player.set_state(Gst.State.NULL)
        os.remove(dosya)



def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('192.168.212.105', 9999))  # Raspberry Pi'nin IP'si ve port numarası
    server_socket.listen(1)
    print('Server is listening on port 9999')
    
    while True:
        client_socket, addr = server_socket.accept()
        print(f'Connection from {addr}')
        message = client_socket.recv(1024).decode('utf-8')
        print(f'Received message: {message}')
        print("Message received")
        if message == '15':

            takeoff(6)
            # Set the target location in global-relative frame
            a_location = LocationGlobalRelative(-34.364114, 149.166022, 6)  # buradaki değerler değişiyor
            vehicle.simple_goto(a_location)
            print("Sent vehicle to new location")
            # Start the voice assistant
            sesli_asistan = SesliAsistan()

            end_time = time.time() + 15  # 5 saniye boyunca döngü
            while time.time() < end_time:
                sesli_asistan.seslendirme("Buradan uzaklas")
                time.sleep(3)  # 5 saniye arayla sesli mesajlar gönder

            vehicle.mode = VehicleMode("RTL")
        client_socket.close()
def takeoff(irtifa):
    while vehicle.is_armable is not True:
        print("İHA arm edilebilir durumda değil.")
        time.sleep(1)


    print("İHA arm edilebilir.")

    vehicle.mode = VehicleMode("GUIDED")

    vehicle.armed = True
    vehicle.airspeed = 2

    while vehicle("İHA arm ediliyor..."):
        time.sleep(0.5)

    print("İHA arm edildi.")

    vehicle.simple_takeoff(irtifa)
    
    while vehicle.location.global_relative_frame.alt < irtifa * 0.9:
        print("İha hedefe yükseliyor.")
        time.sleep(1)


def connectMyPlane():
    # Simülasyonun bağlantısı
    parser = argparse.ArgumentParser(description='commands')
    parser.add_argument('--connect', default='tcp:127.0.0.1:5762')
    args = parser.parse_args()

    connection_string = args.connect
    baud_rate = 57600

    print(f'Connecting to vehicle on: {connection_string}')
    vehicle = connect(connection_string, baud=baud_rate, wait_ready=True)
    return vehicle
if __name__ == '__main__':
    vehicle = connectMyPlane()
    try:
        start_server()
    except KeyboardInterrupt:
        print("User interrupted, exiting...")
    finally:
        vehicle.close()
