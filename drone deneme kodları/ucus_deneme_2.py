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
    

def sol(heading):
    msg = firat.message_factory.command_long_encode(
        0, 0,    # target_system, target_component
        mavutil.mavlink.MAV_CMD_CONDITION_YAW, #command
        0, #confirmation
        heading,    # param 1, yaw in degrees
        0,          # param 2, yaw speed deg/s
        -1,          # param 3, direction -1 ccw, 1 cw
        1, # param 4, relative offset 1, absolute angle 0
        0, 0, 0)    # param 5 ~ 7 not used
    # send command to vehicle
    firat.send_mavlink(msg)
    time.sleep(3)


def sag(heading):
    msg = firat.message_factory.command_long_encode(
        0, 0,    # target_system, target_component
        mavutil.mavlink.MAV_CMD_CONDITION_YAW, #command
        0, #confirmation
        heading,    # param 1, yaw in degrees
        0,          # param 2, yaw speed deg/s
        1,          # param 3, direction -1 ccw, 1 cw
        1, # param 4, relative offset 1, absolute angle 0
        0, 0, 0)    # param 5 ~ 7 not used
    # send command to vehicle
    firat.send_mavlink(msg)
    time.sleep(3)

takeoff(6)

time.sleep(5)

sol(90)

time.sleep(10)

sag(90)

time.sleep(5)

firat.mode = VehicleMode("RTL")