from dronekit import connect, VehicleMode, LocationGlobalRelative
import time
from pymavlink import mavutil

firat = connect('127.0.0.1:14550',wait_ready=True)


def takeoff(irtifa):
    while firat.is_armable is not True:
        print("İHA arm edilebilir durumda değil.")
        time.sleep(1)


    print("İHA arm edilebilir.")

    firat.mode = VehicleMode("GUIDED")

    firat.armed = True

    while firat.armed is not True:
        print("İHA arm ediliyor...")
        time.sleep(0.5)

    print("İHA arm edildi.")

    firat.simple_takeoff(irtifa)
    
    while firat.location.global_relative_frame.alt < irtifa * 0.9:
        print("İha hedefe yükseliyor.")
        time.sleep(1)
    

def gorev(kuzey, dogu, irtifa):

    msg = firat.message_factory.set_position_target_local_ned_encode(
        0,       
        0, 0,    
        mavutil.mavlink.MAV_FRAME_BODY_OFFSET_NED , 
        0b0000111111111000, 
        kuzey, dogu, irtifa, 
        0, 0, 0,
        0, 0, 0,
        0, 0)    
    firat.send_mavlink(msg)
    firat.groundspeed = 3
    time.sleep(10)


takeoff(6)

gorev(10,0,0)

gorev(-10,0,0)

firat.mode = VehicleMode("RTL")