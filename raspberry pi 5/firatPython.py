import mysql.connector
from mysql.connector import Error
import random
import time
import sys
from dronekit import connect, VehicleMode
import argparse
import numpy as np

def connectMyPlane():
    try:
        parser = argparse.ArgumentParser(description='commands')
        #parser.add_argument('--connect', default='tcp:127.0.0.1:5762')
        #raspberry haberleşmesi
        parser.add_argument('--connect', default='/dev/ttyACM0')

        #parser.add_argument('--connect', default="COM5")
        args = parser.parse_args()

        connection_string = args.connect
        baud_rate = 57600
        vehicle = connect(connection_string, baud=baud_rate, wait_ready=True)
        print("Uçak Başarıyla Bağlandı.")
    except Error as e:
        print(f"'{e}' Hatası Oluştu!!")
    return vehicle

    
def create_connection(host_name, user_name, user_password, db_name):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password,
            database=db_name
        )
        print("MySQL Veri Tabanı başarıyla bağlandı.")
    except Error as e:
        print(f"'{e}' Hatası Oluştu!!")
    return connection

def execute_query(connection, query, data):
    cursor = connection.cursor()
    try:
        cursor.execute(query, data)
        connection.commit()
        #print("Query executed successfully")
    except Error as e:
        print(f"'{e}' Hatası Oluştu!!")


def main():
    # Uçak bağlantısı
    #vehicle = connectMyPlane()

    # Uçak modu
    #vehicle.mode = VehicleMode("AUTO")
    #vehicle.armed = True
   
    # Veritabanı bağlantısı
    connection = create_connection("localhost", "root", "Firat1234_2024*", "deneme")   
    # Tabloyu temizle
    truncate_query = "TRUNCATE TABLE fw_uav"
    execute_query(connection, truncate_query, None)

    while True:
        # Rastgele veri oluşturma
        current_time = time.strftime('%Y-%m-%d %H:%M:%S')
        airspeed = random.randint(1, 100)
        altitude = random.randint(1, 100)
        battery = random.randint(1, 100)
        latitude = random.uniform(-90.0,90.0)
        longitude = random.uniform(-180.0,180.0)

        ## Canlı Uçak verileri alınıyor
        airspeed = vehicle.airspeed
        altitude = vehicle.location.global_relative_frame.alt
        battery = vehicle.battery.level
        attitude = vehicle.attitude
        latitude = vehicle.location.global_frame.lat
        longitude =   vehicle.location.global_relative_frame.lon
    
        # Veri ekleme sorgusu
        insert_query = """
        INSERT INTO fw_uav (FW_UAV_time, FW_UAV_velocity, FW_UAV_altitude, FW_UAV_battery, FW_UAV_latitude, FW_UAV_longitude)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        data = (current_time, airspeed, altitude, battery, latitude, longitude)

        # Veriyi ekleme
        execute_query(connection, insert_query, data)
        
        # 1.2 saniye bekle
        time.sleep(1.2)
    

if __name__ == "__main__":
    main()