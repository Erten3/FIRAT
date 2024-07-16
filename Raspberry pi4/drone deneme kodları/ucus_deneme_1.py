from dronekit import Command, connect, VehicleMode, LocationGlobalRelative
import time
from pymavlink import mavutil

firat = connect('/dev/ttyACM0', wait_ready=True, baud=115200)


def takeoff(irtifa):
    while firat.is_armable is not True:
        print("İHA arm edilebilir durumda değil.")
        time.sleep(1)

    print("İHA arm edilebilir.")

    firat.mode = VehicleMode("GUIDED")

    firat.armed = True
    firat.airspeed = 5

    while firat.armed is not True:
        print("İHA arm ediliyor...")
        time.sleep(0.5)

    print("İHA arm edildi.")

    firat.simple_takeoff(irtifa)

    while firat.location.global_relative_frame.alt < irtifa * 0.9:
        print("İha hedefe yükseliyor.")
        time.sleep(1)


takeoff(2)

time.sleep(5)

firat.mode = VehicleMode("RTL")